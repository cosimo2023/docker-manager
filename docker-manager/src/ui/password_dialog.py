from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, 
                           QPushButton, QLabel, QMessageBox, QMenu, QWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QPainter, QLinearGradient, QColor
from ..utils import get_resource_path
import webbrowser
import os

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("隆相.中国 Docker 管理工具 v1.0.0.1")
        self.setFixedSize(400, 300)
        
        # 设置窗口图标
        logo_path = get_resource_path('logo.png')
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        
        self.setup_ui()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#D92196F3"))    # 蓝色 85% 不透明
        gradient.setColorAt(1, QColor("#D9F44336"))    # 红色 85% 不透明
        painter.fillRect(self.rect(), gradient)
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # 创建一个容器用于密码输入区域
        input_container = QWidget()
        input_container.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 15px;
            }
        """)
        input_layout = QVBoxLayout(input_container)
        input_layout.setSpacing(15)
        input_layout.setContentsMargins(20, 20, 20, 20)
        
        # 密码输入提示
        label = QLabel("请输入密码")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        # 密码输入框容器
        password_container = QWidget()
        password_container.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
        """)
        password_layout = QVBoxLayout(password_container)
        password_layout.setContentsMargins(10, 10, 10, 10)
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("请输入访问密码")
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: none;
                font-size: 16px;
                background: transparent;
                color: white;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }
        """)
        
        password_layout.addWidget(self.password_input)
        
        # 确认按钮
        confirm_button = QPushButton("登 录")
        confirm_button.setFixedSize(200, 45)
        confirm_button.setCursor(Qt.CursorShape.PointingHandCursor)  # 添加手型光标
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 22px;
                font-size: 16px;
                font-weight: bold;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border-color: rgba(255, 255, 255, 0.4);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                border-color: rgba(255, 255, 255, 0.2);
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
            }
        """)
        confirm_button.clicked.connect(self.verify_password)
        
        # 组装输入区域
        input_layout.addWidget(label)
        input_layout.addWidget(password_container)
        input_layout.addSpacing(10)
        input_layout.addWidget(confirm_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 主布局
        layout.addStretch(1)
        layout.addWidget(input_container)
        layout.addStretch(1)
        
        self.setLayout(layout)
        
    def verify_password(self):
        if self.password_input.text() == "17321008396":
            self.accept()
        else:
            QMessageBox.warning(self, "错误", "密码错误，请重试！")
            self.password_input.clear()

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        
        website_action = QAction("隆相.中国官网", self)
        website_action.triggered.connect(lambda: webbrowser.open("https://lonxang.com"))
        context_menu.addAction(website_action)
        
        phone_action = QAction("中国区业务电话: 17321008396", self)
        context_menu.addAction(phone_action)
        
        context_menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #BBDEFB;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #2196F3;
                color: white;
            }
        """)
        
        context_menu.exec(self.mapToGlobal(position)) 