# 设置基础镜像为 Python 3.9 Alpine 版
FROM python:3.9-alpine

# 设置工作目录
WORKDIR /magnet

# 将当前目录下的所有文件复制到容器中的 /magnet 目录下
COPY ai_analyzer/ .

COPY requirements.txt .

# 安装依赖项
RUN apk add --no-cache freetype-dev gcc gfortran musl-dev build-base && pip install --no-cache-dir -r requirements.txt

# 启动 Python 程序
CMD ["python", "main.py", "--config", "config.yaml"]