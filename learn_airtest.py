#!/usr/bin/env python
# -*- coding: utf-8 -*-

from airtest.core.api import *
from airtest.core.ios.ios import IOS

def init_ios_device():
    """
    初始化iOS设备的示例
    支持以下几种方式：
    1. 不带参数：自动连接设备
    2. 指定设备UDID
    3. 指定WDA端口
    """
    try:
        # 方式1：自动连接第一个设备
        device = init_device(platform="iOS")
        
        # 方式2：通过UDID连接特定设备
        # device = init_device(platform="iOS", uuid="your_device_udid")
        
        # 方式3：指定WDA端口
        # device = init_device(platform="iOS", uuid="http://localhost:8100")
        
        print(f"设备初始化成功: {device}")
        return device
    except Exception as e:
        print(f"设备初始化失败: {str(e)}")
        return None

def connect_ios_device():
    """
    连接iOS设备的示例
    展示了直接使用IOS类连接设备的方法
    """
    try:
        # 方式1：自动连接第一个设备
        device = connect_device("iOS:///")
        
        # 方式2：通过UDID连接
        # device = connect_device("iOS:///your_device_udid")
        
        # 方式3：指定WDA服务地址和端口
        # device = connect_device("iOS://127.0.0.1:8100/")
        
        print(f"设备连接成功: {device}")
        return device
    except Exception as e:
        print(f"设备连接失败: {str(e)}")
        return None
    

def auto_setup_ios():
    """
    使用auto_setup快速初始化iOS设备的示例
    auto_setup会自动完成以下工作：
    1. 初始化日志系统
    2. 连接设备
    3. 启动应用（如果指定）
    """
    try:
        # 方式1：基础用法，自动连接设备
        auto_setup(__file__, devices=["iOS:///http://127.0.0.1:8100"])
        
        # 方式2：指定设备
        # auto_setup(__file__, devices=["iOS:///"])
        
        # 方式3：完整参数示例
        # auto_setup(
        #     __file__,                    # 脚本路径，用于设置日志路径
        #     devices=["iOS:///"],         # 设备列表
        #     logdir="air_log",           # 日志目录
        #     project_root=".",           # 项目根目录
        #     compress=90                 # 截图压缩比例
        # )
        
        print("auto_setup初始化成功")
    except Exception as e:
        print(f"auto_setup初始化失败: {str(e)}")


def start_ios_app(bundle_id):
    """
    启动iOS应用的示例
    展示了不同的启动方式和参数设置
    """
    try:
        # 方式1：基础用法，只指定包名启动
        # start_app("com.vv.work")
        start_app(bundle_id)
        
        # 方式2：启动时带参数
        # start_app(
        #     "com.example.app",
        #     args={
        #         "url": "scheme://path",           # 启动scheme
        #         "wait_timeout": 30,               # 启动超时时间（秒）
        #         "stop": True                      # 如果应用在运行，是否先停止
        #     }
        # )
        
        # 方式3：完整启动流程示例
        # stop_app("com.example.app")              # 先停止应用
        # sleep(1)                                 # 等待应用完全停止
        # clear_app("com.example.app")             # 清除应用数据（可选）
        # start_app("com.example.app")             # 启动应用
        
        print("应用启动成功")
    except Exception as e:
        print(f"应用启动失败: {str(e)}")


def start_ios_app_by_instance(bundle_id):
    """
    使用iOS实例启动iOS应用的示例
    可以获得更多控制选项和详细信息
    """
    try:
        # 获取当前设备实例
        ios_dev = device()
        
        # 方式2：使用iOS实例启动
        ios_dev.start_app(
            bundle_id=bundle_id,          # 应用的Bundle ID
            args=[],                      # 启动参数（可选）
            wait=True,                    # 是否等待启动完成
            timeout=30,                   # 启动超时时间
        )
        
        # 获取应用状态
        app_state = ios_dev.app_state(bundle_id)
        print(f"应用 {bundle_id} 启动成功（通过iOS实例）")
        print(f"应用状态: {app_state}")
        
    except Exception as e:
        print(f"应用启动失败: {str(e)}")

if __name__ == "__main__":
    # 使用init_device方式
    # device1 = init_ios_device()
    
    # # 使用connect_device方式
    device2 = connect_ios_device()
    print(device2.list_app())


    # auto_setup_ios()
    #start_ios_app("com.apple.mobilesafari")

    start_ios_app_by_instance("com.apple.mobilesafari")  # 使用iOS实例