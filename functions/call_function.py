from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    function_args = function_call_part.args

    if function_name == "get_files_info":
        function_result = get_files_info(**function_args)
    elif function_name == "get_file_content":
        function_result = get_file_content(**function_args)
    elif function_name == "write_file":
        function_result = write_file(**function_args)
    elif function_name == "run_python_file":
        function_result = run_python_file(**function_args)
    else:  
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
            )
        ],
    )



    # match function_name:
    #     case get_files_info:
    #         get_files_info(**function_args)
    #     case get_file_content:
    #         get_file_content(**function_args)