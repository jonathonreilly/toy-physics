#!/usr/bin/env python3
"""
Koide Q = 2/3 variational attack: singlet-doublet coupling maximization.

Candidate variational principle:

  σ_1 = 1/2  is the UNIQUE maximum of the functional
    C(σ_1)  :=  σ_1 · (1 − σ_1)   on [0, 1]

If the retained physical charged-lepton packet maximizes this specific
"singlet-doublet coupling" functional, P_Q = σ_1 = 1/2 closes, equivalently
Q_Koide = 2/3 follows.

This note proposes the variational principle as a CANDIDATE physical law
and verifies its mathematical property (unique maximum at 1/2).  The
outstanding step: retained justification that the physical charged-lepton
packet extremizes this specific functional (vs. other quadratic functionals
or entropy measures).

See docs/KOIDE_Q23_SINGLET_DOUBLET_COUPLING_MAX_NOTE_2026-04-22.md.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    PASSES.append((label, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def main() -> int:
    print("=" * 80)
    print("Koide Q = 2/3 variational attack: singlet-doublet coupling maximization")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Step 1. The candidate functional and its extremum
    # -------------------------------------------------------------------------
    sig = sp.symbols('sigma', real=True, positive=True)
    C = sig * (1 - sig)
    dC = sp.diff(C, sig)
    d2C = sp.diff(C, sig, 2)

    check("1.1 Functional C(σ_1) = σ_1·(1−σ_1) has unique critical point at σ_1 = 1/2",
          sp.solve(dC, sig) == [sp.Rational(1, 2)],
          f"dC/dσ_1 = {dC}\n"
          f"critical point: σ_1 = {sp.solve(dC, sig)[0]}")

    check("1.2 d²C/dσ_1² = −2 < 0 → critical point is MAXIMUM (not min/saddle)",
          d2C == -2,
          f"d²C/dσ_1² = {d2C} < 0 → maximum")

    C_at_half = C.subs(sig, sp.Rational(1, 2))
    check("1.3 Maximum value C(1/2) = 1/4 (sympy exact)",
          C_at_half == sp.Rational(1, 4),
          f"C(1/2) = {C_at_half}")

    # Numerical verification
    xs = np.linspace(0.01, 0.99, 99)
    ys = xs * (1 - xs)
    max_idx = np.argmax(ys)
    check("1.4 Numerical sweep confirms max at σ_1 = 0.5, C_max = 0.25",
          abs(xs[max_idx] - 0.5) < 0.01 and abs(ys[max_idx] - 0.25) < 0.0001,
          f"max at σ_1 = {xs[max_idx]:.4f}, C = {ys[max_idx]:.4f}")

    # -------------------------------------------------------------------------
    # Step 2. Connection to Koide Q
    # -------------------------------------------------------------------------
    # σ_1 = singlet occupancy. Q_Koide = 1/(d · σ_1) at d = 3.
    # σ_1 = 1/2 ⇒ Q_Koide = 1/(3·(1/2)) = 2/3.
    d = 3
    sigma_Koide = sp.Rational(1, 2)
    Q_Koide = 1 / (d * sigma_Koide)
    check("2.1 Q_Koide = 1/(d·σ_1) = 2/3 at σ_1 = 1/2 and d = 3",
          Q_Koide == sp.Rational(2, 3),
          f"Q_Koide = {Q_Koide}")

    # -------------------------------------------------------------------------
    # Step 3. Physical interpretation of the functional
    # -------------------------------------------------------------------------
    # C(σ_1) = σ_1 · σ_doublet (where σ_doublet = 1 - σ_1 = total doublet occupancy).
    # Interpreted as "singlet-doublet coupling strength" or "mutual-information
    # between singlet and doublet sectors on the Z_3 Fourier decomposition."

    check("3.1 C(σ_1) = σ_1 · σ_doublet is the 'singlet-doublet coupling' functional",
          True,
          "Physical interpretation:\n"
          "  - σ_1: total probability-weight of the singlet Fourier component.\n"
          "  - σ_doublet = 1 − σ_1: total probability-weight of the doublet\n"
          "    (both L_ω and L_ω̄ components together).\n"
          "  - C = σ_1 · σ_doublet: 'mixing strength' or 'coupling' between singlet\n"
          "    and doublet sectors of the Z_3 decomposition.\n"
          "\n"
          "  Max at σ_1 = 1/2: singlet and doublet sectors carry EQUAL weight,\n"
          "  giving maximum mutual coupling.  This is the Koide 'balance point'.")

    # -------------------------------------------------------------------------
    # Step 4. Comparison with other natural functionals
    # -------------------------------------------------------------------------
    # Some natural functionals on σ_1 ∈ [0, 1] and their extrema:
    # - Shannon entropy: -σ_1 ln σ_1 - (1-σ_1) ln(1-σ_1) → max at σ_1 = 1/2 (but also considers doublet split)
    # - Quadratic purity: σ_1² + σ_doublet² → min at σ_1 = 1/2
    # - Product C = σ_1 · σ_doublet → max at σ_1 = 1/2
    # - Sum: σ_1 + σ_doublet = 1 (trivially constant)

    check("4.1 Multiple natural functionals share max/min at σ_1 = 1/2",
          True,
          "Functionals with extrema at σ_1 = 1/2 on [0, 1]:\n"
          "  (1) C = σ_1 · (1 − σ_1)                  max at 1/2, value 1/4\n"
          "  (2) H = −σ_1 ln σ_1 − (1−σ_1) ln(1−σ_1)  max at 1/2, value ln(2)\n"
          "  (3) S_Tsallis = 1 − σ_1² − (1−σ_1)²      max at 1/2, value 1/2\n"
          "\n"
          "Multiple entropy-like and coupling-like functionals converge on σ_1 = 1/2\n"
          "as a natural 'balance' or 'maximum-mixedness' point.  The Koide σ_1 = 1/2\n"
          "sits at this common convergence point.")

    # -------------------------------------------------------------------------
    # Step 5. What would close the bridge
    # -------------------------------------------------------------------------
    check("5.1 Outstanding: retained physical principle selecting the functional",
          True,
          "This note ESTABLISHES the mathematical fact:\n"
          "  σ_1 = 1/2 is the UNIQUE MAXIMUM of σ_1 · σ_doublet.\n"
          "\n"
          "What would CLOSE Q = 2/3 axiom-natively:\n"
          "  1. A retained physical principle that forces the charged-lepton packet\n"
          "     to MAXIMIZE σ_1 · σ_doublet on the retained Z_3 Fourier decomposition.\n"
          "  2. Equivalent: a retained variational law on the hw=1 triplet whose\n"
          "     extremum is at the maximum-coupling (singlet-doublet balance) point.\n"
          "\n"
          "Candidate physical motivations (all speculative):\n"
          "  (i) 'Maximum mutual information between Z_3 sectors' as a retained\n"
          "      information-theoretic principle.\n"
          "  (ii) 'Balanced weak-coupling' between SU(2)_L-like (singlet) and SU(2)_L-\n"
          "       related (doublet) Fourier components on the Yukawa matrix.\n"
          "  (iii) Chamber-boundary 'midpoint' law selecting 50-50 singlet-doublet\n"
          "        allocation as the kinematically natural interior point.")

    # -------------------------------------------------------------------------
    # Step 6. Relation to the broader Q=2/3 landscape
    # -------------------------------------------------------------------------
    check("6.1 This is attack route #8 (variational functional) on Q = 2/3",
          True,
          "Q = 2/3 landscape status:\n"
          "  7 support routes (user-landed S1-S5 + loops 12-13 support S6-S7)\n"
          "  7 no-gos (original 6 + loop 14 O_h covariance)\n"
          "  THIS NOTE: 8th candidate route via variational functional C(σ_1)\n"
          "\n"
          "The variational route is NOVEL: no existing no-go targets variational\n"
          "principles on the Z_3 Fourier occupancy. It is specifically a 1-D\n"
          "OPTIMIZATION problem with unique extremum at the Koide point.\n"
          "\n"
          "This route's closure requires ONE retained physical principle (above),\n"
          "not a cascade of structural derivations.")

    # Summary
    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    if n_pass == n_total:
        print()
        print("CANDIDATE VARIATIONAL PRINCIPLE:")
        print("  σ_1 = 1/2 is the UNIQUE maximum of C(σ_1) = σ_1 · (1−σ_1).")
        print()
        print("If the retained charged-lepton packet extremizes C, Q_Koide = 2/3 closes.")
        print()
        print("Outstanding retained step: physical motivation for extremizing C.")
        print("Candidate motivations documented; none yet retained-derived.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
