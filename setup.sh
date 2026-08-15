#!/bin/bash

set -e

echo "🔧 Setting up Command Tracker (Arch Linux friendly)..."

# Project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is not installed."
    exit 1
fi

# Create virtual environment
if [[ ! -d "$VENV_DIR" ]]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "🐍 Virtual environment already exists."
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -r "$PROJECT_DIR/requirements.txt"

# Create global showcmm launcher
echo "🔗 Adding 'showcmm' command..."

sudo tee /usr/local/bin/showcmm > /dev/null <<EOF
#!/bin/bash
exec "$VENV_PYTHON" "$PROJECT_DIR/main.py" "\$@"
EOF

sudo chmod +x /usr/local/bin/showcmm

# Install man page
MAN_PAGE="$PROJECT_DIR/showcmm.1"
MAN_DIR="/usr/local/share/man/man1"

if [[ -f "$MAN_PAGE" ]]; then
    echo "📘 Installing man page..."

    sudo mkdir -p "$MAN_DIR"
    sudo cp "$MAN_PAGE" "$MAN_DIR/"
    sudo gzip -f "$MAN_DIR/showcmm.1"

    echo "✅ Man page installed."
else
    echo "⚠️  No man page found. Skipping."
fi

echo
echo "✅ Setup complete!"
echo
echo "You can now run:"
echo "  showcmm"
echo "  showcmm --help"
echo "  man showcmm"
echo
echo "Works from Bash, Zsh, Fish, and other shells."
