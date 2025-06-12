from fpdf import FPDF
from pathlib import Path
import os

class PDF(FPDF):
    pass

def txt_to_pdf(txt_file_path, pdf_file_path, font_path, font_size=12):
    if os.stat(txt_file_path).st_size == 0:
        print(f"Skipped empty file: {txt_file_path}")
        return

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("Unicode", "", font_path, uni=True)
    pdf.set_font("Unicode", size=font_size)

    line_height = font_size * 0.6

    with open(txt_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                pdf.multi_cell(0, line_height, txt=stripped_line)

    pdf.output(pdf_file_path)
    print(f"PDF saved to: {pdf_file_path}")

# Font path
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Example usage
file1_in_txt_file = "final_screenplay_plot_hole_report.txt"
file2_in_txt_file = "final_screenplay_coverage_report.txt"

for files_ in [file1_in_txt_file, file2_in_txt_file]:
    file_path = Path(files_)
    filename_without_ext = file_path.stem
    txt_to_pdf(files_, f"{filename_without_ext}.pdf", font_path=FONT_PATH)
