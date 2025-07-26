from autogen_agentchat.agents import CodeExecutorAgent, AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_core import CancellationToken
import asyncio


async def main():
    docker_executor = DockerCommandLineCodeExecutor(work_dir="~/temp")

    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutor",
        code_executor=docker_executor,
    )

    model = OpenAIChatCompletionClient(
        model="o3-mini",
        api_key="",
        temperature=0.1,
    )

    code_developer_agent = AssistantAgent(
        name="CodeDeveloper",
        model_client=
        description="An agent that writes code to be executed by the CodeExecutor.",
    )
    # start docker container before using it
    await docker_executor.start()


    # stop docker container after use
    await docker_executor.stop()


if __name__ == "__main__":
    asyncio.run(main())
