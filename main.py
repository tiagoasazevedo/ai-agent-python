import os # for environment variables
from dotenv import load_dotenv # to load .env file that contains environment variables
load_dotenv() # take environment variables from .env.
api_key = os.environ.get("GEMINI_API_KEY") # get the API key from environment variables

from google import genai # import the genai library
client = genai.Client(api_key=api_key) # create a client object with the API key

from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

import sys # to access command line arguments
user_prompt = sys.argv[1] if len(sys.argv) > 1 else None
if user_prompt is None:
    print("Error: No prompt provided. Please provide a prompt as a command-line argument.")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt
    ),
) # generate content using the model

prompt_tokens = response.usage_metadata.prompt_token_count # get the number of prompt tokens used
response_tokens = response.usage_metadata.candidates_token_count # get the number of response tokens used


def main(): # main function to print the response
    # Check if the response contains function calls
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call_part = part.function_call
                print(f"Calling function: {function_call_part.name}({dict(function_call_part.args)})")
            elif part.text:
                print(part.text)
    elif response.text:
        print(response.text) # print the generated content to the console
    
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}") # print the user prompt
        print(f"Prompt tokens: {prompt_tokens}") # print the number of prompt tokens
        print(f"Response tokens: {response_tokens}") # print the number of response tokens


if __name__ == "__main__": # run the main function if this file is executed directly
    main() # call the main function
