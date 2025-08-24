from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import List

from prometheus_client import Histogram

K8S_CMD_LATENCY = Histogram(
    "k8s_cmd_latency_seconds", "Kubernetes command latency", ["command"]
)


def list_namespaces() -> List[str]:
    """Return the list of namespaces in the current context."""
    result = subprocess.run(
        [
            "kubectl",
            "get",
            "namespaces",
            "-o",
            "jsonpath={.items[*].metadata.name}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip().split()


def apply(file: Path, namespace: str | None = None) -> str:
    """Server-side dry-run apply."""
    cmd = ["kubectl", "apply", "--dry-run=server", "-f", str(file)]
    if namespace:
        cmd.extend(["-n", namespace])
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    K8S_CMD_LATENCY.labels("apply").observe(time.time() - start)
    return result.stdout + result.stderr


def get_pod_logs(pod: str, namespace: str) -> str:
    cmd = ["kubectl", "logs", pod, "-n", namespace]
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    K8S_CMD_LATENCY.labels("logs").observe(time.time() - start)
    return result.stdout + result.stderr


def health() -> bool:
    result = subprocess.run(
        ["kubectl", "version", "--short"], capture_output=True, text=True, check=False
    )
    return result.returncode == 0
