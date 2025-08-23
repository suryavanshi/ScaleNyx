import subprocess
from pathlib import Path
from typing import Dict, List


def _var_flags(variables: Dict[str, str]) -> List[str]:
    flags: List[str] = []
    for key, value in variables.items():
        flags.extend(["-var", f"{key}={value}"])
    return flags


def run_plan(path: Path, variables: Dict[str, str]) -> str:
    cmd = ["terraform", "plan", "-input=false", "-lock=false", *_var_flags(variables)]
    result = subprocess.run(cmd, cwd=path, capture_output=True, text=True, check=False)
    return result.stdout + result.stderr


def run_apply(path: Path, variables: Dict[str, str]) -> str:
    cmd = ["terraform", "apply", "-auto-approve", *_var_flags(variables)]
    result = subprocess.run(cmd, cwd=path, capture_output=True, text=True, check=False)
    return result.stdout + result.stderr
