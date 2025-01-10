#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import sys
import os.path

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))

from utils.logger import setup_logger
from config import APP_DOWNLOAD_URL, BASE_DIR

# 设置日志
logger = setup_logger(__name__)

class IPADownloader:
    def __init__(self):
        self.base_url = APP_DOWNLOAD_URL['IPA_DOWNLOAD_URL']
        self.download_dir = os.path.join(BASE_DIR, 'pkgs')
        
        # 确保下载目录存在
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logger.info(f"创建下载目录: {self.download_dir}")

    def get_download_url(self, version):
        """获取指定版本的下载链接"""
        try:
            # 获取版本列表页面
            response = requests.get(self.base_url)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有链接
            links = soup.find_all('a')
            
            # 查找匹配版本号的HTML页面链接
            version_page_url = None
            for link in links:
                href = link.get('href', '')
                if version in href and href.endswith('.html'):
                    version_page_url = urljoin(self.base_url, href)
                    break
            
            if not version_page_url:
                raise ValueError(f"未找到版本 {version} 的页面")
            
            logger.info(f"找到版本页面: {version_page_url}")
            
            # 获取版本详情页面
            detail_response = requests.get(version_page_url)
            detail_response.raise_for_status()
            
            # 检查响应内容
            if not detail_response.text:
                raise ValueError("详情页面响应内容为空")
            
            logger.info(f"获取到详情页面内容长度: {len(detail_response.text)}")
            
            # 解析详情页面
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
            
            # 使用 CSS 选择器查找下载链接
            download_link = detail_soup.select_one('body > div.wrapper > div.qrCode > a.ipa')
            if not download_link:
                raise ValueError(f"在详情页面中未找到下载链接")
            
            download_url = download_link.get('href')
            logger.info(f"解析到的下载链接: {download_url}") 
            if not download_url:
                raise ValueError(f"下载链接为空")
            
            full_download_url = urljoin(version_page_url, download_url)
            logger.info(f"获取到下载链接: {full_download_url}")
            return full_download_url
            
        except requests.RequestException as e:
            logger.error(f"获取下载链接失败: {str(e)}")
            raise Exception(f"获取下载链接失败: {str(e)}")

    def download_ipa(self, version):
        """下载指定版本的IPA文件"""
        try:
            download_url = self.get_download_url(version)
            filename = os.path.join(self.download_dir, f"app_{version}.ipa")
            
            logger.info(f"开始下载版本 {version}")
            logger.info(f"下载地址: {download_url}")
            
            # 使用流式下载以处理大文件
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            
            # 下载文件并显示进度
            with open(filename, 'wb') as f:
                if total_size == 0:
                    f.write(response.content)
                else:
                    downloaded = 0
                    for data in response.iter_content(chunk_size=8192):
                        downloaded += len(data)
                        f.write(data)
                        # 计算下载进度
                        done = int(50 * downloaded / total_size)
                        print(f"\r下载进度: [{'=' * done}{' ' * (50-done)}] {downloaded}/{total_size} bytes", 
                              end='', flush=True)
            
            logger.info(f"下载完成: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"下载失败: {str(e)}")
            raise Exception(f"下载失败: {str(e)}")

def download_app(version):
    """便捷的下载函数"""
    downloader = IPADownloader()
    return downloader.download_ipa(version)

if __name__ == "__main__":
    # 示例使用
    try:
        version = "2.9.24.19848"
        version = "2.9.26.19736"
        downloaded_file = download_app(version)
        logger.info(f"文件已下载到: {downloaded_file}")
    except Exception as e:
        logger.error(f"错误: {str(e)}")


