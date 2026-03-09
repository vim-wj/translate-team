"""
配置管理器 - 加载和验证 transpdf 配置
"""
import json
import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Any


class ConfigManager:
    """配置管理器类"""
    
    _instance = None
    _config = None
    _config_path = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self.load_config()
    
    @classmethod
    def get_config_path(cls) -> Path:
        """获取配置文件路径"""
        # 配置文件位于项目根目录的 config/config.json
        project_root = Path(__file__).parent.parent
        return project_root / "config" / "config.json"
    
    def load_config(self, config_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径，默认使用项目 config/config.json
            
        Returns:
            配置字典
            
        Raises:
            FileNotFoundError: 配置文件不存在
            json.JSONDecodeError: JSON 格式错误
        """
        if config_path is None:
            config_path = self.get_config_path()
        
        self._config_path = config_path
        
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在：{config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = json.load(f)
        
        return self._config
    
    def get_config(self) -> Dict[str, Any]:
        """获取完整配置"""
        if self._config is None:
            self.load_config()
        return self._config
    
    def get_translation_config(self) -> Dict[str, Any]:
        """获取翻译相关配置"""
        config = self.get_config()
        return config.get("translation", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志相关配置"""
        config = self.get_config()
        return config.get("logging", {})
    
    def get_providers(self) -> List[Dict[str, Any]]:
        """获取所有翻译服务商配置"""
        translation_config = self.get_translation_config()
        return translation_config.get("providers", [])
    
    def get_enabled_providers(self) -> List[Dict[str, Any]]:
        """
        获取已启用的翻译服务商配置
        会自动验证 API Key 是否已配置
        
        Returns:
            已启用且配置有效的服务商列表
        """
        providers = self.get_providers()
        enabled_providers = []
        
        for provider in providers:
            if not provider.get("enabled", False):
                continue
            
            # 验证 API Key 是否已设置
            api_key_env = provider.get("api_key_env")
            if api_key_env and os.environ.get(api_key_env):
                enabled_providers.append(provider)
        
        return enabled_providers
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """
        验证所有服务商的 API Key 配置状态
        
        Returns:
            字典，key 为服务商名称，value 表示是否已配置
        """
        providers = self.get_providers()
        validation_result = {}
        
        for provider in providers:
            name = provider.get("name", "unknown")
            api_key_env = provider.get("api_key_env")
            
            if api_key_env:
                validation_result[name] = bool(os.environ.get(api_key_env))
            else:
                validation_result[name] = False
        
        return validation_result
    
    def select_provider(self) -> Optional[Dict[str, Any]]:
        """
        根据配置的选择模式选择一个翻译服务商
        
        Returns:
            选中的服务商配置，如果没有可用服务则返回 None
            
        Raises:
            RuntimeError: 当没有可用的翻译服务时抛出
        """
        enabled_providers = self.get_enabled_providers()
        
        if not enabled_providers:
            # 获取所有配置的服务商名称用于错误提示
            all_providers = self.get_providers()
            enabled_names = [p.get("name") for p in all_providers if p.get("enabled")]
            
            if not enabled_names:
                raise RuntimeError(
                    "错误：配置文件中没有启用任何翻译服务商。"
                    "请编辑 config/config.json，将至少一个服务商的 enabled 设置为 true。"
                )
            else:
                missing_keys = []
                for name in enabled_names:
                    provider = next((p for p in all_providers if p.get("name") == name), None)
                    if provider:
                        api_key_env = provider.get("api_key_env")
                        if api_key_env and not os.environ.get(api_key_env):
                            missing_keys.append(f"{name} ({api_key_env})")
                
                raise RuntimeError(
                    f"错误：没有可用的翻译服务。以下服务商已启用但未配置 API Key:\n"
                    f"  {', '.join(missing_keys)}\n\n"
                    f"请设置相应的环境变量或启用其他已配置的服务商。"
                )
        
        selection_mode = self.get_translation_config().get("selection_mode", "random")
        
        if selection_mode == "random":
            return random.choice(enabled_providers)
        elif selection_mode == "first":
            return enabled_providers[0]
        else:
            # 默认使用随机模式
            return random.choice(enabled_providers)
    
    def get_provider_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        根据名称获取服务商配置
        
        Args:
            name: 服务商名称
            
        Returns:
            服务商配置，不存在则返回 None
        """
        providers = self.get_providers()
        for provider in providers:
            if provider.get("name") == name:
                return provider
        return None
    
    def get_log_file_path(self) -> Path:
        """获取日志文件路径"""
        logging_config = self.get_logging_config()
        log_file = logging_config.get("file", "logs/transpdf.log")
        
        # 相对于项目根目录
        project_root = Path(__file__).parent.parent
        return project_root / log_file
    
    def get_log_level(self) -> str:
        """获取日志级别"""
        logging_config = self.get_logging_config()
        return logging_config.get("level", "INFO")


# 全局配置管理器实例
config_manager = ConfigManager()


def get_config() -> Dict[str, Any]:
    """获取完整配置"""
    return config_manager.get_config()


def get_translation_config() -> Dict[str, Any]:
    """获取翻译配置"""
    return config_manager.get_translation_config()


def get_logging_config() -> Dict[str, Any]:
    """获取日志配置"""
    return config_manager.get_logging_config()


def select_provider() -> Dict[str, Any]:
    """选择一个翻译服务商"""
    return config_manager.select_provider()


def validate_api_keys() -> Dict[str, bool]:
    """验证 API Key 配置"""
    return config_manager.validate_api_keys()


if __name__ == "__main__":
    # 测试配置管理器
    import sys
    
    print("=" * 60)
    print("TransPDF 配置管理器测试")
    print("=" * 60)
    
    try:
        cm = ConfigManager()
        config = cm.get_config()
        print("\n✓ 配置文件加载成功")
        
        # 显示所有服务商
        providers = cm.get_providers()
        print(f"\n配置的服务商数量：{len(providers)}")
        for p in providers:
            status = "✓" if p.get("enabled") else "✗"
            print(f"  {status} {p.get('name')}: {p.get('model')}")
        
        # 验证 API Keys
        print("\nAPI Key 配置状态:")
        validation = cm.validate_api_keys()
        for name, is_configured in validation.items():
            status = "✓ 已配置" if is_configured else "✗ 未配置"
            print(f"  {name}: {status}")
        
        # 获取可用服务商
        enabled = cm.get_enabled_providers()
        print(f"\n可用服务商数量：{len(enabled)}")
        if enabled:
            print("  可用服务商:", ", ".join([p.get("name") for p in enabled]))
            
            # 测试选择
            selected = cm.select_provider()
            print(f"  随机选择结果：{selected.get('name')}")
        else:
            print("  无可用服务商")
        
        # 日志配置
        print(f"\n日志级别：{cm.get_log_level()}")
        print(f"日志文件：{cm.get_log_file_path()}")
        
        print("\n" + "=" * 60)
        print("配置测试完成")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"\n✗ 错误：{e}")
        print("请确保 config/config.json 文件存在")
        sys.exit(1)
    except RuntimeError as e:
        print(f"\n✗ 错误：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 未知错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
