# JYAutotest - 跨平台UI自动化测试框架

🚀 基于Airtest的多平台UI自动化测试框架，支持Android、iOS、Windows、macOS等多个平台的自动化测试。

## ✨ 特性

- 🔄 **跨平台支持**: 支持Android、iOS、Windows、macOS等多个平台
- 🎯 **统一接口**: 通过BaseTest基类提供统一的操作接口
- 📱 **设备管理**: 自动设备检测、连接和管理
- 📊 **报告生成**: 集成pytest和Allure，生成美观的测试报告
- 🔧 **环境检查**: 内置环境检查工具，确保测试环境就绪
- 📸 **图像识别**: 基于Airtest的图像识别和Poco控件操作
- 🛠️ **扩展功能**: 弹窗处理、应用管理、权限控制等实用功能

## 🏗️ 项目结构

```
JYAutotest/
├── cases/                    # 测试用例
│   ├── android/             # Android测试用例
│   ├── ios/                 # iOS测试用例
│   ├── windows/             # Windows测试用例
│   └── macos/               # macOS测试用例
├── core/                    # 核心功能模块
│   ├── base.py             # 基类封装
│   ├── android.py          # Android特定功能
│   ├── ios.py              # iOS特定功能
│   ├── win.py              # Windows特定功能
│   └── popup_handler.py    # 弹窗处理
├── utils/                   # 工具类
│   ├── device_manager.py   # 设备管理
│   ├── logger.py           # 日志管理
│   └── installer.py        # 应用安装
├── config.py               # 配置文件
├── conftest.py             # pytest配置
├── check_android_env.py    # Android环境检查
└── requirements.txt        # 依赖包
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.7+
- Android SDK (Android测试)
- Xcode命令行工具 (iOS测试)
- WebDriverAgent (iOS测试)

### 2. 安装依赖

```bash
# 克隆项目
git clone https://github.com/oaqoe-DWQ/JYAutotest.git
cd JYAutotest

# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 3. 环境检查

#### Android环境检查
```bash
python check_android_env.py
```

#### 验证安装
```bash
python -c "import airtest; print(airtest.__version__)"
```

### 4. 运行测试

#### 运行单个测试
```bash
# Android测试
pytest cases/android/test1/test_android_demo.py -v

# iOS测试
pytest cases/ios/feature1/test_home.py -v
```

#### 运行所有测试
```bash
pytest cases/ -v
```

#### 生成Allure报告
```bash
# 生成报告数据
pytest cases/android/ --alluredir=allure_result

# 启动报告服务
allure serve allure_result
```

## 📱 平台支持

### Android
- ✅ 设备信息获取
- ✅ 应用管理（启动、停止、安装、卸载）
- ✅ 权限管理
- ✅ 内存监控
- ✅ 网络控制
- ✅ ADB连接管理

### iOS
- ✅ WebDriverAgent集成
- ✅ iOS 17+支持
- ✅ 应用启动管理
- ✅ 设备信息获取

### Windows
- ✅ 基础框架支持
- 🚧 功能扩展中

### macOS
- ✅ 基础框架支持
- 🚧 功能扩展中

## 🔧 使用示例

### 基础用法

```python
from core.base import BaseTest

# 初始化测试（自动识别平台）
android_test = BaseTest(platform="Android")
ios_test = BaseTest(platform="iOS")

# 基础操作
android_test.start_app("com.example.app")
android_test.touch((100, 200))
android_test.swipe((100, 200), (300, 400))
android_test.snapshot("screenshot.png")
```

### Android特定功能

```python
from core.android import get_device_info, get_installed_apps

# 获取设备信息
device_info = get_device_info()
print(f"设备信息: {device_info}")

# 获取已安装应用
apps = get_installed_apps()
print(f"已安装应用: {len(apps)} 个")
```

### 测试用例示例

```python
import pytest
import allure
from core.base import BaseTest

class TestAndroidApp:
    def setup_method(self):
        self.test = BaseTest(platform="Android")
    
    @allure.story("应用启动测试")
    def test_app_launch(self):
        assert self.test.start_app("com.example.app")
        self.test.sleep(3)
        assert self.test.exists("应用主界面标志")
```

## 🔍 环境配置

### Android配置

1. **安装Android SDK**
   ```bash
   # 下载Android Studio或单独安装SDK Platform Tools
   # 配置环境变量
   export ANDROID_HOME=/path/to/android-sdk
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```

2. **设备配置**
   - 启用开发者选项
   - 开启USB调试
   - 信任调试计算机

3. **验证连接**
   ```bash
   adb devices
   ```

### iOS配置

1. **安装依赖**
   ```bash
   # 安装tidevice
   pip install tidevice
   
   # 安装facebook-wda
   pip install facebook-wda
   ```

2. **WebDriverAgent配置**
   - 下载并构建WebDriverAgent
   - 配置开发者证书
   - 部署到iOS设备

## 📊 测试报告

框架集成了Allure报告系统，提供：

- 📈 详细的测试执行报告
- 📸 自动截图附件
- 📋 测试步骤追踪
- 🔗 失败用例分析
- 📊 统计图表展示

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 作者: oaqoe-DWQ
- 项目链接: https://github.com/oaqoe-DWQ/JYAutotest

## 🙏 致谢

- [Airtest](https://github.com/AirtestProject/Airtest) - 强大的自动化测试框架
- [pytest](https://docs.pytest.org/) - 优秀的Python测试框架
- [Allure](https://docs.qameta.io/allure/) - 美观的测试报告工具

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！