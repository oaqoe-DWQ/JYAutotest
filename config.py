#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Allure 相关配置
ALLURE_CONFIG = {
    'REPORT_DIR': os.path.join(BASE_DIR, "allure_report"),
    'RESULT_DIR': os.path.join(BASE_DIR, "allure_result"),
}

# Airtest 相关配置
AIRTEST_CONFIG = {
    'EXPORT_DIR': os.path.join(BASE_DIR, "export_dir"),
}

# 其他配置可以按需添加
LOG_CONFIG = {
    'LEVEL': 'INFO',
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# 设备连接配置
DEVICE_CONFIG = {
    'IOS': {
        'uri': "iOS:///http://127.0.0.1:8100",
        'options': {}
    },
    'ANDROID': {
        'uri': "Android:///",  # 默认连接第一个设备
        'options': {
            'cap_method': 'JAVACAP',  # 截图方法
            'touch_method': 'ADBTOUCH',  # 触摸方法
            'ori_method': 'ADBORI',  # 旋转方法
            'ime_method': 'ADBIME'  # 输入法方法
        },
        # 可以指定特定设备
        'specific_device': None,  # 例如: "emulator-5554" 或设备序列号
    },
    'WINDOWS': {
        'uri': "Windows:///",
        'options': {}
    }
} 


# 日志配置
LOG_CONFIG = {
    'LEVEL': logging.INFO,
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'HANDLERS': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
        },
        # 如果需要文件日志，可以在这里添加
        # 'file': {
        #     'class': 'logging.FileHandler',
        #     'filename': 'test.log',
        #     'level': logging.INFO,
        # }
    }
}

# 安装包下载地址
APP_DOWNLOAD_URL = {
    'IPA_DOWNLOAD_URL': "",
    'ANDROID_DOWNLOAD_URL': "",
}
