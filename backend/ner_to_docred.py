from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json

# Load model
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")
ner = pipeline("ner", model=model, tokenizer=tokenizer)

# Sample data
examples = ["My name is Micheal Wolfgang, and I live in Berlin",
            "My name is Dylan and I live in Dublin"]

tokens = [sentences.split() for sentences in examples]

# Pass data through NER model
ner_results = ner(examples)


def format_ner_tags(sentences, ner_output):
    formatted_ner = []
    output_dict = {}
    for i in range(len(ner_output)):
        formatted_ner.append([])
        for j in range(len(ner_output[i])):
            if (ner_output[i][j]["entity"][0] == "B"):
                formatted_ner[i].append({
                    "entity" : ner_output[i][j]["entity"].replace("B-", ""),
                    "wordStart" : ner_output[i][j]["index"],
                    "wordEnd": ner_output[i][j]["index"] + 1,
                    "word" : sentences[i][ner_output[i][j]["start"] : ner_output[i][j]["end"]],
                    "charStart" : ner_output[i][j]["start"],
                    "charEnd": ner_output[i][j]["end"],
                    "sentId": i
                })
            elif (ner_output[i][j]["entity"][0] == "I"):
                formatted_ner[i][len(formatted_ner[i]) - 1]["charEnd"] = ner_output[i][j]["end"]
                formatted_ner[i][len(formatted_ner[i]) - 1]["word"] =  sentences[i][
                    formatted_ner[i][len(formatted_ner[i]) - 1]["charStart"] : ner_output[i][j]["end"]]
                formatted_ner[i][len(formatted_ner[i]) - 1]["wordEnd"] = \
                    formatted_ner[i][len(formatted_ner[i]) - 1]["wordStart"] + 1 +(formatted_ner[i][len(formatted_ner[i]) - 1]["word"].count(" "))

    for i in range(len(formatted_ner)):
        for j in range(len(formatted_ner[i])):
            if formatted_ner[i][j]["word"] in output_dict.keys():
                output_dict[formatted_ner[i][j]["word"]].append(formatted_ner[i][j])
            else:
                output_dict[formatted_ner[i][j]["word"]] = []
                output_dict[formatted_ner[i][j]["word"]].append(formatted_ner[i][j])
    return output_dict

def ner_to_docred(sentences, ner_results, tokens):
    formatted_results = format_ner_tags(sentences, ner_results)
    output = [{}]
    output[0]["vertexSet"] = []
    i = 0
    for ner_word in formatted_results.keys():
        output[0]["vertexSet"].append([])
        for j in range(len(formatted_results[ner_word])):
            pos1 = formatted_results[ner_word][j]["wordStart"]
            pos2 = formatted_results[ner_word][j]["wordEnd"]
            entType = formatted_results[ner_word][j]["entity"]
            sentId = formatted_results[ner_word][j]["sentId"]
            name = formatted_results[ner_word][j]["word"]
            output[0]["vertexSet"][i].append(
                {
                "pos" : [pos1, pos2],
                "type": entType,
                "sent_id": sentId,
                "name" :name
            })

        output[0]["labels"] = [{"r": "", "h": "", "t": "", "evidence": []}]

        output[0]["title"] = "Legal text about AI"
        output[0]["sents"] = tokens
        i+=1
    return output


ner_json_format = ner_to_docred(examples, ner_results, tokens)
# Export data to JSON
with open("extracted_entities/dataset/docred/ner_output.json", 'w') as file:
    json.dump(ner_json_format, file, indent=4)
