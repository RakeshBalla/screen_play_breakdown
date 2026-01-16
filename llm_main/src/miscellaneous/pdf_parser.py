import os
import pdfplumber
import argparse
import pickle


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
        word_data.append(page.extract_words())
        alltext.append(page.extract_text())
    pdf.close()
    return word_data, alltext

def create_page_dict(page_data, alltext):
    """Create a dictionary with the original words and their bounding box coordinates.

    Parameters
    ----------
    page_data : List
        List of word information from pdfplumber for a single page.
    alltext : List
        List of extracted text for the page.
    Returns
    -------
    Dict
        Returns a dictionary with the original words and their bounding box coordinates.
    """
    page_dict = {
        "word_coordinates": [],
        "words": [],
        "alltext": alltext
    }
    for ele in page_data:
        # Store the original word
        page_dict["words"].append(ele["text"])
        # Bounding box format: (x0, top, width, height)
        page_dict["word_coordinates"].append((
            ele["x0"],
            ele["top"],
            ele["x1"] - ele["x0"],
            ele["bottom"] - ele["top"]
        ))
    return page_dict

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process a PDF to extract word data and bounding boxes.")
    parser.add_argument("--pdf", type=str, required=True, help="Path to the input PDF file")
    args = parser.parse_args()

    # Get word grid from PDF
    word_grid, alltext = return_word_grid(args.pdf)

    # Create page-wise dictionary
    output_dict = {}
    for page_num, page_data in enumerate(word_grid):
        page_key = f"page{page_num}"
        output_dict[page_key] = create_page_dict(page_data, alltext[page_num])

    # Example: Print the page-wise data
    for page_key, page_data in output_dict.items():
        print(f"{page_key}:")
        print(f"Words: {page_data['words'][:5]}...")  # Print first 5 for brevity
        print(f"All Text: {page_data['alltext']}")
        print(f"Word Coordinates: {page_data['word_coordinates'][:5]}...\n")

    import json

    # Save output_dict to a JSON file
    with open('screenplay_breakdown.json', 'w', encoding='utf-8') as f:
        json.dump(output_dict, f, ensure_ascii=False, indent=4)


    # Optionally, save to a file
    output_file = "page_wise_word_data.pkl"
    with open(output_file, "wb") as f:
        pickle.dump(output_dict, f)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()