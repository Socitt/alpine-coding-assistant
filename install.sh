#!/bin/sh
# install.sh — One-shot setup for Alpine Code Assistant on Alpine Linux / iSH
# Usage: sh install.sh

set -e

echo "==> Alpine Code Assistant setup"

# ── Resolve the repo directory (where this script lives) ──────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Package manager ────────────────────────────────────────────────────────
if command -v apk > /dev/null 2>&1; then
    echo "==> Detected Alpine Linux (apk)"
    apk add --no-cache python3 py3-pip 2>/dev/null || true
elif command -v apt-get > /dev/null 2>&1; then
    echo "==> Detected Debian/Ubuntu (apt)"
    apt-get install -y python3 python3-pip 2>/dev/null || true
fi

# ── Python dependencies ────────────────────────────────────────────────────
echo "==> Installing Python dependencies…"
pip3 install --quiet -r "$SCRIPT_DIR/requirements.txt"

# ── Projects directory ─────────────────────────────────────────────────────
PROJECTS_DIR="${KIRO_PROJECTS_DIR:-/root/projects}"
if [ ! -d "$PROJECTS_DIR" ]; then
    echo "==> Creating projects directory: $PROJECTS_DIR"
    mkdir -p "$PROJECTS_DIR"
fi

# ── Install `aca` global command ───────────────────────────────────────────
echo "==> Installing 'aca' command to /usr/local/bin/aca"

cat > /usr/local/bin/aca << EOF
#!/bin/sh
# Alpine Code Assistant launcher
exec python3 "$SCRIPT_DIR/main.py" "\$@"
EOF

chmod +x /usr/local/bin/aca

echo "==> 'aca' installed. You can now run the assistant with just: aca"

# ── API key check ──────────────────────────────────────────────────────────
if [ -z "$GROQ_API_KEY" ]; then
    echo ""
    echo "⚠  GROQ_API_KEY is not set."
    echo "   Get a free key at: https://console.groq.com"
    echo "   Then run:"
    echo "     export GROQ_API_KEY='your_key_here'"
    echo "   To persist it, add that line to ~/.profile:"
    echo "     echo 'export GROQ_API_KEY=\"your_key_here\"' >> ~/.profile"
    echo "     source ~/.profile"
    echo ""
fi

echo "==> Setup complete. Run:  aca"
