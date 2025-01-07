# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

import allure
import pytest
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report,LogToHtml
from datetime import datetime
from utils.logger import setup_logger

# 设置日志
logger = setup_logger(__name__)


@allure.feature("测试HOME快捷键")
def test_home(setup_test):
    # if not cli_setup():
    #     auto_setup(__file__, logdir=True, devices=["iOS:///http://127.0.0.1:8100"])
    
    logger.info(f"开始执行用例: {os.path.basename(__file__)}")
    try:
        keyevent("HOME")
        touch(Template(r"./images/tpl1735555105458.png", record_pos=(-0.11, 0.214), resolution=(1242, 2688)))
        sleep(2)
        keyevent("HOME")
    except Exception as e:
        raise Exception("脚本执行错误，退出")
    finally:
        # 获取时间戳和脚本名
        now = os.environ.get('TEST_TIMESTAMP', datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        
        # 构建日志和导出路径
        log_root = os.path.join(os.path.dirname(__file__), 'log', script_name)
        export_dir = os.path.join("./export_dir", script_name, now)
        
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
#     # if not cli_setup():
#     #     auto_setup(__file__, logdir=True, devices=["iOS:///http://127.0.0.1:8100"])
#     test_home()