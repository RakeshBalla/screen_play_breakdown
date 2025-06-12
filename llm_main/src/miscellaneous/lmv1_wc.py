from transformers import LayoutLMTokenizer, LayoutLMForTokenClassification
from PIL import Image
import pytesseract
import torch

# 1. Load image
image_path = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/pdf_pages_as_png/Ak_For_Testing-current_draft_2024-07-23_5_26pm_02.png"
image = Image.open(image_path).convert("RGB")

# 2. OCR using pytesseract
ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

words = []
boxes = []

for i in range(len(ocr_data["text"])):
    word = ocr_data["text"][i]
    if word.strip() == "":
        continue
    x, y, w, h = ocr_data["left"][i], ocr_data["top"][i], ocr_data["width"][i], ocr_data["height"][i]
    words.append(word)
    # Normalize bounding box to 0-1000
    boxes.append([int(1000 * x / image.width),
                  int(1000 * y / image.height),
                  int(1000 * (x + w) / image.width),
                  int(1000 * (y + h) / image.height)])

# 3. Tokenizer & model
tokenizer = LayoutLMTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")
model = LayoutLMForTokenClassification.from_pretrained("microsoft/layoutlm-base-uncased")  # Replace with fine-tuned model if available

encoding = tokenizer(words,
                     boxes=boxes,
                     return_tensors="pt",
                     truncation=True,
                     padding="max_length",
                     max_length=512,
                     is_split_into_words=True)

# 4. Run model
with torch.no_grad():
    outputs = model(**encoding)

logits = outputs.logits
predicted_ids = logits.argmax(-1).squeeze().tolist()
tokens = tokenizer.convert_ids_to_tokens(encoding["input_ids"].squeeze().tolist())

# 5. Print predictions
print("Word-level token classification:")
for word, pred_id in zip(words, predicted_ids[1:len(words)+1]):  # Skip [CLS]
    print(f"{word}: Label {pred_id}")
