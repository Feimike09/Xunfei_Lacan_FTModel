import json

def remove_keys_from_json(input_file, output_file, keys_to_remove):
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 检查data是否是列表，因为JSON文件可能包含一个对象或对象列表
    if isinstance(data, list):
        # 如果是列表，遍历每个对象
        for item in data:
            for key in keys_to_remove:
                if key in item:
                    del item[key]
    elif isinstance(data, dict):
        # 如果是单个对象，直接遍历键
        for key in keys_to_remove:
            if key in data:
                del data[key]
    
    # 将修改后的数据写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# 调用函数，传入输入文件名、输出文件名和要移除的键
remove_keys_from_json('./datasets/lacanyt.json', './datasets/lacanyt1.json', ['text'])