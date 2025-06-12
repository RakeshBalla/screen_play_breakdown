import os
import pdfplumber
import argparse
import pickle
import fitz
import random
from pathlib import Path
from screenplay_breakdown.src.utility import get_prompt_structure_recognition, llm_response, get_prompt_production_categories,\
    enrich_with_ids_struct_recog, get_prompt_production_categories_revised, process_input
import re
from pdf2image import convert_from_path
from PIL import Image
from typing import List, Dict
import copy
from screenplay_breakdown.src.constants import task_name
from screenplay_breakdown.src.final_text_id_mappings import enrich_with_ids

def return_word_grid(pdf_path):
    """Return the word information from a PDF file using pdfplumber.

    Parameters
    ----------
    pdf_path : str
        The path to the input PDF file.

    Returns
    -------
    List
        Returns a list of word information for each page.
    """
    pdf = pdfplumber.open(pdf_path)
    word_data = []
    alltext = []
    for page in pdf.pages:
        all_text_ = page.extract_text()
        alltext.append(all_text_)
        # Step 1: Split the text by newlines
        lines = all_text_.split('\n')
        # Step 2: Split each line by spaces and flatten into a list of words
        words = []
        for line in lines:
            # Split line by spaces and filter out empty strings
            line_words = [word for word in line.split() if word]
            words.extend(line_words)
        # Print the list of words
        print(words)
        word_data.append(words)
        
        # word_data.append(page.extract_words())
    pdf.close()
    return word_data, alltext

def create_page_dict(page_data, alltext):
    """Create a dictionary with the original words, their bounding box coordinates, and random word IDs.

    Parameters
    ----------
    page_data : List
        List of word information from pdfplumber for a single page.
    alltext : List
        List of extracted text for the page.
    Returns
    -------
    Dict
        Returns a dictionary with the original words, their bounding box coordinates, and word IDs.
    """
    page_dict = {
        # "word_coordinates": [],
        # "words": [],
        "alltext": alltext,
        # "word_coordinates_ids": [],
        "words_ids": {}
    }
    for wo in page_data:
        word_id = random.randint(1000, 9999)
        # page_dict["word_coordinates_ids"].append(word_id)
        page_dict["words_ids"][word_id] = wo
    return page_dict
        
    for ele in page_data:
        # Store the original word
        word = ele["text"]
        page_dict["words"].append(word)
        # Bounding box format: (x0, top, width, height)
        coords = (
            ele["x0"],
            ele["top"],
            ele["x1"] - ele["x0"],
            ele["bottom"] - ele["top"]
        )
        page_dict["word_coordinates"].append(coords)
        # Generate a random ID for the word (between 1000 and 9999 for uniqueness)
        word_id = random.randint(1000, 9999)
        page_dict["word_coordinates_ids"].append(word_id)
        page_dict["words_ids"][word_id] = word
        
    print(page_dict)
    return page_dict


import fitz

def draw_rectangles_from_enriched_scene(enriched_scene_with_bboxes, pdf_path, output_path, page_num):
    """Draw rectangles and their corresponding keys from enriched scene data on a PDF.

    Parameters
    ----------
    enriched_scene_with_bboxes : Dict
        Dictionary containing scene data with 'bbox' and 'ids' keys.
    pdf_path : str
        Path to the input PDF.
    output_path : str
        Path to save the output PDF.
    page_num : int
        Page number to process (1-indexed).
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]  # 0-indexed

    def collect_bboxes_and_keys(item, current_key=None, parent_keys=None):
        """Recursively collect bboxes and their associated keys."""
        if parent_keys is None:
            parent_keys = []
        
        if isinstance(item, dict):
            # Initialize key_to_display
            key_to_display = None
            
            # Check if this dictionary has 'value', 'ids', and 'bbox' (indicating a string with metadata)
            if 'value' in item and 'ids' in item and 'bbox' in item:
                # Use the parent_keys list to construct the full hierarchy
                key_to_display = '_'.join(parent_keys) if parent_keys else None
            
            if 'bbox' in item and item['bbox']:
                x0, top, width, height = item['bbox']
                # Convert bbox to rectangle points
                rect = [
                    [x0, top],
                    [x0 + width, top],
                    [x0 + width, top + height],
                    [x0, top + height]
                ]
                # Draw green rectangle outline
                rect_closed = rect + [rect[0]]
                page.draw_polyline(rect_closed, color=(0, 1, 0), width=1.5)
                
                # Draw key in red text above the bbox (adjust position slightly)
                if key_to_display:
                    text_pos = (x0, top - 2)  # 2 points above the bbox
                    page.insert_text(text_pos, key_to_display, fontsize=8, color=(1, 0, 0))  # Red text
            
            # Recurse into dictionary keys, tracking parent keys
            for key, value in item.items():
                if isinstance(value, (list, dict)):
                    collect_bboxes_and_keys(value, key, parent_keys + [key] if key != 'value' else parent_keys)
        
        elif isinstance(item, list):
            for sub_item in item:
                collect_bboxes_and_keys(sub_item, current_key, parent_keys)

    collect_bboxes_and_keys(enriched_scene_with_bboxes)

    # Create new PDF with only that page
    new_doc = fitz.open()  # Create empty PDF
    new_doc.insert_pdf(doc, from_page=page_num - 1, to_page=page_num - 1)
    new_doc.save(output_path)
    new_doc.close()
    doc.close()



def draw_rectangles_prod_recog(enriched_scene_with_bboxes, pdf_path, output_path, page_num):
    """Draw rectangles and their corresponding keys from enriched scene data on a PDF.

    Parameters
    ----------
    enriched_scene_with_bboxes : Dict
        Dictionary containing scene data with 'bbox' and 'ids' or 'index_value' keys.
    pdf_path : str
        Path to the input PDF.
    output_path : str
        Path to save the output PDF.
    page_num : int
        Page number to process (1-indexed).
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]  # 0-indexed

    # Track drawn bboxes to avoid duplicates
    drawn_bboxes = set()

    def collect_bboxes_and_keys(item, current_key=None, parent_keys=None):
        """Recursively collect bboxes and their associated keys."""
        if parent_keys is None:
            parent_keys = []
        
        if isinstance(item, dict):
            # Use the top-most parent key for annotation (e.g., 'CAST', 'PROPS')
            key_to_display = parent_keys[0] if parent_keys else current_key
            
            if 'bboxes' in item and item['bboxes']:
                for bbox in item['bboxes']:
                    x0, top, width, height = bbox
                    # Validate bbox coordinates
                    if width <= 0 or height <= 0 or x0 < 0 or top < 0:
                        continue  # Skip invalid bboxes
                    
                    # Create a unique identifier for the bbox to avoid duplicates
                    bbox_tuple = (x0, top, width, height)
                    if bbox_tuple in drawn_bboxes:
                        continue  # Skip already drawn bbox
                    drawn_bboxes.add(bbox_tuple)
                    
                    # Convert bbox to rectangle points
                    rect = [
                        [x0, top],
                        [x0 + width, top],
                        [x0 + width, top + height],
                        [x0, top + height]
                    ]
                    # Draw green rectangle outline
                    rect_closed = rect + [rect[0]]
                    page.draw_polyline(rect_closed, color=(0, 1, 0), width=1.5)
                    
                    # Draw key in red text above the bbox, ensuring no overlap
                    if key_to_display:
                        text_pos = (x0, top - 5)  # Adjusted to 5 points above to reduce gap
                        # Check if text fits within page boundaries
                        if text_pos[1] >= 0:
                            page.insert_text(
                                text_pos,
                                key_to_display,
                                fontsize=8,
                                color=(1, 0, 0)  # Red text
                            )
            
            # Recurse into dictionary keys, tracking parent keys
            for key, value in item.items():
                if isinstance(value, (list, dict)):
                    collect_bboxes_and_keys(value, key, parent_keys + [key] if key != 'value' else parent_keys)
        
        elif isinstance(item, list):
            for sub_item in item:
                collect_bboxes_and_keys(sub_item, current_key, parent_keys)

    collect_bboxes_and_keys(enriched_scene_with_bboxes)

    # Create new PDF with only the processed page
    new_doc = fitz.open()  # Create empty PDF
    new_doc.insert_pdf(doc, from_page=page_num - 1, to_page=page_num - 1)
    new_doc.save(output_path)
    new_doc.close()
    doc.close()
    
    
def get_rectangles_from_enriched_scene(enriched_scene, page_dict, pdf_file):
    """Add merged bounding boxes to enriched scene data by mapping word IDs to coordinates.

    Parameters
    ----------
    enriched_scene : Dict
        Dictionary containing scene data with word IDs.
    page_dict : Dict
        Dictionary containing word coordinates and their corresponding IDs.
    pdf_file : str
        Name of the PDF file for error reporting.

    Returns
    -------
    Dict
        Modified enriched_scene with 'bbox' keys added alongside 'ids' keys, containing merged (x0, top, width, height).
    """
    # Create a deep copy to avoid modifying the input
    result_scene = copy.deepcopy(enriched_scene)
    
    def process_ids(item):
        """Recursively process IDs and add merged bboxes to the structure."""
        if isinstance(item, dict):
            if 'ids' in item and isinstance(item['ids'], list) and item['ids']:  # Check for non-empty IDs list
                # Collect all bboxes for the IDs in this list
                bboxes = []
                for word_id in item['ids']:
                    if word_id:  # Ensure ID is not None
                        try:
                            idx = page_dict['word_coordinates_ids'].index(word_id)
                            x0, top, width, height = page_dict['word_coordinates'][idx]
                            if width <= 0 or height <= 0:
                                print(f"Invalid coordinates for word ID {word_id} in {pdf_file}: {(x0, top, width, height)}")
                                continue
                            bboxes.append((x0, top, x0 + width, top + height))  # (x0, top, x1, bottom)
                        except ValueError:
                            print(f"Word ID {word_id} not found in {pdf_file}.")
                if bboxes:
                    # Merge bboxes into a single bbox
                    min_x0 = min(x0 for x0, _, _, _ in bboxes)
                    min_top = min(top for _, top, _, _ in bboxes)
                    max_x1 = max(x1 for _, _, x1, _ in bboxes)
                    max_bottom = max(bottom for _, _, _, bottom in bboxes)
                    merged_bbox = (min_x0, min_top, max_x1 - min_x0, max_bottom - min_top)
                    # Add merged bbox to the current dictionary
                    item['bbox'] = merged_bbox
            # Recurse into other dictionary keys
            for key, value in item.items():
                if isinstance(value, (list, dict)):
                    process_ids(value)
        elif isinstance(item, list):
            for sub_item in item:
                process_ids(sub_item)

    process_ids(result_scene)
    return result_scene


def add_bboxes_to_enriched_scene(enriched_scene, page_dict, pdf_file):
    """Add bounding boxes to enriched scene data by mapping word IDs to coordinates.

    Parameters
    ----------
    enriched_scene : Dict
        Dictionary containing scene data with 'index_value' keys (e.g., {'scene_number': {'value': 1, 'index_value': [1146]}, ...}).
    page_dict : Dict
        Dictionary containing word coordinates and their corresponding IDs.
    pdf_file : str
        Name of the PDF file for error reporting.

    Returns
    -------
    Dict
        Modified enriched_scene with 'bboxes' keys added alongside 'index_value' keys, containing list of (x0, top, width, height).
    """
    # Create a deep copy to avoid modifying the input
    result_scene = copy.deepcopy(enriched_scene)
    
    def process_index_values(item):
        """Recursively process index_value lists and add individual bboxes."""
        if isinstance(item, dict):
            if 'index_value' in item and isinstance(item['index_value'], list) and item['index_value']:  # Check for non-empty index_value list
                # Collect all bboxes for the IDs in this list
                bboxes = []
                for word_id in item['index_value']:
                    if word_id:  # Ensure ID is not None
                        try:
                            idx = page_dict['word_coordinates_ids'].index(word_id)
                            x0, top, width, height = page_dict['word_coordinates'][idx]
                            if width <= 0 or height <= 0:
                                print(f"Invalid coordinates for word ID {word_id} in {pdf_file}: {(x0, top, width, height)}")
                                continue
                            bboxes.append((x0, top, width, height))  # Store original bbox
                        except ValueError:
                            print(f"Word ID {word_id} not found in {pdf_file}.")
                if bboxes:
                    # Add list of bboxes to the current dictionary
                    item['bboxes'] = bboxes
            # Recurse into other dictionary keys
            for key, value in item.items():
                if isinstance(value, (list, dict)):
                    process_index_values(value)
        elif isinstance(item, list):
            for sub_item in item:
                process_index_values(sub_item)

    process_index_values(result_scene)
    return result_scene

import json
def process_pdfs(master_folder, json_output, output_pdf_path):
    """Process all PDFs in the master folder, enrich scene data, and draw rectangles.

    Parameters
    ----------
    master_folder : str
        Path to the master folder containing sample folders with PDFs.
    output_folder : str
        Path to save the output PDFs with drawn rectangles.
    """

    # Iterate through sample folders in master folder
    for sample_folder in os.listdir(master_folder):
        sample_path = os.path.join(master_folder, sample_folder)
        if not os.path.isdir(sample_path):
            continue

        # Iterate through PDFs in sample folder
        for pdf_file in os.listdir(sample_path):
            if not pdf_file.lower().endswith('.pdf'):
                continue

            pdf_path = os.path.join(sample_path, pdf_file)
            # pdf_path = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_samples/data/medium/sample1/page_20.pdf"
            print('pdf_path:', pdf_path)
            # Get word data and text from PDF (single page)
            word_data, alltext = return_word_grid(pdf_path)
            if not word_data or not alltext:
                print(f"Skipping {pdf_file}: No data extracted.")
                continue

            # Create page dictionary with word IDs
            # page_dict = create_page_dict(word_data[0], alltext[0])  # Single page
            page_dict = process_input(alltext[0])
            final_result = {}
            final_result['page_dict'] = page_dict
            final_result['sample_no'] = sample_folder
            final_result['pdf_file_name'] = pdf_file
            # Get prompt and system prompt for LLM
            if task_name == "structure_recognition":
                prompt, sys_prompt = get_prompt_structure_recognition(page_dict['alltext'])
                # Get LLM response
                scene_data = llm_response(prompt, sys_prompt)
                print("Scene data:", scene_data)
                final_result['llm_response'] = scene_data
                # Enrich scene data with word IDs
                enriched_scene = enrich_with_ids(scene_data, page_dict['words_ids'])
                final_result['response_mapping_wordIds'] = enriched_scene
                print("Enriched scene data:", enriched_scene)
                # Prepare rectangles for drawing ******************
                # enriched_scene_with_bboxes = get_rectangles_from_enriched_scene(enriched_scene, page_dict, pdf_file)
                # Define output path
                # print(enriched_scene_with_bboxes)
                output_pdf = os.path.join(output_pdf_path, f"annotated_{pdf_file}")
                # Draw rectangles on PDF ****************
                # draw_rectangles_from_enriched_scene(enriched_scene_with_bboxes, pdf_path, output_pdf, 1)
                print(f"Processed {pdf_file} and saved to {output_pdf}")
                exit('???????????????????/')
            else:
                print('INPUT DATA \n\n')
                print(page_dict['alltext'])
                print(page_dict['words_ids'])
                print('$$$$$$$$$$$$$$$$$$$$$$$$$')
                prompt, sys_prompt = get_prompt_production_categories_revised(page_dict['alltext'])#, page_dict['words_ids'])
                scene_data = llm_response(prompt, sys_prompt)
                final_result['llm_result'] = scene_data
                
                enriched_scene = enrich_with_ids(scene_data, page_dict['words_ids'])
                final_result['predicted_word_ids'] = enriched_scene
                
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                print("Scene data:", enriched_scene)
                # enriched_scene_with_bboxes = add_bboxes_to_enriched_scene(scene_data['production_categories'], page_dict, pdf_file)
                # output_pdf_path = os.path.join(output_pdf_path, f"annotated_{pdf_file}")
                # # Draw rectangles on PDF
                # print('%%%%%%%%%%%%%%%%%%%%%%%%')
                # print('%%%%%%%%%%%%%%%%%%%%%%%%')
                # print(enriched_scene_with_bboxes)
                # draw_rectangles_prod_recog(enriched_scene_with_bboxes, pdf_path, output_pdf_path, 1)
                print(f"Processed {pdf_file} and saved to {output_pdf_path}")
                
            file_base_name = os.path.splitext(pdf_file)[0]
            json_file_path = os.path.join(json_output, f"{file_base_name}.json")
            # Save to JSON file
            with open(json_file_path, "w", encoding="utf-8") as f:
                json.dump(final_result, f, ensure_ascii=False, indent=2)
            
def main():
    parser = argparse.ArgumentParser(description="Process PDFs and annotate with rectangles.")
    parser.add_argument('--master_folder', type=str, required=True, help="Path to the master folder containing sample folders with PDFs.")
    parser.add_argument('--output_folder', type=str, required=True, help="Path to save annotated PDFs.")
    args = parser.parse_args()
    
    
        # Ensure output folder exists
    # Path(output_folder).mkdir(parents=True, exist_ok=True)
    output_pdf_path_ = os.path.join(args.output_folder, task_name)
    os.makedirs(output_pdf_path_, exist_ok=True)
    
    os.makedirs(args.output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_pdf_path_, 'json_files'), exist_ok=True)
    # os.makedirs(os.path.join(output_pdf_path_, 'pdf_files'), exist_ok=True)
    
    
    
    process_pdfs(args.master_folder, os.path.join(output_pdf_path_, 'json_files'), os.path.join(output_pdf_path_, 'pdf_files'))

if __name__ == "__main__":
    main()