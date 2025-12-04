"""设置页面模块"""
import customtkinter as ctk
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import SECTION_BG, SETTINGS_HEADER_BG, PREVIEW_CONTAINER_BG, TEXT_SECONDARY, ACCENT_COLOR


class SettingsPage:
    """设置页面"""
    
    def __init__(self, parent, config, background_manager, save_config_callback):
        """初始化设置页面
        
        Args:
            parent: 父容器
            config: 配置字典
            background_manager: 背景管理器实例
            save_config_callback: 保存配置的回调函数
        """
        self.parent = parent
        self.config = config
        self.bg_manager = background_manager
        self.save_config_callback = save_config_callback
        
        # 组件引用
        self.bg_path_var = None
        self.preview_label = None
        self.preview_container = None
        self.opacity_var = None
        self.opacity_slider = None
        self.opacity_value_label = None
        
        self.page = self._create()
        
        # 将预览组件引用传递给背景管理器
        self.bg_manager.preview_label = self.preview_label
        self.bg_manager.bg_path_var = self.bg_path_var
    
    def _create(self):
        """创建设置页面"""
        page = ctk.CTkFrame(self.parent, fg_color="transparent")
        
        # 页面标题
        self._create_header(page)
        
        # 背景图片设置区域
        self._create_bg_section(page)
        
        # 背景预览区域
        self._create_preview_section(page)
        
        # 透明度设置区域
        self._create_opacity_section(page)
        
        return page
    
    def _create_header(self, parent):
        """创建页面头部"""
        header = ctk.CTkFrame(parent, corner_radius=15, fg_color=SETTINGS_HEADER_BG)
        header.pack(fill="x", pady=(0, 20))
        
        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(padx=40, pady=30)
        
        title = ctk.CTkLabel(
            header_inner, 
            text="设置",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_inner, 
            text="自定义应用外观与个性化设置",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", pady=(10, 0))
    
    def _create_bg_section(self, parent):
        """创建背景图片设置区域"""
        section = ctk.CTkFrame(parent, corner_radius=15, fg_color=SECTION_BG)
        section.pack(fill="x", pady=(0, 20))
        
        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(padx=40, pady=30, fill="x")
        
        title = ctk.CTkLabel(
            inner, 
            text="背景图片",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(anchor="w")
        
        desc = ctk.CTkLabel(
            inner, 
            text="选择一张图片作为应用背景，支持高分辨率屏幕",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY
        )
        desc.pack(anchor="w", pady=(5, 15))
        
        # 当前背景路径显示
        path_frame = ctk.CTkFrame(inner, fg_color="transparent")
        path_frame.pack(fill="x", pady=(0, 15))
        
        path_label = ctk.CTkLabel(
            path_frame, 
            text="当前背景:",
            font=ctk.CTkFont(size=13)
        )
        path_label.pack(side="left")
        
        current_bg = self.bg_manager.bg_image_path if self.bg_manager.bg_image_path else "无"
        self.bg_path_var = ctk.StringVar(value=current_bg)
        
        self.bg_path_display = ctk.CTkLabel(
            path_frame, 
            textvariable=self.bg_path_var,
            font=ctk.CTkFont(size=12),
            text_color=ACCENT_COLOR,
            wraplength=400
        )
        self.bg_path_display.pack(side="left", padx=(10, 0), fill="x", expand=True)
        
        # 按钮区域
        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        choose_btn = ctk.CTkButton(
            btn_frame, 
            text="选择图片",
            font=ctk.CTkFont(size=14),
            width=140, 
            height=40,
            corner_radius=10,
            fg_color=("#667eea", "#667eea"),
            hover_color=("#5a6fd6", "#5a6fd6"),
            command=self.bg_manager.choose_background_image
        )
        choose_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            btn_frame, 
            text="清除背景",
            font=ctk.CTkFont(size=14),
            width=140, 
            height=40,
            corner_radius=10,
            fg_color=("#e53e3e", "#e53e3e"),
            hover_color=("#c53030", "#c53030"),
            command=self.bg_manager.clear_background_image
        )
        clear_btn.pack(side="left")
    
    def _create_preview_section(self, parent):
        """创建背景预览区域"""
        section = ctk.CTkFrame(parent, corner_radius=15, fg_color=SECTION_BG)
        section.pack(fill="both", expand=True)
        
        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(padx=40, pady=30, fill="both", expand=True)
        
        title = ctk.CTkLabel(
            inner, 
            text="背景预览",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(anchor="w")
        
        desc = ctk.CTkLabel(
            inner, 
            text="预览当前设置的背景图片效果",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY
        )
        desc.pack(anchor="w", pady=(5, 15))
        
        # 预览图片容器
        self.preview_container = ctk.CTkFrame(
            inner, 
            corner_radius=10,
            fg_color=PREVIEW_CONTAINER_BG,
            height=250
        )
        self.preview_container.pack(fill="both", expand=True)
        self.preview_container.pack_propagate(False)
        
        # 预览标签
        self.preview_label = ctk.CTkLabel(
            self.preview_container, 
            text="暂无背景图片",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_SECONDARY
        )
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # 如果已有背景图片，更新预览
        if self.config.get("background_image"):
            # 延迟更新预览
            self.parent.after(100, self.bg_manager.update_preview_image)
    
    def _create_opacity_section(self, parent):
        """创建透明度设置区域"""
        section = ctk.CTkFrame(parent, corner_radius=15, fg_color=SECTION_BG)
        section.pack(fill="x", pady=(20, 0))
        
        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(padx=40, pady=30, fill="x")
        
        title = ctk.CTkLabel(
            inner, 
            text="背景透明度",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(anchor="w")
        
        desc = ctk.CTkLabel(
            inner, 
            text="调整背景图片的透明度以确保内容可读性",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY
        )
        desc.pack(anchor="w", pady=(5, 15))
        
        # 透明度滑块
        slider_frame = ctk.CTkFrame(inner, fg_color="transparent")
        slider_frame.pack(fill="x")
        
        self.opacity_var = ctk.DoubleVar(value=self.config.get("background_opacity", 0.3))
        
        opacity_label = ctk.CTkLabel(
            slider_frame, 
            text="透明度:",
            font=ctk.CTkFont(size=13)
        )
        opacity_label.pack(side="left")
        
        self.opacity_slider = ctk.CTkSlider(
            slider_frame, 
            from_=0.1, 
            to=1.0,
            variable=self.opacity_var,
            width=300,
            command=self._on_opacity_change
        )
        self.opacity_slider.pack(side="left", padx=(15, 15))
        
        self.opacity_value_label = ctk.CTkLabel(
            slider_frame, 
            text=f"{self.opacity_var.get():.0%}",
            font=ctk.CTkFont(size=13),
            width=50
        )
        self.opacity_value_label.pack(side="left")
    
    def _on_opacity_change(self, value):
        """透明度变化回调"""
        self.opacity_value_label.configure(text=f"{value:.0%}")
        self.config["background_opacity"] = value
        self.save_config_callback()
        # 更新背景透明度
        if self.bg_manager.bg_image_original:
            self.bg_manager.update_background()


def create_settings_page(parent, config, background_manager, save_config_callback):
    """创建设置页面
    
    Args:
        parent: 父容器
        config: 配置字典
        background_manager: 背景管理器实例
        save_config_callback: 保存配置的回调函数
        
    Returns:
        page: 页面Frame
    """
    settings_page = SettingsPage(parent, config, background_manager, save_config_callback)
    return settings_page.page
