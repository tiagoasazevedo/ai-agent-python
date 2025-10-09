import os # for environment variables
from dotenv import load_dotenv # to load .env file that contains environment variables
load_dotenv() # take environment variables from .env.
api_key = os.environ.get("GEMINI_API_KEY") # get the API key from environment variables

from google import genai # import the genai library
client = genai.Client(api_key=api_key) # create a client object with the API key

import sys # to access command line arguments
prompt = sys.argv[1] if len(sys.argv) > 1 else None
if prompt is None:
    print("Error: No prompt provided. Please provide a prompt as a command-line argument.")
    sys.exit(1)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt
) # generate content using the model

prompt_tokens = response.usage_metadata.prompt_token_count # get the number of prompt tokens used
response_tokens = response.usage_metadata.candidates_token_count # get the number of response tokens used

def main(): # main function to print the response
    print(response.text) # print the generated content to the console
    print(f"Prompt tokens: {prompt_tokens}") # print the number of prompt tokens
    print(f"Response tokens: {response_tokens}") # print the number of response tokens


if __name__ == "__main__": # run the main function if this file is executed directly
    main() # call the main function
