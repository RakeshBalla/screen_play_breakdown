import os
import dotenv
import re
import json
import re
from openai import OpenAI

# Load environment variables
dotenv.load_dotenv()
# api_key_ge = os.getenv("GEMINI_API_KEY")
api_key_ge = 'AIzaSyCe4MP9KyzILCFOFnMn1BX_b57tzzjwvls'


client = OpenAI(
    api_key=api_key_ge,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def llm_response(prompt, sys_prompt):
    """
    Generate a response from the language model based on the provided prompt and system prompt.
    Parameters
    ----------
    prompt : str
        The user prompt to be processed by the language model.
    sys_prompt : str
        The system prompt to guide the language model's behavior.
    Returns
    -------
    str
        The generated response from the language model.
    """
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": sys_prompt},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    answer = response.choices[0].message.content
    # print(answer)
    print('formattted_res:', answer)
    return answer

sys_prompt = 'You Are a Usefull Assistent'
prompt = 'Tell Me About The Knowledge Distillation'
ans_ = llm_response(prompt, sys_prompt)
print(ans_)