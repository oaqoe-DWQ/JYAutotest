# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

import sys
from airtest.core.api import *
from airtest.core.api import device as get_device
from airtest.cli.parser import cli_setup
from config import DEVICE_CONFIG
from utils.logger import setup_logger

# 设置日志
logger = setup_logger(__name__)

def launch(device_type='IOS'):
    """
    连接测试设备
    
    Args:
        device_type (str): 设备类型，可选值：'IOS', 'ANDROID', 'WINDOWS'
        
    Returns:
        bool: 连接是否成功
        
    Raises:
        SystemExit: 当设备连接失败时，终止程序执行
    """
    try:
        device_type = device_type.upper()
        if device_type not in DEVICE_CONFIG:
            logger.error(f"不支持的设备类型: {device_type}")
            logger.error(f"支持的设备类型: {list(DEVICE_CONFIG.keys())}")
            sys.exit(1)
            
        device_conf = DEVICE_CONFIG[device_type]
        
        # 先检查是否已有设备连接
        try:
            current_device = get_device()
            if current_device:
                logger.info(f"已有设备连接: {current_device.uuid}")
                return True
        except:
            logger.info("没有已连接的设备，准备新建连接")
            
        # 连接设备
        logger.info(f"正在连接 {device_type} 设备: {device_conf['uri']}")
        try:
            # 直接使用 connect_device 而不是 auto_setup
            connect_device(
                device_conf['uri'],
                **device_conf.get('options', {})
            )
            
            # 验证设备连接
            current_device = get_device()
            if current_device:
                logger.info(f"设备连接成功: {current_device.uuid}")
                return True
            else:
                logger.error("设备连接失败: 无法获取设备实例")
                return False
                
        except Exception as e:
            logger.error(f"设备连接失败: {str(e)}")
            return False
            
    except Exception as e:
        logger.error(f"启动过程出现未知错误: {str(e)}")
        return False
