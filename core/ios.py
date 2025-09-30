#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
封装一些ios平台下Airtest核心api不支持的方法
"""

# TODO: ios17以上、及以下需要分开实现，ios17以下使用aritest原生api

import wda
import time
import subprocess
import os
import requests
import traceback
from pathlib import Path


def get_wda_project_path():
    """
    获取Airtest IDE中的WebDriverAgent路径
    """
    # Airtest IDE 中 WebDriverAgent 的默认路径
    possible_paths = [
        os.path.expanduser("~/Library/Application Support/Airtest/iOS/WebDriverAgent"),
        os.path.expanduser("~/.airtest/iOS/WebDriverAgent"),
        os.path.expanduser("~/Documents/code/WebDriverAgent"),
        os.path.expanduser("~/Documents/code/iOS-Tagent")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError("未找到WebDriverAgent项目，请确保已安装Airtest IDE")


def start_wda_server():
    """启动WDA服务器"""
    try:
        # 获取设备UDID
        cmd_devices = "idevice_id -l"
        udid = subprocess.check_output(cmd_devices, shell=True).decode('utf-8').strip()

        if not udid:
            print("未找到已连接的iOS设备")
            return False

        print(f"设备UDID: {udid}")

        # 先终止现有的WDA进程
        kill_cmd = "pkill -f WebDriverAgent"
        subprocess.run(kill_cmd, shell=True)
        time.sleep(2)

        # 使用Airtest IDE中的WebDriverAgent
        wda_project = get_wda_project_path()

        # 直接运行test命令，让Xcode自动处理签名
        test_cmd = (
            f"xcodebuild -project {wda_project}/WebDriverAgent.xcodeproj "
            "-scheme WebDriverAgentRunner "
            f"-destination 'id={udid}' "
            "-allowProvisioningUpdates "  # 允许自动更新配置文件
            "test"
        )

        print("启动WDA...")
        print(f"执行命令: {test_cmd}")

        process = subprocess.Popen(
            test_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # 先确保 iproxy 在运行
        check_proxy = "ps aux | grep 'iproxy 8100' | grep -v grep"
        proxy_running = subprocess.run(check_proxy, shell=True, capture_output=True, text=True)

        if not proxy_running.stdout.strip():
            print("iproxy 未运行，正在启动...")
            # 后台运行 iproxy
            subprocess.Popen(
                "iproxy 8100 8100",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(1)  # 给 iproxy 一点启动时间

        # 等待WDA启动
        start_time = time.time()
        while time.time() - start_time < 60:
            try:
                response = requests.get('http://localhost:8100/status', timeout=1)
                if response.status_code == 200:
                    print("WDA服务器启动成功")
                    return True
            except requests.exceptions.RequestException:
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    print("WDA进程退出")
                    print(f"输出: {stdout}")
                    print(f"错误: {stderr}")
                    return False
                time.sleep(2)
                print("等待WDA服务启动...")

        print("WDA服务器启动超时")
        process.terminate()
        return False

    except Exception as e:
        print(f"启动WDA服务器失败: {str(e)}")
        print(f"异常详情: {traceback.format_exc()}")
        return False


def start_ios_app_by_wda(bundle_id, wait_timeout=30, retry_times=3):
    """
    使用WDA启动iOS应用

    Args:
        bundle_id: 应用的Bundle ID
        wait_timeout: 等待应用启动的超时时间（秒）
        retry_times: 重试次数
    """
    try:
        # 检查并启动WDA服务
        if not start_wda_server():
            raise Exception("WDA服务器启动失败")

        # 连接WDA客户端
        print("正在连接WDA客户端...")
        client = wda.Client('http://localhost:8100')

        # 等待WDA服务就绪
        start_time = time.time()
        while time.time() - start_time < 30:  # 30秒超时
            try:
                client.status()
                print("WDA客户端连接成功")
                break
            except Exception as e:
                print(f"等待WDA服务就绪... ({str(e)})")
                time.sleep(2)
        else:
            raise Exception("WDA客户端连接超时")

        # 获取会话
        session = client.session()

        for i in range(retry_times):
            try:
                # 检查应用当前状态
                app_state = client.app_state(bundle_id)
                print(f"应用当前状态: {app_state}")

                # 应用状态值说明：
                # 0: 未运行
                # 1: 后台运行（挂起）
                # 2: 后台运行
                # 3: 前台运行（挂起）
                # 4: 前台运行

                # 如果应用在运行，先终止
                if app_state['value'] != 0:  # NOT_RUNNING = 0
                    print("终止现有应用...")
                    client.app_terminate(bundle_id)
                    time.sleep(1)

                # 启动应用
                print(f"正在启动应用 {bundle_id}...")
                client.app_launch(
                    bundle_id,
                    wait_for_quiescence=True
                )

                # 等待应用进入前台
                start_time = time.time()
                while time.time() - start_time < wait_timeout:
                    app_state = client.app_state(bundle_id)
                    if app_state['value'] == 4:  # RUNNING_FOREGROUND = 4
                        print(f"应用 {bundle_id} 启动成功")
                        return True
                    print(f"等待应用启动，当前状态: {app_state}")
                    time.sleep(1)

                print(f"等待应用启动超时（尝试 {i + 1}/{retry_times}）")

            except wda.WDAError as e:
                print(f"WDA错误（尝试 {i + 1}/{retry_times}）: {str(e)}")
                if i == retry_times - 1:
                    raise
                time.sleep(2)

        return False

    except Exception as e:
        print(f"启动应用失败: {str(e)}")
        return False


def check_wda_status():
    """
    检查WDA服务状态，包括自动处理 iproxy
    """
    try:
        # 先检查 iproxy 是否运行
        check_proxy = "ps aux | grep 'iproxy 8100' | grep -v grep"
        proxy_running = subprocess.run(check_proxy, shell=True, capture_output=True, text=True)

        # 如果 iproxy 没有运行，启动它
        if not proxy_running.stdout.strip():
            print("iproxy 未运行，正在启动...")
            # 后台运行 iproxy
            subprocess.Popen(
                "iproxy 8100 8100",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(1)  # 给 iproxy 一点启动时间

        # 然后检查 WDA 状态
        response = requests.get('http://localhost:8100/status', timeout=1)
        return response.status_code == 200

    except Exception as e:
        print(f"WDA状态检查失败: {str(e)}")
        return False


def cleanup_iproxy():
    """
    清理 iproxy 进程
    """
    subprocess.run("pkill -f 'iproxy 8100'", shell=True)


if __name__ == "__main__":
    # 使用示例
    bundle_id = "com.apple.mobilesafari"  # 以Safari为例
    start_ios_app_by_wda(bundle_id)