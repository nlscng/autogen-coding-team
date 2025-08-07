import streamlit as st
from two_agent_coding_team import run, team_config
import asyncio
import os

st.title("My Coding Team Agents!")

default_task = "What is the 18th prime number?"

task = st.text_area("Task: ", default_task)

clicked: bool = st.button("Run!")

chat = st.container()

if clicked:
    # clear out chat from previous runs if any
    chat.empty()

    async def run_task(task):
        with st.spinner("Running..."):
            team, docker = await team_config()
            with chat:
                async for one_message in run(team, docker, task):
                    if one_message.startswith("CodeDeveloper"):
                        with st.chat_message("ai"):
                            st.markdown(one_message)
                    elif one_message.startswith("CodeExecutor"):
                        with st.chat_message("user"):
                            st.markdown(one_message)

                    if 'GENERATED' in one_message:
                        # extract filename
                        filename = one_message.split('GENERATED:')[1].strip()[0]
                        filepath = os.path.join('temp', filename)
                        if os.path.exists(filepath):
                            st.image(filepath)
                        else:
                            st.write(f"File {filepath} not found.")

    asyncio.run(run_task(task))