# MCP Security Scanner

**Security Assessment for MCP Servers | MCP 服务器安全评估工具**

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

One-click security scanner for MCP (Model Context Protocol) servers. Detect TOP 25 MCP vulnerabilities with automatic scoring.

### Quick Start (2 Steps)

#### Step 1: Install

**Windows**:
```bash
setup.bat
```

**Linux/Mac**:
```bash
bash setup.sh
```

The installation script will automatically create a virtual environment and install all dependencies.

#### Step 2: Run Scan

```bash
# Windows
python run_scan.py

# Linux/Mac
python3 run_scan.py
```

This will generate and open `security-report.html` automatically.

---

### Advanced Usage

#### Custom Scan

Create your own scan script `my_scan.py`:

```python
from mcp_security_scanner import MCPSecurityScanner, MCPTool

scanner = MCPSecurityScanner()

# Define your tool list
tools = [
    MCPTool(
        name="get_weather",
        description="Get current weather for a location",
        input_schema={"type": "object", "properties": {"location": {"type": "string"}}}
    )
]

# Execute scan
result = scanner.scan_tools_only(tools)
print(f"Security Score: {result.score}/100")

# View vulnerabilities
for vuln in result.vulnerabilities:
    print(f"- [{vuln.severity}] {vuln.name}")

# Save report
result.save_report("report.html")
```

#### Scan Real MCP Server

```python
from mcp_security_scanner import MCPSecurityScanner

scanner = MCPSecurityScanner()
result = scanner.scan("http://localhost:8080")  # Your MCP server URL

print(f"Security Score: {result.score}/100")
result.save_report("my-report.html")
```

---

### Features

1. **Security Scoring** - Automatic assessment based on TOP 25 MCP Vulnerabilities:
   - 90-100: Secure
   - 70-89: Good
   - 50-69: Needs Improvement
   - 0-49: Dangerous

2. **Vulnerability Detection**:
   - Prompt Injection (Critical)
   - Tool Poisoning (Critical)
   - Command Injection (Critical)
   - Unauthenticated Access (Critical)
   - Token/Credential Theft (High)
   - Path Traversal (High)

3. **Risk Reports** - Generate HTML or JSON format reports with:
   - Overall score
   - Vulnerability list
   - Remediation suggestions
   - Compliance checks

---

### Developer Mode

```bash
# Clone repository
git clone https://github.com/BrentZhang1214/mcp-security-scanner
cd mcp-security-scanner

# Install
bash setup.sh  # Linux/Mac
setup.bat      # Windows

# Run tests
pytest tests/

# View examples
ls examples/
```

---

<a name="中文"></a>
## 中文

一键扫描MCP服务器安全漏洞，基于TOP 25 MCP Vulnerabilities自动评分。

### 快速开始（2步上手）

#### 第1步：安装

**Windows用户**：
```bash
setup.bat
```

**Linux/Mac用户**：
```bash
bash setup.sh
```

安装脚本会自动创建虚拟环境并安装所有依赖。

#### 第2步：运行扫描

```bash
# Windows
python run_scan.py

# Linux/Mac
python3 run_scan.py
```

运行后会自动生成并打开 `security-report.html` 报告。

---

### 高级用法

#### 自定义扫描

创建自己的扫描脚本 `my_scan.py`：

```python
from mcp_security_scanner import MCPSecurityScanner, MCPTool

scanner = MCPSecurityScanner()

# 定义你的工具列表
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
```

#### 扫描真实MCP Server

```python
from mcp_security_scanner import MCPSecurityScanner

scanner = MCPSecurityScanner()
result = scanner.scan("http://localhost:8080")  # 你的MCP server地址

print(f"安全评分: {result.score}/100")
result.save_report("my-report.html")
```

---

### 核心功能

1. **安全评分** - 基于TOP 25 MCP Vulnerabilities自动评估：
   - 90-100：安全
   - 70-89：良好
   - 50-69：需改进
   - 0-49：危险

2. **漏洞检测**：
   - Prompt Injection（Critical）
   - Tool Poisoning（Critical）
   - Command Injection（Critical）
   - Unauthenticated Access（Critical）
   - Token/Credential Theft（High）
   - Path Traversal（High）

3. **风险报告** - 生成HTML或JSON格式报告：
   - 总体评分
   - 漏洞列表
   - 修复建议
   - 合规性检查

---

### 开发者模式

```bash
# 克隆仓库
git clone https://github.com/BrentZhang1214/mcp-security-scanner
cd mcp-security-scanner

# 安装
bash setup.sh  # Linux/Mac
setup.bat      # Windows

# 运行测试
pytest tests/

# 查看示例
ls examples/
```

---

## Acknowledgments | 致谢

- [Adversa AI](https://adversa.ai/) - TOP 25 MCP Vulnerabilities
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP Specification
- [OWASP](https://owasp.org/) - Security Best Practices

---

## License | 许可证

MIT License

---

## Changelog | 更新日志

### v0.1.0 (2026-05-29)

- Initial release
- Support TOP 25 vulnerability detection
- Security scoring system
- HTML/JSON report generation
- One-click installation scripts for Windows/Linux/Mac
