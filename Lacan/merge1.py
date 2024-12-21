import os
import json

# 指定要处理的文件夹路径
folder_path = './datasets'
# 输出文件路径
output_file_path = './merged.json'

# 确保输出文件夹存在
if not os.path.exists(os.path.dirname(output_file_path)):
    os.makedirs(os.path.dirname(output_file_path))

# 初始化一个空列表来存储所有JSON文件的内容
merged_data = []

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):  # 确保处理.json文件
        file_path = os.path.join(folder_path, filename)
        
        # 读取JSON文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 将读取的数据添加到列表中
        merged_data.append(data)

# 将合并后的数据写入新的JSON文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

print(f"所有JSON文件已合并并存储到 {output_file_path}")