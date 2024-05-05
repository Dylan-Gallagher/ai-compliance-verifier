from pdf_parser import convert_pdf_data_to_json_data

with open("GoodAI_FactSheet.pdf",'rb') as file:
    print(convert_pdf_data_to_json_data(file.read()))