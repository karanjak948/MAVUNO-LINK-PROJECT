import os
import openai
from dotenv import load_dotenv
import logging

# Load .env file
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

# Get and validate OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")

openai.api_key = api_key

def ask_openai(prompt, role="user"):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # use "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant for agricultural products. Provide accurate, short, and simple responses."},
                {"role": role, "content": prompt}
            ],
            max_tokens=250,
            temperature=0.6,
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "Sorry, I'm having trouble connecting to the AI service. Please try again later."
    except Exception as ex:
        logger.exception("Unexpected error in ask_openai")
        return "Unexpected error occurred while processing your request."
