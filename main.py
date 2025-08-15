import os
from dotenv import load_dotenv
from google.genai import types
from google import genai
import sys
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function, available_functions

def main():  
    if len(sys.argv) < 2:
        print("no prompt given")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    messages = [
        types.Content(
            role="user", 
            parts=[types.Part(text=user_prompt)]
            ),
    ]

    generate_content(client, messages, verbose, user_prompt)

def generate_content(client, messages, verbose, user_prompt):
        
    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001', 
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    
    pr_tokens = response.usage_metadata.prompt_token_count
    res_tokens = response.usage_metadata.candidates_token_count

    if response.function_calls:
        handle_function_calls(response, verbose)
    else:
        handle_text_response(response, verbose, user_prompt, pr_tokens, res_tokens)


def handle_function_calls(response, verbose):
    function_call_part = response.function_calls[0]
    function_call_part.args['working_directory'] = './calculator'
    
    function_call_result = call_function(function_call_part, verbose=verbose)
    
    if not function_call_result.parts[0].function_response.response:
        raise Exception("Something went wrong")
    
    result = function_call_result.parts[0].function_response.response["result"]
    
    if verbose:
        print(f"-> Result:\n{result}")
    else:
        print(result)

def handle_text_response(response, verbose, user_prompt, pr_tokens, res_tokens):
    if verbose:
        print(f"{response.text}\nUser prompt: {user_prompt}\nPrompt tokens: {pr_tokens}\nResponse tokens: {res_tokens}")
    else:
        print(f"{response.text}")
    elif response.function_calls == None and ("--verbose" in sys.argv):
        print(f"{response.text}\nUser prompt: {user_prompt}\nPrompt tokens: {pr_tokens}\nResponse tokens: {res_tokens}")

if __name__ == "__main__":
    main()
