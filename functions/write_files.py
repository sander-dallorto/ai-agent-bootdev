import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes desired content to the specified file.",
    parameters=types.Schema(
        required=["file_path", "content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path to the desired file."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written on the file of choice."
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_path)
    working_directory = os.path.abspath(working_directory)

    if not abs_file_path.startswith(working_directory):
        return f'Error: Cannot write to "{abs_file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        parent_dir = os.path.dirname(abs_file_path)
        os.makedirs(parent_dir, exist_ok=True)
    
    try:
        with open(abs_file_path, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: An error writing on the file has occured: {e}'


