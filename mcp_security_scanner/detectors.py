"""
漏洞检测器实现
"""

import re
from typing import List
from .mcp_client import MCPTool
from .models import Vulnerability, Severity


class PromptInjectionDetector:
    """Prompt Injection检测器"""
    
    # 可疑指令关键词
    SUSPICIOUS_PATTERNS = [
        r'ignore\s+(previous|all)\s+(instructions?|rules?)',
        r'disregard\s+',
        r'forget\s+',
        r'override\s+',
        r'you\s+must\s+',
        r'system\s*:\s*',  # 模拟系统提示
        r'<!--.*?-->',  # HTML注释可能藏指令
        r'<script.*?>',  # 脚本标签
    ]
    
    def detect(self, tools: List[MCPTool]) -> List[Vulnerability]:
        """
        检测Prompt Injection漏洞
        
        检查工具描述是否包含指令性文本
        """
        vulnerabilities = []
        
        for tool in tools:
            # 检查工具描述
            if self._contains_suspicious_content(tool.description):
                vulnerabilities.append(Vulnerability(
                    name="Prompt Injection in Tool Description",
                    severity=Severity.CRITICAL,
                    description=f"工具 '{tool.name}' 的描述包含可疑指令",
                    remediation="确保工具描述是纯描述性文本，不包含任何指令或控制字符",
                    references=[
                        "https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/",
                        "https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks"
                    ]
                ))
            
            # 检查工具名称
            if self._contains_suspicious_content(tool.name):
                vulnerabilities.append(Vulnerability(
                    name="Prompt Injection in Tool Name",
                    severity=Severity.CRITICAL,
                    description=f"工具名称 '{tool.name}' 包含可疑内容",
                    remediation="工具名称应只包含字母、数字、下划线",
                    references=[
                        "https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/"
                    ]
                ))
            
            # 检查参数描述
            if tool.input_schema and 'properties' in tool.input_schema:
                for param_name, param_info in tool.input_schema['properties'].items():
                    if 'description' in param_info:
                        if self._contains_suspicious_content(param_info['description']):
                            vulnerabilities.append(Vulnerability(
                                name="Prompt Injection in Parameter Description",
                                severity=Severity.HIGH,
                                description=f"工具 '{tool.name}' 的参数 '{param_name}' 描述包含可疑指令",
                                remediation="参数描述应是纯文本，不包含指令",
                                references=[
                                    "https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/"
                                ]
                            ))
        
        return vulnerabilities
    
    def _contains_suspicious_content(self, text: str) -> bool:
        """检查文本是否包含可疑内容"""
        if not text:
            return False
        
        text_lower = text.lower()
        
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        
        return False


class ToolPoisoningDetector:
    """Tool Poisoning检测器"""
    
    # 危险的schema关键字
    DANGEROUS_SCHEMA_KEYS = [
        'default',  # 默认值可能包含恶意代码
        'examples',  # 示例可能包含恶意数据
        'const',  # 常量可能被滥用
    ]
    
    def detect(self, tools: List[MCPTool]) -> List[Vulnerability]:
        """
        检测Tool Poisoning漏洞
        
        检查工具schema是否包含恶意代码
        """
        vulnerabilities = []
        
        for tool in tools:
            schema = tool.input_schema
            
            if not schema:
                continue
            
            # 检查schema是否包含可执行代码
            if self._contains_executable_code(schema):
                vulnerabilities.append(Vulnerability(
                    name="Tool Poisoning - Executable Code in Schema",
                    severity=Severity.CRITICAL,
                    description=f"工具 '{tool.name}' 的schema包含可执行代码",
                    remediation="工具schema应该是纯数据定义，不包含可执行代码",
                    references=[
                        "https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks",
                        "https://www.cyberark.com/resources/threat-research-blog/poison-everywhere-no-output-from-your-mcp-server-is-safe"
                    ]
                ))
            
            # 检查默认值
            if self._has_dangerous_defaults(schema):
                vulnerabilities.append(Vulnerability(
                    name="Tool Poisoning - Dangerous Default Values",
                    severity=Severity.HIGH,
                    description=f"工具 '{tool.name}' 的schema包含可疑默认值",
                    remediation="检查默认值是否安全，避免包含命令或路径",
                    references=[
                        "https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks"
                    ]
                ))
        
        return vulnerabilities
    
    def _contains_executable_code(self, schema: dict) -> bool:
        """检查schema是否包含可执行代码"""
        schema_str = str(schema)
        
        # 检查可疑模式
        patterns = [
            r'__import__',
            r'eval\s*\(',
            r'exec\s*\(',
            r'compile\s*\(',
            r'os\.system',
            r'subprocess',
        ]
        
        for pattern in patterns:
            if re.search(pattern, schema_str):
                return True
        
        return False
    
    def _has_dangerous_defaults(self, schema: dict) -> bool:
        """检查是否有危险的默认值"""
        if 'properties' not in schema:
            return False
        
        for prop_name, prop_info in schema['properties'].items():
            if 'default' in prop_info:
                default_value = prop_info['default']
                
                # 检查默认值是否包含可疑内容
                if isinstance(default_value, str):
                    suspicious_patterns = [
                        r'^/',  # 路径
                        r'\.\./',  # 路径遍历
                        r'\|',  # 管道符
                        r';',  # 命令分隔符
                        r'&',  # 后台执行
                    ]
                    
                    for pattern in suspicious_patterns:
                        if re.search(pattern, default_value):
                            return True
        
        return False


class AuthenticationDetector:
    """认证检测器"""
    
    def detect(self, url: str, tools: List[MCPTool]) -> List[Vulnerability]:
        """
        检测认证漏洞
        
        检查server是否需要认证
        """
        vulnerabilities = []
        
        # 检查是否需要认证
        # 简单检查：尝试无认证访问
        # TODO: 实现更完善的认证检查
        
        # 如果工具涉及敏感操作但没有认证要求
        sensitive_tools = [
            'delete', 'remove', 'write', 'update', 'execute',
            'admin', 'config', 'secret', 'credential', 'token'
        ]
        
        has_sensitive_tool = False
        for tool in tools:
            tool_name_lower = tool.name.lower()
            for sensitive in sensitive_tools:
                if sensitive in tool_name_lower:
                    has_sensitive_tool = True
                    break
        
        if has_sensitive_tool:
            # TODO: 检查是否真的需要认证
            # 这里先假设需要认证
            pass
        
        return vulnerabilities


class PathTraversalDetector:
    """路径遍历检测器"""
    
    def detect(self, tools: List[MCPTool]) -> List[Vulnerability]:
        """检测路径遍历漏洞"""
        vulnerabilities = []
        
        # 检查工具是否接受文件路径参数
        for tool in tools:
            if not tool.input_schema or 'properties' not in tool.input_schema:
                continue
            
            for param_name, param_info in tool.input_schema['properties'].items():
                # 检查是否是路径参数
                if self._is_path_parameter(param_name, param_info):
                    # 检查是否有路径验证
                    if not self._has_path_validation(param_info):
                        vulnerabilities.append(Vulnerability(
                            name="Path Traversal Vulnerability",
                            severity=Severity.HIGH,
                            description=f"工具 '{tool.name}' 的参数 '{param_name}' 接受文件路径但缺少验证",
                            remediation="使用白名单验证文件路径，禁止../等特殊字符，限制访问范围",
                            references=[
                                "https://nvd.nist.gov/vuln/detail/CVE-2025-53110"
                            ]
                        ))
        
        return vulnerabilities
    
    def _is_path_parameter(self, param_name: str, param_info: dict) -> bool:
        """判断是否是路径参数"""
        path_keywords = ['path', 'file', 'dir', 'directory', 'folder', 'location']
        
        param_name_lower = param_name.lower()
        
        for keyword in path_keywords:
            if keyword in param_name_lower:
                return True
        
        # 检查description
        if 'description' in param_info:
            desc_lower = param_info['description'].lower()
            for keyword in path_keywords:
                if keyword in desc_lower:
                    return True
        
        return False
    
    def _has_path_validation(self, param_info: dict) -> bool:
        """检查是否有路径验证"""
        # 简单检查：是否有pattern或format限制
        if 'pattern' in param_info:
            return True
        
        if 'format' in param_info:
            return True
        
        return False
