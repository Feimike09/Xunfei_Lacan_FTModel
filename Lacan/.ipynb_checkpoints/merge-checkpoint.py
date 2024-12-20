import json

# 读取第一个JSON文件
with open('./datasets/lacan6_1.json', 'r', encoding='utf-8') as f1:
    data1 = json.load(f1)

# 读取第二个JSON文件
with open('./datasets/lacanyt1.json', 'r', encoding='utf-8') as f2:
    data2 = json.load(f2)

# 将两个JSON文件的内容拼接成一个大的JSON数组
merged_data = data1 + data2

# 将合并后的数据写入新的JSON文件
with open('./datasets/lacan_fin.json', 'w', encoding='utf-8') as merged_file:
    json.dump(merged_data, merged_file, ensure_ascii=False, indent=4)