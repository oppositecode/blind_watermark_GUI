# 盲水印工具 GUI - Blind Watermark GUI

基于 CustomTkinter 的现代化盲水印嵌入与提取图形界面工具。

## 功能特性

-  **现代化 UI 界面** - 基于 CustomTkinter 的美观界面
-  **支持自定义背景图片** - 可设置应用背景图片
-  **双重密码保护** - 图片密码 + 水印密码双重加密
-  **多种水印类型** - 支持文本、图片、二进制水印
-  **主题切换** - 支持深色/浅色主题
-  **抗攻击性强** - 可抵抗截图、压缩、裁剪等攻击

## 环境要求

- Python 3.8+
- Windows / macOS / Linux

## 依赖安装

```bash
pip install customtkinter
pip install opencv-python
pip install numpy
pip install Pillow
pip install PyWavelets
```

或使用项目根目录的 requirements.txt：

```bash
pip install -r ../requirements.txt
```

### 依赖说明

| 依赖包          | 版本要求 | 说明                     |
| --------------- | -------- | ------------------------ |
| customtkinter   | 最新版   | 现代化 Tkinter UI 框架   |
| opencv-python   | 最新版   | 图像处理库               |
| numpy           | >=1.17.0 | 数值计算库               |
| Pillow          | 最新版   | Python 图像处理库        |
| PyWavelets      | 最新版   | 小波变换库（盲水印核心） |
| blind_watermark | 本地     | 盲水印核心库（父目录）   |

## 快速开始

### 运行方式

```bash
cd blind_watermark_gui
python main.py
```

或从项目根目录运行：

```bash
python blind_watermark_gui/main.py
```

### 使用流程

#### 嵌入水印
1. 点击侧边栏「嵌入水印」
2. 选择原图路径
3. 选择水印类型（文本/图片/二进制）
4. 输入水印内容或选择水印图片
5. 设置图片密码和水印密码
6. 选择输出路径
7. 点击「嵌入水印」按钮

#### 提取水印
1. 点击侧边栏「提取水印」
2. 选择带水印的图片
3. 选择水印类型
4. 输入水印形状/长度（嵌入时会提示）
5. 输入正确的图片密码和水印密码
6. 选择输出路径
7. 点击「提取水印」按钮

## 项目结构

```
blind_watermark_gui/
├── main.py              # 主入口文件
├── app.py               # 主应用类（BlindWatermarkGUI）
├── config.py            # 配置管理模块（加载/保存配置）
├── background.py        # 背景图片管理模块
├── components.py        # UI组件模块（侧边栏、导航、通用组件）
├── styles.py            # 样式配置模块（颜色、主题）
├── file_browser.py      # 文件浏览对话框模块
├── watermark_handler.py # 水印处理逻辑模块
├── README.md            # 开发文档
└── pages/               # 页面模块
    ├── __init__.py      # 页面模块导出
    ├── home.py          # 主页
    ├── embed.py         # 嵌入水印页面
    ├── extract.py       # 提取水印页面
    └── settings.py      # 设置页面（预留）
```

## 模块详细说明

### main.py - 程序入口

程序启动入口点，负责：
- 添加父目录到系统路径（以便导入 blind_watermark 模块）
- 抑制 OpenCV 警告信息
- 启动主应用

```python
from app import BlindWatermarkGUI

def main():
    app = BlindWatermarkGUI()
    app.mainloop()
```

### app.py - 主应用类

主应用类 `BlindWatermarkGUI`，继承自 `ctk.CTk`，负责：
- 窗口初始化（标题、尺寸、居中显示）
- 加载配置
- 初始化背景管理器
- 创建侧边栏和主内容区域
- 页面切换逻辑
- 主题切换

### config.py - 配置管理

配置文件管理模块：

```python
# 配置文件路径
CONFIG_FILE = "config.json"

# 主要函数
load_config()  # 加载配置，返回配置字典
save_config(config)  # 保存配置到文件

# 配置项
{
    "background_image": "",      # 背景图片路径
    "background_opacity": 0.3    # 背景透明度
}
```

### background.py - 背景管理器

背景图片管理器 `BackgroundManager` 类：

| 方法                            | 说明                             |
| ------------------------------- | -------------------------------- |
| `create_background()`           | 创建背景层                       |
| `load_background_image(path)`   | 加载背景图片                     |
| `update_background()`           | 更新背景（窗口大小变化时）       |
| `clear_background_image()`      | 清除背景图片                     |
| `choose_background_image()`     | 打开文件对话框选择背景           |
| `on_window_resize(event)`       | 窗口大小变化事件处理（带防抖动） |
| `update_preview_image()`        | 更新设置页面的预览图片           |
| `ensure_background_at_bottom()` | 确保背景在最底层                 |

### components.py - UI 组件

#### Sidebar 类 - 侧边栏

```python
class Sidebar:
    def __init__(self, root, show_page_callback, toggle_theme_callback):
        # 创建侧边栏、Logo、导航按钮、主题切换
    
    def update_nav_buttons(active_page):
        # 更新导航按钮激活状态
    
    def get_theme():
        # 获取当前主题
```

#### 通用组件函数

```python
create_section(parent, title, fields)
# 创建表单区域，fields 格式：[(label, variable, browse_command), ...]

create_feature_card(parent, title, description, button_text, command)
# 创建功能卡片
```

### styles.py - 样式配置

统一的颜色和样式定义：

```python
# 卡片背景色 (亮色模式, 深色模式)
CARD_BG_COLOR = ("#e8eef5", "#252538")
SECTION_BG = ("#e8eef5", "#252538")

# 侧边栏背景色
SIDEBAR_BG_COLOR = ("#1e3a5f", "#1a1a2e")

# 文本颜色
TEXT_PRIMARY = ("#1a202c", "#f7fafc")
TEXT_SECONDARY = ("#4a5568", "#a0aec0")

# 强调色
ACCENT_COLOR = ("#667eea", "#667eea")
```

### file_browser.py - 文件浏览

文件对话框封装：

| 函数                        | 说明           |
| --------------------------- | -------------- |
| `browse_original_img()`     | 选择原图       |
| `browse_watermark_img()`    | 选择水印图片   |
| `browse_watermarked_img()`  | 选择带水印图片 |
| `save_output_img()`         | 保存输出图片   |
| `save_extract_output(mode)` | 保存提取结果   |

### watermark_handler.py - 水印处理

水印嵌入和提取逻辑：

```python
embed_watermark(original_path, output_path, password_img, password_wm, 
                mode, watermark_content=None, watermark_img_path=None)
# 返回: (success, message, wm_length)

extract_watermark(img_path, output_path, password_img, password_wm, 
                  mode, wm_shape)
# 返回: (success, message, extracted_content)
```

### pages/ - 页面模块

#### home.py - 主页

```python
create_home_page(parent, show_page_callback)
# 创建主页：欢迎区域、功能卡片、特性说明
```

#### embed.py - 嵌入水印页面

```python
class EmbedPage:
    # 水印类型选择（文本/图片/二进制）
    # 原图选择、水印内容输入
    # 密码设置、输出路径
    # 嵌入操作

create_embed_page(parent, variables)
# 返回页面 Frame
```

#### extract.py - 提取水印页面

```python
class ExtractPage:
    # 带水印图片选择
    # 水印类型和形状参数
    # 密码设置、输出路径
    # 提取操作和结果显示

create_extract_page(parent, variables)
# 返回页面 Frame
```

## 开发指南

### 添加新页面

1. 在 `pages/` 目录创建新页面文件（如 `new_page.py`）
2. 创建页面类或函数：

```python
# pages/new_page.py
import customtkinter as ctk

def create_new_page(parent, **kwargs):
    page = ctk.CTkFrame(parent, fg_color="transparent")
    # 添加页面内容...
    return page
```

3. 在 `pages/__init__.py` 中导出：

```python
from .new_page import create_new_page
__all__ = [..., 'create_new_page']
```

4. 在 `app.py` 中添加页面创建和导航
5. 在 `components.py` 的 `_create_nav_buttons` 中添加导航按钮

### 修改样式

修改 `styles.py` 中的颜色定义即可全局生效。

### 添加新功能

水印处理逻辑放在 `watermark_handler.py`，UI 相关放在对应页面模块。

## 打包发布

使用 PyInstaller 打包：

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="盲水印工具" main.py
```

或使用项目根目录的 spec 文件：

```bash
pyinstaller ../blind_watermark_gui.spec
```

## 常见问题

### Q: 运行时提示 "No module named 'blind_watermark'"
A: 确保从项目根目录运行，或者安装 blind_watermark 包：
```bash
cd ..
pip install -e .
```

### Q: 背景图片不显示
A: 检查图片路径是否正确，支持的格式：jpg、jpeg、png、bmp、gif、webp

### Q: OpenCV 警告信息
A: 这是正常的，已在 main.py 中抑制。如果仍有警告，不影响功能使用。

## 版本历史

- v2.0 - 模块化重构，使用 CustomTkinter 现代化界面
- v1.0 - 初始版本

## License

MIT License
