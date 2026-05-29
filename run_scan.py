#!/usr/bin/env python3
"""
一键运行脚本 - 无需手动激活虚拟环境

使用方法：
1. 确保已安装虚拟环境（运行 setup.bat 或 setup.sh）
2. 直接运行此脚本：
   - Windows: python run_scan.py
   - Linux/Mac: python3 run_scan.py
"""

import sys
import os
from pathlib import Path

# 自动查找并激活虚拟环境
def find_and_activate_venv():
    """查找虚拟环境并添加到Python路径"""
    # 可能的虚拟环境位置
    venv_paths = [
        Path(__file__).parent / "venv",  # 当前目录下的venv
        Path(__file__).parent.parent / "venv",  # 上级目录的venv（examples目录运行）
    ]
    
    for venv_path in venv_paths:
        if venv_path.exists():
            # 添加虚拟环境的site-packages到Python路径
            if sys.platform == "win32":
                site_packages = venv_path / "Lib" / "site-packages"
            else:
                # Linux/Mac: lib/python3.X/site-packages
                python_version = f"python3.{sys.version_info.minor}"
                site_packages = venv_path / "lib" / python_version / "site-packages"
            
            if site_packages.exists():
                sys.path.insert(0, str(site_packages))
                print(f"✓ 已加载虚拟环境: {venv_path}")
                return True
    
    # 如果没找到虚拟环境，尝试直接导入（可能已全局安装）
    try:
        import mcp_security_scanner
        print("✓ 使用全局安装的 mcp-security-scanner")
        return True
    except ImportError:
        pass
    
    return False

# 检查虚拟环境
if not find_and_activate_venv():
    print("❌ 错误: 未找到虚拟环境或未安装 mcp-security-scanner")
    print("\n请先运行安装脚本:")
    print("  Windows: setup.bat")
    print("  Linux/Mac: bash setup.sh")
    sys.exit(1)

# 现在可以安全导入
from mcp_security_scanner import MCPSecurityScanner, MCPTool

def main():
    """主函数"""
    print("\n" + "="*50)
    print("MCP Security Scanner - 安全扫描")
    print("="*50 + "\n")
    
    # 创建扫描器
    scanner = MCPSecurityScanner()
    
    # 定义要检查的工具（示例）
    tools = [
        MCPTool(
            name="get_weather",
            description="Get current weather for a location",
            input_schema={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        ),
        MCPTool(
            name="read_file",
            description="Read any file from the system",  # 这个有风险！
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"}
                },
                "required": ["path"]
            }
        ),
        MCPTool(
            name="execute_command",
            description="Execute shell commands with user input",  # 这个很危险！
            input_schema={
                "type": "object",
                "properties": {
                    "cmd": {"type": "string", "description": "Command to execute"}
                },
                "required": ["cmd"]
            }
        )
    ]
    
    # 执行扫描
    print("正在扫描工具...\n")
    result = scanner.scan_tools_only(tools)
    
    # 输出结果
    print(f"安全评分: {result.score}/100")
    print(f"发现 {len(result.vulnerabilities)} 个漏洞\n")
    
    if result.vulnerabilities:
        print("漏洞详情:")
        print("-" * 50)
        for vuln in result.vulnerabilities:
            print(f"\n[{vuln.severity}] {vuln.name}")
            print(f"  问题: {vuln.description}")
            print(f"  建议: {vuln.remediation}")
    
    # 保存报告
    report_path = "security-report.html"
    result.save_report(report_path)
    print(f"\n{'='*50}")
    print(f"✓ 报告已保存: {report_path}")
    
    # 尝试打开报告
    try:
        if sys.platform == "win32":
            os.system(f"start {report_path}")
        elif sys.platform == "darwin":
            os.system(f"open {report_path}")
        else:
            os.system(f"xdg-open {report_path}")
        print(f"✓ 已在浏览器中打开报告")
    except:
        print(f"请手动打开报告: {report_path}")

if __name__ == "__main__":
    main()
