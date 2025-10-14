import streamlit as st
import random
from datetime import datetime
import streamlit.components.v1 as components

# Set page icon to a daisy
st.set_page_config(page_title="🌼", page_icon="🌼", layout="centered")

# --- CSS for background, falling daisies, and general styling ---
st.markdown("""
<style>
/* --- Main Background (Original pink gradient) --- */
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
    z-index: 10; 
    padding: 20px; 
    /* Using a soft white/pink background for the content box */
    background: rgba(255, 255, 255, 0.85); 
    border-radius: 15px;
    margin: 20px auto;
    max-width: 800px; 
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* --- Falling Daisy Animation (More prominent) --- */
.daisy-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
    z-index: 5; /* Below main content, above background */
    opacity: 0.7; /* Slightly more visible */
}
.daisy {
    position: absolute;
    color: #FFF; /* Pure white center */
    font-size: 20px;
    opacity: 0; 
    animation: daisyFall 20s linear infinite; 
    /* Using text-shadow to give the emoji a subtle glow/border */
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.9);
}
@keyframes daisyFall {
    0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
    10% { opacity: 0.9; }
    100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}
/* Staggering daisy animation delays (Increased number of daisies) */
.daisy:nth-child(1) { animation-delay: 0s; left: 5%; font-size: 25px;}
.daisy:nth-child(2) { animation-delay: 1.5s; left: 15%; font-size: 20px;}
.daisy:nth-child(3) { animation-delay: 3s; left: 25%; font-size: 30px;}
.daisy:nth-child(4) { animation-delay: 4.5s; left: 35%; font-size: 22px;}
.daisy:nth-child(5) { animation-delay: 6s; left: 45%; font-size: 28px;}
.daisy:nth-child(6) { animation-delay: 7.5s; left: 55%; font-size: 23px;}
.daisy:nth-child(7) { animation-delay: 9s; left: 65%; font-size: 27px;}
.daisy:nth-child(8) { animation-delay: 10.5s; left: 75%; font-size: 21px;}
.daisy:nth-child(9) { animation-delay: 12s; left: 85%; font-size: 26px;}
.daisy:nth-child(10) { animation-delay: 13.5s; left: 95%; font-size: 24px;}
.daisy:nth-child(11) { animation-delay: 15s; left: 2%; font-size: 18px;}
.daisy:nth-child(12) { animation-delay: 16.5s; left: 12%; font-size: 32px;}
.daisy:nth-child(13) { animation-delay: 18s; left: 22%; font-size: 26px;}
.daisy:nth-child(14) { animation-delay: 19.5s; left: 32%; font-size: 20px;}
.daisy:nth-child(15) { animation-delay: 21s; left: 42%; font-size: 25px;}

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
/* Floral tree visual */
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
# Increased the number of daisies
daisy_html = """
<div class="daisy-container">
    <div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div>
    <div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div>
    <div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div><div class="daisy">🌼</div>
</div>
"""
st.markdown(daisy_html, unsafe_allow_html=True)


# --- Main App Content wrapped in the content-wrapper div ---
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Updated Title with Daisies
st.markdown('<h1 class="title-text">🌼 For Drishu 🌼</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">A little garden of love just for you 💐</div>', unsafe_allow_html=True)

# Floral Tree visual (Changed emojis)
st.markdown('<div class="love-tree"><div class="tree">🌸🌳🌼</div></div>', unsafe_allow_html=True)

# Messages (Using flower emojis)
messages = [
    "i cant eat you i will get diabetes cuz youre too sweet for even a guju like me 🌼",
    "most percious pookie of all time 🌷",
    "sorry to make you cry last month baby 😊",
    "I love you more every single day 🌸",
    "You’re my baby may you glow everday 💐",
    " your beauty is so glorious by itself its just have its own dimansion to decode not even binary or matrixes can work in it (you called me drunk when i wrte this ) 💫",
    # USER'S NEW MESSAGE ADDED HERE
    "YOURE THE MOST SWEETEST POOKIES MY KUCHUPUCHU RASMALI"
]

if "custom_msgs" not in st.session_state:
    st.session_state.custom_msgs = []

if "love_clicks" not in st.session_state:
    st.session_state.love_clicks = 0

st.subheader("💌Love Message for MY KUCHUPUCHU RASMALI")
col1, col2 = st.columns([1,1])
with col1:
    # Button label changed to floral theme
    if st.button("🌷a message for you 🌷"):
        st.session_state.love_clicks += 1
        # Logic to combine default messages and user-added messages is correct.
        msg_list = messages + st.session_state.custom_msgs
        chosen = random.choice(msg_list)
        st.success(chosen)

with col2:
    # Button label changed to floral theme
    if st.button("🌼 Send a daisy"):
        st.session_state.love_clicks += 1
        st.info("Daisy sent! 🌼")

st.subheader("💬 atheiest me belive in god when i had you ")
new_msg = st.text_input("here dobi")
if st.button("🌸 write what ever you want to baby") and new_msg: # Button label changed
    st.session_state.custom_msgs.append(new_msg)
    st.success("Added! Now it’s a beautiful petal in our collection 🌸")

# Close the content-wrapper div
st.markdown('</div>', unsafe_allow_html=True)


# --- ADMIN FEATURE: Download All Custom Messages (Fixed position) ---

# Prepare the data for download
download_data = "--- Flower Love Note Collection ---\n"
if st.session_state.custom_msgs:
    for i, msg in enumerate(st.session_state.custom_msgs):
        download_data += f"\nNote {i+1}:\n"
        download_data += f"  Text: {msg}\n"
else:
    download_data += "\nNo custom messages yet."

# Use st.markdown to open the fixed container
st.markdown('<div class="fixed-download-container">', unsafe_allow_html=True)

# Place the st.download_button inside the fixed div
st.download_button(
    label="Download All Notes 🤫",
    data=download_data.encode('utf-8'),
    file_name=f"LoveNotes_History_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
    mime="text/plain",
    key="admin_download_key"
)

# Use st.markdown to close the fixed container
st.markdown('</div>', unsafe_allow_html=True)


# If the love button was clicked, render a temporary floating heart/flower animation
trigger = st.session_state.love_clicks

# HTML+JS for temporary floating animation on button click.
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
    // clear previous animation elements
    container.innerHTML = '';
    // Changed colors to flower/plant emojis
    const colors = ['🌼','🌸','🌷','🌱','💐','💖']; 
    const count = 14; 
    for (let i=0;i<count;i++) {{
        const el = document.createElement('div');
        el.className = 'float-heart';
        el.style.left = (10 + Math.random()*80) + 'vw';
        el.style.top = (60 + Math.random()*30) + 'vh';
        el.style.fontSize = (16 + Math.random()*30) + 'px';
        el.style.opacity = 1;
        el.style.transform = 'translateY(0)';
        // Randomly select a flower/heart emoji
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
st.caption(f"Made with 🌼 for you — {datetime.now().year}")
