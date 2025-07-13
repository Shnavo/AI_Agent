import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

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

    # print(sys.argv)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001', 
        contents = messages
    )
    pr_tokens = response.usage_metadata.prompt_token_count
    res_tokens = response.usage_metadata.candidates_token_count
    if "--verbose" in sys.argv:
        print(f"{response.text}\nUser prompt: {user_prompt}\nPrompt tokens: {pr_tokens}\nResponse tokens: {res_tokens}")
    else:
        print(f"{response.text}")


if __name__ == "__main__":
    main()
