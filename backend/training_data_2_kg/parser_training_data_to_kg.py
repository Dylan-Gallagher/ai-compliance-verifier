import json
import random

# path = 'backend/training_data_2_kg/sample.json'

path = 'backend/training_data_2_kg/relation-training-data.json'

knowledge_graphs = []

with open(path, 'r') as file:
    data = json.load(file)

def find_entity_by_id(entity_id, annotations):
    for annotation in annotations:
        for result in annotation['result']:
            if 'id' in result and result['id'] == entity_id:
                return result
    return None

for item in data:
    annotations = item['annotations']
    for annotation in annotations:
        for result in annotation['result']:
            if result['type'] == 'relation':
                head_entity = find_entity_by_id(result['from_id'], annotations)
                tail_entity = find_entity_by_id(result['to_id'], annotations)
                if head_entity and tail_entity:
                    head_cat = head_entity['value']['labels'][0] if 'labels' in head_entity['value'] else 'Unknown'
                    tail_cat = tail_entity['value']['labels'][0] if 'labels' in tail_entity['value'] else 'Unknown'
                    knowledge_graphs.append({
                        "head": head_entity['value']['text'],
                        "head_cat": head_cat,
                        "type": result['labels'][0],
                        "tail": tail_entity['value']['text'],
                        "tail_cat": tail_cat
                    })

# print(json.dumps(knowledge_graphs, indent=2))
                    
# file_path = 'backend/training_data_2_kg/knowledge_graphs.jsonl'
# with open(file_path, 'w') as file:
#     for entry in knowledge_graphs:
#         json.dump(entry, file)
#         file.write('\n')
                    

nodes = []
edges = []
existing_nodes = {} 
node_details = {} 

next_id = 1 

def add_node(entity, category, tail=None):
    global next_id
    if entity not in existing_nodes:
        centrality = random.uniform(0, 0.01) if tail else 0  
        title = f"Type: {category}<br>"
        if tail:  
            title += f"Tail: {tail}<br>Centrality: {centrality:.16f}<br>"
        node = {
            "id": next_id,
            "label": entity,
            "title": title,
            "value": random.uniform(0, 1),
            "group": category,
            "x": random.randint(-100, 100),
            "y": random.randint(-100, 100)
        }
        nodes.append(node)
        existing_nodes[entity] = next_id
        node_details[next_id] = {"has_tail": bool(tail)}  
        next_id += 1
    else:
        node_id = existing_nodes[entity]
        if not node_details[node_id]["has_tail"] and tail:
            centrality = random.uniform(0, 0.01)
            for node in nodes:
                if node['id'] == node_id:
                    node['title'] += f"Tail: {tail}<br>Centrality: {centrality:.16f}<br>"
                    node_details[node_id]["has_tail"] = True
                    break

    return existing_nodes[entity]

for entry in knowledge_graphs:
    head_id = add_node(entry['head'], entry['head_cat'], entry['tail'])
    tail_id = add_node(entry['tail'], entry['tail_cat'])

    edge = {"from": head_id, "to": tail_id, "label": entry['type']}
    if edge not in edges:
        edges.append(edge)

js_file_path = 'backend/training_data_2_kg/data_from_training_relation_data.js'
with open(js_file_path, 'w') as js_file:
    js_file.write("var nodes = ")
    json.dump(nodes, js_file, indent=4)
    js_file.write(";\n\nvar edges = ")
    json.dump(edges, js_file, indent=4)
    js_file.write(";")

# print("var nodes = ")
# print(nodes)
# print("var edges = ")
# print(edges)
