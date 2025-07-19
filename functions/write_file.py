import os

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)

    if not (abspath == abs_working_path or abspath.startswith(abs_working_path + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abspath):
        try:
            os.mknod(abspath)
        except FileExistsError as e:
            return f'Error: {e}'
    
    try:
        with open(abspath, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except OSError as e:
        return f'Error: {e}'