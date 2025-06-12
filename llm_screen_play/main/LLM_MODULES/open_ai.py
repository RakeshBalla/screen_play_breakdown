

open_ai_key = "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"

from openai import OpenAI

client = OpenAI(api_key=open_ai_key)  # Replace with your actual key

response = client.chat.completions.create(
    model="gpt-4",  # Or "gpt-4-turbo", "gpt-4o", etc.
    messages=[
        {"role": "user", "content": "Explain how AI works in a few words"}
    ],
    temperature=1,
    max_tokens=2048,
    top_p=1
)

print(response.choices[0].message.content)
