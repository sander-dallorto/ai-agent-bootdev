from google.genai import types
from functions.get_files_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_files import write_file

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    else:
        print(f" - Calling function: {function_call_part.name}")

    function_dictionary = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    if function_call_part.name not in function_dictionary:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    function_call_part.args["working_directory"] = "./calculator"
    function = function_dictionary[function_call_part.name]
    function_result = function(**function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )


