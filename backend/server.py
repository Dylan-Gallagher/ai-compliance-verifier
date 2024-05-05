from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from documentation_input.pdf_parser import convert_pdf_data_to_json_data
from rules_mining.rules_mining import pdf_data_to_rules
import json

ALLOWED_ORIGINS = {'http://localhost:3000', 'https://group22.sprinty.tech'}

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

@app.route('/', methods=['GET'])
def home():
    return 'Hello, GET Method', 200

@app.route('/upload', methods=['POST'])
def process():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file part in the request'}), 400
    if file and file.filename.endswith('.pdf'):
        response = json.loads(convert_pdf_data_to_json_data(file.read()))
        factsheet_data = response['parsed_data']
        empty_fields = response['empty_fields']
        if empty_fields:
            return jsonify({'error': 'Some fields are empty', 'empty_fields': empty_fields}), 400
        rules_mining = pdf_data_to_rules(json.dumps(factsheet_data))
        response_data = {
            'factsheet_data': factsheet_data,
            'rules_mining_data': rules_mining
        }
        return jsonify(response_data), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400


if __name__ == '__main__':
    print("App is starting")
    app.run(host='0.0.0.0', port=8000)