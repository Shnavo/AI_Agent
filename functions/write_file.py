import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to an existing file, overwriting the existing file, or creates a new file with the 'file_path' name and fills it with 'content'",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file fill with 'content', relative to the working directory, required to be able to run",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="contents that will be used to fill the specified file"
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_path, file_path))

        if os.path.commonpath([abs_path, target_file_path]) != abs_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error listing files: {e}"
