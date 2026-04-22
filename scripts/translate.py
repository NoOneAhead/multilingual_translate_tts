#!/usr/bin/env python3
"""
多语言翻译脚本
使用 Hunyuan-MT-7B 模型将中文翻译成英、日、韩、德等多种语言
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict


class HunyuanMTTranslator:
    """一键翻译中文到多语言"""

    LANGUAGE_MAP = {
        "en": "英文",
        "ja": "日文",
        "ko": "韩文",
        "de": "德文",
    }

    def __init__(self, model_id: str, device: str = "CPU"):
        self.model_id = model_id
        self.device = device
        self.model = None
        self.tokenizer = None

    def _load_model(self):
        """加载模型"""
        if self.model is not None:
            return

        print(f"[正在加载翻译模型]...")

        try:
            from optimum.intel import OVModelForCausalLM
            from transformers import AutoTokenizer

            self.model = OVModelForCausalLM.from_pretrained(
                Path(self.model_id),
                export=False,
                device=self.device
            )
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            print("✅ 翻译模型加载完成\n")
        except Exception as e:
            raise Exception(f"模型加载失败: {str(e)}")

    def _build_prompt(self, text: str, tgt_lang: str) -> str:
        """构建翻译 prompt"""
        tgt_name = self.LANGUAGE_MAP[tgt_lang]
        return (
            f"<|im_start|>user\n"
            f"将下文翻译成{tgt_name}：\n"
            f"{text}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

    def _clean_output(self, text: str) -> str:
        """清理输出中的特殊 token 和多余内容"""
        text = text.replace("<|im_end|>", "").replace("<|im_start|>", "")
        text = text.replace("user", "").replace("assistant", "")

        if "将下文翻译成" in text:
            return ""

        sentences = text.split('\n\n')
        if sentences:
            result = sentences[0].strip()
            result = re.sub(r'<\|.*?\|>', '', result)
            return result.strip()

        return text.strip()

    def translate(
        self,
        text: str,
        tgt_lang: str = "en",
        max_tokens: int = 256
    ) -> str:
        """翻译单条文本，返回翻译结果"""
        self._load_model()

        prompt = self._build_prompt(text, tgt_lang)

        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.3,
            top_p=0.9,
            do_sample=False,
        )

        full_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        translation = full_output.replace(prompt, "").strip()
        translation = self._clean_output(translation)

        return translation if translation else "[翻译失败]"

    def translate_to_all(
        self,
        text: str,
        max_tokens: int = 256,
    ) -> Dict[str, str]:
        """一键翻译成所有语言"""
        results = {}

        for lang_code, lang_name in self.LANGUAGE_MAP.items():
            try:
                translation = self.translate(text, lang_code, max_tokens)
                results[lang_code] = translation
            except Exception as e:
                results[lang_code] = f"[错误: {str(e)[:30]}]"

        return results


def main():
    parser = argparse.ArgumentParser(description="多语言文本翻译")
    parser.add_argument("--text", type=str, required=True, help="要翻译的中文文本")
    parser.add_argument(
        "--target-lang",
        type=str,
        default="all",
        choices=["all", "en", "ja", "ko", "de"],
        help="目标语言 (默认: all)"
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default="./models/Hunyuan-MT-7B-int4-ov",
        help="翻译模型目录"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="CPU",
        choices=["CPU", "AUTO"],
        help="推理设备"
    )
    args = parser.parse_args()

    translator = HunyuanMTTranslator(args.model_dir, args.device)

    if args.target_lang == "all":
        results = translator.translate_to_all(args.text)
    else:
        results = {args.target_lang: translator.translate(args.text, args.target_lang)}

    output = {
        "status": "success",
        "source_text": args.text,
        "translations": results
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
