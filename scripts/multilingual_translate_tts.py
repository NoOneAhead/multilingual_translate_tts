"""
OpenClaw / CoPaw Skill
多语言翻译 + 语音合成学习助手
基于 HY-MT-7B + Qwen3-TTS + OpenVINO
"""

import time
import numpy as np
from typing import Dict, Any
from modelscope import snapshot_download
from pathlib import Path

# 翻译模型
from mt_translator import HunyuanMTTranslator

# TTS 模型
from qwen_3_tts_helper import OVQwen3TTSModel

# ==============================================
# Skill 元信息（CoPaw 必须）
# ==============================================
SKILL_NAME = "multilingual_translate_tts"
SKILL_DESCRIPTION = "输入中文，自动翻译成英、日、韩、德四种语言，并生成对应语音，用于外语发音学习"
SKILL_AUTHOR = "NoOneAhead"
SKILL_VERSION = "1.0.0"

# ==============================================
# 全局模型加载（仅第一次）
# ==============================================
_translator = None
_tts_model = None

def get_translator():
    global _translator
    if _translator is None:
        _translator = HunyuanMTTranslator(model_id="Hunyuan-MT-7B-int4-ov", device="CPU")
    return _translator

def get_tts_model():
    global _tts_model
    if _tts_model is None:
        model_dir = Path("Qwen3-TTS-CustomVoice-0.6B-fp16-ov")
        if not model_dir.exists():
            snapshot_download("snake7gun/Qwen3-TTS-CustomVoice-0.6B-fp16-ov", local_dir=str(model_dir))
        _tts_model = OVQwen3TTSModel.from_pretrained(model_dir=model_dir, device="CPU")
    return _tts_model

# ==============================================
# Skill 主入口（CoPaw 标准调用格式）
# ==============================================
def run(input_text: str, **kwargs) -> Dict[str, Any]:
    """
    CoPaw Skill 主函数
    :param input_text: 中文输入
    :return: 翻译结果 + 语音数据
    """
    try:
        print("[Skill] 开始运行多语言翻译+语音合成...")
        translator = get_translator()
        tts_model = get_tts_model()

        # 1. 翻译
        trans_result = translator.translate_to_all(input_text)

        # 2. 语音合成
        speeches = {}
        lang_map = {
            "en": "english",
            "ja": "japanese",
            "ko": "korean",
            "de": "german"
        }

        for lang_code, text in trans_result.items():
            if text and text != "[翻译失败]":
                wavs, sr = tts_model.generate_custom_voice(
                    text=text,
                    speaker="vivian",
                    language=lang_map[lang_code],
                    instruct="用友好亲切的语气说话。",
                    non_streaming_mode=True
                )
                speeches[lang_code] = {
                    "audio": wavs[0].tolist(),
                    "sample_rate": sr
                }

        # 3. 返回标准格式
        return {
            "status": "success",
            "original": input_text,
            "translations": trans_result,
            "speeches": speeches
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
