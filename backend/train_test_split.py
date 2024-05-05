import json
import sys
import os


def train_test_split(path, train_size=0.8):
    """
    train_dev_test_split:
        Takes a path to a json file and splits it into train, dev and test datasets according to train_size and dev_size
    """
    with open(path, "r") as file:
        data = json.load(file)

    n = len(data)

    # Dataset = (train:dev:test)
    train_test_boundary = int(train_size * n)

    # Split the data into train-dev-test
    train_split = data[:train_test_boundary]
    test_split = data[train_test_boundary:]

    # Make new directory
    folder_path = "dataset/dataset/docred"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


    # Export the splits to json files
    with open(os.path.join(folder_path, "train.json"), "w") as file:
        json.dump(train_split, file, indent=4)

    with open(os.path.join(folder_path, "dev.json"), "w") as file:
        json.dump(test_split, file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        train_test_split(sys.argv[1])
    else:
        print("Usage: python train_test_dev_split.py path/to/file_you_want_to_split.json")

