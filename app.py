#!/usr/bin/env python3
"""
transpdf - PDF 翻译工具主入口
基于 PDFMathTranslate 二次开发的简化 PDF 翻译工具
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# 添加 transpdf 目录到 Python 路径
transpdf_dir = root_dir / "transpdf"
if str(transpdf_dir) not in sys.path:
    sys.path.insert(0, str(transpdf_dir))

# 加载环境变量
from dotenv import load_dotenv
env_file = root_dir / ".env"
if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ 已加载环境变量：{env_file}")

# 初始化日志系统
from transpdf.logger import get_logger, log_startup
logger = get_logger()
log_startup()

logger.info("=" * 60)
logger.info("transpdf - PDF 翻译工具")
logger.info("=" * 60)

# 验证配置
from transpdf.config_manager import ConfigManager
config = ConfigManager()

logger.info(f"配置文件：{config._config_path}")
logger.info("配置加载成功")

# 启动 GUI
logger.info("启动 GUI...")
from transpdf.gui import demo

if __name__ == "__main__":
    logger.info("打开浏览器...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        debug=True,
        inbrowser=True,
    )
