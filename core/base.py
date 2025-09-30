#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Airtest UI自动化测试基类
支持iOS、Android、Windows等多平台
封装常用的Airtest核心API
"""

import os
import time
from typing import Union, List, Optional
from airtest.core.api import *
from airtest.core.helper import G
from airtest.core.ios.ios import IOS
from airtest.core.android.android import Android
from airtest.core.win.win import Windows
from poco.drivers.ios import iosPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from ios import start_ios_app_by_wda


class BaseTest:
    def __init__(self, platform: str = "iOS"):
        """
        初始化测试基类

        Args:
            platform: 测试平台，支持 "iOS"(默认)、"Android"、"Windows"
        """
        self.platform = platform.lower()
        self.device = None
        self.poco = None
        self._init_device()
        self._init_poco()

    def _init_device(self):
        """初始化设备"""
        if self.platform == "ios":
            self.device = IOS()
        elif self.platform == "android":
            self.device = Android()
        elif self.platform == "windows":
            self.device = Windows()
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")

        if self.device:
            G.add_device(self.device)

    def _init_poco(self):
        """初始化Poco对象"""
        if self.platform == "ios":
            self.poco = iosPoco()
        elif self.platform == "android":
            self.poco = AndroidUiautomationPoco(use_airtest_input=True)

    def start_app(self, package: str) -> bool:
        """
        启动应用

        Args:
            package: 应用包名/Bundle ID
        """
        try:
            if self.platform == "ios":
                # iOS 17及以上使用WDA启动
                return start_ios_app_by_wda(package)
            else:
                self.device.start_app(package)
                return True
        except Exception as e:
            print(f"启动应用失败: {str(e)}")
            return False

    def stop_app(self, package: str) -> bool:
        """停止应用"""
        try:
            self.device.stop_app(package)
            return True
        except Exception as e:
            print(f"停止应用失败: {str(e)}")
            return False

    def clear_app(self, package: str) -> bool:
        """清除应用数据"""
        try:
            self.device.clear_app(package)
            return True
        except Exception as e:
            print(f"清除应用数据失败: {str(e)}")
            return False

    def install(self, filepath: str) -> bool:
        """安装应用"""
        try:
            self.device.install_app(filepath)
            return True
        except Exception as e:
            print(f"安装应用失败: {str(e)}")
            return False

    def uninstall(self, package: str) -> bool:
        """卸载应用"""
        try:
            self.device.uninstall_app(package)
            return True
        except Exception as e:
            print(f"卸载应用失败: {str(e)}")
            return False

    def snapshot(self, filename: str = None) -> str:
        """截图"""
        try:
            return self.device.snapshot(filename)
        except Exception as e:
            print(f"截图失败: {str(e)}")
            return ""

    def wake(self) -> bool:
        """唤醒设备"""
        try:
            self.device.wake()
            return True
        except Exception as e:
            print(f"唤醒设备失败: {str(e)}")
            return False

    def home(self) -> bool:
        """回到主页"""
        try:
            self.device.home()
            return True
        except Exception as e:
            print(f"回到主页失败: {str(e)}")
            return False

    def touch(self, v: Union[tuple, list, str], **kwargs) -> bool:
        """点击操作"""
        try:
            self.device.touch(v, **kwargs)
            return True
        except Exception as e:
            print(f"点击失败: {str(e)}")
            return False

    def click(self, v: Union[tuple, list, str], **kwargs) -> bool:
        """点击操作（同touch）"""
        return self.touch(v, **kwargs)

    def double_click(self, v: Union[tuple, list, str], **kwargs) -> bool:
        """双击操作"""
        try:
            self.device.double_click(v, **kwargs)
            return True
        except Exception as e:
            print(f"双击失败: {str(e)}")
            return False

    def swipe(self, v1: Union[tuple, list, str], v2: Union[tuple, list, str], **kwargs) -> bool:
        """滑动操作"""
        try:
            self.device.swipe(v1, v2, **kwargs)
            return True
        except Exception as e:
            print(f"滑动失败: {str(e)}")
            return False

    def pinch(self, in_or_out: str = 'in', center: Optional[tuple] = None, percent: float = 0.5) -> bool:
        """缩放操作"""
        try:
            self.device.pinch(in_or_out, center, percent)
            return True
        except Exception as e:
            print(f"缩放失败: {str(e)}")
            return False

    def keyevent(self, keyname: str, **kwargs) -> bool:
        """按键事件"""
        try:
            self.device.keyevent(keyname, **kwargs)
            return True
        except Exception as e:
            print(f"按键事件失败: {str(e)}")
            return False

    def text(self, text: str, enter: bool = True) -> bool:
        """输入文本"""
        try:
            self.device.text(text, enter)
            return True
        except Exception as e:
            print(f"输入文本失败: {str(e)}")
            return False

    def sleep(self, secs: float = 1.0) -> None:
        """等待指定时间"""
        time.sleep(secs)

    def wait(self, v: Union[tuple, list, str], timeout: float = 20, interval: float = 0.5, **kwargs) -> bool:
        """等待元素出现"""
        try:
            return self.device.wait(v, timeout, interval, **kwargs)
        except Exception as e:
            print(f"等待元素失败: {str(e)}")
            return False

    def exists(self, v: Union[tuple, list, str]) -> bool:
        """判断元素是否存在"""
        try:
            return self.device.exists(v)
        except Exception as e:
            print(f"检查元素存在失败: {str(e)}")
            return False

    def find_all(self, v: Union[tuple, list, str]) -> List:
        """查找所有匹配的元素"""
        try:
            return self.device.find_all(v)
        except Exception as e:
            print(f"查找元素失败: {str(e)}")
            return []

    def get_clipboard(self) -> str:
        """获取剪贴板内容"""
        try:
            return self.device.get_clipboard()
        except Exception as e:
            print(f"获取剪贴板失败: {str(e)}")
            return ""

    def set_clipboard(self, content: str) -> bool:
        """设置剪贴板内容"""
        try:
            self.device.set_clipboard(content)
            return True
        except Exception as e:
            print(f"设置剪贴板失败: {str(e)}")
            return False

    def shell(self, cmd: str) -> str:
        """执行shell命令"""
        try:
            return self.device.shell(cmd)
        except Exception as e:
            print(f"执行shell命令失败: {str(e)}")
            return ""

    def paste(self, text: str, enter: bool = True) -> bool:
        """
        粘贴文本（通常用于处理包含特殊字符的文本）
        
        Args:
            text: 要粘贴的文本
            enter: 是否在末尾发送回车键
        """
        try:
            self.device.paste(text, enter)
            return True
        except Exception as e:
            print(f"粘贴文本失败: {str(e)}")
            return False

    def push(self, src: str, dst: str) -> bool:
        """
        推送文件到设备
        
        Args:
            src: 本地文件路径
            dst: 设备上的目标路径
        """
        try:
            self.device.push(src, dst)
            return True
        except Exception as e:
            print(f"推送文件失败: {str(e)}")
            return False

    def pull(self, src: str, dst: str) -> bool:
        """
        从设备拉取文件
        
        Args:
            src: 设备上的文件路径
            dst: 本地目标路径
        """
        try:
            self.device.pull(src, dst)
            return True
        except Exception as e:
            print(f"拉取文件失败: {str(e)}")
            return False