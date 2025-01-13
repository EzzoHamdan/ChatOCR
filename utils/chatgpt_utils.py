# utils/chatgpt_utils.py

from openai import OpenAI
import os

def initialize_client():
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def chatgpt_response(client, prompt):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo"
    )
    reply = response.choices[0].message.content
    return reply
