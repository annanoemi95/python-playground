from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

def talking_with_genai():

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    while True:
        contents = input("> ")
        if contents == "exit":
            break
        else:
            response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=contents
            )
            for chunk in response:
                print(chunk.text, end="\n", flush=True)
            
talking_with_genai()    