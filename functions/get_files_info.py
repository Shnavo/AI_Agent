import os


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abspath = os.path.abspath(full_path)

    if working_directory not in abspath:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if os.path.isfile(directory):
        return f'Error: "{directory}" is not a directory'
    
    answer = ""
    for item in os.listdir(abspath):
        try:
            item_path = os.path.join(abspath, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
        except OSError as e:
            print(f'Error: {e}')
        answer += f"{item}: file_size={size} bytes, is_dir={is_dir}\n"
    return answer

    
    

# get_files_info("calculator", ".")
# get_files_info("calculator", "pkg")
# result = get_files_info("calculator", "tests")
# result = get_files_info("calculator", "/bin")

# print(result)