from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Example: Extract text from an existing PDF
# pdf_path = "./orig/test.pdf"  # Path to your existing PDF
# extracted_text = extract_text_from_pdf(pdf_path)
# print(extracted_text)