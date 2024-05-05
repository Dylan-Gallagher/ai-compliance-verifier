# pip install pymupdf

import fitz  # Import the PyMuPDF library
import re
import json
import os 

def parse_model_doc(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ''
        for page in doc:
            text += page.get_text()
    return text

def parse_text_into_sections(text, structure):
    extracted = {}
    for main_section, sub_sections in structure.items():
        if isinstance(sub_sections, dict):  # For nested sections
            extracted[main_section] = {}
            for sub_section, regex_pattern in sub_sections.items():
                match = re.search(regex_pattern, text, re.DOTALL)
                if match:
                    clean_text = match.group(1).strip().replace("\\", "").replace("\n", " ")
                    extracted[main_section][sub_section] = clean_text
                else:
                    extracted[main_section][sub_section] = ""
        else:  # For direct string values / patterns
            match = re.search(sub_sections, text, re.DOTALL)
            if match:
                clean_text = match.group(1).strip().replace("\\", "").replace("\n", " ")
                extracted[main_section] = clean_text
            else:
                extracted[main_section] = ""
    return extracted

def save_to_json(data, file_name="output.json"):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

def save_to_py(data, file_name="../rules_mining/factsheet_data.py"):
    with open(file_name, 'w') as file:
        file.write("json_data = ")
        json.dump(data, file, indent=4)

def parse_pdf_to_doc(pdf_data):
    with fitz.open(stream=pdf_data, filetype="pdf") as doc:
        text = ''
        for page in doc:
            text += page.get_text()
    return text

# Updated dictionary to match the structure and content of your PDF text output
ai_model_documentation = {
    "model": {
        "name": r"Model\s+Name:\s+(.*?)\n"
    },
    "author_notes": {
        "ensemble": r"Ensemble:\s+(.*?)(?=Robustness:|\Z)",
        "robustness": r"Robustness:\s+(.*?)(?=Overview|\Z)"
    },
    "overview": {
        "document_summary": r"Document Summary:\s+(.*?)(?=Purpose:|\Z)",
        "purpose": r"Purpose:\s+(.*?)(?=Intended Domain:|\Z)",
        "intended_domain": r"Intended Domain:\s+(.*?)(?=Training Data|\Z)"
    },
    "training_data": {
        "dataset_used": r"Dataset Used:\s+(.*?)(?=Preprocessing:|\Z)",
        "preprocessing": r"Preprocessing:\s+(.*?)(?=Model Information|\Z)"
    },
    "model_information": {
        "architecture_description": r"Architecture Description:\s+(.*?)(?=Input Output Process:|\Z)",
        "input_output_process": r"Input Output Process:\s+(.*?)(?=Inputs and Outputs|\Z)"
    },
    "inputs_outputs": {
        "inputs": r"Inputs:\s+(.*?)(?=Outputs:|\Z)",
        "outputs": r"Outputs:\s+(.*?)(?=Performance Metrics|\Z)"
    },
    "performance_metrics": {
        "metrics_used": r"Metrics Used:\s+(.*?)(?=Results:|\Z)",
        "results": r"Results:\s+(.*?)(?=Bias|\Z)"
    },
    "bias": {
        "potential_biases": r"Potential Biases:\s+(.*?)(?=Robustness Tests|\Z)"
    },
    "robustness_tests": {
        "attack_resilience": r"Attack Resilience:\s+(.*?)(?=Domain Shift|\Z)"
    },
    "domain_shift": {
        "evaluation": r"Evaluation:\s+(.*?)(?=Test Data|\Z)"
    },
    "test_data": {
        "description": r"Description:\s+(.*?)(?=Split Ratio:|\Z)",
        "split_ratio": r"Split Ratio:\s+(.*?)(?=Class Ratio Maintenance:|\Z)",
        "class_ratio_maintenance": r"Class Ratio Maintenance:\s+(.*?)(?=Operational Conditions|\Z)"
    },
    "operational_conditions": {
        "optimal_conditions": r"Optimal Conditions:\s+(.*?)(?=Poor Conditions:|\Z)",
        "poor_conditions": r"Poor Conditions:\s+(.*?)(?=Explanation|\Z)"
    },
    "explanation": {
        "model_explainability": r"Model Explainability:\s+(.*?)(?=Contact|\Z)"
    },
    "contact": {
        "information": r"Contact\s+Information:\s+(.*?)$"
    }
}

def convert_pdf_data_to_json_data(pdf_data):
    text_data = parse_pdf_to_doc(pdf_data)
    parsed_data = parse_text_into_sections(text_data, ai_model_documentation)

    # Check for empty fields
    empty_fields = [key for key, value in parsed_data.items() if not value or (isinstance(value, dict) and not all(value.values()))]

    return json.dumps({'parsed_data': parsed_data, 'empty_fields': empty_fields}, indent=4)



if __name__ == "__main__":
    pdf_path = "./GoodAI_FactSheet.pdf"

    #pdf_path = 'backend/documentation_input/SentimAI_FactSheet.pdf'

    # Assuming you've already run the parse_model_doc function and have the pdf_text variable
    pdf_text = parse_model_doc(pdf_path)

    # Let's use the provided text output directly for demonstration, assuming it's stored in pdf_text
    parsed_data = parse_text_into_sections(pdf_text, ai_model_documentation)

    # Save the structured dictionary to a JSON file
    save_to_json(parsed_data)

    # Save the structured dictionary to a Python file
    save_to_py(parsed_data)

    print("Data has been parsed and saved to output.json.")
