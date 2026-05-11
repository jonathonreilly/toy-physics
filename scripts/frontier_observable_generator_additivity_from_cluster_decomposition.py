#!/usr/bin/env python3
"""Runner for observable-generator additivity on a finite block split."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import sympy as sp
except ImportError:
    print("FAIL: sympy required for exact symbolic checks")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
NOTE = (
    ROOT
    / "docs"
    / "OBSERVABLE_GENERATOR_ADDITIVITY_FROM_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-05-10.md"
)

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
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def main() -> int:
    print("=" * 76)
    print("OBSERVABLE GENERATOR ADDITIVITY FINITE-BLOCK RUNNER")
    print("=" * 76)

    a1, a2, b1, b2, c = sp.symbols("a1 a2 b1 b2 c")

    d_a = sp.diag(2 + a1, 3 + a2)
    d_b = sp.diag(5 + b1, 7 + b2)
    d_full = sp.diag(2 + a1, 3 + a2, 5 + b1, 7 + b2)

    z_a = sp.factor(d_a.det())
    z_b = sp.factor(d_b.det())
    z_full = sp.factor(d_full.det())
    check("block determinant factorizes", sp.simplify(z_full - z_a * z_b) == 0)

    # Use positive diagonal baseline values, so log(abs(det)) is just log(det)
    # on a neighborhood of zero source.
    w_full = sp.log(z_full) - sp.log(z_full.subs({a1: 0, a2: 0, b1: 0, b2: 0}))
    w_a = sp.log(z_a) - sp.log(z_a.subs({a1: 0, a2: 0}))
    w_b = sp.log(z_b) - sp.log(z_b.subs({b1: 0, b2: 0}))
    normalized_full = z_full / z_full.subs({a1: 0, a2: 0, b1: 0, b2: 0})
    normalized_blocks = (z_a / z_a.subs({a1: 0, a2: 0})) * (z_b / z_b.subs({b1: 0, b2: 0}))
    check(
        "normalized determinant factorization gives log-generator additivity",
        sp.simplify(normalized_full - normalized_blocks) == 0,
    )

    mixed = sp.diff(w_full, a1, b1)
    check("mixed cumulant across a no-cut block split vanishes", sp.simplify(mixed) == 0)

    pure = sp.diff(w_full, a1, a1)
    check("same-site second source derivative is nonzero in the test block", sp.simplify(pure) != 0)

    coupled = sp.Matrix(
        [
            [2 + a1, 0, c, 0],
            [0, 3 + a2, 0, 0],
            [c, 0, 5 + b1, 0],
            [0, 0, 0, 7 + b2],
        ]
    )
    z_coupled = sp.factor(coupled.det())
    check("counterfactual cut bond breaks determinant factorization", sp.simplify(z_coupled - z_a * z_b) != 0)

    w_coupled = sp.log(z_coupled)
    mixed_coupled = sp.diff(w_coupled, a1, b1)
    check("counterfactual cut bond creates a mixed derivative", sp.simplify(mixed_coupled) != 0)

    if NOTE.exists():
        body = NOTE.read_text()
        required = [
            "**Claim type:** bounded_theorem",
            "does not retire the parent selection step",
            "does not change the status",
        ]
        forbidden = [
            "proposed" + "_retained",
            "audited" + "_clean",
            "A" + "1",
            "A" + "2",
            "A" + "3",
        ]
        check(
            "companion note keeps bounded status and avoids A-label theorem names",
            all(item in body for item in required)
            and all(item not in body for item in forbidden),
        )
    else:
        check("companion note exists", False, str(NOTE))

    print("=" * 76)
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    print("=" * 76)
    if FAIL == 0:
        print("VERDICT: bounded finite-block additivity only")
        return 0
    print("VERDICT: runner failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
