"""水印处理逻辑模块"""
from tkinter import messagebox
from blind_watermark import WaterMark


def embed_watermark(original_path, output_path, password_img, password_wm, 
                    mode, watermark_content=None, watermark_img_path=None):
    """嵌入水印
    
    Args:
        original_path: 原图路径
        output_path: 输出路径
        password_img: 图片密码
        password_wm: 水印密码
        mode: 水印类型 ('str', 'img', 'bit')
        watermark_content: 水印内容（文本或二进制数据）
        watermark_img_path: 水印图片路径
        
    Returns:
        tuple: (success, message, wm_length)
    """
    try:
        # 验证参数
        if not original_path:
            return False, "请选择原图路径", None
        
        if mode == "str" and not watermark_content:
            return False, "请输入水印文本", None
        
        if mode == "img" and not watermark_img_path:
            return False, "请选择水印图片路径", None
        
        if mode == "bit":
            try:
                bits = list(map(bool, map(int, watermark_content.split(','))))
            except:
                return False, "二进制数据格式错误(用逗号分隔0/1)", None
        
        if not output_path:
            return False, "请选择输出图片路径", None
        
        # 初始化水印对象
        bwm = WaterMark(
            password_img=int(password_img),
            password_wm=int(password_wm)
        )
        
        # 读取原图
        bwm.read_img(original_path)
        
        # 读取水印
        if mode == "str":
            bwm.read_wm(watermark_content, mode="str")
        elif mode == "img":
            bwm.read_wm(watermark_img_path, mode="img")
        elif mode == "bit":
            bwm.read_wm(bits, mode="bit")
        
        # 嵌入水印
        bwm.embed(output_path)
        
        # 返回水印长度
        wm_length = len(bwm.wm_bit) if mode in ("str", "bit") else None
        
        return True, "水印嵌入成功！", wm_length
        
    except Exception as e:
        return False, f"嵌入失败: {str(e)}", None


def extract_watermark(img_path, output_path, password_img, password_wm, 
                      mode, wm_shape):
    """提取水印
    
    Args:
        img_path: 带水印图片路径
        output_path: 输出路径
        password_img: 图片密码
        password_wm: 水印密码
        mode: 水印类型 ('str', 'img', 'bit')
        wm_shape: 水印形状/长度
        
    Returns:
        tuple: (success, message, extracted_content)
    """
    try:
        # 验证参数
        if not img_path:
            return False, "请选择带水印图片路径", None
        
        if not wm_shape:
            return False, "请输入水印形状/长度", None
        
        if not output_path:
            return False, "请选择提取结果路径", None
        
        # 解析水印形状
        if mode == "img":
            try:
                w, h = map(int, wm_shape.split(','))
                parsed_shape = (w, h)
            except:
                return False, "图片水印形状格式错误(宽,高)", None
        else:
            try:
                parsed_shape = int(wm_shape)
            except:
                return False, "文本/二进制水印长度需为整数", None
        
        # 初始化水印对象
        bwm = WaterMark(
            password_img=int(password_img),
            password_wm=int(password_wm)
        )
        
        # 提取水印
        if mode == "img":
            bwm.extract(
                filename=img_path,
                wm_shape=parsed_shape,
                out_wm_name=output_path,
                mode="img"
            )
            return True, f"图片水印提取成功！\n\n已保存至:\n{output_path}", None
            
        elif mode == "str":
            wm_extract = bwm.extract(
                filename=img_path,
                wm_shape=parsed_shape,
                mode="str"
            )
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(wm_extract)
            return True, f"文本水印提取成功！\n\n已保存至:\n{output_path}", wm_extract
            
        elif mode == "bit":
            wm_extract = bwm.extract(
                filename=img_path,
                wm_shape=parsed_shape,
                mode="bit"
            )
            bit_str = ','.join(['1' if x >= 0.5 else '0' for x in wm_extract])
            with open(output_path, 'w') as f:
                f.write(bit_str)
            return True, f"二进制水印提取成功！\n\n已保存至:\n{output_path}", bit_str
        
    except Exception as e:
        return False, f"提取失败: {str(e)}", None
