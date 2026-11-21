# Smart Appliance Manual Assistant — PS 40

A Retrieval-Augmented Generation (RAG) application that lets a user upload an appliance manual PDF and ask troubleshooting questions in plain language. Answers are grounded in retrieved manual excerpts and show source page numbers.

## Features
- Upload a PDF appliance manual.
- Extract text page by page and retain page metadata.
- Split text into overlapping chunks.
- Create Gemini embeddings and store them in a FAISS similarity index.
- Retrieve the most relevant chunks for a question.
- Generate numbered troubleshooting steps with Gemini.
- Show source page numbers and relevant excerpts.
- Say when the answer is not present in the uploaded manual.
- Display safety guidance.

## Technology
Python, Streamlit, PyPDF, Google GenAI SDK, Gemini Embeddings, Gemini Flash, FAISS, NumPy.

## Run locally (Windows / VS Code)
1. Install Python 3.10 or newer.
2. Open this project folder in VS Code.
3. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and add your Gemini API key. Never upload `.env` to GitHub.
6. Run:
   ```powershell
   streamlit run app.py
   ```

You can also paste the API key into the sidebar while the app is running.

## How the RAG pipeline works
1. PDF upload: the user selects an appliance manual.
2. Text extraction: PyPDF extracts text from each page and records its page number.
3. Chunking: text is divided into overlapping chunks to preserve context.
4. Embedding: Gemini converts each chunk into a numerical vector.
5. Indexing: FAISS stores vectors for similarity search.
6. Retrieval: the question is embedded and the top matching chunks are retrieved.
7. Generation: Gemini receives the question and retrieved excerpts, and generates a grounded answer.
8. Source display: the app shows page numbers and excerpts used.

## Testing
Test with at least five questions from the manual:
- Ask for a normal operating instruction.
- Ask about a troubleshooting symptom.
- Ask about an error code that appears in the manual.
- Ask about cleaning or maintenance.
- Ask a question whose answer is absent from the manual; the app should say it could not find the information.

Record the actual output and screenshots after running the app with a real manual and API key.

## Limitations
- Text-based PDFs are supported. Scanned/image-only PDFs need OCR, which is not included in this version.
- Answer quality depends on the manual's text quality and the retrieved passages.
- This is an informational assistant, not a replacement for the manufacturer's support or an authorised technician.
- API access and usage may be subject to provider quotas and charges.

## Assignment
Problem Statement 40 — Product Manual Assistant, Document Q&A / RAG.
