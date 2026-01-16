

import json
from open_ai_api import get_llm_response
import os


if __name__ == "__main__":
    json_file = "/home/ntlpt19/personal_projects/screen_play_breakdown/llm_screen_play/main/screenplay_breakdown.json"
    output_file = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/screenplay_breakdown"
    os.makedirs(output_file, exist_ok=True)
    with open(json_file, "r") as f:
        content_text = f.read()
    content_text = json.loads(content_text) 
    for page_key, page_content in content_text.items():
        llm_input_content = page_content.get('alltext', '')
        print(f"page_key: {page_key}, llm_input_content: {llm_input_content}")
        response, formattted_res, final_response = get_llm_response(llm_input_content)
        # print(response)
        page_content['llm_response'] = response
        page_content['formatted_response'] = formattted_res
        page_content['page_final_response'] = final_response
        output_file_path = os.path.join(output_file, f"{page_key}.json")
        with open(output_file_path, "w") as output_f:
            json.dump(page_content, output_f, indent=4)
        print(f"Output written to {output_file_path}")
        if page_key == 'page1':
            break
#     # print(content_text)