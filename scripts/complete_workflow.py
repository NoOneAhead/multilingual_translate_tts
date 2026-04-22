#!/usr/bin/env python3
"""
一键完成多语言翻译和语音合成
将中文文本翻译成英/日/韩/德四种语言，并为每种语言生成语音文件
"""

import argparse
import json
import sys
from pathlib import Path


def complete_workflow(
    text: str,
    output_dir: str,
    translation_model_dir: str,
    tts_model_dir: str,
    device: str = "CPU",
    speaker: str = "vivian",
    instruct: str = "用友好亲切的语气说话"
):
    """执行完整工作流程：翻译 + 语音合成"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    results = {
        "status": "processing",
        "source_text": text,
        "output_dir": str(output_path.absolute()),
        "translations": {},
        "audio_files": {}
    }

    # 导入翻译模块
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from translate import HunyuanMTTranslator

        print("步骤 1/2: 执行多语言翻译...")
        translator = HunyuanMTTranslator(translation_model_dir, device)
        translations = translator.translate_to_all(text)

        results["translations"] = translations

        language_mapping = {
            "en": ("english", "english"),
            "ja": ("japanese", "japanese"),
            "ko": ("korean", "korean"),
            "de": ("german", "german")
        }

        # 导入语音合成模块
        print("\n步骤 2/2: 生成语音文件...")
        from tts import TTSGenerator

        tts = TTSGenerator(tts_model_dir, device)

        for lang_code, lang_name in language_mapping.items():
            lang_for_tts = lang_name[1]

            if lang_code in translations and not translations[lang_code].startswith("[错误"):
                translated_text = translations[lang_code]
                audio_file = output_path / f"{lang_code}.wav"

                print(f"  生成 {lang_name[0]} 语音...")

                tts_result = tts.generate_speech(
                    text=translated_text,
                    language=lang_for_tts,
                    speaker=speaker,
                    instruct=instruct,
                    output_file=str(audio_file)
                )

                results["audio_files"][lang_code] = {
                    "file": str(audio_file.absolute()),
                    "text": translated_text,
                    "status": tts_result["status"]
                }

                if tts_result["status"] == "error":
                    results["audio_files"][lang_code]["error"] = tts_result.get("error", "未知错误")
            else:
                results["audio_files"][lang_code] = {
                    "status": "skipped",
                    "reason": translations.get(lang_code, "翻译失败")
                }

        results["status"] = "completed"

    except Exception as e:
        results["status"] = "failed"
        results["error"] = str(e)

    return results


def main():
    parser = argparse.ArgumentParser(description="一键完成多语言翻译和语音合成")
    parser.add_argument("--text", type=str, required=True, help="要翻译的中文文本")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="输出目录 (默认: ./output)"
    )
    parser.add_argument(
        "--translation-model-dir",
        type=str,
        default="./models/Hunyuan-MT-7B-int4-ov",
        help="翻译模型目录"
    )
    parser.add_argument(
        "--tts-model-dir",
        type=str,
        default="./models/Qwen3-TTS-CustomVoice-0.6B-fp16-ov",
        help="语音合成模型目录"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="CPU",
        choices=["CPU", "AUTO"],
        help="推理设备"
    )
    parser.add_argument(
        "--speaker",
        type=str,
        default="vivian",
        help="说话人名称"
    )
    parser.add_argument(
        "--instruct",
        type=str,
        default="用友好亲切的语气说话",
        help="语气指令"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("多语言翻译 + 语音合成助手")
    print("=" * 60)
    print(f"\n输入文本: {args.text}")
    print(f"输出目录: {args.output_dir}")
    print()

    results = complete_workflow(
        text=args.text,
        output_dir=args.output_dir,
        translation_model_dir=args.translation_model_dir,
        tts_model_dir=args.tts_model_dir,
        device=args.device,
        speaker=args.speaker,
        instruct=args.instruct
    )

    print("\n" + "=" * 60)
    print("执行完成")
    print("=" * 60)

    if results["status"] == "completed":
        print("\n翻译结果:")
        for lang, text in results["translations"].items():
            print(f"  {lang}: {text}")

        print("\n音频文件:")
        for lang, info in results["audio_files"].items():
            if info["status"] == "success":
                print(f"  {lang}: {info['file']}")
            else:
                print(f"  {lang}: 生成失败 - {info.get('reason', info.get('error', '未知错误'))}")
    else:
        print(f"\n执行失败: {results.get('error', '未知错误')}")

    print("\n" + json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
