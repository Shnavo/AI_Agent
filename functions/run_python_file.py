import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)
    arguments = ["python", abspath]
    arguments.extend(args)

    if not (abspath == abs_working_path or abspath.startswith(abs_working_path + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abspath):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(arguments, timeout=30, capture_output=True, cwd=abs_working_path, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    final = f'STDOUT: \n{result.stdout}STDERR: {result.stderr}'
    if result.stdout == "" and result.stderr == "":
        return "No output produced."
    if result.returncode != 0:
        final += f"\nProcess exited with code {result.returncode}"
    return final
    

