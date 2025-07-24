import os

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