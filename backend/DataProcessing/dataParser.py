import json
import networkx as nx




def calculate_centralities(input_file):
    G = nx.DiGraph()  # Create a directed graph
    centrality_values = {}
    

    with open(input_file, 'r') as infile:
        for line in infile:
            data = json.loads(line)
            G.add_edge(data['head'], data['tail'])  # Add a directed edge

    # Calculate centralities
    degree_centrality = nx.in_degree_centrality(G)  
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    # eigenvector_centrality = nx.eigenvector_centrality(G)  # Calculate eigenvector centrality

    centrality_values['value'] = degree_centrality
    centrality_values['betweenness_centrality'] = betweenness_centrality
    centrality_values['closeness_centrality'] = closeness_centrality
    # centrality_values['eigenvector_centrality'] = eigenvector_centrality  # Add eigenvector centrality
    return centrality_values

def generate_nodes(input_file, centrality_values):
    nodes = []
    node_id = 1  # Start with ID 1
    seen_labels = set()  # Track labels we've already added
    category_colors = {
        'ORG': '#a2191f',  # Red
        'PER': '#0000FF',  # Blue
        'LOC': '#005d5d',  # Green
        'SYS': '#da1e28',  # Teal
        'ACT': '#24a148',  # Green
        'SPA': '#be95ff',  # Purple
        'STA': '#491d8b',  # Dark Purple
        'ALG': '#009d9a',  # Olive
        'PRO': '#a7f0ba',  # Cyan
        'HAR': '#da1e28',  # Magenta
        'MAR': '#800000',  # Maroon
        'DOC': '#4B4B4B',  # Dark Gray
        'ETH': '#a56eff',  # Pale Yellow
        'DAT': '#740937',
    }
    with open(input_file, 'r') as infile:
        for line in infile:
            data = json.loads(line)

            for entity in ['head', 'tail']:
                if data[entity] not in seen_labels:  # Check if new label
                    node = {
                    "id": node_id,
                    "label": data[entity],
                    "group": data[entity + '_cat'],
                    # "color": category_colors.get(data[entity + '_cat'], '#000000'), (color attribute no longer needed)
                    "title": f"Node name: {data[entity]}\n" +  # Multi-line 'title'
                             f"ID: {node_id}\n" +
                             f"Group: {data[entity + '_cat']}\n" + 
                             f"Value: {centrality_values['value'].get(data[entity], 0.0)}", 
                }
                    for centrality_name, centrality_dict in centrality_values.items():
                        node[centrality_name] = centrality_dict.get(data[entity], 0.0)

                    nodes.append(node)
                    node_id += 1
                    seen_labels.add(data[entity])  # Mark label as seen 
    return nodes

unique_edges = set()  # Set to store (from, to) tuples
def generate_edges(nodes, input_file):  
    edges = []
    relation_counts = {}  
    unique_edges = set()  # Track unique edge combinations

    with open(input_file, 'r') as infile:
        for line in infile:
            data = json.loads(line)
            relation_type = data['type']

            head_node = next(n for n in nodes if n['label'] == data['head'])  
            tail_node = next(n for n in nodes if n['label'] == data['tail']) 

            edge = {
                "from": head_node['id'],
                "to": tail_node['id'],
                # "color": head_node['color'], 
                "color": "#808080",
                "label": f"{relation_type}",
                "edge details": f"Head node: {head_node['label']}\n" +
                              f"Head node group: {head_node['group']}\n" +
                              f"Tail node: {tail_node['label']}\n" + 
                              f"Tail node group: {tail_node['group']}" 
            }

            relation_counts[relation_type] = relation_counts.get(relation_type, 0) + 1
            edge['weight'] = relation_counts[relation_type] 

            edge_key = (head_node['id'], tail_node['id'])
            if edge_key not in unique_edges:
                unique_edges.add(edge_key)
                edges.append(edge)

    return edges

def export_to_js(output_file, nodes, edges):
    """Exports data to a JavaScript file."""
    js_content = f"var nodes = \n{json.dumps(nodes, indent=4)};\n\n" \
                 f"var edges = \n{json.dumps(edges, indent=4)};"
    with open(output_file, 'w') as outfile:
        outfile.write(js_content)


# Main Logic
input_file = 'dreeam_output_combined.jsonl'
output_file = 'data.js'

centrality_values = calculate_centralities(input_file)
nodes = generate_nodes(input_file, centrality_values)
edges = generate_edges(nodes, input_file)
export_to_js(output_file, nodes, edges)