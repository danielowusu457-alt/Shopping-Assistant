
import os
from dotenv import load_dotenv
from google import genai

# Load the API key from the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Check whether the API key exists
if not api_key:
    print("Error: Gemini API key was not found.")
else:
    try:
        # Connect to Gemini
        client = genai.Client(api_key=api_key)

        # Send a simple question to Gemini
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents="Introduce yourself in one short sentence."
        )

        # Display Gemini's response
        print("Gemini connection successful!")
        print(response.text)

        client.close()

    except Exception as error:
        print("Gemini connection failed.")
        print("Error details:", error)
