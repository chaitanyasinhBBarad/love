import streamlit as st
import random
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Love App 💖", page_icon="🌼", layout="centered")

# --- CSS for background, falling daisies, and general styling ---
st.markdown("""
<style>
/* --- Main Background Image of Drishya --- */
html, body, [data-testid="stAppViewContainer"] > .main {
    background-image: url('https://www.dropbox.com/scl/fi/bu7xv708qiv0xy1bp4ngr/Screenshot-2025-10-02-040930.png?rlkey=zn1n99m5cnu5eplzv0o2i0rpp&st=v5my2by8&dl=0'); /* !!! IMPORTANT: REPLACE THIS URL !!! */
    background-size: cover; /* Cover the entire area */
    background-position: center; /* Center the image */
    background-repeat: no-repeat; /* Do not repeat the image */
    background-attachment: fixed; /* Keep image fixed when scrolling */
    background-color: #ffd6e0; /* Fallback color if image fails */
    position: relative; /* Needed for z-index context */
    z-index: 0; /* Base layer */
}

/* --- Content Wrapper to ensure text/buttons are readable --- */
.content-wrapper {
    position: relative;
    z-index: 10; /* Higher than falling daisies, below fixed download button */
    padding: 20px; /* Add some padding so content isn't on edges */
    background: rgba(255, 255, 255, 0.7); /* Slightly transparent white background for readability */
    border-radius: 15px;
    margin: 20px auto;
    max-width: 800px; /* Constrain width for better layout */
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Specific styling for elements inside the content wrapper to ensure they override default Streamlit styles if needed */
.title-text {
    color: #5e0035;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    text-align: center;
    background: none; /* No background for title text itself */
}
.subtitle-text {
    text-align: center;
    color: #7a0b3b;
    margin-top: -10px;
    margin-bottom: 20px;
    background: none;
}
.stText, .stButton {
    background: none; /* Ensure text inputs and buttons don't have conflicting backgrounds */
}
/* Ensure Streamlit components also have some transparency or blend with the new content-wrapper */
div[data-testid="stVerticalBlock"] {
    background: none; /* Remove default block backgrounds */
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
    z-index: 5; /* Above background image, below main content */
}
.daisy {
    position: absolute;
    color: #FFD700; /* Gold-like color for daisies */
    font-size: 20px;
    opacity: 0; /* Start hidden */
    animation: daisyFall linear infinite;
}
@keyframes daisyFall {
    0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
    10% { opacity: 0.8; }
    100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}
/* Delay for each daisy */
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


/* --- Love tree --- */
.love-tree { text-align: center; margin-top: 10px; margin-bottom: 10px; z-index: 1; }
.tree { font-size: 72px; animation: sway 3s ease-in-out infinite; }
@keyframes sway {
    0%, 100% { transform: rotate(-2deg); }
    50% { transform: rotate(2deg); }
}

/* --- Custom button styling --- */
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
    z-index: 1000; /* Ensure it stays above everything */
    padding: 0; 
}

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

# --- Falling Daisies Animation (added HTML) ---
daisy_html = """
<div class="daisy-container">
    <div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div>
    <div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div>
    <div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div>
    <div class="daisy">🌼</div><div class="daisy">🌼</div>
</div>
"""
st.markdown(daisy_html, unsafe_allow_html=True)

# --- Main App Content ---
# All main content (title, buttons, etc.) should be wrapped in the 'content-wrapper' div
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
    if st.button("💓 Send a heart"):
        st.session_state.love_clicks += 1
        st.info("Heart sent!")

st.subheader("💬 Add Your Own Love Note")
new_msg = st.text_input("Write something sweet...")
if st.button("💌 Add Message") and new_msg:
    st.session_state.custom_msgs.append(new_msg)
    st.success("Added! Now it’s part of our love collection 💞")

# Close the content-wrapper div
st.markdown('</div>', unsafe_allow_html=True)

# --- ADMIN FEATURE: Download All Custom Messages (positioned outside content-wrapper) ---

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
with st.container():
    st.download_button(
        label="Download All Notes 🤫",
        data=download_data.encode('utf-8'),
        file_name=f"LoveNotes_History_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        key="admin_download_key"
    )
st.markdown('</div>', unsafe_allow_html=True)


# --- Floating Hearts Animation (Unchanged logic, but z-index might need adjustment if it conflicts) ---
# Ensure floating hearts are above the content wrapper if desired, or below if they are purely aesthetic.
# For this setup, we'll keep them above for a more dynamic effect over the content box.
trigger = st.session_state.love_clicks

floating_hearts_html = f"""
<div id="heart-container" style="position:fixed;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:100;"></div> <style>
.float-heart{{ position:fixed; font-size:24px; pointer-events:none; user-select:none; transform:translateY(0); }}
@keyframes floatUp{{
    0% {{ transform: translateY(0) scale(1); opacity: 1; }}
    100% {{ transform: translateY(-30vh) scale(1.6); opacity: 0; }}
}}
</style>
<script>
(function(){{
    const container = document.getElementById('heart-container');
    container.innerHTML = ''; // Clear previous hearts
    const colors = ['❤️','💖','💘','💕','💞'];
    const count = 14;
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
        (function(e, delay){{
            setTimeout(function(){{
                e.style.transition = 'transform 1400ms ease-out, opacity 1400ms ease-out';
                e.style.transform = 'translateY(-40vh) translateX(' + (Math.random()*60-30) + 'px) scale(1.3)';
                e.style.opacity = 0;
                setTimeout(function(){{ e.remove(); }}, 1500);
            }}, delay);
        }})(el, i*70);
    }}
}})();
</script>
"""

components.html(floating_hearts_html, height=1)

st.write('---')
st.caption(f"Made with ❤️ for you — {datetime.now().year}")
