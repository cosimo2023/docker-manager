# docker-manager
Docker 管理工具是一个基于 PySide6 的桌面应用程序，用于简化 Docker 容器的管理。它提供了容器自动运行、版本更新、镜像打包、导入导出等功能。方便小白！

# Docker 管理工具

## 项目简介

Docker 管理工具是一个基于 PySide6 的桌面应用程序，用于简化 Docker 容器的管理。它提供了容器自动运行、版本更新、镜像打包、导入导出等功能。

## 功能特性

- **容器自动运行**：设置容器在启动时自动运行。
- **容器版本更新**：更新容器到最新版本。
- **容器镜像打包**：将容器打包为镜像。
- **导出镜像**：将镜像导出为文件。
- **导入镜像**：从文件导入镜像。

## 安装与运行

### 环境要求

- Python 3.x
- Docker

### 安装步骤

1. 克隆项目到本地：

   ```bash
   git clone https://github.com/cosimo2023/docker-manager.git
   cd docker-manager
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序：

   ```bash
   python src/main.py
   ```

### 打包为可执行文件

1. 确保 `app.ico` 和 `src/img/logo.png` 存在。
2. 运行打包脚本：

   ```bash
   python build.py
   ```

3. 在 `dist` 目录下找到 `DockerManager.exe`。

## 目录结构
docker-manager/
├── app.ico
├── build.py
├── requirements.txt
└── src/
├── init.py
├── main.py
├── utils.py
├── img/
│ └── logo.png
├── ui/
│ ├── init.py
│ ├── main_window.py
│ ├── password_dialog.py
│ └── confirm_dialog.py
└── core/
├── init.py
└── docker_operations.py

## 贡献

欢迎提交问题和请求。请确保在提交之前阅读贡献指南。

## 许可证

该项目使用 MIT 许可证。详细信息请参阅 LICENSE 文件。
