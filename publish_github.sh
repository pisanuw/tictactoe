#!/usr/bin/env bash
set -euo pipefail

OWNER="${OWNER:-pisanuw}"
REPO="${REPO:-tictactoe}"
PRIVATE="${PRIVATE:-false}"
DESCRIPTION="${DESCRIPTION:-Tic-Tac-Toe PRO with Cloud Run deployment setup}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --owner)
      OWNER="${2:-}"
      shift 2
      ;;
    --repo)
      REPO="${2:-}"
      shift 2
      ;;
    --private)
      PRIVATE="true"
      shift
      ;;
    --public)
      PRIVATE="false"
      shift
      ;;
    -h|--help)
      cat <<'EOF'
Usage: ./publish_github.sh [--owner OWNER] [--repo REPO] [--private|--public]

Requires:
  - GITHUB_TOKEN env var with repo scope

Defaults:
  OWNER=pisanuw
  REPO=tictactoe
  PRIVATE=false
EOF
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Run with --help for usage."
      exit 1
      ;;
  esac
done

if ! command -v git >/dev/null 2>&1; then
  echo "Error: git not found"
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "Error: curl not found"
  exit 1
fi

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "Error: GITHUB_TOKEN is not set."
  echo "Create a token with repo permissions and run:"
  echo "  GITHUB_TOKEN=YOUR_TOKEN ./publish_github.sh"
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: current directory is not a git repository"
  exit 1
fi

echo "Checking if repository exists: ${OWNER}/${REPO}"
STATUS="$(curl -s -o /tmp/github_repo_check.json -w "%{http_code}" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/${OWNER}/${REPO}")"

if [[ "${STATUS}" == "404" ]]; then
  echo "Repository not found. Creating ${OWNER}/${REPO}..."
  CREATE_STATUS="$(curl -s -o /tmp/github_repo_create.json -w "%{http_code}" \
    -X POST \
    -H "Authorization: Bearer ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    https://api.github.com/user/repos \
    -d "{\"name\":\"${REPO}\",\"description\":\"${DESCRIPTION}\",\"private\":${PRIVATE}}")"

  if [[ "${CREATE_STATUS}" != "201" ]]; then
    echo "Error: failed to create repository (HTTP ${CREATE_STATUS})"
    cat /tmp/github_repo_create.json
    exit 1
  fi
  echo "Repository created."
elif [[ "${STATUS}" == "200" ]]; then
  echo "Repository already exists."
else
  echo "Error: unable to verify repository (HTTP ${STATUS})"
  cat /tmp/github_repo_check.json
  exit 1
fi

REMOTE_URL="https://github.com/${OWNER}/${REPO}.git"

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "${REMOTE_URL}"
else
  git remote add origin "${REMOTE_URL}"
fi

echo "Pushing main branch..."
git push -u origin main

echo "Published successfully: https://github.com/${OWNER}/${REPO}"
