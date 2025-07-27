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

async def main():
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
            'Once the code executor agent executes the code and you have the results, '
            'you should validate and explain the result, and say exactly the word "TERMINATE"'
            'Never say the "TERMINATE" word before you have the results from the code executor agent.'
        )
    )
    # start docker container before using it
    await docker_executor.start()

    team_chat = RoundRobinGroupChat(
        participants=[code_developer_agent, code_executor_agent],
        termination_condition=TextMentionTermination(text="TERMINATE"),
        max_turns=10,
    )

    # task = 'What is the 18th prime number?'
    task = 'what is the sum of numbers from 1 to 100?'
    async for one_message in team_chat.run_stream(task=task):
        # TaskResult is return when agent run completes, not during the stream, so we handle the them separately
        if isinstance(one_message, TaskResult):
            print(f"Stopping reason: {one_message.stop_reason}")
        else:
            print(f"{one_message.source}: {one_message.content}")
    
    print("Task completed.")


    # stop docker container after use
    await docker_executor.stop()


if __name__ == "__main__":
    asyncio.run(main())
