import streamlit as st

def load_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=JetBrains+Mono&display=swap');

        body {
            font-family: 'JetBrains Mono', monospace;
            background-color: #f9f9f9;
        }

        .hero {
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-family: 'Indie Flower', cursive;
            border-radius: 1rem;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }

        .hero h1 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }

        .hero p {
            font-size: 1.25rem;
            margin-bottom: 1.5rem;
        }

        .btn-cta {
            background-color: #ff6f91;
            color: white;
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 9999px;
            cursor: pointer;
            font-weight: bold;
            font-size: 1.1rem;
            transition: background-color 0.3s ease;
        }
        .btn-cta:hover {
            background-color: #ff5472;
        }

        /* Sidebar avatar circle */
        .avatar-sidebar {
            position: fixed;
            top: 20px;
            left: 20px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            font-family: 'Indie Flower', cursive;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 10px rgba(102,126,234,0.7);
        }

        /* Typing animation */
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        .typing-text {
            overflow: hidden;
            white-space: nowrap;
            border-right: 0.15em solid orange;
            animation: typing 3.5s steps(40, end) infinite;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            color: #444;
            margin: 1rem 0;
        }

        /* Floating Action Button */
        .fab {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            background: #ff6f91;
            color: white;
            border-radius: 50%;
            font-size: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 5px 15px rgba(255,111,145,0.5);
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .fab:hover {
            background-color: #ff5472;
        }

        /* Notebook style card */
        .notebook-card {
            background: 2C2E3E;
            color: #FFFDF6;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            padding: 2rem;
            margin-bottom: 1.5rem;
       
            line-height: 1.5;
            position: relative;
            border: 1px dashed #ccc;
# background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
        }

        /* Easter egg hidden */
        .easter-egg {
            display: none;
            position: fixed;
            bottom: 10px;
            left: 10px;
            font-size: 1.5rem;
            color: #ff6f91;
            cursor: pointer;
        }
        .easter-egg.visible {
            display: block;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% {opacity: 1;}
            50% {opacity: 0.5;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def notebook_divider():
    st.markdown(
        """
        <hr style="
            border: none; 
            border-top: 2px dashed #ccc; 
            margin: 1.5rem 0;
            width: 80%;
            margin-left: auto;
            margin-right: auto;
        ">
        """,
        unsafe_allow_html=True,
    )


def hero_section():
    st.markdown(
        """
        <div class="hero">
            <h1>Your AI-powered Note Wizard ✨</h1>
            <p>Turn lectures into neat, clear notes – instantly.</p>
            <button class="btn-cta" onclick="window.scrollTo(0,document.body.scrollHeight)">Upload Your File</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

def avatar_sidebar(username):
    # Show user initials
    initials = "".join([part[0] for part in username.split()]).upper()
    st.markdown(
        f'<div class="avatar-sidebar">{initials}</div>',
        unsafe_allow_html=True,
    )

def loading_animation():
    st.markdown(
        '<div class="typing-text">🤖 Gemini is writing your notes...</div>',
        unsafe_allow_html=True,
    )

def floating_button():
    st.markdown(
        """
        <div class="fab" title="Help" onclick="alert('How can I help you?')">?</div>
        """,
        unsafe_allow_html=True,
    )

def notebook_card(content):
    st.markdown(f'<div class="notebook-card">{content}</div>', unsafe_allow_html=True)

def easter_egg():
    st.markdown(
        """
        <div class="easter-egg visible" onclick="alert('You found the easter egg! 🎉')">🎁</div>
        """,
        unsafe_allow_html=True,
    )
