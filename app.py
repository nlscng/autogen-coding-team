import streamlit as st

st.title("My Coding Team Agents!")

default_task = "What is the 18th prime number?"

task = st.text_area("Task: ", default_task)

clicked: bool = st.button("Run!")

chat = st.container()

if clicked:
    chat.empty()
    with chat:
        st.write("Running task...")