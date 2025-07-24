from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_core import CancellationToken
import asyncio


async def main():
    docker = DockerCommandLineCodeExecutor(work_dir="~/temp")

    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutor",
        code_executor=docker,
    )

    # start docker container before using it
    await docker.start()

    # format of the md code block is very strict,
    # and there are no spaces between 'python' and 'print'
    code = """```python
print('Hello world from coding agents team!')
```"""

    res = await code_executor_agent.on_messages(
        messages=[TextMessage(content=code, source="user")],
        cancellation_token=CancellationToken(),
    )
    print(res)

    # stop docker container after use
    await docker.stop()


if __name__ == "__main__":
    asyncio.run(main())
