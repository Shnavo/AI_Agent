import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Missing API key for AI. Check the .env file")
    
    parser = argparse.ArgumentParser(description="Chatbot input message") 
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=args.user_prompt,
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be missing")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
