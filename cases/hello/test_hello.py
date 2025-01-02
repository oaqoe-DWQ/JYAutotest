# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

import allure
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report,LogToHtml

# if not cli_setup():
#     auto_setup(__file__, logdir=True, devices=["ios:///http://127.0.0.1:8100",])
# import os
# print("当前工作目录:", os.getcwd())

@allure.feature("测试发送hello消息")
def test_hello():
    try:
        # script content
        print("start testing...")
        import os
        print("11111")
        print(os.getcwd())

        keyevent("HOME")
        touch(Template(r"cases/hello/tpl1735555105458.png", record_pos=(-0.11, 0.214), resolution=(1242, 2688)))
        sleep(2)


        touch(Template(r"cases/hello/tpl1735555141044.png", record_pos=(-0.393, 0.939), resolution=(1242, 2688)))
        sleep(2)

        touch(Template(r"cases/hello/tpl1735555159076.png", record_pos=(0.332, -0.92), resolution=(1242, 2688)))
        sleep(2)

        text("张国栋")
        sleep(2)

        wait(Template(r"cases/hello/tpl1735555209082.png", record_pos=(-0.085, -0.452), resolution=(1242, 2688)))
        touch(Template(r"cases/hello/tpl1735555215942.png", record_pos=(-0.249, -0.465), resolution=(1242, 2688)))
        sleep(2)

        touch(Template(r"cases/hello/tpl1735555237908.png", record_pos=(-0.05, 0.94), resolution=(1242, 2688)))
        text("hello")
        sleep(2)
        touch(Template(r"cases/hello/tpl1735555268161.png", record_pos=(0.375, 0.834), resolution=(1242, 2688)))


        touch(Template(r"cases/hello/tpl1735555278609.png", record_pos=(-0.434, -0.929), resolution=(1242, 2688)))
        touch(Template(r"cases/hello/tpl1735555288524.png", record_pos=(0.422, -0.935), resolution=(1242, 2688)))


        keyevent("HOME")

    except Exception as e:
        raise Exception("脚本执行错误，退出")
    finally:
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        current_file_name = os.path.basename(__file__)
        report_path_name = now + '_' + current_file_name
        log_root = os.path.join(os.path.dirname(__file__), 'log')
        export_dir = os.path.join("./export_dir", current_file_name, now)
        tmp = LogToHtml(script_root=__file__, log_root=log_root, export_dir=export_dir,
                        lang='en',
                        plugins=None)
        # tmp.home(output_file=log_root + "result.html")
        tmp.report()

#NOTE:如果想以纯python的方式调试该单个脚本，请添加下面的内容
# if __name__ == "__main__":
#     if not cli_setup():
#         auto_setup(__file__, logdir=True, devices=["iOS:///http://127.0.0.1:8100", ])
