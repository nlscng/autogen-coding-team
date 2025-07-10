from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_core import CancellationToken
import asyncio


async def main():
    docker = DockerCommandLineCodeExecutor(work_dir="~/temp")

    code_executor = CodeExecutorAgent(
        name="CodeExecutor",
        code_executor=docker,
    )

    code = """```python
    print("Hello from autogen-coding-team!")
    ```"""

    res = await code_executor.on_messages(
        messages=[TextMessage(content=code, source="user")],
        cancellation_token=CancellationToken(),
    )
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
