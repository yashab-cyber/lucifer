#!/bin/bash

# Lucifer Installation Script for Kali Linux and Debian-based distributions
# This script installs Lucifer and all required dependencies

set -e

echo "================================================"
echo "  Lucifer AI Pentesting Assistant Installer"
echo "================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}Please do not run as root${NC}"
    exit 1
fi

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | grep -Po '(?<=Python )(.+)')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then 
    echo -e "${RED}Python 3.10 or higher is required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi
echo -e "${GREEN}Python $PYTHON_VERSION found ✓${NC}"

# Update package list
echo -e "${YELLOW}Updating package list...${NC}"
sudo apt-get update -qq

# Install system dependencies
echo -e "${YELLOW}Installing system dependencies...${NC}"
sudo apt-get install -y -qq \
    tesseract-ocr \
    tesseract-ocr-eng \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    git

echo -e "${GREEN}System dependencies installed ✓${NC}"

# Install optional pentesting tools
echo -e "${YELLOW}Checking for pentesting tools...${NC}"

TOOLS=("nmap" "gobuster" "nikto" "sqlmap" "searchsploit")
MISSING_TOOLS=()

for tool in "${TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        MISSING_TOOLS+=("$tool")
    fi
done

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo -e "${YELLOW}Optional tools not found: ${MISSING_TOOLS[*]}${NC}"
    read -p "Install optional pentesting tools? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt-get install -y "${MISSING_TOOLS[@]}"
        echo -e "${GREEN}Optional tools installed ✓${NC}"
    fi
fi

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created ✓${NC}"
else
    echo -e "${GREEN}Virtual environment already exists ✓${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel -q

# Install Lucifer
echo -e "${YELLOW}Installing Lucifer...${NC}"
pip install -e . -q

echo -e "${GREEN}Lucifer installed ✓${NC}"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created ✓${NC}"
    echo -e "${YELLOW}Please edit .env file and add your AI API keys${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}Creating directories...${NC}"
mkdir -p logs reports recordings

# Create desktop shortcut (optional)
read -p "Create desktop shortcut? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    DESKTOP_FILE="$HOME/.local/share/applications/lucifer.desktop"
    mkdir -p "$(dirname "$DESKTOP_FILE")"
    
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Lucifer
Comment=AI-Powered Cybersecurity Automation Assistant
Exec=$(pwd)/venv/bin/lucifer start -i
Icon=security
Terminal=true
Categories=Security;Network;
EOF
    
    chmod +x "$DESKTOP_FILE"
    echo -e "${GREEN}Desktop shortcut created ✓${NC}"
fi

# Installation complete
echo ""
echo "================================================"
echo -e "${GREEN}Installation Complete!${NC}"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your AI API keys:"
echo "   nano .env"
echo ""
echo "2. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Start Lucifer:"
echo "   lucifer start --interactive"
echo ""
echo "4. Check configuration:"
echo "   lucifer config-check"
echo ""
echo "5. View available workflows:"
echo "   lucifer workflows"
echo ""
echo -e "${YELLOW}Documentation: https://github.com/yashab-cyber/lucifer${NC}"
echo ""
