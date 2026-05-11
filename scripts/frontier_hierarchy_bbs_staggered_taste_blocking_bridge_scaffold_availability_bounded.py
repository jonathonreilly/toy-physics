#!/usr/bin/env python3
"""Runner for the BBS scaffold-availability bounded note.

This runner is a boundary and bookkeeping check. It does not verify the
external papers themselves and does not construct a framework BBS bridge.
"""

from __future__ import annotations

import sys
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 80

ROOT = Path(__file__).resolve().parent.parent
NOTE = (
    ROOT
    / "docs"
    / "HIERARCHY_BBS_STAGGERED_TASTE_BLOCKING_BRIDGE_SCAFFOLD_AVAILABILITY_BOUNDED_NOTE_2026-05-11.md"
)

PI = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286209"
)
P_AVG = Decimal("0.5934")
ALPHA_BARE = Decimal(1) / (Decimal(4) * PI)
U0 = P_AVG ** (Decimal(1) / Decimal(4))
ALPHA_LM = ALPHA_BARE / U0
ALPHA_LM_REFERENCE = Decimal("0.09066783601728631")

SCAFFOLDS = [
    {
        "name": "finite-range scalar Gaussian covariance decomposition",
        "available_domain": "scalar Gaussian covariance kernels",
        "missing_bridge": "coupled gauge-plus-staggered-fermion covariance",
    },
    {
        "name": "constructive RG Banach-space scaffold",
        "available_domain": "adjacent rigorous lattice field theory settings",
        "missing_bridge": "framework staggered taste-blocking Banach map",
    },
]

ADMISSIONS = [
    "scalar covariance scaffold is not the coupled framework covariance",
    "constructive RG scaffold is not the framework taste-blocking map",
    "kappa equals alpha_LM is not derived",
]

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
    print("BBS SCAFFOLD-AVAILABILITY BOUNDED RUNNER")
    print("=" * 76)

    check("two scaffold domains are recorded", len(SCAFFOLDS) == 2)
    check(
        "each scaffold has a named available domain",
        all(row["available_domain"] for row in SCAFFOLDS),
    )
    check(
        "each scaffold has a named missing bridge",
        all(row["missing_bridge"] for row in SCAFFOLDS),
    )
    check("three independent admissions are recorded", len(ADMISSIONS) == 3)

    rel_err = abs(ALPHA_LM - ALPHA_LM_REFERENCE) / ALPHA_LM_REFERENCE
    check(
        "alpha_LM transparency value matches the canonical surface",
        rel_err < Decimal("1e-15"),
        f"alpha_LM={ALPHA_LM:.18}",
    )

    arbitrary_kappa = Decimal("0.5")
    check(
        "Banach contraction arithmetic does not select alpha_LM",
        Decimal(0) < arbitrary_kappa < Decimal(1)
        and arbitrary_kappa != ALPHA_LM,
        "kappa=0.5 is also a valid abstract contraction constant",
    )

    if NOTE.exists():
        body = NOTE.read_text()
        required = [
            "**Claim type:** bounded_theorem",
            "This note does not supply those",
            "framework-specific objects for the staggered taste-blocking bridge",
            "The bridge remains bounded",
            "The safe result is scaffold availability plus explicit open admissions",
        ]
        forbidden = [
            "closes the hierarchy formula",
            "kappa = alpha_LM is derived",
        ]
        check("companion note contains required boundary phrases", all(s in body for s in required))
        check("companion note avoids promotion and closed-PR authority language", all(s not in body for s in forbidden))
        bare_admission_labels = ("A" + "1", "A" + "2", "A" + "3")
        check(
            "companion note uses explicit admissions, not bare A-labels",
            all(label not in body for label in bare_admission_labels),
        )
    else:
        check("companion note exists", False, str(NOTE))
        check("companion note avoids promotion and closed-PR authority language", False)
        check("companion note uses explicit admissions, not bare A-labels", False)

    print("=" * 76)
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    print("=" * 76)
    if FAIL == 0:
        print("VERDICT: bounded scaffold availability only; bridge still open")
        return 0
    print("VERDICT: runner failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
