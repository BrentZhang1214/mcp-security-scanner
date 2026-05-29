# MCP Security Scanner - 快速使用指南

## 安装

### 方式1：虚拟环境安装（推荐）

```bash
cd /mnt/f/Linux/hermes/projects/mcp-security-scanner

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装工具
pip install -e .

# 验证安装
python -c "from mcp_security_scanner import MCPSecurityScanner; print('✅ 安装成功')"
```

### 方式2：直接使用（无需安装）

```bash
cd /mnt/f/Linux/hermes/projects/mcp-security-scanner

# 设置PYTHONPATH后运行
PYTHONPATH=/mnt/f/Linux/hermes/projects/mcp-security-scanner python3 examples/test_real_detection.py
```

## 使用

### 1. 离线分析工具列表

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行测试示例
python examples/test_real_detection.py

# 查看报告
# 生成 real-detection-report.html
```

### 2. 扫描真实MCP server

```python
from mcp_security_scanner import MCPSecurityScanner

# 创建扫描器
scanner = MCPSecurityScanner()

# 扫描MCP server
result = scanner.scan("https://your-mcp-server.com")

# 查看评分
print(f"安全评分: {result.score}/100")

# 查看漏洞
for vuln in result.vulnerabilities:
    print(f"[{vuln.severity.value}] {vuln.name}")

# 保存报告
result.save_report("report.html")
```

### 3. 自定义配置

```python
from mcp_security_scanner import MCPSecurityScanner

# 自定义配置
config = {
    'timeout': 30,  # 30秒超时
    'verify_ssl': False  # 不验证SSL（测试环境）
}

scanner = MCPSecurityScanner(config=config)
result = scanner.scan("https://localhost:8080")
```

## 测试示例

项目包含多个测试示例：

### test_real_detection.py
测试真实漏洞检测功能，包含：
- Prompt Injection示例
- Tool Poisoning示例
- Path Traversal示例

运行：
```bash
source venv/bin/activate
python examples/test_real_detection.py
```

输出：
```
安全评分: 30/100
发现漏洞 (6):
[Critical] Prompt Injection in Tool Description
[High] Tool Poisoning - Dangerous Default Values
[High] Path Traversal Vulnerability
...
```

### basic_usage.py
演示基本功能：
- 扫描MCP server
- 保存报告
- CI/CD集成
- 漏洞过滤

运行：
```bash
source venv/bin/activate
python examples/basic_usage.py
```

## 报告格式

### HTML报告
- 可视化界面
- 评分颜色编码（绿色/黄色/红色）
- 漏洞详情和修复建议
- 参考链接

### JSON报告
```json
{
  "url": "https://example.com",
  "score": 30,
  "vulnerabilities": [
    {
      "name": "Prompt Injection",
      "severity": "Critical",
      "description": "...",
      "remediation": "..."
    }
  ]
}
```

## 检测能力

当前支持检测：

| 漏洞类型 | 严重性 | 检测项 |
|---------|--------|--------|
| Prompt Injection | Critical | 工具描述、参数描述中的指令性文本 |
| Tool Poisoning | Critical | schema中的可执行代码、危险默认值 |
| Path Traversal | High | 文件路径参数缺少验证 |
| Authentication | High | 敏感工具缺少认证 |

## 下一步

- 扫描你自己的MCP server
- 集成到CI/CD流程
- 扩展检测规则
- 贡献代码

## 常见问题

### Q: 为什么创建虚拟环境？
A: Debian 12 PEP 668限制，不能直接pip安装系统级包。虚拟环境是推荐做法。

### Q: 如何扫描真实MCP server？
A: 确保server运行并提供HTTP接口，然后使用`scanner.scan("https://server-url")`。

### Q: 检测结果准确吗？
A: 当前是静态分析，可能有误报。建议结合人工审查。

### Q: 如何贡献？
A: 提Issue、PR，或扩展检测规则。详见GitHub。

---

**项目路径**：`/mnt/f/Linux/hermes/projects/mcp-security-scanner`

**现在可以用这个工具了！** 🎉
