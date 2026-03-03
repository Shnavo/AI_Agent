import os
from config_items.config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Provides the content of the selected file within the working directory. If the file is longer than {MAX_CHARS} characters, truncates it to that number",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to read file from, relative to the working directory, required to be able to run",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        print(target_file)
        if os.path.commonpath([abs_path, target_file]) != abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'File not found or is not a regular file: "{file_path}"'
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(MAX_CHARS + 1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error listing files: {e}"