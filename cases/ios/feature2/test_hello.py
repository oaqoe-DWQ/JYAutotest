# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

import allure
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report,LogToHtml
from datetime import datetime
from utils.logger import setup_logger
import os 


# 设置日志
logger = setup_logger(__name__)

@allure.feature("im通信功能-feature2")
@allure.story("通讯录中搜索一个人，然后给他发送一条消息-story")
@allure.title("test_hello-title")
@allure.testcase("这里指向测试用例地址-testcase-https://www.baidu.com")
@allure.issue("这里指向bug地址-issue-https://www.baidu.com")
@allure.description("这里是对用例的描述-description")
@allure.severity(allure.severity_level.BLOCKER)
def test_hello(setup_test):
    logger.info(f"开始执行用例: {os.path.basename(__file__)}")

    try:
        # script content
        keyevent("HOME")
        with allure.step("点击桌面app图标"):
            touch(Template(r"./images/tpl1735555105458.png", record_pos=(-0.11, 0.214), resolution=(1242, 2688)))
            sleep(2)

        with allure.step("点击app内消息图标"):
            touch(Template(r"./images/tpl1735555141044.png", record_pos=(-0.393, 0.939), resolution=(1242, 2688)))
            sleep(2)

        with allure.step("点击app内右上角搜索图标"):
            touch(Template(r"./images/tpl1735555159076.png", record_pos=(0.332, -0.92), resolution=(1242, 2688)))
            sleep(2)

        with allure.step("输入人名搜索"):
            text("张国栋")
            sleep(2)

        with allure.step("等待搜索结果出现"):
            wait(Template(r"./images/tpl1735555209082.png", record_pos=(-0.085, -0.452), resolution=(1242, 2688)))

        with allure.step("点击搜索结果"):
            touch(Template(r"./images/tpl1735555215942.png", record_pos=(-0.249, -0.465), resolution=(1242, 2688)))
            sleep(2)

        with allure.step("点击消息框获取输入焦点"):
            touch(Template(r"./images/tpl1735555237908.png", record_pos=(-0.05, 0.94), resolution=(1242, 2688)))
        
        with allure.step("输入消息内容"):
            text("hello")
            sleep(2)

        with allure.step("点击发送按钮"):
            touch(Template(r"./images/tpl1735555268161.png", record_pos=(0.375, 0.834), resolution=(1242, 2688)))

        with allure.step("点击返回按钮箭头"):
            touch(Template(r"./images/tpl1735555278609.png", record_pos=(-0.434, -0.929), resolution=(1242, 2688)))

        with allure.step("点击取消按钮"):
            touch(Template(r"./images/tpl1735555288524.png", record_pos=(0.422, -0.935), resolution=(1242, 2688)))

        keyevent("HOME")

    except Exception as e:
        raise Exception("脚本执行错误，退出")
    finally:
        # 获取时间戳和脚本名
        now = os.environ.get('TEST_TIMESTAMP', datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        
        # 构建日志和导出路径
        log_root = os.path.join(os.path.dirname(__file__), 'log', script_name)
        export_dir = os.path.join("./export_dir", f"{script_name}.py", now)
        logger.info(f"export_dir: {export_dir}")
        
        # 生成报告
        tmp = LogToHtml(
            script_root=__file__,
            log_root=log_root,
            export_dir=export_dir,
            lang='en',
            plugins=None
        )
        tmp.report()
        logger.info(f"用例执行完成: {script_name}")

#NOTE:如果想以纯python的方式调试该单个脚本，请添加下面的内容
# if __name__ == "__main__":
#     test_hello()