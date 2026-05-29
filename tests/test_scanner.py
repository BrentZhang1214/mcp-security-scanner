"""
Tests for MCP Security Scanner
"""

import pytest
from mcp_security_scanner import (
    MCPSecurityScanner,
    ScanResult,
    Vulnerability,
    Severity
)


def test_scanner_initialization():
    """测试扫描器初始化"""
    scanner = MCPSecurityScanner()
    assert scanner.timeout == 10
    assert scanner.verify_ssl is True
    
    # 自定义配置
    config = {'timeout': 30, 'verify_ssl': False}
    scanner = MCPSecurityScanner(config=config)
    assert scanner.timeout == 30
    assert scanner.verify_ssl is False


def test_scan_result_creation():
    """测试扫描结果创建"""
    result = ScanResult(
        url="https://example.com",
        score=85,
        vulnerabilities=[],
        checked_items=5,
        passed_items=5
    )
    
    assert result.url == "https://example.com"
    assert result.score == 85
    assert len(result.vulnerabilities) == 0
    assert result.checked_items == 5
    assert result.passed_items == 5


def test_vulnerability_creation():
    """测试漏洞创建"""
    vuln = Vulnerability(
        name="Test Vulnerability",
        severity=Severity.CRITICAL,
        description="This is a test vulnerability",
        remediation="Fix it",
        references=["https://example.com/ref"]
    )
    
    assert vuln.name == "Test Vulnerability"
    assert vuln.severity == Severity.CRITICAL
    assert vuln.description == "This is a test vulnerability"
    assert len(vuln.references) == 1


def test_score_calculation():
    """测试评分计算"""
    scanner = MCPSecurityScanner()
    
    # 无漏洞 = 100分
    score = scanner._calculate_score([])
    assert score == 100
    
    # 一个Critical = 80分
    vulns = [
        Vulnerability(
            name="Critical Issue",
            severity=Severity.CRITICAL,
            description="Test",
            remediation="Fix"
        )
    ]
    score = scanner._calculate_score(vulns)
    assert score == 80
    
    # 一个High = 90分
    vulns = [
        Vulnerability(
            name="High Issue",
            severity=Severity.HIGH,
            description="Test",
            remediation="Fix"
        )
    ]
    score = scanner._calculate_score(vulns)
    assert score == 90


def test_scan():
    """测试基本扫描功能"""
    scanner = MCPSecurityScanner()
    result = scanner.scan("https://example-mcp-server.com")
    
    assert result.url == "https://example-mcp-server.com"
    assert 0 <= result.score <= 100
    assert isinstance(result.vulnerabilities, list)


def test_save_json_report(tmp_path):
    """测试保存JSON报告"""
    result = ScanResult(
        url="https://example.com",
        score=85,
        vulnerabilities=[],
        checked_items=5,
        passed_items=5
    )
    
    json_file = tmp_path / "report.json"
    result.save_report(str(json_file), format="json")
    
    assert json_file.exists()
    
    import json
    with open(json_file) as f:
        data = json.load(f)
    
    assert data['url'] == "https://example.com"
    assert data['score'] == 85


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
