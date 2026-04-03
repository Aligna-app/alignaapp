import streamlit as st
import sqlite3
from datetime import datetime

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Aligna", layout="centered")

# -------------------------
# DATABASE
# -------------------------
conn = sqlite3.connect("waitlist.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS waitlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    name TEXT,
    email TEXT,
    user_type TEXT
)
""")
conn.commit()

# -------------------------
# FUNCTIONS
# -------------------------
def save_signup(name, email, user_type):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "INSERT INTO waitlist (timestamp, name, email, user_type) VALUES (?, ?, ?, ?)",
        (timestamp, name, email, user_type)
    )
    conn.commit()

def get_signups():
    return cur.execute("SELECT * FROM waitlist").fetchall()

def email_exists(email):
    result = cur.execute(
        "SELECT * FROM waitlist WHERE email = ?", (email,)
    ).fetchone()
    return result is not None

# -------------------------
# HEADER (PERFECT CENTER)
# -------------------------
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.image("logo.png", width=110)
# -------------------------
# SOCIAL PROOF / URGENCY
# -------------------------
rows = get_signups()
count = len(rows)

if count == 0:
    text = "🔥 Limited beta — only 100 spots"
elif count == 1:
    text = "🔥 1 person already joined"
else:
    text = f"🔥 {count} people already joined"

st.markdown(
    f"<h4 style='text-align: center;'>{text}</h4>",
    unsafe_allow_html=True
)

st.markdown("---")

# -------------------------
# FEATURES
# -------------------------
st.subheader("Why Aligna is different")

col1, col2 = st.columns(2)

with col1:
    st.markdown("✅ AI-curated daily matches")
    st.markdown("✅ No endless swiping")
    st.markdown("✅ Intent-based dating")

with col2:
    st.markdown("✅ Built for ambitious people")
    st.markdown("✅ Higher-quality matches")
    st.markdown("✅ Less time wasted")

st.markdown("---")

# -------------------------
# FORM
# -------------------------
st.subheader("Apply for Early Access")

name = st.text_input("Your name")
email = st.text_input("Email")
user_type = st.selectbox(
    "What best describes you?",
    ["Entrepreneur", "Professional", "Student", "Other"]
)

if st.button("Apply for Early Access"):
    if not name.strip() or not email.strip():
        st.error("Please fill all fields.")
    elif email_exists(email.strip()):
        st.warning("This email is already on the waitlist.")
    else:
        save_signup(name.strip(), email.strip(), user_type)
        st.success("You're in 🚀 We'll notify you when we launch.")

st.info("💡 Designed for serious relationships — not casual swiping")
st.error("⏳ Limited beta: Only 100 spots available")

st.markdown("---")

# -------------------------
# HIDDEN ADMIN PANEL
# Access with: ?admin=true
# Example: https://alignaapp.streamlit.app/?admin=true
# -------------------------
admin_mode = st.query_params.get("admin")

if admin_mode == "true":
    st.markdown("### 🔒 Admin Dashboard")
    password = st.text_input("Enter admin password", type="password")

    if password == "aligna_admin_2026":
        rows = get_signups()
        st.success(f"Total signups: {len(rows)}")
        st.dataframe(rows)

# -------------------------
# FOOTER
# -------------------------
st.caption("Aligna © 2026")
