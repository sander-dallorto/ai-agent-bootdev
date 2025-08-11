import sys
from google.genai import types

if len(sys.argv) < 2:
    print("No prompt provided.")
    sys.exit(1)

user_prompt = sys.argv[1]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""                               

messages = [
    types.Content(
        role="user",
        parts=[types.Part(text=user_prompt)],
    )
]