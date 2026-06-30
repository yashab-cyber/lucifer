# Lucifer Quick Start Guide

<div align="center">

<img src="gui/public/icon.svg" alt="Lucifer Logo" width="100" height="100"/>

### Created by Yashab Alam
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Yashab%20Alam-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yashab-alam)
[![Instagram](https://img.shields.io/badge/Instagram-@yashabcyber-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/yashabcyber)
[![X](https://img.shields.io/badge/X-@Yashab__cyber-000000?style=flat&logo=x&logoColor=white)](https://x.com/Yashab_cyber)
[![Threads](https://img.shields.io/badge/Threads-@yashabcyber-000000?style=flat&logo=threads&logoColor=white)](https://www.threads.net/@yashabcyber)

</div>

## Welcome to Lucifer! 🔥

This guide will help you get started with Lucifer, the AI-powered cybersecurity automation assistant.

## Prerequisites

- Kali Linux, Parrot OS, or any Debian-based security distribution
- Python 3.10 or higher
- Node.js 16+ (for GUI)
- At least 4GB RAM
- Internet connection (for AI API calls, unless using Ollama)

## Installation

### Option 1: GUI Desktop Application (Recommended)

```bash
# Install GUI application
./install-gui.sh

# Create desktop entry and shortcuts
./create-desktop-entry.sh
```

This will:
- Install Node.js dependencies
- Build the Electron desktop app
- Create desktop shortcuts
- Add Lucifer to your application menu

### Option 2: CLI Installation

```bash
./install.sh
```

This will:
- Check Python version
- Install system dependencies
- Create virtual environment
- Install Lucifer
- Set up configuration files

### Option 3: Manual Installation

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install Lucifer
pip install -e .

# 3. Install system dependencies
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# 4. Configure environment
cp .env.example .env
nano .env  # Add your AI API keys
```

## Configuration

### 1. Get an AI API Key

Choose one of the following providers:

#### Anthropic Claude (Recommended)
- Visit: https://console.anthropic.com/
- Create account and get API key
- Set in `.env`: `ANTHROPIC_API_KEY=your_key_here`

#### OpenAI
- Visit: https://platform.openai.com/
- Create account and get API key
- Set in `.env`: `OPENAI_API_KEY=your_key_here`

#### Ollama (Local/Offline)
- Install: `curl https://ollama.ai/install.sh | sh`
- Pull a model: `ollama pull llama2`
- Set in `.env`: `AI_PROVIDER=ollama`

### 2. Edit Configuration

```bash
nano .env
```

Key settings:
```bash
AI_PROVIDER=anthropic          # Your chosen provider
ANTHROPIC_API_KEY=sk-...      # Your API key
LOG_LEVEL=INFO                 # Logging verbosity
CONFIRMATION_REQUIRED=true     # Safety feature
```

## First Run

### Launch GUI Application

After installation, you can launch Lucifer from:
- **Application Menu**: Search for "Lucifer" in your app launcher
- **Desktop Shortcut**: Double-click the Lucifer icon on your desktop
- **Command Line**: Run `./gui/lucifer-gui`

### CLI Interactive Mode

```bash
lucifer start --interactive
```

### Check Configuration

```bash
lucifer config-check
```

This verifies:
- Python version
- API credentials
- Directory permissions
- Dependencies

Try these commands:
```
lucifer> help              # Show all commands
lucifer> analyze           # Analyze current state
lucifer> suggest           # Get AI suggestions
lucifer> workflow recon scanme.nmap.org  # Run workflow
lucifer> report            # Generate report
lucifer> exit              # Exit
```

## Basic Examples

### 1. Quick Reconnaissance

```bash
lucifer quick-scan scanme.nmap.org
```

This performs a fast reconnaissance scan using automated workflows.

### 2. Web Application Testing

```bash
lucifer start -t https://example.com -w webapp
```

Runs a complete web application security assessment.

### 3. Custom Workflow

```bash
lucifer start -i
lucifer> workflow recon 192.168.1.100
lucifer> analyze
lucifer> suggest
lucifer> execute nmap -sV -sC 192.168.1.100
lucifer> report
```

## Python API Usage

```python
from lucifer import LuciferAssistant
import asyncio

async def main():
    assistant = LuciferAssistant()
    
    try:
        await assistant.start_terminal_monitoring()
        results = await assistant.run_automated_recon("target.com")
        suggestions = await assistant.suggest_next_actions()
        report = await assistant.generate_report()
    finally:
        assistant.stop()

asyncio.run(main())
```

## Available Workflows

| Workflow | Command | Description |
|----------|---------|-------------|
| Reconnaissance | `recon` | Network discovery and enumeration |
| Web App Testing | `webapp` | Web vulnerability scanning |
| Exploitation | `exploit` | Exploit search and execution |
| Privilege Escalation | `privesc` | Linux privilege escalation |

## Tips for Best Results

### 1. Terminal Monitoring
- Start Lucifer before running security tools
- It captures and analyzes all terminal output
- AI provides real-time insights

### 2. Screen Capture
- Works best with dark-themed terminals
- OCR extracts text from GUI applications
- Computer vision detects UI elements

### 3. AI Suggestions
- More context = better suggestions
- Run `analyze` frequently
- Review suggestions before executing

### 4. Report Generation
- Reports include:
  - Commands executed
  - Findings discovered
  - Screenshots captured
  - AI analysis
- Generate reports regularly

## Common Issues

### "AI credentials not configured"
**Solution**: Add API key to `.env` file

### "Command not found: lucifer"
**Solution**: Activate virtual environment: `source venv/bin/activate`

### "Permission denied"
**Solution**: Make install script executable: `chmod +x install.sh`

### OCR not working
**Solution**: Install Tesseract: `sudo apt-get install tesseract-ocr`

## Safety Features

### Dangerous Command Filter
Lucifer warns about potentially dangerous commands:
- `rm -rf`
- `dd if=`
- `mkfs`
- Fork bombs

Configure in `.env`:
```bash
DANGEROUS_COMMANDS_FILTER=true
CONFIRMATION_REQUIRED=true
```

### Audit Logging
All commands are logged for security audit:
```bash
AUDIT_LOG_ENABLED=true
AUDIT_LOG_FILE=logs/audit.log
```

## Legal & Ethical Use

⚠️ **IMPORTANT**: Only use Lucifer on systems you own or have explicit written permission to test.

Unauthorized access to computer systems is illegal. Users are responsible for compliance with all applicable laws.

## Getting Help

- **Documentation**: See `README.md`
- **Examples**: Check `examples/` directory
- **Support**: Contact yashabalam9@gmail.com / yashabalam707@gmail.com
- **Contributing**: See `CONTRIBUTING.md`
- **Donate**: See [DONATE.md](DONATE.md) to support development

## Next Steps

1. ✅ Complete installation
2. ✅ Configure `.env` file
3. ✅ Run `lucifer config-check`
4. ✅ Try interactive mode
5. ✅ Run your first workflow
6. ✅ Review generated reports

## Example Workflow Session

```bash
# Start Lucifer
lucifer start -i

# In Lucifer shell:
lucifer> workflow recon scanme.nmap.org
[Lucifer executes reconnaissance workflow]

lucifer> analyze
[AI analyzes findings]

lucifer> suggest
[AI suggests next steps]
1. Test discovered HTTP service on port 80
2. Check for known vulnerabilities in detected SSH version
3. Enumerate subdomains
4. Run web application scan
5. Check for default credentials

lucifer> execute nmap --script vuln scanme.nmap.org
[Executes vulnerability scan]

lucifer> report
[Generates comprehensive report]

lucifer> exit
```

## Advanced Features

### Screen Recording
```bash
lucifer> record          # Start recording
lucifer> stop-record     # Stop and save
```

### Custom Workflows
See `examples/custom_workflow.py` for creating custom workflows.

### Python API
See `examples/` directory for programmatic usage examples.

## Resources

- **Official Docs**: https://github.com/yashab-cyber/lucifer
- **Bug Reports**: https://github.com/yashab-cyber/lucifer/issues
- **Feature Requests**: https://github.com/yashab-cyber/lucifer/discussions
- **Security**: Use responsibly and ethically

---

**Happy Hacking! 🔥**

Remember: With great power comes great responsibility. Use Lucifer ethically and legally.
