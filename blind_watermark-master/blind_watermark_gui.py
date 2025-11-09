import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import cv2
import numpy as np
from blind_watermark import WaterMark


class BlindWatermarkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("盲水印工具")
        self.root.geometry("700x500")

        # 存储参数
        self.original_img_path = tk.StringVar()
        self.watermark_content = tk.StringVar()
        self.watermark_img_path = tk.StringVar()
        self.output_img_path = tk.StringVar()
        self.password_img = tk.StringVar(value="1")
        self.password_wm = tk.StringVar(value="1")
        self.wm_shape = tk.StringVar(value="128,128")  # 图片水印形状，文本水印为长度
        self.wm_mode = tk.StringVar(value="str")
        #str / img / bit

        self.create_widgets()

    def create_widgets(self):
        # 标签页
        tab_control = ttk.Notebook(self.root)

        # 嵌入水印标签页
        embed_tab = ttk.Frame(tab_control)
        tab_control.add(embed_tab, text="嵌入水印")

        # 提取水印标签页
        extract_tab = ttk.Frame(tab_control)
        tab_control.add(extract_tab, text="提取水印")

        tab_control.pack(expand=1, fill="both")

        # 构建嵌入水印界面
        self.build_embed_tab(embed_tab)

        # 构建提取水印界面
        self.build_extract_tab(extract_tab)

    def build_embed_tab(self, parent):
        # 原图路径
        ttk.Label(parent, text="原图路径:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.original_img_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(parent, text="浏览", command=self.browse_original_img).grid(row=0, column=2, padx=5, pady=5)

        # 水印类型
        ttk.Label(parent, text="水印类型:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        mode_frame = ttk.Frame(parent)
        mode_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="文本", variable=self.wm_mode, value="str").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="图片", variable=self.wm_mode, value="img").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="二进制", variable=self.wm_mode, value="bit").pack(side=tk.LEFT, padx=5)

        # 水印内容/路径
        self.wm_content_frame = ttk.Frame(parent)
        self.wm_content_label = ttk.Label(self.wm_content_frame, text="水印文本:")
        self.wm_content_label.pack(side=tk.LEFT, padx=5)
        self.wm_content_entry = ttk.Entry(self.wm_content_frame, textvariable=self.watermark_content, width=40)
        self.wm_content_entry.pack(side=tk.LEFT, padx=5)
        self.wm_content_frame.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        self.wm_img_frame = ttk.Frame(parent)
        ttk.Label(self.wm_img_frame, text="水印图片路径:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(self.wm_img_frame, textvariable=self.watermark_img_path, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.wm_img_frame, text="浏览", command=self.browse_watermark_img).pack(side=tk.LEFT, padx=5)

        # 密码设置
        ttk.Label(parent, text="图片密码:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.password_img).grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(parent, text="水印密码:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.password_wm).grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        # 输出路径
        ttk.Label(parent, text="输出图片路径:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.output_img_path, width=50).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(parent, text="浏览", command=self.browse_output_img).grid(row=5, column=2, padx=5, pady=5)

        # 嵌入按钮
        ttk.Button(parent, text="嵌入水印", command=self.embed_watermark).grid(row=6, column=1, padx=5, pady=20)

        # 绑定水印类型切换事件
        self.wm_mode.trace_add("write", self.update_wm_input)
        self.update_wm_input()  # 初始化显示

    def build_extract_tab(self, parent):
        # 带水印图片路径
        ttk.Label(parent, text="带水印图片路径:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.original_img_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(parent, text="浏览", command=self.browse_watermarked_img).grid(row=0, column=2, padx=5, pady=5)

        # 水印类型
        ttk.Label(parent, text="水印类型:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        mode_frame = ttk.Frame(parent)
        mode_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="文本", variable=self.wm_mode, value="str").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="图片", variable=self.wm_mode, value="img").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="二进制", variable=self.wm_mode, value="bit").pack(side=tk.LEFT, padx=5)

        # 水印形状/长度
        ttk.Label(parent, text="水印形状/长度:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.wm_shape, width=50).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(parent, text="(图片:宽,高; 文本/二进制:长度)").grid(row=3, column=1, padx=5, pady=0, sticky=tk.W)

        # 密码设置
        ttk.Label(parent, text="图片密码:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.password_img).grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(parent, text="水印密码:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.password_wm).grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        # 输出路径
        ttk.Label(parent, text="提取结果路径:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.output_img_path, width=50).grid(row=6, column=1, padx=5, pady=5)
        ttk.Button(parent, text="浏览", command=self.browse_extract_output).grid(row=6, column=2, padx=5, pady=5)

        # 提取按钮
        ttk.Button(parent, text="提取水印", command=self.extract_watermark).grid(row=7, column=1, padx=5, pady=20)

        # 提取结果显示
        self.extract_result = tk.Text(parent, height=5, width=60)
        self.extract_result.grid(row=8, column=1, padx=5, pady=5)

    def update_wm_input(self, *args):
        # 根据水印类型切换输入框
        mode = self.wm_mode.get()
        if mode == "str" or mode == "bit":
            self.wm_content_frame.grid()
            self.wm_img_frame.grid_remove()
            if mode == "str":
                self.wm_content_label.config(text="水印文本:")
            else:
                self.wm_content_label.config(text="二进制数据(用逗号分隔):")
        else:
            self.wm_content_frame.grid_remove()
            self.wm_img_frame.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    def browse_original_img(self):
        path = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.bmp")])
        if path:
            self.original_img_path.set(path)

    def browse_watermark_img(self):
        path = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.bmp")])
        if path:
            self.watermark_img_path.set(path)

    def browse_output_img(self):
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG文件", "*.png"), ("JPG文件", "*.jpg")])
        if path:
            self.output_img_path.set(path)

    def browse_watermarked_img(self):
        path = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.bmp")])
        if path:
            self.original_img_path.set(path)

    def browse_extract_output(self):
        if self.wm_mode.get() == "img":
            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("图片文件", "*.png;*.jpg")])
        else:
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("文本文件", "*.txt")])
        if path:
            self.output_img_path.set(path)

    def embed_watermark(self):
        try:
            # 验证参数
            if not self.original_img_path.get():
                messagebox.showerror("错误", "请选择原图路径")
                return

            mode = self.wm_mode.get()
            if mode == "str" and not self.watermark_content.get():
                messagebox.showerror("错误", "请输入水印文本")
                return
            if mode == "img" and not self.watermark_img_path.get():
                messagebox.showerror("错误", "请选择水印图片路径")
                return
            if mode == "bit":
                try:
                    bits = list(map(bool, map(int, self.watermark_content.get().split(','))))
                except:
                    messagebox.showerror("错误", "二进制数据格式错误(用逗号分隔0/1)")
                    return

            if not self.output_img_path.get():
                messagebox.showerror("错误", "请选择输出图片路径")
                return

            # 初始化水印对象
            bwm = WaterMark(
                password_img=int(self.password_img.get()),
                password_wm=int(self.password_wm.get())
            )

            # 读取原图
            bwm.read_img(self.original_img_path.get())

            # 读取水印
            if mode == "str":
                bwm.read_wm(self.watermark_content.get(), mode="str")
            elif mode == "img":
                bwm.read_wm(self.watermark_img_path.get(), mode="img")
            elif mode == "bit":
                bwm.read_wm(bits, mode="bit")

            # 嵌入水印
            bwm.embed(self.output_img_path.get())

            # 保存水印长度（文本/二进制）
            if mode in ("str", "bit"):
                len_wm = len(bwm.wm_bit)
                messagebox.showinfo("成功", f"水印嵌入成功！\n水印长度: {len_wm}\n(提取时需使用此长度)")
            else:
                messagebox.showinfo("成功", "水印嵌入成功！")

        except Exception as e:
            messagebox.showerror("错误", f"嵌入失败: {str(e)}")

    def extract_watermark(self):
        try:
            # 验证参数
            if not self.original_img_path.get():
                messagebox.showerror("错误", "请选择带水印图片路径")
                return

            if not self.wm_shape.get():
                messagebox.showerror("错误", "请输入水印形状/长度")
                return

            if not self.output_img_path.get():
                messagebox.showerror("错误", "请选择提取结果路径")
                return

            mode = self.wm_mode.get()
            # 解析水印形状
            if mode == "img":
                try:
                    w, h = map(int, self.wm_shape.get().split(','))
                    wm_shape = (w, h)
                except:
                    messagebox.showerror("错误", "图片水印形状格式错误(宽,高)")
                    return
            else:
                try:
                    wm_shape = int(self.wm_shape.get())
                except:
                    messagebox.showerror("错误", "文本/二进制水印长度需为整数")
                    return

            # 初始化水印对象
            bwm = WaterMark(
                password_img=int(self.password_img.get()),
                password_wm=int(self.password_wm.get())
            )

            # 提取水印
            if mode == "img":
                bwm.extract(
                    filename=self.original_img_path.get(),
                    wm_shape=wm_shape,
                    out_wm_name=self.output_img_path.get(),
                    mode="img"
                )
                messagebox.showinfo("成功", f"图片水印提取成功！\n已保存至: {self.output_img_path.get()}")
            elif mode == "str":
                wm_extract = bwm.extract(
                    filename=self.original_img_path.get(),
                    wm_shape=wm_shape,
                    mode="str"
                )
                self.extract_result.delete(1.0, tk.END)
                self.extract_result.insert(tk.END, f"提取的文本水印:\n{wm_extract}")
                with open(self.output_img_path.get(), 'w', encoding='utf-8') as f:
                    f.write(wm_extract)
                messagebox.showinfo("成功", f"文本水印提取成功！\n已保存至: {self.output_img_path.get()}")
            elif mode == "bit":
                wm_extract = bwm.extract(
                    filename=self.original_img_path.get(),
                    wm_shape=wm_shape,
                    mode="bit"
                )
                # 转换为0/1
                bit_str = ','.join(['1' if x >= 0.5 else '0' for x in wm_extract])
                self.extract_result.delete(1.0, tk.END)
                self.extract_result.insert(tk.END, f"提取的二进制水印:\n{bit_str}")
                with open(self.output_img_path.get(), 'w') as f:
                    f.write(bit_str)
                messagebox.showinfo("成功", f"二进制水印提取成功！\n已保存至: {self.output_img_path.get()}")

        except Exception as e:
            messagebox.showerror("错误", f"提取失败: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BlindWatermarkGUI(root)
    root.mainloop()