import PyInstaller.__main__
import os
import shutil
import time
import sys

def build_exe():
    # 清理旧的构建文件
    try:
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('DockerManager.spec'):
            os.remove('DockerManager.spec')
    except Exception as e:
        print(f"清理旧文件时出错: {str(e)}")
        return False

    # 检查必要文件
    if not os.path.exists('app.ico'):
        print("错误: 未找到app.ico文件！")
        return False
    if not os.path.exists('src/img/logo.png'):
        print("错误: 未找到logo.png文件！")
        return False

    # PyInstaller 打包参数
    params = [
        'src/main.py',                          # 主程序入口
        '--name=DockerManager',                 # 生成的exe名称
        '--icon=app.ico',                       # 程序图标
        '--noconsole',                          # 不显示控制台
        '--windowed',                           # GUI程序
        # 资源文件
        '--add-data=src/img/logo.png;img',      # 将logo放在img目录下
        # 必要的依赖
        '--hidden-import=PySide6',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=subprocess',
        '--hidden-import=webbrowser',
        # 项目模块
        '--hidden-import=src',
        '--hidden-import=src.core',
        '--hidden-import=src.ui',
        '--hidden-import=src.utils',
        '--hidden-import=src.core.docker_operations',
        '--hidden-import=src.ui.confirm_dialog',
        '--hidden-import=src.ui.password_dialog',
        '--hidden-import=src.ui.main_window',
        # QT插件和运行时
        '--collect-all=PySide6',
        '--collect-all=shiboken6',
        # 搜索路径
        '--paths=.',
        '--paths=src',
        # 打包选项
        '--onefile',                            # 单文件模式
        '--clean',                              # 清理临时文件
        '--noconfirm',                          # 不确认覆盖
        # 性能和兼容性优化
        '--noupx',                              # 不使用UPX压缩
        '--disable-windowed-traceback',         # 禁用窗口化回溯
        '--optimize=2',                         # 优化字节码
        # 额外选项
        '--runtime-tmpdir=.',                   # 运行时临时目录
    ]

    try:
        print("开始打包...")
        print("正在收集依赖...")
        PyInstaller.__main__.run(params)
        print("\n打包完成！")
        print("可执行文件位置: dist/DockerManager.exe")
        return True
    except Exception as e:
        print(f"打包过程中出错: {str(e)}")
        return False

if __name__ == "__main__":
    print("Docker管理工具打包程序")
    print("=" * 50)
    print("环境检查:")
    
    # 检查Python环境
    print(f"• Python版本: {sys.version.split()[0]}")
    
    # 检查必要的包
    required_packages = ['PySide6', 'PyInstaller']
    for package in required_packages:
        try:
            __import__(package)
            print(f"• {package}: 已安装")
        except ImportError:
            print(f"• {package}: 未安装")
            print(f"请执行: pip install {package}")
            sys.exit(1)
    
    print("\n文件检查:")
    print(f"• app.ico: {'存在' if os.path.exists('app.ico') else '不存在'}")
    print(f"• logo.png: {'存在' if os.path.exists('src/img/logo.png') else '不存在'}")
    
    print("\n准备开始打包...")
    time.sleep(2)
    
    if build_exe():
        print("\n打包成功！")
        print("\n注意事项：")
        print("1. 程序可以在任何Windows系统上独立运行")
        print("2. 不需要安装Python或其他依赖")
        print("3. 需要确保目标系统安装了Docker")
        print("4. 建议在目标系统上测试运行")
        print("\n程序位置: dist/DockerManager.exe")
    else:
        print("\n打包失败，请检查错误信息。") 