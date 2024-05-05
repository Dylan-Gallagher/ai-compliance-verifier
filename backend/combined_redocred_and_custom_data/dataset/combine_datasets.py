import json
import random

with open("training.json", "r") as file:
    sweng = json.load(file)

with open("train_revised.json", "r") as file:
    redocred = json.load(file)

with open("docred_meta/rel_info.json", "r") as file:
    docred_rel_info = json.load(file)

with open("docred_meta/rel2id.json", "r") as file:
    docred_rel2id = json.load(file)

with open("custom_meta/rel_info.json", "r") as file:
    sweng_rel_info = json.load(file)

# Remove empty vertex keys in redocred
for element in redocred:
    for vertex in element["vertexSet"]:
        for vertexInstance in vertex:
            del vertexInstance["global_pos"]
            del vertexInstance["index"]

# Add in docred rel_info values
docred_rel_info_modified = {f"P{i+26}": relation for i, relation in enumerate(docred_rel_info.values())}

# Combine our rel_info with docred rel_info
combined_rel_info = {**sweng_rel_info, **docred_rel_info_modified}

with open("rel_info.json", "w") as file:
    json.dump(combined_rel_info, file, indent=4)

# Make a combined rel2id
combined_rel2id = {f"P{i}": i for i in range(1, 122)}
combined_rel2id["Na"] = 0

with open("rel2id.json", "w") as file:
    json.dump(combined_rel2id, file, indent=4)

reverse_combined_rel_info = {value: key for key, value in combined_rel_info.items()}

# Update redocred relations to the new dataset values
for element in redocred:
    for label in element["labels"]:
        label["r"] = reverse_combined_rel_info[docred_rel_info[label["r"]]]

combined_dataset = redocred + sweng
random.shuffle(combined_dataset)

with open("docred/train.json", "w") as file:
    json.dump(combined_dataset, file, indent=4)
