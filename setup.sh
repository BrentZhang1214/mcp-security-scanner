#!/bin/bash
# Linux/Mac安装脚本 - 一键设置虚拟环境并安装依赖

echo "===================================="
echo "MCP Security Scanner - 安装向导"
echo "===================================="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "[1/3] 检测到Python版本:"
python3 --version
echo

# 创建虚拟环境
echo "[2/3] 创建虚拟环境..."
if [ -d "venv" ]; then
    echo "虚拟环境已存在，跳过创建"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[错误] 创建虚拟环境失败"
        exit 1
    fi
    echo "虚拟环境创建成功"
fi
echo

# 激活虚拟环境并安装依赖
echo "[3/3] 安装依赖..."
source venv/bin/activate
pip install -e .
if [ $? -ne 0 ]; then
    echo "[错误] 安装依赖失败"
    exit 1
fi

echo
echo "===================================="
echo "✓ 安装完成！"
echo "===================================="
echo
echo "使用方法:"
echo "  1. 运行扫描: python3 run_scan.py"
echo "  2. 或激活虚拟环境后运行:"
echo "     source venv/bin/activate"
echo "     python3 examples/my_scan.py"
echo