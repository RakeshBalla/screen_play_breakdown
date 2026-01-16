import os
import pdfplumber
import argparse
import pickle
import fitz
import random
from pathlib import Path
from screenplay_breakdown.src.utility import get_prompt_structure_recognition, get_prompt_production_categories,\
    enrich_with_ids_struct_recog, get_prompt_production_categories_revised, process_input
import re
from pdf2image import convert_from_path
from PIL import Image
from typing import List, Dict
import copy
from constants import task_name, model_name
from screenplay_breakdown.src.final_text_id_mappings import enrich_with_ids
from common_utilities.src.main.llm_calling import LLMFactory
import fitz
import json
import dotenv


llm_client = LLMFactory.get_client(model_name)


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

            else:
                print('INPUT DATA \n\n')
                print(page_dict['alltext'])
                print(page_dict['words_ids'])
                print('$$$$$$$$$$$$$$$$$$$$$$$$$')
                prompt, sys_prompt = get_prompt_production_categories_revised(page_dict['alltext'])#, page_dict['words_ids'])
            
            scene_data = llm_client.generate_response(prompt, sys_prompt)
            # scene_data = llm_response(prompt, sys_prompt)
            final_result['llm_result'] = scene_data
            enriched_scene = enrich_with_ids(scene_data, page_dict['words_ids'])
            final_result['predicted_word_ids'] = enriched_scene
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print("Scene data:", enriched_scene)
            
            
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