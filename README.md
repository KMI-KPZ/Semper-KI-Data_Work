# PDF Extractor

## Overview

The PDF Extractor is a web application that allows users to upload PDF files, extract text from them, and then process the extracted text to generate JSON files. The application supports two types of extraction: `desired` and `generic`. It leverages OpenAI's GPT models to parse and structure the extracted text into a specified JSON format.

## Features

- **Upload PDFs:** Users can upload multiple PDF files for processing.
- **Text Extraction:** Extracts text from PDF files using PyMuPDF.
- **JSON Extraction:** Processes extracted text to generate JSON files based on the selected extraction type and GPT model.
- **Download Processed Files:** Provides links to download the generated JSON files.
- **Progress Tracking:** Shows progress of the file processing.

## Technologies Used

- **Flask:** Web framework for Python.
- **PyMuPDF (fitz):** Library for PDF text extraction.
- **OpenAI API:** For processing the extracted text using GPT models.
- **TQDM:** For displaying progress bars during file processing.
- **Bootstrap:** For styling the web interface.
- **JavaScript/jQuery:** For handling file uploads and previews.

## Setup and Installation

### Prerequisites

- Python 3.6 or higher
- Pip (Python package installer)
- OpenAI API key

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/pdf-extractor.git
    cd pdf-extractor
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Create a `.env` file in the root directory.
    - Add your OpenAI API key to the `.env` file:
      ```plaintext
      OPENAI_API_KEY=your_openai_api_key
      ```

### Running the Application

1. **Start the Flask server:**
    ```bash
    python app.py
    ```

2. **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

1. **Upload PDF Files:**
    - Select PDF files to upload by clicking the "Select PDF Files" button.
    - Choose the extraction type (`desired` or `generic`).
    - Choose the GPT model (`gpt-3.5-turbo` or `gpt-4`).

2. **Process Files:**
    - Click the "Upload" button to start processing.
    - The progress bar will display the processing progress.
    - Once processing is complete, download links for the generated JSON files will be displayed.

## Project Structure

pdf-extractor/
├── app.py # Main Flask application
├── extract_text.py # Script for extracting text from PDFs
├── extract_desired_json.py # Script for extracting desired JSON
├── extract_generic_json.py # Script for extracting generic JSON
├── templates/
│ └── index.html # HTML template for the web interface
├── static/
│ ├── css/
│ │ └── styles.css # Custom CSS styles
│ └── images/
│ └── logo.png # Project logo
├── .env # Environment variables file
├── requirements.txt # Python dependencies
└── README.md # Project documentation



## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the ...... License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please reach out to mahmoudi@infai.org.
