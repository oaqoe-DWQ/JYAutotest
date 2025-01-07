from airtest.core.api import *
from config import DEVICE_CONFIG
from utils.logger import setup_logger
from airtest.cli.parser import cli_setup


logger = setup_logger(__name__)

class DeviceManager:
    @staticmethod
    def init_device(test_file, log_dir):
        """初始化设备并设置日志目录"""
        try:
            if not cli_setup():
                auto_setup(
                    test_file,
                    logdir=log_dir,
                    devices=[DEVICE_CONFIG['IOS']['uri']]
                )
            logger.info("设备初始化成功")
        except Exception as e:
            logger.error(f"设备初始化失败: {str(e)}")
            raise

    @staticmethod
    def disconnect():
        """断开设备连接"""
        try:
            # 获取当前设备
            current_device = device()
            if current_device:
                # 使用 airtest 的 device 实例方法断开连接
                current_device.disconnect()
                logger.info("设备已断开连接")
            else:
                logger.warning("没有找到已连接的设备")
        except Exception as e:
            logger.error(f"断开设备失败: {str(e)}") 