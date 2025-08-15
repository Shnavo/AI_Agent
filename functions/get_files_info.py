import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abspath = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)

    if not (abspath == abs_working_path or abspath.startswith(abs_working_path + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abspath):
        return f'Error: "{directory}" is not a directory'
    
    answer = []
    if len(os.listdir(abspath)) == 0:
        return "Error: No files found"
    for item in os.listdir(abspath):
        try:
            item_path = os.path.join(abspath, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            answer.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        except OSError as e:
            return f'Error: {e}'
    return "\n".join(answer) 

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
    

# get_files_info("calculator", ".")
# get_files_info("calculator", "pkg")
# result = get_files_info("calculator", "tests")
# result = get_files_info("calculator", "/bin")

# print(result)