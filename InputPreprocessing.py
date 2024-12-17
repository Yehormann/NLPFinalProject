import os
from PyPDF2 import PdfReader

# Define directories
CV_FOLDER = os.path.join('Public', 'InputFolder', 'CVInputFolder')
JOB_FOLDER = os.path.join('Public', 'InputFolder', 'JobInputFolder')
LETTER_FOLDER = os.path.join('Public', 'InputFolder', 'LetterFolder')
OUTPUT_FOLDER = os.path.join('Public', 'InputFolder', 'Preprocessed')

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def find_file_in_directory(directory, extensions):
    """
    Search for the first file in the given directory with the specified extensions.

    Args:
        directory (str): Path to the directory to search.
        extensions (tuple): Allowed file extensions (e.g., ('.pdf', '.docx')).

    Returns:
        str: Path to the found file or None if no file is found.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                return os.path.join(root, file)
    return None

def extract_text_from_pdf(pdf_path):
    """Extract plain text from a PDF file."""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def save_text_to_file(text, output_path):
    """Save extracted text to a .txt file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"File saved: {output_path}")
    except Exception as e:
        print(f"Error saving file {output_path}: {e}")

def preprocess_and_save(folder, file_type, output_folder):
    """
    Preprocess files from a specific folder and save the extracted text to the output folder.

    Args:
        folder (str): Directory where the input files are located.
        file_type (str): Type of file being processed ('CV', 'Job', 'Letter').
        output_folder (str): Directory to save the preprocessed text files.
    """
    print(f"Searching for {file_type} file...")
    file_path = find_file_in_directory(folder, ('.pdf', '.docx', '.txt'))

    if not file_path:
        print(f"No {file_type} file found in {folder}.")
        return

    print(f"Processing {file_type}: {file_path}")
    extracted_text = extract_text_from_pdf(file_path)

    # Define output file path
    output_file_name = f"{file_type}_preprocessed.txt"
    output_file_path = os.path.join(output_folder, output_file_name)

    # Save text to file
    save_text_to_file(extracted_text, output_file_path)

def preprocess_files():
    """Preprocess the uploaded files and save them to the output folder."""
    # Process Job Description
    preprocess_and_save(JOB_FOLDER, "JobDescription", OUTPUT_FOLDER)

    # Process CV
    preprocess_and_save(CV_FOLDER, "CV", OUTPUT_FOLDER)

    # Process Cover Letter
    preprocess_and_save(LETTER_FOLDER, "Letter", OUTPUT_FOLDER)

if __name__ == "__main__":
    preprocess_files()
