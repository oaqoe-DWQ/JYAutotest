#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

import sys
from airtest.core.api import *
from airtest.core.api import device as get_device
from airtest.cli.parser import cli_setup
from config import DEVICE_CONFIG, BASE_DIR
from utils.logger import setup_logger
import os
from datetime import datetime

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
        
        # 使用环境变量中的时间戳
        timestamp = os.environ.get('TEST_TIMESTAMP', datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
        
        # 创建日志目录（与 test_home.py 保持一致）
        current_file_name = os.path.basename(__file__)
        log_dir = os.path.join(os.path.dirname(__file__), "log")
        os.makedirs(log_dir, exist_ok=True)
        
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
            # 使用 auto_setup 进行设备连接
            if not cli_setup():
                # 获取设备选项
                device_options = device_conf.get('options', {})
                
                # 使用 auto_setup 连接设备
                # auto_setup(
                #     __file__,
                #     logdir=log_dir,  # 使用统一的日志目录
                #     devices=[
                #         f"{device_conf['uri']}?{','.join([f'{k}={v}' for k,v in device_options.items()])}" if device_options else device_conf['uri']
                #     ],
                #     project_root=os.path.dirname(__file__)
                # )

                auto_setup(__file__, logdir=True, devices=["iOS:///http://127.0.0.1:8100"])
            
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
