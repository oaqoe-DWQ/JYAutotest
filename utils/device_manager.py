#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

from airtest.core.api import *
from config import DEVICE_CONFIG
from utils.logger import setup_logger
from airtest.cli.parser import cli_setup
import os


logger = setup_logger(__name__)

class DeviceManager:
    @staticmethod
    def init_device(test_file, log_dir):
        """初始化设备并设置日志目录"""
        try:
            # 获取脚本名（不含扩展名）
            script_name = os.path.splitext(os.path.basename(test_file))[0]
            
            # 在 log_dir 中创建以脚本名命名的子目录
            script_log_dir = os.path.join(log_dir, script_name)
            os.makedirs(script_log_dir, exist_ok=True)
            
            if not cli_setup():
                auto_setup(
                    test_file,
                    logdir=script_log_dir,  # 使用包含脚本名的目录
                    devices=[DEVICE_CONFIG['IOS']['uri']]
                )
            logger.info(f"设备初始化成功，日志目录: {script_log_dir}")
            
        except Exception as e:
            logger.error(f"设备初始化失败: {str(e)}")
            raise

    @staticmethod
    def disconnect():
        """断开设备连接"""
        try:
            # 获取当前设备
            current_device = device()
            if current_device:
                # 使用 airtest 的 device 实例方法断开连接
                current_device.disconnect()
                logger.info("设备已断开连接")
            else:
                logger.warning("没有找到已连接的设备")
        except Exception as e:
            logger.error(f"断开设备失败: {str(e)}") 