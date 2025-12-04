"""提取水印页面模块"""
import customtkinter as ctk
from tkinter import messagebox
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components import create_section
from file_browser import browse_watermarked_img, save_extract_output
from watermark_handler import extract_watermark
from styles import SECTION_BG, TEXT_SECONDARY


class ExtractPage:
    """提取水印页面"""
    
    def __init__(self, parent, variables):
        """初始化提取页面
        
        Args:
            parent: 父容器
            variables: 变量字典，包含 original_img_path, output_img_path, 
                      password_img, password_wm, wm_shape
        """
        self.parent = parent
        self.variables = variables
        
        # 水印类型变量
        self.extract_type_var = ctk.StringVar(value="str")
        
        # 结果显示组件
        self.extract_result = None
        
        self.page = self._create()
    
    def _create(self):
        """创建提取页面"""
        page = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        
        # 页面标题
        self._create_header(page)
        
        # 图片选择区域
        create_section(page, "选择带水印图片", [
            ("图片路径:", self.variables['original_img_path'], self._browse_watermarked)
        ])
        
        # 水印参数区域
        self._create_param_section(page)
        
        # 密码设置区域
        self._create_password_section(page)
        
        # 输出设置区域
        create_section(page, "输出设置", [
            ("结果路径:", self.variables['output_img_path'], self._browse_output)
        ])
        
        # 提取按钮
        self._create_extract_button(page)
        
        # 结果显示区域
        self._create_result_section(page)
        
        return page
    
    def _create_header(self, parent):
        """创建页面头部"""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header, 
            text="提取水印",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header, 
            text="从带水印的图片中提取隐藏信息",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", pady=(5, 0))
    
    def _create_param_section(self, parent):
        """创建水印参数区域"""
        section = ctk.CTkFrame(parent, corner_radius=15, fg_color=SECTION_BG)
        section.pack(fill="x", pady=10)
        
        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(padx=25, pady=20, fill="x")
        
        title = ctk.CTkLabel(
            inner, 
            text="水印参数",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(anchor="w", pady=(0, 15))
        
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
                variable=self.extract_type_var,
                value=value, 
                font=ctk.CTkFont(size=13)
            )
            rb.pack(side="left", padx=15)
        
        # 水印形状/长度
        shape_frame = ctk.CTkFrame(inner, fg_color="transparent")
        shape_frame.pack(fill="x")
        
        ctk.CTkLabel(
            shape_frame, 
            text="水印形状/长度:", 
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w")
        
        ctk.CTkEntry(
            shape_frame, 
            textvariable=self.variables['wm_shape'], 
            height=40,
            font=ctk.CTkFont(size=13)
        ).pack(fill="x", pady=(5, 0))
        
        ctk.CTkLabel(
            shape_frame, 
            text="提示: 图片格式为 宽,高  |  文本/二进制格式为长度",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_SECONDARY
        ).pack(anchor="w", pady=(5, 0))
    
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
    
    def _create_extract_button(self, parent):
        """创建提取按钮"""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        extract_btn = ctk.CTkButton(
            btn_frame, 
            text="提取水印",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50, 
            corner_radius=10,
            command=self._do_extract
        )
        extract_btn.pack(pady=10)
    
    def _create_result_section(self, parent):
        """创建结果显示区域"""
        section = ctk.CTkFrame(parent, corner_radius=15, fg_color=SECTION_BG)
        section.pack(fill="x", pady=10)
        
        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(padx=25, pady=20, fill="x")
        
        title = ctk.CTkLabel(
            inner, 
            text="提取结果",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(anchor="w", pady=(0, 10))
        
        self.extract_result = ctk.CTkTextbox(
            inner, 
            height=120,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.extract_result.pack(fill="x")
    
    def _browse_watermarked(self):
        """浏览带水印图片"""
        path = browse_watermarked_img()
        if path:
            self.variables['original_img_path'].set(path)
    
    def _browse_output(self):
        """浏览输出路径"""
        mode = self.extract_type_var.get()
        path = save_extract_output(mode)
        if path:
            self.variables['output_img_path'].set(path)
    
    def _do_extract(self):
        """执行提取操作"""
        mode = self.extract_type_var.get()
        
        success, message, extracted = extract_watermark(
            img_path=self.variables['original_img_path'].get(),
            output_path=self.variables['output_img_path'].get(),
            password_img=self.variables['password_img'].get(),
            password_wm=self.variables['password_wm'].get(),
            mode=mode,
            wm_shape=self.variables['wm_shape'].get()
        )
        
        if success:
            # 显示提取结果
            if extracted is not None:
                self.extract_result.delete("1.0", "end")
                if mode == "str":
                    self.extract_result.insert("1.0", f"提取的文本水印:\n{extracted}")
                elif mode == "bit":
                    self.extract_result.insert("1.0", f"提取的二进制水印:\n{extracted}")
            
            messagebox.showinfo("成功", message)
        else:
            messagebox.showerror("错误", message)


def create_extract_page(parent, variables):
    """创建提取水印页面
    
    Args:
        parent: 父容器
        variables: 变量字典
        
    Returns:
        page: 页面Frame
    """
    extract_page = ExtractPage(parent, variables)
    return extract_page.page
