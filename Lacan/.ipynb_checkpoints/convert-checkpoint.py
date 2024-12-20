import pandas as pd
import json
import os

def parquet_to_jsonl(parquet_file_path, jsonl_file_path):
    # 读取Parquet文件
    df = pd.read_parquet(parquet_file_path)

    # 将DataFrame转换为JSONL格式并保存到文件
    with open(jsonl_file_path, 'w', encoding='utf-8') as f:
        df.to_json(f, orient='records', lines=True)

def jsonl_to_json(jsonl_file_path, json_file_path):
    # 初始化一个列表来存储所有的JSON对象
    json_list = []

    # 逐行读取JSONL文件
    with open(jsonl_file_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            # 将每一行的JSON字符串转换为Python对象
            json_obj = json.loads(line)
            # 将Python对象添加到列表中
            json_list.append(json_obj)

    # 将列表转换为JSON数组并写入文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_list, json_file, ensure_ascii=False, indent=4)

# 调用函数进行转换
parquet_file_path = '/root/Lacan/datasets/lacanyt.parquet'
jsonl_file_path = './datasets/lacanyt.jsonl'
json_file_path = './datasets/lacanyt.json'

parquet_to_jsonl(parquet_file_path, jsonl_file_path)
jsonl_to_json(jsonl_file_path, json_file_path)    