"""背景图片管理模块"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os


class BackgroundManager:
    """背景图片管理器"""
    
    def __init__(self, root, config, save_config_callback):
        """初始化背景管理器
        
        Args:
            root: 主窗口
            config: 配置字典
            save_config_callback: 保存配置的回调函数
        """
        self.root = root
        self.config = config
        self.save_config_callback = save_config_callback
        
        # 背景图片相关属性
        self.bg_image_path = config.get("background_image") or None
        self.bg_image_original = None  # 原始PIL图片
        self.bg_ctk_image = None  # CTkImage对象
        self.bg_label = None  # 背景标签
        self.resize_after_id = None  # 防抖动定时器ID
        self.last_size = (0, 0)  # 上次窗口大小
        self.preview_ctk_image = None  # 预览图片CTkImage对象
        
        # 预览相关引用（由设置页面设置）
        self.preview_label = None
        self.bg_path_var = None
    
    def create_background(self):
        """创建背景层"""
        self.bg_label = ctk.CTkLabel(self.root, text="", fg_color="transparent")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 如果有保存的背景图片，加载它
        if self.bg_image_path:
            self.load_background_image(self.bg_image_path)
    
    def ensure_background_at_bottom(self):
        """确保背景始终在最底层"""
        if self.bg_label:
            self.bg_label.lower()
    
    def load_background_image(self, image_path):
        """加载背景图片
        
        Args:
            image_path: 图片路径
            
        Returns:
            bool: 是否成功
        """
        try:
            self.bg_image_original = Image.open(image_path)
            self.bg_image_path = image_path
            self.update_background()
            
            # 更新配置
            self.config["background_image"] = image_path
            self.save_config_callback()
            return True
        except Exception as e:
            messagebox.showerror("错误", f"加载背景图片失败: {str(e)}")
            return False
    
    def update_background(self):
        """更新背景图片大小以适应窗口"""
        if self.bg_image_original is None:
            return
        
        win_width = self.root.winfo_width()
        win_height = self.root.winfo_height()
        
        if win_width <= 1 or win_height <= 1:
            return
        
        # 计算cover模式的缩放比例
        img_width, img_height = self.bg_image_original.size
        scale_w = win_width / img_width
        scale_h = win_height / img_height
        scale = max(scale_w, scale_h)
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # 使用LANCZOS进行高质量缩放
        resized_img = self.bg_image_original.resize((new_width, new_height), Image.LANCZOS)
        
        # 居中裁剪
        left = (new_width - win_width) // 2
        top = (new_height - win_height) // 2
        cropped_img = resized_img.crop((left, top, left + win_width, top + win_height))
        
        # 创建CTkImage
        self.bg_ctk_image = ctk.CTkImage(
            light_image=cropped_img,
            dark_image=cropped_img,
            size=(win_width, win_height)
        )
        
        # 更新背景标签
        self.bg_label.configure(image=self.bg_ctk_image)
        self.ensure_background_at_bottom()
    
    def on_window_resize(self, event):
        """窗口大小变化事件处理（带防抖动）"""
        if event.widget != self.root:
            return
        
        new_size = (event.width, event.height)
        if new_size == self.last_size:
            return
        
        self.last_size = new_size
        
        # 取消之前的定时器
        if self.resize_after_id is not None:
            self.root.after_cancel(self.resize_after_id)
        
        # 设置新的定时器，延迟150ms后更新背景
        self.resize_after_id = self.root.after(150, self.update_background)
    
    def choose_background_image(self):
        """选择背景图片"""
        path = filedialog.askopenfilename(
            title="选择背景图片",
            filetypes=[
                ("图片文件", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.webp"),
                ("所有文件", "*.*")
            ]
        )
        if path:
            self.load_background_image(path)
            # 更新设置页面的路径显示
            if self.bg_path_var:
                self.bg_path_var.set(path)
            # 更新预览
            if self.preview_label:
                self.update_preview_image()
    
    def clear_background_image(self):
        """清除背景图片"""
        self.bg_image_path = None
        self.bg_image_original = None
        self.bg_ctk_image = None
        
        if self.bg_label:
            try:
                self.bg_label._label.configure(image="")
            except:
                pass
        
        # 清除配置
        self.config["background_image"] = ""
        self.save_config_callback()
        
        # 更新设置页面
        if self.bg_path_var:
            self.bg_path_var.set("无")
        
        if self.preview_label:
            self.preview_ctk_image = None
            self.preview_label.configure(text="暂无背景图片")
            try:
                self.preview_label._label.configure(image="")
            except:
                pass
    
    def update_preview_image(self):
        """更新预览图片"""
        if self.preview_label is None:
            return
        
        try:
            bg_path = self.config.get("background_image")
            if bg_path and os.path.exists(bg_path):
                img = Image.open(bg_path)
                
                # 计算预览尺寸（保持宽高比）
                preview_width = 400
                preview_height = 220
                img_ratio = img.width / img.height
                preview_ratio = preview_width / preview_height
                
                if img_ratio > preview_ratio:
                    new_height = preview_height
                    new_width = int(preview_height * img_ratio)
                else:
                    new_width = preview_width
                    new_height = int(preview_width / img_ratio)
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
                
                # 居中裁剪
                left = (new_width - preview_width) // 2
                top = (new_height - preview_height) // 2
                img = img.crop((left, top, left + preview_width, top + preview_height))
                
                self.preview_ctk_image = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(preview_width, preview_height)
                )
                
                self.preview_label.configure(image=self.preview_ctk_image, text="")
            else:
                self.preview_ctk_image = None
                self.preview_label.configure(text="暂无背景图片")
                try:
                    self.preview_label._label.configure(image="")
                except:
                    pass
        except Exception:
            self.preview_ctk_image = None
            self.preview_label.configure(text="加载预览失败")
            try:
                self.preview_label._label.configure(image="")
            except:
                pass
