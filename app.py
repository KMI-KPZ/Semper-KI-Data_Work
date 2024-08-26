import streamlit as st
import os
from pathlib import Path
from extract_text import process_folder as extract_text
from extract_desired_json import process_folder as extract_desired_json
from extract_generic_json import process_folder as extract_generic_json
import openai

# Define paths
UPLOAD_FOLDER = Path('uploads')
INTERIM_FOLDER = Path('interim')
DESIRED_PROCESSED_FOLDER = Path('desired_processed')
GENERIC_PROCESSED_FOLDER = Path('generic_processed')

# Ensure paths exist
def ensure_directories():
    for folder in [UPLOAD_FOLDER, INTERIM_FOLDER, DESIRED_PROCESSED_FOLDER, GENERIC_PROCESSED_FOLDER]:
        folder.mkdir(parents=True, exist_ok=True)

ensure_directories()

def clear_folders():
    for folder in [UPLOAD_FOLDER, INTERIM_FOLDER, DESIRED_PROCESSED_FOLDER, GENERIC_PROCESSED_FOLDER]:
        if folder.exists():
            for file in folder.iterdir():
                file.unlink()

@st.cache_data
def cache_process_files(uploaded_files, extraction_type, model_type, api_key):
    return process_files(uploaded_files, extraction_type, model_type, api_key)

def process_files(uploaded_files, extraction_type, model_type, api_key):
    # Clear previous files
    clear_folders()
    
    # Ensure the upload folder exists
    ensure_directories()
    
    # Save uploaded files
    for uploaded_file in uploaded_files:
        file_path = UPLOAD_FOLDER / uploaded_file.name
        try:
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
        except Exception as e:
            st.error(f"Failed to save file {uploaded_file.name}: {e}")
            raise e

    # Set the OpenAI API key
    openai.api_key = api_key

    # Process the uploaded files
    try:
        extract_text(UPLOAD_FOLDER, INTERIM_FOLDER)

        if extraction_type == 'desired':
            extract_desired_json(INTERIM_FOLDER, DESIRED_PROCESSED_FOLDER, model_type)
            processed_folder = DESIRED_PROCESSED_FOLDER
        else:
            extract_generic_json(INTERIM_FOLDER, GENERIC_PROCESSED_FOLDER, model_type)
            processed_folder = GENERIC_PROCESSED_FOLDER

        output_folder = processed_folder
        if not output_folder.exists():
            st.error(f"Output folder not found: {output_folder}")
            return [], processed_folder

        output_files = list(output_folder.iterdir())
        return output_files, processed_folder
    
    except Exception as e:
        st.error(f"An error occurred during processing: {e}")
        return [], processed_folder

def main():
    st.title('PDF Extractor')

    st.header('Upload PDFs for JSON Data Extraction')

    # API Key input
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    uploaded_files = st.file_uploader("Select PDF Files:", accept_multiple_files=True, type=["pdf", "txt"])

    extraction_type = st.selectbox("Choose Extraction Type:", ["desired", "generic"])
    model_type = st.selectbox("Choose GPT Model:", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])

    if uploaded_files:
        st.session_state.upload_button_disabled = False
    else:
        st.session_state.upload_button_disabled = True

    if st.button("Upload", disabled=st.session_state.upload_button_disabled):
        if uploaded_files:
            if not api_key:
                st.error("Please enter your OpenAI API key.")
            else:
                with st.spinner('Processing files...'):
                    try:
                        output_files, processed_folder = cache_process_files(uploaded_files, extraction_type, model_type, api_key)
                        st.success('Files processed successfully!')
                        
                        # Display download links
                        if output_files:
                            st.subheader('Download Processed Files:')
                            for file_path in output_files:
                                if file_path.exists():
                                    with open(file_path, 'rb') as f:
                                        st.download_button(
                                            label=f"Download {file_path.name}",
                                            data=f.read(),
                                            file_name=file_path.name,
                                            mime='application/octet-stream'
                                        )
                                else:
                                    st.error(f"File not found: {file_path}")
                        else:
                            st.warning("No files found in the output directory.")

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
        else:
            st.error("Please upload files.")

    if uploaded_files:
        st.sidebar.header('File Details')
        for uploaded_file in uploaded_files:
            st.sidebar.write(f"**File Name:** {uploaded_file.name}")
            st.sidebar.write(f"**File Type:** {uploaded_file.type}")
            st.sidebar.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")

if __name__ == "__main__":
    if 'upload_button_disabled' not in st.session_state:
        st.session_state.upload_button_disabled = True
    main()

