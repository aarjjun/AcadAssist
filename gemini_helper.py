# gemini_helper.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_notes_with_context(index):
    from streamlit import session_state as st_session  # Needed to access session_state in utils file

    chunks = st_session.chunks

    # Get previous, current, and next chunks if they exist
    prev_chunk = chunks[index - 1] if index > 0 else ""
    current_chunk = chunks[index]
    next_chunk = chunks[index + 1] if index < len(chunks) - 1 else ""

    # Combine context
    combined_text = ""
    if prev_chunk:
        combined_text += "Previous Context:\n" + prev_chunk + "\n\n"
    combined_text += "Current Content:\n" + current_chunk + "\n\n"
    if next_chunk:
        combined_text += "Next Context:\n" + next_chunk + "\n"

    # Prompt for continuity
    prompt = (
        "You are a brilliant academic tutor helping a university student prepare for Kerala Technological University (KTU) exams. "
        "Convert the **current content** into easy, detailed, and connected notes. "
        "Maintain smooth continuity from the previous topic and a clear bridge into the next topic. "
        "Avoid repeating full content — just use previous/next chunks for reference.\n\n"
        "Instructions:\n"
        "- Use clear headings and bullet points.\n"
        "- Simplify explanations with real-world analogies and examples.\n"
        "- Maintain logical flow.\n"
        "- Don’t repeat; summarize and connect.\n\n"
        f"{combined_text}\n\n"
        "Now create connected, easy-to-understand notes suitable for KTU exams."
    )

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
    
