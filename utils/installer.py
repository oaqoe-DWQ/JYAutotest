#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

import os
import sys
from airtest.core.api import *
from airtest.core.helper import G
from airtest.core.ios.ios import IOS
from airtest.core.android.android import Android

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))

from utils.logger import setup_logger
from config import BASE_DIR, DEVICE_CONFIG

# 设置日志
logger = setup_logger(__name__)

# 根据当前平台决定是否导入Windows模块
if sys.platform == 'win32':
    from airtest.core.win.win import Windows
    WINDOWS_SUPPORT = True
else:
    WINDOWS_SUPPORT = False
    Windows = None  # 定义一个空的Windows类型
    logger.info("当前非Windows平台, Windows支持未启用")


class AppInstaller:
    def __init__(self):
        self.device = None
        self.pkgs_dir = os.path.join(BASE_DIR, 'pkgs')
        self.bundle_id = "com.vv.work"
        
    def connect_device(self, platform):
        """连接设备"""
        try:
            if platform.upper() == 'WINDOWS' and not WINDOWS_SUPPORT:
                raise ValueError("当前系统不支持Windows平台测试")
            
            if platform.upper() not in DEVICE_CONFIG:
                raise ValueError(f"不支持的平台: {platform}")
            
            device_conf = DEVICE_CONFIG[platform.upper()]
            self.device = connect_device(device_conf['uri'])
            
            # 设置设备特定选项
            for key, value in device_conf['options'].items():
                setattr(self.device, key, value)
            
            logger.info(f"成功连接{platform}设备")
            return self.device
            
        except Exception as e:
            logger.error(f"连接设备失败: {str(e)}")
            raise
    
    def find_package(self, platform, version):
        """查找安装包"""
        try:
            # 定义平台对应的文件后缀
            platform_extensions = {
                'ios': '.ipa',
                'android': '.apk',
                'windows': '.exe'
            }
            
            # 获取当前平台的文件后缀
            platform_key = platform.lower()
            if platform_key not in platform_extensions:
                raise ValueError(f"不支持的平台类型: {platform}")
                
            extension = platform_extensions[platform_key]
            
            # 遍历查找匹配的文件
            for file in os.listdir(self.pkgs_dir):
                # 检查文件后缀和版本号
                if file.endswith(extension) and version in file:
                    logger.info(f"找到{platform}平台版本{version}的安装包: {file}")
                    return os.path.join(self.pkgs_dir, file)
            
            raise FileNotFoundError(f"未找到{platform}平台版本{version}的安装包（后缀{extension})")
            
        except Exception as e:
            logger.error(f"查找安装包失败: {str(e)}")
            raise
    
    def get_installed_version(self):
        """获取已安装的应用版本号"""
        try:
            if isinstance(self.device, IOS):
                # 使用 app_info 方法获取应用信息
                app_info = self.device.app_info(self.bundle_id)
                if not app_info:
                    raise ValueError(f"应用 {self.bundle_id} 未安装")
                return app_info.get('CFBundleShortVersionString')
            elif isinstance(self.device, Android):
                return self.device.get_app_version(self.bundle_id)
            elif isinstance(self.device, Windows):
                # Windows版本获取方法可能需要特殊处理
                raise NotImplementedError("Windows版本号获取方法未实现")
            else:
                raise ValueError("不支持的设备类型")
                
        except Exception as e:
            logger.error(f"获取应用版本号失败: {str(e)}")
            raise
    
    def install_app(self, platform, version):
        """安装应用"""
        try:
            # 连接设备
            self.connect_device(platform)
            
            # 先尝试卸载已有应用
            logger.info("检查并卸载已有应用...")
            self.uninstall_app(platform)
            
            # 查找安装包
            package_path = self.find_package(platform, version)
            logger.info(f"找到安装包: {package_path}")
            
            # 安装应用
            logger.info("开始安装应用...")
            if isinstance(self.device, IOS):
                self.device.install_app(package_path)
            elif isinstance(self.device, Android):
                self.device.install_app(package_path)
            elif isinstance(self.device, Windows):
                # Windows安装方法可能需要特殊处理
                raise NotImplementedError("Windows安装方法未实现")
            
            # 验证安装结果
            installed_version = None
            if isinstance(self.device, IOS):
                installed_apps = self.device.list_app()
                logger.info(f"设备上已安装的应用列表: {installed_apps}")
                for app in installed_apps:
                    if app[0] == self.bundle_id:
                        installed_version = app[2]
                        break
            elif isinstance(self.device, Android):
                installed_apps = self.device.list_app()
                logger.info(f"设备上已安装的应用列表: {installed_apps}")
                for app in installed_apps:
                    if app[0] == self.bundle_id:
                        installed_version = app[2]
                        break
            elif isinstance(self.device, Windows):
                raise NotImplementedError("Windows版本验证未实现")
            
            # 检查安装结果
            if not installed_version:
                raise ValueError(f"应用 {self.bundle_id} 安装失败")
            
            # 检查版本号前三段是否匹配
            if not installed_version.startswith('.'.join(version.split('.')[:3])):
                raise ValueError(f"安装版本不匹配: 期望是 {'.'.join(version.split('.')[:3])} , 实际为 {installed_version}")
            
            logger.info(f"应用安装成功，版本: {installed_version}")
            
        except Exception as e:
            logger.error(f"安装应用失败: {str(e)}")
            raise
    
    def uninstall_app(self, platform):
        """卸载应用"""
        try:
            # 连接设备（如果还未连接）
            if not self.device:
                self.connect_device(platform)
            
            # 检查应用是否已安装
            logger.info(f"检查应用 {self.bundle_id} 是否已安装...")
            
            is_installed = False
            app_version = None
            try:
                if isinstance(self.device, IOS):
                    installed_apps = self.device.list_app()
                    logger.info(f"设备上已安装的应用列表: {installed_apps}")
                    # 查找目标应用并获取版本信息
                    for app in installed_apps:
                        if app[0] == self.bundle_id:
                            is_installed = True
                            app_version = app[2]  # 获取版本号
                            break
                elif isinstance(self.device, Android):
                    is_installed = self.device.check_app(self.bundle_id)
                elif isinstance(self.device, Windows):
                    # Windows检查方法可能需要特殊处理
                    raise NotImplementedError("Windows平台未实现")
            except:
                is_installed = False
            
            # 根据安装状态决定是否卸载
            if not is_installed:
                logger.info(f"应用 {self.bundle_id} 未安装，跳过卸载步骤")
                return
            
            # 卸载应用（添加版本信息到日志）
            logger.info(f"开始卸载 {self.bundle_id}(版本: {app_version})")
            
            # 卸载应用
            if isinstance(self.device, IOS):
                self.device.uninstall_app(self.bundle_id)
            elif isinstance(self.device, Android):
                self.device.uninstall_app(self.bundle_id)
            elif isinstance(self.device, Windows):
                # Windows卸载方法可能需要特殊处理
                raise NotImplementedError("Windows卸载方法未实现")
            
            logger.info("应用卸载成功")
            
        except Exception as e:
            logger.error(f"卸载应用失败: {str(e)}")
            raise

def install_app(platform, version):
    """便捷的安装函数"""
    installer = AppInstaller()
    installer.install_app(platform, version)

def uninstall_app(platform):
    """便捷的卸载函数"""
    installer = AppInstaller()
    installer.uninstall_app(platform)

if __name__ == "__main__":
    # 示例使用
    try:
        # 安装应用
        platform = "ios"
        version = "2.9.26.19736"
        install_app(platform, version)
        
        # 卸载应用
        # uninstall_app(platform)
    except Exception as e:
        logger.error(f"错误: {str(e)}")



