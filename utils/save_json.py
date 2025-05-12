import os
import json

def save_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def continue_save_json(data, file_path):
    with open(file_path, 'r') as f:
        datas = json.load(f)
    datas.extend(data)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(datas, f, ensure_ascii=False, indent=2)

def save_jsonl(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')