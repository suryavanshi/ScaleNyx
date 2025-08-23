from pathlib import Path

from ..tools import terraform


def plan_s3_bucket(env: str, name: str) -> str:
    """Run terraform plan for an S3 bucket."""
    path = Path("infra/terraform/live") / env / "s3"
    return terraform.run_plan(path, {"bucket_name": name})
