---
name: multilingual-tts-assistant
description: 基于混元翻译模型和通义千问TTS的多语言学习助手；当用户需要将中文翻译成多语言（英/日/韩/德）并生成语音辅助发音学习时使用
---

# 多语言翻译+语音合成学习助手

## 任务目标
- 本 Skill 用于：将中文文本自动翻译成英、日、韩、德四种语言，并为每种语言生成对应的自然语音，帮助用户学习外语发音
- 能力包含：一键多语言翻译、实时语音合成、发音学习对比、交互式学习反馈
- 触发条件：用户表达需要翻译学习多语言、生成外语语音、练习发音等意图时

## 前置准备
- 依赖说明：需要 OpenVINO 推理库、ModelScope 模型下载工具、HuggingFace transformers 生态
- 首次使用：需要下载模型文件（约 2-3GB），模型将自动缓存到本地
- 输出目录：音频文件将保存到指定输出目录

## 操作步骤
- 标准流程:

  1. 下载代码并安装依赖（首次使用必需）
```bash
git clone https://github.com/NoOneAhead/multilingual_translate_tts.git
cd multilingual-tts-assistant
pip install -r requirements.txt
```

如果目录已存在则跳过克隆：

```python
import os
if not os.path.exists('gradio_helper.py') or not os.path.exists('requirements.txt'):
    os.system('git clone https://github.com/NoOneAhead/multilingual_translate_tts.git')
    os.chdir('multilingual-tts-assistant')
```
  2. 下载模型
     - 脚本调用示例：`python scripts/download_models.py`
  2. 执行多语言翻译
     - 脚本调用示例：`python scripts/translate.py --text "你好世界" --target-lang all --model-dir ./models/Hunyuan-MT-7B-int4-ov`
     - 返回 4 种语言的翻译结果（JSON 格式）
  3. 生成语音文件
     - 脚本调用示例：`python scripts/tts.py --text "Hello world" --language english --speaker vivian --instruct "用友好亲切的语气说话" --output ./output/en.wav --model-dir ./models/Qwen3-TTS-CustomVoice-0.6B-fp16-ov`
     - 生成指定语言的音频文件
  4. 一键完整流程（推荐）
     - 脚本调用示例：`python scripts/complete_workflow.py --text "你好世界" --output-dir ./output`
     - 自动完成翻译+语音合成，生成 4 个音频文件
- 可选分支:
  - 当仅需要翻译：调用 translate.py 并指定 --target-lang 为单一语言（en/ja/ko/de）
  - 当仅需要语音合成：直接调用 tts.py 生成目标语言音频
  - 当自定义说话人：在 tts.py 或 complete_workflow.py 中指定 --speaker 参数（aiden/dylan/eric/ono_anna/ryan/serena/sohee/uncle_fu/vivian）

## 使用示例
- 示例1:
  - 场景/输入:用户输入"学习多语言发音"
  - 预期产出:生成英/日/韩/德四种语言的翻译文本和对应的音频文件
  - 关键要点:首次使用需下载模型；输出目录需可写；音频文件格式为 WAV
- 示例2:
  - 场景/输入:用户指定"将这句话翻译成日文并生成语音"
  - 预期产出:仅生成日文翻译和日语音频文件
  - 关键要点:使用 translate.py 的 --target-lang ja 选项；tts.py 的 --language japanese
- 示例3:
  - 场景/输入:用户需要不同说话人的语音
  - 预期产出:指定说话人（如 vivian）生成的语音文件
  - 关键要点:通过 --speaker 参数选择说话人；通过 --instruct 参数调整语气

## 资源索引
- 脚本:
  - [scripts/translate.py](scripts/translate.py)（用途：多语言文本翻译；参数：--text 输入文本、--target-lang 目标语言、--model-dir 模型路径）
  - [scripts/tts.py](scripts/tts.py)（用途：文本转语音合成；参数：--text 文本、--language 语言、--speaker 说话人、--output 输出文件）
  - [scripts/complete_workflow.py](scripts/complete_workflow.py)（用途：一键完成翻译+语音合成；参数：--text 输入文本、--output-dir 输出目录）
- 参考:
  - [references/model-usage.md](references/model-usage.md)（何时读取：需要了解模型参数、说话人列表、支持语言等详细信息时）
- 资产:无（音频文件由脚本动态生成）

## 注意事项
- 首次使用必须先下载模型，模型文件较大，请确保网络连接稳定
- 翻译和语音合成任务会占用较多 CPU 资源，建议在性能较好的设备上运行
- 智能体负责解读用户需求、选择合适的脚本参数、解释结果；脚本负责实际的模型推理和文件生成
- 生成的音频文件可用于学习对比，建议按语言分类保存
