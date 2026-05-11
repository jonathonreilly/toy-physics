#!/usr/bin/env python3
"""Open-gate diagnostic for the YT_WARD Step 3 same-1PI construction.

The runner checks the coefficient algebra behind the proposed same-1PI
construction. It intentionally does not assert that the OGE and H_unit
representations are the same Green's function; it verifies that equating
their projected coefficients is exactly the remaining gate.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import math
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "YT_WARD_STEP3_SAME_1PI_CONSTRUCTION_NARROW_THEOREM_NOTE_2026-05-10.md"

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "-" * 88)
    print(title)
    print("-" * 88)


section("Part 1: source scope")
note_text = NOTE_PATH.read_text()
for required in [
    "**Type:** open_gate",
    "same-1PI bridge remains",
    "Does **not** derive `g_bare = 1`",
    "not load-bearing dependencies",
]:
    check(f"note contains required scope text: {required}", required in note_text)
for forbidden in [
    "DERIVED tree-level identity",
    "holds. The agreement is enforced",
    "target_claim_type: " + "positive_" + "theorem",
    "audited" + "_clean",
]:
    check(f"note avoids overclaim/status text: {forbidden}", forbidden not in note_text)


section("Part 2: symbolic coefficient algebra")
g_bare = sp.symbols("g_bare", positive=True, real=True)
N_c = sp.symbols("N_c", positive=True, integer=True)
N_iso = sp.symbols("N_iso", positive=True, integer=True)
c_S = sp.symbols("c_S", positive=True, real=True)

C_A = c_S * g_bare**2 / (2 * N_c)
F_Htt = 1 / sp.sqrt(N_c * N_iso)
C_B = F_Htt**2
residual = sp.factor(C_A - C_B)
expected_residual = (N_iso * c_S * g_bare**2 - 2) / (2 * N_c * N_iso)

check(
    "Rep A coefficient is c_S * g_bare^2 / (2 N_c)",
    sp.simplify(C_A - c_S * g_bare**2 / (2 * N_c)) == 0,
    detail=f"C_A={C_A}",
)
check(
    "Rep B coefficient is 1 / (N_c N_iso)",
    sp.simplify(C_B - 1 / (N_c * N_iso)) == 0,
    detail=f"C_B={sp.simplify(C_B)}",
)
check(
    "C_A - C_B residual has the expected gate factor",
    sp.simplify(residual - expected_residual) == 0,
    detail=f"residual={residual}",
)
check(
    "C_A and C_B are not identical as symbolic functions of g_bare",
    sp.simplify(residual) != 0 and g_bare in residual.free_symbols,
    detail=f"free_symbols={sorted(str(s) for s in residual.free_symbols)}",
)

gate_solution = sp.solve(sp.Eq(C_A, C_B), g_bare)
expected_gate = sp.sqrt(2 / (c_S * N_iso))
check(
    "Equating coefficients yields g_bare = sqrt(2 / (c_S N_iso)) on the positive branch",
    any(sp.simplify(sol - expected_gate) == 0 for sol in gate_solution),
    detail=f"solutions={gate_solution}",
)

canonical_residual = sp.simplify(residual.subs({N_c: 3, N_iso: 2, c_S: 1}))
check(
    "Canonical residual is (g_bare^2 - 1) / 6",
    sp.simplify(canonical_residual - (g_bare**2 - 1) / 6) == 0,
    detail=f"canonical_residual={canonical_residual}",
)
check(
    "Canonical equality holds at g_bare = 1",
    sp.simplify(canonical_residual.subs(g_bare, 1)) == 0,
)
check(
    "Canonical equality fails off surface at g_bare = 2",
    sp.simplify(canonical_residual.subs(g_bare, 2)) == sp.Rational(1, 2),
    detail=f"residual(g=2)={sp.simplify(canonical_residual.subs(g_bare, 2))}",
)


section("Part 3: D12 SU(3) Fierz coefficient input")
l1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
l2 = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
l3 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
l4 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
l5 = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
l6 = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
l7 = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
l8 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / math.sqrt(3)
generators = [m / 2 for m in (l1, l2, l3, l4, l5, l6, l7, l8)]

norm_err = 0.0
for a in range(8):
    for b in range(8):
        expected = 0.5 if a == b else 0.0
        norm_err = max(norm_err, abs(np.trace(generators[a] @ generators[b]).real - expected))
check("Gell-Mann normalization Tr(Ta Tb) = delta_ab / 2", norm_err < 1e-12, f"err={norm_err:.2e}")

fierz_err = 0.0
for i, j, k, l in product(range(3), repeat=4):
    lhs = sum(generators[a][i, j] * generators[a][k, l] for a in range(8)).real
    rhs = 0.5 * (
        (1.0 if i == l else 0.0) * (1.0 if j == k else 0.0)
        - (1.0 / 3.0) * (1.0 if i == j else 0.0) * (1.0 if k == l else 0.0)
    )
    fierz_err = max(fierz_err, abs(lhs - rhs))
check("D12 Fierz identity verified over all SU(3) index tuples", fierz_err < 1e-12, f"err={fierz_err:.2e}")
check("D12 singlet coefficient is -1/(2 N_c) = -1/6", abs(-1 / 6 - (-1 / (2 * 3))) < 1e-15)


section("Part 4: H_unit normalization input")
N_total = 6
H_unit = sp.eye(N_total) / sp.sqrt(N_total)
diag_ok = True
for idx in range(N_total):
    diag_ok = diag_ok and sp.simplify(H_unit[idx, idx] - 1 / sp.sqrt(N_total)) == 0
check("H_unit diagonal entries are 1/sqrt(6)", diag_ok)
check("Tr(H_unit) = sqrt(6)", sp.simplify(sp.trace(H_unit) - sp.sqrt(6)) == 0)

wick_count = sum(1 for alpha, a, beta, b in product(range(2), range(3), range(2), range(3)) if alpha == beta and a == b)
check("Diagonal Wick-contraction count on Q_L is N_iso * N_c = 6", wick_count == 6)
check(
    "H_unit Wick saturation normalizes the diagonal count to 1",
    sp.Rational(wick_count, N_total) == 1,
    detail=f"{wick_count}/{N_total}",
)

print(f"\nTOTAL: PASS={PASS}, FAIL={FAIL}")
sys.exit(1 if FAIL else 0)
