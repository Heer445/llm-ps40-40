import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from rag_engine import build_manual_index, answer_question

load_dotenv()

st.set_page_config(page_title="Smart Appliance Manual Assistant", page_icon="🔧", layout="wide")

st.title("🔧 Smart Appliance Manual Assistant")
st.caption("Ask questions about an appliance using its uploaded PDF manual.")

with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Gemini API key", type="password",
                            value=os.getenv("GEMINI_API_KEY", ""))
    st.info("Your manual is processed for this session. Do not upload confidential documents.")
    st.markdown("**How it works**\n1. Upload a manual PDF\n2. Build the searchable knowledge base\n3. Ask a troubleshooting question\n4. Review the answer and source pages")

uploaded = st.file_uploader("Upload appliance manual (PDF)", type=["pdf"])

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "manual_name" not in st.session_state:
    st.session_state.manual_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []

if uploaded:
    st.write(f"**Selected manual:** {uploaded.name} · {uploaded.size / 1024:.1f} KB")
    if st.button("Process manual", type="primary"):
        if not api_key:
            st.error("Enter your Gemini API key in the sidebar or add it to the .env file.")
        else:
            with st.spinner("Reading the PDF and creating the searchable index..."):
                try:
                    pdf_bytes = uploaded.getvalue()
                    store, chunk_count = build_manual_index(pdf_bytes, api_key)
                    st.session_state.vector_store = store
                    st.session_state.manual_name = uploaded.name
                    st.session_state.messages = []
                    st.success(f"Manual processed successfully. Created {chunk_count} searchable text chunks.")
                except Exception as exc:
                    st.error(f"Could not process this PDF: {exc}")

if st.session_state.vector_store is not None:
    st.divider()
    st.subheader(f"Ask your manual: {st.session_state.manual_name}")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Example: Why is my washing machine not draining?")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching the manual and preparing an answer..."):
                try:
                    result = answer_question(
                        question, st.session_state.vector_store, api_key
                    )
                    st.markdown(result["answer"])
                    if result["sources"]:
                        with st.expander("View source pages"):
                            for source in result["sources"]:
                                st.markdown(f"**Page {source['page']}**")
                                st.caption(source["excerpt"])
                    st.session_state.messages.append(
                        {"role": "assistant", "content": result["answer"]}
                    )
                except Exception as exc:
                    st.error(f"Unable to answer this question: {exc}")
else:
    st.info("Upload a PDF manual and select **Process manual** to begin.")

st.divider()
st.caption(
    "Safety notice: Follow the manufacturer's instructions. Disconnect power or stop using "
    "the appliance when the manual advises it or when there is smoke, burning smell, sparking, "
    "leakage, or another immediate hazard. Do not attempt repairs involving live electrical "
    "parts, gas systems, or sealed components. Contact an authorised technician when needed."
)
