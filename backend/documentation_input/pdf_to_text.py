import fitz  # Import the PyMuPDF library

def parse_model_doc(pdf_path):
    """
    Convert a PDF file to text.

    :param pdf_path: Path to the PDF file.
    :return: The text content of the PDF.
    """
    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        text = ''
        # Iterate through each page in the PDF
        for page in doc:
            # Extract text from the page and add it to the overall text
            text += page.get_text()
    
    return text

# Path to your PDF file
pdf_path = './GoodAI_FactSheet.pdf'

# Convert the PDF to text
pdf_text = parse_model_doc(pdf_path)

# Print or process the text as needed
print(pdf_text)
