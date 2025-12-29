#!/bin/bash

# Create desktop entry for Lucifer

INSTALL_DIR="$(cd "$(dirname "$0")" && pwd)"
ICON_PATH="$INSTALL_DIR/gui/public/icon.svg"
DESKTOP_FILE="$HOME/.local/share/applications/lucifer.desktop"
DESKTOP_SHORTCUT="$HOME/Desktop/lucifer.desktop"

echo "Creating Lucifer desktop entry..."

# Create .local/share/applications if it doesn't exist
mkdir -p "$HOME/.local/share/applications"

# Create the desktop entry
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Lucifer
Comment=AI-Powered Cybersecurity Automation Assistant
Exec=$INSTALL_DIR/gui/node_modules/.bin/electron $INSTALL_DIR/gui/electron/main.js
Icon=$ICON_PATH
Terminal=false
Categories=Development;Security;Utility;
Keywords=pentesting;security;hacking;cybersecurity;AI;
StartupWMClass=Lucifer
Actions=

[Desktop Action]
Name=Lucifer AI Assistant
EOF

# Make it executable
chmod +x "$DESKTOP_FILE"

# Create desktop shortcut if Desktop folder exists
if [ -d "$HOME/Desktop" ]; then
    cp "$DESKTOP_FILE" "$DESKTOP_SHORTCUT"
    chmod +x "$DESKTOP_SHORTCUT"
    # Make it trusted on GNOME
    if command -v gio &> /dev/null; then
        gio set "$DESKTOP_SHORTCUT" metadata::trusted true
    fi
    echo "✓ Desktop shortcut created: $DESKTOP_SHORTCUT"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications"
fi

echo "✓ Desktop entry created: $DESKTOP_FILE"
echo ""
echo "Lucifer will now appear in your application menu!"
echo ""
echo "You can also launch it with: lucifer-gui"
