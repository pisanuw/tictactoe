#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  SUDO="sudo"
else
  SUDO=""
fi

# Try DNF package installation first (using el8 repo for better compatibility)
install_via_dnf() {
  echo "Attempting DNF installation (using EL8 repository for compatibility)..."

  ${SUDO} tee /etc/yum.repos.d/google-cloud-sdk.repo >/dev/null <<'EOF'
[google-cloud-cli]
name=Google Cloud CLI
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el8-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

  ${SUDO} dnf makecache -y

  if ${SUDO} dnf install -y --nobest google-cloud-cli 2>/dev/null; then
    return 0
  else
    echo "DNF installation failed. Trying manual installation..."
    return 1
  fi
}

# Manual installation via tarball
install_via_tarball() {
  echo "Installing Google Cloud CLI manually..."

  cd /tmp
  curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
  tar -xf google-cloud-cli-linux-x86_64.tar.gz

  INSTALL_DIR="${HOME}/.local"
  mkdir -p "${INSTALL_DIR}"

  if [[ -d "${INSTALL_DIR}/google-cloud-sdk" ]]; then
    echo "Removing existing installation..."
    rm -rf "${INSTALL_DIR}/google-cloud-sdk"
  fi

  mv google-cloud-sdk "${INSTALL_DIR}/"

  echo "Running installer..."
  "${INSTALL_DIR}/google-cloud-sdk/install.sh" \
    --usage-reporting=false \
    --path-update=true \
    --bash-completion=true \
    --quiet

  echo
  echo "Add to your PATH by running:"
  echo "  source '${INSTALL_DIR}/google-cloud-sdk/path.bash.inc'"
  echo "  source '${INSTALL_DIR}/google-cloud-sdk/completion.bash.inc'"
  echo
  echo "Or add to ~/.bashrc:"
  echo "  echo 'source ${INSTALL_DIR}/google-cloud-sdk/path.bash.inc' >> ~/.bashrc"
  echo "  echo 'source ${INSTALL_DIR}/google-cloud-sdk/completion.bash.inc' >> ~/.bashrc"
}

if command -v dnf >/dev/null 2>&1; then
  if ! install_via_dnf; then
    install_via_tarball
  fi
else
  echo "DNF not found. Using manual installation..."
  install_via_tarball
fi

echo
echo "Google Cloud CLI installation complete."
echo "Run: gcloud init"
echo "Then authenticate: gcloud auth login"
