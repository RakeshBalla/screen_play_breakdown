import pandas as pd
import ast
import os
import json
from collections import defaultdict
from screenplay_breakdown.src.final_text_id_mappings import enrich_with_ids
from screenplay_breakdown.src.utility import process_input, get_prompt_production_categories_revised
from common_utilities.src.main.llm_calling import LLMFactory
import fitz
import json
import dotenv
from constants import task_name, model_name
import ast
import math
import pandas as pd  # assuming you're using pandas


llm_client = LLMFactory.get_client(model_name)





# Categories to evaluate
categories = ["ANIMALS", "SET", "PROPS", "STUNTS", "VEHICLES", "CAST", "NUDITY", "GREENERY", "SOUND"]
# categories = ['CAST']


def calculate_metrics(actual_pairs, predicted_pairs):

    actual_set = set(elem.lower() for elem in actual_pairs)
    predicted_set = set(elem.lower() for elem in predicted_pairs)
    print(f"Actual Set: {actual_set}")
    true_positives = actual_set & predicted_set  # Intersection
    print(f"True Positives: {true_positives}")
    precision = len(true_positives) / len(predicted_set) if predicted_set else 0.0
    recall = len(true_positives) / len(actual_set) if actual_set else 0.0

    return precision, recall


def process_scenes(output_json_dir, csv_path, metrics):

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
        WORDS_ID = row.get("WORDS_ID", str({"empty": []}))
        print(WORDS_ID)
        SCENE_NUMBER = row["scene_no"]
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
            WORDS_ID = process_input(ALL_TEXT).get("words_ids", None)
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
            scene_data = scene_data.get("production_categories", {})
        # Print predicted_word_ids as in original code
        # print(predicted_word_ids)
        
        # Initialize row result dictionary
        row_result = {"SCENE_NUMBER": SCENE_NUMBER}
        
        # Evaluate each category
        for category in categories:
            print(f"%%%%%%%%%%%%%%%%%%%%%%%% Processing category: {category}")
            # Get ground truth from *_ID column
            ground_truth_str = row.get(f"{category}", "Empty")
            print(f"Ground Truth for {category}: {ground_truth_str}")
            # Check and handle nan or "None" safely
            if isinstance(ground_truth_str, float) and math.isnan(ground_truth_str):
                ground_truth_str = []
            elif ground_truth_str == "None":
                ground_truth_str = []
            else:
                print(ground_truth_str)
                print('%%%%%%%%%%%%%%%%%%%%%%%%%')
                ground_truth_str = ast.literal_eval(ground_truth_str.strip())
            predicted_pairs = scene_data.get(f"{category}", [])
            print(ground_truth_str)
            print(predicted_pairs)
            if isinstance(predicted_pairs, list) and isinstance(ground_truth_str, list):
                precision, recall = calculate_metrics(set(ground_truth_str), set(predicted_pairs))
            else:
                precision, recall = 0.0, 0.0
                ground_truth_str = []
                predicted_pairs = []
            print(f"Precision: {precision}, Recall: {recall} for category: {category}")
            # exit('>>>>>>')
            
            metrics[category]["precision"].append(precision)
            metrics[category]["recall"].append(recall)
            if len(ground_truth_str) > 0 or len(predicted_pairs) > 0:
                metrics[category]["is_available"].append(True)
            else:
                metrics[category]["is_available"].append(False)
            
            # Store actual and predicted pairs, precision, and recall for this row
            # Store actual and predicted pairs, precision, and recall for this row
            row_result[f"ACTUAL_{category}_ID"] = str(ground_truth_str)
            row_result[f"PREDICTED_{category}_ID"] = str(predicted_pairs)
            row_result[f"{category}_PRECISION"] = precision
            row_result[f"{category}_RECALL"] = recall

        # Append row result
        row_results.append(row_result)
    return row_results, metrics

if __name__ == "__main__":
    metrics_ = defaultdict(lambda: {"precision": [], "recall": [], "is_available": []})

    # Read input CSV
    csv_path = "/home/ntlpt19/personal_projects/screen_play_breakdown_project/screen_data/testing_jun10/prod_reco_gt.csv"
    output_json_dir = "/home/ntlpt19/personal_projects/screen_play_breakdown_project/screen_data/testing_jun10/AK_outputs_gemini_itr2"
    output_csv_path = "metrics_output.csv"
    row_results, metrics = process_scenes(output_json_dir, csv_path, metrics_)
    
    # Create DataFrame for row-level results
    results_df = pd.DataFrame(row_results)

    # Add aggregated metrics as additional rows
    agg_metrics = {"Row_Index": ["Average_Precision", "Average_Recall"]}
    for category in categories:
        precisions = metrics[category]["precision"]
        recalls = metrics[category]["recall"]
        is_available = metrics[category]["is_available"]
        filtered_precisions = [p for p, available in zip(precisions, is_available) if available]
        filtered_recalls = [r for r, available in zip(recalls, is_available) if available]
        
        avg_precision = sum(filtered_precisions) / len(filtered_precisions) if filtered_precisions else 0.0
        avg_recall = sum(filtered_recalls) / len(filtered_recalls) if filtered_recalls else 0.0
        agg_metrics[f"ACTUAL_{category}_ID"] = ["", ""]
        agg_metrics[f"PREDICTED_{category}_ID"] = ["", ""]
        agg_metrics[f"{category}_PRECISION"] = [avg_precision, ""]
        agg_metrics[f"{category}_RECALL"] = ["", avg_recall]

    # Append aggregated metrics to DataFrame
    agg_df = pd.DataFrame(agg_metrics)
    results_df = pd.concat([results_df, agg_df], ignore_index=True)

    # Save to CSV
    results_df.to_csv(output_csv_path, index=False)

    # Print results
    print("Category-wise Precision and Recall:")
    for category in categories:
        precisions = metrics[category]["precision"]
        recalls = metrics[category]["recall"]
        recalls = metrics[category]["recall"]
        avg_precision = sum(precisions) / len(precisions) if precisions else 0.0
        avg_recall = sum(recalls) / len(recalls) if recalls else 0.0
        print(f"{category}:")
        print(f"  Average Precision: {avg_precision:.4f}")
        print(f"  Average Recall: {avg_recall:.4f}")

    print(f"\nMetrics saved to: {output_csv_path}")
    print(f"JSON files saved to: {output_json_dir}")
