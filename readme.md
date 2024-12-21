# 项目概要
> 本项目是基于讯飞大模型平台星辰MAAS微调的拉康精神分析模型的数据集构建方案，模型以拉康的手段进行精神分析诊断或说明精神分析学概念。
> 请评审会审核
## 项目文件树：
├── Lacan
│   ├── alpaca.py
│   ├── app.log
│   ├── app1.log
│   ├── chunk.py
│   ├── convert.py
│   ├── datasets
│   ├── merge.py
│   ├── remove.py
│   ├── requirements.txt
│   ├── saveChunk
│   ├── saveChunk1
│   ├── system.py
│   ├── 拉康研讨班.md
│   └── 拉康选集.md
└── readme.md
## 项目使用说明：
首先配置好基础的conda环境，下载annaconda
创建conda环境，`conda creat -n FT python==3.10`
文本分块：`python chunk.py`
生成问答数据对`python alpaca.py`
转换数据格式`python convert.py`
去除无效字段`python remove.py`
合并数据`python merge.py`
添加系统提示词`python system.py`
数据保存在datasets文件夹下。
