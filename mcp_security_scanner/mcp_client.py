"""
MCP Client - 连接MCP Server并获取信息
"""

import json
import subprocess
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class MCPTool:
    """MCP工具信息"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    annotations: Optional[Dict[str, Any]] = None


@dataclass
class MCPResource:
    """MCP资源信息"""
    uri: str
    name: str
    description: Optional[str] = None
    mime_type: Optional[str] = None


class MCPClient:
    """MCP客户端 - 连接server并获取信息"""
    
    def __init__(self, url: str, timeout: int = 10):
        """
        初始化MCP客户端
        
        Args:
            url: MCP server地址（HTTP或stdio）
            timeout: 请求超时（秒）
        """
        self.url = url
        self.timeout = timeout
        self.tools: List[MCPTool] = []
        self.resources: List[MCPResource] = []
    
    def connect(self) -> bool:
        """
        连接MCP server并获取信息
        
        Returns:
            bool: 是否连接成功
        """
        # 判断连接类型
        if self.url.startswith('http://') or self.url.startswith('https://'):
            return self._connect_http()
        else:
            # 假设是stdio连接（命令行）
            return self._connect_stdio()
    
    def _connect_http(self) -> bool:
        """连接HTTP MCP server"""
        try:
            # MCP协议：发送initialize请求
            response = requests.post(
                self.url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {
                            "name": "mcp-security-scanner",
                            "version": "0.1.0"
                        }
                    }
                },
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                return False
            
            # 获取工具列表
            self._fetch_tools_http()
            
            return True
            
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    
    def _fetch_tools_http(self):
        """从HTTP server获取工具列表"""
        try:
            response = requests.post(
                self.url,
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'tools' in data['result']:
                    for tool_data in data['result']['tools']:
                        self.tools.append(MCPTool(
                            name=tool_data.get('name', ''),
                            description=tool_data.get('description', ''),
                            input_schema=tool_data.get('inputSchema', {}),
                            annotations=tool_data.get('annotations')
                        ))
        
        except Exception as e:
            print(f"获取工具列表失败: {e}")
    
    def _connect_stdio(self) -> bool:
        """连接stdio MCP server（命令行）"""
        # TODO: 实现stdio连接
        # 这需要启动子进程并通过stdin/stdout通信
        return False
    
    def get_tools(self) -> List[MCPTool]:
        """获取工具列表"""
        return self.tools
    
    def get_resources(self) -> List[MCPResource]:
        """获取资源列表"""
        return self.resources
