from mcp_security_scanner import MCPSecurityScanner, MCPTool

# 创建扫描器
scanner = MCPSecurityScanner()

# 定义你的工具列表（从你的MCP server获取）
tools = [
    MCPTool(
        name="get_weather",
        description="Get current weather for a location",
        input_schema={"type": "object", "properties": {"location": {"type": "string"}}}
    )
]

# 执行扫描
result = scanner.scan_tools_only(tools)
print(f"安全评分: {result.score}/100")

# 查看漏洞
for vuln in result.vulnerabilities:
    print(f"- [{vuln.severity}] {vuln.name}")

# 保存报告
result.save_report("report.html")