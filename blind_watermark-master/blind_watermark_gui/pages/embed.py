"""嵌入水印页面模块"""
import customtkinter as ctk
from tkinter import messagebox
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components import create_section
from file_browser import browse_original_img, browse_watermark_img, save_output_img
from watermark_handler import embed_watermark
from styles import SECTION_BG, TEXT_SECONDARY


class EmbedPage:
    """嵌入水印页面"""
    
    def __init__(self, parent, variables):
        """初始化嵌入页面
        
        Args:
            parent: 父容器
            variables: 变量字典，包含 original_img_path, watermark_content, 
                      watermark_img_path, output_img_path, password_img, password_wm
        """
        self.parent = parent
        self.variables = variables
        
        # 水印类型变量
        self.embed_type_var = ctk.StringVar(value="str")
        
        # 组件引用
        self.embed_text_frame = None
        self.embed_text_label = None
        self.embed_text_entry = None
        self.embed_img_frame = None
        self.embed_wm_content_frame = None
        
        self.page = self._create()
    
    def _create(self):
        """创建嵌入页面"""
        page = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        
        # 页面标题
        self._create_header(page)
        
        # 原图选择区域
        create_section(page, "选择原图", [
            ("原图路径:", self.variables['original_img_path'], self._browse_original)
        ])
        
        # 水印设置区域
        self._create_watermark_section(page)
        
        # 密码设置区域
        self._create_password_section(page)
        
        # 输出设置区域
        create_section(page, "输出设置", [
            ("输出路径:", self.variables['output_img_path'], self._browse_output)
        ])
        
        # 嵌入按钮
        self._create_embed_button(page)
        
        return page
    
    def _create_header(self, parent):
        """创建页面头部"""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header, 
            text="嵌入水印",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header, 
            text="将水印信息隐藏到图片中",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def _create_watermark_section(self, parent):
        """创建水印设置区域"""
        section = ctk.CTkFrame(parent, corner_radius=15, fg_color=SECTION_BG)
        section.pack(fill="x", pady=10)
        
        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(padx=25, pady=20, fill="x")
        
        section_title = ctk.CTkLabel(
            inner, 
            text="水印设置",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        section_title.pack(anchor="w", pady=(0, 15))
        
        # 水印类型选择
        type_frame = ctk.CTkFrame(inner, fg_color="transparent")
        type_frame.pack(fill="x", pady=(0, 15))
        
        type_label = ctk.CTkLabel(
            type_frame, 
            text="水印类型:",
            font=ctk.CTkFont(size=13)
        )
        type_label.pack(side="left", padx=(0, 15))
        
        for text, value in [("文本", "str"), ("图片", "img"), ("二进制", "bit")]:
            rb = ctk.CTkRadioButton(
                type_frame, 
                text=text, 
                variable=self.embed_type_var,
                value=value, 
                font=ctk.CTkFont(size=13),
                command=self._update_wm_input
            )
            rb.pack(side="left", padx=15)
        
        # 水印内容输入框架
        self.embed_wm_content_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.embed_wm_content_frame.pack(fill="x")
        
        # 文本/二进制输入
        self.embed_text_frame = ctk.CTkFrame(self.embed_wm_content_frame, fg_color="transparent")
        self.embed_text_label = ctk.CTkLabel(
            self.embed_text_frame, 
            text="水印文本:",
            font=ctk.CTkFont(size=13)
        )
        self.embed_text_label.pack(anchor="w")
        self.embed_text_entry = ctk.CTkEntry(
            self.embed_text_frame, 
            textvariable=self.variables['watermark_content'],
            height=40, 
            font=ctk.CTkFont(size=13)
        )
        self.embed_text_entry.pack(fill="x", pady=(5, 0))
        
        # 图片输入
        self.embed_img_frame = ctk.CTkFrame(self.embed_wm_content_frame, fg_color="transparent")
        img_label = ctk.CTkLabel(
            self.embed_img_frame, 
            text="水印图片:",
            font=ctk.CTkFont(size=13)
        )
        img_label.pack(anchor="w")
        
        img_input = ctk.CTkFrame(self.embed_img_frame, fg_color="transparent")
        img_input.pack(fill="x", pady=(5, 0))
        
        self.embed_img_entry = ctk.CTkEntry(
            img_input, 
            textvariable=self.variables['watermark_img_path'],
            height=40, 
            font=ctk.CTkFont(size=13)
        )
        self.embed_img_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        img_btn = ctk.CTkButton(
            img_input, 
            text="浏览", 
            width=100, 
            height=40,
            command=self._browse_watermark_img
        )
        img_btn.pack(side="right")
        
        # 初始化显示
        self._update_wm_input()
    
    def _create_password_section(self, parent):
        """创建密码设置区域"""
        section = ctk.CTkFrame(parent, corner_radius=15, fg_color=SECTION_BG)
        section.pack(fill="x", pady=10)
        
        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(padx=25, pady=20, fill="x")
        
        title = ctk.CTkLabel(
            inner, 
            text="安全设置",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(anchor="w", pady=(0, 15))
        
        grid = ctk.CTkFrame(inner, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1), weight=1)
        
        # 图片密码
        pwd_img_frame = ctk.CTkFrame(grid, fg_color="transparent")
        pwd_img_frame.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ctk.CTkLabel(pwd_img_frame, text="图片密码:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        ctk.CTkEntry(
            pwd_img_frame, 
            textvariable=self.variables['password_img'], 
            height=40,
            font=ctk.CTkFont(size=13)
        ).pack(fill="x", pady=(5, 0))
        
        # 水印密码
        pwd_wm_frame = ctk.CTkFrame(grid, fg_color="transparent")
        pwd_wm_frame.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        ctk.CTkLabel(pwd_wm_frame, text="水印密码:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        ctk.CTkEntry(
            pwd_wm_frame, 
            textvariable=self.variables['password_wm'], 
            height=40,
            font=ctk.CTkFont(size=13)
        ).pack(fill="x", pady=(5, 0))
    
    def _create_embed_button(self, parent):
        """创建嵌入按钮"""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)
        
        embed_btn = ctk.CTkButton(
            btn_frame, 
            text="嵌入水印",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50, 
            corner_radius=10,
            fg_color="#00b894", 
            hover_color="#00a085",
            command=self._do_embed
        )
        embed_btn.pack(pady=10)
    
    def _update_wm_input(self):
        """更新水印输入框显示"""
        mode = self.embed_type_var.get()
        
        for widget in self.embed_wm_content_frame.winfo_children():
            widget.pack_forget()
        
        if mode in ("str", "bit"):
            self.embed_text_frame.pack(fill="x")
            if mode == "str":
                self.embed_text_label.configure(text="水印文本:")
            else:
                self.embed_text_label.configure(text="二进制数据 (用逗号分隔0/1):")
        else:
            self.embed_img_frame.pack(fill="x")
    
    def _browse_original(self):
        """浏览原图"""
        path = browse_original_img()
        if path:
            self.variables['original_img_path'].set(path)
    
    def _browse_watermark_img(self):
        """浏览水印图片"""
        path = browse_watermark_img()
        if path:
            self.variables['watermark_img_path'].set(path)
    
    def _browse_output(self):
        """浏览输出路径"""
        path = save_output_img()
        if path:
            self.variables['output_img_path'].set(path)
    
    def _do_embed(self):
        """执行嵌入操作"""
        mode = self.embed_type_var.get()
        
        success, message, wm_length = embed_watermark(
            original_path=self.variables['original_img_path'].get(),
            output_path=self.variables['output_img_path'].get(),
            password_img=self.variables['password_img'].get(),
            password_wm=self.variables['password_wm'].get(),
            mode=mode,
            watermark_content=self.variables['watermark_content'].get(),
            watermark_img_path=self.variables['watermark_img_path'].get()
        )
        
        if success:
            if wm_length is not None:
                messagebox.showinfo("成功", f"{message}\n\n水印长度: {wm_length}\n\n提示: 提取时需使用此长度")
            else:
                messagebox.showinfo("成功", message)
        else:
            messagebox.showerror("错误", message)


def create_embed_page(parent, variables):
    """创建嵌入水印页面
    
    Args:
        parent: 父容器
        variables: 变量字典
        
    Returns:
        page: 页面Frame
    """
    embed_page = EmbedPage(parent, variables)
    return embed_page.page
