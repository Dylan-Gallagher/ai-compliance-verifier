import json

path_docred = 'backend/docRed_2_kg/docred_example.json'

def type_to_group(type_code):
    return {
        "ORG": "Organisations",
        "PER": "Person",
        "LOC": "Location",
        "DAT": "Data",
        "SYS": "System",
        "ACT": "Action",
        "SPA": "Space",
        "STA": "Standard",
        "ALG": "Automated Process or Algorithm",
        "PRO": "Process",
        "HAR": "Harm",
        "MAR": "Marking",
        "DOC": "Document",
        "ETH": "Ethics"
    }.get(type_code, "Other")

def relation_to_label(relation_code):
    return {
        "P1": "interact with",
        "P2": "perform in",
        "P3": "are central to",
        "P4": "utilises",
        "P5": "involved in",
        "P6": "based on",
        "P7": "relate to",
        "P8": "require",
        "P9": "consider",
        "P10": "has implications for",
        "P11": "governs or guides",
        "P12": "is affected by",
        "P13": "certifies or validates",
        "P14": "regulates",
        "P15": "must be",
        "P16": "must not be",
        "P17": "should be",
        "P18": "should not be",
        "P19": "can be",
        "P20": "cannot be",
        "P21": "helps",
        "P22": "works with",
        "P23": "contains",
        "P24": "applies to",
        "P25": "does not apply to"
    }.get(relation_code, "Other")

with open(path_docred,'r') as file:
    data = json.load(file)

entity_info = {}
nodes = []
vertices = []

for doc in data:
    sentence = ' '.join(doc["sents"][0])
    entity_info[sentence] = {}
    
    for i, vertex in enumerate(doc["vertexSet"]):
        entity_info[sentence][str(i)] = {
            "type": vertex["type"],
            "name": vertex["name"],
            "tails": []
        }
        
    for label in doc["labels"]:
        head_index = str(label["h"])
        tail_index = str(label["t"])
        tail_entity_name = doc["vertexSet"][label["t"]]["name"]
        
        if tail_entity_name not in entity_info[sentence][head_index]["tails"]:
            entity_info[sentence][head_index]["tails"].append(tail_entity_name)

current_node_id = 1
node_id_mapping = {}  # Maps sentence index and vertex index to node ID
for sentence, entities in entity_info.items():
    for entity_index, entity_details in entities.items():
        node = {
            "id": current_node_id,
            "label": entity_details["name"],
            "title": f"Type: {type_to_group(entity_details['type'])}<br>Tail: {', '.join(entity_details['tails'])}<br>Centrality: 0.000",
            "value": 0,
            "group": type_to_group(entity_details["type"]),
            "x": 0,
            "y": 0
        }
        nodes.append(node)
        node_id_mapping[(sentence, entity_index)] = current_node_id
        current_node_id += 1

for doc in data:
    sentence = ' '.join(doc["sents"][0]) 
    for label in doc["labels"]:
        head_index = str(label["h"])
        tail_index = str(label["t"])
        
        if (sentence, head_index) in node_id_mapping and (sentence, tail_index) in node_id_mapping:
            vertex = {
                "from": node_id_mapping[(sentence, head_index)],
                "to": node_id_mapping[(sentence, tail_index)],
                "label": relation_to_label(label["r"])
            }
            vertices.append(vertex)

js_file_path = 'backend/docRed_2_kg/kg_data.js'
with open(js_file_path, 'w') as js_file:
    js_file.write("var nodes = ")
    json.dump(nodes, js_file, indent=4)
    js_file.write(";\n\nvar edges = ")
    json.dump(vertices, js_file, indent=4)
    js_file.write(";")