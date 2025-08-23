#!/usr/bin/env bash
set -e
pip install -U pip pre-commit >/dev/null
pre-commit install >/dev/null
