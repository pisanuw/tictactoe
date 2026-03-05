#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-tictactoe-pro}"
FIX_MISSING_APIS="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)
      PROJECT_ID="${2:-}"
      shift 2
      ;;
    --region)
      REGION="${2:-}"
      shift 2
      ;;
    --service)
      SERVICE="${2:-}"
      shift 2
      ;;
    --fix)
      FIX_MISSING_APIS="true"
      shift
      ;;
    -h|--help)
      cat <<'EOF'
Usage: ./preflight_cloud_run.sh [--project PROJECT_ID] [--region REGION] [--service SERVICE] [--fix]

Checks:
  - gcloud CLI installed
  - active gcloud auth account
  - project selected and accessible
  - local deployment files present
  - required APIs enabled

Options:
  --project   Google Cloud project ID (or set PROJECT_ID)
  --region    Cloud Run region (default: us-central1)
  --service   Cloud Run service name (default: tictactoe-pro)
  --fix       Enable missing required APIs automatically
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

pass() { echo "[OK] $1"; }
warn() { echo "[WARN] $1"; }
fail() { echo "[FAIL] $1"; }

FAILED=0

echo "Cloud Run preflight"
echo "Region:  ${REGION}"
echo "Service: ${SERVICE}"

if ! command -v gcloud >/dev/null 2>&1; then
  fail "gcloud CLI not found on PATH"
  echo "Install guide: https://cloud.google.com/sdk/docs/install"
  exit 1
fi
pass "gcloud CLI found"

ACTIVE_ACCOUNT="$(gcloud auth list --filter=status:ACTIVE --format='value(account)' 2>/dev/null || true)"
if [[ -z "${ACTIVE_ACCOUNT}" ]]; then
  fail "No active gcloud auth account"
  echo "Run: gcloud auth login"
  FAILED=1
else
  pass "Authenticated as ${ACTIVE_ACCOUNT}"
fi

if [[ -z "${PROJECT_ID}" ]]; then
  PROJECT_ID="$(gcloud config get-value project 2>/dev/null || true)"
fi

if [[ -z "${PROJECT_ID}" || "${PROJECT_ID}" == "(unset)" ]]; then
  fail "No project configured"
  echo "Run: gcloud config set project YOUR_PROJECT_ID"
  FAILED=1
else
  pass "Project configured: ${PROJECT_ID}"
fi

if [[ -n "${PROJECT_ID}" && "${PROJECT_ID}" != "(unset)" ]]; then
  if gcloud projects describe "${PROJECT_ID}" >/dev/null 2>&1; then
    pass "Project access verified"
  else
    fail "Cannot access project ${PROJECT_ID}"
    FAILED=1
  fi

  BILLING_ENABLED="$(gcloud beta billing projects describe "${PROJECT_ID}" --format='value(billingEnabled)' 2>/dev/null || true)"
  if [[ "${BILLING_ENABLED}" == "True" || "${BILLING_ENABLED}" == "true" ]]; then
    pass "Billing enabled"
  elif [[ -z "${BILLING_ENABLED}" ]]; then
    warn "Could not verify billing status (missing permission or API); ensure billing is enabled"
  else
    warn "Billing appears disabled; Cloud Run deploy will fail until billing is enabled"
    FAILED=1
  fi
fi

for required_file in Dockerfile cloudbuild.yaml cloud_app.py requirements.txt; do
  if [[ -f "${required_file}" ]]; then
    pass "Found ${required_file}"
  else
    fail "Missing ${required_file}"
    FAILED=1
  fi
done

REQUIRED_APIS=(
  run.googleapis.com
  cloudbuild.googleapis.com
  artifactregistry.googleapis.com
)

if [[ -n "${PROJECT_ID}" && "${PROJECT_ID}" != "(unset)" ]]; then
  ENABLED_APIS="$(gcloud services list --enabled --project "${PROJECT_ID}" --format='value(config.name)' 2>/dev/null || true)"

  MISSING_APIS=()
  for api in "${REQUIRED_APIS[@]}"; do
    if grep -qx "${api}" <<<"${ENABLED_APIS}"; then
      pass "API enabled: ${api}"
    else
      MISSING_APIS+=("${api}")
      warn "API not enabled: ${api}"
    fi
  done

  if [[ ${#MISSING_APIS[@]} -gt 0 ]]; then
    if [[ "${FIX_MISSING_APIS}" == "true" ]]; then
      echo "Enabling missing APIs..."
      gcloud services enable --project "${PROJECT_ID}" "${MISSING_APIS[@]}"
      pass "Missing APIs enabled"
    else
      echo "Run with --fix to enable missing APIs automatically."
      FAILED=1
    fi
  fi
fi

echo
if [[ ${FAILED} -eq 0 ]]; then
  echo "Preflight passed. Ready to deploy."
else
  echo "Preflight found issues. Fix the failures above and re-run."
fi

exit ${FAILED}
