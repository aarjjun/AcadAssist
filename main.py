# main.py

import streamlit as st
import os
import tempfile
import threading

from parser.pdf_parser import extract_text_from_pdf
from parser.docx_parser import extract_text_from_docx
from parser.pptx_parser import extract_text_from_pptx
from utils.chunking import chunk_text
from gemini_helper import generate_notes_with_context


# Session state setup
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "notes" not in st.session_state:
    st.session_state.notes = []
if "page" not in st.session_state:
    st.session_state.page = 0
if "background_loaded" not in st.session_state:
    st.session_state.background_loaded = {}

# Page config
st.set_page_config(page_title="Academic Assistant", layout="wide")

# App title
st.title("📘 Academic Assistant — Intelligent Note Generator")

# Upload file
uploaded_file = st.file_uploader("Upload PDF, DOCX, or PPTX", type=["pdf", "docx", "pptx"])

def handle_file_upload(file):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(file.read())
        temp_path = temp.name

    ext = file.name.split(".")[-1].lower()

    if ext == "pdf":
        raw_text = extract_text_from_pdf(temp_path)
    elif ext == "docx":
        raw_text = extract_text_from_docx(temp_path)
    elif ext == "pptx":
        raw_text = extract_text_from_pptx(temp_path)
    else:
        st.error("Unsupported file type")
        return

    os.remove(temp_path)

    # Chunk text
    st.session_state.chunks = chunk_text(raw_text)
    st.session_state.notes = [None] * len(st.session_state.chunks)
    st.session_state.page = 0
    st.session_state.background_loaded = {}
    fetch_notes_for_page(0)  # Load the first page
    preload_next_page(1)     # Start background loading
    preload_next_page(2)     # Start background loading


def fetch_notes_for_page(i):
    if st.session_state.notes[i] is None:
        chunk = st.session_state.chunks[i]
        st.session_state.notes[i] = generate_notes_with_context(i)


def preload_next_page(i):
    def bg_task(index, chunks_copy, notes_copy):
        if 0 <= index < len(chunks_copy):
            if st.session_state.notes[index] is None:
                note = generate_notes_with_context(index)
                st.session_state.notes[index] = note
                st.session_state.background_loaded[index] = True

    chunks_copy = st.session_state.chunks[:]
    notes_copy = st.session_state.notes[:]

    threading.Thread(
        target=bg_task,
        args=(i, chunks_copy, notes_copy),
        daemon=True
    ).start()


# Run if file uploaded
if uploaded_file:
    if not st.session_state.chunks:
        handle_file_upload(uploaded_file)

    total_pages = len(st.session_state.chunks)
    current_page = st.session_state.page

    st.markdown(f"### 📄 Page {current_page + 1} of {total_pages}")

    with st.spinner("Loading notes..."):
        notes = st.session_state.notes[current_page]
        if notes:
            st.markdown(notes, unsafe_allow_html=True)
        else:
            fetch_notes_for_page(current_page)
            st.markdown(st.session_state.notes[current_page], unsafe_allow_html=True)

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous", disabled=current_page == 0):
            st.session_state.page -= 1

    with col3:
        if st.button("Next ➡️", disabled=current_page == total_pages - 1):
            st.session_state.page += 1
            preload_next_page(st.session_state.page + 1)
            preload_next_page(st.session_state.page + 2)
