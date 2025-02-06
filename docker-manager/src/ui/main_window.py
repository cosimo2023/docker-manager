from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QGridLayout, QInputDialog, QFileDialog,
                           QMessageBox, QProgressBar, QLabel, QFrame, QMenu)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QPixmap, QIcon, QPainter, QLinearGradient, QColor
from ..core.docker_operations import DockerOperations
from .confirm_dialog import ConfirmDialog
from ..utils import get_resource_path
import webbrowser
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("隆相.中国 Docker 管理工具 v1.0.0.1")
        self.setFixedSize(1000, 500)
        
        # 设置窗口图标
        logo_path = get_resource_path('logo.png')
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
            
        self.setup_ui()
        self.docker_ops = DockerOperations()
        self.setup_connections()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def setup_connections(self):
        self.docker_ops.progress_updated.connect(self.update_progress)
        self.docker_ops.operation_completed.connect(self.show_operation_result)
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        
        # 创建顶部容器，用于放置logo和标题
        top_container = QHBoxLayout()
        top_container.setContentsMargins(20, 10, 20, 10)  # 设置边距
        
        # 添加logo图片到左侧
        logo_label = QLabel()
        logo_path = get_resource_path('logo.png')
        if os.path.exists(logo_path):
            original_pixmap = QPixmap(logo_path)
            # 计算缩放比例，保持宽高比
            target_size = 120
            ratio = min(target_size / original_pixmap.width(), target_size / original_pixmap.height())
            new_width = int(original_pixmap.width() * ratio)
            new_height = int(original_pixmap.height() * ratio)
            
            # 缩放图片
            scaled_pixmap = original_pixmap.scaled(
                new_width, new_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # 创建一个固定大小的标签，居中显示图片
            logo_label.setFixedSize(target_size, target_size)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setStyleSheet("""
                QLabel {
                    padding: 5px;
                    background-color: transparent;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
            """)
            logo_label.setContentsMargins(10, 10, 10, 10)
            top_container.addWidget(logo_label)
        
        # 添加标题标签
        title_label = QLabel("隆相.中国 Docker 管理工具")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: 900;
                color: white;
                padding: 20px;
                margin: 0 50px;
                background-color: transparent;
            }
        """)
        
        # 使用弹性空间实现居中
        top_container.addStretch(1)
        top_container.addWidget(title_label)
        top_container.addStretch(1)
        
        # 将顶部容器添加到主布局
        main_layout.addLayout(top_container)
        
        # 创建按钮区域（居中显示）
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)  # 增加按钮之间的间距
        button_layout.setContentsMargins(20, 0, 20, 0)  # 设置左右边距
        
        # 创建功能按钮
        buttons = [
            ("容器自动运行", self.auto_restart_container),
            ("容器版本更新", self.update_container),
            ("容器镜像打包", self.commit_container),
            ("导出镜像", self.save_image),
            ("导入镜像", self.load_image)
        ]
        
        # 添加左侧弹性空间
        button_layout.addStretch(1)
        
        for text, callback in buttons:
            button = QPushButton(text)
            button.setFixedSize(160, 50)  # 统一按钮大小
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    color: white;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 14px;
                    font-weight: bold;
                    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                    border-color: rgba(255, 255, 255, 0.4);
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.1);
                    border-color: rgba(255, 255, 255, 0.2);
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                }
            """)
            button.clicked.connect(callback)
            button_layout.addWidget(button)
        
        # 添加右侧弹性空间
        button_layout.addStretch(1)
        
        button_container.setLayout(button_layout)
        
        # 创建分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        
        # 创建状态显示区域（下部30%）
        status_container = QWidget()
        status_container.setMinimumHeight(int(self.height() * 0.3))
        status_layout = QVBoxLayout()
        
        # 添加状态标签
        self.status_label = QLabel("当前状态: 就绪")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: white;
                padding: 5px;
                background-color: transparent;
            }
        """)
        
        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                text-align: center;
                height: 25px;
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
            }
            QProgressBar::chunk {
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 3px;
            }
        """)
        
        # 添加详细信息显示
        self.detail_label = QLabel()
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.8);
                padding: 5px;
                background-color: transparent;
            }
        """)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        status_layout.addWidget(self.detail_label)
        status_container.setLayout(status_layout)
        
        # 组装主布局
        main_layout.addStretch(1)
        main_layout.addWidget(button_container)
        main_layout.addStretch(1)
        main_layout.addWidget(line)
        main_layout.addWidget(status_container)
        
        central_widget.setLayout(main_layout)
        
        # 修改主窗口尺寸和样式
        self.setFixedSize(1000, 500)  # 1000 * 0.5 = 500
        self.setStyleSheet("""
            QMainWindow {
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
            }
        """)
        
    def update_progress(self, value):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(value)
        if value < 100:
            self.status_label.setText(f"当前状态: 正在执行 ({value}%)")
        else:
            self.status_label.setText("当前状态: 操作完成")
        
    def show_operation_result(self, success, message):
        msg_box = QMessageBox(self)
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
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 5px 15px;
                color: white;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border-color: rgba(255, 255, 255, 0.4);
            }
        """)
        msg_box.setWindowTitle("操作结果")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Information if success else QMessageBox.Icon.Critical)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        
    def confirm_operation(self, operation_name):
        dialog = ConfirmDialog(operation_name, self)
        return dialog.exec() == ConfirmDialog.DialogCode.Accepted
        
    def auto_restart_container(self):
        if not self.confirm_operation("容器自动运行"):
            return
            
        input_dialog = QInputDialog(self)
        input_dialog.setStyleSheet("""
            QDialog {
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
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 5px;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 5px 15px;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border-color: rgba(255, 255, 255, 0.4);
            }
        """)
        input_dialog.setWindowTitle("容器ID")
        input_dialog.setLabelText("请输入要设置自动重启的容器ID:")
        input_dialog.setInputMode(QInputDialog.InputMode.TextInput)
        input_dialog.setOkButtonText("确定")
        input_dialog.setCancelButtonText("取消")
        
        if input_dialog.exec() == QDialog.Accepted:
            container_id = input_dialog.textValue()
            if container_id:
                self.docker_ops.update_container_restart(container_id)
            
    def update_container(self):
        if not self.confirm_operation("容器版本更新"):
            return
            
        reply = QMessageBox.warning(
            self, "更新提示", 
            "更新过程可能需要较长时间，请勿进行其他操作。是否继续？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.docker_ops.update_container_version()
            
    def commit_container(self):
        if not self.confirm_operation("容器镜像打包"):
            return
            
        container_id, ok1 = QInputDialog.getText(
            self, "容器ID", "请输入要打包的容器ID:"
        )
        if not ok1 or not container_id:
            return
            
        image_name, ok2 = QInputDialog.getText(
            self, "镜像名称", "请输入镜像名称:"
        )
        if not ok2 or not image_name:
            return
            
        tag, ok3 = QInputDialog.getText(
            self, "标签", "请输入标签(版本号):"
        )
        if ok3 and tag:
            self.docker_ops.commit_container(container_id, image_name, tag)
            
    def save_image(self):
        if not self.confirm_operation("导出镜像"):
            return
            
        image_name, ok1 = QInputDialog.getText(
            self, "镜像名称", "请输入要导出的镜像名称:"
        )
        if not ok1 or not image_name:
            return
            
        file_dialog = QFileDialog(self)
        file_dialog.setStyleSheet("""
            QFileDialog {
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
            QLabel, QCheckBox {
                color: white;
            }
            QLineEdit, QComboBox {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 5px 15px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border-color: rgba(255, 255, 255, 0.4);
            }
        """)
        save_path = file_dialog.getSaveFileName(
            self, "选择保存位置", "", "Docker 镜像 (*.tar)"
        )[0]
        if save_path:
            self.docker_ops.save_image(image_name, save_path)
            
    def load_image(self):
        if not self.confirm_operation("导入镜像"):
            return
            
        file_path = QFileDialog.getOpenFileName(
            self, "选择镜像文件", "", "Docker 镜像 (*.tar)"
        )[0]
        if file_path:
            self.docker_ops.load_image(file_path)
            
    def show_context_menu(self, position):
        context_menu = QMenu(self)
        
        # 添加官网选项
        website_action = QAction("隆相.中国官网", self)
        website_action.triggered.connect(lambda: webbrowser.open("https://lonxang.com"))
        context_menu.addAction(website_action)
        
        # 添加电话选项
        phone_action = QAction("中国区业务电话: 17321008396", self)
        context_menu.addAction(phone_action)
        
        # 设置菜单样式
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
        
        # 显示菜单
        context_menu.exec(self.mapToGlobal(position))

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        # 蓝色渐变
        gradient.setColorAt(0, QColor("#D92196F3"))      # 蓝色起始
        gradient.setColorAt(0.7, QColor("#D92196F3"))    # 蓝色保持到70%
        gradient.setColorAt(0.85, QColor("#992196F3"))   # 蓝色85%处开始减淡
        # 红色渐变
        gradient.setColorAt(0.7, QColor("#99F44336"))    # 红色70%处开始淡入
        gradient.setColorAt(0.85, QColor("#D9F44336"))   # 红色85%处加深
        gradient.setColorAt(1, QColor("#D9F44336"))      # 红色结束
        painter.fillRect(self.rect(), gradient) 