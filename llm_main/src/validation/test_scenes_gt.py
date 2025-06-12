import pandas as pd
import ast
import os
import json
from collections import defaultdict
from screenplay_breakdown.src.final_text_id_mappings import enrich_with_ids
from screenplay_breakdown.src.utility import get_prompt_structure_recognition, get_prompt_production_categories, enrich_with_ids_struct_recog, get_prompt_production_categories_revised
from common_utilities.src.main.llm_calling import LLMFactory
import fitz
import json
import dotenv
from constants import task_name, model_name


llm_client = LLMFactory.get_client(model_name)





# Categories to evaluate
categories = ["ANIMALS", "SET", "PROPS", "STUNTS", "VEHICLES", "CAST", "NUDITY", "GREENERY", "SOUND"]




def process_scenes(output_json_dir, csv_path):

    # Initialize metrics and row-level results
    row_results = []
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
            if task_name == "prod_recog":
                prompt, sys_prompt = get_prompt_production_categories_revised(ALL_TEXT)
                
            scene_data = llm_client.generate_response(prompt, sys_prompt)
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

if __name__ == "__main__":
        # Read input CSV
    csv_path = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_jun10/prod_reco_gt.csv"
    output_json_dir = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_jun10/outputs"
    output_csv_path = "metrics_output.csv"
    process_scenes(output_json_dir, csv_path)
