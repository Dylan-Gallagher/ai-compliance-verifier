from rules_mining import pdf_data_to_rules
import os
original_path = os.getcwd()
import sys
sys.path.insert(0, '../documentation_input')
from pdf_parser import convert_pdf_data_to_json_data
os.chdir(original_path)


with open("../documentation_input/GoodAI_FactSheet.pdf",'rb') as file:
    factsheet_data = convert_pdf_data_to_json_data(file.read())
    print(pdf_data_to_rules(factsheet_data))