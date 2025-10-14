import streamlit as st
import random
from datetime import datetime
import streamlit.components.v1 as components

# Set page icon to a daisy
st.set_page_config(page_title="Love App 💖", page_icon="🌼", layout="centered")

# --- CSS for background, falling daisies, and general styling ---
st.markdown("""
<style>
/* --- Main Background (Reverted to original gradient, no image) --- */
html, body, [data-testid="stAppViewContainer"] > .main {
    /* Reverting to the original pink gradient */
    background: linear-gradient(135deg, #ffd6e0, #fff0f5);
    position: relative; 
    z-index: 0; 
    min-height: 100vh;
}

/* --- Content Wrapper for Readability --- */
.content-wrapper {
    position: relative;
    z-index: 10; /* Higher than falling daisies */
    padding: 20px; 
    /* Using a soft pink background for the content box */
    background: rgba(255, 240, 245, 0.85); 
    border-radius: 15px;
    margin: 20px auto;
    max-width: 800px; 
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* --- Falling Daisy Animation --- */
.daisy-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
    z-index: 5; /* Below main content, above background */
}
.daisy {
    position: absolute;
    color: #FFD700; 
    font-size: 20px;
    opacity: 0; 
    animation: daisyFall 20s linear infinite; 
}
@keyframes daisyFall {
    0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
    10% { opacity: 0.8; }
    100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}
/* Staggering daisy animation delays */
.daisy:nth-child(1) { animation-delay: 0s; left: 10%; font-size: 25px;}
.daisy:nth-child(2) { animation-delay: 2s; left: 20%; font-size: 20px;}
.daisy:nth-child(3) { animation-delay: 4s; left: 30%; font-size: 30px;}
.daisy:nth-child(4) { animation-delay: 6s; left: 40%; font-size: 22px;}
.daisy:nth-child(5) { animation-delay: 8s; left: 50%; font-size: 28px;}
.daisy:nth-child(6) { animation-delay: 10s; left: 60%; font-size: 23px;}
.daisy:nth-child(7) { animation-delay: 12s; left: 70%; font-size: 27px;}
.daisy:nth-child(8) { animation-delay: 14s; left: 80%; font-size: 21px;}
.daisy:nth-child(9) { animation-delay: 16s; left: 90%; font-size: 26px;}
.daisy:nth-child(10) { animation-delay: 18s; left: 5%; font-size: 24px;}
.daisy:nth-child(11) { animation-delay: 20s; left: 15%; font-size: 29px;}


/* --- Other Styling --- */
.title-text {
    color: #5e0035;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    text-align: center;
}
.subtitle-text {
    text-align: center;
    color: #7a0b3b;
    margin-top: -10px;
    margin-bottom: 20px;
}
.love-tree { text-align: center; margin-top: 10px; margin-bottom: 10px; z-index: 1; }
.tree { font-size: 72px; animation: sway 3s ease-in-out infinite; }
@keyframes sway {
    0%, 100% { transform: rotate(-2deg); }
    50% { transform: rotate(2deg); }
}

/* Custom button styling */
.stButton>button {
    background: linear-gradient(90deg,#ff7aa2,#ff4b6e);
    color: white;
    border-radius: 24px;
    padding: 10px 28px;
    font-size: 18px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}


/* --- Fixed Position Container for Download Button --- */
.fixed-download-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1000; 
    padding: 0; 
}

.fixed-download-container .stDownloadButton>button {
    background: #007bff;
    color: white;
    border-radius: 8px;
    padding: 8px 15px;
    font-size: 14px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# --- Falling Daisies Animation (HTML) ---
daisy_html = """
<div class="daisy-container">
    <div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div>
    <div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div>
    <div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div>
    <div class="daisy">🌼</div><div class="daisy">🌼</div>
</div>
"""
st.markdown(daisy_html, unsafe_allow_html=True)


# --- Main App Content wrapped in the content-wrapper div ---
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

st.markdown('<h1 class="title-text">💖 For Drishya — Love App 💖</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">A little corner of the internet made just for you 💐</div>', unsafe_allow_html=True)

# Love tree visual
st.markdown('<div class="love-tree"><div class="tree">🌳❤️🌳</div></div>', unsafe_allow_html=True)

# Messages
messages = [
    "You are my favorite notification ❤️",
    "Every moment with you feels like magic ✨",
    "You make my heart smile 😊",
    "I love you more every single day 💕",
    "You’re my today and all of my tomorrows 💞",
    "With you, ordinary moments become unforgettable 💫",
]

if "custom_msgs" not in st.session_state:
    st.
