import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
import argparse
from functions.get_files_info import get_files_info


def main():
        
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", help="Specify the prompt.")
    parser.add_argument("--verbose","-v",help="Enable verbosity", action="store_true")
    args = parser.parse_args()

    user_prompt = args.user_prompt

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

    print(response.text)

    if args.verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()