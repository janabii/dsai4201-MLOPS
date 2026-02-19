# support_bot/ui.py
import requests
import streamlit as st

API_BASE = st.secrets.get("API_BASE", "http://localhost:8000")

st.set_page_config(page_title="Support Bot", page_icon="💬")
st.title("💬 Customer Support Chatbot (Mistral)")

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Session")
    st.write("Session ID:", st.session_state.session_id or "(new)")
    if st.button("Summarize conversation"):
        if st.session_state.session_id:
            r = requests.get(f"{API_BASE}/summary/{st.session_state.session_id}", timeout=30)
            st.info(r.json().get("summary", ""))
        else:
            st.info("Send a message first to start a session.")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_text = st.chat_input("Type your message…")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    payload = {"inquiry": user_text, "session_id": st.session_state.session_id}
    r = requests.post(f"{API_BASE}/chat", json=payload, timeout=60)
    data = r.json()

    st.session_state.session_id = data.get("session_id", st.session_state.session_id)
    bot_reply = data.get("response", "(no response)")
    intent = data.get("intent", "unknown")

    st.session_state.messages.append(
        {"role": "assistant", "content": f"{bot_reply}\n\n_Intent: {intent}_"}
    )
    with st.chat_message("assistant"):
        st.markdown(f"{bot_reply}\n\n_Intent: {intent}_")
