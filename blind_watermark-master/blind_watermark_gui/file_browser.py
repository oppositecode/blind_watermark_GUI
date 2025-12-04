"""文件浏览对话框模块"""
from tkinter import filedialog


def browse_image(title="选择图片"):
    """浏览图片文件
    
    Args:
        title: 对话框标题
        
    Returns:
        str: 选择的文件路径，未选择返回空字符串
    """
    return filedialog.askopenfilename(
        title=title,
        filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.bmp")]
    ) or ""


def browse_original_img():
    """选择原图"""
    return browse_image("选择原图")


def browse_watermark_img():
    """选择水印图片"""
    return browse_image("选择水印图片")


def browse_watermarked_img():
    """选择带水印图片"""
    return browse_image("选择带水印图片")


def save_output_img():
    """保存输出图片
    
    Returns:
        str: 选择的文件路径
    """
    return filedialog.asksaveasfilename(
        title="保存输出图片",
        defaultextension=".png",
        filetypes=[("PNG文件", "*.png"), ("JPG文件", "*.jpg")]
    ) or ""


def save_extract_output(mode):
    """保存提取结果
    
    Args:
        mode: 水印类型 ('img', 'str', 'bit')
        
    Returns:
        str: 选择的文件路径
    """
    if mode == "img":
        return filedialog.asksaveasfilename(
            title="保存提取的水印图片",
            defaultextension=".png",
            filetypes=[("图片文件", "*.png;*.jpg")]
        ) or ""
    else:
        return filedialog.asksaveasfilename(
            title="保存提取结果",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt")]
        ) or ""


def browse_background_img():
    """选择背景图片
    
    Returns:
        str: 选择的文件路径
    """
    return filedialog.askopenfilename(
        title="选择背景图片",
        filetypes=[
            ("图片文件", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.webp"),
            ("所有文件", "*.*")
        ]
    ) or ""
