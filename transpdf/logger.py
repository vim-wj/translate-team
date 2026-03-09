"""
日志系统 - 为 transpdf 提供完整的日志记录功能
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def get_config_manager():
    """获取配置管理器（支持模块导入和直接运行）"""
    try:
        # 尝试相对导入（模块方式）
        from .config_manager import config_manager
        return config_manager
    except ImportError:
        # 尝试绝对导入（直接运行方式）
        try:
            from config_manager import config_manager
            return config_manager
        except ImportError:
            # 手动添加路径
            transpdf_dir = Path(__file__).parent
            if str(transpdf_dir) not in sys.path:
                sys.path.insert(0, str(transpdf_dir))
            from config_manager import config_manager
            return config_manager


class TransPDFLogger:
    """TransPDF 专用日志类"""
    
    _instance = None
    _logger = None
    _config_manager = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self.setup_logger()
    
    def setup_logger(self, log_file: Optional[Path] = None, level: Optional[str] = None):
        """
        设置日志器
        
        Args:
            log_file: 日志文件路径，默认从配置读取
            level: 日志级别，默认从配置读取
        """
        # 获取配置管理器
        self._config_manager = get_config_manager()
        
        # 获取配置
        if log_file is None:
            log_file = self._config_manager.get_log_file_path()
        if level is None:
            level = self._config_manager.get_log_level()
        
        # 确保日志目录存在
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建 logger
        self._logger = logging.getLogger("transpdf")
        self._logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        
        # 清除已有的 handlers
        self._logger.handlers.clear()
        
        # 创建 formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 文件 handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        
        # 控制台 handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        self._log_startup_info()
    
    def _log_startup_info(self):
        """记录启动信息"""
        self.info("=" * 60)
        self.info("TransPDF 启动")
        self.info("=" * 60)
        self.info(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.info(f"日志级别：{self._logger.level}")
        self.info(f"日志文件：{self._config_manager.get_log_file_path()}")
        self.info("=" * 60)
    
    def debug(self, msg: str, *args, **kwargs):
        """记录 DEBUG 级别日志"""
        if self._logger:
            self._logger.debug(msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        """记录 INFO 级别日志"""
        if self._logger:
            self._logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        """记录 WARNING 级别日志"""
        if self._logger:
            self._logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        """记录 ERROR 级别日志"""
        if self._logger:
            self._logger.error(msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        """记录 CRITICAL 级别日志"""
        if self._logger:
            self._logger.critical(msg, *args, **kwargs)
    
    def exception(self, msg: str, *args, **kwargs):
        """记录异常日志"""
        if self._logger:
            self._logger.exception(msg, *args, **kwargs)
    
    def log_translation_start(self, source_lang: str, target_lang: str, provider: str):
        """记录翻译开始"""
        self.info(
            f"开始翻译 | 源语言：{source_lang} | 目标语言：{target_lang} | 服务商：{provider}"
        )
    
    def log_translation_end(self, source_lang: str, target_lang: str, provider: str, 
                           char_count: int, duration: float):
        """记录翻译结束"""
        self.info(
            f"翻译完成 | 源语言：{source_lang} | 目标语言：{target_lang} | "
            f"服务商：{provider} | 字符数：{char_count} | 耗时：{duration:.2f}s"
        )
    
    def log_translation_error(self, error: str, provider: str, retry_count: int = 0):
        """记录翻译错误"""
        if retry_count > 0:
            self.warning(
                f"翻译错误 (第{retry_count}次重试) | 服务商：{provider} | 错误：{error}"
            )
        else:
            self.error(f"翻译错误 | 服务商：{provider} | 错误：{error}")
    
    def log_pdf_operation(self, operation: str, pdf_path: str, status: str = "success"):
        """记录 PDF 操作"""
        if status == "success":
            self.info(f"PDF 操作 | 类型：{operation} | 文件：{pdf_path} | 状态：成功")
        else:
            self.error(f"PDF 操作 | 类型：{operation} | 文件：{pdf_path} | 状态：失败 - {status}")
    
    def log_cache_operation(self, operation: str, key: str, hit: bool = False):
        """记录缓存操作"""
        if hit:
            self.debug(f"缓存命中 | 操作：{operation} | 键：{key[:50]}...")
        else:
            self.debug(f"缓存未命中 | 操作：{operation} | 键：{key[:50]}...")


# 全局日志器实例
logger = TransPDFLogger()


def get_logger() -> logging.Logger:
    """获取日志器实例"""
    return logger._logger


def log_startup():
    """记录启动日志"""
    logger.info("=" * 60)
    logger.info("TransPDF 启动")
    logger.info("=" * 60)
    logger.info(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"日志级别：{logger._config_manager.get_log_level()}")
    logger.info(f"日志文件：{logger._config_manager.get_log_file_path()}")
    
    # 记录配置的服务商
    providers = logger._config_manager.get_providers()
    enabled_providers = logger._config_manager.get_enabled_providers()
    logger.info(f"配置的服务商：{len(providers)}个")
    for p in providers:
        status = "已启用" if p.get("enabled") else "已禁用"
        logger.info(f"  - {p.get('name')}: {p.get('model')} ({status})")
    logger.info(f"可用的服务商：{len(enabled_providers)}个")
    logger.info("=" * 60)


def log_translation_request(text: str, source_lang: str, target_lang: str, provider: str):
    """记录翻译请求"""
    logger.debug(f"翻译请求 | 源：{source_lang} | 目标：{target_lang} | 服务商：{provider}")
    logger.debug(f"原文：{text[:100]}{'...' if len(text) > 100 else ''}")


def log_translation_response(translated: str, provider: str, duration: float):
    """记录翻译响应"""
    logger.debug(f"翻译响应 | 服务商：{provider} | 耗时：{duration:.2f}s")
    logger.debug(f"译文：{translated[:100]}{'...' if len(translated) > 100 else ''}")


def log_error(error: Exception, context: str = ""):
    """记录错误"""
    logger.exception(f"错误 | {context}: {error}")


if __name__ == "__main__":
    # 独立运行时使用默认配置
    print("=" * 60)
    print("TransPDF 日志系统测试")
    print("=" * 60)
    
    try:
        # 初始化日志（使用默认配置）
        log_startup()
        
        # 测试各种日志级别
        logger.debug("这是一条 DEBUG 日志")
        logger.info("这是一条 INFO 日志")
        logger.warning("这是一条 WARNING 日志")
        logger.error("这是一条 ERROR 日志")
        
        print("\n✓ 日志系统测试完成")
        print(f"日志文件位置：{logger._config_manager.get_log_file_path()}")
        
    except Exception as e:
        print(f"\n✗ 测试失败：{e}")
        import traceback
        traceback.print_exc()
