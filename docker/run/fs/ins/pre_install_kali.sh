#!/bin/bash
set -e

# fix permissions for cron files if directory exists
if [ -d "/etc/cron.d" ] && [ "$(ls -A /etc/cron.d)" ]; then
    chmod 0644 /etc/cron.d/*
fi

echo "=====BEFORE UPDATE====="

apt clean

# ★ 1. Add sid repo & pin it
echo "deb http://deb.debian.org/debian sid main" > /etc/apt/sources.list.d/debian-sid.list
cat >/etc/apt/preferences.d/python312 <<'EOF'
Package: *
Pin: release a=sid
Pin-Priority: 100

Package: python3.12*
Pin: release a=sid
Pin-Priority: 990
EOF

apt-get update && apt-get -y upgrade

# Try to install Python 3.12, but fall back to system Python if unavailable
if apt-cache show python3.12 > /dev/null 2>&1; then
    echo "Installing Python 3.12 from sid..."
    apt-get install -y --no-install-recommends \
        python3.12 python3.12-venv python3.12-dev || {
        echo "WARNING: Failed to install Python 3.12, using system Python"
        apt-get install -y --no-install-recommends \
            python3 python3-venv python3-dev python3-pip
    }
else
    echo "Python 3.12 not available in sid, using system Python"
    apt-get install -y --no-install-recommends \
        python3 python3-venv python3-dev python3-pip
fi

echo "=====MID UPDATE====="

# ★ 2. Refresh & install everything we need, including python3.12

apt-get install -y --no-install-recommends \
    nodejs openssh-server sudo curl wget git ffmpeg supervisor cron

echo "=====AFTER UPDATE====="

# ★ 3. Switch the interpreter (if Python 3.12 is available)
if command -v python3.12 > /dev/null 2>&1; then
    echo "Setting up Python 3.12 as default..."
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 0 2>/dev/null || true
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
    update-alternatives --set python3 /usr/bin/python3.12
else
    echo "Using system Python version: $(python3 --version)"
fi

# ★ 4. Make sure pip matches
python3 -m ensurepip --upgrade 2>/dev/null || apt-get install -y python3-pip
python3 -m pip install --upgrade pip

echo "Python setup complete: $(python3 --version)"

# Prepare SSH daemon
bash /ins/setup_ssh.sh "$@"
