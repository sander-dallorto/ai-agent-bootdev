import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments. The file must be a valid .py file located within the allowed working directory.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path to the desired file."
              ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)
    working_directory = os.path.abspath(working_directory)

    if not abs_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not file_path:
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'

    command = ["python", abs_path]

    if args:
        command += args
    
    try:
        result = subprocess.run(command, timeout=30, capture_output=True, cwd=working_directory, text=True)

        return_string = f'STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}'

        if result.returncode != 0:
            return_string += f' Process exited with code {result.returncode}'

        if not result.stdout:
            return_string += " No output produced."

        return return_string

    except Exception as e:
        return f'Error: executing Python file: {e}'

    