import os # for environment variables
from dotenv import load_dotenv # to load .env file that contains environment variables
load_dotenv() # take environment variables from .env.
api_key = os.environ.get("GEMINI_API_KEY") # get the API key from environment variables

from google import genai # import the genai library
client = genai.Client(api_key=api_key) # create a client object with the API key

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
) # generate content using the model

def main(): # main function to print the response
    print(response.text) # print the generated content to the console


if __name__ == "__main__": # run the main function if this file is executed directly
    main() # call the main function
