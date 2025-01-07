import logging
from config import LOG_CONFIG


def setup_logger(name=None):
    """
    统一的日志配置函数
    
    Args:
        name: logger名称,默认为None(根logger)
        
    Returns:
        logger实例
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加handler
    if not logger.handlers:
        # 设置日志级别
        logger.setLevel(LOG_CONFIG['LEVEL'])
        
        # 创建格式化器
        formatter = logging.Formatter(LOG_CONFIG['FORMAT'])
        
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_CONFIG['HANDLERS']['console']['level'])
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 如果配置了文件处理器，也可以在这里添加
    
    return logger