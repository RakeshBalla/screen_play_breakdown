import pandas as pd
import ast
import os
import json
from collections import defaultdict
from screenplay_breakdown.src.final_text_id_mappings import enrich_with_ids
from screenplay_breakdown.src.utility import  get_prompt_production_categories_revised,process_input
from common_utilities.src.main.llm_calling import LLMFactory
import fitz
import json
import dotenv
from constants import task_name, model_name


llm_client = LLMFactory.get_client(model_name)

def process_scenes(output_json_dir, csv_path):

    row_results = []

    # Ensure output directory exists
    os.makedirs(output_json_dir, exist_ok=True)

    # Load CSV
    df = pd.read_csv(csv_path)

    # Process each row
    for index, row in df.iterrows():
        # Get ALL_TEXT and WORDS_ID
        ALL_TEXT = row["text"]
        WORDS_ID = process_input(ALL_TEXT).get("words_ids", None)
        # WORDS_ID = row["WORDS_ID"]  # Restore WORDS_ID assignment
        SCENE_NUMBER = row["scene_no"]
        print('SCENE_NUMBER %%%%%%%%%%%%%%%%%%%%%%%%', SCENE_NUMBER)
        # WORDS_ID = ast.literal_eval(WORDS_ID)
        # Define JSON file path (using row index as scene number)
        scene_json_path = os.path.join(output_json_dir, f"scene_{SCENE_NUMBER}.json")
        
        # Initialize scene_data and predicted_word_ids
        scene_data = None
        predicted_word_ids = None
        
        # Check if JSON file exists
        if os.path.exists(scene_json_path):
            try:
                with open(scene_json_path, 'r') as f:
                    json_data = json.load(f)
                    scene_data = json_data.get("scene_data", {})
                    predicted_word_ids = json_data.get("predicted_word_ids", {})
            except (json.JSONDecodeError, IOError):
                print(f"Error reading {scene_json_path}. Regenerating data.")
        
        # If JSON file doesn't exist or failed to load, generate data
        if scene_data is None or predicted_word_ids is None:
            if task_name == "prod_recog":
                prompt, sys_prompt = get_prompt_production_categories_revised(ALL_TEXT)
            scene_data = llm_client.generate_response(prompt, sys_prompt)
            predicted_word_ids = enrich_with_ids(scene_data, WORDS_ID)
            
            # Save to JSON
            json_data = {
                "ALL_TEXT": ALL_TEXT,
                "WORDS_ID": WORDS_ID,
                "llm_result": scene_data,
                "predicted_word_ids": predicted_word_ids
            }
            try:
                with open(scene_json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2)
                    print(f"Saved data to {scene_json_path}")                                                                                                                                
            except IOError:
                print(f"Error saving {scene_json_path}")
                

if __name__ == "__main__":
    # Read input CSV
    csv_path = "/home/ntlpt19/personal_projects/screen_play_breakdown_project/screen_data/testing_jun10/Nava_draft_all_scenes.csv"
    output_json_dir = "/home/ntlpt19/personal_projects/screen_play_breakdown_project/screen_data/testing_jun10/Nava_output"
    process_scenes(output_json_dir, csv_path)
