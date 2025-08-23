import json
import shutil
import subprocess
from pathlib import Path

import pytest

POLICY = Path("security/opa/s3.rego")


def opa_available() -> bool:
    return shutil.which("opa") is not None


@pytest.mark.skipif(not opa_available(), reason="opa binary not installed")
def test_s3_policy_denies_public_bucket() -> None:
    data = {"resource": {"aws_s3_bucket": {"public": True}}}
    cmd = [
        "opa",
        "eval",
        "--format=json",
        "-d",
        str(POLICY),
        "data.scalenyx.s3.deny",
        "--input",
        "-",
    ]
    result = subprocess.run(
        cmd, input=json.dumps(data), text=True, capture_output=True, check=True
    )
    assert "Public S3 buckets are not allowed" in result.stdout
