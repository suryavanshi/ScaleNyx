#!/usr/bin/env bash
set -e
ACTION=${1:-plan}
DIR=${2:-infra/terraform/live/dev/s3}
cd "$(git rev-parse --show-toplevel)/$DIR"
terraform init -backend=false >/dev/null
case "$ACTION" in
  plan)
    terraform plan "$@"
    ;;
  apply)
    terraform apply -auto-approve "$@"
    ;;
  *)
    echo "Usage: $0 [plan|apply] [dir]" >&2
    exit 1
    ;;
esac
