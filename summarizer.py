# summarizer.py

import streamlit as st
import google.generativeai as genai

def summarize_text(text):
    genai.configure(api_key=st.secrets["gemini"]["api_key"])
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    prompt = f"Summarize the following text:\n\n{text}\n\nProvide a concise summary and list key highlights for students to easily remember it."
    response = model.generate_content(prompt)
    return response.text

def show_summarization(notes):
    st.header("📑 Smart Summarization & Highlights")
    summary = summarize_text(notes)
    st.markdown(summary)
