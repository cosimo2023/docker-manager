import sys
import os

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from src.utils import get_resource_path
from src.ui.password_dialog import PasswordDialog
from src.ui.main_window import MainWindow
from src.core.docker_operations import DockerOperations

def check_environment(app):
    """检查运行环境"""
    from src import DOCKER_CHECK_TITLE, DOCKER_CHECK_MESSAGE, FULL_APP_NAME
    
    # 检查Docker
    docker_ok, message = DockerOperations.check_docker_installed()
    
    # 创建自定义样式的消息框
    msg_box = QMessageBox()
    
    # 设置窗口图标
    logo_path = get_resource_path('logo.png')
    if os.path.exists(logo_path):
        msg_box.setWindowIcon(QIcon(logo_path))
    
    # 设置样式
    msg_box.setStyleSheet("""
        QMessageBox {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #CC2196F3,
                stop:0.7 #CC2196F3,
                stop:0.85 #992196F3,
                stop:0.7 #99F44336,
                stop:0.85 #CCF44336,
                stop:1 #CCF44336);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
        }
        QLabel {
            color: white;
            font-size: 14px;
            font-weight: bold;
            background-color: transparent;
        }
        QPushButton {
            background-color: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 5px;
            padding: 5px 15px;
            color: white;
            min-width: 80px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.4);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.2);
        }
    """)
    
    if not docker_ok:
        status = "❌ 检查失败"
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(f"{FULL_APP_NAME} - {DOCKER_CHECK_TITLE}")
        msg_box.setText(DOCKER_CHECK_MESSAGE.format(
            status=status,
            message=message
        ))
        msg_box.exec()
        return False
    
    # Docker 正常运行
    status = "✅ 检查通过"
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setWindowTitle(f"{FULL_APP_NAME} - {DOCKER_CHECK_TITLE}")
    msg_box.setText(DOCKER_CHECK_MESSAGE.format(
        status=status,
        message="Docker 环境正常，可以开始使用程序。"
    ))
    msg_box.exec()
    return True

def main():
    # 创建应用实例
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    try:
        # 检查环境
        if not check_environment(app):
            return
        
        # 显示密码验证对话框
        password_dialog = PasswordDialog()
        if password_dialog.exec() == PasswordDialog.DialogCode.Accepted:
            # 密码验证通过，显示主窗口
            window = MainWindow()
            window.show()
            sys.exit(app.exec())
        else:
            sys.exit(0)
            
    except Exception as e:
        # 使用GUI显示错误
        QMessageBox.critical(None, 
                           "错误",
                           f"程序运行出错：\n{str(e)}\n\n请联系技术支持。")
        sys.exit(1)

if __name__ == '__main__':
    main() 