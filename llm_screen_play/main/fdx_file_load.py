import xml.etree.ElementTree as ET

# Load the .fdx file
file_path = "/home/ntlpt19/Downloads/Ak_For_Testing-current_draft_2024-07-22_6_53pm.fdx"
tree = ET.parse(file_path)
root = tree.getroot()

# Helper function to recursively extract text
def extract_text_lines(elem, lines):
    # Collect text from this element
    if elem.text and elem.text.strip():
        lines.append(elem.text.strip())

    # Recurse into children
    for child in elem:
        extract_text_lines(child, lines)

    # Collect tail text (text after a tag)
    if elem.tail and elem.tail.strip():
        lines.append(elem.tail.strip())

# Gather all lines
all_lines = []
extract_text_lines(root, all_lines)
print(f"Total lines extracted: {len(all_lines)}")
print(f"First 5 lines: {all_lines[:50]}")
exit('done')
# Print line-by-line
for i, line in enumerate(all_lines, start=1):
    print(f"{i:03}: {line}")
