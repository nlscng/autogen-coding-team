from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors import DockerCommandLineExecutor

docker = DockerCommandLineExecutor(
    working_dir="~/temp"
)

code_executor = CodeExecutorAgent(
    name="CodeExecutor",
    code_executor=docker,
)

code = """```python
print("Hello from autogen-coding-team!")
```"""