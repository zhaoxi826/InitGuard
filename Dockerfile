# 使用轻量级的 Python 镜像
FROM python:3.11-slim

# 安装系统依赖 (pg_dump 需要 postgresql-client)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv (高性能依赖管理工具)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 设置工作目录
WORKDIR /app

# 先拷贝依赖文件 (利用 Docker 缓存层优化)
COPY pyproject.toml uv.lock ./

# 安装依赖到系统环境 (不使用虚拟环境，保持镜像简洁)
RUN uv pip install --system -r pyproject.toml

# 拷贝源代码
COPY . .

# 创建日志目录 (确保程序有地方写日志)
RUN mkdir -p logs

# 设置启动命令 (暂定为 test.py，后期改为 main.py)
CMD ["python", "test.py"]