# Multilingual Translate & TTS Skill
适配 OpenClaw / QwenPaw 平台的多语言翻译+语音合成学习助手 Skill，基于**混元HY-MT-7B翻译模型**+**通义千问Qwen3-TTS语音合成模型**+**OpenVINO端侧加速引擎**开发，专为Intel AI PC打造，实现中文到英/日/韩/德的一键翻译与自然语音生成，助力外语发音学习。

## 核心功能
- 📝 中文文本一键翻译为**英语、日语、韩语、德语**四种语言
- 🔊 为每种翻译结果生成自然流畅的对应语言语音
- 💻 基于Intel AI PC端侧推理，无需云端依赖，低延迟高隐私
- 🧰 适配QwenPaw/OpenClaw Skill标准，可直接导入、调度、调用
- 🎙 支持自定义说话人、语音语气，发音贴合母语特征

## 适配平台
- OpenClaw / QwenPaw 创空间（魔搭ModelScope）
- Intel AI PC（x86架构，支持OpenVINO加速）
- 兼容Windows/Linux系统

## 模型依赖
- 翻译模型：Hunyuan-MT-7B-int4-ov（OpenVINO量化版）
- 语音合成模型：Qwen3-TTS-CustomVoice-0.6B-fp16-ov（OpenVINO量化版）
- 模型自动从ModelScope下载，首次运行自动缓存

## CoPaw/OpenClaw 调用方式
### 1. 技能导入
进入QwenPaw创空间 → **Skills** → **Import Skill** → 粘贴本Skill的GitHub仓库链接，自动完成依赖安装与模型加载。
### 2. 自然语言调用
在QwenPaw对话界面直接输入中文文本需求，示例：
> 把“坚持学习，每天进步一点点”翻译成英日韩德并生成语音
