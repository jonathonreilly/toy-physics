#!/usr/bin/env python3
"""Shared bootstrap for retained numpy replay scripts.

Several retained replay lanes on this machine rely on numpy, but the default
Homebrew ``python3`` does not ship with it. The system Python at
``/usr/bin/python3`` does.

This helper keeps the replay scripts themselves narrow: they can call
``ensure_numpy_runtime(__file__, sys.argv)`` before importing numpy-heavy
modules. If the current interpreter lacks numpy and the system Python exists,
the process re-execs there with the same script and arguments.
"""

from __future__ import annotations

import importlib.util
import os
import sys

SYSTEM_PYTHON = "/usr/bin/python3"


def ensure_numpy_runtime(script_path: str, argv: list[str] | None = None) -> None:
    """Re-exec the script under the system Python if numpy is missing.

    The helper is intentionally conservative:
    - if numpy is already importable, it does nothing
    - if not, and the system Python exists, it re-execs there
    - otherwise it raises a clear local error
    """

    if importlib.util.find_spec("numpy") is not None:
        return

    if os.path.exists(SYSTEM_PYTHON) and sys.executable != SYSTEM_PYTHON:
        args = [SYSTEM_PYTHON, "-u", script_path]
        if argv is None:
            args.extend(sys.argv[1:])
        else:
            args.extend(argv[1:])
        os.execv(SYSTEM_PYTHON, args)

    raise SystemExit(
        "numpy is required for this retained replay. On this machine use "
        "/usr/bin/python3, or add numpy to a repo-local venv."
    )
