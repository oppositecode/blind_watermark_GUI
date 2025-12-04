"""主页模块"""
import customtkinter as ctk
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components import create_feature_card
from styles import WELCOME_BG, FEATURES_BG, TEXT_SECONDARY


def create_home_page(parent, show_page_callback):
    """创建主页
    
    Args:
        parent: 父容器
        show_page_callback: 显示页面的回调函数
        
    Returns:
        page: 主页Frame
    """
    page = ctk.CTkFrame(parent, fg_color="transparent")
    
    # 欢迎区域 - 使用半透明背景
    welcome_frame = ctk.CTkFrame(page, corner_radius=15, fg_color=WELCOME_BG)
    welcome_frame.pack(fill="x", pady=(0, 20))
    
    welcome_inner = ctk.CTkFrame(welcome_frame, fg_color="transparent")
    welcome_inner.pack(padx=40, pady=40)
    
    title = ctk.CTkLabel(
        welcome_inner, 
        text="欢迎使用盲水印工具",
        font=ctk.CTkFont(size=28, weight="bold")
    )
    title.pack(anchor="w")
    
    subtitle = ctk.CTkLabel(
        welcome_inner, 
        text="一款强大的隐形水印嵌入与提取工具，保护您的图片版权",
        font=ctk.CTkFont(size=14),
        text_color=TEXT_SECONDARY
    )
    subtitle.pack(anchor="w", pady=(10, 0))
    
    # 功能卡片区域
    cards_frame = ctk.CTkFrame(page, fg_color="transparent")
    cards_frame.pack(fill="both", expand=True)
    cards_frame.grid_columnconfigure((0, 1), weight=1)
    cards_frame.grid_rowconfigure(0, weight=1)
    
    # 嵌入水印卡片
    embed_card = create_feature_card(
        cards_frame,
        title="嵌入水印",
        description="将文本、图片或二进制数据\n隐藏到图片中",
        button_text="开始嵌入",
        command=lambda: show_page_callback("embed")
    )
    embed_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
    
    # 提取水印卡片
    extract_card = create_feature_card(
        cards_frame,
        title="提取水印",
        description="从带水印的图片中\n提取隐藏的信息",
        button_text="开始提取",
        command=lambda: show_page_callback("extract")
    )
    extract_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
    
    # 特性说明 - 使用半透明背景
    features_frame = ctk.CTkFrame(page, corner_radius=15, fg_color=FEATURES_BG)
    features_frame.pack(fill="x", pady=(20, 0))
    
    features_inner = ctk.CTkFrame(features_frame, fg_color="transparent")
    features_inner.pack(padx=30, pady=25)
    
    features_title = ctk.CTkLabel(
        features_inner, 
        text="主要特性",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    features_title.pack(anchor="w", pady=(0, 15))
    
    features = [
        "抗攻击性强：支持抵抗截图、压缩、裁剪等攻击",
        "双重密码保护：图片密码 + 水印密码双重加密",
        "多种水印类型：支持文本、图片、二进制数据",
        "操作简便：直观的图形界面，一键完成操作"
    ]
    
    for feature in features:
        feat_label = ctk.CTkLabel(
            features_inner, 
            text=feature,
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        feat_label.pack(anchor="w", pady=3)
    
    return page
