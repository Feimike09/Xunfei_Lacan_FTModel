import json
import os
import time
import pandas as pd
import re
from typing import List, Dict
from openai import OpenAI
import logging
import backoff

# 设置日志
logging.basicConfig(filename='app8.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 初始化 OpenAI 客户端
client = OpenAI(base_url="https://api.deepseek.com/v1", api_key="sk-ae284886694a4020aae65e61402db9e2")  # 替换为你的 API 密钥

def read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def generate_single_entry(text: str) -> Dict:
    prompt = f"""
    你现在是一个模型微调大师，请帮助我构建一个微调数据集，相关资料和要求在下方
    - 让微调模型具有对用户输入打分的能力
    - 根据黑话晦涩程度、哲学深度、符号使用频率等标准，为文本生成黑话评分，趣味化展示文本的“黑话浓度”。
    例如：
    {{
      "instruction": "给这段文字的黑话晦涩度打分：'象征界是一架自动机器，能指的差异性法则以一种不为主体所知的方式主宰着象征界的运作'。",
      "input": "象征界是一架自动机器，能指的差异性法则以一种不为主体所知的方式主宰着象征界的运作。",
      "output": "黑话评分：9/10。这段文本充满了拉康的专业术语，如'象征界'、'能指'等，晦涩度极高。"
}}
    
    文本内容：
    {text}

    请以下面的格式生成条目，确保所有字段都有适当的内容：
    {{
        "instruction": "请按照上述示例和要求，提出一个具体的、与文本相关的问题或任务",
        "input": "用户可能的输入",
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
                if entry and all(key in entry for key in ['instruction', 'input', 'output']):
                    dataset.append(entry)
                    logger.info(f"  成功生成 1 个完整条目")
                else:
                    logger.warning(f"  跳过不完整的条目")
                time.sleep(2)  # 在请求之间增加延迟到2秒

    return dataset

def save_dataset_as_json(dataset: List[Dict], output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_folder = "../saveChunk"  # 指定输入文件夹路径
    output_file = "../datasets/lacan8.json"  # 修改输出文件为JSON格式

    logger.info("开始生成数据集")
    dataset = generate_dataset(input_folder, entries_per_file=1)
    save_dataset_as_json(dataset, output_file)
    logger.info(f"数据集已生成并保存到 {output_file}")
    logger.info(f"共生成 {len(dataset)} 个有效条目")
