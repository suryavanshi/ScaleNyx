from pathlib import Path

from ..tools import terraform


def apply_s3_bucket(env: str, name: str) -> str:
    """Run terraform apply for an S3 bucket."""
    path = Path("infra/terraform/live") / env / "s3"
    return terraform.run_apply(path, {"bucket_name": name})
