# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"
from utils.time_manager import TimeManager
from launch import launch
import pytest
import os
from config import ALLURE_CONFIG
import sys
import logging
import argparse

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='UI自动化测试启动程序')
    parser.add_argument(
        '--device', 
        type=str, 
        choices=['ios', 'android', 'windows'], 
        default='ios',
        help='指定测试设备类型: ios, android, windows (默认: ios)'
    )
    return parser.parse_args()

if __name__ == '__main__':
    # 解析命令行参数
    args = parse_args()
    device_type = args.device.upper()
    logger.info(f"选择的设备类型: {device_type}")
    
    # 获取统一的时间戳
    timestamp = TimeManager.get_timestamp()
    # 设置为环境变量，供所有测试用例使用
    os.environ['TEST_TIMESTAMP'] = timestamp
    
    # 启动连接设备模块
    try:
        launch(device_type=device_type)
    except SystemExit:
        logger.error("设备连接失败，终止测试执行")
        sys.exit(1)

    # 生成报告路径
    allure_report = ALLURE_CONFIG['REPORT_DIR']
    allure_result = ALLURE_CONFIG['RESULT_DIR']

    # 运行测试并生成报告
    pytest.main(['-v', '--alluredir', allure_result, '--clean-alluredir'])
    os.system("allure generate -c -o %s " % (allure_report))
    os.system('allure serve %s' % allure_result)
