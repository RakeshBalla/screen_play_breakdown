import os
from pdf2image import convert_from_path

def convert_pdf_to_png(pdf_path, output_folder, dpi=200):
    """
    Converts each page of the given PDF into a PNG image.

    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Folder to save the PNG images.
        dpi (int): Resolution in DPI (default: 200).

    Returns:
        List of saved image paths.
    """
    os.makedirs(output_folder, exist_ok=True)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    images = convert_from_path(pdf_path)#, dpi=dpi)
    image_paths = []

    for idx, page in enumerate(images):
        image_name = f"{pdf_name}_{idx + 1:02d}.png"
        image_path = os.path.join(output_folder, image_name)
        page.save(image_path, 'PNG')
        image_paths.append(image_path)
    
    return image_paths

pdf_path = "/home/ntlpt19/Downloads/Ak_For_Testing-current_draft_2024-07-23_5_26pm.pdf"
output_folder = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/pdf_pages_as_png"
os.makedirs(output_folder, exist_ok=True)
image_paths = convert_pdf_to_png(pdf_path, output_folder)
