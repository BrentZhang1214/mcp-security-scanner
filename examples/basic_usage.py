"""
MCP Security Scanner - Example Usage

演示如何使用mcp-security-scanner评估MCP server安全性
"""

from mcp_security_scanner import MCPSecurityScanner

def example_basic_usage():
    """基本使用示例"""
    
    print("=== 基本使用 ===")
    
    # 创建扫描器
    scanner = MCPSecurityScanner()
    
    # 扫描MCP server（这里使用模拟URL）
    result = scanner.scan("https://example-mcp-server.com")
    
    # 显示评分
    print(f"安全评分: {result.score}/100")
    
    # 显示检查项
    print(f"检查项: {result.checked_items}")
    print(f"通过项: {result.passed_items}")
    
    # 显示漏洞
    if result.vulnerabilities:
        print(f"\n发现漏洞 ({len(result.vulnerabilities)}):")
        for vuln in result.vulnerabilities:
            print(f"- [{vuln.severity.value}] {vuln.name}")
            print(f"  描述: {vuln.description}")
            print(f"  修复: {vuln.remediation}")
    else:
        print("\n✅ 未发现漏洞")


def example_save_report():
    """保存报告示例"""
    
    print("\n=== 保存报告 ===")
    
    scanner = MCPSecurityScanner()
    result = scanner.scan("https://example-mcp-server.com")
    
    # 保存HTML报告
    result.save_report("security-report.html", format="html")
    print("HTML报告已保存到 security-report.html")
    
    # 保存JSON报告
    result.save_report("security-report.json", format="json")
    print("JSON报告已保存到 security-report.json")


def example_custom_config():
    """自定义配置示例"""
    
    print("\n=== 自定义配置 ===")
    
    # 配置扫描器
    config = {
        'timeout': 30,  # 30秒超时
        'user_agent': 'My-MCP-Scanner/1.0',
        'verify_ssl': False  # 测试环境不验证SSL
    }
    
    scanner = MCPSecurityScanner(config=config)
    result = scanner.scan("https://localhost:8080")
    
    print(f"本地server评分: {result.score}/100")


def example_ci_cd():
    """CI/CD集成示例"""
    
    print("\n=== CI/CD集成 ===")
    
    scanner = MCPSecurityScanner()
    result = scanner.scan("https://staging-mcp-server.com")
    
    # 设置最低评分阈值
    MIN_SCORE = 70
    
    if result.score < MIN_SCORE:
        print(f"❌ 安全评分过低: {result.score}/100 (最低要求: {MIN_SCORE})")
        print("需要修复以下问题:")
        for vuln in result.vulnerabilities:
            if vuln.severity.value in ["Critical", "High"]:
                print(f"- {vuln.name}")
        # 在CI/CD中抛出异常
        # raise Exception(f"Security score too low: {result.score}")
    else:
        print(f"✅ 安全评分合格: {result.score}/100")


def example_filter_vulnerabilities():
    """过滤漏洞示例"""
    
    print("\n=== 过滤漏洞 ===")
    
    scanner = MCPSecurityScanner()
    result = scanner.scan("https://example-mcp-server.com")
    
    # 只显示Critical和High漏洞
    critical_vulns = [
        v for v in result.vulnerabilities 
        if v.severity.value in ["Critical", "High"]
    ]
    
    if critical_vulns:
        print(f"高危漏洞 ({len(critical_vulns)}):")
        for vuln in critical_vulns:
            print(f"- [{vuln.severity.value}] {vuln.name}")
    else:
        print("✅ 无高危漏洞")


if __name__ == "__main__":
    # 运行所有示例
    example_basic_usage()
    example_save_report()
    example_custom_config()
    example_ci_cd()
    example_filter_vulnerabilities()
    
    print("\n=== 完成 ===")
    print("查看生成的报告文件了解更多详情")