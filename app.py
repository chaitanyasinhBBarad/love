import streamlit as st
import datetime
import random
import re
import pandas as pd

# --- 1. CONFIGURATION AND STYLING INJECTION (The "Escape Hatch") ---

# Tailwind CSS and Google Fonts setup (UPDATED FONTS)
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Custom CSS for Background, Card, Daisy Effect, and Streamlit Overrides
st.markdown("""
<style>
    /* Custom Fonts for global use */
    :root {
        --primary-font: 'Roboto', sans-serif; /* For body text */
        --display-font: 'Pacifico', cursive; /* Applied "My Sunshine Font" */
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
        font-family: var(--display-font); /* Apply fancy font to Streamlit headings */
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

    /* NEW FLOWER GALLERY STYLING */
    .flower-card {
        background-color: white;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1), 0 0 5px rgba(255, 100, 150, 0.15);
        text-align: center;
        transition: transform 0.3s ease;
        border: 2px solid #ffccd5;
    }
    .flower-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2), 0 0 10px rgba(255, 64, 129, 0.5);
    }
    .flower-emoji {
        font-size: 4rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    .flower-title {
        font-family: var(--display-font);
        font-size: 1.25rem;
        color: #ff4081;
    }
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
    
    # --- NEW FLOWER BOUQUET GALLERY SECTION ---
    
    st.subheader("🌷 A Garden Just For You", divider="rainbow")
    
    # Data for the bouquets (Flower emoji, Name/Title)
    bouquets = [
        ("🌹", "Endless Love"),
        ("💐", "Pure Joy"),
        ("🌸", "Sweet Beginnings"),
        ("🌻", "My Sunshine"),
        ("🌼", "Innocence & Truth"),
        ("🌷", "Perfect Match"),
    ]
    
    # Custom HTML for the responsive flower grid
    bouquet_html = """
    <div class="grid grid-cols-2 md:grid-cols-3 gap-6 my-8">
    """
    
    for emoji, title in bouquets:
        bouquet_html += f"""
        <div class="flower-card">
            <span class="flower-emoji">{emoji}</span>
            <p class="flower-title">{title}</p>
        </div>
        """

    bouquet_html += "</div>"
    
    st.markdown(bouquet_html, unsafe_allow_html=True)
    
    st.markdown("<p class='text-center text-sm text-pink-700 mb-6'>Each flower represents a beautiful part of our journey together! Click the message box for a little extra love.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    # --- END NEW BOUQUET GALLERY SECTION ---
    
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
    )
    
