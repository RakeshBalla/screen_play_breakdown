import os
import cv2
import fitz  # PyMuPDF
import json
import argparse
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import fitz  # PyMuPDF
from pdf_parser import return_word_grid, create_page_dict
# --------- Drawing & Contour Helpers ---------

def draw_rectangles(image, rectangles, color=(0, 255, 0), thickness=2):
    img_copy = image.copy()
    for rect in rectangles:
        # rect_np = np.array(rect, dtype=np.int32)
        rect_np = np.array(rect, dtype=np.int32).reshape((-1, 1, 2))  # Ensure correct shape
        cv2.polylines(img_copy, [rect_np], isClosed=True, color=color, thickness=thickness)
    return img_copy

def process_word_coordinates(word_coordinates):
    """
    Process word coordinates to create initial rectangles
    """
    rectangles = []
    for word_data in word_coordinates:
        # Map the keys to your expected names
        word_data['left'] = word_data['x0']
        word_data['x2'] = word_data['x1']
        word_data['y2'] = word_data['bottom']

        # Create rectangle vertices
        topleft = (word_data['left'], word_data['top'])
        topright = (word_data['x2'], word_data['top'])
        bottomright = (word_data['x2'], word_data['y2'])
        bottomleft = (word_data['left'], word_data['y2'])
        
        vertices = [topleft, topright, bottomright, bottomleft]
        rectangles.append(vertices)
    
    return rectangles

def merge_overlapping_rectangles(rectangles):
    """
    Merge overlapping rectangular bounding boxes.
    Each rectangle is represented as [[x1,y1], [x2,y1], [x2,y2], [x1,y2]]
    """
    if not rectangles:
        return []
    merged_rectangles = []
    rectangles = rectangles.copy()  # Create a copy to avoid modifying original list
    while rectangles:
        current_rect = rectangles.pop(0)
        # Extract coordinates of current rectangle
        x1, y1 = current_rect[0]  # top-left
        x2, y2 = current_rect[2]  # bottom-right
        # Flag to check if current rectangle was merged
        merged = False
        # Check against remaining rectangles
        i = 0
        while i < len(rectangles):
            rect = rectangles[i]
            rx1, ry1 = rect[0]  # top-left of comparison rectangle
            rx2, ry2 = rect[2]  # bottom-right of comparison rectangle
            # Check for vertical overlap (using y-coordinates)
            vertical_overlap = (ry1 <= y2 + 5) and (ry2 >= y1 - 5)  # Added small threshold
            # Check for horizontal overlap (using x-coordinates)
            horizontal_overlap = (rx1 <= x2 + 5) and (rx2 >= x1 - 5)  # Added small threshold
            # If rectangles overlap both vertically and horizontally
            # if vertical_overlap and horizontal_overlap:
            if vertical_overlap:
                # Merge the rectangles by taking min/max of coordinates
                x1 = min(x1, rx1)
                y1 = min(y1, ry1)
                x2 = max(x2, rx2)
                y2 = max(y2, ry2)
                # Remove the merged rectangle
                rectangles.pop(i)
                merged = True
            else:
                i += 1
        # Add the final merged rectangle
        new_rect = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        merged_rectangles.append(new_rect)
        # If merged occurred, add back the merged rectangle to check for more potential merges
        if merged:
            rectangles.insert(0, new_rect)
    return merged_rectangles
    
    




def draw_rectangles_on_pdf(pdf_path, output_path, page_num, rectangles):
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]  # 0-indexed

    for rect in rectangles:
        # rect is [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        # poly = fitz.Polygon(rect)
        rect_closed = rect + [rect[0]]
        page.draw_polyline(rect_closed, color=(0, 1, 0), width=1.5)  # green outline

    # Create new PDF with only that page
    new_doc = fitz.open()         # Create empty PDF
    new_doc.insert_pdf(doc, from_page=page_num - 1, to_page=page_num - 1)
    new_doc.save(output_path)
    new_doc.close()
    doc.close()
# --------- Main Logic ---------

def main():
    parser = argparse.ArgumentParser(description="Draw word contours page-wise from a PDF.")
    parser.add_argument("--pdf", type=str, required=True, help="Path to input PDF")
    parser.add_argument("--output", type=str, required=True, help="Output folder for annotated pages")
    parser.add_argument("--debug", action='store_true', help="Enable debug mode to draw and save images")
    args = parser.parse_args()
    pdf_images = convert_from_path(args.pdf)
    os.makedirs(args.output, exist_ok=True)

    word_grid, alltext = return_word_grid(args.pdf)

    for page_num, page_data in enumerate(word_grid):
        print(f"Processing page {page_num+1}...")
        print(page_data)
        # page_dict = create_page_dict(page_data, alltext[page_num])
        # word_coordinates = page_dict["word_coordinates"]

        use_contours = process_word_coordinates(page_data)
        merged_once = merge_overlapping_rectangles(use_contours)
        merged_final = merge_overlapping_rectangles(merged_once)
        print(f"Number of merged rectangles: {len(merged_final)}")
        print(f"Page {page_num+1} - Merged Rectangles: {merged_final}")
        # exit('???????????????')
        # if args.debug:
        # image = pdf_page_to_image(args.pdf, page_num)
        # page_image = pdf_images[page_num - 1]  # list is 0-indexed
        # page_image = pdf_images[page_num]  # list is 0-indexed
        # page_image_cv = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)
        # drawn_image = draw_rectangles(page_image_cv, merged_final)
        draw_rectangles_on_pdf(
            pdf_path=args.pdf,
            output_path=os.path.join(args.output, f"page_{page_num+1:02d}.pdf"),
            page_num=page_num + 1,
            rectangles=merged_final
        )
        
        save_path = os.path.join(args.output, f"page_{page_num+1:02d}.png")
        # cv2.imwrite(save_path, drawn_image)
        print(f"Saved: {save_path}")

if __name__ == "__main__":
    main()
