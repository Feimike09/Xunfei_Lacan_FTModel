import os
import re
import json

# 指定要处理的文件夹路径
folder_path = './qadata'
# 输出文件夹路径
output_folder_path = './datasets'

# 确保输出文件夹存在
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 自定义文件名前缀
custom_prefix = "lacan_"

# 遍历文件夹中的所有文件
file_index = 1
for filename in os.listdir(folder_path):
    if filename.endswith('.log'):  # 确保处理.txt文件
        input_file_path = os.path.join(folder_path, filename)
        # 自定义输出文件名，添加唯一编号
        custom_filename = f"{custom_prefix}{file_index}.json"
        output_file_path = os.path.join(output_folder_path, custom_filename)

        # 读取文件内容
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式匹配JSON字段
        json_pattern = r'\{.*?\}'
        json_matches = re.findall(json_pattern, content, re.DOTALL)

        # 存储提取的JSON字段
        extracted_jsons = []

        for match in json_matches:
            try:
                # 尝试将匹配的字符串转换为JSON对象
                json_obj = json.loads(match)
                extracted_jsons.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"文件 {filename} 中的JSON解码错误: {e}")

        # 将提取的JSON字段写入新文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(extracted_jsons, output_file, ensure_ascii=False, indent=4)

        print(f"文件 {filename} 的JSON字段已提取并存储到 {output_file_path}")
        file_index += 1  # 更新文件编号