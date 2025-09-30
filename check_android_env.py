#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Android环境检查脚本
检查Android自动化测试所需的环境是否就绪
"""

import subprocess
import sys
import os
from utils.logger import setup_logger
from utils.device_manager import DeviceManager
from core.andriod import get_device_info

logger = setup_logger(__name__)


def check_python_version():
    """检查Python版本"""
    print("=" * 50)
    print("1. 检查Python版本")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python版本: {sys.version}")
        return True
    else:
        print(f"❌ Python版本过低: {sys.version}")
        print("   要求: Python 3.7+")
        return False


def check_adb_installation():
    """检查ADB是否安装"""
    print("=" * 50)
    print("2. 检查ADB安装")
    
    try:
        result = subprocess.run(['adb', 'version'], capture_output=True, text=True, check=True)
        print(f"✅ ADB已安装: {result.stdout.split()[4]}")
        return True
    except FileNotFoundError:
        print("❌ ADB未安装或未配置到环境变量")
        print("   解决方案:")
        print("   - 安装Android SDK Platform Tools")
        print("   - 将adb路径添加到系统环境变量PATH中")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ ADB命令执行失败: {e}")
        return False


def check_android_devices():
    """检查Android设备连接"""
    print("=" * 50)
    print("3. 检查Android设备连接")
    
    devices = DeviceManager.get_android_devices()
    if devices:
        print(f"✅ 发现 {len(devices)} 个Android设备:")
        for i, device in enumerate(devices, 1):
            print(f"   {i}. {device}")
        return True
    else:
        print("❌ 未发现Android设备")
        print("   解决方案:")
        print("   - 连接Android设备并启用USB调试")
        print("   - 启动Android模拟器")
        print("   - 检查设备驱动是否正常")
        return False


def check_required_packages():
    """检查必需的Python包"""
    print("=" * 50)
    print("4. 检查Python依赖包")
    
    required_packages = [
        'airtest',
        'pytest', 
        'allure-pytest',
        'opencv-contrib-python',
        'pillow',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True


def check_device_capabilities():
    """检查设备功能"""
    print("=" * 50)
    print("5. 检查设备功能")
    
    devices = DeviceManager.get_android_devices()
    if not devices:
        print("⚠️  无设备连接，跳过功能检查")
        return False
    
    try:
        # 连接第一个设备
        if DeviceManager.connect_android_device(devices[0]):
            print(f"✅ 成功连接设备: {devices[0]}")
            
            # 获取设备信息
            device_info = get_device_info()
            if device_info:
                print("✅ 设备信息获取成功:")
                for key, value in device_info.items():
                    print(f"   {key}: {value}")
            else:
                print("❌ 设备信息获取失败")
                return False
            
            return True
        else:
            print(f"❌ 连接设备失败: {devices[0]}")
            return False
            
    except Exception as e:
        print(f"❌ 设备功能检查失败: {str(e)}")
        return False


def check_airtest_capabilities():
    """检查Airtest功能"""
    print("=" * 50)
    print("6. 检查Airtest功能")
    
    try:
        from airtest.core.api import *
        from airtest.core.android.android import Android
        
        devices = DeviceManager.get_android_devices()
        if not devices:
            print("⚠️  无设备连接，跳过Airtest功能检查")
            return False
        
        # 测试截图功能
        print("测试截图功能...")
        screenshot_path = snapshot("environment_check.png")
        if screenshot_path and os.path.exists(screenshot_path):
            print(f"✅ 截图功能正常: {screenshot_path}")
            # 清理测试截图
            try:
                os.remove(screenshot_path)
            except:
                pass
        else:
            print("❌ 截图功能异常")
            return False
        
        print("✅ Airtest功能检查通过")
        return True
        
    except Exception as e:
        print(f"❌ Airtest功能检查失败: {str(e)}")
        return False


def print_environment_summary():
    """打印环境配置建议"""
    print("=" * 50)
    print("环境配置建议")
    print("=" * 50)
    
    print("🔧 Android开发环境配置:")
    print("1. 安装Android Studio或Android SDK Platform Tools")
    print("2. 配置环境变量:")
    print("   - ANDROID_HOME: Android SDK路径")
    print("   - PATH: 添加 %ANDROID_HOME%\\platform-tools")
    
    print("\n📱 设备配置:")
    print("1. 真机设备:")
    print("   - 启用开发者选项")
    print("   - 开启USB调试")
    print("   - 信任调试计算机")
    
    print("2. 模拟器:")
    print("   - 使用Android Studio AVD Manager创建")
    print("   - 推荐配置: API 28+, 2GB+ RAM")
    
    print("\n🐍 Python环境:")
    print("1. Python 3.7+")
    print("2. 安装项目依赖: pip install -r requirements.txt")
    
    print("\n🧪 运行测试:")
    print("1. 单个测试: pytest cases/andriod/test1/test_android_demo.py -v")
    print("2. 生成报告: pytest cases/andriod/ --alluredir=allure_result")
    print("3. 查看报告: allure serve allure_result")


def main():
    """主函数"""
    print("Android自动化测试环境检查")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_adb_installation, 
        check_android_devices,
        check_required_packages,
        check_device_capabilities,
        check_airtest_capabilities
    ]
    
    results = []
    
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ 检查过程中出现错误: {str(e)}")
            results.append(False)
    
    # 总结
    print("=" * 50)
    print("检查结果总结")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 所有检查通过 ({passed}/{total})")
        print("✅ Android自动化测试环境就绪!")
    else:
        print(f"⚠️  检查通过: {passed}/{total}")
        print("❌ 请根据上述提示解决环境问题")
    
    print_environment_summary()


if __name__ == "__main__":
    main()