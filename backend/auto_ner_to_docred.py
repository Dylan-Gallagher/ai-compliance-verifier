import json
import os
import re

# Takes in token, list of tokens, and index of token to be split
# splits tokens with brackets/punctuation/whatever else and makes those seperate tokens.
def punc_split(token, tokens, index, startpunc, endpunc):
    last_element = token[len(token) - 1]
    first_element = token[0]
    # Checks if this is the root of the word
    root = True

    if first_element in ('(', '[', '{') and token not in ('(', '[', '{'):
        root = False
        startpunc += 1
        punc_split(token[1:len(token)], tokens, index, startpunc, endpunc)
        tokens.insert(index, first_element)
    if last_element in (',', ';', ':', ')', ']', '}') and token not in (',', ';', ':', ')', ']', '}') and root == True:
        root = False
        tokens.insert(index + 1, last_element)
        punc_split(token[0:len(token) - 1], tokens, index, startpunc, endpunc)

    if root == True:
        tokens[index] = token

    return tokens

def tokenize_sentence(sentence):
    tokens = sentence.split()
    i= 0
    oldlen =len(tokens)
    while i < len(tokens):
        tokens = punc_split(tokens[i], tokens, i, 0, 0)
        if (len(tokens) > oldlen):
            i-=1
            oldlen = len(tokens)
        i+=1
    splits_with_space = [True] * (len(tokens) - 1)

    index = 0
    for i in range(len(tokens) - 1):
        if (tokens[i] in [".", ",", ")", "]", "}", ";", ":"]):
            splits_with_space[i-1] = False
        elif (tokens[i] in ["(", "[", "{"]):
            splits_with_space[i] = False
    return tokens, splits_with_space

def get_token_index(tokenized_sentence, split_info, target_indexes):
    target_start, target_end = target_indexes
    cumulative_length = 0
    token_index = None

    for i, token in enumerate(tokenized_sentence):
        token_length = len(token)
        cumulative_length += token_length
        if cumulative_length >= target_end:  # Target token is within or after this token
            if cumulative_length - token_length <= target_start:  # Check if the target token starts within this token
                token_index = i
                break
        if (i < len(split_info)):
            cumulative_length += split_info[i]

    return token_index

def auto_ner_to_docred(data):
    output = [{}]
    output[0]["vertexSet"] = []
    output[0]["sents"] = []

    all_tags_dict = {}

    for i in range(len(data)):
        entry = data[i]
        text = entry["data"]["text"]
        tokens, gap_info = tokenize_sentence(text)
        for j in range(len(entry["predictions"][0]["result"])):
            tag_dict = entry["predictions"][0]["result"][j]



            pos1 = get_token_index(tokens, gap_info, (tag_dict["value"]["start"], tag_dict["value"]["start"] +
                                                             (len(tag_dict["value"]["text"].split()[0] ))))
            if (pos1 == None):
                try:
                    pos1 = tokens.index(tag_dict["value"]["text"].split()[0])
                except Exception as e:
                    tokens_chars = [" ", ".", ",", ";", ":", "(", ")", "[", "]", "{", "}", "?"]
                    token_count = 0
                    for tokens_char in tokens_chars:
                        token_count += text[:tag_dict["value"]["start"]].count(tokens_char)
                    pos1 = token_count

            pos2 = pos1 + len(tag_dict["value"]["text"].split())
            entType = tag_dict["value"]["labels"][0]
            sentId = i
            name = tag_dict["value"]["text"]

            if (name in all_tags_dict.keys()):
                all_tags_dict[name].append({
                    "pos" : [pos1, pos2],
                    "type": entType,
                    "sent_id": sentId,
                    "name" :name
                })
            else:
                all_tags_dict[name] = [{
                    "pos" : [pos1, pos2],
                    "type": entType,
                    "sent_id": sentId,
                    "name" :name
                }]


        output[0]["labels"] = [{"r": "", "h": "", "t": "", "evidence": []}]

        output[0]["title"] = "Legal text about AI"
        output[0]["sents"].append(tokens)

    for key in all_tags_dict.keys():
        if (len(all_tags_dict[key]) != 0):
            output[0]["vertexSet"].append(all_tags_dict[key])

    return output



if __name__ == "__main__":
    # File paths
    input_file = "training-data-final.json"
    output_file = "output.json"

    # Read input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Call ner_to_docred function
    output_data = auto_ner_to_docred(data)

    # Write output JSON file
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)
