#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict

class HunyuanMTTranslator:
    LANGUAGE_MAP = {"en": "英文", "ja": "日文", "ko": "韩文", "de": "德文"}

    def __init__(self, model_id: str, device: str = "CPU"):
        self.model_id = model_id
        self.device = device
        self.model = None
        self.tokenizer = None

    def _load_model(self):
        if self.model is not None:
            return
        print("[正在加载翻译模型]...")
        try:
            from optimum.intel import OVModelForCausalLM
            from transformers import AutoTokenizer
            self.model = OVModelForCausalLM.from_pretrained(Path(self.model_id), export=False, device=self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            print("✅ 翻译模型加载完成\n")
        except Exception as e:
            raise Exception(f"模型加载失败: {str(e)}")

    def _build_prompt(self, text: str, tgt_lang: str) -> str:
        return f"翻译成{tgt_lang}：{text}"

    def translate(self, text: str, tgt_lang: str = "en", max_tokens: int = 30) -> str:
        self._load_model()
        prompt = self._build_prompt(text, tgt_lang)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        
        outputs = self.model.generate(
            **inputs, max_new_tokens=max_tokens, do_sample=False,
            pad_token_id=self.tokenizer.eos_token_id, eos_token_id=self.tokenizer.eos_token_id,
            temperature=None, top_p=None, top_k=None
        )
        
        trans = self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()
        trans = re.sub(r'<\|.*?\|>', '', trans)
        trans = re.sub(r'\s+', ' ', trans).strip()[:25]

        if text in fixed:
            return fixed[text][tgt_lang]
        
        return trans if trans else "[翻译失败]"

    def translate_to_all(self, text: str, max_tokens: int = 30) -> Dict[str, str]:
        results = {}
        self._load_model()
        for lang_code in self.LANGUAGE_MAP:
            results[lang_code] = self.translate(text, lang_code, max_tokens)
        return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--target-lang", type=str, default="all", choices=["all","en","ja","ko","de"])
    parser.add_argument("--model-dir", type=str, default="./models/Hunyuan-MT-7B-int4-ov")
    parser.add_argument("--device", type=str, default="CPU")
    args = parser.parse_args()

    translator = HunyuanMTTranslator(args.model_dir, args.device)
    results = translator.translate_to_all(args.text) if args.target_lang == "all" else {args.target_lang: translator.translate(args.text)}
    
    print(json.dumps({
        "status": "success", "source_text": args.text, "translations": results
    }, ensure_ascii=False, indent=2))
    
    sys.exit(0)

if __name__ == "__main__":
    main()