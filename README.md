# transpdf - PDF 翻译工具

基于 PDFMathTranslate 二次开发的简化 PDF 翻译工具，支持多种大语言模型 API，提供友好的图形界面。

## 📖 项目介绍

transpdf 是一个专注于 PDF 文档翻译的轻量级工具，具有以下特点：

- 🎯 **简洁高效**：去除复杂功能，专注于核心翻译需求
- 🌐 **多模型支持**：支持 DeepSeek、千问、豆包、MiniMax、Kimi、OpenAI 等多种模型
- 🖥️ **图形界面**：基于 Gradio 构建，操作简单直观
- 🔒 **本地运行**：所有处理在本地完成，保护文档隐私
- 📊 **格式保留**：尽可能保持原文档的格式和排版

## 🚀 安装说明

### 系统要求

- Python 3.10 - 3.12
- Windows / Linux / Mac OS

### 快速开始

#### Linux / Mac

```bash
# 1. 进入项目目录
cd /home/admin/code/translate-team

# 2. 运行启动脚本
chmod +x start.sh
./start.sh

# 3. 首次运行会提示配置 API Key
# 编辑 .env 文件，填入至少一个模型的 API Key

# 4. 再次运行启动脚本
./start.sh
```

#### Windows

```batch
# 1. 进入项目目录
cd C:\path\to\translate-team

# 2. 双击运行 start.bat
# 或命令行运行：
start.bat

# 3. 首次运行会提示配置 API Key
# 编辑 .env 文件，填入至少一个模型的 API Key

# 4. 再次运行启动脚本
start.bat
```

### 手动安装

```bash
# 1. 创建虚拟环境
python3 -m venv .venv

# 2. 激活虚拟环境
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 API Key

# 5. 启动应用
python app.py
```

## 📖 使用说明

1. **启动应用**：运行启动脚本后，在浏览器中访问 `http://localhost:7860`

2. **上传 PDF**：在界面中拖拽或选择要翻译的 PDF 文件

3. **选择模型**：从下拉菜单中选择要使用的翻译模型

4. **设置参数**：
   - 源语言：原文档的语言
   - 目标语言：翻译后的语言
   - 翻译模式：全文翻译 / 指定页面

5. **开始翻译**：点击"开始翻译"按钮，等待处理完成

6. **下载结果**：翻译完成后下载翻译后的 PDF 文件

## ⚙️ 配置说明

### 环境变量配置

复制 `.env.example` 为 `.env`，然后根据使用的模型填写对应的 API Key：

```bash
# 至少配置一个模型的 API Key

# DeepSeek
DEEPSEEK_API_KEY=sk-your-key-here
DEEPSEEK_MODEL=deepseek-chat

# 千问 (阿里云)
DASHSCOPE_API_KEY=sk-your-key-here

# 豆包 (字节跳动)
DOUBAO_API_KEY=your-key-here

# MiniMax
MINIMAX_API_KEY=your-key-here

# Kimi (月之暗面)
KIMI_API_KEY=your-key-here

# OpenAI
OPENAI_API_KEY=sk-your-key-here
```

### 配置项说明

| 环境变量 | 说明 | 是否必需 |
|---------|------|---------|
| DEEPSEEK_API_KEY | DeepSeek API 密钥 | 可选 |
| DEEPSEEK_MODEL | DeepSeek 模型名称 | 可选 |
| DASHSCOPE_API_KEY | 阿里云千问 API 密钥 | 可选 |
| DOUBAO_API_KEY | 字节豆包 API 密钥 | 可选 |
| MINIMAX_API_KEY | MiniMax API 密钥 | 可选 |
| KIMI_API_KEY | Kimi API 密钥 | 可选 |
| OPENAI_API_KEY | OpenAI API 密钥 | 可选 |

**注意**：至少需要配置一个模型的 API Key 才能使用。

## 🌟 支持的模型厂商

| 厂商 | 模型 | 环境变量 | 特点 |
|-----|------|---------|------|
| **DeepSeek** | deepseek-chat | DEEPSEEK_API_KEY | 性价比高，翻译质量好 |
| **阿里云** | qwen-turbo/plus | DASHSCOPE_API_KEY | 国内访问快，支持长文本 |
| **字节跳动** | doubao-pro | DOUBAO_API_KEY | 多语言支持好 |
| **MiniMax** | abab6 | MINIMAX_API_KEY | 中文理解能力强 |
| **Kimi** | moonshot-v1 | KIMI_API_KEY | 长上下文处理优秀 |
| **OpenAI** | gpt-3.5/4-turbo | OPENAI_API_KEY | 翻译质量稳定 |

## 📁 项目结构

```
translate-team/
├── start.sh          # Linux/Mac 启动脚本
├── start.bat         # Windows 启动脚本
├── requirements.txt  # Python 依赖列表
├── .env.example      # 环境变量模板
├── .env              # 实际配置（需自行创建）
├── app.py            # 主应用程序
├── logs/             # 日志目录
└── README.md         # 项目文档
```

## 🔧 故障排除

### 常见问题

1. **Python 版本错误**
   ```
   错误：Python 版本需要在 3.10-3.12 之间
   解决：安装 Python 3.10/3.11/3.12
   ```

2. **API Key 未配置**
   ```
   警告：未检测到任何已配置的 API Key
   解决：编辑 .env 文件，至少配置一个 API Key
   ```

3. **依赖安装失败**
   ```bash
   # 尝试升级 pip
   pip install --upgrade pip
   # 重新安装依赖
   pip install -r requirements.txt
   ```

4. **端口被占用**
   ```
   错误：Address already in use
   解决：关闭占用 7860 端口的程序，或修改 app.py 中的端口
   ```

## 📝 日志查看

运行日志保存在 `logs/` 目录下：

```bash
# 查看最新日志
tail -f logs/app.log

# 查看历史日志
ls -la logs/
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目基于 PDFMathTranslate 二次开发，遵循原项目许可证。

## 📞 支持

如有问题，请提交 Issue 或联系开发团队。
