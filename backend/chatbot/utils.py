# chatbot/utils.py
import os
import openai
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")

openai.api_key = api_key

def ask_openai(prompt, role="user"):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",   # change to "gpt-3.5-turbo" if you want cheaper
            messages=[
                {"role": "system", "content": "You are MavunoLink Assistant, specializing in agriculture, seeds, fertilizers, and dealer information in Kenya. Provide short, clear, and helpful answers."},
                {"role": role, "content": prompt}
            ],
            max_tokens=250,
            temperature=0.6,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "⚠️ Sorry, I couldn't connect to the AI service. Please try again later."
