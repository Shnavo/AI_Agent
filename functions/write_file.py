import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)

    if not (abspath == abs_working_path or abspath.startswith(abs_working_path + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(os.path.dirname(abspath), exist_ok=True)
        with open(abspath, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content in the designated file in the specified directory, constrained to the working directory. If the file does not exists, creates it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to write or create files in, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)