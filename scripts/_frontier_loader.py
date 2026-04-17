#!/usr/bin/env python3
"""Local loader for sibling frontier scripts on the main branch."""

from __future__ import annotations

from importlib.machinery import SourceFileLoader
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent


def load_frontier(module_name: str, filename: str):
    return SourceFileLoader(module_name, str(SCRIPTS_DIR / filename)).load_module()
