import json


def read_dreeam_files():
    with open("dreeam/dataset/docred/test.json", "r") as file:
        dreeam_input = json.load(file)

    with open("dreeam/output_from_dreeam.json", "r") as file:
        dreeam_output = json.load(file)

    with open("dreeam/meta/rel_info.json", "r") as file:
        rel_info = json.load(file)

    return dreeam_input, dreeam_output, rel_info


def get_triplets(dreeam_input, dreeam_output, rel_info):
    relations = [{"input_idx": relation["title"].split()[-1],
                  "h_idx": relation["h_idx"],
                  "t_idx": relation["t_idx"],
                  "r": relation["r"]} for relation in dreeam_output]

    triplets = []
    for relation in relations:
        head = dreeam_input[int(relation["input_idx"])]["vertexSet"][relation["h_idx"]][0]["name"]
        tail = dreeam_input[int(relation["input_idx"])]["vertexSet"][relation["t_idx"]][0]["name"]
        head_cat = dreeam_input[int(relation["input_idx"])]["vertexSet"][relation["h_idx"]][0]["type"]
        tail_cat = dreeam_input[int(relation["input_idx"])]["vertexSet"][relation["t_idx"]][0]["type"]
        relation = rel_info[relation["r"]]

        if head == 'AI system':
            head = "AI systems"

        if tail == 'AI system':
            tail = "AI systems"

        triplets.append({"head": head, "head_cat": head_cat, "type": relation,"tail": tail, "tail_cat": tail_cat})

    return triplets


def find_matching_pairs(triplets):
    pairs = []
    seen = set()

    for i in range(len(triplets)):
        for j in range(i + 1, len(triplets)):
            dict1 = triplets[i]
            dict2 = triplets[j]

            # Check if head and tail match, but types are different
            if (dict1['head'], dict1['tail']) == (dict2['head'], dict2['tail']) and dict1['type'] != dict2['type']:
                # Create a key to ensure we don't find reverse duplicates
                key = tuple(sorted([dict1['head'], dict1['tail']]))

                if key not in seen:
                    pairs.append((dict1, dict2))
                    seen.add(key)

    return pairs


def dump_to_jsonl(triplets):
    with open("dreeam_outputs/dreeam_output_combined.jsonl", "w") as outfile:
        for data in triplets:
            json_line = json.dumps(data)
            outfile.write(json_line + "\n")


def main():
    dreeam_input, dreeam_output, rel_info = read_dreeam_files()
    triplets = get_triplets(dreeam_input, dreeam_output, rel_info)
    dump_to_jsonl(triplets)


if __name__ == "__main__":
    main()


