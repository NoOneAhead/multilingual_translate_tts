#!/usr/bin/env python3
"""
演示脚本：学习"早上好"的多国发音
基于灵感流的完整代码逻辑
"""

import sys
import json
from pathlib import Path

def show_translations():
    """展示"早上好"的多语言翻译"""

    print("=" * 80)
    print("🌅 学习主题：早上好")
    print("=" * 80)
    print()

    print("=" * 80)
    print("📝 多语言翻译结果")
    print("=" * 80)
    print()

    translations = {
        "en": {
            "language": "英文",
            "text": "Good morning",
            "phonetic": "ɡʊd ˈmɔːrnɪŋ",
            "chinese": "古德 摸宁"
        },
        "ja": {
            "language": "日文",
            "text": "おはようございます",
            "romaji": "Ohayō gozaimasu",
            "chinese": "哦哈哟 告扎伊马斯"
        },
        "ko": {
            "language": "韩文",
            "text": "안녕하세요",
            "romanization": "Annyeonghaseyo",
            "chinese": "安宁哈赛哟"
        },
        "de": {
            "language": "德文",
            "text": "Guten Morgen",
            "phonetic": "ˈɡuːtn̩ ˈmɔʁɡn̩",
            "chinese": "古滕 摩根"
        }
    }

    for code, info in translations.items():
        print(f"🇬🇧" if code == "en" else f"🇯🇵" if code == "ja" else f"🇰🇷" if code == "ko" else f"🇩🇪", end=" ")
        print(f"{info['language']}")
        print(f"  原文：{info['text']}")
        if 'phonetic' in info:
            print(f"  音标：{info['phonetic']}")
        if 'romaji' in info:
            print(f"  罗马音：{info['romaji']}")
        if 'romanization' in info:
            print(f"  罗马音：{info['romanization']}")
        print(f"  中文注音：{info['chinese']}")
        print()

    print("=" * 80)
    print("🎯 使用灵感流代码生成语音")
    print("=" * 80)
    print()

    print("【第一步：下载模型】")
    print("python scripts/download_models.py --model-dir ./models")
    print()

    print("【第二步：翻译文本】")
    print("""
from optimum.intel import OVModelForCausalLM
from transformers import AutoTokenizer

# 加载翻译模型
model = OVModelForCausalLM.from_pretrained(
    "./models/Hunyuan-MT-7B-int4-ov",
    device="CPU"
)
tokenizer = AutoTokenizer.from_pretrained("./models/Hunyuan-MT-7B-int4-ov")

# 构建翻译 prompt
prompt = (
    "<|im_start|>user\\n"
    "将下文翻译成英文：\\n"
    "早上好<|im_end|>\\n"
    "<|im_start|>assistant\\n"
)

# 执行翻译
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=256)
translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    """)
    print()

    print("【第三步：生成语音】")
    print("""
from qwen_3_tts_helper import OVQwen3TTSModel
from scipy.io import wavfile

# 加载语音合成模型
ov_model = OVQwen3TTSModel.from_pretrained(
    model_dir="./models/Qwen3-TTS-CustomVoice-0.6B-fp16-ov",
    device="CPU"
)

# 生成英文语音
wavs, sr = ov_model.generate_custom_voice(
    text="Good morning",
    speaker="vivian",
    language="english",
    instruct="用友好亲切的语气说话。",
    non_streaming_mode=True,
    max_new_tokens=2048,
)

# 保存音频文件
wavfile.write("en_good_morning.wav", sr, wavs[0])
    """)
    print()

    print("【第四步：生成其他语言语音】")
    print("""
# 生成日文语音
wavs, sr = ov_model.generate_custom_voice(
    text="おはようございます",
    speaker="vivian",
    language="japanese",
    instruct="用友好亲切的语气说话。",
    non_streaming_mode=True,
    max_new_tokens=2048,
)
wavfile.write("ja_good_morning.wav", sr, wavs[0])

# 生成韩文语音
wavs, sr = ov_model.generate_custom_voice(
    text="안녕하세요",
    speaker="vivian",
    language="korean",
    instruct="用友好亲切的语气说话。",
    non_streaming_mode=True,
    max_new_tokens=2048,
)
wavfile.write("ko_good_morning.wav", sr, wavs[0])

# 生成德文语音
wavs, sr = ov_model.generate_custom_voice(
    text="Guten Morgen",
    speaker="vivian",
    language="german",
    instruct="用友好亲切的语气说话。",
    non_streaming_mode=True,
    max_new_tokens=2048,
)
wavfile.write("de_good_morning.wav", sr, wavs[0])
    """)
    print()

    print("=" * 80)
    print("💡 学习要点")
    print("=" * 80)
    print()
    print("1. 英文：Good morning")
    print("   - 注意 'morning' 的 'r' 不卷舌")
    print("   - 语调上扬，表示问候")
    print()
    print("2. 日文：おはようございます")
    print("   - 正式场合使用，非正式可说 おはよう")
    print("   - 注意长音 おはよ- う")
    print()
    print("3. 韩文：안녕하세요")
    print("   - 通用的问候语，可用于早上、下午、晚上")
    print("   - 注意收音 '하세요' 的发音")
    print()
    print("4. 德文：Guten Morgen")
    print("   - Guten 的 'G' 发音像 'K'")
    print("   - Morgen 的 'r' 在词尾发轻声")
    print()

    print("=" * 80)
    print("📚 完整工作流")
    print("=" * 80)
    print()
    print("方法一：一键完成（推荐）")
    print("  python scripts/complete_workflow.py --text '早上好' --output-dir ./output")
    print()
    print("方法二：分步执行")
    print("  1. python scripts/download_models.py --model-dir ./models")
    print("  2. python scripts/workflow_lite.py --text '早上好' --model-dir ./models")
    print("  3. python scripts/tts.py --text 'Good morning' --language english --output ./output/en.wav")
    print()

    # 输出 JSON 格式结果
    output = {
        "source": "早上好",
        "translations": translations,
        "code_example": {
            "translation": "使用 HunyuanMTTranslator 类",
            "tts": "使用 OVQwen3TTSModel.generate_custom_voice()"
        }
    }

    print("=" * 80)
    print("📊 JSON 输出")
    print("=" * 80)
    print()
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    show_translations()
