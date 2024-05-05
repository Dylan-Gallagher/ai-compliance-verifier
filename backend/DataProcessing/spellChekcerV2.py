
import json
from spellchecker import SpellChecker

input_file = "dreeam_output_combined.jsonl"
output_file = "spellCheckedData.jsonl"
spell = SpellChecker()  # Initialize the spell checker

def load_data_from_jsonl(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            entry = json.loads(line)
            data.append(entry)  # Append the entire dictionary 
    return data

## Runs a spell check on the head, tail, and type(relation)
def spellcheck_array(data):
    corrected_data = []
    for entry in data:  # Iterate through dictionaries
        if entry['head'] is not None:  # Check for 'head'
            subwords = entry['head'].replace('_', ' ').replace('-', ' ').split(' ')  
            corrected_subwords = []  
            for subword in subwords:
                correction = spell.correction(subword) 
                if correction is not None:  
                    corrected_subwords.append(correction)
                else:
                    corrected_subwords.append(subword) 
            corrected_head = ' '.join(corrected_subwords) 
            entry['head'] = corrected_head  

        if entry['tail'] is not None: 
            subwords = entry['tail'].replace('_', ' ').replace('-', ' ').split(' ')  
            corrected_subwords = []  
            for subword in subwords:
                correction = spell.correction(subword) 
                if correction is not None:  
                    corrected_subwords.append(correction)
                else:
                    corrected_subwords.append(subword) 
            corrected_tail = ' '.join(corrected_subwords) 
            entry['tail'] = corrected_tail

        if entry['type'] is not None: 
            subwords = entry['type'].replace('_', ' ').replace('-', ' ').split(' ')  
            corrected_subwords = []  
            for subword in subwords:
                correction = spell.correction(subword) 
                if correction is not None:  
                    corrected_subwords.append(correction)
                else:
                    corrected_subwords.append(subword) 
            corrected_type = ' '.join(corrected_subwords) 
            entry['type'] = corrected_type

        corrected_data.append(entry)
    return corrected_data


## Saves Data to file whilst also checking for capital letters and stray random letters
def save_corrected_data(data, filename=output_file):
    with open(filename, 'w') as outfile:
        for entry in data:
            original_head = entry['head']
            original_tail = entry['tail']
            original_type = entry['type']

            corrected_head = capitalize_if_needed(original_head)  
            corrected_tail = capitalize_if_needed(original_tail)  
            corrected_type = capitalize_if_needed(original_type) 

            corrected_entry = {
                "head": corrected_head,
                "head_cat": entry['head_cat'],  
                "type": corrected_type,
                "tail": corrected_tail,
                "tail_cat": entry['tail_cat']
            }
            outfile.write(json.dumps(corrected_entry) + '\n')

## Capitalises first letter and checks for stray letters and removes them.
def capitalize_if_needed(text):
    if text: 
        words = text.split()  
        if len(words[0]) == 1:  
            if len(words) > 1:  # Ensure there's a word to capitalize
                words[1] = words[1].capitalize()  # Capitalize the second word
                text = " ".join(words[1:])  # Remove the first letter, join back
            else:
                text = ""  # If just a single letter, make the text empty
        else:
            words[0] = words[0].capitalize()  # Capitalize the first word (if not a single letter)
            text = " ".join(words)
        return text
    else:
        return text

if __name__ == "__main__":
    data = load_data_from_jsonl(input_file)
    corrected_data = spellcheck_array(data) 
    save_corrected_data(corrected_data) 

    print("Original Data:")
    print(data)

    print("\nCorrected Data:")
    print(corrected_data)