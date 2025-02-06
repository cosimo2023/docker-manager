VERSION = "v1.0.0.1"
APP_NAME = "隆相.中国 Docker 管理工具"
FULL_APP_NAME = f"{APP_NAME} {VERSION}"

# 环境检查信息
DOCKER_CHECK_TITLE = "环境检查"
DOCKER_CHECK_MESSAGE = """
Docker 环境检查

状态: {status}

详细信息: 
{message}

请确保:
• 已安装 Docker Desktop
• Docker 服务已启动
• Docker 命令可用

如需帮助，请访问:
https://docs.docker.com/desktop/install/windows-install/
""" 