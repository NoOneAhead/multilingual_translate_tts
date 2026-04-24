#!/usr/bin/env python3
"""
语音合成脚本
使用 Qwen3-TTS 模型生成指定语言的语音
"""

import argparse
import json
import sys
from pathlib import Path
import time


class TTSGenerator:
    """文本转语音生成器"""

    def __init__(self, model_id: str, device: str = "CPU"):
        self.model_id = model_id
        self.device = device
        self.model = None

    def _load_model(self):
        """加载模型"""
        if self.model is not None:
            return

        print(f"[正在加载语音合成模型]...")

        try:
            from qwen_3_tts_helper import OVQwen3TTSModel

            self.model = OVQwen3TTSModel.from_pretrained(
                model_dir=self.model_id,
                device=self.device,
            )
            print("[OK] 语音合成模型加载完成\n")
        except ImportError:
            raise Exception("Qwen3-TTS 未安装，请先运行: pip install -e Qwen3-TTS")
        except Exception as e:
            raise Exception(f"模型加载失败: {str(e)}")

    def generate_speech(
        self,
        text: str,
        language: str = "english",
        speaker: str = "vivian",
        instruct: str = "",
        output_file: str = None,
        max_new_tokens: int = 2048
    ):
        """生成语音"""
        self._load_model()

        if output_file is None:
            output_file = f"{language}_speech.wav"

        start_time = time.time()

        try:
            wavs, sr = self.model.generate_custom_voice(
                text=text,
                speaker=speaker,
                language=language,
                instruct=instruct if instruct else None,
                non_streaming_mode=True,
                max_new_tokens=max_new_tokens,
            )

            inference_time = time.time() - start_time

            if wavs is None or len(wavs) == 0:
                return {
                    "status": "error",
                    "error": "语音生成失败，返回空结果"
                }

            # 保存音频文件
            from scipy.io import wavfile
            import numpy as np

            # 确保音频数据在有效范围内
            audio_data = np.array(wavs[0])
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)

            # 归一化到 [-1, 1]
            max_val = np.max(np.abs(audio_data))
            if max_val > 0:
                audio_data = audio_data / max_val

            # 转换为 16-bit PCM
            audio_data = (audio_data * 32767).astype(np.int16)

            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            wavfile.write(output_path, sr, audio_data)

            audio_duration = len(wavs[0]) / sr

            return {
                "status": "success",
                "output_file": str(output_path.absolute()),
                "language": language,
                "speaker": speaker,
                "sample_rate": sr,
                "duration": audio_duration,
                "inference_time": inference_time,
                "rtf": inference_time / audio_duration if audio_duration > 0 else 0
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


def main():
    parser = argparse.ArgumentParser(description="文本转语音合成")
    parser.add_argument("--text", type=str, required=True, help="要转换为语音的文本")
    parser.add_argument(
        "--language",
        type=str,
        required=True,
        choices=["auto", "chinese", "english", "french", "german", "italian", "japanese", "korean", "portuguese", "russian", "spanish"],
        help="目标语言"
    )
    parser.add_argument(
        "--speaker",
        type=str,
        default="vivian",
        help="说话人名称 (默认: vivian)"
    )
    parser.add_argument(
        "--instruct",
        type=str,
        default="",
        help="语气指令 (如: 用友好亲切的语气说话)"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="输出音频文件路径"
    )
    parser.add_argument(
        "--model-dir",
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
    args = parser.parse_args()

    generator = TTSGenerator(args.model_dir, args.device)

    result = generator.generate_speech(
        text=args.text,
        language=args.language,
        speaker=args.speaker,
        instruct=args.instruct,
        output_file=args.output
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
