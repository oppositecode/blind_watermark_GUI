"""UI组件模块 - 侧边栏、导航按钮等"""
import customtkinter as ctk
from styles import (
    CARD_BG_COLOR, SIDEBAR_BG_COLOR, FEATURE_CARD_BG, 
    SECTION_BG, TEXT_SECONDARY
)


class Sidebar:
    """侧边栏组件"""
    
    def __init__(self, root, show_page_callback, toggle_theme_callback):
        """初始化侧边栏
        
        Args:
            root: 父容器
            show_page_callback: 显示页面的回调函数
            toggle_theme_callback: 切换主题的回调函数
        """
        self.root = root
        self.show_page_callback = show_page_callback
        self.toggle_theme_callback = toggle_theme_callback
        self.nav_buttons = {}
        self.theme_switch = None
        self.sidebar = None
        
        self._create()
    
    def _create(self):
        """创建侧边栏"""
        self.sidebar = ctk.CTkFrame(
            self.root, 
            width=220, 
            corner_radius=0,
            fg_color=SIDEBAR_BG_COLOR,
            bg_color="transparent"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)
        self.sidebar.lift()
        
        self._create_logo()
        self._create_separator()
        self._create_nav_buttons()
        self._create_bottom_section()
    
    def _create_logo(self):
        """创建Logo区域"""
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(30, 10), sticky="ew")
        
        logo_label = ctk.CTkLabel(
            logo_frame, 
            text="BWM",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        logo_label.pack()
        
        title_label = ctk.CTkLabel(
            logo_frame, 
            text="盲水印工具",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=(5, 0))
        
        subtitle_label = ctk.CTkLabel(
            logo_frame, 
            text="Blind Watermark",
            font=ctk.CTkFont(size=11),
            text_color=("#a0c4e8", "#8090a0")
        )
        subtitle_label.pack()
    
    def _create_separator(self):
        """创建分割线"""
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color=("#3d5a80", "gray30"))
        separator.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
    
    def _create_nav_buttons(self):
        """创建导航按钮"""
        nav_items = [
            ("主页", "home", 2),
            ("嵌入水印", "embed", 3),
            ("提取水印", "extract", 4)
        ]
        
        for text, page_name, row in nav_items:
            self.nav_buttons[page_name] = self._create_nav_button(text, page_name, row)
    
    def _create_nav_button(self, text, page_name, row):
        """创建单个导航按钮"""
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            font=ctk.CTkFont(size=14),
            height=45,
            anchor="w",
            corner_radius=10,
            fg_color="transparent",
            text_color=("#e0e8f0", "#e0e8f0"),
            hover_color=("#2d4a6f", "#3d3d5c"),
            command=lambda: self.show_page_callback(page_name)
        )
        btn.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        return btn
    
    def _create_bottom_section(self):
        """创建底部区域"""
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.grid(row=11, column=0, padx=20, pady=20, sticky="sew")
        
        # 主题切换
        theme_label = ctk.CTkLabel(
            bottom_frame, 
            text="主题模式",
            font=ctk.CTkFont(size=12),
            text_color="white"
        )
        theme_label.pack(anchor="w")
        
        self.theme_switch = ctk.CTkSwitch(
            bottom_frame, 
            text="深色模式",
            command=self.toggle_theme_callback,
            onvalue="dark", 
            offvalue="light",
            text_color="white",
            progress_color=("#667eea", "#667eea")
        )
        self.theme_switch.pack(anchor="w", pady=(5, 15))
        self.theme_switch.select()  # 默认深色模式
        
        # 版本信息
        version_label = ctk.CTkLabel(
            bottom_frame, 
            text="v2.0 Modern UI",
            font=ctk.CTkFont(size=10),
            text_color=("#a0c4e8", "#8090a0")
        )
        version_label.pack(anchor="w")
    
    def update_nav_buttons(self, active_page):
        """更新导航按钮状态
        
        Args:
            active_page: 当前激活的页面名称
        """
        for page_name, btn in self.nav_buttons.items():
            if page_name == active_page:
                btn.configure(
                    fg_color=("#667eea", "#667eea"),
                    text_color="white"
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=("#e0e8f0", "#e0e8f0")
                )
    
    def get_theme(self):
        """获取当前主题"""
        return self.theme_switch.get() if self.theme_switch else "dark"


def create_section(parent, title, fields):
    """创建表单区域
    
    Args:
        parent: 父容器
        title: 区域标题
        fields: 字段列表 [(label_text, variable, browse_command), ...]
        
    Returns:
        section: 创建的区域Frame
    """
    section = ctk.CTkFrame(parent, corner_radius=15, fg_color=SECTION_BG)
    section.pack(fill="x", pady=10)
    
    inner = ctk.CTkFrame(section, fg_color="transparent")
    inner.pack(padx=25, pady=20, fill="x")
    
    section_title = ctk.CTkLabel(
        inner, 
        text=title,
        font=ctk.CTkFont(size=16, weight="bold")
    )
    section_title.pack(anchor="w", pady=(0, 15))
    
    for label_text, variable, browse_command in fields:
        field_frame = ctk.CTkFrame(inner, fg_color="transparent")
        field_frame.pack(fill="x", pady=(0, 10))
        
        label = ctk.CTkLabel(field_frame, text=label_text, font=ctk.CTkFont(size=13))
        label.pack(anchor="w")
        
        input_frame = ctk.CTkFrame(field_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=(5, 0))
        
        entry = ctk.CTkEntry(
            input_frame, 
            textvariable=variable, 
            height=40,
            font=ctk.CTkFont(size=13)
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn = ctk.CTkButton(
            input_frame, 
            text="浏览", 
            width=100, 
            height=40,
            command=browse_command
        )
        btn.pack(side="right")
    
    return section


def create_feature_card(parent, title, description, button_text, command):
    """创建功能卡片
    
    Args:
        parent: 父容器
        title: 卡片标题
        description: 卡片描述
        button_text: 按钮文字
        command: 按钮命令
        
    Returns:
        card: 创建的卡片Frame
    """
    card = ctk.CTkFrame(parent, corner_radius=15, fg_color=FEATURE_CARD_BG)
    
    inner = ctk.CTkFrame(card, fg_color="transparent")
    inner.pack(padx=30, pady=30, fill="both", expand=True)
    
    title_label = ctk.CTkLabel(
        inner, 
        text=title,
        font=ctk.CTkFont(size=20, weight="bold")
    )
    title_label.pack(pady=(20, 0))
    
    desc_label = ctk.CTkLabel(
        inner, 
        text=description,
        font=ctk.CTkFont(size=13),
        text_color=("#4a5568", "#a0aec0"),
        justify="center"
    )
    desc_label.pack(pady=(10, 25))
    
    btn = ctk.CTkButton(
        inner, 
        text=button_text,
        font=ctk.CTkFont(size=14, weight="bold"),
        height=40, 
        corner_radius=10,
        command=command
    )
    btn.pack()
    
    return card
