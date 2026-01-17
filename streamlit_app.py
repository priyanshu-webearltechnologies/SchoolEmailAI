import streamlit as st
import requests
import time

# ==============================
# FASTAPI BASE URL
# ==============================
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="School Email Automation",
    page_icon="📧",
    layout="wide"
)

st.title("🏫 School Email Automation Dashboard")

# ==============================
# HELPER FUNCTIONS
# ==============================

def wait_for_completion():
    with st.spinner("⏳ Automation is running..."):
        while True:
            try:
                status = requests.get(f"{API_BASE}/status").json()["status"]
                if status == "completed":
                    break
                time.sleep(2)
            except:
                time.sleep(2)

def show_sent_emails():
    r = requests.get(f"{API_BASE}/logs/sent-emails")
    emails = r.json()

    if not emails:
        st.warning("No sent emails found.")
    else:
        st.success(f"Total Emails Sent: {len(emails)}")
        st.dataframe({"Sent Emails": emails})

def show_replies():
    r = requests.get(f"{API_BASE}/logs/replies")
    replies = r.json()

    if not replies:
        st.warning("No replies received yet.")
    else:
        st.success(f"Total Replies: {len(replies)}")
        st.dataframe({"Replies": replies})

# ==============================
# ACTION BUTTONS
# ==============================

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📤 Send Emails", use_container_width=True):
        requests.post(f"{API_BASE}/send-emails")
        st.success("Email sending started in background")

with col2:
    if st.button("📥 Process Replies", use_container_width=True):
        requests.post(f"{API_BASE}/process-replies")
        st.success("Reply processing started in background")

with col3:
    if st.button("🔁 Run Full Automation", use_container_width=True):
        requests.post(f"{API_BASE}/run-all")
        wait_for_completion()
        st.balloons()
        st.success("🎉 Full automation completed successfully")

st.divider()

# ==============================
# LOG VIEW SECTION
# ==============================

st.subheader("📊 Execution Results")

tab1, tab2 = st.tabs(["📨 Sent Emails", "💬 Incoming Replies"])

with tab1:
    if st.button("🔄 Refresh Sent Emails"):
        show_sent_emails()

with tab2:
    if st.button("🔄 Refresh Replies"):
        show_replies()

st.divider()

# ==============================
# SYSTEM STATUS
# ==============================

try:
    status = requests.get(f"{API_BASE}/status").json()["status"]
    if status == "running":
        st.info("🟡 System Status: Running")
    elif status == "completed":
        st.success("🟢 System Status: Completed")
    else:
        st.info("⚪ System Status: Idle")
except:
    st.error("❌ Cannot connect to FastAPI backend")
