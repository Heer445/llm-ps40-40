# Smart Appliance Manual Assistant — Procedure Report

**PS Number:** 40  
**Student Name:** [Enter your name]  
**Roll Number:** 40  
**Class:** [Enter class/division]  
**GitHub Link:** [Add repository URL]

## 1. Problem Statement
Users rarely read appliance manuals when troubleshooting a problem. This project provides a web application where users upload an appliance manual in PDF format and ask questions in plain language. The application retrieves relevant manual content and generates numbered troubleshooting steps with source page numbers and safety warnings where relevant.

## 2. Tools and Model
- Language: Python
- User interface: Streamlit
- PDF extraction: PyPDF
- Text processing: chunking with overlap
- Embeddings: Gemini Embedding model
- Vector database: FAISS
- LLM: Gemini Flash through the Google GenAI SDK

## 3. Procedure
1. Created a Python project and virtual environment.
2. Installed the required libraries using `requirements.txt`.
3. Created a Gemini API key and stored it in `.env`, which is excluded from Git.
4. Built PDF extraction to read text page by page and preserve page numbers.
5. Split the extracted text into overlapping chunks.
6. Generated embeddings for the chunks and stored them in a FAISS index.
7. Embedded each user question and retrieved the most relevant manual chunks.
8. Designed a prompt instructing the LLM to answer only from retrieved manual content, use numbered steps, avoid unsupported claims, and include safety warnings when relevant.
9. Built the Streamlit interface for PDF upload, processing, questions, answers and source-page display.
10. Tested the application with questions based on an actual appliance manual.

## 4. Prompt Used
You are a careful appliance-manual assistant. Answer the user's question using only the supplied manual excerpts. If the excerpts do not contain the answer, say that the information could not be found in the uploaded manual. Do not invent error-code meanings or procedures. For troubleshooting, provide numbered steps in plain language. Include relevant safety warnings. End with the source page numbers.

**Prompt improvement:** Added an explicit instruction to say when information is missing, preventing the model from guessing beyond the uploaded manual.

## 5. Results
[After running the application, insert 1–2 screenshots showing the uploaded manual, a question, the generated answer and source page numbers.]

**Test cases:** Record at least five real questions and their observed results. Do not enter expected results as actual results.

## 6. Challenges
[Record actual issues encountered, such as scanned PDFs without selectable text, API-key errors, package installation issues or irrelevant retrieval. Explain the fixes you actually applied.]

## 7. Conclusion
The application demonstrates a basic RAG pipeline for asking questions about appliance manuals. It extracts and indexes manual content, retrieves relevant passages and generates answers with page references. A future improvement would be OCR support for scanned manuals and more advanced retrieval evaluation.

> Complete the Results, Challenges and GitHub Link sections with your actual implementation evidence before submission.
