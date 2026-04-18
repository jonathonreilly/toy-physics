#!/usr/bin/env python3
"""
Sharpen the plaquette propagated retained triple seam:
even fixed first-retained coefficients plus fixed Tau_(>1) do not collapse the
minimal propagated triple on the current coefficient-side bank.
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

SAMPLES = {
    "W_A": (-13 * math.pi / 16.0, 5 * math.pi / 8.0),
    "W_B": (-5 * math.pi / 16.0, -7 * math.pi / 16.0),
    "W_C": (7 * math.pi / 16.0, -11 * math.pi / 16.0),
}

ORBIT_1 = (0, 2)
ORBIT_2 = (0, 3)


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def su3_character(p: int, q: int, theta1: float, theta2: float) -> complex:
    x = [
        cmath.exp(1j * theta1),
        cmath.exp(1j * theta2),
        cmath.exp(-1j * (theta1 + theta2)),
    ]
    lam = [p + q, q, 0]
    num = np.array([[x[i] ** (lam[j] + 2 - j) for j in range(3)] for i in range(3)], dtype=complex)
    den = np.array([[x[i] ** (2 - j) for j in range(3)] for i in range(3)], dtype=complex)
    return complex(np.linalg.det(num) / np.linalg.det(den))


def orbit_summary_row(p: int, q: int) -> np.ndarray:
    d = dim_su3(p, q)
    mult = 1 if p == q else 2
    row = [float(mult * d * d)]
    for theta1, theta2 in SAMPLES.values():
        ch = su3_character(p, q, theta1, theta2)
        value = d * ch if p == q else 2.0 * (d * ch).real
        row.append(float(np.real_if_close(value)))
    return np.array(row, dtype=float)


def main() -> int:
    target_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_TARGET_NOTE_2026-04-17.md"
    )
    minimality_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_MINIMALITY_CURRENT_BANK_NOGO_NOTE_2026-04-17.md"
    )
    envelope_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md"
    )
    identity_tau_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_IDENTITY_TAU_INSUFFICIENCY_NOTE_2026-04-17.md"
    )
    higher_orbit_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_IDENTITY_PLUS_THREE_SAMPLE_HIGHER_ORBIT_UNDERDETERMINATION_NOTE_2026-04-17.md"
    )

    row1 = orbit_summary_row(*ORBIT_1)
    row2 = orbit_summary_row(*ORBIT_2)
    w1 = float(row1[0])
    w2 = float(row2[0])
    rem1 = row1[1:]
    rem2 = row2[1:]
    profile_gap = float(np.max(np.abs(rem1 / w1 - rem2 / w2)))

    p_vec = np.array([1.0 / 40.0, 0.0], dtype=float)
    q_vec = np.array([0.0, 9.0 / 1000.0], dtype=float)
    weights = np.array([w1, w2], dtype=float)

    tau_p = float(weights @ p_vec)
    tau_q = float(weights @ q_vec)

    tail_p = p_vec[0] * rem1 + p_vec[1] * rem2
    tail_q = q_vec[0] * rem1 + q_vec[1] * rem2
    zhat_p = np.ones(3, dtype=float) + tail_p
    zhat_q = np.ones(3, dtype=float) + tail_q
    triple_gap = float(np.max(np.abs(zhat_p - zhat_q)))
    min_p = float(np.min(zhat_p))
    min_q = float(np.min(zhat_q))

    print("=" * 124)
    print("GAUGE-VACUUM PLAQUETTE FIRST PROPAGATED RETAINED TRIPLE FIXED-RETAINED-PAIR/TAU NONCOLLAPSE")
    print("=" * 124)
    print()
    print("Two-orbit higher-tail slice")
    print(f"  orbit 1                                    = {ORBIT_1}")
    print(f"  orbit 2                                    = {ORBIT_2}")
    print(f"  identity weights                           = {w1:.12f}, {w2:.12f}")
    print(f"  remainder row 1                            = {rem1}")
    print(f"  remainder row 2                            = {rem2}")
    print(f"  max normalized-profile gap                 = {profile_gap:.12f}")
    print()
    print("Explicit fixed-retained-pair / fixed-Tau witness pair")
    print(f"  P higher-orbit coefficients                = {p_vec}")
    print(f"  Q higher-orbit coefficients                = {q_vec}")
    print(f"  Tau(P), Tau(Q)                             = {tau_p:.12f}, {tau_q:.12f}")
    print(f"  Zhat(P)                                    = {zhat_p}")
    print(f"  Zhat(Q)                                    = {zhat_q}")
    print(f"  max propagated-triple gap                  = {triple_gap:.12f}")
    print()

    check(
        "The propagated-triple target and minimality notes already place the live plaquette seam directly at the minimal finite propagated three-sample target",
        "propagated retained three-sample output" in target_note
        and "minimal honest positive finite target" in minimality_note
        and "normalized propagated retained triple is still not determined" in minimality_note,
        bucket="SUPPORT",
    )
    check(
        "The truncation-envelope note already separates fixed first-retained data from the higher-orbit tail mass Tau_(>1)",
        "`Z_hat_A = 1 + a rho_(1,0) + R_A^(>1)`" in envelope_note
        and "`Z_hat_B = 1 + b rho_(1,0) + c rho_(1,1) + R_B^(>1)`" in envelope_note
        and "`Z_hat_C = 1 + d rho_(1,0) + e rho_(1,1) + R_C^(>1)`" in envelope_note
        and "`Tau_(>1)`" in envelope_note,
        bucket="SUPPORT",
    )
    check(
        "The identity-Tau insufficiency note already proves fixed identity plus fixed Tau_(>1) is too weak, so a sharper current-bank test should fix the retained pair too",
        "fixed `Z_hat_6(e)` and fixed `Tau_(>1)`" in identity_tau_note
        and "still do **not** determine the" in identity_tau_note
        and "retained three-sample data" in identity_tau_note,
        bucket="SUPPORT",
    )

    check(
        "On the chosen two-orbit slice the higher-orbit tail mass is one affine constraint 72 u + 200 v = Tau_(>1)",
        abs(w1 - 72.0) < 1.0e-12 and abs(w2 - 200.0) < 1.0e-12,
        detail=f"weights=({w1:.0f}, {w2:.0f})",
    )
    check(
        "The two higher-orbit sample profiles are not proportional to their identity weights, so fixed Tau_(>1) does not collapse the remainder triple on that slice",
        profile_gap > 1.0e-6,
        detail=f"max |r_(0,2)/72 - r_(0,3)/200| = {profile_gap:.12f}",
    )
    check(
        "There is an explicit witness pair with the same fixed retained pair and the same fixed Tau_(>1)",
        abs(tau_p - tau_q) < 1.0e-12,
        detail=f"Tau(P)=Tau(Q)={tau_p:.12f}",
    )
    check(
        "That explicit witness pair yields distinct propagated retained triples, so fixed (rho_(1,0), rho_(1,1), Tau_(>1)) still does not determine the minimal finite target on the current coefficient-side bank",
        triple_gap > 1.0e-6,
        detail=f"max |Zhat(P)-Zhat(Q)| = {triple_gap:.12f}",
    )

    check(
        "At the three named sample points the explicit witness pair already stays positive, so this sharper no-go is not coming from a trivial sign crash on the seam",
        min_p > 0.0 and min_q > 0.0,
        detail=f"mins=({min_p:.12f}, {min_q:.12f})",
        bucket="SUPPORT",
    )
    check(
        "The older higher-orbit underdetermination theorem is consistent with this sharper result: that theorem fixed the first sample packet, while the new result fixes retained pair and Tau_(>1) and lets the propagated triple move",
        "same identity value and the same three named sample values" in higher_orbit_note
        and "higher-orbit beta-side coefficients would still not be" in higher_orbit_note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
