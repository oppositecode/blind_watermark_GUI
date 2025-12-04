"""配置管理模块"""
import os
import json

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# 默认配置
DEFAULT_CONFIG = {
    "background_image": "",
    "background_opacity": 0.3
}


def load_config():
    """加载配置文件
    
    Returns:
        dict: 配置字典
    """
    config = DEFAULT_CONFIG.copy()
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                config.update(saved_config)
                # 验证背景图片路径是否存在
                bg_path = config.get("background_image", "")
                if bg_path and not os.path.exists(bg_path):
                    config["background_image"] = ""
    except Exception:
        pass
    return config


def save_config(config):
    """保存配置文件
    
    Args:
        config: 配置字典
    """
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
