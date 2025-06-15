import streamlit as st
import os
import requests
from streamlit_oauth import OAuth2Component
from datetime import datetime

# Auth0
oauth2 = OAuth2Component(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    authorize_endpoint=os.getenv("AUTHORIZE_URL"),
    token_endpoint=os.getenv("TOKEN_URL"),
    refresh_token_endpoint=os.getenv("REFRESH_TOKEN_URL"),
    revoke_token_endpoint=os.getenv("REVOKE_TOKEN_URL"),
)

# GitHub
GH_PAT = os.getenv("GH_PAT")
REPO = os.getenv("REPO")
WORKFLOW_FILE = os.getenv("WORKFLOW_FILE")

# Authenticate
if "token" not in st.session_state:
    result = oauth2.authorize_button(
        "🔐 Login with Auth0",
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope=os.getenv("SCOPE")
    )
    if result and "token" in result:
        st.session_state["token"] = result["token"]
        st.rerun()
else:
    st.success("✅ Logged in")

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
        headers = {
            "Authorization": f"Bearer {GH_PAT}",
            "Accept": "application/vnd.github+json"
        }

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
            st.success("✅ Log submitted and pushed to GitHub!")
        else:
            st.error(f"❌ Failed: {r.status_code}")
            st.code(r.text)
