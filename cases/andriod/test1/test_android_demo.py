#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Android平台测试用例示例
展示如何使用框架进行Android自动化测试
"""

import allure
import pytest
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report, LogToHtml
from datetime import datetime
from utils.logger import setup_logger
from core.base import BaseTest
from core.andriod import get_device_info, get_installed_apps, get_current_activity

# 设置日志
logger = setup_logger(__name__)


@allure.feature("Android基础功能测试")
class TestAndroidBasic:
    
    def setup_method(self):
        """每个测试方法开始前执行"""
        self.android_test = BaseTest(platform="Android")
        logger.info("Android测试环境初始化完成")
    
    @allure.story("设备信息获取")
    def test_get_device_info(self, setup_test):
        """测试获取Android设备信息"""
        logger.info("开始测试获取设备信息")
        
        try:
            # 获取设备信息
            device_info = get_device_info()
            
            # 验证设备信息
            assert device_info, "设备信息获取失败"
            assert 'device_id' in device_info, "设备ID缺失"
            assert 'android_version' in device_info, "Android版本信息缺失"
            
            logger.info(f"设备信息: {device_info}")
            
            # 添加到Allure报告
            allure.attach(
                str(device_info),
                name="设备信息",
                attachment_type=allure.attachment_type.TEXT
            )
            
        except Exception as e:
            logger.error(f"获取设备信息失败: {str(e)}")
            raise
    
    @allure.story("应用列表获取")
    def test_get_installed_apps(self, setup_test):
        """测试获取已安装应用列表"""
        logger.info("开始测试获取已安装应用")
        
        try:
            # 获取已安装应用
            apps = get_installed_apps()
            
            # 验证应用列表
            assert isinstance(apps, list), "应用列表类型错误"
            assert len(apps) > 0, "未找到已安装应用"
            
            logger.info(f"已安装应用数量: {len(apps)}")
            logger.info(f"前5个应用: {apps[:5]}")
            
            # 添加到Allure报告
            allure.attach(
                "\n".join(apps[:10]),  # 只显示前10个应用
                name="已安装应用列表(前10个)",
                attachment_type=allure.attachment_type.TEXT
            )
            
        except Exception as e:
            logger.error(f"获取应用列表失败: {str(e)}")
            raise
    
    @allure.story("基础操作测试")
    def test_basic_operations(self, setup_test):
        """测试Android基础操作"""
        logger.info("开始测试Android基础操作")
        
        try:
            # 截图
            screenshot_path = self.android_test.snapshot("test_screenshot.png")
            assert screenshot_path, "截图失败"
            logger.info(f"截图成功: {screenshot_path}")
            
            # 回到主页
            home_result = self.android_test.home()
            assert home_result, "回到主页失败"
            logger.info("回到主页成功")
            
            # 等待2秒
            self.android_test.sleep(2)
            
            # 获取当前Activity
            current_activity = get_current_activity()
            logger.info(f"当前Activity: {current_activity}")
            
            # 再次截图对比
            screenshot_path2 = self.android_test.snapshot("test_screenshot_after_home.png")
            assert screenshot_path2, "第二次截图失败"
            
        except Exception as e:
            logger.error(f"基础操作测试失败: {str(e)}")
            raise
    
    @allure.story("应用启动测试")
    @pytest.mark.parametrize("package_name", [
        "com.android.settings",  # 系统设置
        "com.android.calculator2",  # 计算器（如果存在）
    ])
    def test_app_launch(self, setup_test, package_name):
        """测试应用启动功能"""
        logger.info(f"开始测试启动应用: {package_name}")
        
        try:
            # 检查应用是否已安装
            installed_apps = get_installed_apps()
            if package_name not in installed_apps:
                pytest.skip(f"应用 {package_name} 未安装，跳过测试")
            
            # 启动应用
            start_result = self.android_test.start_app(package_name)
            assert start_result, f"启动应用 {package_name} 失败"
            
            # 等待应用启动
            self.android_test.sleep(3)
            
            # 截图验证
            screenshot_path = self.android_test.snapshot(f"app_launch_{package_name.split('.')[-1]}.png")
            assert screenshot_path, "启动后截图失败"
            
            # 获取当前Activity验证
            current_activity = get_current_activity()
            logger.info(f"启动后当前Activity: {current_activity}")
            
            # 停止应用
            stop_result = self.android_test.stop_app(package_name)
            assert stop_result, f"停止应用 {package_name} 失败"
            
            logger.info(f"应用 {package_name} 启动测试完成")
            
        except Exception as e:
            logger.error(f"应用启动测试失败: {str(e)}")
            raise
    
    def teardown_method(self):
        """每个测试方法结束后执行"""
        try:
            # 回到主页
            self.android_test.home()
            logger.info("测试清理完成")
        except Exception as e:
            logger.error(f"测试清理失败: {str(e)}")


@allure.feature("Android手势操作测试")
def test_gesture_operations(setup_test):
    """测试Android手势操作"""
    logger.info("开始测试Android手势操作")
    
    try:
        android_test = BaseTest(platform="Android")
        
        # 回到主页
        android_test.home()
        android_test.sleep(2)
        
        # 截图获取屏幕尺寸信息
        android_test.snapshot("gesture_test_start.png")
        
        # 获取屏幕尺寸（这里使用固定值，实际可以通过device获取）
        screen_width = 1080
        screen_height = 1920
        
        # 测试滑动操作：从下往上滑动
        start_point = (screen_width // 2, screen_height * 3 // 4)
        end_point = (screen_width // 2, screen_height // 4)
        
        swipe_result = android_test.swipe(start_point, end_point)
        assert swipe_result, "滑动操作失败"
        logger.info("向上滑动成功")
        
        android_test.sleep(2)
        android_test.snapshot("gesture_test_after_swipe.png")
        
        # 测试点击操作：点击屏幕中央
        center_point = (screen_width // 2, screen_height // 2)
        touch_result = android_test.touch(center_point)
        assert touch_result, "点击操作失败"
        logger.info("点击屏幕中央成功")
        
        android_test.sleep(1)
        android_test.snapshot("gesture_test_after_touch.png")
        
    except Exception as e:
        logger.error(f"手势操作测试失败: {str(e)}")
        raise
    finally:
        # 生成测试报告
        generate_test_report(__file__)


def generate_test_report(test_file):
    """生成测试报告"""
    try:
        # 获取时间戳和脚本名
        now = os.environ.get('TEST_TIMESTAMP', datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
        script_name = os.path.splitext(os.path.basename(test_file))[0]
        
        # 构建日志和导出路径
        log_root = os.path.join(os.path.dirname(test_file), 'log', script_name)
        export_dir = os.path.join("./export_dir", f"{script_name}.py", now)
        
        # 生成报告
        tmp = LogToHtml(
            script_root=test_file,
            log_root=log_root,
            export_dir=export_dir,
            lang='zh',
            plugins=None
        )
        tmp.report()
        logger.info(f"测试报告生成完成: {script_name}")
        
    except Exception as e:
        logger.error(f"生成测试报告失败: {str(e)}")


if __name__ == "__main__":
    # 单独运行此脚本时的调试代码
    print("Android测试用例模块")
    print("使用 pytest 运行: pytest cases/andriod/test1/test_android_demo.py -v")