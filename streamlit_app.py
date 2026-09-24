import sqlite3
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="Medical Emergency Assistance", page_icon="+", layout="centered")

st.markdown(
    """
    <style>
        :root { --navy: #103b66; --blue: #1769aa; --pale-blue: #eaf5ff; }
        .stApp { background: #ffffff; color: var(--navy); }
        [data-testid="stHeader"] { background: #ffffff; }
        h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] { color: var(--navy) !important; }
        .hero { padding: 1.2rem 0 0.6rem; }
        .hero img { width: 100%; height: 230px; object-fit: cover; border-radius: 14px; }
        .hero-caption { margin-top: -3.8rem; padding: 1rem 1.3rem; position: relative; color: white; }
        .hero-caption h1, .hero-caption p { color: white !important; margin: 0; }
        .hero-caption h1 { font-size: 2rem; }
        .queue-number { background: var(--pale-blue); border: 2px solid #8bc7f2; border-radius: 14px; padding: 1rem; text-align: center; }
        .queue-number strong { color: var(--blue); font-size: 3rem; display: block; }
        div.stButton > button { background: var(--blue); color: white; border: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


def next_queue_number():
    """Reserve the next number safely when submissions arrive together."""
    database_path = Path(__file__).with_name("queue_numbers.db")
    with sqlite3.connect(database_path, timeout=10) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS queue (id INTEGER PRIMARY KEY AUTOINCREMENT)")
        connection.execute("INSERT INTO queue DEFAULT VALUES")
        return connection.execute("SELECT last_insert_rowid()").fetchone()[0]


st.markdown(
    """
    <div class="hero">
        <img src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1400&q=85" alt="Doctor speaking with a patient">
        <div class="hero-caption">
            <h1>Medical Emergency Assistance</h1>
            <p>Tell us a little about yourself so we can help you in order.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("Please complete every field below.")
name = st.text_input("What is your name?", key="name")
contact = st.text_input("What is your contact number?", key="contact")
email = st.text_input("What is your email address?", key="email")
repeat_email = st.text_input("Please repeat your email address:", key="repeat_email")
sickness = st.selectbox(
    "What is your medical condition?",
    ["Select a condition", "Heart Attack", "Stroke", "Severe Bleeding", "Other"],
    key="sickness",
)
pain_level = st.slider("How much pain are you currently feeling?", 0, 10, 0, key="pain_level")

emails_match = email.strip() and repeat_email.strip() and email.strip().casefold() == repeat_email.strip().casefold()
form_complete = bool(name.strip() and contact.strip() and emails_match and sickness != "Select a condition")

if email.strip() and repeat_email.strip() and not emails_match:
    st.error("The email addresses do not match.")

if form_complete:
    if "queue_number" not in st.session_state:
        st.session_state.queue_number = next_queue_number()

    st.markdown(
        f'<div class="queue-number">Your place in line is:<strong>{st.session_state.queue_number}</strong>'
        "Please keep this number to see when it is your turn to see a doctor.</div>",
        unsafe_allow_html=True,
    )
