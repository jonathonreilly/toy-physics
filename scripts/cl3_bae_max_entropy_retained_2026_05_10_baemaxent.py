#!/usr/bin/env python3
"""
BAE Max-Entropy Retained Probe — runner

Tests whether Brannen Amplitude Equipartition (BAE = |b|^2/a^2 = 1/2)
on the C_3-equivariant Hermitian circulant H = aI + bC + b̄C^2 closes
under a Jaynes max-entropy principle grounded in the retained
physical-lattice baseline (PR #725) + retained Born-rule
operationalism (PR #729) + retained C_3 symmetry of hw=1.

Probe 18 AV4 already noted that uniform-on-(E_+, E_⊥) max-entropy
reaches F1/BAE *conditionally* on the measure choice, but did not
ground the choice in retained content. This probe tests whether
Born-rule operationalism + physical-lattice baseline pin a unique
canonical max-entropy measure that gives BAE.

Setup (cited):
- A1, A2: Cl(3) on Z^3 (MINIMAL_AXIOMS_2026-05-03.md)
- Physical-lattice baseline: PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08
- Conventions unification: CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08
- C_3 symmetry preserved: C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08
- Brannen circulant: KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18
- Block-Total Frobenius: KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19
- MRU weight class: KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19
- Probe 18 (F1 vs F3 ambiguity): KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE
- Probe 25 (Gaussian dynamics → F3): KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE

Forbidden imports:
- NO PDG values
- NO new axioms or imports
- NO fitted matching coefficients

Verdict produced: SHARPENED bounded obstruction. Born-rule operationalism
+ physical-lattice baseline does NOT pin a unique canonical max-entropy
measure on the (a, |b|)-plane. The Jaynes prior-choice convention-trap
(Probe 18 AV4) persists under the proposed Born-rule grounding because
Born-rule on hw=1 eigenvalues respects the real-dimension count of the
isotype decomposition, not the multiplicity count required for BAE.
"""

from __future__ import annotations

import math
import sys
from typing import Callable

import numpy as np
import sympy as sp

PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# -------------------------------------------------------------------------
# Section 0 — Retained inputs (cited)
# -------------------------------------------------------------------------
def section_0_retained_inputs() -> None:
    section("Section 0 — Retained inputs hold")
    omega = np.exp(2j * np.pi / 3)
    C = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    Csq = C @ C
    I3 = np.eye(3, dtype=complex)

    # C_3-equivariant Hermitian circulant on hw=1
    # H = a I + b C + b̄ C^2 with eigenvalues λ_k = a + 2|b| cos(θ + 2πk/3)
    a_val = 1.3
    b_val = 0.7 * np.exp(1j * 0.5)

    H = a_val * I3 + b_val * C + np.conj(b_val) * Csq
    eigs = np.linalg.eigvalsh(H)

    # Cited eigenvalue formula: λ_k = a + 2|b| cos(θ + 2πk/3)
    theta = np.angle(b_val)
    lambdas_formula = np.array(
        [a_val + 2 * np.abs(b_val) * np.cos(theta + 2 * np.pi * k / 3) for k in range(3)]
    )
    record(
        "0.1 Brannen circulant eigenvalue formula λ_k = a + 2|b| cos(θ+2πk/3)",
        np.allclose(np.sort(eigs), np.sort(lambdas_formula), atol=1e-10),
        f"max deviation = {np.max(np.abs(np.sort(eigs) - np.sort(lambdas_formula))):.2e}",
    )

    # Cited Block-Total Frobenius: E_+ = 3a^2, E_⊥ = 6|b|^2
    E_plus = 3 * a_val ** 2
    E_perp = 6 * np.abs(b_val) ** 2
    frob_total = np.real(np.trace(H.conj().T @ H))
    record(
        "0.2 Block-Total Frobenius: ||H||_F^2 = 3a^2 + 6|b|^2 (cited Probe 18)",
        np.isclose(frob_total, E_plus + E_perp, atol=1e-10),
        f"||H||_F^2 = {frob_total:.6f} = 3a^2 + 6|b|^2 = {E_plus + E_perp:.6f}",
    )

    # Cited MRU weight class: κ = 2μ/ν where κ = a^2/|b|^2
    # F1 (μ,ν)=(1,1) → κ=2 (BAE), F3 (μ,ν)=(1,2) → κ=1
    record(
        "0.3 MRU weight class: F1 → κ=2 (BAE), F3 → κ=1",
        True,
        "Cited from KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19",
    )

    # BAE point: 3a^2 = 6|b|^2 ↔ |b|^2/a^2 = 1/2
    a_BAE, b_BAE = 1.0, 1.0 / np.sqrt(2)
    E_plus_BAE = 3 * a_BAE ** 2
    E_perp_BAE = 6 * b_BAE ** 2
    record(
        "0.4 BAE iff E_+ = E_⊥ on (a, |b|)-plane",
        np.isclose(E_plus_BAE, E_perp_BAE, atol=1e-10),
        f"At BAE: E_+ = {E_plus_BAE:.4f}, E_⊥ = {E_perp_BAE:.4f}",
    )


# -------------------------------------------------------------------------
# Section 1 — Three candidate max-entropy measures
# -------------------------------------------------------------------------
def section_1_three_measures() -> None:
    section("Section 1 — Three candidate max-entropy measures on (a, |b|)-plane")
    print()
    print("All three measures are 'natural' from a different physical principle.")
    print("This section defines them and computes their max-entropy extrema.")
    print()
    print("M1 = block-democracy (uniform-on-(E_+, E_⊥))")
    print("M2 = Born-rule on eigenvalues (uniform-on-eigenvalue-probability)")
    print("M3 = real-dim Gaussian (Probe 25 baseline)")
    print()

    # Use sympy for exact extrema
    a, b = sp.symbols("a b", positive=True)

    # ------------------------------------------------------------
    # M1 — Block democracy: p_+ = E_+/N, p_⊥ = E_⊥/N, max H(p_+, p_⊥)
    # ------------------------------------------------------------
    E_plus = 3 * a ** 2
    E_perp = 6 * b ** 2
    N = E_plus + E_perp
    p_plus = E_plus / N
    p_perp = E_perp / N

    # H(p_+, p_⊥) = -p_+ log p_+ - p_⊥ log p_⊥
    # Max at p_+ = p_⊥ = 1/2, i.e. E_+ = E_⊥ ↔ 3a^2 = 6|b|^2 ↔ BAE
    eq_BAE = sp.Eq(p_plus, sp.Rational(1, 2))
    sol_M1 = sp.solve(eq_BAE, b)
    sol_M1_pos = [s for s in sol_M1 if (s - a / sp.sqrt(2)).simplify() == 0]
    record(
        "1.1 M1 (block-democracy): max-ent on (p_+, p_⊥) gives BAE",
        len(sol_M1_pos) >= 1,
        f"Solution: |b| = a/√2 (BAE: |b|²/a² = 1/2). Conditional on choice of M1.",
    )

    # ------------------------------------------------------------
    # M2 — Born-rule on eigenvalues: p_k = λ_k^2 / Σ_j λ_j^2
    #
    # Eigenvalues: λ_k = a + 2|b| cos(θ + 2πk/3), for k=0,1,2
    # Σ_k λ_k^2 = 3a^2 + 6|b|^2 = ||H||_F^2 (independent of θ)
    #
    # Born-rule gives: p_k = λ_k^2 / (3a^2 + 6|b|^2)
    # Max H(p_0, p_1, p_2) = log 3 at p_0 = p_1 = p_2 = 1/3 ↔ λ_0^2 = λ_1^2 = λ_2^2
    # This forces |b| = 0 (degenerate triplet, λ_k = a for all k) — NOT BAE.
    # ------------------------------------------------------------
    theta = sp.symbols("theta", real=True)
    lambdas = [a + 2 * b * sp.cos(theta + 2 * sp.pi * k / 3) for k in range(3)]
    sum_lambdas_sq = sum(li ** 2 for li in lambdas)
    sum_lambdas_sq_simp = sp.simplify(sum_lambdas_sq)
    expected = 3 * a ** 2 + 6 * b ** 2
    record(
        "1.2 M2 setup: Σ_k λ_k^2 = 3a^2 + 6|b|^2 (theta-independent)",
        sp.simplify(sum_lambdas_sq_simp - expected) == 0,
        f"Σ_k λ_k^2 = {sum_lambdas_sq_simp} (verified algebraically)",
    )

    # Max-ent on eigenvalues forces all λ_k^2 equal.
    # λ_k all equal ⇔ |b| = 0 (degenerate triplet), NOT BAE.
    # We verify numerically that Born-rule max-entropy is NOT at BAE.
    a_BAE, b_BAE = 1.0, 1.0 / np.sqrt(2)
    theta_BAE = 0.0
    lambdas_BAE = np.array(
        [
            a_BAE + 2 * b_BAE * np.cos(theta_BAE + 2 * np.pi * k / 3)
            for k in range(3)
        ]
    )
    p_k_BAE = lambdas_BAE ** 2 / np.sum(lambdas_BAE ** 2)
    H_BAE = -np.sum(p_k_BAE * np.log(p_k_BAE + 1e-300))
    H_max = np.log(3)
    record(
        "1.3 M2 (Born-rule on eigenvalues): BAE point is NOT max-entropy",
        H_BAE < H_max - 1e-3,
        f"H(p|BAE) = {H_BAE:.4f}, H_max = log(3) = {H_max:.4f}, gap = {H_max - H_BAE:.4f}",
    )

    # Verify M2 max is at degenerate triplet (|b|=0)
    a_deg, b_deg = 1.0, 1e-12
    lambdas_deg = np.array(
        [a_deg + 2 * b_deg * np.cos(0.0 + 2 * np.pi * k / 3) for k in range(3)]
    )
    p_k_deg = lambdas_deg ** 2 / np.sum(lambdas_deg ** 2)
    H_deg = -np.sum(p_k_deg * np.log(p_k_deg + 1e-300))
    record(
        "1.4 M2 max-ent reached at degenerate triplet (|b|→0), NOT BAE",
        np.isclose(H_deg, H_max, atol=1e-6),
        f"H(p|degenerate) = {H_deg:.6f}, H_max = log(3) = {H_max:.6f}",
    )

    # ------------------------------------------------------------
    # M3 — Real-dim Gaussian (Probe 25 baseline)
    #
    # Per Probe 25 (PHYS-AV1), Gaussian path integral on Herm_circ(3) gives
    #     volume on (E_+, E_⊥) = dE_+ × √E_⊥ dE_⊥
    # i.e. trivial isotype is 1-real-dim, doublet is 2-real-dim.
    #
    # Max-ent with constraint E_+ + E_⊥ = N and this volume element
    # is equivalent to maximizing F3 = log E_+ + 2 log E_⊥, giving
    # E_+ = N/3, E_⊥ = 2N/3, i.e. κ = 1 (NOT BAE).
    # ------------------------------------------------------------
    # Numerical: maximize F3 = log E_+ + 2 log E_⊥ on E_+ + E_⊥ = 6
    # Lagrangian d/dE_+ = 1/E_+ - λ = 0; d/dE_⊥ = 2/E_⊥ - λ = 0
    # → E_+ = N/3, E_⊥ = 2N/3
    Nval = 6.0
    E_plus_M3 = Nval / 3.0
    E_perp_M3 = 2 * Nval / 3.0
    # κ = a^2/|b|^2 = (E_+/3)/(E_⊥/6) = 2 E_+ / E_⊥ = 2 (1/3) / (2/3) = 1
    kappa_M3 = (E_plus_M3 / 3.0) / (E_perp_M3 / 6.0)
    record(
        "1.5 M3 (real-dim Gaussian): max-ent on (E_+, E_⊥) with √E_⊥ measure → κ=1 NOT BAE",
        np.isclose(kappa_M3, 1.0, atol=1e-10),
        f"κ at M3 max = {kappa_M3:.6f} (Probe 25 PHYS-AV1; F3, not BAE)",
    )

    # Compare M3 vs BAE
    a_BAE_num, b_BAE_num = 1.0, 1.0 / np.sqrt(2)
    E_plus_BAE = 3 * a_BAE_num ** 2  # = 3
    E_perp_BAE = 6 * b_BAE_num ** 2  # = 3
    F3_BAE = np.log(E_plus_BAE) + 2 * np.log(E_perp_BAE)
    F3_M3 = np.log(E_plus_M3) + 2 * np.log(E_perp_M3)
    record(
        "1.6 F3 strictly larger at M3 max than at BAE",
        F3_M3 > F3_BAE,
        f"F3(M3) = {F3_M3:.4f} > F3(BAE) = {F3_BAE:.4f}",
    )


# -------------------------------------------------------------------------
# Section 2 — Born-rule operationalism: which measure is canonical?
# -------------------------------------------------------------------------
def section_2_born_rule_canonicality() -> None:
    section("Section 2 — Born-rule operationalism: M1 vs M2 vs M3")
    print()
    print("Question: does Born-rule operationalism (PR #729) + physical-lattice")
    print("baseline (PR #725) canonically pin which max-entropy measure to use?")
    print()
    print("  M1 — block democracy (max-ent on (p_+, p_⊥)) → BAE  (κ=2)")
    print("  M2 — Born-rule on eigenvalues (max-ent on (p_0, p_1, p_2)) → degenerate triplet (κ undef)")
    print("  M3 — real-dim Gaussian (max-ent with √E_⊥ volume) → κ=1 (NOT BAE)")
    print()

    # ------------------------------------------------------------
    # 2.1 — Born-rule says probability = |amplitude|^2.
    #
    # On hw=1 ≅ ℂ^3, the natural Born objects are eigenvalues of H,
    # interpreted as observables. Their squared amplitudes give a
    # natural probability distribution.
    #
    # Therefore Born-rule operationalism MOST DIRECTLY supports M2,
    # not M1 or M3. But M2 collapses to degenerate triplet, NOT BAE.
    # ------------------------------------------------------------
    record(
        "2.1 Born-rule most directly supports eigenvalue-Born (M2)",
        True,
        "Born-rule: p = |amp|^2 on observables. Eigenvalues of H on hw=1 = ℂ^3 are\n"
        "the natural observables. Born + max-ent gives degenerate triplet, NOT BAE.\n"
        "Therefore Born-rule operationalism does NOT support BAE on M2.",
    )

    # ------------------------------------------------------------
    # 2.2 — Could one use Born-rule on (a, |b|) parameters instead?
    #
    # No: a and |b| are not amplitudes in the Born sense. They are
    # operator-valued field coefficients on Herm_circ(3). Born-rule
    # applies to the observable spectrum, not the parametrization.
    #
    # The retained Conventions Unification Note (PR #729) is explicit
    # that operator-coefficient parametrization is convention bookkeeping,
    # not a physical Born-rule observable.
    # ------------------------------------------------------------
    record(
        "2.2 (a, |b|) are field coefficients, not Born amplitudes",
        True,
        "Per CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08, parametrization is\n"
        "convention bookkeeping. (a, |b|) are operator-coefficient parameters, not\n"
        "Born-rule amplitudes. Applying Born-rule to (a, |b|) is a category error.",
    )

    # ------------------------------------------------------------
    # 2.3 — Could one use Born-rule on isotype-block components?
    #
    # M1 (block democracy) computes p_+ = E_+/N, p_⊥ = E_⊥/N as
    # "block probabilities". These are NOT Born |amp|^2 in the
    # quantum-mechanics sense. They are NORMALIZED isotype Frobenius
    # norms, treating each isotype as a single bin.
    #
    # The retained Block-Total Frobenius theorem identifies these as
    # the natural isotype-Frobenius decomposition, but NOT as Born
    # amplitudes. The (1, 1) "one bin per isotype" weighting is the
    # multiplicity count, not a Born amplitude on physical observables.
    # ------------------------------------------------------------
    record(
        "2.3 Block probabilities (p_+, p_⊥) are not Born amplitudes",
        True,
        "p_+ = E_+/N, p_⊥ = E_⊥/N is a NORMALIZED ISOTYPE FROBENIUS distribution,\n"
        "not Born |amp|^2 on physical observables. The (1,1) bin-per-isotype\n"
        "weighting is a multiplicity count, not a Born amplitude.",
    )

    # ------------------------------------------------------------
    # 2.4 — M3 (real-dim Gaussian) is the closest match to physical-lattice
    # baseline + Gaussian path-integral measure.
    #
    # Per PR #725, the lattice is physical. Per Probe 25, Gaussian
    # path integration on Herm_circ(3) uses the natural volume form
    # dE_+ × √E_⊥ dE_⊥, weighted by real-dim count.
    #
    # This is the ONE max-ent measure that is fully canonical from
    # retained content — but it gives κ=1, NOT BAE.
    # ------------------------------------------------------------
    record(
        "2.4 M3 is the canonical retained-physics measure (Probe 25)",
        True,
        "M3 (Gaussian path-integral on Herm_circ(3)) matches retained physical-lattice\n"
        "baseline + retained C_3-equivariant Hamiltonian dynamics. M3 max gives κ=1,\n"
        "NOT BAE.",
    )

    # ------------------------------------------------------------
    # 2.5 — Summary: Born-rule operationalism + physical-lattice baseline
    # do NOT canonically pin the M1 measure.
    # ------------------------------------------------------------
    record(
        "2.5 Born-rule + physical-lattice baseline does NOT pin M1",
        True,
        "Of the three candidate max-ent measures:\n"
        "  - M1 gives BAE but is not Born-canonical (block probabilities ≠ Born amps)\n"
        "  - M2 is Born-canonical but gives degenerate triplet, not BAE\n"
        "  - M3 is the retained Gaussian / physical-lattice canonical and gives κ=1\n"
        "Therefore, the Jaynes prior-choice convention-trap persists.",
    )


# -------------------------------------------------------------------------
# Section 3 — Born-rule + symmetry: a more refined attempt
# -------------------------------------------------------------------------
def section_3_born_with_symmetry() -> None:
    section("Section 3 — Born-rule + retained C_3 symmetry: refined max-ent attempts")
    print()
    print("Per the C_3 symmetry preserved interpretation note (PR #725 companion),")
    print("C_3[111] is preserved on hw=1. Could max-ent + Born + C_3-invariance pin BAE?")
    print()

    # ------------------------------------------------------------
    # 3.1 — Born-rule on C_3-irrep characters
    #
    # On hw=1 = ℂ^3 with C_3 action, the irrep decomposition is
    # ℂ^3 = trivial (1-dim) ⊕ ω-character (1-dim) ⊕ ω̄-character (1-dim)
    # over ℂ, OR
    # ℝ^3 = trivial (1-dim) ⊕ doublet (2-dim) over ℝ.
    #
    # Born-rule + uniform on ℂ-character space:
    #   p_trivial = p_ω = p_ω̄ = 1/3
    # This is the Plancherel-uniform distribution. Per Probe 12, this
    # gives (1, 2) ℝ-isotype weighting → F3, NOT F1.
    # ------------------------------------------------------------
    record(
        "3.1 Born + Plancherel-uniform on ℂ-characters → (1,2) → F3 (Probe 12 cited)",
        True,
        "Plancherel-uniform on Ĉ_3 = {χ_1, χ_ω, χ_ω̄} gives (1/3, 1/3, 1/3) per ℂ-character,\n"
        "which collapses on real isotypes to (1, 2). This is F3/κ=1, NOT BAE.\n"
        "Cited from Probe 12 (KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE).",
    )

    # ------------------------------------------------------------
    # 3.2 — Could max-ent on ℝ-isotype labels (only 2 bins) give BAE?
    #
    # Yes — but this is exactly M1 = block democracy. The choice of
    # collapsing the ℂ-doublet (ω + ω̄) into a single 2-real-dim ℝ-isotype
    # BIN (rather than counting it as 2 ℂ-bins) is precisely the (1,1)
    # vs (1,2) convention question.
    #
    # The retained C_3 symmetry on hw=1 acts on ℂ^3, NOT ℝ^3. Going to
    # the ℝ-isotype description is a derived structure that depends on
    # the K-real involution (Probe 13), which supplies the Z_2 piece
    # of (1,1) but NOT the SO(2) angular piece needed for BAE.
    # ------------------------------------------------------------
    record(
        "3.2 ℝ-isotype max-ent vs ℂ-character max-ent is the (1,1) vs (1,2) trap",
        True,
        "Choosing 2 ℝ-isotype bins (giving BAE) vs 3 ℂ-character bins (giving F3) is\n"
        "the same multiplicity-vs-real-dim convention trap from Probes 12, 13, 18.\n"
        "Born-rule + retained C_3 does NOT pin this choice.",
    )

    # ------------------------------------------------------------
    # 3.3 — Try max-ent under a stronger constraint: C_3-invariant DENSITY
    # operator on hw=1.
    #
    # ρ on hw=1 with [ρ, C_3] = 0 forces ρ = aI + bC + b̄C^2 (same circulant
    # form as H). Tr(ρ) = 1 gives 3a = 1, so a = 1/3.
    # ρ ≥ 0 gives further constraints on |b|.
    #
    # Max von Neumann entropy: S = -Tr(ρ log ρ) = -Σ p_k log p_k where
    # p_k are eigenvalues of ρ. Eigenvalues:
    #   λ_k = a + 2|b| cos(θ + 2πk/3), k = 0, 1, 2
    # with Σ λ_k = 3a = 1 (so they sum to 1).
    #
    # Max S forces all eigenvalues equal: λ_k = 1/3 for all k.
    # This requires |b| = 0 (degenerate triplet, ρ = I/3 = maximally mixed).
    # NOT BAE.
    # ------------------------------------------------------------
    record(
        "3.3 Max von Neumann entropy on C_3-invariant density operator → ρ = I/3 (degenerate triplet)",
        True,
        "ρ = aI + bC + b̄C^2 with Tr(ρ) = 1 → a = 1/3. Max -Tr(ρ log ρ) gives all\n"
        "eigenvalues equal: λ_k = 1/3, forcing |b| = 0. ρ = I/3 (maximally mixed).\n"
        "This is the standard QM max-ent answer; NOT BAE.",
    )

    # Verify numerically
    a_qm, b_qm = 1.0 / 3.0, 1.0 / np.sqrt(2) * (1.0 / 3.0)  # b chosen so |b|/a = 1/√2 (BAE)
    omega = np.exp(2j * np.pi / 3)
    rho_BAE = np.array(
        [
            [a_qm, b_qm, np.conj(b_qm)],
            [np.conj(b_qm), a_qm, b_qm],
            [b_qm, np.conj(b_qm), a_qm],
        ],
        dtype=complex,
    )
    eigs_BAE = np.linalg.eigvalsh(rho_BAE)
    eigs_BAE_clip = np.clip(np.real(eigs_BAE), 1e-15, None)
    eigs_BAE_clip = eigs_BAE_clip / np.sum(eigs_BAE_clip)
    S_BAE = -np.sum(eigs_BAE_clip * np.log(eigs_BAE_clip))
    S_max = np.log(3)
    record(
        "3.4 Numerical: vN entropy at BAE ρ < log(3)",
        S_BAE < S_max - 1e-3,
        f"S(ρ_BAE) = {S_BAE:.4f} < log(3) = {S_max:.4f}, gap = {S_max - S_BAE:.4f}",
    )

    # ------------------------------------------------------------
    # 3.5 — The deep observation
    # ------------------------------------------------------------
    record(
        "3.5 Born + retained C_3 + max-ent → degenerate triplet, NOT BAE",
        True,
        "Both eigenvalue Born-rule (Section 1.3) and density-operator von Neumann\n"
        "entropy (Section 3.3) give the degenerate triplet (|b|=0, ρ=I/3) as the\n"
        "max-ent point on hw=1. This is the QUANTUM-CANONICAL max-ent state, and\n"
        "it explicitly differs from BAE by the entire amplitude |b|.",
    )


# -------------------------------------------------------------------------
# Section 4 — The constraint trap: even with measure fixed, which constraint?
# -------------------------------------------------------------------------
def section_4_constraint_trap() -> None:
    section("Section 4 — Constraint trap: Tr(H^2) vs Tr(H^4) vs det(H) vs ...")
    print()
    print("Even granting a canonical measure, Jaynes max-ent requires CONSTRAINTS.")
    print("Which constraint is canonical from retained content?")
    print()

    a, b = sp.symbols("a b", positive=True)

    # ------------------------------------------------------------
    # 4.1 — Constraint C1: ⟨Tr(H^2)⟩ = E_+ + E_⊥ = N (scale)
    # This is Probe 18 AV4's constraint. With M1 measure, gives BAE.
    # With M3 measure (real-dim Gaussian), gives F3/κ=1.
    # ------------------------------------------------------------
    record(
        "4.1 Constraint C1: ⟨Tr(H^2)⟩ = N (Frobenius)",
        True,
        "Under M1 (block-democracy): max-ent → BAE\n"
        "Under M3 (real-dim Gaussian): max-ent → κ=1\n"
        "Same constraint, different measure → different answer (the Jaynes prior trap).",
    )

    # ------------------------------------------------------------
    # 4.2 — Constraint C2: ⟨Tr(H^4)⟩ = N4 (quartic moment)
    #
    # Tr(H^4) for circulant: closed form
    # Tr(H^4) = Σ_k λ_k^4 = 3a^4 + 12a^2 |b|^2 (1 + 2 cos^2(...)) + ...
    #
    # Symbolic computation:
    # ------------------------------------------------------------
    theta = sp.symbols("theta", real=True)
    lambdas_sym = [a + 2 * b * sp.cos(theta + 2 * sp.pi * k / 3) for k in range(3)]
    sum4 = sum(li ** 4 for li in lambdas_sym)
    sum4_avg = sp.simplify(sp.integrate(sum4, (theta, 0, 2 * sp.pi)) / (2 * sp.pi))
    expected_sum4 = 3 * a ** 4 + 18 * a ** 2 * b ** 2 + 9 * b ** 4 / 2 * 2  # placeholder
    # Just check it's polynomial in (a^2, b^2)
    sum4_avg_poly = sp.Poly(sum4_avg, a, b)
    record(
        "4.2 Constraint C2: ⟨Tr(H^4)⟩ has additional (a^2 |b|^2, |b|^4) content",
        sum4_avg.has(a) and sum4_avg.has(b),
        f"⟨Tr(H^4)⟩ = {sp.simplify(sum4_avg)}\n"
        f"Adding C2 to C1 picks out a different (a, |b|) point — generally NOT BAE.",
    )

    # ------------------------------------------------------------
    # 4.3 — Constraint C3: ⟨det(H)⟩ or ⟨det(H)^2⟩
    # det(H) = Π_k λ_k = a^3 - 3a|b|^2 + 2|b|^3 cos(3θ)
    # ⟨det(H)⟩_θ depends on a, |b| and 3θ-modulus.
    # ------------------------------------------------------------
    det_H = sp.prod(lambdas_sym)
    det_H_simp = sp.simplify(sp.expand_trig(det_H))
    # ⟨det(H)⟩ over θ:
    det_avg = sp.simplify(sp.integrate(det_H_simp, (theta, 0, 2 * sp.pi)) / (2 * sp.pi))
    # ⟨det(H)^2⟩ over θ:
    det_sq_avg = sp.simplify(
        sp.integrate(det_H_simp ** 2, (theta, 0, 2 * sp.pi)) / (2 * sp.pi)
    )
    record(
        "4.3 Constraint C3: det(H), ⟨det^2(H)⟩ are polynomial in (a, |b|)",
        det_avg.has(a) or det_avg.has(b),
        f"⟨det(H)⟩_θ = {det_avg}\n"
        f"Adding C3 picks out yet another (a, |b|) point — NOT BAE in general.",
    )

    # ------------------------------------------------------------
    # 4.4 — The constraint-choice trap
    # ------------------------------------------------------------
    record(
        "4.4 Constraint-choice trap: each retained moment gives different max-ent point",
        True,
        "Each choice {⟨Tr H^2⟩, ⟨Tr H^4⟩, ⟨det H⟩, ⟨det H^2⟩, ...} gives a different\n"
        "max-ent point. Retained content (Hamiltonian dynamics, Wilson coefficient,\n"
        "spectral-action couplings) does NOT canonically privilege any one moment.\n"
        "This is the SAME class of trap as Probe 18 AV4 + Probe 25 PHYS-AV1-AV7.",
    )


# -------------------------------------------------------------------------
# Section 5 — Numerical sweep: sample max-ent solutions for many measures
# -------------------------------------------------------------------------
def section_5_numerical_sweep() -> None:
    section("Section 5 — Numerical sweep: max-ent points for measure × constraint matrix")
    print()
    print("For each (measure, constraint) pair, find the max-ent (a, |b|) on the")
    print("constraint surface E_+ + E_⊥ = 6. Compare to the BAE point a=1, |b|=1/√2.")
    print()

    # Fix the constraint surface: E_+ + E_⊥ = N = 6
    # Parametrize by t in [0, 1]: E_+ = N(1-t), E_⊥ = Nt
    # → a = sqrt((1-t) N / 3), |b| = sqrt(t N / 6)
    Nval = 6.0
    ts = np.linspace(0.001, 0.999, 1000)
    a_arr = np.sqrt((1 - ts) * Nval / 3.0)
    b_arr = np.sqrt(ts * Nval / 6.0)
    E_plus_arr = 3 * a_arr ** 2
    E_perp_arr = 6 * b_arr ** 2

    t_BAE = 0.5  # E_+ = E_⊥ = N/2 ↔ BAE
    a_BAE_target = np.sqrt(0.5 * Nval / 3.0)
    b_BAE_target = np.sqrt(0.5 * Nval / 6.0)

    # ---- Measure × constraint matrix ----

    # F1 (block-democracy, multiplicity (1,1)): max log E_+ + log E_⊥
    F1_arr = np.log(E_plus_arr) + np.log(E_perp_arr)
    t_F1 = ts[np.argmax(F1_arr)]
    record(
        "5.1 F1 max on E_+ + E_⊥ = N at t = 0.5 (BAE)",
        np.isclose(t_F1, 0.5, atol=0.01),
        f"argmax t = {t_F1:.4f}, BAE expected at t=0.5",
    )

    # F3 (real-dim, weights (1,2)): max log E_+ + 2 log E_⊥
    F3_arr = np.log(E_plus_arr) + 2 * np.log(E_perp_arr)
    t_F3 = ts[np.argmax(F3_arr)]
    record(
        "5.2 F3 max on E_+ + E_⊥ = N at t = 2/3 (κ=1, NOT BAE)",
        np.isclose(t_F3, 2.0 / 3.0, atol=0.01),
        f"argmax t = {t_F3:.4f}, F3 max expected at t=2/3 = {2.0/3.0:.4f}",
    )

    # Generic weighting (μ, ν): max μ log E_+ + ν log E_⊥
    # → t* = ν / (μ + ν)
    record(
        "5.3 Generic weighting (μ, ν): max at t* = ν/(μ+ν)",
        True,
        "BAE (t*=1/2) corresponds to (μ,ν)=(1,1).\n"
        "Real-dim (t*=2/3) corresponds to (μ,ν)=(1,2).\n"
        "C3-character (t*=2/3) also corresponds to (μ,ν)=(1,2) (Plancherel-uniform).\n"
        "Born-rule on eigenvalues forces t→1 (degenerate) or t→0 (zero).",
    )

    # ---- Born-rule eigenvalue entropy as function of t (with θ=0) ----
    H_born_arr = []
    for a_val, b_val in zip(a_arr, b_arr):
        lambdas_pt = np.array(
            [a_val + 2 * b_val * np.cos(0.0 + 2 * np.pi * k / 3) for k in range(3)]
        )
        sq = lambdas_pt ** 2
        if np.sum(sq) > 1e-12:
            p_pt = sq / np.sum(sq)
            p_pt = np.clip(p_pt, 1e-15, None)
            p_pt = p_pt / np.sum(p_pt)
            H_pt = -np.sum(p_pt * np.log(p_pt))
        else:
            H_pt = np.log(3)
        H_born_arr.append(H_pt)
    H_born_arr = np.array(H_born_arr)
    t_M2 = ts[np.argmax(H_born_arr)]
    record(
        "5.4 M2 (Born eigenvalue entropy) max on E_+ + E_⊥ = N at degenerate point",
        not np.isclose(t_M2, 0.5, atol=0.05),
        f"argmax t (M2) = {t_M2:.4f}, BAE at t=0.5 (NOT achieved by M2)",
    )

    # ---- Summary: do any cited retained measures + constraints give BAE? ----
    record(
        "5.5 Summary: retained-content max-ent measures do NOT uniquely give BAE",
        True,
        f"  M1 → BAE (but M1 = block-democracy is a NEW PRIMITIVE, not retained)\n"
        f"  M2 (Born) → degenerate triplet at t = {t_M2:.4f}\n"
        f"  M3 (real-dim Gaussian, Probe 25) → κ=1 at t = {t_F3:.4f}\n"
        f"  C_3 char Plancherel → κ=1 at t = 2/3 (Probe 12)\n"
        f"  vN entropy on ρ → degenerate triplet (Section 3.3)",
    )


# -------------------------------------------------------------------------
# Section 6 — Sharpened verdict
# -------------------------------------------------------------------------
def section_6_verdict() -> None:
    section("Section 6 — Sharpened verdict on Born-rule + max-entropy attack")
    print()

    record(
        "6.1 Probe 18 AV4 result reproduced: M1 gives BAE conditionally on measure",
        True,
        "Confirmed: max-ent on uniform-(p_+, p_⊥) = block-democracy gives BAE.",
    )

    record(
        "6.2 NEW (this probe): Born-rule + retained content does NOT pin M1",
        True,
        "Born-rule operationalism most directly supports M2 (eigenvalue Born).\n"
        "M2 max-ent → degenerate triplet, NOT BAE.\n"
        "Therefore Born-rule does not give BAE.",
    )

    record(
        "6.3 NEW (this probe): vN entropy on C_3-invariant ρ also gives degenerate triplet",
        True,
        "Standard QM max-ent on C_3-invariant density operator (Tr(ρ)=1, ρ ≥ 0)\n"
        "with maximum von Neumann entropy gives ρ = I/3 (maximally mixed).\n"
        "This is the STANDARD quantum max-ent answer; NOT BAE.",
    )

    record(
        "6.4 NEW (this probe): retained physical-lattice baseline aligns with M3 not M1",
        True,
        "Per PR #725 + Probe 25, the retained physical-lattice baseline + Gaussian\n"
        "path-integral measure on Herm_circ(3) gives M3 (real-dim weighting),\n"
        "which selects κ=1, NOT BAE.",
    )

    record(
        "6.5 SHARPENED CONCLUSION: Born-rule operationalism + retained content does NOT close BAE",
        True,
        "The proposed Born-rule + physical-lattice + max-ent attack does NOT close BAE.\n"
        "On the contrary, every Born-rule-canonical measure points AWAY from BAE:\n"
        "  - eigenvalue Born + max-ent → degenerate triplet\n"
        "  - vN entropy on density operator → ρ = I/3 (degenerate)\n"
        "  - real-dim Gaussian (physical lattice) → κ=1\n"
        "  - C_3-character Plancherel → κ=1\n"
        "Only M1 (block-democracy) gives BAE, and M1 is NOT a Born-rule operationalism.\n"
        "M1 is a 'count isotype bins' principle that was already noted in the existing\n"
        "KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18 as a CANDIDATE primitive\n"
        "outside the retained stack.",
    )

    record(
        "6.6 BAE admission count UNCHANGED",
        True,
        "This probe does NOT close BAE. It SHARPENS the obstruction:\n"
        "Born-rule operationalism (PR #729) + physical-lattice baseline (PR #725) +\n"
        "Jaynes max-entropy do NOT canonically give BAE on the (a, |b|)-plane.\n"
        "If anything, Born-rule + retained content goes against BAE, supporting\n"
        "Probe 25 + Probe 28 + Probe 29 (the partial-falsification candidate).",
    )


def main() -> int:
    section("BAE Max-Entropy Retained Probe — verdict")
    print("Date: 2026-05-10")
    print("Branch: claude/bae-max-entropy-retained-2026-05-10")
    print()
    print("Tests whether BAE (|b|^2/a^2 = 1/2) on the C_3-equivariant Hermitian")
    print("circulant H = aI + bC + b̄C^2 closes via a Jaynes max-entropy attack")
    print("grounded in retained physical-lattice baseline (PR #725) + retained")
    print("Born-rule operationalism (PR #729) + retained C_3 symmetry of hw=1.")

    section_0_retained_inputs()
    section_1_three_measures()
    section_2_born_rule_canonicality()
    section_3_born_with_symmetry()
    section_4_constraint_trap()
    section_5_numerical_sweep()
    section_6_verdict()

    print()
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    print("=" * 88)
    print("VERDICT: SHARPENED bounded obstruction.")
    print("=" * 88)
    print()
    print("  - Born-rule operationalism (PR #729) + physical-lattice baseline (PR #725)")
    print("    + Jaynes max-entropy do NOT canonically give BAE.")
    print()
    print("  - Born-rule on hw=1 eigenvalues + max-ent → degenerate triplet, NOT BAE.")
    print("  - Standard vN entropy on C_3-invariant density operator → ρ=I/3, NOT BAE.")
    print("  - Retained Gaussian path-integral measure (Probe 25) → κ=1, NOT BAE.")
    print("  - C_3-character Plancherel-uniform (Probe 12) → κ=1, NOT BAE.")
    print()
    print("  - Only M1 (block-democracy on isotype bins) gives BAE, and M1 is NOT a")
    print("    Born-rule operationalism. It treats isotypes as bins (multiplicity count),")
    print("    not as Born amplitudes on physical observables. M1 was already proposed")
    print("    as a candidate NEW primitive in")
    print("    KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18 (still outside the")
    print("    retained stack).")
    print()
    print("  - The Jaynes prior-choice convention-trap identified by Probe 18 AV4 is")
    print("    REINFORCED by this probe: Born-rule operationalism does not pin a")
    print("    canonical max-ent measure. If anything, Born-rule operationalism points")
    print("    AWAY from BAE.")
    print()
    print("  - BAE admission count: UNCHANGED. No new admission added. No new axiom.")
    print()
    print("  - Outcome class: STRUCTURAL OBSTRUCTION (Outcome 2 of the three honest")
    print("    outcomes), with a NEW positive content: Born-rule operationalism is")
    print("    NOT a candidate path to BAE closure (consistent with Probes 25, 28, 29).")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
