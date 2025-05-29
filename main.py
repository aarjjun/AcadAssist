import streamlit as st
import os
import tempfile
import threading
import queue

from parser.pdf_parser import extract_text_from_pdf
from parser.docx_parser import extract_text_from_docx
from parser.pptx_parser import extract_text_from_pptx
from utils.chunking import chunk_text
from gemini_helper import generate_notes_with_context

from ui_components import (
    load_custom_css,
    hero_section,
    avatar_sidebar,
    loading_animation,
    floating_button,
    notebook_divider,
    notebook_card,
    easter_egg,
)

# Import your feature modules
from summarizer import show_summarization
from flashcard import show_flashcards

# === SETUP ===
st.set_page_config(page_title="Academic Assistant", layout="wide")
load_custom_css()
avatar_sidebar("Arjun")  # Show sidebar avatar/profile
hero_section()           # Show hero landing section

# === THREAD-SAFE QUEUE FOR BACKGROUND RESULTS ===
result_queue = queue.Queue()

# === SESSION STATE INIT ===
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "notes" not in st.session_state:
    st.session_state.notes = []
if "page" not in st.session_state:
    st.session_state.page = 0
if "background_loaded" not in st.session_state:
    st.session_state.background_loaded = {}

def update_notes_from_queue():
    while not result_queue.empty():
        index, note = result_queue.get()
        st.session_state.notes[index] = note
        st.session_state.background_loaded[index] = True

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

    st.session_state.chunks = chunk_text(raw_text)
    st.session_state.notes = [None] * len(st.session_state.chunks)
    st.session_state.page = 0
    st.session_state.background_loaded = {}

    fetch_notes_for_page(0)
    preload_next_page(1)
    preload_next_page(2)

def fetch_notes_for_page(i):
    if st.session_state.notes[i] is None:
        note = generate_notes_with_context(i)
        st.session_state.notes[i] = note

def preload_next_page(i):
    chunks_copy = st.session_state.chunks[:]

    def bg_task(index):
        note = generate_notes_with_context(index)
        result_queue.put((index, note))

    if 0 <= i < len(chunks_copy):
        threading.Thread(target=bg_task, args=(i,), daemon=True).start()

# Update notes from background threads
update_notes_from_queue()

# === MAIN UI ===

st.title("📘 Academic Assistant — Intelligent Note Generator")

uploaded_file = st.file_uploader("Upload PDF, DOCX, or PPTX", type=["pdf", "docx", "pptx"])

if uploaded_file:
    if not st.session_state.chunks:
        handle_file_upload(uploaded_file)

    total_pages = len(st.session_state.chunks)
    current_page = st.session_state.page

    st.markdown(f"### 📄 Page {current_page + 1} of {total_pages}")

    # Show loading animation if note not ready yet
    if st.session_state.notes[current_page] is None:
        loading_animation()
        fetch_notes_for_page(current_page)
        update_notes_from_queue()

    notes = st.session_state.notes[current_page]

    if notes is None:
        loading_animation()
    else:
        notebook_card(notes)

        # Below notes, add tabbed interface for extra features
        st.markdown("---")
        tab1, tab2 = st.tabs(["📝 Summarization", "🃏 Flashcards"])

        with tab1:
            show_summarization(notes)

        with tab2:
            show_flashcards(notes)


    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous", disabled=current_page == 0):
            st.session_state.page -= 1

    with col3:
        if st.button("Next ➡️", disabled=current_page == total_pages - 1):
            st.session_state.page += 1
            preload_next_page(st.session_state.page + 1)
            preload_next_page(st.session_state.page + 2)

# Floating Action Button always visible
floating_button()

# Easter egg section visible somewhere
easter_egg()
