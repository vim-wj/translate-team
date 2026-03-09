#!/bin/bash

# transpdf 启动脚本 (Linux/Mac)
# 基于 PDFMathTranslate 二次开发的简化 PDF 翻译工具

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"

echo "=========================================="
echo "  transpdf - PDF 翻译工具"
echo "=========================================="
echo ""

# 1. 检查 Python 版本并创建虚拟环境
echo "[1/7] 检查 Python 版本..."

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

echo "   当前 Python 版本：$PYTHON_VERSION"

# 检查版本范围 (3.10-3.12)
PYTHON_OK=true
if [[ "$PYTHON_MAJOR" -lt 3 ]] || \
   [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -lt 10 ]] || \
   [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -gt 12 ]] || \
   [[ "$PYTHON_MAJOR" -gt 3 ]]; then
    echo "   ⚠️  Python 版本不在 3.10-3.12 范围内"
    PYTHON_OK=false
fi

# 如果 Python 版本不符合，使用 uv 创建虚拟环境
if [ "$PYTHON_OK" = false ]; then
    echo ""
    echo "   检测到 Python 版本不符合要求"
    
    # 检查 uv 是否安装
    if command -v uv &> /dev/null; then
        echo "   使用 uv 创建 Python 3.11 虚拟环境..."
        uv venv "$VENV_DIR" --python 3.11
        echo "   ✓ 虚拟环境创建成功 (Python 3.11)"
    else
        echo "   ⚠️  未找到 uv 工具，尝试使用系统 Python 创建..."
        echo "   提示：安装 uv 可获得更好的体验：curl -LsSf https://astral.sh/uv/install.sh | sh"
        python3 -m venv "$VENV_DIR"
        echo "   ✓ 虚拟环境创建成功"
    fi
else
    echo "   ✓ Python 版本符合要求"
    
    # 检查虚拟环境
    echo ""
    echo "[2/7] 检查虚拟环境..."
    if [ ! -d "$VENV_DIR" ]; then
        echo "   虚拟环境不存在，正在创建..."
        python3 -m venv "$VENV_DIR"
        echo "   ✓ 虚拟环境创建成功"
    else
        echo "   ✓ 虚拟环境已存在"
    fi
fi

# 激活虚拟环境
echo ""
echo "   激活虚拟环境..."
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
    echo "   ✓ 虚拟环境已激活 ($(python --version))"
else
    echo "   ❌ 错误：虚拟环境激活脚本不存在"
    exit 1
fi

# 3. 安装依赖
echo ""
echo "[3/7] 安装依赖..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误：requirements.txt 不存在"
    exit 1
fi

echo "   升级 pip..."
pip install --upgrade pip -q

echo "   安装依赖包..."
pip install -r requirements.txt -q
echo "   ✓ 依赖安装完成"

# 4. 检查配置文件
echo ""
echo "[4/7] 检查配置文件..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "   配置文件不存在，从 .env.example 创建..."
        cp .env.example .env
        echo "   ⚠️  请编辑 .env 文件配置 API Key"
        echo "   配置文件位置：$SCRIPT_DIR/.env"
        exit 0
    else
        echo "❌ 错误：.env 和 .env.example 均不存在"
        exit 1
    fi
else
    echo "   ✓ 配置文件存在"
fi

# 5. 验证 API Key 配置
echo ""
echo "[5/7] 验证 API Key 配置..."
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

api_keys = [
    ('DEEPSEEK_API_KEY', 'DeepSeek'),
    ('DASHSCOPE_API_KEY', '千问'),
    ('DOUBAO_API_KEY', '豆包'),
    ('MINIMAX_API_KEY', 'MiniMax'),
    ('KIMI_API_KEY', 'Kimi'),
    ('OPENAI_API_KEY', 'OpenAI')
]

configured = False
for key, name in api_keys:
    value = os.getenv(key)
    if value and value != 'sk-xxx' and value != 'xxx':
        print(f'   ✓ {name} API Key 已配置')
        configured = True

if not configured:
    print('   ⚠️  警告：未检测到任何已配置的 API Key')
    print('   请编辑 .env 文件至少配置一个 API Key')
    exit(1)
"
if [ $? -ne 0 ]; then
    exit 1
fi

# 6. 检查日志目录
echo ""
echo "[6/7] 检查日志目录..."
LOG_DIR="logs"
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
    echo "   创建日志目录：$LOG_DIR"
fi
echo "   ✓ 日志目录就绪"

# 7. 启动应用
echo ""
echo "[7/7] 启动应用..."
echo "=========================================="
echo "  启动成功！"
echo "  访问地址：http://localhost:7860"
echo "  虚拟环境：$VENV_DIR"
echo "=========================================="
echo ""

python3 app.py
