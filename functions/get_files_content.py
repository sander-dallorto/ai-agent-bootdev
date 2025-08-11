import os 
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a specified file. If the file has more than 10,000 characters, the content is truncated at that limit.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path to the desired file."
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path)
    file_path = os.path.abspath(full_path)
    working_directory = os.path.abspath(working_directory)

    if not file_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the working directory'
    
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'   
    
    MAX_CHARS = 10000
    
    try:
        with open(file_path, 'r') as f:
            file_content_string = f.read(MAX_CHARS + 1) # read up to MAX_CHARS + 1 to check for truncation

    except Exception as e:
        return f'Error: {str(e)}'

    if len(file_content_string) > MAX_CHARS:
        file_content_string_10k = file_content_string[:MAX_CHARS]
        file_content_string_10k += f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string_10k

    return file_content_string  