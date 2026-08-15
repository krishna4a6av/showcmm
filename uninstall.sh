#!/bin/bash

# Uninstall script for showcmm

echo "🔧 Uninstalling showcmm..."

# Remove global showcmm command
if [ -f /usr/local/bin/showcmm ]; then
    sudo rm /usr/local/bin/showcmm
    echo "✅ Removed 'showcmm' command from /usr/local/bin"
else
    echo "⚠️ 'showcmm' command not found in /usr/local/bin"
fi

# Ask before removing project directory
read -p "Do you want to remove the showcmm project folder? (y/N): " del_proj

if [[ "$del_proj" == "y" || "$del_proj" == "Y" ]]; then
    proj_dir="$(cd "$(dirname "$0")" && pwd)"

    echo "Deleting $proj_dir..."
    rm -rf "$proj_dir"

    echo "✅ Project folder removed."
else
    echo "Skipping project folder removal."
fi

# Remove man page
MAN_PAGE="/usr/local/share/man/man1/showcmm.1.gz"

if [ -f "$MAN_PAGE" ]; then
    sudo rm "$MAN_PAGE"
    echo "✅ Removed man page."
fi

echo "Uninstallation complete."
