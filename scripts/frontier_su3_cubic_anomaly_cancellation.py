#!/usr/bin/env python3
"""
SU(3)³ cubic gauge anomaly cancellation theorem verification.

Verifies (*) in
  docs/SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md

  (*) Σ_R ε_R · A(R) · (multiplicity)  =  0    on retained SM content.

Where:
  ε_R = +1 for LH (or LH-conj of RH)
  A(3) = +1, A(3̄) = -1, A(1) = 0, A(6) = +7, A(8) = 0, ...

Authorities (all retained on main):
  - ONE_GENERATION_MATTER_CLOSURE_NOTE.md
  - GRAPH_FIRST_SU3_INTEGRATION_NOTE.md (N_c = 3)
  - LEFT_HANDED_CHARGE_MATCHING_NOTE.md (Q_L, L_L SU(3) reps)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import List, Tuple

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    return condition


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# --------------------------------------------------------------------------
# SU(3) anomaly indices
# --------------------------------------------------------------------------

ANOMALY_INDEX = {
    "1":   0,    # singlet
    "3":  +1,    # fundamental
    "3bar": -1,  # anti-fundamental
    "6":  +7,    # symmetric tensor
    "6bar": -7,
    "8":   0,    # adjoint
    "10": +27,
    "10bar": -27,
}


# --------------------------------------------------------------------------
# Retained one-generation SM content (LH-conjugate frame, all chiral fields LH)
# --------------------------------------------------------------------------

@dataclass
class WeylFermion:
    name: str
    su3_rep: str         # one of ANOMALY_INDEX keys
    su2_mult: int        # SU(2) multiplicity (2 for doublet, 1 for singlet)

    @property
    def anomaly_contribution(self) -> int:
        """Σ multiplicity × A(R) for this fermion."""
        return self.su2_mult * ANOMALY_INDEX[self.su3_rep]


# Retained one-generation SM in LH-conjugate frame
ONE_GEN_FERMIONS = [
    WeylFermion("Q_L",     su3_rep="3",    su2_mult=2),
    WeylFermion("u_R^c",   su3_rep="3bar", su2_mult=1),
    WeylFermion("d_R^c",   su3_rep="3bar", su2_mult=1),
    WeylFermion("L_L",     su3_rep="1",    su2_mult=2),
    WeylFermion("e_R^c",   su3_rep="1",    su2_mult=1),
    WeylFermion("nu_R^c",  su3_rep="1",    su2_mult=1),
]


# --------------------------------------------------------------------------
# Part 0: anomaly index reference values
# --------------------------------------------------------------------------

def part0_reference_values() -> None:
    banner("Part 0: SU(3) anomaly indices A(R) (textbook reference)")

    expected = [
        ("1 (singlet)",       "1",      0),
        ("3 (fundamental)",   "3",     +1),
        ("3̄ (anti-fund)",     "3bar",  -1),
        ("8 (adjoint)",       "8",      0),
        ("6 (sym tensor)",    "6",     +7),
        ("6̄ (sym anti)",      "6bar",  -7),
    ]
    for name, key, val in expected:
        check(
            f"A({name}) = {val}",
            ANOMALY_INDEX[key] == val,
            f"runtime value: {ANOMALY_INDEX[key]}",
        )

    # Verify A(R̄) = -A(R)
    check(
        "A(3̄) = -A(3) [conjugate-rep relation]",
        ANOMALY_INDEX["3bar"] == -ANOMALY_INDEX["3"],
        f"A(3̄) = {ANOMALY_INDEX['3bar']}, -A(3) = {-ANOMALY_INDEX['3']}",
    )
    check(
        "A(6̄) = -A(6)",
        ANOMALY_INDEX["6bar"] == -ANOMALY_INDEX["6"],
        f"A(6̄) = {ANOMALY_INDEX['6bar']}, -A(6) = {-ANOMALY_INDEX['6']}",
    )


# --------------------------------------------------------------------------
# Part 1: enumerate retained content
# --------------------------------------------------------------------------

def part1_content_audit() -> None:
    banner("Part 1: retained one-generation SM content (LH-conjugate frame)")

    print(f"  {'field':>10s}  {'SU(3) rep':>10s}  {'A(R)':>5s}  {'SU(2) mult':>10s}  {'contribution':>13s}")
    total = 0
    for f in ONE_GEN_FERMIONS:
        contribution = f.anomaly_contribution
        a_r = ANOMALY_INDEX[f.su3_rep]
        print(f"  {f.name:>10s}  {f.su3_rep:>10s}  {a_r:>+5d}  {f.su2_mult:>10d}  {contribution:>+13d}")
        total += contribution
    print(f"  {' ' * 50} Total: {total:+d}")
    print()

    check(
        "Q_L contributes +2 (= 2 × A(3) = 2)",
        ONE_GEN_FERMIONS[0].anomaly_contribution == 2,
        f"Q_L: {ONE_GEN_FERMIONS[0].anomaly_contribution}",
    )
    check(
        "u_R^c contributes -1 (= 1 × A(3̄) = -1)",
        ONE_GEN_FERMIONS[1].anomaly_contribution == -1,
        f"u_R^c: {ONE_GEN_FERMIONS[1].anomaly_contribution}",
    )
    check(
        "d_R^c contributes -1",
        ONE_GEN_FERMIONS[2].anomaly_contribution == -1,
        f"d_R^c: {ONE_GEN_FERMIONS[2].anomaly_contribution}",
    )
    check(
        "Leptons (L_L, e_R^c, ν_R^c) contribute 0 (SU(3) singlets)",
        sum(f.anomaly_contribution for f in ONE_GEN_FERMIONS[3:]) == 0,
        f"sum = {sum(f.anomaly_contribution for f in ONE_GEN_FERMIONS[3:])}",
    )


# --------------------------------------------------------------------------
# Part 2: (*) cancellation condition
# --------------------------------------------------------------------------

def part2_cancellation() -> None:
    banner("Part 2: (*) Σ ε A(R) = 0 on retained content")

    total = sum(f.anomaly_contribution for f in ONE_GEN_FERMIONS)
    print(f"  Σ A(R) = +2 - 1 - 1 + 0 + 0 + 0 = {total}")
    print()

    check(
        "(*) Σ ε A(R) = 0 on retained one-generation content",
        total == 0,
        f"total = {total}",
    )

    # Three-generation total (each generation gives 0, so total is 0)
    three_gen_total = 3 * total
    check(
        "Three-generation total = 0 (each generation cancels independently)",
        three_gen_total == 0,
        f"3 × 0 = {three_gen_total}",
    )


# --------------------------------------------------------------------------
# Part 3: net 3-vs-3̄ structural count
# --------------------------------------------------------------------------

def part3_net_count_structural() -> None:
    banner("Part 3: 'net 3 - 3̄ = 0' structural form")

    # Count fundamentals and anti-fundamentals weighted by SU(2) multiplicity
    n_fund = sum(f.su2_mult for f in ONE_GEN_FERMIONS if f.su3_rep == "3")
    n_antifund = sum(f.su2_mult for f in ONE_GEN_FERMIONS if f.su3_rep == "3bar")
    n_singlet = sum(f.su2_mult for f in ONE_GEN_FERMIONS if f.su3_rep == "1")

    print(f"  Net SU(3) fundamentals (weighted by SU(2) mult): {n_fund}")
    print(f"  Net SU(3) anti-fundamentals (weighted):           {n_antifund}")
    print(f"  Net SU(3) singlets (weighted):                    {n_singlet}")
    print(f"  Net (3 - 3̄) count:                                 {n_fund - n_antifund}")
    print()

    check(
        "Q_L contributes 2 fundamentals (3 of SU(3))",
        n_fund == 2,
        f"n_fund = {n_fund}",
    )
    check(
        "u_R^c + d_R^c contribute 2 anti-fundamentals (3̄)",
        n_antifund == 2,
        f"n_antifund = {n_antifund}",
    )
    check(
        "Net 3 - 3̄ = 0 (vector-like)",
        n_fund == n_antifund,
        f"3-fund - 3̄-fund = {n_fund - n_antifund}",
    )


# --------------------------------------------------------------------------
# Part 4: falsification scenarios
# --------------------------------------------------------------------------

def part4_falsification() -> None:
    banner("Part 4: falsification scenarios")

    base_total = sum(f.anomaly_contribution for f in ONE_GEN_FERMIONS)

    scenarios = [
        ("retained SM (Q_L + u_R + d_R + leptons)",                    base_total,                                            True),
        ("add 4th chiral fundamental (no partner)",                     base_total + 1,                                        False),
        ("add SU(3) sextet 6 (no sextet-bar)",                          base_total + ANOMALY_INDEX["6"],                       False),
        ("add 4th-gen Q_L only (no u_R^c, d_R^c)",                      base_total + 2 * ANOMALY_INDEX["3"],                   False),
        ("add full 4th gen (Q_L + u_R + d_R + leptons)",                2 * base_total,                                        True),
        ("remove u_R^c (incomplete RH completion)",                     base_total - (-1),                                     False),
        ("add chiral 3 + chiral 3̄ (vector-like pair)",                   base_total + 1 - 1,                                    True),
        ("add adjoint (8) - vector-like",                               base_total + ANOMALY_INDEX["8"],                       True),
    ]

    print(f"  {'scenario':<55s}  {'Σ ε A(R)':>10s}  {'consistent?':>12s}")
    for description, count, expected_consistent in scenarios:
        actual_consistent = (count == 0)
        marker = "✓" if actual_consistent else "✗"
        print(f"  {description:<55s}  {count:>+10d}  {marker:>12s}")
        check(
            f"{description}: {'cancels' if expected_consistent else 'fails'}",
            actual_consistent == expected_consistent,
            f"Σ = {count}, expected {'= 0' if expected_consistent else '≠ 0'}",
        )


# --------------------------------------------------------------------------
# Part 5: SU(2)³ vanishes trivially
# --------------------------------------------------------------------------

def part5_su2_cube_trivial() -> None:
    banner("Part 5: SU(2)³ ≡ 0 trivially (d^{abc} = 0 for SU(2))")

    # SU(2) has only 3 generators (Pauli/2). Their totally symmetric structure
    # constants d^{abc} all vanish because any symmetric rank-3 tensor with
    # 3 indices on the 3-dimensional Lie algebra of SU(2) is constrained.

    # Concrete: for SU(2) = SO(3) ≅ a 3-dim Lie algebra, d^{abc} ≡ 0.
    # Hence A^{abc}(SU(2)³) = 0 for ANY matter content.

    print("  SU(2) has 3 generators T^a = σ^a / 2.")
    print("  The symmetric structure constants d^{abc} satisfy")
    print("    d^{abc}  =  2 Tr(T^a {T^b, T^c})  =  0")
    print("  for all a, b, c by direct computation on Pauli matrices.")
    print()
    print("  Therefore A^{abc}(SU(2)³) ≡ 0 identically, regardless of matter.")
    print()

    # Verify on Pauli matrices
    import numpy as np
    sigma = np.array([
        [[0, 1], [1, 0]],     # σ_x
        [[0, -1j], [1j, 0]],  # σ_y
        [[1, 0], [0, -1]],    # σ_z
    ])
    T = sigma / 2.0  # SU(2) generators in fundamental

    max_d = 0.0
    for a in range(3):
        for b in range(3):
            for c in range(3):
                anti_comm = T[b] @ T[c] + T[c] @ T[b]
                d_abc = 2 * np.trace(T[a] @ anti_comm).real
                if abs(d_abc) > max_d:
                    max_d = abs(d_abc)

    check(
        "SU(2) d^{abc} = 0 for all (a, b, c) (verified on Pauli matrices)",
        max_d < 1e-10,
        f"max |d^{{abc}}| = {max_d:.2e}",
    )

    print(f"  Verified: max |d^{{abc}}| over SU(2) generators = {max_d:.2e}")


# --------------------------------------------------------------------------
# Part 6: SU(3) d^{abc} computational verification
# --------------------------------------------------------------------------

def part6_su3_d_abc_nonzero() -> None:
    banner("Part 6: SU(3) d^{abc} ≠ 0 (so SU(3)³ cancellation is non-trivial)")

    # Gell-Mann matrices λ_a (a=1,...,8); T^a = λ^a / 2
    import numpy as np
    lam = np.zeros((8, 3, 3), dtype=complex)
    lam[0] = [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
    lam[1] = [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]]
    lam[2] = [[1, 0, 0], [0, -1, 0], [0, 0, 0]]
    lam[3] = [[0, 0, 1], [0, 0, 0], [1, 0, 0]]
    lam[4] = [[0, 0, -1j], [0, 0, 0], [1j, 0, 0]]
    lam[5] = [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
    lam[6] = [[0, 0, 0], [0, 0, -1j], [0, 1j, 0]]
    lam[7] = (1 / np.sqrt(3)) * np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]])

    T = lam / 2.0

    # Compute d^{abc} = 2 Tr(T^a {T^b, T^c}) and find max value
    d_max = 0.0
    nonzero_examples: List[Tuple[int, int, int, float]] = []
    for a in range(8):
        for b in range(8):
            for c in range(8):
                anti_comm = T[b] @ T[c] + T[c] @ T[b]
                d_abc = 2 * np.trace(T[a] @ anti_comm).real
                if abs(d_abc) > d_max:
                    d_max = abs(d_abc)
                if abs(d_abc) > 0.1:
                    nonzero_examples.append((a + 1, b + 1, c + 1, d_abc))

    check(
        "SU(3) has non-zero d^{abc} (cubic anomaly is non-trivial)",
        d_max > 0.5,
        f"max |d^{{abc}}| = {d_max:.4f}",
    )

    print(f"  max |d^{{abc}}| = {d_max:.4f}")
    print(f"  Number of significant non-zero d^{{abc}} entries: {len(nonzero_examples)}")
    if len(nonzero_examples) > 0:
        a, b, c, val = nonzero_examples[0]
        print(f"  Example: d^{{{a},{b},{c}}} = {val:.4f}")


# --------------------------------------------------------------------------
# Part 7: summary
# --------------------------------------------------------------------------

def part7_summary() -> None:
    banner("Part 7: summary - SU(3)³ cubic gauge anomaly cancellation retained")

    print("  THEOREM (*): SU(3)³ pure-gauge cubic anomaly vanishes on retained")
    print("              one-generation SM content:")
    print()
    print("    Σ ε A(R)  =  +2 (Q_L) − 1 (u_R^c) − 1 (d_R^c)  =  0  ✓")
    print()
    print("  STRUCTURAL FORM: 'net 3 − 3̄ = 0' (vector-like in SU(3))")
    print("    2 fundamentals (Q_L doublet × 1 colour-3) and")
    print("    2 anti-fundamentals (u_R^c + d_R^c) precisely cancel.")
    print()
    print("  COMPLEMENT: SU(2)³ ≡ 0 trivially (d^{abc} = 0 for SU(2)),")
    print("              so SU(3)³ is the non-trivial cubic-gauge condition.")
    print()
    print("  RETAINED RH FERMION ROLE:")
    print("    Both u_R AND d_R are required for SU(3)³ cancellation.")
    print("    Removing either restores anomaly.")
    print()
    print("  FALSIFICATION:")
    print("    - 4th chiral fundamental without partner → +1 → anomaly")
    print("    - SU(3) sextet without sextet-bar       → +7 → anomaly")
    print("    - any unbalanced SU(3)-charged content   → ≠ 0 → anomaly")
    print()
    print("  DOES NOT CLAIM:")
    print("    - Perturbative-Y anomalies (in ANOMALY_FORCES_TIME)")
    print("    - Witten Z₂ (in SU2_WITTEN_Z2_ANOMALY)")
    print("    - Native uniqueness of N_c = 3 (separate retained theorem)")
    print("    - SM is the only SU(3)³-anomaly-free completion")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    print("=" * 88)
    print("SU(3)³ cubic gauge anomaly cancellation theorem verification")
    print("See docs/SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md")
    print("=" * 88)

    part0_reference_values()
    part1_content_audit()
    part2_cancellation()
    part3_net_count_structural()
    part4_falsification()
    part5_su2_cube_trivial()
    part6_su3_d_abc_nonzero()
    part7_summary()

    print()
    print("=" * 88)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
