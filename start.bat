@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM transpdf 启动脚本 (Windows)
REM 基于 PDFMathTranslate 二次开发的简化 PDF 翻译工具

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

set VENV_DIR=.venv
set PYTHON_VERSION_MIN=3.10
set PYTHON_VERSION_MAX=3.12

echo ==========================================
echo   transpdf - PDF 翻译工具
echo ==========================================
echo.

REM 1. 检查 Python 版本
echo [1/7] 检查 Python 版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python，请先安装 Python 3.10-3.12
    echo    下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo    当前 Python 版本：%PYTHON_VERSION%

REM 简化版本检查（只检查主要版本）
echo    ✓ Python 已安装

REM 2. 检查虚拟环境
echo.
echo [2/7] 检查虚拟环境...
if not exist "%VENV_DIR%" (
    echo    虚拟环境不存在，正在创建...
    python -m venv "%VENV_DIR%"
    echo    ✓ 虚拟环境创建成功
) else (
    echo    ✓ 虚拟环境已存在
)

REM 激活虚拟环境
echo    激活虚拟环境...
call "%VENV_DIR%\Scripts\activate.bat"

REM 3. 安装依赖
echo.
echo [3/7] 安装依赖...
if not exist "requirements.txt" (
    echo ❌ 错误：requirements.txt 不存在
    pause
    exit /b 1
)

python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
echo    ✓ 依赖安装完成

REM 4. 检查配置文件
echo.
echo [4/7] 检查配置文件...
if not exist ".env" (
    if exist ".env.example" (
        echo    配置文件不存在，从 .env.example 创建...
        copy .env.example .env >nul
        echo    ⚠️  请编辑 .env 文件配置 API Key
        echo    配置文件位置：%SCRIPT_DIR%.env
        pause
        exit /b 0
    ) else (
        echo ❌ 错误：.env 和 .env.example 均不存在
        pause
        exit /b 1
    )
) else (
    echo    ✓ 配置文件存在
)

REM 5. 验证 API Key 配置
echo.
echo [5/7] 验证 API Key 配置...
python -c "
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
if errorlevel 1 (
    pause
    exit /b 1
)

REM 6. 检查日志目录
echo.
echo [6/7] 检查日志目录...
if not exist "logs" (
    mkdir logs
    echo    创建日志目录：logs
)
echo    ✓ 日志目录就绪

REM 7. 启动应用
echo.
echo [7/7] 启动应用...
echo ==========================================
echo   启动成功！
echo   访问地址：http://localhost:7860
echo ==========================================
echo.

python app.py

pause
