@echo off
REM Windows安装脚本 - 一键设置虚拟环境并安装依赖

echo ====================================
echo MCP Security Scanner - 安装向导
echo ====================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] 检测到Python版本:
python --version
echo.

REM 创建虚拟环境
echo [2/3] 创建虚拟环境...
if exist venv (
    echo 虚拟环境已存在，跳过创建
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
)
echo.

REM 激活虚拟环境并安装依赖
echo [3/3] 安装依赖...
call venv\Scripts\activate.bat
pip install -e .
if errorlevel 1 (
    echo [错误] 安装依赖失败
    pause
    exit /b 1
)

echo.
echo ====================================
echo ✓ 安装完成！
echo ====================================
echo.
echo 使用方法:
echo   1. 运行扫描: python run_scan.py
echo   2. 或激活虚拟环境后运行:
echo      venv\Scripts\activate.bat
echo      python examples\my_scan.py
echo.
pause
