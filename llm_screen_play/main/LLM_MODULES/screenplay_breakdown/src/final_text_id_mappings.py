import re
import pprint
import os
import json
from pathlib import Path
import re
import random


# Input data
# scene_data = {'scene_number': ['13'], 'slugline': {'type': ['EXT.'], 'location': ['RUINED TEMPLE'], 'time_of_day': ['NIGHTFADE IN.']}, 'action_lines': ['On the edge of a platform in tattered,\ndishevelled rags, two bums, SURESH and a mute BUM, are\nsmoking up using chillams and listening to the Gita on the\nradio. The mute BUM is slow-dancing against a female\nmannequin torso stuck in the middle of a tree.', 'SURESH takes the radio and opens a compartment in the back.\nHe takes out some weed from it, puts it in his chillam, and\ncontinues smoking up.'], 'dialogue': [{'character': ['RADIO'], 'extension': ['(V.O.)'], 'parenthetical': [None], 'text': ['Jaatasya hi dhruvo martyurdhruvaam\njanma martasya cha\ntasmaadaparihaaryerthe na tvam\nsochitumarhasi. Puttina vaaniki\nmaranamu tappadhu. Maraninchina\nvaaniki janmamu tappadhu.\nAnivaaryamagu ee vishayamunu\ngoorchi Sokimpa tagadhu.']}], 'transitions': ['CUT TO:'], 'shot_directions': [], 'superimpose': ['2009.']}
scene_data = {
    "scene_number": [
      16
    ]}
in_data = {
    "1000": "CREDITS",
    "1001": "START.",
    "1002": "1",
    "1003": "EXT.",
    "1004": "VAST",
    "1005": "GRASSLAND",
    "1006": "-",
    "1007": "NIGHT",
    "1008": "A",
    "1009": "man",
    "1010": "riding",
    "1011": "a",
    "1012": "horse",
    "1013": "looks",
    "1014": "at",
    "1015": "the",
    "1016": "stars.",
    "1017": "In",
    "1018": "his",
    "1019": "hand",
    "1020": "is",
    "1021": "KRISHNA\u2019s",
    "1022": "box.",
    "1023": "NARRATOR",
    "1024": "Oka",
    "1025": "adbutam",
    "1026": "jarigey",
    "1027": "gadiyelo",
    "1028": "koni",
    "1029": "jeevithaalu",
    "1030": "aa",
    "1031": "kroddhipaati",
    "1032": "samayamlo",
    "1033": "taarumaarai,",
    "1034": "aa",
    "1035": "adhbuthaaniki",
    "1036": "margamu",
    "1037": "chuuputaaru",
    "1038": "CUT",
    "1039": "TO:"
  }

# Sample tokenizer
def tokenize(text):
    return re.findall(r"\b\w+(?:\.\w+)?\b", text)


def custom_tokenize(text):
    tokens = []
    # Match tokens including \n or \n\n
    raw_tokens = re.split(r'(\n\n|\n)', text)

    for token in raw_tokens:
        if token in ['\n', '\n\n']:
            # Treat the newline delimiters as separators
            continue
        else:
            # Split token on spaces to separate words
            words = token.strip().split()
            for word in words:
                # if len(word) > 1:
                if len(word) > 1 and word.strip(',') != '' and word.strip('.') != '':
                    # Remove leading/trailing special characters
                    cleaned_word = re.sub(r'^[^\w]+|[^\w]+$', '', word)
                    # If the cleaned word still contains \n or \n\n inside, split them
                    if '\n\n' in cleaned_word:
                        parts = cleaned_word.split('\n\n')
                        tokens.extend([p for p in parts if p])
                    elif '\n' in cleaned_word:
                        parts = cleaned_word.split('\n')
                        tokens.extend([p for p in parts if p])
                    elif cleaned_word:
                        tokens.append(cleaned_word)
                else:
                    tokens.append(word)
    return tokens

def process_input(tezt):
    # print(tokenize(tezt))
    '''word_data = []
    lines = tezt.split('\n')
    # Step 2: Split each line by spaces and flatten into a list of words
    words = []
    for line in lines:
        # Split line by spaces and filter out empty strings
        line_words = [word for word in line.split() if word]
        words.extend(line_words)
    # Print the list of words
    word_data.append(words)'''
    
    tezt = tezt.replace('\n', ' ')
    tezt = tezt.replace('  ', ' ')
    # Step 2: Split by spaces and remove empty strings
    words = [word for word in tezt.split(' ') if word]
    
    page_dict = {
        # "word_coordinates": [],
        # "words": [],
        "alltext": tezt,
        # "word_coordinates_ids": [],
        "words_ids": {}
    }
    # for wo in words:
    for i, wo in enumerate(words):
        # word_id = random.randint(1000, 9999)
        word_id = str(1000 + i)
        # page_dict["word_coordinates_ids"].append(word_id)
        page_dict["words_ids"][word_id] = wo
    return page_dict


# tezt = "Nee abba! Okka saari... okka saari\nco-operate cheyi GOVARDHAN . Inka\nidi last. Aa tharavaatha nijanga\nokari mohaalu okaram chudaalsina\navasaram undadu."

# print(process_input(tezt)['words_ids'])
# exit('PLLLLLLLLLLLL')


# Recursive function to walk through nested dict/list and add matched IDs

import datetime
def enrich_with_ids(data, word_ids):
    ids_list = list(word_ids.keys())
    words_list = list(word_ids.values())
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            # print(key, '>>>>>>>>>>>>>>>', value)
            enriched = enrich_with_ids(value, word_ids)
            result[key] = enriched
        return result

    elif isinstance(data, list):
        enriched_list = []
        for item in data:
            enriched_list.append(enrich_with_ids(item, word_ids))
        return enriched_list

    elif isinstance(data,(str, int, float, bool, datetime.date, datetime.datetime)):
        # data = "grassland"
        data = str(data)

        tokens = custom_tokenize(data)
        print('tokenize(data) >>>>>>>>>>', tokens)
        res = find_all_sequences_with_ids(tokens, words_list, ids_list)
        # print(res)
        # exit('???????????')
        if len(res):
            # print(res)
            final_res = []
            for id_re in res:
                data_val, matched_ids = id_re
                final_res.append({'value': ' '.join(data_val), 'ids':matched_ids})
                # final_res.append({'value': data_val, 'ids':matched_ids})
            return final_res
        else:
            return [{'value': data, 'ids':['unable to find ids']}]
    else:
        if data == None:
            # For None or unexpected types, just return as is
            return [{"value": 'empty', "ids": []}]
        else:
            return [{'value': data, 'ids':['unable to find ids']}]
            

# Apply enrichment for the scene
# scene = scene_data['scenes'][0]

def find_all_sequences_with_ids(required_items, words_all, ids_all):
    matched_sequences = []
    seen_sequences_ids = set()

    n = len(words_all)
    m = len(required_items)

    # First pass: exact match
    for i in range(n - m + 1):
        if words_all[i:i + m] == required_items:
            matched_words = words_all[i:i + m]
            matched_ids = ids_all[i:i + m]
            seq_key = tuple(matched_ids)
            if seq_key not in seen_sequences_ids:
                matched_sequences.append((matched_words, matched_ids))
                seen_sequences_ids.add(seq_key)

    # Tokenized version of required items
    required_tokens = required_items#' '.join(required_items)
    # required_tokens = tokenize(required_text)

    # Second pass: tokenized string match
    for i in range(n - m + 1):
        candidate_words = words_all[i:i + m]
        candidate_text = ' '.join(candidate_words)
        candidate_tokens = custom_tokenize(candidate_text)
        matched_ids = ids_all[i:i + m]
        
        # print(candidate_tokens)
        # if candidate_tokens == required_tokens:
        if [str(token).lower() for token in candidate_tokens] == [str(token).lower() for token in required_tokens]: #change 1
            seq_key = tuple(matched_ids)
            if seq_key not in seen_sequences_ids:
                matched_sequences.append((candidate_words, matched_ids))
                seen_sequences_ids.add(seq_key)

    return matched_sequences



# enriched_scene = enrich_with_ids(scene_data, in_data)

# # # Print nicely
# print(enriched_scene)#, width=120)
# exit('?????')




def process_json_files(input_folder, output_folder):
    # Ensure output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
      
        updated_final_results = {}
        if filename.endswith('.json'):
            input_path = os.path.join(input_folder, filename)
            
            # Read the JSON file
            with open(input_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}")
                    continue
                
            # Check if page_dict exists
            if 'page_dict' not in data:
                print(f"No page_dict found in {filename}")
                continue
                
            page_dict = data#['page_dict']
            updated_final_results['sample_no'] = page_dict['sample_no']
            updated_final_results['pdf_file_name'] = page_dict['pdf_file_name']
            updated_final_results['alltext'] = page_dict['page_dict']['alltext']
            # Process alltext if it exists
            if 'alltext' in page_dict['page_dict']:
                print("INPUT ALL TEST\n\n")
                print(page_dict['page_dict']['alltext'])
                alltext_result = process_input(str(page_dict['page_dict']['alltext']))
                print('OUTPUT ALL TEXT\n\n')
                print(alltext_result)
                words_ids_ = alltext_result['words_ids']
                updated_final_results['words_ids'] = words_ids_
                
            else:
                print(f"No alltext found in {filename}")
                alltext_result = {}
                
            # Process llm_response if it exists
            if 'llm_response' in page_dict:
                updated_final_results['llm_response'] = page_dict['llm_response']
              
                enrich_llm_result = enrich_with_ids(page_dict['llm_response'], words_ids_)
            else:
                print(f"No llm_response found in {filename}")
                enrich_llm_result = {}
            updated_final_results['response_mapping_wordIds'] = enrich_llm_result
            
            # Save to output folder
            output_path = os.path.join(output_folder, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(updated_final_results, f, indent=2)
                
            print(f"Processed and saved: {filename}")
        # exit('PLLLLLLLLLLLLL')
        
if __name__ == "__main__":
    # Example usage
    input_folder = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_samples/results/prod_recog/updated_prompt_json_files"
    output_folder = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_samples/results/prod_recog/updated_prompt_json_files_itr2"
    process_json_files(input_folder, output_folder)

