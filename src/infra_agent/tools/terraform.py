import subprocess
import time
from pathlib import Path
from typing import Dict, List

from prometheus_client import Histogram


def _var_flags(variables: Dict[str, str]) -> List[str]:
    flags: List[str] = []
    for key, value in variables.items():
        flags.extend(["-var", f"{key}={value}"])
    return flags


TERRAFORM_CMD_LATENCY = Histogram(
    "terraform_cmd_latency_seconds", "Terraform command latency", ["command"]
)


def run_plan(path: Path, variables: Dict[str, str]) -> str:
    cmd = ["terraform", "plan", "-input=false", "-lock=false", *_var_flags(variables)]
    start = time.time()
    result = subprocess.run(cmd, cwd=path, capture_output=True, text=True, check=False)
    TERRAFORM_CMD_LATENCY.labels("plan").observe(time.time() - start)
    return result.stdout + result.stderr


def run_apply(path: Path, variables: Dict[str, str]) -> str:
    cmd = ["terraform", "apply", "-auto-approve", *_var_flags(variables)]
    start = time.time()
    result = subprocess.run(cmd, cwd=path, capture_output=True, text=True, check=False)
    TERRAFORM_CMD_LATENCY.labels("apply").observe(time.time() - start)
    return result.stdout + result.stderr
