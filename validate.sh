#!/bin/bash

# Lucifer Project Validation Script
# Run this to verify the project structure is complete

echo "╔═══════════════════════════════════════════════════════╗"
echo "║    Lucifer Project Structure Validation              ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track validation status
ERRORS=0

# Function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1 (missing)"
        ((ERRORS++))
    fi
}

# Function to check if directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
    else
        echo -e "${RED}✗${NC} $1/ (missing)"
        ((ERRORS++))
    fi
}

echo -e "${BLUE}Checking Core Source Files...${NC}"
check_file "src/lucifer/__init__.py"
check_file "src/lucifer/cli.py"
check_file "src/lucifer/core/__init__.py"
check_file "src/lucifer/core/config.py"
check_file "src/lucifer/core/terminal_capture.py"
check_file "src/lucifer/core/vision.py"
check_file "src/lucifer/core/ai_engine.py"
check_file "src/lucifer/core/assistant.py"
check_file "src/lucifer/automation/__init__.py"
check_file "src/lucifer/automation/workflows.py"
check_file "src/lucifer/utils/__init__.py"
check_file "src/lucifer/utils/logger.py"
check_file "src/lucifer/utils/report_generator.py"

echo ""
echo -e "${BLUE}Checking Test Files...${NC}"
check_file "tests/conftest.py"
check_file "tests/test_config.py"
check_file "tests/test_terminal_capture.py"

echo ""
echo -e "${BLUE}Checking Example Scripts...${NC}"
check_file "examples/__init__.py"
check_file "examples/basic_recon.py"
check_file "examples/custom_workflow.py"
check_file "examples/screenshot_analysis.py"

echo ""
echo -e "${BLUE}Checking Documentation...${NC}"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "CONTRIBUTING.md"
check_file "LICENSE"
check_file "PROJECT_SUMMARY.md"

echo ""
echo -e "${BLUE}Checking Configuration Files...${NC}"
check_file "pyproject.toml"
check_file ".env.example"
check_file ".gitignore"
check_file "install.sh"

echo ""
echo -e "${BLUE}Checking Directories...${NC}"
check_dir "src/lucifer"
check_dir "src/lucifer/core"
check_dir "src/lucifer/automation"
check_dir "src/lucifer/utils"
check_dir "tests"
check_dir "examples"

echo ""
echo -e "${BLUE}Code Statistics...${NC}"

# Count lines of code
if command -v cloc &> /dev/null; then
    cloc src/ --quiet
else
    TOTAL_LINES=$(find src -name "*.py" -type f -exec wc -l {} + | tail -1 | awk '{print $1}')
    FILE_COUNT=$(find src -name "*.py" -type f | wc -l)
    echo -e "${GREEN}Python files:${NC} $FILE_COUNT"
    echo -e "${GREEN}Total lines:${NC} $TOTAL_LINES"
fi

echo ""
echo -e "${BLUE}File Structure:${NC}"
tree -L 3 -I '__pycache__|*.pyc|venv|.git|node_modules' --dirsfirst 2>/dev/null || find . -type d -not -path '*/\.*' -not -path '*/venv/*' -not -path '*/__pycache__/*' | head -20

echo ""
echo "═══════════════════════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Project structure validation PASSED${NC}"
    echo -e "${GREEN}✓ All required files present${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./install.sh"
    echo "2. Configure: nano .env"
    echo "3. Test: lucifer config-check"
    echo "4. Start: lucifer start --interactive"
else
    echo -e "${RED}✗ Validation FAILED with $ERRORS error(s)${NC}"
    echo "Please check missing files above"
fi

echo "═══════════════════════════════════════════════════════"
