from parse_EU_act import parse_EU_act
from auto_label_function import set_to_lower, filter_text, paragraph_to_labeled_sentences, better_studio
from transformers import AutoTokenizer, AutoModelForMaskedLM
from auto_ner_to_docred import auto_ner_to_docred
import re
import json


def split_into_sentences(ai_act):
    ai_act = filter_text(ai_act)
    ai_act = ai_act.replace("\n", " ")
    ai_act = ai_act.replace("  ", " ")
    sentences = re.split(r'[.;]', ai_act)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 7]
    for i in range(len(sentences)):
        sentences[i] = sentences[i].replace("\n", "")
        while len(sentences[i]) != 0 and (sentences[i][0] == " "):
            sentences[i] = sentences[i][1:]
    return sentences


def sliding_window(sent_array, window_size, stride):
    windows = []
    i = 0
    while i < len(sent_array):
        this_arr_len = min(window_size, len(sent_array) - i)
        this_sentence = ""
        j = 0
        while j < this_arr_len:
            if this_sentence != "":
                this_sentence += " "
            this_sentence += sent_array[i] + "."
            j += 1
        windows.append(this_sentence)
        i += stride
    return windows


def paragraphs_token_limit(sentences, model_name_or_path):
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    paragraphs = []
    i = 0
    while i < len(sentences):
        this_sentence = ""
        total_tokens = 0
        while total_tokens < 512 and i < len(sentences):
            new_sentence = this_sentence
            if new_sentence != "":
                new_sentence += " "
            new_sentence += sentences[i] + "."
            new_total_tokens = len(tokenizer.tokenize(new_sentence))
            if new_total_tokens < 512:
                this_sentence = new_sentence
                i += 1
                total_tokens = new_total_tokens
            else:
                paragraphs.append(this_sentence)
                break
    return paragraphs


def filter_paragraphs(paragraphs):
    # Remove empty entities
    for paragraph in paragraphs:
        indices_to_remove = []
        for i, entity in enumerate(paragraph[0]["predictions"][0]["result"]):
            if not entity["value"]["text"].strip():
                indices_to_remove.append(i)
        for index in sorted(indices_to_remove, reverse=True):
            del paragraph[0]["predictions"][0]["result"][index]

    return paragraphs


def to_docred(auto_ner_output):
    docred_format = [auto_ner_to_docred(sentence)[0] for sentence in auto_ner_output]
    docred_format_filtered = [element for element in docred_format if len(element["vertexSet"]) > 1 and len(element["vertexSet"][0]) > 1]

    for element in docred_format_filtered:
        element.pop("labels", None)

    for i in range(len(docred_format_filtered)):
        docred_format_filtered[i]["title"] += f", {i}"

    for element in docred_format_filtered:
        element["sents"].pop()

    return docred_format_filtered


def dump_to_json(docred_format):
    with open("ai_act_docred_format.json", "w") as outfile:
        json.dump(docred_format, outfile, indent=4)


def main():
    set_to_lower()
    ai_act = parse_EU_act("ai_act/ai-act-draft.pdf")
    sentences = split_into_sentences(ai_act)
    sliding_window_sentences = sliding_window(sentences, 3, 2)
    tokenizer = AutoTokenizer.from_pretrained("FacebookAI/roberta-large")
    paragraphs = [sent for sent in sliding_window_sentences if len(tokenizer.tokenize(sent)) <= 512]
    auto_ner_output = [better_studio(*paragraph_to_labeled_sentences(paragraph)) for paragraph in paragraphs]
    auto_ner_output = filter_paragraphs(auto_ner_output)
    docred_format = to_docred(auto_ner_output)
    dump_to_json(docred_format)


if __name__ == "__main__":
    main()

