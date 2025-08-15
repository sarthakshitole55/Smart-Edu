import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    text = ""
    
    # Iterate over each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    
    return text

# Example usage
pdf_path = "C:/Users/HP/OneDrive/Documents/Source.pdf"  # Replace with the actual path to your PDF file
extracted_text = extract_text_from_pdf(pdf_path)

# Save the extracted text to a file
with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
    text_file.write(extracted_text)