import os
import json
import csv

from constants import task_name, sigregate_folder

def extract_data_from_json_folder(folder_path, output_csv_path):
    rows = []
    all_keys = set()

    # First pass: collect all keys from llm_response
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as f:
                data = json.load(f)
                if task_name == 'prod_recog':
                    llm_response = data.get('llm_result', {}).get('production_categories', {})
                else:
                    llm_response = data.get('response_mapping_wordIds', {})
                    
                all_keys.update(llm_response.keys())

    all_keys = sorted(list(all_keys))

    # Second pass: build rows
    for file_name in os.listdir(folder_path):
        file_name_no_ext = os.path.splitext(file_name)[0] + '.pdf'
        
        if file_name.endswith('.json'):
            with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as f:
                data = json.load(f)
                content_length = ''
                if sigregate_folder:
                    if file_name_no_ext in large_files:
                        content_length = 'large'
                    elif file_name_no_ext in medium_files:
                        content_length = 'medium'
                    elif file_name_no_ext in small_files:
                        content_length = 'small'
                    row = {
                        'sample_no': data.get('sample_no', ''),
                        'pdf_file_name': data.get('pdf_file_name', ''),
                        'content_length': content_length
                    }
                else:
                    row = {
                        'file_name': file_name
                        # 'pdf_file_name': data.get('pdf_file_name', ''),
                    }
                if task_name == 'prod_recog':
                    llm_response = data.get('llm_result', {}).get('production_categories', {})
                else:
                    llm_response = data.get('response_mapping_wordIds', {})
                  
                for key in all_keys:
                    value = llm_response.get(key, '')
                    row[key] = value  # Original value
                    if sigregate_folder:
                        row[f'len_{key}'] = len(value) # Length of the string representation

                rows.append(row)

    # Create fieldnames: original fields + length fields
    if sigregate_folder:
        fieldnames = ['content_length', 'sample_no', 'pdf_file_name'] + all_keys + [f'len_{key}' for key in all_keys]
    else:
        fieldnames = ['file_name'] + all_keys
    # Write CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    folder_path = '/home/ntlpt19/personal_projects/screen_play_breakdown_project/screen_data/testing_jun10/Nava_output'
    output_csv_path = '/home/ntlpt19/personal_projects/screen_play_breakdown_project/screen_data/testing_jun10'
    output_csv_path = f'{output_csv_path}/{task_name}.csv'
    
    
    if sigregate_folder:
        data_path = '/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_samples/data'
        large_files = []
        medium_files = []
        small_files = []

        for size in ['large', 'medium', 'small']:
            size_path = os.path.join(data_path, size)
            if not os.path.isdir(size_path):
                continue

            for subfolder in os.listdir(size_path):
                subfolder_path = os.path.join(size_path, subfolder)
                if os.path.isdir(subfolder_path):
                    for file in os.listdir(subfolder_path):
                        full_path = os.path.join(subfolder_path, file)
                        if os.path.isfile(full_path):
                            if size == 'large':
                                large_files.append(file)
                            elif size == 'medium':
                                medium_files.append(file)
                            elif size == 'small':
                                small_files.append(file)


    extract_data_from_json_folder(folder_path, output_csv_path)