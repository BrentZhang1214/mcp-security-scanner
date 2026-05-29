"""
用户使用示例 - 复制这段代码到任意位置运行

这个脚本演示如何使用 mcp-security-scanner 扫描工具列表
不需要依赖项目文件夹结构
"""

from mcp_security_scanner import MCPSecurityScanner, MCPTool

# 创建扫描器
scanner = MCPSecurityScanner()

# 定义要检查的工具
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
print("正在扫描工具...")
result = scanner.scan_tools_only(tools)

# 输出结果
print(f"\n安全评分: {result.score}/100")
print(f"发现 {len(result.vulnerabilities)} 个漏洞\n")

for vuln in result.vulnerabilities:
    print(f"[{vuln.severity}] {vuln.name}")
    print(f"  工具: {vuln.tool_name}")
    print(f"  问题: {vuln.description}")
    print(f"  建议: {vuln.remediation}\n")

# 保存报告
result.save_report("security-report.html")
print("报告已保存到: security-report.html")