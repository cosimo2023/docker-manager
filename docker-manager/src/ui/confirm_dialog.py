from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
                           QPushButton, QLabel, QMessageBox, QMenu)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QPainter, QLinearGradient, QColor
import random
import webbrowser

class ConfirmDialog(QDialog):
    def __init__(self, operation_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("隆相.中国 Docker 管理工具 v1.0.0.1")
        self.setFixedSize(400, 300)
        self.operation_name = operation_name
        self.setup_ui()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        # 蓝色渐变
        gradient.setColorAt(0, QColor("#CC2196F3"))      # 蓝色起始，80%不透明
        gradient.setColorAt(0.7, QColor("#CC2196F3"))    # 蓝色保持到70%
        gradient.setColorAt(0.85, QColor("#992196F3"))   # 蓝色85%处开始减淡
        # 红色渐变
        gradient.setColorAt(0.7, QColor("#99F44336"))    # 红色70%处开始淡入
        gradient.setColorAt(0.85, QColor("#CCF44336"))   # 红色85%处加深
        gradient.setColorAt(1, QColor("#CCF44336"))      # 红色结束，80%不透明
        painter.fillRect(self.rect(), gradient)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)  # 增加组件之间的间距
        
        # 操作提示
        operation_label = QLabel(f"您确定要执行{self.operation_name}操作吗？")
        operation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        operation_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: white;
                font-weight: bold;
                padding: 10px;
                background-color: transparent;
            }
        """)
        
        # 生成验证码算式
        self.num1 = random.randint(1, 9)
        self.num2 = random.randint(1, 9)
        self.result = self.num1 + self.num2
        
        # 验证码提示
        verify_label = QLabel(f"请输入验证码: {self.num1} + {self.num2} = ?")
        verify_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        verify_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
                padding: 10px;
                background-color: transparent;
            }
        """)
        
        # 验证码输入框
        self.verify_input = QLineEdit()
        self.verify_input.setFixedHeight(35)
        self.verify_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verify_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
            }
            QLineEdit:focus {
                border-color: rgba(255, 255, 255, 0.5);
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        
        # 创建水平布局用于按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)  # 按钮之间的间距
        
        # 确认按钮
        confirm_button = QPushButton("确认")
        confirm_button.setFixedSize(100, 35)
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                box-shadow: 0 2px 5px rgba(33, 150, 243, 0.3);
            }
            QPushButton:hover {
                background-color: #1976D2;
                box-shadow: 0 4px 8px rgba(33, 150, 243, 0.5);
            }
            QPushButton:pressed {
                background-color: #0D47A1;
                box-shadow: 0 1px 3px rgba(33, 150, 243, 0.3);
            }
        """)
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.setFixedSize(100, 35)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                box-shadow: 0 2px 5px rgba(244, 67, 54, 0.3);
            }
            QPushButton:hover {
                background-color: #D32F2F;
                box-shadow: 0 4px 8px rgba(244, 67, 54, 0.5);
            }
            QPushButton:pressed {
                background-color: #B71C1C;
                box-shadow: 0 1px 3px rgba(244, 67, 54, 0.3);
            }
        """)
        
        confirm_button.clicked.connect(self.verify_input_result)
        cancel_button.clicked.connect(self.reject)
        
        # 将按钮添加到水平布局
        button_layout.addStretch()  # 添加弹性空间
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()  # 添加弹性空间
        
        # 添加所有组件到主布局
        layout.addStretch()  # 顶部弹性空间
        layout.addWidget(operation_label)
        layout.addWidget(verify_label)
        layout.addWidget(self.verify_input)
        layout.addLayout(button_layout)
        layout.addStretch()  # 底部弹性空间
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog {
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
            }
        """)
        
    def verify_input_result(self):
        try:
            if int(self.verify_input.text()) == self.result:
                self.accept()
            else:
                QMessageBox.warning(self, "错误", "验证码错误，请重试！")
                self.verify_input.clear()
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的数字！")
            self.verify_input.clear()

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