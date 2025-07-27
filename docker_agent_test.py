from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_core import CancellationToken
import asyncio
import os
import dotenv

async def main():
    docker_executor = DockerCommandLineCodeExecutor(work_dir="~/temp")

    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutor",
        code_executor=docker_executor,
    )

    # start docker container before using it
    await docker_executor.start()

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
    await docker_executor.stop()


if __name__ == "__main__":
    asyncio.run(main())
