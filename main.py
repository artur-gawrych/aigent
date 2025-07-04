import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
import argparse
from functions.get_files_info import get_files_info

from prompts import system_prompt
from call_function import available_functions
from functions.call_functions import call_function

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

    for n in range(1,20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt)
        )
        response_candidates = response.candidates
        for candidate in response_candidates:
            messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_response_content  = call_function(function_call_part, verbose=args.verbose)
                messages.append(function_response_content)
                if not isinstance(function_response_content, types.Content):
                    raise RuntimeError("FATAL EXCEPTION: Missing function response structure.")
                elif args.verbose:
                    print(f"-> {function_response_content.parts[0].function_response.response}")
        else:
            print(response.text)

    if args.verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()