import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

# Define the raw and text directories
raw_dir = 'raw'
text_dir = 'text'

# Create the text directory if it doesn't exist
if not os.path.exists(text_dir):
    os.makedirs(text_dir)

# Iterate through all files in the raw directory
for root, dirs, files in os.walk(raw_dir):
    # Create the corresponding directory in the text directory
    text_root = root.replace(raw_dir, text_dir)
    if not os.path.exists(text_root):
        os.makedirs(text_root)
    # Iterate through all PDF files in the current directory
    for file in files:
        if file.endswith('.pdf'):
            # Construct the full file paths
            raw_file = os.path.join(root, file)
            text_file = os.path.join(text_root, file.replace('.pdf', '.txt'))
            # Extract text from the PDF if the text file doesn't exist
            if not os.path.exists(text_file):
                print(f"Extracting text from {file}...")
                rsrcmgr = PDFResourceManager()
                retstr = StringIO()
                laparams = LAParams()
                device = TextConverter(rsrcmgr, retstr, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                with open(raw_file, 'rb') as fp:
                    for page in PDFPage.get_pages(fp):
                        interpreter.process_page(page)
                device.close()
                str = retstr.getvalue()
                retstr.close()
                with open(text_file, 'w') as f:
                    f.write(str)
