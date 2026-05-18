#!/bin/bash

# integrate_scabd_jules.sh
# Integrates SCABD architecture and verifies the Jules environment.

echo "--- Starting SCABD-Jules Integration ---"

# 1. Verify gh CLI
if ! command -v gh &> /dev/null; then
    echo "[!] gh CLI not found. Attempting installation..."
    (type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
    && sudo mkdir -p -m 755 /etc/apt/keyrings \
    && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && sudo apt update \
    && sudo apt install gh -y
else
    echo "[PASS] GitHub CLI is installed."
fi

# 2. Setup Environment Variables
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "[!] .env not found. Creating from .env.example..."
        cp .env.example .env
        echo "[INFO] Created .env. Please update it with your actual credentials."
    else
        echo "[FAIL] .env and .env.example are missing. Cannot configure environment."
    fi
else
    echo "[PASS] .env file exists."
fi

# 3. Instruction for GitHub Auth
echo ""
echo "--- GitHub Authentication ---"
if ! gh auth status &> /dev/null; then
    echo "[ACTION REQUIRED] Please run 'gh auth login' to authenticate with GitHub."
else
    echo "[PASS] Already authenticated with GitHub."
fi

# 4. Run Diagnostic Script
echo ""
echo "--- Running Jules Environment Diagnostics ---"
if [ -f test_jules_env.py ]; then
    python3 test_jules_env.py
else
    echo "[FAIL] test_jules_env.py not found. Integration check skipped."
fi

echo ""
echo "--- Integration Script Completed ---"
