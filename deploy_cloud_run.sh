#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-tictactoe-pro}"

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
    -h|--help)
      cat <<'EOF'
Usage: ./deploy_cloud_run.sh --project PROJECT_ID [--region REGION] [--service SERVICE]

Options:
  --project   Google Cloud project ID (required unless PROJECT_ID env var is set)
  --region    Cloud Run region (default: us-central1)
  --service   Cloud Run service name (default: tictactoe-pro)

You can also set env vars:
  PROJECT_ID, REGION, SERVICE
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

if ! command -v gcloud >/dev/null 2>&1; then
  echo "Error: gcloud CLI is not installed or not on PATH."
  echo "Install it from: https://cloud.google.com/sdk/docs/install"
  exit 1
fi

if [[ -z "$PROJECT_ID" ]]; then
  echo "Error: project ID is required."
  echo "Use --project YOUR_PROJECT_ID or set PROJECT_ID env var."
  exit 1
fi

if [[ -x "./preflight_cloud_run.sh" ]]; then
  echo "Running preflight checks..."
  ./preflight_cloud_run.sh \
    --project "$PROJECT_ID" \
    --region "$REGION" \
    --service "$SERVICE" \
    --fix
else
  echo "Preflight script not found/executable; skipping preflight checks."
fi

IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy/${SERVICE}"

echo "Project: ${PROJECT_ID}"
echo "Region:  ${REGION}"
echo "Service: ${SERVICE}"
echo "Image:   ${IMAGE}"

gcloud config set project "${PROJECT_ID}" >/dev/null

echo "Enabling required APIs..."
timeout 60s gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com || {
    echo "Warning: API enable timed out or failed. Attempting to continue..."
  }

echo "Building container image with Cloud Build..."
gcloud builds submit \
  --config cloudbuild.yaml \
  --substitutions _IMAGE="${IMAGE}" \
  .

echo "Deploying to Cloud Run..."
gcloud run deploy "${SERVICE}" \
  --image "${IMAGE}" \
  --platform managed \
  --region "${REGION}" \
  --allow-unauthenticated

SERVICE_URL="$(gcloud run services describe "${SERVICE}" --region "${REGION}" --format='value(status.url)')"

echo
echo "Deployment complete."
echo "Service URL: ${SERVICE_URL}"
echo "Health check: ${SERVICE_URL}/healthz"
