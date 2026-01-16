
import os
import dotenv
import re
import json
import re

dotenv.load_dotenv()

# Please install OpenAI SDK first: `pip3 install openai`
deep_seek_api = os.getenv("deep_seek_api")

from openai import OpenAI

client = OpenAI(
    api_key=deep_seek_api,
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "tell me about the weather today"},
    ]
)
print(response.choices[0].message.content)
