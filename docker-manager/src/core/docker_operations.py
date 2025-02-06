import subprocess
import os
import time
from PySide6.QtCore import QObject, Signal

class DockerOperations(QObject):
    progress_updated = Signal(int)
    operation_completed = Signal(bool, str)
    
    def __init__(self):
        super().__init__()
        
    @staticmethod
    def check_docker_installed():
        """检查Docker是否已安装并正在运行"""
        try:
            # 检查docker命令是否存在
            subprocess.run(['docker', '--version'], 
                         check=True, 
                         capture_output=True,
                         text=True)
            
            # 检查docker服务是否运行
            result = subprocess.run(['docker', 'info'], 
                                 capture_output=True,
                                 text=True)
            
            if result.returncode == 0:
                return True, "Docker 运行正常"
            else:
                return False, "Docker 服务未启动，请启动 Docker 服务"
                
        except FileNotFoundError:
            return False, "未检测到 Docker，请先安装 Docker"
        except subprocess.CalledProcessError:
            return False, "Docker 服务异常，请检查 Docker 状态"
        except Exception as e:
            return False, f"Docker 检测失败: {str(e)}"
        
    def update_progress_simulation(self, operation_name):
        """模拟操作进度"""
        self.progress_updated.emit(0)
        self.status_label.setText(f"当前状态: 正在{operation_name}...")
        for i in range(0, 101, 10):
            time.sleep(0.2)  # 模拟操作耗时
            self.progress_updated.emit(i)
        
    def update_container_restart(self, container_id):
        try:
            self.progress_updated.emit(0)
            cmd = f"docker update --restart unless-stopped {container_id}"
            self.progress_updated.emit(50)
            result = subprocess.run(cmd, shell=True, check=True,
                                  capture_output=True, text=True)
            self.progress_updated.emit(100)
            self.operation_completed.emit(True, "容器更新成功")
            return True
        except subprocess.CalledProcessError as e:
            self.operation_completed.emit(False, f"错误: {e.stderr}")
            return False
            
    def update_container_version(self):
        try:
            self.progress_updated.emit(0)
            cmd = ("docker run --rm -v /var/run/docker.sock:/var/run/docker.sock "
                  "containrrr/watchtower --run-once open-webui")
            self.progress_updated.emit(30)
            result = subprocess.run(cmd, shell=True, check=True,
                                  capture_output=True, text=True)
            self.progress_updated.emit(100)
            self.operation_completed.emit(True, "版本更新成功")
            return True
        except subprocess.CalledProcessError as e:
            self.operation_completed.emit(False, f"错误: {e.stderr}")
            return False
            
    def commit_container(self, container_id, image_name, tag):
        try:
            self.progress_updated.emit(0)
            cmd = f"docker commit {container_id} {image_name}:{tag}"
            self.progress_updated.emit(50)
            result = subprocess.run(cmd, shell=True, check=True,
                                  capture_output=True, text=True)
            self.progress_updated.emit(100)
            self.operation_completed.emit(True, "镜像打包成功")
            return True
        except subprocess.CalledProcessError as e:
            self.operation_completed.emit(False, f"错误: {e.stderr}")
            return False
            
    def save_image(self, image_name, save_path):
        try:
            self.progress_updated.emit(0)
            self.operation_completed.emit(True, f"开始导出镜像: {image_name}")
            
            cmd = f"docker save -o {save_path} {image_name}"
            process = subprocess.Popen(
                cmd, 
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 模拟进度更新
            while process.poll() is None:
                self.progress_updated.emit(50)
                time.sleep(0.5)
            
            self.progress_updated.emit(100)
            self.operation_completed.emit(True, f"镜像已保存到: {save_path}")
            return True
        except subprocess.CalledProcessError as e:
            self.operation_completed.emit(False, f"错误: {e.stderr}")
            return False
            
    def load_image(self, file_path):
        try:
            self.progress_updated.emit(0)
            self.operation_completed.emit(True, f"开始导入镜像...")
            
            cmd = f"docker load -i {file_path}"
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 模拟进度更新
            while process.poll() is None:
                self.progress_updated.emit(50)
                time.sleep(0.5)
                
            self.progress_updated.emit(100)
            self.operation_completed.emit(True, "镜像导入成功")
            return True
        except subprocess.CalledProcessError as e:
            self.operation_completed.emit(False, f"错误: {e.stderr}")
            return False 