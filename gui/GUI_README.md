# Lucifer Desktop GUI - Installation & Usage Guide

<div align="center">

<img src="public/icon.svg" alt="Lucifer Logo" width="120" height="120"/>

## AI-Powered Cybersecurity Automation Assistant

### Created by Yashab Alam

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Yashab%20Alam-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yashab-alam)
[![Instagram](https://img.shields.io/badge/Instagram-@yashab.alam-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/yashab.alam)

</div>

---

## Overview

The Lucifer Desktop GUI provides a modern, user-friendly interface for AI-powered cybersecurity automation. Built with Electron and React, it offers:

- 🖥️ **Native Desktop App** - Runs on Linux with full OS integration
- 🎨 **Modern UI** - Clean, professional interface with dark theme
- 🔄 **Real-time Updates** - Live terminal output and AI suggestions
- 🤖 **AI Integration** - Seamless connection to Claude, GPT-4, or Ollama
- 📊 **Workflow Management** - Visual workflow execution and monitoring
- ⚡ **Fast Performance** - Optimized for security operations

---

## Installation

### Prerequisites

- **OS**: Kali Linux, Parrot OS, Ubuntu, or any Debian-based distribution
- **Node.js**: Version 16 or higher
- **Python**: Version 3.10 or higher
- **RAM**: At least 4GB
- **Disk Space**: 500MB for dependencies

### Quick Install

```bash
# From the Lucifer project root directory
./install-gui.sh
```

This script will:
1. Check for Node.js installation
2. Install npm dependencies
3. Build the React application
4. Create Electron packages (.AppImage and .deb)
5. Display installation instructions

### Manual Installation

If you prefer manual installation:

```bash
# Navigate to GUI directory
cd gui

# Install dependencies
npm install

# Build the app
npm run build

# Package for Linux
npm run build:linux
```

### Creating Desktop Entry

After building, create desktop shortcuts:

```bash
# From project root
./create-desktop-entry.sh
```

This will:
- Add Lucifer to your application menu
- Create a desktop shortcut
- Configure the app icon
- Make it searchable in your launcher

---

## Usage

### Launching the Application

**Method 1: Application Menu**
1. Open your application launcher (Activities/Menu)
2. Search for "Lucifer"
3. Click the Lucifer icon

**Method 2: Desktop Shortcut**
1. Find the Lucifer icon on your desktop
2. Double-click to launch

**Method 3: Command Line**
```bash
# Development mode
cd gui && npm start

# Production launcher
./gui/lucifer-gui
```

### First Time Setup

1. **Launch Lucifer** from your application menu
2. **Click Settings** (⚙️ icon in header)
3. **Configure AI Provider**:
   - Choose provider (Claude, GPT-4, or Ollama)
   - Enter your API key
   - Set other preferences
4. **Save Configuration**
5. **You're ready to go!**

### Using the Interface

#### Header Bar
- **Logo & Title**: Lucifer branding
- **Settings (⚙️)**: Configuration modal
- **Info (ℹ️)**: About dialog with credits
- **Report (📄)**: Generate security report

#### Sidebar Navigation
- **Terminal**: Interactive terminal emulator
- **Workflows**: Pre-built automation workflows
- **Analysis**: AI-powered analysis tools

#### Main Content Area

**Terminal Tab**
- Execute commands directly
- View output in real-time
- Command history navigation
- Syntax highlighting

**Workflows Tab**
- **Reconnaissance**: Network discovery and enumeration
- **Web Application**: Web vulnerability scanning
- **Exploitation**: Exploit search and execution
- **Privilege Escalation**: Linux privilege escalation

Each workflow:
1. Enter target (IP/domain)
2. Click "Run" button
3. Monitor progress
4. Review results

#### Output Panel (Right Side)
- Real-time AI suggestions
- Context-aware recommendations
- Security insights
- Next step guidance

---

## Features

### Terminal Emulator
- Full terminal functionality
- Command history (↑/↓ arrows)
- Output capture and analysis
- Syntax highlighting
- Copy/paste support

### AI-Powered Suggestions
- Contextual command recommendations
- Vulnerability analysis
- Exploitation guidance
- Next steps suggestions
- Risk assessment

### Automated Workflows

**Reconnaissance**
```
Target: scanme.nmap.org
Actions:
- Port scanning
- Service detection
- OS fingerprinting
- Vulnerability scanning
```

**Web Application Testing**
```
Target: https://example.com
Actions:
- Directory enumeration
- Parameter discovery
- SQL injection testing
- XSS detection
```

**Exploitation**
```
Target: 192.168.1.100
Actions:
- Exploit search
- Metasploit integration
- Payload generation
- Exploit execution
```

**Privilege Escalation**
```
Target: Local system
Actions:
- SUID enumeration
- Kernel exploit check
- Misconfiguration detection
- Automation suggestions
```

### Report Generation
- Comprehensive HTML reports
- Markdown documentation
- JSON export for automation
- Screenshot inclusion
- Command timeline
- Findings summary

---

## Configuration

### Settings Modal

Access via ⚙️ icon in header.

**AI Provider**
- Anthropic Claude (Recommended)
- OpenAI GPT-4
- Ollama (Local/Offline)

**API Configuration**
- API key input
- Model selection
- Temperature settings

**Application Settings**
- Theme selection
- Log level
- Confirmation prompts
- OCR enable/disable

**Advanced Options**
- Custom workflows
- Plugin management
- Integration settings

### Configuration File

Config stored in: `~/.config/lucifer/config.json`

```json
{
  "ai_provider": "anthropic",
  "api_key": "sk-ant-...",
  "log_level": "INFO",
  "confirmation_required": true,
  "ocr_enabled": true,
  "theme": "dark"
}
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+T` | Focus terminal input |
| `Ctrl+K` | Clear terminal |
| `Ctrl+L` | Clear terminal (alternative) |
| `Ctrl+R` | Generate report |
| `Ctrl+,` | Open settings |
| `Ctrl+Q` | Quit application |
| `F1` | Show help |
| `F5` | Refresh current view |

---

## Architecture

### Components

```
┌─────────────────────────────────────┐
│         Electron Main Process       │
│  - Window Management                │
│  - IPC Communication                │
│  - Menu System                      │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│       React Renderer Process        │
│  - UI Components                    │
│  - State Management                 │
│  - Event Handling                   │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│      Python Backend Server          │
│  - Terminal Capture                 │
│  - AI Processing                    │
│  - Workflow Execution               │
└─────────────────────────────────────┘
```

### IPC Communication

Electron uses secure IPC (Inter-Process Communication):

**Frontend → Backend**
```javascript
window.electron.executeCommand(cmd)
window.electron.runWorkflow(name, target)
window.electron.getSuggestions()
```

**Backend → Frontend**
```javascript
window.electron.onTerminalOutput((output) => {})
window.electron.onWorkflowUpdate((status) => {})
```

---

## Troubleshooting

### Application Won't Start

**Check Node.js version:**
```bash
node --version  # Should be 16+
```

**Reinstall dependencies:**
```bash
cd gui
rm -rf node_modules package-lock.json
npm install
```

### Icon Not Showing

**Rebuild desktop database:**
```bash
update-desktop-database ~/.local/share/applications
```

**Check icon path:**
```bash
ls -la gui/public/icon.svg
```

### Python Backend Not Responding

**Check server status:**
```bash
ps aux | grep "python.*server.py"
```

**Restart backend:**
```bash
pkill -f "python.*server.py"
python3 src/lucifer/server.py &
```

### Settings Not Saving

**Check config directory:**
```bash
mkdir -p ~/.config/lucifer
chmod 755 ~/.config/lucifer
```

---

## Development

### Running in Development Mode

```bash
cd gui

# Start backend server (Terminal 1)
python3 ../src/lucifer/server.py

# Start Electron app (Terminal 2)
npm start
```

### Building from Source

```bash
# Install dependencies
npm install

# Run in dev mode
npm start

# Build production
npm run build

# Package for Linux
npm run build:linux
```

### Project Structure

```
gui/
├── electron/           # Electron main process
│   ├── main.js        # Main entry point
│   └── preload.js     # Preload script (IPC bridge)
├── src/               # React application
│   ├── components/    # UI components
│   ├── App.js         # Main app component
│   └── index.js       # React entry point
├── public/            # Static assets
│   ├── icon.svg       # Application logo
│   └── index.html     # HTML template
└── package.json       # Dependencies & scripts
```

---

## About

### Creator

**Yashab Alam**

Cybersecurity professional and software developer passionate about automation and AI.

- 🔗 LinkedIn: [linkedin.com/in/yashab-alam](https://www.linkedin.com/in/yashab-alam)
- 📸 Instagram: [@yashab.alam](https://www.instagram.com/yashab.alam)
- 📧 Email: yashabalam9@gmail.com

### Support the Project

If you find Lucifer useful, consider supporting its development:

**[View Donation Options](../DONATE.md)**

Your support helps:
- Maintain and improve Lucifer
- Add new features
- Provide better documentation
- Offer community support

---

## Legal & Ethics

⚠️ **IMPORTANT**: Lucifer is designed for:
- Legal penetration testing
- Authorized security assessments
- Educational purposes
- Personal lab environments

**NEVER** use Lucifer on systems you don't own or don't have explicit written permission to test.

Unauthorized access to computer systems is illegal under:
- Computer Fraud and Abuse Act (USA)
- Computer Misuse Act (UK)
- Similar laws worldwide

**Users are solely responsible for ensuring legal and ethical use.**

---

## License

MIT License - See LICENSE file for details

---

## Acknowledgments

- Electron & React communities
- Cybersecurity tool developers
- AI model providers (Anthropic, OpenAI, Ollama)
- Open source contributors

---

<div align="center">

**Made with ❤️ by Yashab Alam**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/yashab-alam)
[![Instagram](https://img.shields.io/badge/Instagram-Follow-E4405F?style=for-the-badge&logo=instagram)](https://www.instagram.com/yashab.alam)

</div>
