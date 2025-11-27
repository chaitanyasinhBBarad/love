import streamlit as st

import random

from datetime import datetime

import streamlit.components.v1 as components

import re

import pandas as pd

from collections import Counter

import io # Added for file handling



# --- Python functions for chat analysis logic ---



def parse_chat(chat_text):

    """

    Parses WhatsApp chat text into a structured list of messages.

    Handles multi-line messages and identifies key omissions.

    """

    # Regex pattern to match a standard WhatsApp message line: [DD/MM/YY, HH:MM:SS AM/PM] Sender: Message

    pattern = re.compile(r'^\[(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2} (?:AM|PM))\] (.+?): (.*)$')

    messages = []

    

    # Clean up the text: remove the byte order mark and split lines

    text = chat_text.strip().replace('\ufeff', '')

    

    current_message = None



    # Using io.StringIO to treat the string as a file object for line-by-line reading

    for line in io.StringIO(text):

        line = line.strip()

        if not line:

            continue

            

        match = pattern.match(line)

        

        if match:

            # Start of a new message

            timestamp_str, sender, message_content = match.groups()

            

            # Skip the system message

            if message_content.startswith('‎Messages and calls are end-to-end encrypted'):

                continue 



            current_message = {

                'Timestamp': datetime.strptime(timestamp_str, '%d/%m/%y, %I:%M:%S %p'),

                'Sender': sender.strip(),

                'Message': message_content.strip()

            }

            messages.append(current_message)

            

        elif current_message:

            # Continuation of a multi-line message

            current_message['Message'] += ' ' + line



    return pd.DataFrame(messages)





def analyze_chat_data(df, user_1, user_2):

    """Performs core analysis on the chat DataFrame."""

    if df.empty:

        return None



    # --- Core Metrics ---

    total_messages = len(df)

    messages_1 = df[df['Sender'] == user_1]

    messages_2 = df[df['Sender'] == user_2]

    

    # --- Identify Special Message Types (Media & Deleted) ---

    

    # Identify Deleted Messages

    deleted_msgs_1 = messages_1['Message'].str.contains('This message was deleted', na=False, case=False).sum()

    deleted_msgs_2 = messages_2['Message'].str.contains('This message was deleted', na=False, case=False).sum()



    # Identify Media Messages (Media messages will typically say "omitted" or similar)

    media_msgs_1 = messages_1['Message'].str.contains('omitted', na=False, case=False).sum()

    media_msgs_2 = messages_2['Message'].str.contains('omitted', na=False, case=False).sum()



    # --- Filter messages down to only TEXT content for word counting & pet name counting ---

    # We use a combined filter to ensure accuracy.

    text_filter = ~df['Message'].str.contains('omitted|deleted', na=False, case=False)

    

    messages_1_text_only = df[df['Sender'] == user_1][text_filter]

    messages_2_text_only = df[df['Sender'] == user_2][text_filter]

    

    # Total text messages sent is the count of messages that are NOT media or deleted

    text_messages_sent_1 = len(messages_1_text_only)

    text_messages_sent_2 = len(messages_2_text_only)



    # --- Word Counting and Cleaning ---

    

    # Custom stop words (English + common chat filler/emojis)

    STOP_WORDS = set([

        'a', 'an', 'the', 'is', 'am', 'are', 'was', 'were', 'and', 'but', 'or', 'to', 'of', 'in', 'on', 'it', 'i', 'you', 

        'my', 'me', 'at', 'that', 'this', 'we', 'he', 'she', 'they', 'what', 'who', 'when', 'where', 'why', 'how', 'do', 

        'did', 'will', 'have', 'had', 'for', 'just', 'too', 'nah', 'yk', 'cuz', 'af', 'your', 'with', 'even', 'one', 'be',

        'omitted', 'sticker', 'image', 'video', 'audio', 'gif', 'media', 'messages', 'calls', 'are', 'endtoend', 'encrypted',

        # Common emojis/tokens found in this specific chat

        '😂😂😂', '😂', '😂😂', '😂😂😂😂', '🥹', '✨', '🤧', '🫠', '🤌', '🫡', '🤝', '💗', '🌸', '~', 'msg', 'deleted', 'this'

    ])



    def get_word_counts(messages_df):

        text = ' '.join(messages_df['Message'].astype(str).str.lower())

        # Clean text: remove punctuation but keep spaces for tokenization

        text = re.sub(r'[^a-z0-9\s]', '', text) 

        words = text.split()

        

        # Filter out stop words and single-letter tokens

        filtered_words = [word for word in words if word not in STOP_WORDS and len(word) > 1]

        # Total words is the count before stop word filtering

        return Counter(filtered_words), len(words) 



    # Get word counts for each user (using text-only filtered data)

    counter_1, total_words_1 = get_word_counts(messages_1_text_only)

    counter_2, total_words_2 = get_word_counts(messages_2_text_only)

    

    # Combine counters for total top words

    total_counter = counter_1 + counter_2

    

    # --- Date & Time Metrics ---

    start_date = df['Timestamp'].min().strftime('%d %B %Y')

    end_date = df['Timestamp'].max().strftime('%d %B %Y')

    

    # Hourly Activity

    hourly_activity = df.groupby(df['Timestamp'].dt.hour)['Message'].count().reset_index()

    hourly_activity.columns = ['Hour', 'Message Count']

    

    # --- Pet Name Counts (Case-Insensitive) ---

    def count_pet_name(df_messages, term):

        # Count pet names in text-only messages to avoid counting in "Media omitted"

        return df_messages['Message'].str.lower().str.contains(r'\b' + re.escape(term) + r'\b', na=False).sum()



    pet_names = {

        'baby': (count_pet_name(messages_1_text_only, 'baby'), count_pet_name(messages_2_text_only, 'baby')),

        'love': (count_pet_name(messages_1_text_only, 'love'), count_pet_name(messages_2_text_only, 'love')),

        'darling': (count_pet_name(messages_1_text_only, 'darling'), count_pet_name(messages_2_text_only, 'darling')),

        'sweetheart': (count_pet_name(messages_1_text_only, 'sweetheart'), count_pet_name(messages_2_text_only, 'sweetheart')),

        'dobi': (count_pet_name(messages_1_text_only, 'dobi'), count_pet_name(messages_2_text_only, 'dobi'))

    }



    # --- Final structured results ---

    results = {

        'total_messages': total_messages,

        'start_date': start_date,

        'end_date': end_date,

        'users': {

            user_1: {

                'messages': len(messages_1), # Total entries

                'words': total_words_1, # Word count from text-only entries

                'text_sent': text_messages_sent_1,

                'media': media_msgs_1,

                'deleted': deleted_msgs_1

            },

            user_2: {

                'messages': len(messages_2),

                'words': total_words_2,

                'text_sent': text_messages_sent_2,

                'media': media_msgs_2,

                'deleted': deleted_msgs_2

            }

        },

        'top_words': total_counter.most_common(10),

        'hourly_activity': hourly_activity,

        'pet_names': pet_names

    }

    

    return results



# Set page icon to a daisy

st.set_page_config(page_title="🌼", page_icon="🌼", layout="centered")



# --- Python functions for app logic ---



def calculate_duration_live(start_date_str):

    """Calculates and formats the relationship duration from the start date to now."""

    start_date = datetime.strptime(start_date_str, '%d/%m/%Y')

    today = datetime.now()

    delta = today - start_date



    total_seconds = int(delta.total_seconds())

    

    # Approximate years/months based on seconds for a friendly display

    years = total_seconds // (365 * 24 * 3600)

    remaining_seconds = total_seconds % (365 * 24 * 3600)

    

    # Using 30 days as a standard for a month approximation

    months = remaining_seconds // (30 * 24 * 3600)

    remaining_seconds = remaining_seconds % (30 * 24 * 3600)

    

    days = remaining_seconds // (24 * 3600)

    remaining_seconds = remaining_seconds % (24 * 3600)

    

    hours = remaining_seconds // 3600

    

    duration_str = f"{years} years, {months} months, {days} days, {hours} hours"

    

    return duration_str, delta.days



# --- CSS for background, falling daisies, and general styling ---

st.markdown("""

<style>

/* --- Main Background (Set to Pink Gradient) --- */

html, body, [data-testid="stAppViewContainer"] > .main {

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



/* --- Falling Daisy Animation --- */

.daisy-container {

    position: fixed;

    top: 0;

    left: 0;

    width: 100%;

    height: 100%;

    pointer-events: none;

    overflow: hidden;

    z-index: 5; 

    opacity: 0.7; 

}

.daisy {

    position: absolute;

    color: #FFF; 

    font-size: 20px;

    opacity: 0; 

    animation: daisyFall 20s linear infinite; 

    text-shadow: 0 0 5px rgba(255, 255, 255, 0.9);

}

@keyframes daisyFall {

    0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }

    10% { opacity: 0.9; }

    100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }

}

/* Staggering daisy animation delays (Retained from user's file) */

.daisy:nth-child(1) { animation-delay: 0s; left: 5%; font-size: 25px;}

.daisy:nth-child(2) { animation-delay: 1.5s; left: 15%; font-size: 20px;}

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
