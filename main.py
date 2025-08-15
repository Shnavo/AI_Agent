import sys
import os
from dotenv import load_dotenv
from google.genai import types
from google import genai
from config import system_prompt
from call_function import call_function, available_functions

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
    i=0
    while i<20:
        i+=1
        try:
            response = generate_content(client, messages, verbose, user_prompt)
            for candidate in response.candidates:
                messages.append(
                    types.Content(
                        role="user", 
                        parts=[types.Part(text=str(candidate.content))]
                    )
                )
        except Exception as e:
            print("there was a problem:", e)
        if response.text:
            print(response.text)
            break

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
    return response


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

if __name__ == "__main__":
    main()
