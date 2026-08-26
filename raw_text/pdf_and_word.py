import pdfplumber
from docx import Document

pdf_path = "data/sample_summary_of_benefits.pdf"
docx_path = "data/sample_claims_process.docx"

pdf_text = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            pdf_text.append(text)

with open("raw_text/benefits.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(pdf_text))

claims_doc = Document(docx_path)

docx_text = []

for paragraph in claims_doc.paragraphs:
    if paragraph.text.strip():
        docx_text.append(paragraph.text)

with open("raw_text/claims_process.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(docx_text))