#!/usr/bin/env python3
"""
盲水印工具 - Blind Watermark Tool
主入口文件
"""
import sys
import os

# 添加父目录到路径，以便导入 blind_watermark 模块
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 抑制 OpenCV 的警告信息
os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

from app import BlindWatermarkGUI


def main():
    """主函数"""
    app = BlindWatermarkGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
