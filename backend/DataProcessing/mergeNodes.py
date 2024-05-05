import json
from transformers import BertModel, BertTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def load_jsonl(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def save_jsonl(filepath, data):
    with open(filepath, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + "\n")


def get_embedding(text):
    inputs = tokenizer(text,
                       return_tensors="pt",
                       padding=True,
                       truncation=True,
                       max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.detach().numpy()


def compute_embeddings(data):
    unique_entities = set()
    for item in data:
        unique_entities.add(item['head'])
        unique_entities.add(item['tail'])
    embeddings_dict = {phrase: get_embedding(phrase) for phrase in unique_entities}
    return embeddings_dict


def find_similar_terms(embeddings_dict, threshold=0.96):
    phrases = list(embeddings_dict.keys())
    embeddings = np.array([embeddings_dict[phrase] for phrase in phrases])
    embeddings = np.squeeze(embeddings)
    similarity_matrix = cosine_similarity(embeddings)
    term_mapping = {}
    mapped_phrases = set()
    for i, phrase_i in enumerate(phrases):
        if phrase_i in mapped_phrases:
            continue
        for j, phrase_j in enumerate(phrases):
            if i != j and phrase_j not in mapped_phrases and similarity_matrix[i, j] > threshold:
                if phrase_i not in term_mapping:
                    term_mapping[phrase_j] = phrase_i
                    mapped_phrases.add(phrase_i)
                    mapped_phrases.add(phrase_j)
                else:
                    common_phrase = term_mapping[phrase_i]
                    term_mapping[phrase_j] = common_phrase
                    mapped_phrases.add(phrase_j)
    return term_mapping


def apply_mapping(data, mapping):
    for item in data:
        original_head = item['head']
        original_tail = item['tail']
        if item['head'] in mapping:
            mapped_head = mapping[item['head']]
            print(f"Mapping '{original_head}' to '{mapped_head}' in 'head'")
            item['head'] = mapped_head
        if item['tail'] in mapping:
            mapped_tail = mapping[item['tail']]
            print(f"Mapping '{original_tail}' to '{mapped_tail}' in 'tail'")
            item['tail'] = mapped_tail
    return data


def run(filepath):
    data = load_jsonl(filepath)
    embeddings_dict = compute_embeddings(data)
    term_mapping = find_similar_terms(embeddings_dict)
    updated_data = apply_mapping(data, term_mapping)
    save_jsonl("dreeam_merged2.jsonl", updated_data)


if __name__ == "__main__":
    run("spellCheckedData.jsonl")
