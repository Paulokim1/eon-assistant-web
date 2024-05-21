import json
import os
import secrets
import string
from typing import List

import requests
import streamlit as st
from dotenv import load_dotenv

from tools.htmlTemplates import bot_template, css, user_template

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_URL = os.getenv("API_URL")


def gen_random_id(size=28):
    """Generate a random string of letters and digits."""
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(size))


def handle_userinput(user_question):
    """Handle user input and send it to the chatbot API."""
    reqUrl = API_URL

    headersList = {
        "Accept": "*/*",
        "Authorization": AUTH_TOKEN,
        "Content-Type": "application/json",
    }

    payload = json.dumps({"session_id": st.session_state.session_id, "message": user_question})

    response = requests.request("POST", reqUrl, data=payload, headers=headersList)
    output = response.text

    st.session_state.chat_history.append(user_question)
    st.session_state.chat_history.append(output)

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)


### MAIN FUNCTION ###
def main():
    load_dotenv()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if 'session_id' not in st.session_state:
        st.session_state.session_id = gen_random_id()

    st.set_page_config(page_title="EON Assistant", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    st.write(f"Session id: {st.session_state.session_id}")
    
    prompt = st.chat_input("Say something")
    if prompt:
        with st.spinner("Loading..."):
            handle_userinput(prompt)


if __name__ == "__main__":
    main()
