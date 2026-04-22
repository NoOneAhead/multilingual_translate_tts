# 模型使用指南

## 概览

本指南详细说明多语言翻译和语音合成模型的使用方法、参数配置和最佳实践。

## 翻译模型 (Hunyuan-MT-7B)

### 模型说明
Hunyuan-MT-7B 是腾讯混元推出的多语言翻译模型，支持 33 种语言之间的互译。

### 支持的语言
本 Skill 使用的语言映射：
- `en`: 英文
- `ja`: 日文
- `ko`: 韩文
- `de`: 德文

### 模型参数

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `model_dir` | 模型目录路径 | `./models/Hunyuan-MT-7B-int4-ov` | - |
| `device` | 推理设备 | `CPU` | `CPU`, `AUTO` |
| `max_tokens` | 最大生成 token 数 | `256` | 正整数 |
| `temperature` | 采样温度 | `0.3` | 0.0-2.0 |
| `top_p` | nucleus sampling | `0.9` | 0.0-1.0 |

### 输入格式
- 单行或多行中文文本
- 建议长度：10-500 字符

### 输出格式
```json
{
  "status": "success",
  "source_text": "你好世界",
  "translations": {
    "en": "Hello world",
    "ja": "こんにちは世界",
    "ko": "안녕하세요 세계",
    "de": "Hallo Welt"
  }
}
```

### 性能参考
- 英文翻译：约 15-20 秒（CPU）
- 日文翻译：约 8-12 秒（CPU）
- 韩文翻译：约 14-16 秒（CPU）
- 德文翻译：约 10-12 秒（CPU）

## 语音合成模型 (Qwen3-TTS)

### 模型说明
Qwen3-TTS 是阿里巴巴通义千问团队推出的文本转语音模型，支持多语言语音合成、声音克隆和声音设计。

### 支持的语言
- `auto`: 自动识别
- `chinese`: 中文
- `english`: 英文
- `french`: 法文
- `german`: 德文
- `italian`: 意大利文
- `japanese`: 日文
- `korean`: 韩文
- `portuguese`: 葡萄牙文
- `russian`: 俄文
- `spanish`: 西班牙文

### 支持的说话人
- `aiden`: 男性声音，年轻
- `dylan`: 男性声音，稳重
- `eric`: 男性声音，成熟
- `ono_anna`: 女性声音，柔和
- `ryan`: 男性声音，活力
- `serena`: 女性声音，专业
- `sohee`: 女性声音，甜美
- `uncle_fu`: 男性声音，亲切
- `vivian`: 女性声音，友好（默认）

### 模型参数

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `model_dir` | 模型目录路径 | `./models/Qwen3-TTS-CustomVoice-0.6B-fp16-ov` | - |
| `device` | 推理设备 | `CPU` | `CPU`, `AUTO` |
| `speaker` | 说话人 | `vivian` | 见上方说话人列表 |
| `language` | 目标语言 | `english` | 见上方支持的语言 |
| `instruct` | 语气指令 | `null` | 自然语言描述 |
| `max_new_tokens` | 最大生成 token 数 | `2048` | 正整数 |

### 语气指令示例
- "用友好亲切的语气说话"
- "用专业正式的语气说话"
- "用活泼热情的语气说话"
- "用平静温和的语气说话"

### 输入格式
- 目标语言的文本
- 建议长度：10-500 字符

### 输出格式
```json
{
  "status": "success",
  "output_file": "/path/to/audio.wav",
  "language": "english",
  "speaker": "vivian",
  "sample_rate": 24000,
  "duration": 3.52,
  "inference_time": 1.25,
  "rtf": 0.355
}
```

### 性能指标
- RTF (Real-Time Factor): 推理时间 / 音频时长
- RTF < 1.0 表示实时生成
- 典型 RTF: 0.3-0.6（CPU）

## 常见问题

### 模型下载失败
- 检查网络连接
- 确保安装了 `modelscope`: `pip install modelscope`
- 检查磁盘空间（至少需要 3GB）

### 翻译结果不准确
- 确保输入是中文文本
- 调整 `max_tokens` 参数
- 尝试降低 `temperature` 参数

### 语音合成失败
- 确保安装了 Qwen3-TTS: `pip install -e Qwen3-TTS`
- 检查语言参数是否正确
- 确保文本长度在合理范围内

### 内存不足
- 使用 INT4 量化模型
- 减小 `max_tokens` 参数
- 关闭其他占用内存的程序

## 最佳实践

1. **首次使用**: 必须先运行 `download_models.py` 下载模型
2. **批量处理**: 使用 `complete_workflow.py` 一次性完成翻译和语音合成
3. **性能优化**: 使用 CPU 推理，如需加速可尝试 GPU（需硬件支持）
4. **音频质量**: 选择合适的说话人和语气指令以获得最佳效果
5. **文件管理**: 按语言和日期组织输出目录，便于管理

## 示例

### 示例1: 基础翻译
```bash
python scripts/translate.py --text "你好世界" --target-lang all
```

### 示例2: 基础语音合成
```bash
python scripts/tts.py --text "Hello world" --language english --speaker vivian --output ./output/en.wav
```

### 示例3: 完整工作流
```bash
python scripts/complete_workflow.py --text "学习多语言发音" --output-dir ./output
```

### 示例4: 自定义说话人
```bash
python scripts/complete_workflow.py --text "你好世界" --speaker ono_anna --output-dir ./output
```

### 示例5: 自定义语气
```bash
python scripts/tts.py --text "Hello" --language english --speaker vivian --instruct "用专业正式的语气说话" --output ./output/formal.wav
```
