#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  SUDO="sudo"
else
  SUDO=""
fi

if ! command -v dnf >/dev/null 2>&1; then
  echo "Error: This installer targets Rocky Linux/Fedora systems with dnf."
  exit 1
fi

echo "Configuring Google Cloud CLI repository..."
${SUDO} tee /etc/yum.repos.d/google-cloud-sdk.repo >/dev/null <<'EOF'
[google-cloud-cli]
name=Google Cloud CLI
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el9-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

echo "Refreshing package metadata..."
${SUDO} dnf makecache -y

echo "Installing Google Cloud CLI..."
${SUDO} dnf install -y google-cloud-cli

echo
echo "Google Cloud CLI installation complete."
echo "Run: gcloud init"
echo "Then authenticate: gcloud auth login"
