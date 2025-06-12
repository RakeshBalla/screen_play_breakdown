import fitz
import os

def split_pdf(input_pdf_path, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the input PDF
    pdf_document = fitz.open(input_pdf_path)
    
    # Iterate through each page
    for page_number in range(pdf_document.page_count):
        # Create a new PDF with one page
        output_pdf = fitz.open()
        output_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
        
        # Define output file path
        output_file = os.path.join(output_dir, f"page_{page_number + 1}.pdf")
        
        # Save the single page PDF
        output_pdf.save(output_file)
        output_pdf.close()
    
    # Close the input PDF
    pdf_document.close()


# Example usage
if __name__ == "__main__":
    input_pdf = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/Ak_For_Testing-current_draft_2024-07-23_5_26pm-2.pdf"  # Replace with your PDF file path
    output_directory = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/pdf_to_pdf/pdf_to_pdf"  # Replace with desired output directory
    split_pdf(input_pdf, output_directory)