"""
MCP Security Scanner - 主扫描器
"""

from typing import List, Dict, Optional
from .models import Vulnerability, Severity, ScanResult
from .mcp_client import MCPClient, MCPTool
from .detectors import (
    PromptInjectionDetector,
    ToolPoisoningDetector,
    AuthenticationDetector,
    PathTraversalDetector
)


class MCPSecurityScanner:
    """MCP安全扫描器"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化扫描器
        
        Args:
            config: 配置选项
                - timeout: 请求超时（秒），默认10
                - user_agent: User-Agent字符串
                - verify_ssl: 是否验证SSL证书，默认True
        """
        self.config = config or {}
        self.timeout = self.config.get('timeout', 10)
        self.user_agent = self.config.get('user_agent', 'MCP-Security-Scanner/0.1.0')
        self.verify_ssl = self.config.get('verify_ssl', True)
        
        # 初始化检测器
        self.detectors = {
            'prompt_injection': PromptInjectionDetector(),
            'tool_poisoning': ToolPoisoningDetector(),
            'authentication': AuthenticationDetector(),
            'path_traversal': PathTraversalDetector()
        }
    
    def scan(self, url: str) -> ScanResult:
        """
        扫描MCP server
        
        Args:
            url: MCP server地址
        
        Returns:
            ScanResult: 扫描结果
        """
        vulnerabilities = []
        checked_items = 0
        passed_items = 0
        
        # 连接MCP server
        client = MCPClient(url, timeout=self.timeout)
        connected = client.connect()
        
        if not connected:
            # 连接失败，返回警告
            vulnerabilities.append(Vulnerability(
                name="Connection Failed",
                severity=Severity.INFO,
                description=f"无法连接到MCP server: {url}",
                remediation="检查server地址是否正确，server是否运行",
                references=[]
            ))
            checked_items = 1
            passed_items = 0
            
            return ScanResult(
                url=url,
                score=0,
                vulnerabilities=vulnerabilities,
                checked_items=checked_items,
                passed_items=passed_items
            )
        
        # 获取工具列表
        tools = client.get_tools()
        
        # 运行所有检测器
        for detector_name, detector in self.detectors.items():
            checked_items += 1
            
            # 检测漏洞
            if detector_name == 'authentication':
                # 认证检测器需要url参数
                vulns = detector.detect(url, tools)
            else:
                # 其他检测器只需要tools参数
                vulns = detector.detect(tools)
            
            vulnerabilities.extend(vulns)
            
            if not vulns:
                passed_items += 1
        
        # 计算安全评分
        score = self._calculate_score(vulnerabilities)
        
        return ScanResult(
            url=url,
            score=score,
            vulnerabilities=vulnerabilities,
            checked_items=checked_items,
            passed_items=passed_items
        )
    
    def scan_tools_only(self, tools: List[MCPTool]) -> ScanResult:
        """
        只扫描工具（不需要连接server）
        
        用于离线分析或测试
        
        Args:
            tools: 工具列表
        
        Returns:
            ScanResult: 扫描结果
        """
        vulnerabilities = []
        checked_items = 0
        passed_items = 0
        
        # 运行检测器（除了认证检测器）
        for detector_name, detector in self.detectors.items():
            if detector_name == 'authentication':
                # 跳过认证检测器（需要server连接）
                continue
            
            checked_items += 1
            vulns = detector.detect(tools)
            vulnerabilities.extend(vulns)
            
            if not vulns:
                passed_items += 1
        
        score = self._calculate_score(vulnerabilities)
        
        return ScanResult(
            url="offline-analysis",
            score=score,
            vulnerabilities=vulnerabilities,
            checked_items=checked_items,
            passed_items=passed_items
        )
    
    def _calculate_score(self, vulnerabilities: List[Vulnerability]) -> int:
        """
        计算安全评分
        
        基于漏洞严重性扣分：
        - Critical: -20分
        - High: -10分
        - Medium: -5分
        - Low: -2分
        - Info: -0分（不扣分）
        """
        score = 100
        
        for vuln in vulnerabilities:
            if vuln.severity == Severity.CRITICAL:
                score -= 20
            elif vuln.severity == Severity.HIGH:
                score -= 10
            elif vuln.severity == Severity.MEDIUM:
                score -= 5
            elif vuln.severity == Severity.LOW:
                score -= 2
        
        return max(0, min(100, score))


# 导出主要类
__all__ = [
    'MCPSecurityScanner',
    'ScanResult',
    'Vulnerability',
    'Severity',
    'MCPClient',
    'MCPTool'
]