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

# Use st.markdown to open the fixed container
st.markdown('<div class="fixed-download-container">', unsafe_allow_html=True)

# FIX: Removed the unnecessary and conflicting 'with st.container():' wrapper.
st.download_button(
    label="Download All Notes 🤫",
    data=download_data.encode('utf-8'),
    file_name=f"LoveNotes_History_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
    mime="text/plain",
    key="admin_download_key"
)

# Use st.markdown to close the fixed container
st.markdown('</div>', unsafe_allow_html=True)


# If the love button was clicked, render a temporary floating hearts animation
trigger = st.session_state.love_clicks

# HTML+JS for floating hearts on button click.
floating_hearts_html = f"""
<div id="heart-container" style="position:fixed;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:100;"></div>
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
