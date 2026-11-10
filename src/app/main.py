import streamlit as st
from src.utils.ask_question import ask_question
from src.config import config

st.set_page_config(page_title=config.APP_NAME, page_icon="🤖")
st.title(config.APP_NAME)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(f"Hello I am {config.APP_NAME}, How can I help you?"):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_question(prompt)
            answer_text = response['answer']            
            st.markdown(answer_text)            
            st.session_state.messages.append({"role": "assistant", "content": answer_text})