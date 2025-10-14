import streamlit as st
import random
from datetime import datetime
import streamlit.components.v1 as components
# Note: Removed smtplib imports as per previous request to avoid email

st.set_page_config(page_title="Love App 💖", page_icon="💌", layout="centered")

# --- CSS for background, tree, and general styling ---
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(135deg, #ffd6e0, #fff0f5);
}
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

/* Persistent gentle background hearts (low z-index so UI remains clickable) */
.bg-heart {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
    z-index: 0;
    opacity: 0.25;
}
.bg-heart .heart {
    position: absolute;
    animation: slowFloat 10s linear infinite;
    font-size: 22px;
}
@keyframes slowFloat {
    0% { transform: translateY(-10vh) rotate(0deg); opacity: 0.7; }
    50% { opacity: 1; }
    100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
}

/* Love tree */
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
}

/* Container to keep components above background */
.content-wrapper { position: relative; z-index: 2; }

/* --- NEW: Fixed Position Container for Download Button --- */
.fixed-download-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1000; /* Ensure it stays above everything */
    /* Remove default Streamlit padding from container */
    padding: 0; 
}

/* Style the button inside the fixed container differently if needed */
.fixed-download-container .stDownloadButton>button {
    background: #007bff; /* Blue for a 'secret' admin button */
    color: white;
    border-radius: 8px;
    padding: 8px 15px;
    font-size: 14px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# Render gentle background hearts once
bg_hearts_html = """
<div class="bg-heart">""" + "".join([f"<div class='heart' style='left:{i*9}%; animation-delay:{i*0.9}s;'>❤️</div>" for i in range(11)]) + """</div>
"""

st.markdown(bg_hearts_html, unsafe_allow_html=True)

# Title
st.markdown('<div class="content-wrapper"><h1 class="title-text">💖 For Drishya — Love App 💖</h1></div>', unsafe_allow_html=True)
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
    st.session_state.custom_msgs = []

if "love_clicks" not in st.session_state:
    st.session_state.love_clicks = 0

st.subheader("💌 Random Love Message")
col1, col2 = st.columns([1,1])
with col1:
    if st.button("💞 Show me some love 💞"):
        st.session_state.love_clicks += 1
        msg_list = messages + st.session_state.custom_msgs
        chosen = random.choice(msg_list)
        st.success(chosen)

with col2:
    # interactive quick react button (a smaller heart button)
    if st.button("💓 Send a heart"):
        st.session_state.love_clicks += 1
        st.info("Heart sent!")

st.subheader("💬 Add Your Own Love Note")
new_msg = st.text_input("Write something sweet...")
if st.button("💌 Add Message") and new_msg:
    st.session_state.custom_msgs.append(new_msg)
    st.success("Added! Now it’s part of our love collection 💞")

# --- ADMIN FEATURE: Download All Custom Messages ---

# Prepare the data for download
download_data = "--- Love Note Collection ---\n"
if st.session_state.custom_msgs:
    for i, msg in enumerate(st.session_state.custom_msgs):
        download_data += f"\nNote {i+1}:\n"
        download_data += f"  Text: {msg}\n"
else:
    download_data += "\nNo custom messages yet."

# Use st.markdown and the fixed container CSS to position the button

st.markdown('<div class="fixed-download-container">', unsafe_allow_html=True)

# Place the st.download_button inside the fixed div using a temporary container (this is a Streamlit hack)
with st.container():
    st.download_button(
        label="Download All Notes 🤫",
        data=download_data.encode('utf-8'),
        file_name=f"LoveNotes_History_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        key="admin_download_key" # Added key for uniqueness
    )

st.markdown('</div>', unsafe_allow_html=True)
# The button is now physically located within the HTML container which is fixed to the bottom-right.


# If the love button was clicked, render a temporary floating hearts animation
trigger = st.session_state.love_clicks

# HTML+JS for floating hearts on button click.
floating_hearts_html = f"""
<div id="heart-container" style="position:fixed;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:9999;"></div>
<style>
.float-heart{{ position:fixed; font-size:24px; pointer-events:none; user-select:none; transform:translateY(0); }}
@keyframes floatUp{{
    0% {{ transform: translateY(0) scale(1); opacity: 1; }}
    100% {{ transform: translateY(-30vh) scale(1.6); opacity: 0; }}
}}
</style>
<script>
(function(){{
    const container = document.getElementById('heart-container');
    // clear previous hearts
    container.innerHTML = '';
    const colors = ['❤️','💖','💘','💕','💞'];
    const count = 14; // number of hearts to spawn each click
    for (let i=0;i<count;i++) {{
        const el = document.createElement('div');
        el.className = 'float-heart';
        el.style.left = (10 + Math.random()*80) + 'vw';
        el.style.top = (60 + Math.random()*30) + 'vh';
        el.style.fontSize = (16 + Math.random()*30) + 'px';
        el.style.opacity = 1;
        el.style.transform = 'translateY(0)';
        el.innerText = colors[Math.floor(Math.random()*colors.length)];
        container.appendChild(el);
        // stagger animations
        (function(e, delay){{
            setTimeout(function(){{
                e.style.transition = 'transform 1400ms ease-out, opacity 1400ms ease-out';
                e.style.transform = 'translateY(-40vh) translateX(' + (Math.random()*60-30) + 'px) scale(1.3)';
                e.style.opacity = 0;
                // remove after animation
                setTimeout(function(){{ e.remove(); }}, 1500);
            }}, delay);
        }})(el, i*70);
    }}
}})();
</script>
"""

# Embed the HTML.
components.html(floating_hearts_html, height=1)

st.write('---')
st.caption(f"Made with ❤️ for you — {datetime.now().year}")
