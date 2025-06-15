import streamlit as st
import requests
import os
from datetime import datetime

# Load environment variables (optional for Render, required locally)
GH_PAT = os.getenv("GH_PAT")
REPO = os.getenv("REPO", "your-username/abc-eln")
WORKFLOW_FILE = os.getenv("WORKFLOW_FILE", ".github/workflows/dispatch-log.yml")

headers = {
    "Authorization": f"Bearer {GH_PAT}",
    "Accept": "application/vnd.github+json"
}

st.set_page_config(page_title="ABC Lab RA Log")
st.title("🧪 ABC Lab - RA Log Entry")

with st.form("log_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date")
        time = st.time_input("Time")
        pid = st.text_input("Participant ID")
    with col2:
        ra = st.text_input("RA Name")
        tasks = st.text_input("Task Order")
        bonus = st.text_input("Bonus")
    notes = st.text_area("Notes", height=150)
    submitted = st.form_submit_button("📩 Submit Log")

if submitted:
    payload = {
        "ref": "main",
        "inputs": {
            "pid": pid,
            "date": str(date),
            "time": time.strftime("%H:%M"),
            "ra": ra,
            "tasks": tasks,
            "bonus": bonus,
            "notes": notes
        }
    }

    r = requests.post(
        f"https://api.github.com/repos/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches",
        headers=headers,
        json=payload
    )

    if r.status_code == 204:
        st.success("✅ Log successfully submitted and pushed to GitHub!")
    else:
        st.error(f"❌ Failed to submit log. Status code: {r.status_code}")
        st.code(r.text)

