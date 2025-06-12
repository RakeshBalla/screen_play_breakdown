
deep_seek_api = "sk-1aa52e52ef694dd79d8f27625877b579"


# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(
    api_key=deep_seek_api,
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ]
)
print(response.choices[0].message.content)
