import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    
    return_list = []

    full_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(full_path)
    abs_path_working = os.path.abspath(working_directory)

    if not abs_path.startswith(abs_path_working):
        return f'Error: Cannot list "{directory}" as it is outside the working directory'
    
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'

    files_list = os.listdir(abs_path)

    for file in sorted(files_list):
        file_path = os.path.join(abs_path, file)

        try:
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            return_list.append(f'- {file}: file_size={file_size} bytes, is_dir={is_dir}')
        
        except Exception as e:
            return_list.append(f'Error: {str(e)}')

    return "\n".join(return_list)