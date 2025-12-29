#!/bin/bash

# Lucifer GUI Installation Script

set -e

echo "╔═══════════════════════════════════════════════════════╗"
echo "║    Lucifer GUI Desktop App Installer                ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed${NC}"
    echo "Please install Node.js 16 or higher from https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}Node.js $(node --version) found ✓${NC}"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}npm is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}npm $(npm --version) found ✓${NC}"

# Navigate to GUI directory
cd "$(dirname "$0")/gui"

# Install dependencies
echo -e "${YELLOW}Installing GUI dependencies...${NC}"
npm install

# Build the application
echo -e "${YELLOW}Building desktop application...${NC}"
npm run build

# Build Electron app for Linux
echo -e "${YELLOW}Building Linux package...${NC}"
npm run build:linux

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║    Installation Complete!                            ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Lucifer GUI has been built successfully!${NC}"
echo ""
echo "Application packages created in: gui/dist/"
echo ""
echo "To install:"
echo "  • AppImage: Double-click to run or:"
echo "    chmod +x dist/Lucifer-*.AppImage"
echo "    ./dist/Lucifer-*.AppImage"
echo ""
echo "  • DEB package: sudo dpkg -i dist/lucifer_*.deb"
echo ""
echo "Desktop shortcut will be automatically created!"
echo ""
echo "To run in development mode:"
echo "  cd gui && npm start"
echo ""
