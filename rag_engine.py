import io
import numpy as np
import faiss
from pypdf import PdfReader
from google import genai

EMBED_MODEL = "gemini-embedding-001"
GEN_MODEL = "gemini-3.8-flash"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4


def extract_pdf_pages(pdf_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = " ".join(text.split())
        if text:
            pages.append({"page": page_number, "text": text})
    if not pages:
        raise ValueError("No readable text was found. The PDF may be scanned; OCR is not included.")
    return pages


def split_pages(pages, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    for item in pages:
        text = item["text"]
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            piece = text[start:end].strip()
            if piece:
                chunks.append({"page": item["page"], "text": piece})
            if end == len(text):
                break
            start = max(end - overlap, start + 1)
    return chunks


def embed_texts(client, texts):
    vectors = []
    # Small batches reduce the chance of oversized API requests.
    for start in range(0, len(texts), 32):
        batch = texts[start:start + 32]
        response = client.models.embed_content(
            model=EMBED_MODEL,
            contents=batch,
            config={"output_dimensionality": 768},
        )
        vectors.extend([item.values for item in response.embeddings])
    array = np.asarray(vectors, dtype="float32")
    faiss.normalize_L2(array)
    return array


def build_manual_index(pdf_bytes, api_key):
    client = genai.Client(api_key=api_key)
    pages = extract_pdf_pages(pdf_bytes)
    chunks = split_pages(pages)
    vectors = embed_texts(client, [chunk["text"] for chunk in chunks])
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return {"index": index, "chunks": chunks}, len(chunks)


def answer_question(question, vector_store, api_key):
    client = genai.Client(api_key=api_key)
    query_vector = embed_texts(client, [question])
    scores, indices = vector_store["index"].search(query_vector, min(TOP_K, len(vector_store["chunks"])))

    selected = []
    seen = set()
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue
        chunk = vector_store["chunks"][int(idx)]
        key = (chunk["page"], chunk["text"])
        if key not in seen:
            seen.add(key)
            selected.append({**chunk, "score": float(score)})

    context = "\n\n".join(
        f"[Page {item['page']}]\n{item['text']}" for item in selected
    )
    prompt = f"""
You are a careful appliance-manual assistant.
Answer the user's question using ONLY the supplied manual excerpts.
If the excerpts do not contain the answer, clearly say:
"I couldn't find this information in the uploaded manual."
Do not invent error-code meanings, procedures, part names, or specifications.
For troubleshooting, provide clear numbered steps in plain language.
Include a safety warning whenever the manual indicates a hazard or the task
could involve electricity, gas, heat, moving parts, water, or disassembly.
Never instruct the user to bypass safety devices or work on live electrical parts.
End with a "Source pages:" line listing the page numbers used.
Distinguish manual instructions from any general caution.

MANUAL EXCERPTS:
{context}

USER QUESTION:
{question}
"""
    response = client.models.generate_content(
        model=GEN_MODEL,
        contents=prompt,
        config={"temperature": 0.2, "max_output_tokens": 900},
    )
    sources = []
    for item in selected:
        sources.append({
            "page": item["page"],
            "excerpt": item["text"][:350] + ("..." if len(item["text"]) > 350 else "")
        })
    return {"answer": response.text or "The model returned an empty response.", "sources": sources}
