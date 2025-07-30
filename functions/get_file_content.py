import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)

    if not (abspath == abs_working_path or abspath.startswith(abs_working_path + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abspath):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abspath, "r") as f:
            file_string = f.read(MAX_CHARS + 1)
    except OSError as e:
        return f'Error: {e}'
    
    if len(file_string) > MAX_CHARS:
        return f'{file_string}[...File "{file_path}" truncated at 10000 characters]'
    else:
        return file_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Prints files content in the specified directory truncating if more than 1000 characters, constrained to the working directory.",
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