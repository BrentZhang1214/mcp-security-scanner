"""
测试漏洞检测功能 - 模拟漏洞场景
"""

from mcp_security_scanner import (
    MCPSecurityScanner,
    Vulnerability,
    Severity
)


def test_vulnerability_detection():
    """测试漏洞检测"""
    scanner = MCPSecurityScanner()
    
    # 模拟发现漏洞
    vulnerabilities = [
        Vulnerability(
            name="Prompt Injection",
            severity=Severity.CRITICAL,
            description="工具描述包含可能的恶意指令",
            remediation="确保工具描述是纯描述性文本，不包含任何指令",
            references=["https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/"]
        ),
        Vulnerability(
            name="Unauthenticated Access",
            severity=Severity.HIGH,
            description="MCP server不需要认证即可访问",
            remediation="实现OAuth 2.1认证或API key验证"
        ),
        Vulnerability(
            name="Path Traversal",
            severity=Severity.MEDIUM,
            description="文件访问未正确验证路径",
            remediation="使用白名单验证文件路径，禁止../等特殊字符"
        )
    ]
    
    # 计算评分
    score = scanner._calculate_score(vulnerabilities)
    print(f"安全评分: {score}/100")
    
    # 显示评分结果
    if score >= 90:
        print("✅ 安全")
    elif score >= 70:
        print("⚠️ 良好")
    elif score >= 50:
        print("🔶 需改进")
    else:
        print("❌ 危险")
    
    # 显示漏洞详情
    print(f"\n发现漏洞 ({len(vulnerabilities)}):")
    for vuln in vulnerabilities:
        print(f"\n[{vuln.severity.value}] {vuln.name}")
        print(f"  描述: {vuln.description}")
        print(f"  修复: {vuln.remediation}")
        if vuln.references:
            print(f"  参考: {', '.join(vuln.references)}")
    
    # 验证评分计算
    # 100 - 20(Critical) - 10(High) - 5(Medium) = 65
    expected_score = 100 - 20 - 10 - 5
    assert score == expected_score, f"评分错误：期望{expected_score}，实际{score}"
    print(f"\n✅ 评分计算正确: {score}/100")


if __name__ == "__main__":
    test_vulnerability_detection()
