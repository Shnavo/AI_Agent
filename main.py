import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():  
    if len(sys.argv) < 2:
        print("no prompt given")
        sys.exit(1)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )
        
    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001', 
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    function_call_part = response.function_calls[0]
    pr_tokens = response.usage_metadata.prompt_token_count
    res_tokens = response.usage_metadata.candidates_token_count
    if "--verbose" in sys.argv:
        print(f"{response.text}\nUser prompt: {user_prompt}\nPrompt tokens: {pr_tokens}\nResponse tokens: {res_tokens}")
    elif response.function_calls != None:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")#{response.function_calls}")
    else:
        print(f"{response.text}")


if __name__ == "__main__":
    main()
