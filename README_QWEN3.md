# Qwen3-TTS 本地部署与集成指南

本项目已成功集成 Qwen3-TTS (0.6B 版本) 作为本地 Text-to-Speech 引擎，支持自然语言指令驱动的情绪化合成。

## 1. 环境准备

推荐使用 Anaconda 或 Miniconda 管理 Python 环境。Qwen3-TTS 需要 Python 3.10+ 环境。

### 创建虚拟环境
```bash
conda create -n qwen3_tts_env python=3.12 -y
conda activate qwen3_tts_env
```

### 安装依赖
```bash
# 安装 PyTorch (针对 RTX 4060 等支持 CUDA 12.1 的显卡)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 安装服务端核心依赖
pip install modelscope fastapi uvicorn soundfile pydantic

# 安装 Qwen3-TTS 运行库 (假设已从 ModelScope 获取源代码)
# 如果是直接通过 git/modelscope 使用，请确保路径正确
pip install qwen-tts
```

## 2. 模型下载与启动

服务端已配置为通过 `modelscope` 自动下载并缓存模型。

### 启动服务端
进入项目目录下的 `tts/qwen3tts_server/`：
```bash
cd tts/qwen3tts_server
python server.py
```
*   **首次启动**：会从 ModelScope 下载约 1.2GB 的模型文件，请保持网络畅通。
*   **显存要求**：RTX 4060 (8GB) 建议开启 `bfloat16`（代码中已默认开启）。

## 3. Fay 平台配置

### system.conf 配置
确保 `system.conf` 中的以下项已正确配置：
```ini
[key]
# tts类型选择 qwen3
tts_module = qwen3

# Qwen3-TTS 本地服务端地址 (默认 8000 端口)
qwen3_tts_url = http://127.0.0.1:8000/tts
```

### config.json 配置
在 UI 面板或直接修改 `config.json`：
*   `voice`: 选择 `Qwen3-灵动女声` 或 `Qwen3-稳重男声`。
*   `playSound`: 设置为 `true` 以在本地扬声器播放。

## 4. 使用特性

Qwen3-TTS 不同于传统的 TTS，它支持通过 **自然语言指令 (Instruct)** 来控制语气。本项目已自动完成以下情绪映射：

| Fay 情绪状态 | Qwen3 语气指令 |
| :--- | :--- |
| **平静 (calm)** | 用平稳、自然、淡定的语气说话 |
| **生气 (angry)** | 用非常生气、严厉的语气说话 |
| **开朗 (cheerful)** | 用开朗、活泼、阳光的语气说话 |
| **温柔 (lyrical)** | 用温柔、感性、充满感情的语气说话 |
| **专业 (assistant)** | 用专业、有礼貌的助手语气说话 |

## 5. 常见问题排查

1.  **Read timed out (120s)**：首次合成时模型需要加载到显存（冷启动），通常耗时 30-50s。后续合成通常在 1-3s 内。
2.  **Unsupported speakers**：请确保 `voice` 选择的是 `Qwen3-灵动女声` 或 `Qwen3-稳重男声`，代码会自动将其映射为模型支持的 `vivian` 或 `eric`。
3.  **端口占用 (WinError 10048)**：如果重启 Fay 提示 10001 端口占用，请在任务管理器中杀掉残留的 python.exe 进程。
