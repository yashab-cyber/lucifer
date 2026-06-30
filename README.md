# Lucifer - AI-Powered Cybersecurity Automation Assistant

<div align="center">

<img src="gui/public/icon.svg" alt="Lucifer Logo" width="150" height="150"/>

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**An intelligent AI assistant that combines terminal output capture and computer vision to automate penetration testing and bug bounty hunting workflows.**

### Created by Yashab Alam

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Yashab%20Alam-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yashab-alam)
[![Instagram](https://img.shields.io/badge/Instagram-@yashabcyber-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/yashabcyber)
[![X](https://img.shields.io/badge/X-@Yashab__cyber-000000?style=flat&logo=x&logoColor=white)](https://x.com/Yashab_cyber)
[![Threads](https://img.shields.io/badge/Threads-@yashabcyber-000000?style=flat&logo=threads&logoColor=white)](https://www.threads.net/@yashabcyber)
[![Email](https://img.shields.io/badge/Email-yashabalam9@gmail.com / yashabalam707@gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:yashabalam9@gmail.com?cc=yashabalam707@gmail.com)

**[Support this project](DONATE.md)** ❤️

</div>

---

## 🔥 Features

### Core Capabilities

- **🖥️ Terminal Output Capture**: Real-time monitoring and analysis of terminal commands and output
- **👁️ Computer Vision**: Screenshot capture, OCR text extraction, and GUI element detection
- **🤖 AI-Powered Analysis**: Integration with Claude, GPT-4, or local Ollama models for intelligent insights
- **🔄 Automated Workflows**: Pre-built penetration testing workflows (recon, webapp, exploit, privesc)
- **📊 Report Generation**: Automated HTML, Markdown, and JSON report creation
- **🎥 Screen Recording**: Record entire testing sessions for documentation
- **🔒 Security Audit Logging**: Track all commands and sensitive operations

### AI Integration

- **Anthropic Claude**: Claude 3.5 Sonnet with vision capabilities
- **OpenAI**: GPT-4 Turbo with vision support
- **Ollama**: Local/offline AI models for privacy-conscious operations

### Automation Features

- Intelligent command suggestions based on context
- Pattern-based terminal monitoring
- Automated reconnaissance workflows
- Vulnerability exploitation assistance
- Privilege escalation enumeration
- Custom workflow creation via AI

---

## 📋 Requirements

### System Requirements

- **OS**: Kali Linux, Parrot OS, BlackArch, or any Debian/Ubuntu-based security distribution
- **Python**: 3.10 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 2GB for dependencies and logs

### Security Tools (Optional)

The following tools enhance Lucifer's capabilities but are not required:

- `nmap` - Network scanning
- `gobuster` - Directory enumeration
- `nikto` - Web server scanning
- `sqlmap` - SQL injection testing
- `metasploit-framework` - Exploitation framework
- `searchsploit` - Exploit database
- `whatweb` - Web technology identification

---

## 🚀 Installation

### Quick Install (Kali Linux)

```bash
# Clone the repository
git clone https://github.com/yashab-cyber/lucifer.git
cd lucifer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Lucifer
pip install -e .

# Install system dependencies (Tesseract for OCR)
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# Copy and configure environment
cp .env.example .env
nano .env  # Add your AI API keys
```

### Configuration

Edit `.env` file with your settings:

```bash
# Choose your AI provider
AI_PROVIDER=anthropic  # or openai, ollama

# Add API key for your provider
ANTHROPIC_API_KEY=your_anthropic_key_here
# or
OPENAI_API_KEY=your_openai_key_here

# Configure settings
LOG_LEVEL=INFO
AUTO_SUGGEST_COMMANDS=true
CONFIRMATION_REQUIRED=true
```

### Verify Installation

```bash
lucifer config-check
```

---

## 💻 Usage

### Interactive Mode

Start Lucifer in interactive mode for full control:

```bash
lucifer start --interactive
```

**Available Commands:**

- `analyze` - Analyze current terminal and screen state
- `suggest` - Get AI-powered next step suggestions
- `execute <command>` - Execute command with AI assistance
- `workflow <name> <target>` - Run automated workflow
- `record` / `stop-record` - Screen recording
- `report` - Generate penetration testing report
- `help` - Show all commands

### Quick Scan

Perform rapid reconnaissance on a target:

```bash
lucifer quick-scan 192.168.1.100
```

### Workflow Mode

Execute specific workflows:

```bash
# Reconnaissance workflow
lucifer start -t 192.168.1.100 -w recon

# Web application testing
lucifer start -t example.com -w webapp

# Exploitation workflow
lucifer start -t 192.168.1.100 -w exploit

# Privilege escalation
lucifer start -t localhost -w privesc
```

### List Available Workflows

```bash
lucifer workflows
```

---

## 🎯 Workflow Examples

### 1. Bug Bounty Reconnaissance

```bash
# Start interactive mode
lucifer start -i

# In Lucifer shell:
lucifer> workflow recon target.com
lucifer> analyze
lucifer> suggest
lucifer> report
```

### 2. Web Application Testing

```bash
# Direct workflow execution
lucifer start -t https://target.com -w webapp

# The workflow will:
# - Enumerate directories with gobuster
# - Scan for vulnerabilities with nikto
# - Test for SQL injection with sqlmap
# - Generate comprehensive report
```

### 3. Network Penetration Testing

```python
# Python API usage
from lucifer import LuciferAssistant
import asyncio

async def main():
    async with LuciferAssistant() as assistant:
        # Start monitoring
        await assistant.start_terminal_monitoring()
        
        # Run recon
        results = await assistant.run_automated_recon("192.168.1.0/24")
        
        # Get AI suggestions
        suggestions = await assistant.suggest_next_actions()
        
        # Generate report
        report = await assistant.generate_report()
        print(f"Report: {report}")

asyncio.run(main())
```

---

## 📚 Documentation

### Architecture

```
lucifer/
├── src/lucifer/
│   ├── core/
│   │   ├── assistant.py          # Main AI assistant
│   │   ├── terminal_capture.py   # Terminal monitoring
│   │   ├── vision.py             # Computer vision
│   │   ├── ai_engine.py          # AI integration
│   │   └── config.py             # Configuration
│   ├── automation/
│   │   └── workflows.py          # Pentest workflows
│   ├── utils/
│   │   ├── logger.py             # Logging utilities
│   │   └── report_generator.py  # Report generation
│   └── cli.py                    # Command-line interface
├── tests/                        # Unit tests
├── pyproject.toml               # Project configuration
└── README.md
```

### Key Components

#### Terminal Capture

Captures and monitors terminal output in real-time:

```python
from lucifer.core.terminal_capture import TerminalCapture

capture = TerminalCapture(buffer_size=10000)
capture.start_shell_capture("/bin/bash")
output = capture.get_recent_output(lines=50)
```

#### Computer Vision

Screenshot capture and analysis:

```python
from lucifer.core.vision import ScreenCapture, OCREngine

# Capture screenshot
screen = ScreenCapture()
screenshot = screen.capture_screenshot()

# Extract text with OCR
ocr = OCREngine()
text = ocr.extract_text(screenshot)
```

#### AI Analysis

Analyze terminal output and screenshots:

```python
from lucifer.core.ai_engine import create_ai_engine

engine = create_ai_engine()
analysis = await engine.analyze_terminal_output(output)
suggestions = await engine.suggest_next_steps(output)
```

---

## 🔒 Security Considerations

### Dangerous Command Filtering

Lucifer includes built-in protection against dangerous commands:

- `rm -rf` - Recursive deletion
- `dd if=` - Disk operations
- `mkfs` - Filesystem formatting
- Fork bombs and destructive operations

Configure in `.env`:
```bash
DANGEROUS_COMMANDS_FILTER=true
CONFIRMATION_REQUIRED=true
```

### Audit Logging

All commands and security events are logged:

```bash
AUDIT_LOG_ENABLED=true
AUDIT_LOG_FILE=logs/audit.log
```

### API Key Security

- Never commit `.env` file to version control
- Use environment variables in production
- Rotate API keys regularly
- Consider using Ollama for offline/sensitive operations

---

## 🧪 Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# With coverage
pytest --cov=src/lucifer --cov-report=html

# Type checking
mypy src/lucifer

# Code formatting
black src/lucifer
ruff check src/lucifer
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/lucifer.git
cd lucifer

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests before committing
pytest
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**IMPORTANT**: Lucifer is designed for **authorized security testing only**. 

- Only use on systems you own or have explicit permission to test
- Unauthorized access to computer systems is illegal
- Users are responsible for compliance with applicable laws
- The authors assume no liability for misuse of this tool

By using Lucifer, you agree to use it responsibly and ethically.

---

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) - Claude AI
- [OpenAI](https://openai.com/) - GPT-4
- [Ollama](https://ollama.ai/) - Local AI models
- Kali Linux and the cybersecurity community
- All open-source contributors

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yashab-cyber/lucifer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yashab-cyber/lucifer/discussions)
- **Documentation**: [Wiki](https://github.com/yashab-cyber/lucifer/wiki)

---

## 🗺️ Roadmap

- [x] Desktop GUI application
- [ ] Multi-target parallel scanning
- [ ] Integration with Burp Suite
- [ ] Custom plugin system
- [ ] Machine learning-based vulnerability detection
- [ ] Automated exploit generation
- [ ] Cloud deployment support
- [ ] Team collaboration features

---

## 👤 Author

**Yashab Alam**

- LinkedIn: [linkedin.com/in/yashab-alam](https://www.linkedin.com/in/yashab-alam)
- Instagram: [@yashabcyber](https://www.instagram.com/yashabcyber)
- 🐦 X (Twitter): [@Yashab_cyber](https://x.com/Yashab_cyber)
- 🧵 Threads: [@yashabcyber](https://www.threads.net/@yashabcyber)
- Email: yashabalam9@gmail.com / yashabalam707@gmail.com

**[Support this project](DONATE.md)** ❤️

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Thanks to the cybersecurity community for inspiration
- All open-source tool developers whose work makes this possible
- AI model providers (Anthropic, OpenAI, Ollama) for powerful inference capabilities

---

<div align="center">

Made with ❤️ by **Yashab Alam**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/yashab-alam)
[![Instagram](https://img.shields.io/badge/Instagram-Follow-E4405F?style=for-the-badge&logo=instagram)](https://www.instagram.com/yashabcyber)
[![X](https://img.shields.io/badge/X-Follow-000000?style=for-the-badge&logo=x)](https://x.com/Yashab_cyber)
[![Threads](https://img.shields.io/badge/Threads-Follow-000000?style=for-the-badge&logo=threads)](https://www.threads.net/@yashabcyber)

</div>

<div align="center">

**Made with ❤️ for the cybersecurity community**

⭐ Star us on GitHub if you find Lucifer useful!

</div>