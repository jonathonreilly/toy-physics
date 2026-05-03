# Python Virtual Environment Setup

**Date:** 2026-05-03
**Purpose:** standard setup for Python runners + SDP-extended dependencies

## Why a venv

Modern Homebrew / macOS Python is **PEP 668-restricted** (externally managed).
`pip install <package>` directly into system Python is blocked, with the
error `error: externally-managed-environment`.

The standard fix is a project-local virtual environment (venv). Each
worktree gets its own `.venv/` (gitignored), keeping dependencies
isolated from system Python.

## Quick setup (worktree-local)

From the worktree root (e.g., `/Users/jonreilly/Projects/Physics/` for
the main worktree, or `.claude/worktrees/<name>/` for a worktree):

```bash
# Create venv
python3 -m venv .venv

# Upgrade pip
.venv/bin/python3 -m pip install --upgrade pip

# Core requirements (numpy + scipy; sufficient for most runners)
.venv/bin/python3 -m pip install -r requirements.txt

# OPTIONAL: SDP-extended requirements (cvxpy + open-source solvers)
# Needed for industrial bootstrap work, semidefinite-programming bounds, etc.
.venv/bin/python3 -m pip install -r requirements-sdp.txt
```

## Running scripts via the venv

Always invoke runners using the venv's Python:

```bash
.venv/bin/python3 scripts/frontier_<lane>_<runner>.py
```

This ensures the runner uses the venv's installed packages, not system
Python.

## Verifying SDP setup

After installing `requirements-sdp.txt`, verify CVXPY + solvers work:

```bash
.venv/bin/python3 -c "
import cvxpy as cp
print('cvxpy version:', cp.__version__)
print('available solvers:', cp.installed_solvers())
"
```

Expected output:
```
cvxpy version: 1.8+
available solvers: ['CLARABEL', 'HIGHS', 'OSQP', 'SCIPY', 'SCS']
```

`CLARABEL` and `SCS` are the open-source SDP solvers; `HIGHS` is for LP;
`OSQP` is for QP; `SCIPY` is the SciPy backend.

For lattice-bootstrap work, CVXPY's default `cp.Variable((N,N), symmetric=True)`
+ constraint `X >> 0` (matrix positive-semidefinite) + `prob = cp.Problem(...);
prob.solve()` is sufficient for small-to-medium SDP problems (L_max ≤ 8,
matrices up to ~100x100).

## Solver capacity

| Solver | Best for | License | Capacity |
|---|---|---|---|
| CLARABEL | SDP, conic programs | Apache 2.0 | small-medium SDP (~100x100 matrices) |
| SCS | SDP, conic programs | MIT | medium-large SDP (~500x500); first-order, lower precision |
| HIGHS | LP, MILP | MIT | very large LP problems |
| OSQP | QP | Apache 2.0 | medium QP |
| Mosek (NOT installed) | LP / QP / SDP / general conic | commercial / academic | industrial precision; needed for published-precision lattice bootstrap (Kazakov-Zheng 2022 L_max=16) |

For published-precision lattice bootstrap work (Kazakov-Zheng 2022 at
L_max=16, ~6505x6505 matrices reduced via 20-irrep symmetry), Mosek is
recommended (academic license available). CLARABEL + SCS suffice for
exploratory work and L_max ≤ 8.

## Gitignore

`.venv/`, `venv/`, `env/` are gitignored repo-wide. Do NOT commit venv
binaries.

## Per-worktree convention

Each worktree gets its own `.venv/`. To verify which worktree's venv is
active:

```bash
which python3   # should print: /opt/homebrew/bin/python3 (system; NOT venv)
.venv/bin/python3 --version  # this is the venv Python
```

Always invoke runners via `.venv/bin/python3 <script>` rather than `python3
<script>` to avoid PEP 668 confusion.

## Troubleshooting

### `error: externally-managed-environment`

You ran `pip install` against system Python. Use the venv Python instead:
`.venv/bin/python3 -m pip install <package>`.

### `ModuleNotFoundError: No module named 'cvxpy'`

You ran a script with system Python. Use `.venv/bin/python3 <script>`.

### `Solver SCS not available` or similar

`requirements-sdp.txt` was not installed. Run:
`.venv/bin/python3 -m pip install -r requirements-sdp.txt`
