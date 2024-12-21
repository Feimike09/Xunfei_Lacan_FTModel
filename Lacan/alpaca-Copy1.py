import json
import os
import time
import pandas as pd
import re
from typing import List, Dict
from openai import OpenAI
import logging
import backoff
import pyarrow as pa
import pyarrow.parquet as pq

# 设置日志
logging.basicConfig(filename='app1.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 初始化 OpenAI 客户端
client = OpenAI(base_url="https://api.deepseek.com/v1", api_key="")  # 替换为你的 API 密钥

def read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def generate_single_entry(text: str) -> Dict:
    prompt = f"""
    你现在是一个模型微调大师，请帮助我构建一个微调数据集，相关资料和要求在下方
    - 基座模型：qwen7b 
    - 让微调模型具有话语分析的能力
    - 利用拉康的精神分析理论，对输入文本进行符号学和精神分析层面的解构，揭示潜意识中的“欲望”与“缺失”。
    例如：
    {
      "instruction": "利用拉康的精神分析理论对以下句子进行符号学和精神分析层面的解构：‘我渴望成功。’",
      "input": "我渴望成功。",
      "output": "‘渴望’一词揭示了主体对成功的无尽追求，这不仅是对成就的欲望，也是对大他者认可的需求。"
    }
    文本内容：
    {text}

    请以下面的格式生成条目，确保所有字段都有适当的内容：
    {{
        "instruction": "请按照上述要求，提出一个具体的、与文本相关的问题或任务",
        "input": "关于此段文字用户可能的输入",
        "output": "对instruction的详细回答或任务的完成结果"
    }}
    确保所有生成的内容都与给定的文本直接相关，生成的是有效的JSON格式，并且内容高质量、准确、详细。
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # 降低温度以使得生成内容更贴近原文
        )
        logger.info(f"API 响应: {response.choices[0].message.content}")

        json_match = re.search(r'\{.*\}', response.choices[0].message.content, re.DOTALL)
        if json_match:
            entry = json.loads(json_match.group())
            required_keys = ['instruction', 'input', 'output']
            if isinstance(entry, dict) and all(key in entry for key in required_keys):
                # 根据 input 是否为空来设置 text 字段
                if entry['input'].strip():
                    entry[
                        'text'] = f"Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.### Instruction: {entry['instruction']}\n### Input: {entry['input']}\n### Response: {entry['output']}"
                else:
                    entry[
                        'text'] = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.### Instruction: {entry['instruction']}\n### Input: {entry['input']}\n### Response: {entry['output']}"

                logger.info("成功生成完整条目")
                return entry
            else:
                logger.warning("JSON 解析成功，但缺少必要字段")
                return {}
        else:
            logger.error("无法从API响应中提取有效的JSON")
            return {}

    except Exception as e:
        logger.error(f"生成条目时发生错误: {str(e)}")
        raise
def generate_dataset(folder_path: str, entries_per_file: int = 2) -> List[Dict]:
    dataset = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            logger.info(f"正在处理文件: {filename}")
            text = read_file(file_path)
            for j in range(entries_per_file):
                logger.info(f"  生成第 {j + 1}/{entries_per_file} 个条目")
                entry = generate_single_entry(text)
                if entry and all(key in entry for key in ['instruction', 'input', 'output', 'text']):
                    dataset.append(entry)
                    logger.info(f"  成功生成 1 个完整条目")
                else:
                    logger.warning(f"  跳过不完整的条目")
                time.sleep(2)  # 在请求之间增加延迟到2秒

    return dataset

def save_dataset_as_parquet(dataset: List[Dict], output_file: str):
    schema = pa.schema([
        ('instruction', pa.string()),
        ('input', pa.string()),
        ('output', pa.string()),
        ('text', pa.string())
    ])

    arrays = [
        pa.array([entry['instruction'] for entry in dataset]),
        pa.array([entry['input'] for entry in dataset]),
        pa.array([entry['output'] for entry in dataset]),
        pa.array([entry['text'] for entry in dataset])
    ]

    table = pa.Table.from_arrays(arrays, schema=schema)
    pq.write_table(table, output_file)

if __name__ == "__main__":
    input_folder = "../saveChunk"  # 指定输入文件夹路径
    output_file = "../lacan.parquet"

    logger.info("开始生成数据集")
    dataset = generate_dataset(input_folder, entries_per_file=2)
    save_dataset_as_parquet(dataset, output_file)
    logger.info(f"数据集已生成并保存到 {output_file}")
    logger.info(f"共生成 {len(dataset)} 个有效条目")