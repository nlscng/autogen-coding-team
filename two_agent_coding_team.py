from autogen_agentchat.agents import CodeExecutorAgent, AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.base import TaskResult
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_core import CancellationToken
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
api_key_name = "OPENAI_API_KEY"
# print(f"Using OpenAI API key: {os.getenv(api_key_name)}")
MAX_TURNS = 10

async def team_config():

    docker_executor = DockerCommandLineCodeExecutor(work_dir="~/temp")

    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutor",
        code_executor=docker_executor,
    )

    model = OpenAIChatCompletionClient(
        model="o3-mini",
        api_key=os.getenv(api_key_name),
    )

    code_developer_agent = AssistantAgent(
        name="CodeDeveloper",
        model_client=model,
        description="An agent that writes code to be executed by the CodeExecutor.",
        system_message=(
            'You are a code developer agent, working with a code executor agent.'
            'Your task is to write code that can be executed by the CodeExecutor agent. '
            'You will receive a task and you should write the code to accomplish that task, in python' \
            'or in shell scripts. At the beginning, you should specify your plan to solve the task, '
            'and then write the code to solve the task. '
            'You should always write your code in a code block with python or shell script specified, '
            'and write one code block at a time, and then pass it to the code executor agent.'
            'Once the code executor agent executes the code successfully, and you have the results, '
            'you should validate and explain the result. If an image is generated, you should say exactly "GENERATED:<filename>"' \
            'like "GENERATED:plot.png" '
            'In the end, after code execution is done, and after image displaying is done if an image is '
            'generated, say exactly the word "TERMINATE"'
            'Never say the "TERMINATE" word before you have the results from the code executor agent.'
        )
    )

    team_chat = RoundRobinGroupChat(
        participants=[code_developer_agent, code_executor_agent],
        termination_condition=TextMentionTermination(text="TERMINATE"),
        max_turns=MAX_TURNS,
    )
    return team_chat, docker_executor


async def run(team_chat: RoundRobinGroupChat, docker_executor: DockerCommandLineCodeExecutor, task: str):
    # start docker container before using it
    await docker_executor.start()

    async for one_message in team_chat.run_stream(task=task):
        # TaskResult is return when agent run completes, not during the stream, so we handle the them separately
        if isinstance(one_message, TaskResult):
            print(msg:=f"Stopping reason: {one_message.stop_reason}")
            yield msg
        else:
            print(msg:=f"{one_message.source}: {one_message.content}")
            yield msg
    
    print("Task completed.")

    # stop docker container after use
    await docker_executor.stop()

async def main():

    # task = 'What is the 18th prime number?'
    task = 'what is the sum of numbers from 1 to 100?'
    task = (
        'Toss a fair coin, from 10 times to 1000 times, with step of 10, plot the results, '
        'and save the plot as "plot.png", and then display the plot.'
    )
    team_chat, docker_executor = await team_config()
    async for one_message in run(team_chat, docker_executor, task):
        pass

if __name__ == "__main__":
    asyncio.run(main())
