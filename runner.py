# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

from launch import launch
import pytest
import os

if __name__ == '__main__':
    # 启动连接设备模块
    launch()


    # 生成报告路径
    #TODO修改成配置文件读取形式
    allure_report = "./allure_report"
    allure_result = "./allure_result"

    # # 运行pytest主运行程序
    # pytest.main(['-v'])
    # # os.system("allure generate %s -o %s --clean" % (allure_result, report_path))
    # os.system("allure generate %s -o %s --clean" % (allure_result, allure_report))
    # os.system('allure serve %s' % allure_report)

    pytest.main(['-v', '--alluredir', allure_result, '--clean-alluredir'])
    os.system("allure generate -c -o %s " % (allure_report))
    os.system('allure serve %s' % allure_result)
