import os
import sys

def get_resource_path(relative_path):
    """获取资源文件的路径"""
    if getattr(sys, 'frozen', False):
        # 打包后的路径
        base_path = sys._MEIPASS
        return os.path.join(base_path, "img", relative_path)
    else:
        # 开发环境路径
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, "src", "img", relative_path) 