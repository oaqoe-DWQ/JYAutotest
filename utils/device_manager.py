#!/usr/bin/env python
# -*- coding: utf-8 -*-

from airtest.core.api import *
from airtest.core.android.android import Android
from airtest.core.ios.ios import IOS
from airtest.core.win.win import Windows
from config import DEVICE_CONFIG
from utils.logger import setup_logger
from airtest.cli.parser import cli_setup
import os
import subprocess
import re
from typing import List, Dict, Optional


logger = setup_logger(__name__)

class DeviceManager:
    @staticmethod
    def init_device(test_file, log_dir, platform="iOS"):
        """初始化设备并设置日志目录
        
        Args:
            test_file: 测试文件路径
            log_dir: 日志目录
            platform: 平台类型 (iOS/Android/Windows)
        """
        try:
            # 获取脚本名（不含扩展名）
            script_name = os.path.splitext(os.path.basename(test_file))[0]
            
            # 在 log_dir 中创建以脚本名命名的子目录
            script_log_dir = os.path.join(log_dir, script_name)
            os.makedirs(script_log_dir, exist_ok=True)
            
            # 根据平台选择设备URI
            platform_upper = platform.upper()
            if platform_upper in DEVICE_CONFIG:
                device_uri = DEVICE_CONFIG[platform_upper]['uri']
            else:
                raise ValueError(f"不支持的平台: {platform}")
            
            if not cli_setup():
                auto_setup(
                    test_file,
                    logdir=script_log_dir,
                    devices=[device_uri]
                )
            logger.info(f"设备初始化成功，平台: {platform}，日志目录: {script_log_dir}")
            
        except Exception as e:
            logger.error(f"设备初始化失败: {str(e)}")
            raise
    
    @staticmethod
    def get_android_devices() -> List[str]:
        """获取已连接的Android设备列表
        
        Returns:
            List[str]: 设备序列号列表
        """
        try:
            result = subprocess.run(
                ['adb', 'devices'], 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            devices = []
            for line in result.stdout.strip().split('\n')[1:]:  # 跳过第一行标题
                if '\t' in line and 'device' in line:
                    device_id = line.split('\t')[0]
                    devices.append(device_id)
            
            logger.info(f"发现Android设备: {devices}")
            return devices
            
        except subprocess.CalledProcessError as e:
            logger.error(f"获取Android设备失败: {str(e)}")
            return []
        except FileNotFoundError:
            logger.error("adb命令未找到，请确保Android SDK已安装并配置环境变量")
            return []
    
    @staticmethod
    def connect_android_device(device_id: Optional[str] = None) -> bool:
        """连接Android设备
        
        Args:
            device_id: 设备序列号，为None时连接第一个可用设备
            
        Returns:
            bool: 连接是否成功
        """
        try:
            devices = DeviceManager.get_android_devices()
            if not devices:
                logger.error("未发现可用的Android设备")
                return False
            
            # 如果未指定设备ID，使用第一个设备
            target_device = device_id if device_id else devices[0]
            
            if target_device not in devices:
                logger.error(f"指定的设备 {target_device} 未连接")
                return False
            
            # 使用Airtest连接设备
            android_device = Android(serialno=target_device)
            connect_device(android_device)
            
            logger.info(f"成功连接Android设备: {target_device}")
            return True
            
        except Exception as e:
            logger.error(f"连接Android设备失败: {str(e)}")
            return False
    
    @staticmethod
    def get_device_info(platform: str) -> Dict[str, str]:
        """获取设备信息
        
        Args:
            platform: 平台类型
            
        Returns:
            Dict: 设备信息
        """
        try:
            current_device = device()
            if not current_device:
                return {"error": "未连接设备"}
            
            info = {"platform": platform}
            
            if isinstance(current_device, Android):
                # Android设备信息
                info.update({
                    "device_id": current_device.serialno,
                    "android_version": current_device.shell('getprop ro.build.version.release').strip(),
                    "api_level": current_device.shell('getprop ro.build.version.sdk').strip(),
                    "brand": current_device.shell('getprop ro.product.brand').strip(),
                    "model": current_device.shell('getprop ro.product.model').strip()
                })
            elif isinstance(current_device, IOS):
                # iOS设备信息
                info.update({
                    "device_id": getattr(current_device, 'uuid', 'unknown'),
                    "ios_version": "unknown",  # 需要特定方法获取
                    "device_name": "unknown"
                })
            
            return info
            
        except Exception as e:
            logger.error(f"获取设备信息失败: {str(e)}")
            return {"error": str(e)}
    
    @staticmethod
    def check_adb_connection() -> bool:
        """检查adb连接状态
        
        Returns:
            bool: adb服务是否正常
        """
        try:
            result = subprocess.run(
                ['adb', 'version'], 
                capture_output=True, 
                text=True, 
                check=True
            )
            logger.info("adb连接正常")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("adb连接异常，请检查Android SDK安装")
            return False
    
    @staticmethod
    def restart_adb() -> bool:
        """重启adb服务
        
        Returns:
            bool: 重启是否成功
        """
        try:
            # 停止adb服务
            subprocess.run(['adb', 'kill-server'], check=True)
            # 启动adb服务
            subprocess.run(['adb', 'start-server'], check=True)
            logger.info("adb服务重启成功")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"adb服务重启失败: {str(e)}")
            return False

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
    
    @staticmethod
    def wait_for_device(timeout: int = 30) -> bool:
        """等待设备连接
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            bool: 是否成功连接设备
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            devices = DeviceManager.get_android_devices()
            if devices:
                logger.info(f"设备连接成功: {devices[0]}")
                return True
            
            logger.info("等待设备连接...")
            time.sleep(2)
        
        logger.error(f"等待设备连接超时 ({timeout}秒)")
        return False