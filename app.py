import streamlit as st
import datetime
import random
import re
import pandas as pd

# --- 1. CONFIGURATION AND STYLING INJECTION (The "Escape Hatch") ---

# Tailwind CSS and Google Fonts setup
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Custom CSS for Background, Card, Daisy Effect, and Streamlit Overrides
st.markdown("""
<style>
    /* Custom Fonts for global use */
    :root {
        --primary-font: 'Inter', sans-serif;
        --display-font: 'Playfair Display', serif;
    }
    
    body {
        font-family: var(--primary-font);
    }
    
    /* 1. Global Background (Pink Gradient) */
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%);
        min-height: 100vh;
        padding-top: 0 !important; /* Remove default padding for full-screen effect */
    }

    /* 2. Custom Header Styles */
    .header-bg {
        background: linear-gradient(90deg, #ff80a0, #ff4081);
        color: white;
        border-bottom-left-radius: 2rem;
        border-bottom-right-radius: 2rem;
        box-shadow: 0 8px 15px rgba(255, 64, 129, 0.4);
        padding-bottom: 2rem !important;
    }
    .header-bg h1 {
        font-family: var(--display-font);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* 3. Streamlit Main Content Card */
    /* Target the main block container where Streamlit widgets live */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 800px; /* Optional: Constrain width for desktop readability */
        margin-left: auto;
        margin-right: auto;
    }
    
    .stMarkdown h1, .stMarkdown h2 {
        font-family: var(--display-font);
    }

    /* 4. Custom Button Styling (Message Button) */
    .stButton>button {
        background-color: #ff80a0; /* Soft Pink */
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #ff4081; /* Deeper Pink */
        box-shadow: 0 6px 10px rgba(255, 64, 129, 0.5);
        transform: translateY(-2px);
    }
    
    /* 5. Daisy Animation */
    .daisy {
        position: absolute;
        width: 20px;
        height: 20px;
        color: #fff;
        font-size: 20px;
        animation: fall linear infinite;
        pointer-events: none;
        z-index: 1000;
        filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.5));
    }
    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 0.8; }
        100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
    }
    /* Set animation duration for each daisy type for variety */
    .daisy-slow { animation-duration: 15s; }
    .daisy-medium { animation-duration: 12s; }
    .daisy-fast { animation-duration: 9s; }
</style>
""", unsafe_allow_html=True)

# --- 2. PYTHON UTILITY FUNCTIONS (Mock Data Analysis) ---

def calculate_duration_live(start_date_str):
    """Calculates the duration between a start date and today."""
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    today = datetime.date.today()
    duration = today - start_date
    total_days = duration.days
    
    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30 # Approximation
    days = remaining_days % 30
    
    duration_str = f"{years} years, {months} months, and {days} days"
    return duration_str, total_days

def parse_chat(uploaded_file):
    """Mocks parsing a chat file and returns fake data for analysis."""
    # In a real app, this would read the file line by line and structure it.
    st.info("Parsing chat file... (This is a mock analysis for display)")
    
    # Mock data to simulate analysis results
    chat_data = {
        'total_messages': 52397,
        'start_date': '2022-01-05',
        'most_active_day': 'Saturday',
        'most_used_word': 'love',
        'top_emojis': ['❤️', '🥺', '😂'],
        'top_sender': 'Drishya',
        'top_sender_count': 32190
    }
    return chat_data

def analyze_chat_data(chat_data):
    """Mocks generating insights from the parsed data."""
    if not chat_data:
        return "No data to analyze."
        
    messages_per_day = chat_data['total_messages'] / (datetime.date.today() - datetime.date(2022, 1, 5)).days
    
    report = f"""
    ### 💌 Our Chat Journey Report 
    
    **Total Messages Exchanged:** {chat_data['total_messages']:,} messages.
    
    **Duration:** Since {chat_data['start_date']}, we've exchanged messages for over **{int(messages_per_day)} messages per day** on average!
    
    **Busiest Day:** Our chats peak on **{chat_data['most_active_day']}**—looks like weekends are for us!
    
    **Top Word:** The word we use the most is **"{chat_data['most_used_word'].upper()}"** (of course!).
    
    **Our Favorite Emojis:** {', '.join(chat_data['top_emojis'])}.
    
    **Top Sender:** **{chat_data['top_sender']}** has sent the most messages ({chat_data['top_sender_count']:,}).
    """
    return report

# --- 3. MAIN STREAMLIT APPLICATION ---

# The start date for the relationship counter
start_date_str = "2023-08-15"

# 3a. Injecting the Custom Header HTML
custom_header_html = f"""
<div class="header-bg p-8 flex flex-col items-center text-center">
    <div class="text-5xl mb-2">💖</div>
    <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight">
        For Drishya - My Love!
    </h1>
    <p class="text-sm font-light opacity-80 mt-2">
        A sweet little project to celebrate us.
    </p>
</div>
"""
st.markdown(custom_header_html, unsafe_allow_html=True)

# 3b. Injecting the Daisy Animation HTML (must be outside the header)
daisies_html = """
<div class="animation-container">
    <div class="daisy daisy-slow" style="left: 10%; animation-delay: 0s;">🌼</div>
    <div class="daisy daisy-medium" style="left: 30%; animation-delay: 3s;">🌸</div>
    <div class="daisy daisy-fast" style="left: 50%; animation-delay: 1s;">🌷</div>
    <div class="daisy daisy-slow" style="left: 70%; animation-delay: 5s;">🌺</div>
    <div class="daisy daisy-medium" style="left: 90%; animation-delay: 2s;">🌹</div>
    <div class="daisy daisy-fast" style="left: 20%; animation-delay: 4s;">💖</div>
    <div class="daisy daisy-slow" style="left: 65%; animation-delay: 7s;">🌼</div>
</div>
"""
st.markdown(daisies_html, unsafe_allow_html=True)


# 3c. Main Content Area (Styled as a card using a container)
with st.container(border=False):
    st.markdown("<div class='mt-10'></div>", unsafe_allow_html=True) # Spacer

    st.subheader("Our Love Counter", divider="rainbow")
    
    # Calculate and display the duration
    duration_str, total_days = calculate_duration_live(start_date_str)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Together for", value=duration_str)
        
    with col2:
        # Custom HTML to make the metric look like a colorful badge
        st.markdown(
            f"""
            <div class="p-3 bg-pink-100 rounded-xl shadow-md text-center">
                <p class="text-xs font-semibold text-pink-600 mb-1">Total Days</p>
                <p class="text-3xl font-bold text-pink-900">{total_days}</p>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("---")
    
    # Random Message Section
    st.subheader("A Sweet Message Box")
    
    MESSAGES = [
        "My heart smiles when you're around. 😊",
        "Every moment with you is my favorite memory. ✨",
        "Thank you for being my constant, beautiful sunshine. ☀️",
        "You are the best thing that ever happened to me. I love you! ❤️",
        "Just a reminder: I'm madly in love with you, Drishya. 🌹"
    ]
    
    if st.button("🌷 Click for a sweet message 🌷"):
        message = random.choice(MESSAGES)
        st.success(f"**A message for you:** {message}")

    st.markdown("---")

    # File Uploader Section
    st.subheader("Chat Data Analysis")
    st.info("Upload your WhatsApp/Telegram chat export (text file) to see fun stats!")
    
    uploaded_file = st.file_uploader("Upload Chat Export (.txt file)", type=["txt", "csv"])
    
    if uploaded_file is not None:
        try:
            # Pass the uploaded file to the mock parser
            with st.spinner('Analyzing your love history...'):
                chat_data = parse_chat(uploaded_file)
                report = analyze_chat_data(chat_data)
                st.markdown(report)
                
            st.balloons()
            
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")

    # Footer/Signature
    st.markdown(
        """
        <div class="mt-10 pt-4 border-t border-pink-300 text-center text-sm text-pink-600">
            Made with all my love ❤️
        </div>
        """, unsafe_allow_html=True
    )ont-size: 20px;}
.daisy:nth-child(3) { animation-delay: 2s; left: 25%; font-size: 30px;}
.daisy:nth-child(4) { animation-delay: 2.5s; left: 35%; font-size: 22px;}
.daisy:nth-child(5) { animation-delay: 3s; left: 45%; font-size: 28px;}
.daisy:nth-child(6) { animation-delay: 3.5s; left: 55%; font-size: 23px;}
.daisy:nth-child(7) { animation-delay: 4s; left: 65%; font-size: 27px;}
.daisy:nth-child(8) { animation-delay: 4.5s; left: 75%; font-size: 21px;}
.daisy:nth-child(9) { animation-delay: 5s; left: 85%; font-size: 26px;}
.daisy:nth-child(10) { animation-delay: 5.5s; left: 95%; font-size: 24px;}
.daisy:nth-child(11) { animation-delay: 6s; left: 2%; font-size: 18px;}
.daisy:nth-child(12) { animation-delay: 6.5s; left: 12%; font-size: 32px;}
.daisy:nth-child(13) { animation-delay: 7s; left: 22%; font-size: 26px;}
.daisy:nth-child(14) { animation-delay: 7.5s; left: 32%; font-size: 20px;}
.daisy:nth-child(15) { animation-delay: 8s; left: 42%; font-size: 25px;}

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
    border-radius: 4px;
    padding: 8px 15px;
    font-size: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# --- Falling Daisies Animation (HTML) ---
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

# --- RELATIONSHIP COUNTER ---
start_date_str = "14/05/2020"
duration_str, total_days = calculate_duration_live(start_date_str)

st.metric(
    label="Our journey since 14/05/2020", 
    value=duration_str, 
    delta=f"{total_days} total days together!"
)
st.markdown("---")
# --- END COUNTER ---

# Floral Tree visual
st.markdown('<div class="love-tree"><div class="tree">🌸🌳🌼</div></div>', unsafe_allow_html=True)

# Messages
messages = [
    "i cant eat you i will get diabetes cuz youre too sweet for even a guju like me 🌼",
    "most percious pookie of all time 🌷",
    "sorry to make you cry last month baby 😊",
    "I love you more every single day 🌸",
    "You’re my baby may you glow everday 💐",
    " your beauty is so glorious by itself its just have its own dimansion to decode not even binary or matrixes can work in it (you called me drunk when i wrte this ) 💫",
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
        msg_list = messages + st.session_state.custom_msgs
        chosen = random.choice(msg_list)
        st.success(chosen)

with col2:
    # Button label changed to floral theme
    if st.button("🌼 Send a daisy"):
        st.session_state.love_clicks += 1
        st.info("Daisy sent! 🌼")

# --- CUSTOM MESSAGE INPUT (MODIFIED SECTION) ---
st.subheader("💬 atheiest me belive in god when i had you ")
# Added a key for better session management
new_msg = st.text_input("here dobi", key="new_note_input") 
if st.button("🌸 write what ever you want to baby") and new_msg: 
    st.session_state.custom_msgs.append(new_msg)
    st.success("Added! Now it’s a beautiful petal in our collection 🌸")
    # New feature: Display the message immediately after saving
    st.info(f"**Just saved:** *{new_msg}*")

# New feature: Display all notes added in the current session
if st.session_state.custom_msgs:
    st.markdown("---")
    st.markdown("#### Notes Written This Session:")
    # Display the most recent notes first
    for i, msg in enumerate(reversed(st.session_state.custom_msgs)):
        st.text(f"🌸 {msg}")
# --- END CUSTOM MESSAGE INPUT ---

# --- WHATSAPP ANALYSIS SECTION (Updated to include logic) ---
st.markdown("---")
st.subheader("📊 Our WhatsApp Chat Analysis (The Story of Us)")
st.caption("Upload your exported WhatsApp chat (.txt file) to see who says 'I love you' more! (Privacy Note: The file is only processed here and not saved.)")

uploaded_file = st.file_uploader("Upload Chat File (.txt)", type=["txt"])

if uploaded_file is not None:
    # Read file content
    bytes_data = uploaded_file.read()
    chat_text = bytes_data.decode("utf-8")
    
    # Define the two user names found in the chat file for analysis (Update this if names change)
    USER_1 = "Little Mouse 💗🌸"
    USER_2 = "Chaitanya ~"

    # Process and Analyze
    with st.spinner("Analyzing our love language..."):
        chat_df = parse_chat(chat_text)
        if not chat_df.empty:
            analysis_results = analyze_chat_data(chat_df, USER_1, USER_2)
            
            st.success(f"Analysis complete! Chat from {analysis_results['start_date']} to {analysis_results['end_date']}.")

            # --- General Stats ---
            colA, colB, colC = st.columns(3)
            colA.metric("Total Messages", analysis_results['total_messages'])
            colB.metric(f"Words by {USER_1.split()[0]}", analysis_results['users'][USER_1]['words'])
            colC.metric(f"Words by {USER_2.split()[0]}", analysis_results['users'][USER_2]['words'])

            # --- Message & Media Breakdown ---
            st.markdown("### Message Volume Breakdown")
            
            msg_data = pd.DataFrame({
                'Metric': ['Total Entries in Chat', 'Text Messages Sent', 'Media (Stickers/Files)', 'Message Deleted 🗑️'],
                USER_1: [
                    analysis_results['users'][USER_1]['messages'],
                    analysis_results['users'][USER_1]['text_sent'], 
                    analysis_results['users'][USER_1]['media'],
                    analysis_results['users'][USER_1]['deleted']
                ],
                USER_2: [
                    analysis_results['users'][USER_2]['messages'],
                    analysis_results['users'][USER_2]['text_sent'],
                    analysis_results['users'][USER_2]['media'],
                    analysis_results['users'][USER_2]['deleted']
                ]
            }).set_index('Metric')
            
            st.table(msg_data)
            
            # --- Pet Name Battle ---
            st.markdown("### The Pet Name Battle 💖")
            
            pet_name_data = []
            for name, counts in analysis_results['pet_names'].items():
                pet_name_data.append({
                    'Pet Name': name.capitalize(),
                    USER_1: counts[0],
                    USER_2: counts[1]
                })
            
            df_pet_names = pd.DataFrame(pet_name_data).set_index('Pet Name')
            st.table(df_pet_names)
            
            # Highlight the winner of "baby"
            winner = USER_1 if df_pet_names.loc['Baby', USER_1] > df_pet_names.loc['Baby', USER_2] else USER_2
            st.info(f"The winner of the **'Baby'** award is: **{winner.split()[0]}!**")
            
            
            # --- Detailed Breakdown (Expander) ---
            with st.expander("More Detailed Insights"):
                
                st.markdown("#### Top 10 Most Used Words (Excluding stop words & emojis) 📜")
                words_df = pd.DataFrame(analysis_results['top_words'], columns=['Word', 'Count'])
                st.table(words_df)
                st.caption("Find your unique love vocabulary! 😊")

                st.markdown("#### Hourly Activity Chart 🕰️")
                # Add a column for the 24-hour clock label (e.g., 0 for 12 AM, 13 for 1 PM)
                analysis_results['hourly_activity']['Time (24h)'] = analysis_results['hourly_activity']['Hour'].astype(str) + ':00'
                
                st.bar_chart(analysis_results['hourly_activity'].set_index('Time (24h)'))
                st.caption("Find out your peak hour of love! (0 is 12:00 AM, 23 is 11:00 PM)")

        else:
            st.error("Could not parse any messages from the uploaded file. Please ensure the chat was exported without media.")

# --- END ANALYSIS SECTION ---

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
    label="Download All Notes ",
    data=download_data.encode('utf-8'),
    file_name=f"LoveNotes_History_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
    mime="text/plain",
    key="admin_download_key"
)

# Use st.markdown to close the fixed container
st.markdown('</div>', unsafe_allow_html=True)


# If the love button was clicked, render a temporary floating flower animation
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
    const trigger = {trigger};
    if (!trigger) return;
    const container = document.getElementById('heart-container');
    container.innerHTML = '';
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

# Embed the HTML.
components.html(floating_hearts_html, height=1)

st.write('---')
st.caption(f"Made by loving husband🌼 for you — {datetime.now().year}")
