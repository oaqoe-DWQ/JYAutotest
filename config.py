import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Allure 相关配置
ALLURE_CONFIG = {
    'REPORT_DIR': os.path.join(BASE_DIR, "allure_report"),
    'RESULT_DIR': os.path.join(BASE_DIR, "allure_result"),
}

# Airtest 相关配置
AIRTEST_CONFIG = {
    'EXPORT_DIR': os.path.join(BASE_DIR, "export_dir"),
}

# 其他配置可以按需添加
LOG_CONFIG = {
    'LEVEL': 'INFO',
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
} 