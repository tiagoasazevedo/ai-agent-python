import os # for environment variables
from dotenv import load_dotenv # to load .env file that contains environment variables
load_dotenv() # take environment variables from .env.
api_key = os.environ.get("GEMINI_API_KEY") # get the API key from environment variables

from google import genai # import the genai library
client = genai.Client(api_key=api_key) # create a client object with the API key

from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

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


def call_function(function_call_part, verbose=False):
    """
    Execute a function call based on the LLM's request.
    
    Args:
        function_call_part: types.FunctionCall with .name and .args properties
        verbose: If True, print detailed information about the function call
        
    Returns:
        types.Content with the function result or error
    """
    function_name = function_call_part.name
    
    # Map of function names to actual function implementations
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    # Print function call information
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if function exists
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Get the function and prepare arguments
    function_to_call = function_map[function_name]
    function_args = dict(function_call_part.args)
    
    # Add working_directory to the arguments
    function_args["working_directory"] = "./calculator"
    
    # Handle None values for args parameter (convert to empty list for run_python_file)
    if function_name == "run_python_file" and function_args.get("args") is None:
        function_args["args"] = []
    
    # Call the function with unpacked keyword arguments
    function_result = function_to_call(**function_args)
    
    # Return the result as a types.Content
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


def main(): # main function to print the response
    verbose = "--verbose" in sys.argv
    
    # Check if the response contains function calls
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call_part = part.function_call
                # Actually call the function
                function_call_result = call_function(function_call_part, verbose=verbose)
                
                # Validate the result has the expected structure
                if not function_call_result.parts or not function_call_result.parts[0].function_response:
                    raise Exception("Function call result does not contain function_response")
                
                # Print the result if verbose
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            elif part.text:
                print(part.text)
    elif response.text:
        print(response.text) # print the generated content to the console
    
    if verbose:
        print(f"User prompt: {user_prompt}") # print the user prompt
        print(f"Prompt tokens: {prompt_tokens}") # print the number of prompt tokens
        print(f"Response tokens: {response_tokens}") # print the number of response tokens


if __name__ == "__main__": # run the main function if this file is executed directly
    main() # call the main function
