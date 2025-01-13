#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
处理各种异常弹窗的装饰器
"""
__author__ = "zhangxiaoguo"

import time
import functools
from typing import Callable, Any
from utils.logger import logger


def handle_popup(popup_configs: list = None, timeout: float = 2.0, interval: float = 0.5, retry_times: int = 3):
    """
    处理弹窗的装饰器

    Args:
        popup_configs: 弹窗配置列表，每项包含 check(检查图片) 和 name(弹窗名称)
        timeout: 每次检查弹窗的超时时间
        interval: 重试间隔时间
        retry_times: 最大重试次数
    """
    # 默认弹窗配置
    default_configs = [
        {"check": "update_close.png", "name": "升级弹窗"},
        {"check": "ad_close.png", "name": "广告弹窗"},
        {"check": "allow_button.png", "name": "权限弹窗"}
    ]

    popup_configs = popup_configs or default_configs

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            result = func(self, *args, **kwargs)

            retry_count = 0
            while retry_count < retry_times:
                try:
                    start_time = time.time()
                    while time.time() - start_time < timeout:
                        for config in popup_configs:
                            if self.exists(config["check"]):
                                logger.info(f"检测到{config['name']}")
                                self.click(config["check"])
                                time.sleep(interval)

                except Exception as e:
                    logger.error(f"处理弹窗时发生错误: {str(e)}")
                    retry_count += 1
                    time.sleep(interval)
                    continue

                break

            return result

        return wrapper

    return decorator



# 示例
@handle_popup(popup_configs=[
    {"check": "custom_close.png", "name": "自定义弹窗"},
    {"check": "privacy_accept.png", "name": "隐私弹窗"}
])
def test_custom(self):
    """自定义弹窗处理测试"""
    self.click("some_button.png")