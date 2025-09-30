#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
封装一些Android平台下Airtest核心api不支持的方法
包括应用管理、设备信息获取、性能监控等扩展功能
"""

import subprocess
import time
import re
import json
from typing import Dict, List, Optional, Union
from airtest.core.android.android import Android
from airtest.core.helper import G


def get_device_info() -> Dict[str, str]:
    """
    获取Android设备详细信息
    
    Returns:
        Dict: 设备信息字典
    """
    try:
        device = G.DEVICE
        if not isinstance(device, Android):
            raise ValueError("当前设备不是Android设备")
        
        # 获取设备基本信息
        info = {
            'device_id': device.serialno,
            'android_version': device.shell('getprop ro.build.version.release').strip(),
            'api_level': device.shell('getprop ro.build.version.sdk').strip(),
            'brand': device.shell('getprop ro.product.brand').strip(),
            'model': device.shell('getprop ro.product.model').strip(),
            'manufacturer': device.shell('getprop ro.product.manufacturer').strip(),
            'resolution': get_screen_resolution(),
            'battery_level': get_battery_level(),
            'wifi_status': get_wifi_status()
        }
        
        return info
    except Exception as e:
        print(f"获取设备信息失败: {str(e)}")
        return {}


def get_screen_resolution() -> str:
    """
    获取屏幕分辨率
    
    Returns:
        str: 分辨率字符串，如 "1080x1920"
    """
    try:
        device = G.DEVICE
        output = device.shell('wm size')
        # 解析输出: Physical size: 1080x1920
        match = re.search(r'(\d+)x(\d+)', output)
        if match:
            return f"{match.group(1)}x{match.group(2)}"
        return "unknown"
    except Exception as e:
        print(f"获取屏幕分辨率失败: {str(e)}")
        return "unknown"


def get_battery_level() -> int:
    """
    获取电池电量
    
    Returns:
        int: 电量百分比
    """
    try:
        device = G.DEVICE
        output = device.shell('dumpsys battery | grep level')
        # 解析输出: level: 85
        match = re.search(r'level: (\d+)', output)
        if match:
            return int(match.group(1))
        return -1
    except Exception as e:
        print(f"获取电池电量失败: {str(e)}")
        return -1


def get_wifi_status() -> bool:
    """
    获取WiFi连接状态
    
    Returns:
        bool: True表示已连接WiFi
    """
    try:
        device = G.DEVICE
        output = device.shell('dumpsys wifi | grep "Wi-Fi is"')
        return "enabled" in output.lower()
    except Exception as e:
        print(f"获取WiFi状态失败: {str(e)}")
        return False


def get_installed_apps() -> List[str]:
    """
    获取已安装应用列表
    
    Returns:
        List[str]: 应用包名列表
    """
    try:
        device = G.DEVICE
        output = device.shell('pm list packages -3')  # -3表示第三方应用
        packages = []
        for line in output.strip().split('\n'):
            if line.startswith('package:'):
                package = line.replace('package:', '')
                packages.append(package)
        return packages
    except Exception as e:
        print(f"获取已安装应用失败: {str(e)}")
        return []


def get_app_info(package_name: str) -> Dict[str, str]:
    """
    获取指定应用的详细信息
    
    Args:
        package_name: 应用包名
        
    Returns:
        Dict: 应用信息字典
    """
    try:
        device = G.DEVICE
        output = device.shell(f'dumpsys package {package_name}')
        
        info = {'package_name': package_name}
        
        # 解析版本号
        version_match = re.search(r'versionName=([^\s]+)', output)
        if version_match:
            info['version'] = version_match.group(1)
            
        # 解析版本码
        code_match = re.search(r'versionCode=(\d+)', output)
        if code_match:
            info['version_code'] = code_match.group(1)
            
        # 解析安装路径
        path_match = re.search(r'codePath=([^\s]+)', output)
        if path_match:
            info['install_path'] = path_match.group(1)
            
        return info
    except Exception as e:
        print(f"获取应用信息失败: {str(e)}")
        return {'package_name': package_name}


def force_stop_app(package_name: str) -> bool:
    """
    强制停止应用
    
    Args:
        package_name: 应用包名
        
    Returns:
        bool: 操作是否成功
    """
    try:
        device = G.DEVICE
        device.shell(f'am force-stop {package_name}')
        return True
    except Exception as e:
        print(f"强制停止应用失败: {str(e)}")
        return False


def clear_app_cache(package_name: str) -> bool:
    """
    清除应用缓存（需要root权限）
    
    Args:
        package_name: 应用包名
        
    Returns:
        bool: 操作是否成功
    """
    try:
        device = G.DEVICE
        result = device.shell(f'pm clear {package_name}')
        return "Success" in result
    except Exception as e:
        print(f"清除应用缓存失败: {str(e)}")
        return False


def grant_permission(package_name: str, permission: str) -> bool:
    """
    授予应用权限
    
    Args:
        package_name: 应用包名
        permission: 权限名称，如 "android.permission.CAMERA"
        
    Returns:
        bool: 操作是否成功
    """
    try:
        device = G.DEVICE
        device.shell(f'pm grant {package_name} {permission}')
        return True
    except Exception as e:
        print(f"授予权限失败: {str(e)}")
        return False


def revoke_permission(package_name: str, permission: str) -> bool:
    """
    撤销应用权限
    
    Args:
        package_name: 应用包名
        permission: 权限名称
        
    Returns:
        bool: 操作是否成功
    """
    try:
        device = G.DEVICE
        device.shell(f'pm revoke {package_name} {permission}')
        return True
    except Exception as e:
        print(f"撤销权限失败: {str(e)}")
        return False


def get_current_activity() -> str:
    """
    获取当前前台Activity
    
    Returns:
        str: 当前Activity名称
    """
    try:
        device = G.DEVICE
        output = device.shell('dumpsys window windows | grep -E "mCurrentFocus|mFocusedApp"')
        # 解析当前焦点窗口
        match = re.search(r'([\w\.]+/[\w\.]+)', output)
        if match:
            return match.group(1)
        return "unknown"
    except Exception as e:
        print(f"获取当前Activity失败: {str(e)}")
        return "unknown"


def get_memory_info(package_name: str) -> Dict[str, Union[int, str]]:
    """
    获取应用内存使用情况
    
    Args:
        package_name: 应用包名
        
    Returns:
        Dict: 内存信息字典
    """
    try:
        device = G.DEVICE
        output = device.shell(f'dumpsys meminfo {package_name}')
        
        info = {'package_name': package_name}
        
        # 解析内存使用量（单位：KB）
        total_match = re.search(r'TOTAL\s+(\d+)', output)
        if total_match:
            info['total_memory_kb'] = int(total_match.group(1))
            info['total_memory_mb'] = round(int(total_match.group(1)) / 1024, 2)
            
        return info
    except Exception as e:
        print(f"获取内存信息失败: {str(e)}")
        return {'package_name': package_name}


def enable_wifi() -> bool:
    """
    启用WiFi
    
    Returns:
        bool: 操作是否成功
    """
    try:
        device = G.DEVICE
        device.shell('svc wifi enable')
        return True
    except Exception as e:
        print(f"启用WiFi失败: {str(e)}")
        return False


def disable_wifi() -> bool:
    """
    禁用WiFi
    
    Returns:
        bool: 操作是否成功
    """
    try:
        device = G.DEVICE
        device.shell('svc wifi disable')
        return True
    except Exception as e:
        print(f"禁用WiFi失败: {str(e)}")
        return False


def set_airplane_mode(enable: bool) -> bool:
    """
    设置飞行模式
    
    Args:
        enable: True启用，False禁用
        
    Returns:
        bool: 操作是否成功
    """
    try:
        device = G.DEVICE
        value = 1 if enable else 0
        device.shell(f'settings put global airplane_mode_on {value}')
        device.shell('am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true' if enable else 'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false')
        return True
    except Exception as e:
        print(f"设置飞行模式失败: {str(e)}")
        return False


def take_bug_report(output_path: str = "/sdcard/bugreport.zip") -> bool:
    """
    生成bug报告
    
    Args:
        output_path: 输出路径
        
    Returns:
        bool: 操作是否成功
    """
    try:
        device = G.DEVICE
        device.shell(f'bugreport {output_path}')
        return True
    except Exception as e:
        print(f"生成bug报告失败: {str(e)}")
        return False


if __name__ == "__main__":
    # 使用示例
    print("Android扩展功能模块")
    
    # 获取设备信息
    device_info = get_device_info()
    print(f"设备信息: {device_info}")
    
    # 获取已安装应用
    apps = get_installed_apps()
    print(f"已安装应用数量: {len(apps)}")