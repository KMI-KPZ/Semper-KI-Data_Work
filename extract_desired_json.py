#extract_desired_json.py


import os
import json
import openai
import instructor
from typing import List
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(filename='pipeline.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = instructor.from_openai(OpenAI())

class Dimension(BaseModel):
    value: float
    unit: str

class BuildVolume(BaseModel):
    width: Dimension
    length: Dimension
    height: Dimension

class SpecificationsDetail(BaseModel):
    manufacturer: str
    printer_model: str
    printing_technology: str
    build_volume: BuildVolume
    compatible_material: List
    support_material: List

def process_file(input_folder, input_path, output_folder, model_type):
    try:
        with open(input_path, 'r', encoding="utf-8") as file:
            text = file.read()

        if len(text.split()) > 16400:
            raise ValueError("Input file content exceeds the maximum token limit for processing")

        if model_type == "gpt-3.5-turbo":
            model = "gpt-3.5-turbo"
        elif model_type == "gpt-4o-mini":
            model = "gpt-4o-mini"
        elif model_type == "gpt-4":
            model = "gpt-4"
        else:
            raise ValueError("Invalid model type selected")

        specifications = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Extract specifications from the text"},
                {"role": "user", "content": text},
            ],
            response_model=SpecificationsDetail
        )

        specifications_dict = specifications.dict()
        relative_path = os.path.relpath(input_path, input_folder)
        output_path = os.path.join(output_folder, relative_path.replace(".txt", ".json"))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding="utf-8") as output_file:
            json.dump(specifications_dict, output_file, indent=2, ensure_ascii=False)
        
        logging.debug(f"Output saved to: {output_path}")

    except Exception as e:
        logging.error(f"Error processing file '{input_path}': {str(e)}")

def process_folder(input_folder, output_folder, model_type):
    try:
        logging.debug(f"Processing folder: {input_folder}")
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                input_path = os.path.join(root, file)
                logging.debug(f"Processing file: {input_path}")
                process_file(input_folder, input_path, output_folder, model_type)
    except Exception as e:
        logging.error(f"Unexpected error processing folder {input_folder}: {e}")