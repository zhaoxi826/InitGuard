# 使用轻量级的 Python 基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装 uv 用于管理依赖
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_SYSTEM_PYTHON=1

# 复制依赖文件 (假设你用了 pyproject.toml)
COPY pyproject.toml .
RUN uv pip install .

# 复制项目代码
COPY . .

# 创建日志目录 (防止代码里没写创建逻辑)
RUN mkdir -p data/logs/task

# 暴露 FastAPI 默认端口
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"]