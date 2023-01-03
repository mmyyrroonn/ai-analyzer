import os
import json

def load_content(profile_id):
    file_path = build_path(profile_id)
    with open(file_path, "r") as file:
        data = json.load(file)

    # 获取 content 字段，并将它们存储到列表中
    content_list = [item["metadata"]["content"] for item in data]
    return content_list

def load_keywords(profile_id):
    file_path = build_result_path(profile_id)
    with open(file_path, "r") as file:
        data = json.load(file)

    keywords_list = [item["metadata"]["keyWords"] for item in data]
    return keywords_list

def build_path(profile_id: str):
    path = os.path.join("/home/ubuntu/ai-analyzer/ai_analyzer/data", profile_id+".json")
    return path

def build_result_path(profile_id: str):
    path = os.path.join("/home/ubuntu/ai-analyzer/ai_analyzer/data", profile_id+"-result.json")
    return path

def write_result(profile_id, results):
    file_path = build_path(profile_id)
    with open(file_path, "r") as file:
        data = json.load(file)

    for item, result in zip(data, results):
        item["metadata"]["keyWords"] = result

    result_file_path = build_result_path(profile_id)
    with open(result_file_path, 'w') as f:
        json.dump(data, f)
    