import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["gemini"]["api_key"])

def generate_flashcards(text):
    prompt = f"Create interactive study flashcards from this text:\n\n{text}\n\nUse the format: Term - Definition"
    response = genai.GenerativeModel('models/gemini-1.5-flash').generate_content(prompt)
    lines = response.text.strip().split("\n")
    cards = [line.split(" - ", 1) for line in lines if " - " in line]
    return cards

def show_flashcards(notes):
    st.subheader("🃏 Interactive Flashcards")
    cards = generate_flashcards(notes)

    for i, (term, definition) in enumerate(cards):
        with st.expander(f"Flashcard {i+1}: {term}"):
            st.markdown(f"**Definition:** {definition}")
            feedback = st.radio(f"Did you know this?", ("✅ I got it!", "❌ I didn't know"), key=i)
            st.markdown("---")

if st.toggle("🎮 Quiz Me!"):
    # Hide answer and ask user to guess
    st.write("Quiz mode activated!")
