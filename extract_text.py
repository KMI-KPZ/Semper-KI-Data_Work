#extract_text.py


import os
import fitz  # PyMuPDF
import shutil
import logging

# Configure logging
logging.basicConfig(filename='pipeline.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def extract_text_with_pymupdf(pdf_file):
    """
    Extract text from a PDF file using PyMuPDF.

    Args:
        pdf_file (str): Path to the PDF file.

    Returns:
        str: Extracted text content from the PDF file.
        None: If an error occurs during extraction.
    """
    try:
        # Open the PDF file
        doc = fitz.open(pdf_file)
        pdf_pages_content = ""

        # Iterate through each page in the PDF
        for page_number in range(doc.page_count):
            page = doc[page_number]
            # Extract text from the page and append to the content string
            pdf_pages_content += page.get_text()

        # Debug log to track processing of each PDF file
        logging.debug(f"Extracted text from PDF file: {pdf_file}")

        return pdf_pages_content
    
    except fitz.FileDataError as e:
        logging.error(f"File data error processing file {pdf_file} with PyMuPDF: {e}")
        return None
    except fitz.PDFPageError as e:
        logging.error(f"PDF page error processing file {pdf_file} with PyMuPDF: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error processing file {pdf_file} with PyMuPDF: {e}")
        return None





def process_folder(main_folder, output_main_folder):
    """
    Process all files in a given folder, extracting text from PDF files
    and copying non-PDF files to an output folder.

    Args:
        main_folder (str): Path to the main folder containing the input files.
        output_main_folder (str): Path to the main output folder where the processed files will be saved.
    """
    try:
        logging.debug(f"Processing folder: {main_folder}")
        for root, dirs, files in os.walk(main_folder):
            # Get relative path of the current folder
            relative_path = os.path.relpath(root, main_folder)
            relative_path_components = relative_path.split(os.sep)

            # Modify path components to indicate text subfolder
            relative_path_components = [f"{component[:-4]}_text" if component.endswith("_pdf") else component
                                        for component in relative_path_components]

            # Define output subfolder path
            output_subfolder = os.path.join(output_main_folder, *relative_path_components)

            logging.debug(f"Output subfolder: {output_subfolder}")

            # Create output subfolder if it doesn't exist
            if not os.path.exists(output_subfolder):
                os.makedirs(output_subfolder)
                logging.debug(f"Created output subfolder: {output_subfolder}")

            # Process each file in the current folder
            for file in files:
                input_file_path = os.path.join(root, file)
                logging.debug(f"Processing file: {input_file_path}")

                if file.endswith(".pdf"):
                    # Extract text from PDF files
                    text = extract_text_with_pymupdf(input_file_path)
                    if text is not None:
                        # Write extracted text to a text file
                        output_file = os.path.join(output_subfolder, f"{os.path.splitext(file)[0]}.txt")
                        with open(output_file, "w", encoding="utf-8") as text_file:
                            text_file.write(text)
                        logging.debug(f"Written text to file: {output_file}")
                else:
                    # For non-PDF files, simply copy them to the output folder
                    output_file = os.path.join(output_subfolder, file)
                    shutil.copy(input_file_path, output_file)
                    logging.debug(f"Copied file to: {output_file}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error processing folder {main_folder}: {e}")
