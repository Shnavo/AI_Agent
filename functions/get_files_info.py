import os


def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        info_string = []
        for item in os.listdir(target_dir):
            temp_path = os.path.join(target_dir, item)
            info_string.append(
                f"{item}: file_size={os.path.getsize(temp_path)} bytes, is_dir={os.path.isdir(temp_path)}\n"
                )
        return "\n".join(info_string)
    except Exception as e:
        return f"Error listing files: {e}"
        