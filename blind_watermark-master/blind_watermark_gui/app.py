"""主应用类模块"""
import customtkinter as ctk

from config import load_config, save_config
from background import BackgroundManager
from components import Sidebar
from pages import create_home_page, create_embed_page, create_extract_page


# 设置CustomTkinter主题
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BlindWatermarkGUI(ctk.CTk):
    """盲水印工具主应用类"""
    
    def __init__(self):
        super().__init__()
        
        # 窗口设置
        self.title("盲水印工具 - Blind Watermark Tool")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # 居中显示
        self._center_window()
        
        # 加载配置
        self.config = load_config()
        
        # 初始化背景管理器
        self.bg_manager = BackgroundManager(
            root=self,
            config=self.config,
            save_config_callback=self._save_config
        )
        
        # 存储参数变量
        self._init_variables()
        
        # 当前页面
        self.current_page = "home"
        
        # 页面字典
        self.pages = {}
        
        # 侧边栏
        self.sidebar = None
        
        # 主内容区域
        self.main_container = None
        
        # 创建背景层
        self.bg_manager.create_background()
        
        # 创建界面
        self._create_layout()
        
        # 确保背景在所有组件之下
        self.bg_manager.ensure_background_at_bottom()
        
        # 绑定窗口大小变化事件
        self.bind("<Configure>", self.bg_manager.on_window_resize)
    
    def _center_window(self):
        """居中显示窗口"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"1000x700+{x}+{y}")
    
    def _init_variables(self):
        """初始化变量"""
        self.original_img_path = ctk.StringVar()
        self.watermark_content = ctk.StringVar()
        self.watermark_img_path = ctk.StringVar()
        self.output_img_path = ctk.StringVar()
        self.password_img = ctk.StringVar(value="1")
        self.password_wm = ctk.StringVar(value="1")
        self.wm_shape = ctk.StringVar(value="128,128")
        self.wm_mode = ctk.StringVar(value="str")
    
    def _get_variables_dict(self):
        """获取变量字典"""
        return {
            'original_img_path': self.original_img_path,
            'watermark_content': self.watermark_content,
            'watermark_img_path': self.watermark_img_path,
            'output_img_path': self.output_img_path,
            'password_img': self.password_img,
            'password_wm': self.password_wm,
            'wm_shape': self.wm_shape,
            'wm_mode': self.wm_mode
        }
    
    def _save_config(self):
        """保存配置"""
        save_config(self.config)
    
    def _create_layout(self):
        """创建主布局"""
        # 配置grid权重
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 创建侧边栏
        self.sidebar = Sidebar(
            root=self,
            show_page_callback=self.show_page,
            toggle_theme_callback=self._toggle_theme
        )
        
        # 创建主内容区域
        self.main_container = ctk.CTkFrame(
            self, 
            corner_radius=15,
            fg_color="transparent",
            bg_color="transparent"
        )
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.lift()
        
        # 创建各个页面
        self._create_pages()
        
        # 默认显示主页
        self.show_page("home")
    
    def _create_pages(self):
        """创建各个页面"""
        variables = self._get_variables_dict()
        
        # 主页
        self.pages["home"] = create_home_page(
            self.main_container, 
            self.show_page
        )
        
        # 嵌入水印页面
        self.pages["embed"] = create_embed_page(
            self.main_container, 
            variables
        )
        
        # 提取水印页面
        self.pages["extract"] = create_extract_page(
            self.main_container, 
            variables
        )
    
    def show_page(self, page_name):
        """显示指定页面
        
        Args:
            page_name: 页面名称
        """
        self.current_page = page_name
        
        # 隐藏所有页面
        for page in self.pages.values():
            page.grid_forget()
        
        # 显示目标页面
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")
        
        # 更新导航按钮状态
        self.sidebar.update_nav_buttons(page_name)
    
    def _toggle_theme(self):
        """切换主题"""
        theme = self.sidebar.get_theme()
        ctk.set_appearance_mode(theme)
