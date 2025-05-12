import os
import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data
