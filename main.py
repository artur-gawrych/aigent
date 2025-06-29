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

    schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info
        ]
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", help="Specify the prompt.")
    parser.add_argument("--verbose","-v",help="Enable verbosity", action="store_true")
    args = parser.parse_args()

    user_prompt = args.user_prompt

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )

    if response.function_calls:
        for function in response.function_calls:
            print(f"Calling function: {function.name}({function.args})")
    else:
        print(response.text)

    if args.verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()