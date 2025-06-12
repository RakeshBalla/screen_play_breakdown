import pandas as pd
import ast
import os
import json
from collections import defaultdict
from screenplay_breakdown.src.final_text_id_mappings import enrich_with_ids
from screenplay_breakdown.src.utility import get_prompt_structure_recognition, llm_response, get_prompt_production_categories, enrich_with_ids_struct_recog, get_prompt_production_categories_revised




def split_list(lst, length):
    return [lst[i:i+length] for i in range(0, len(lst), length)]

def gt_convert(a):
    b = []
    for group in a:
        for item in group:
            value = item['value']
            if 'id' in item:
                ids = [item['id']]
            elif 'ids' in item:
                ids = item['ids']
            ids = [item for sublist in ids for item in sublist]
            value_len = max(1, len(value.split(' ')))
            chunks = split_list(ids, value_len)
            # Generate output
            expanded = []
            id_count = 0
            for chunk in chunks:
                expanded.append({'value': value, 'ids': chunk})
                
                # if chunk:
                #     for id_ in chunk:
                #         expanded.append({'value': value, 'ids': [id_]})
                #         id_count += 1
                # else:
                #     expanded.append({'value': value, 'ids': ['unable to assign ids']})

            b.append(expanded)

    return b

# Function to extract and normalize value-id pairs from ground truth or prediction
def extract_value_id_pairs(data):
    if not data or data == "None" or data == []:
        return set()
    pairs = set()
    
    for item_list in data:
        # For predictions, group items by normalized value
        value_groups = defaultdict(list)
        for item in item_list:
            value = item.get("value", "").strip(",")  # Remove trailing commas
            ids = item.get("id", item.get("ids", []))  # Handle both 'id' and 'ids'
            value_groups[value].extend(ids)
        
        # Combine values and IDs
        for value, ids in value_groups.items():
            # If multiple unique values are similar (e.g., "BUM" and "BUM,"), join with tilde
            unique_values = sorted(set([v.strip(",") for v in value_groups.keys() if v.strip(",")]))
            combined_value = "~".join(unique_values) if len(unique_values) > 1 else value
            combined_ids = tuple(sorted(set(ids)))  # Remove duplicates and sort
            pairs.add((combined_value, combined_ids))
    
    return pairs

def calculate_metrics(actual_pairs, predicted_pairs):
    if not actual_pairs and not predicted_pairs:
        return 0.0, 0.0
    
    # Count exact matches where both value and ids are identical
    correctly_predicted = 0
    finised_pairs = []
    
    for actual in actual_pairs:
        found_flag = False
        for pred in predicted_pairs:
            if pred['value'] == actual['value'] and pred['ids'] == actual['ids'] and pred['ids'] not in finised_pairs:
                correctly_predicted += 1
                finised_pairs.append(pred['ids'])
                found_flag = True
        if not found_flag:
            print(f"Not found: {actual['value']} with ids {actual['ids']}")
    # Calculate precision and recall
    predicted_count = len(predicted_pairs)
    actual_count = len(actual_pairs)
    precision = correctly_predicted / predicted_count if predicted_count > 0 else 0.0
    recall = correctly_predicted / actual_count if actual_count > 0 else 0.0
    
    return precision, recall


# Categories to evaluate
categories = ["ANIMALS", "SET", "PROPS", "STUNTS", "VEHICLES", "CAST", "NUDITY", "GREENERY", "SOUND"]

# Initialize metrics and row-level results
metrics = defaultdict(lambda: {"precision": [], "recall": []})
row_results = []

# Read input CSV
csv_path = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_jun10/prod_reco_gt.csv"
output_json_dir = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_jun10/outputs"
output_csv_path = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_jun10/metrics_output.csv"

# Ensure output directory exists
os.makedirs(output_json_dir, exist_ok=True)

# Load CSV
df = pd.read_csv(csv_path)

# Process each row
for index, row in df.iterrows():
    # Get ALL_TEXT and WORDS_ID
    ALL_TEXT = row["ALL_TEXT"]
    WORDS_ID = row["WORDS_ID"]
    SCENE_NUMBER = row["SCENE_NUMBER"]
    print('SCENE_NUMBER %%%%%%%%%%%%%%%%%%%%%%%%', SCENE_NUMBER)
    WORDS_ID = ast.literal_eval(WORDS_ID)
    # Define JSON file path (using row index as scene number)
    scene_json_path = os.path.join(output_json_dir, f"scene_{SCENE_NUMBER}.json")
    
    # Initialize scene_data and predicted_word_ids
    scene_data = None
    llm_result = None
    
    # Check if JSON file exists
    if os.path.exists(scene_json_path):
        try:
            with open(scene_json_path, 'r') as f:
                json_data = json.load(f)
                # scene_data = json_data.get("scene_data", {})
                scene_data = json_data.get("llm_result", {}).get("production_categories", {})
                llm_result = json_data.get("predicted_word_ids", {}).get("production_categories", {})
        except (json.JSONDecodeError, IOError):
            print(f"Error reading {scene_json_path}. Regenerating data.")
    
    # If JSON file doesn't exist or failed to load, generate data
    if scene_data is None and llm_result is None:
        prompt, sys_prompt = get_prompt_production_categories_revised(ALL_TEXT)
        scene_data = llm_response(prompt, sys_prompt)
        llm_result = enrich_with_ids(scene_data, WORDS_ID)
        
        # Save to JSON
        json_data = {
            "ALL_TEXT": ALL_TEXT,
            "WORDS_ID": WORDS_ID,
            "llm_result": scene_data,
            "predicted_word_ids": llm_result
        }
        try:
            with open(scene_json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
                print(f"Saved data to {scene_json_path}")                                                                                                                                
        except IOError:
            print(f"Error saving {scene_json_path}")
    
    # Print predicted_word_ids as in original code
    # print(predicted_word_ids)
    
    # Initialize row result dictionary
    row_result = {"SCENE_NUMBER": SCENE_NUMBER}
    
    # Evaluate each category
    for category in categories:
        print(f"%%%%%%%%%%%%%%%%%%%%%%%% Processing category: {category}")
        # Get ground truth from *_ID column
        ground_truth_str = row.get(f"{category}", "Empty")
        # try:
        #     ground_truth = ast.literal_eval(ground_truth_str) if ground_truth_str != "None" else []
        # except (ValueError, SyntaxError):
        #     ground_truth = []

        # Get predicted value-id pairs
        predicted_pairs = scene_data.get(f"{category}", "Empty")

        print(ground_truth_str)
        print(predicted_pairs)
        # Store actual and predicted pairs, precision, and recall for this row
        row_result[f"ACTUAL_{category}"] = str(ground_truth_str)
        row_result[f"PREDICTED_{category}"] = str(predicted_pairs)

    # Append row result
    row_results.append(row_result)

# Create DataFrame for row-level results
results_df = pd.DataFrame(row_results)
results_df.to_csv(output_csv_path, index=False)
