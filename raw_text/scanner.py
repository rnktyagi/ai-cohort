import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

text = pytesseract.image_to_string("data/sample_scanned_enrollment_form.png")

with open("raw_text/enrollment_ocr.txt", "w", encoding="utf-8") as f:
    f.write(text)