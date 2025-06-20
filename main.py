import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)



if len(sys.argv) < 2:
    print("Please pass the query as an argument.")
    exit(1)
else:
    user_prompt = sys.argv[1]
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]


print(response.text)

prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_cont = response.usage_metadata.candidates_token_count

print("Prompt tokens:", prompt_token_count)
print("Response tokens:", candidates_token_cont)