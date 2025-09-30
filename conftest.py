#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import allure
import os
import logging
import zipfile
import shutil
from datetime import datetime
from config import AIRTEST_CONFIG, ALLURE_CONFIG
from utils.logger import setup_logger
from utils.device_manager import DeviceManager

# 设置日志
logger = setup_logger(__name__)


@pytest.fixture(scope="module")
def setup_test(request):
    """测试环境初始化，在测试开始时连接设备，在测试结束后断开设备"""
    # 获取当前测试文件路径
    test_file = request.module.__file__
    test_dir = os.path.dirname(test_file)
    log_dir = os.path.join(test_dir, 'log')
    
    # 确保日志目录存在
    os.makedirs(log_dir, exist_ok=True)
    
    # 根据测试文件路径自动识别平台
    platform = "iOS"  # 默认平台
    if "android" in test_file.lower() or "andriod" in test_file.lower():
        platform = "Android"
    elif "windows" in test_file.lower() or "win" in test_file.lower():
        platform = "Windows"
    elif "macos" in test_file.lower() or "mac" in test_file.lower():
        platform = "macOS"
    
    logger.info(f"自动识别平台: {platform}")
    
    # 初始化设备
    DeviceManager.init_device(test_file, log_dir, platform)
    
    yield
    
    # 测试结束后断开设备
    DeviceManager.disconnect()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        try:
            # 获取当前测试文件名
            current_file_name = os.path.basename(item.fspath)
            # 获取时间戳环境变量
            timestamp = os.environ.get('TEST_TIMESTAMP')
            
            if not timestamp:
                logger.warning("TEST_TIMESTAMP 环境变量未设置")
                return
                
            # 构造报告路径
            base_export_dir = os.path.join(AIRTEST_CONFIG['EXPORT_DIR'], current_file_name, timestamp)
            # 添加以测试文件名（不带扩展名）命名的日志目录
            test_name = os.path.splitext(current_file_name)[0]
            export_dir = os.path.join(base_export_dir, f"{test_name}.log")
            airtest_report = os.path.join(export_dir, "log.html")
            
            logger.info(f"查找 Airtest 报告路径: {airtest_report}")
            
            if os.path.exists(airtest_report):
                logger.info(f"找到 Airtest 报告文件: {airtest_report}")
                
                # 获取报告所在目录（而不是具体的html文件）
                report_dir = os.path.dirname(airtest_report)
                logger.info(f"Airtest 报告目录: {report_dir}")
                
                # 创建临时zip文件
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                zip_filename = f"airtest_report_{timestamp_str}.zip"
                zip_filepath = os.path.join(os.getcwd(), zip_filename)
                
                try:
                    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        # 遍历报告目录下的所有文件
                        for root, dirs, files in os.walk(report_dir):
                            # 从遍历列表中移除 __pycache__ 目录
                            if '__pycache__' in dirs:
                                dirs.remove('__pycache__')
                            
                            for file in files:
                                file_path = os.path.join(root, file)
                                # 获取相对路径，这样在zip文件中保持目录结构
                                arcname = os.path.relpath(file_path, report_dir)
                                try:
                                    zipf.write(file_path, arcname)
                                    logger.info(f"添加文件到压缩包: {arcname}")
                                except Exception as e:
                                    logger.error(f"压缩文件 {file_path} 时出错: {str(e)}")
                    
                    # 将zip文件添加到Allure报告
                    with open(zip_filepath, 'rb') as f:
                        allure.attach(
                            f.read(),
                            name=f"{current_file_name} - (下载到本地即可查看)Airtest Report.zip",
                            attachment_type="application/zip",
                            extension='.zip'
                        )
                    logger.info("成功将完整的 Airtest 报告添加到 Allure")
                    
                except Exception as e:
                    logger.error(f"压缩报告文件时出错: {str(e)}", exc_info=True)
                finally:
                    # 清理临时zip文件
                    if os.path.exists(zip_filepath):
                        try:
                            os.remove(zip_filepath)
                            logger.info(f"清理临时zip文件: {zip_filepath}")
                        except Exception as e:
                            logger.error(f"清理临时zip文件时出错: {str(e)}")
            else:
                logger.warning(f"Airtest 报告文件不存在: {airtest_report}")
                
        except Exception as e:
            logger.error(f"添加 Airtest 报告到 Allure 时出错: {str(e)}")