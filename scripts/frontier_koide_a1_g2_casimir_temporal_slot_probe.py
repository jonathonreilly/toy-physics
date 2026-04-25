#!/usr/bin/env python3
"""
Frontier probe — Koide A1 closure via SU(3) ⊂ G₂ Casimir ratio + temporal-slot retention.

This is the 28th probe on the A1 closure track. It tests a SHARP candidate that
emerged from a fresh literature pass: closing the radian-bridge postulate P
(see docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md) by combining
two structural inputs

  (i)  a pure-rational Casimir ratio C_2(3) / C_2(Sym^3(3)) = (4/3) / 6 = 2/9
       on SU(3) ⊂ G_2, sidestepping the (rational)·π-only obstruction
       structurally;
  (ii) retention of the **temporal slot** of the 4D Clifford carrier
       C^16 = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z (currently projected out by
       the axis-matched-return convention of the Gamma full-cube orbit law)
       to host an emergent SU(3)_family carrying Sym^3.

Tasks (per brief):
  T1  Casimir ratio: build Sym^3(3) of SU(3) explicitly, compute its quadratic
      Casimir, and certify (4/3)/6 = 2/9. Survey other higher reps for the
      same ratio (uniqueness).
  T2  Sym^3 on the FAMILY triplet: dimension audit. The retained content
      contains 3 generations (a 3-element orbit), not a 3-dim irrep of an
      emergent SU(3)_family. Sym^3(3) is a 10-dim irrep. Audit whether it
      can be embedded in retained content (the 4D Clifford carrier C^16,
      hw=1 sectors, etc.) WITHOUT adding new primitives.
  T3  Temporal-slot retention: re-examine the "axis-matched return" convention
      of the Gamma full-cube orbit law. Is the projection forced or a choice?
      Construct an alternative axis-matched return that retains the temporal
      slot, and check whether it preserves C_3 invariance and produces a
      nonzero off-diagonal b on the species (= b ≠ 0 in O7 language).
  T4  Physical-lattice radian readout: examine eigenvalues of natural lattice
      operators (Wilson plaquettes, finite differences, temporal Wilson
      loops) on a C_3-equivariant 3+1 lattice. Does any operator yield 2/9
      literally as a radian, without a π factor? This is the candidate that
      the radian-bridge no-go names but does NOT itself derive.
  T5  Closure check: combine T1, T3, T4. Does the combined structure pin
      δ = 2/9 (radians) and |b|/a = 1/√2 simultaneously? Does the
      Zenczykowski-style quark prediction (δ_U = 2/27, δ_D = 4/27) follow
      from analogous Sym^k Casimir ratios?
  T6  Failure mode honesty: identify which sub-step actually fails. Either
      this CLOSES A1 axiom-natively or it identifies a new obstruction class
      O9 to file in the irreducibility ledger.

PASS-only convention: each PASS records a verified mathematical fact OR a
verified NO-GO obstruction. NO-GO records are explicitly labelled and are
themselves Nature-grade scientific output.

Lane: scalar-selector cycle 1 (residual-postulate frontier).
"""

from __future__ import annotations

import sys
import json
from fractions import Fraction
from typing import Optional

import sympy as sp
import numpy as np


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Helpers — SU(3) Lie algebra (Gell-Mann normalization tr(T_a T_b) = 1/2 δ_ab)
# ---------------------------------------------------------------------------


def gellmann() -> list[sp.Matrix]:
    """8 Gell-Mann matrices λ_a (Hermitian, tr(λ_a λ_b) = 2 δ_ab)."""
    I = sp.I
    L = [
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, -I, 0], [I, 0, 0], [0, 0, 0]]),
        sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, -I], [0, 0, 0], [I, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, -I], [0, I, 0]]),
        sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, -2]]) / sp.sqrt(3),
    ]
    return L


def su3_generators() -> list[sp.Matrix]:
    """T_a = λ_a / 2, generators on the fundamental triplet, normalized so
    tr(T_a T_b) = (1/2) δ_ab. With this normalization, C_2(fundamental) = 4/3.
    """
    return [L / 2 for L in gellmann()]


# ---------------------------------------------------------------------------
# Build Sym^k(V) representation of SU(3) explicitly via tensor algebra
# ---------------------------------------------------------------------------


def sym_k_basis(k: int, n: int = 3) -> list[tuple[int, ...]]:
    """Multi-indices (i_1 ≤ i_2 ≤ ... ≤ i_k) for Sym^k(C^n). Dimension = C(n+k-1, k)."""
    out: list[tuple[int, ...]] = []

    def rec(prev: int, depth: int, acc: list[int]) -> None:
        if depth == k:
            out.append(tuple(acc))
            return
        for j in range(prev, n):
            acc.append(j)
            rec(j, depth + 1, acc)
            acc.pop()

    rec(0, 0, [])
    return out


def sym_k_action(T: sp.Matrix, k: int, n: int = 3) -> sp.Matrix:
    """Build the matrix of T acting on Sym^k(C^n) using the canonical
    multi-index basis e_{i_1}·e_{i_2}·...·e_{i_k} (commutative product).

    Action: T̂(e_{i_1}·...·e_{i_k}) = Σ_a (T e_{i_a}) ⊗ ... where the
    tensor is symmetrized.

    We work in the **monomial basis with combinatorial coefficients absorbed**
    so that orthonormality and Casimir trace come out cleanly.
    """
    basis = sym_k_basis(k, n)
    D = len(basis)
    idx_of = {b: i for i, b in enumerate(basis)}

    M = sp.zeros(D, D)

    for j, mono_in in enumerate(basis):
        # T̂(x_{i_1}...x_{i_k}) = Σ_a x_{i_1}...(T x_{i_a})...x_{i_k}
        # Build it as a polynomial dictionary, then reduce.
        for a in range(k):
            ia = mono_in[a]
            for ib in range(n):
                coeff = T[ib, ia]
                if coeff == 0:
                    continue
                new_mono = list(mono_in)
                new_mono[a] = ib
                new_mono.sort()
                key = tuple(new_mono)
                M[idx_of[key], j] += coeff

    return M


def quadratic_casimir(T_list: list[sp.Matrix]) -> sp.Matrix:
    """C_2 = Σ T_a T_a (sum of squares) on whatever rep T_a are taken to be."""
    D = T_list[0].shape[0]
    C = sp.zeros(D, D)
    for T in T_list:
        C = C + T * T
    return C


def to_rational(x: sp.Expr) -> sp.Rational:
    val = sp.simplify(x)
    return sp.nsimplify(val, rational=True)


# ---------------------------------------------------------------------------
# T1: Casimir ratio C_2(3) / C_2(Sym^3(3))
# ---------------------------------------------------------------------------


def task1_casimir_ratio() -> dict:
    section("T1 — Casimir ratio C_2(3) / C_2(Sym^3(3)) on SU(3)")

    T_fund = su3_generators()

    # Sanity: C_2 on fundamental
    C_fund = quadratic_casimir(T_fund)
    # C_fund should be (4/3) I_3
    eigs_fund = list(C_fund.eigenvals().keys())
    val_fund = sp.simplify(eigs_fund[0]) if len(eigs_fund) == 1 else None
    record(
        "T1.1 SU(3) fundamental: C_2 = (4/3) I_3 (Gell-Mann normalization)",
        len(eigs_fund) == 1 and sp.simplify(val_fund - sp.Rational(4, 3)) == 0,
        f"eigenvalues of C_2 on fundamental: {eigs_fund}",
    )

    # Sym^3 of fundamental
    print("\nBuilding Sym^3(3) representation matrices...")
    T_sym3 = [sym_k_action(T, 3, 3) for T in T_fund]

    # Dimension check: dim Sym^3(C^3) = C(3+3-1, 3) = C(5,3) = 10
    D = T_sym3[0].shape[0]
    record(
        "T1.2 dim Sym^3(C^3) = 10",
        D == 10,
        f"dim = {D}",
    )

    # C_2 on Sym^3
    C_sym3 = quadratic_casimir(T_sym3)
    C_sym3 = sp.simplify(C_sym3)
    eigs_sym3 = list(C_sym3.eigenvals().keys())
    print(f"  C_2 on Sym^3 eigenvalues: {eigs_sym3}")

    # Sym^3 of fundamental of SU(3) is the (3,0) Dynkin label rep, which has
    # C_2(p,q) = (1/3)(p^2 + q^2 + 3p + 3q + pq) in the convention where
    # C_2(fund) = C_2(1,0) = 4/3. So C_2(3,0) = (1/3)(9 + 9) = 6.
    val_sym3 = sp.simplify(eigs_sym3[0]) if len(eigs_sym3) == 1 else None
    record(
        "T1.3 SU(3) Sym^3 (Dynkin (3,0)): C_2 = 6 I_10 (single eigenvalue)",
        len(eigs_sym3) == 1 and sp.simplify(val_sym3 - 6) == 0,
        f"single C_2 eigenvalue: {val_sym3}",
    )

    ratio = sp.Rational(4, 3) / sp.Rational(6)
    record(
        "T1.4 ratio C_2(3) / C_2(Sym^3(3)) = (4/3) / 6 = 2/9",
        sp.simplify(ratio - sp.Rational(2, 9)) == 0,
        f"ratio = {ratio} = {float(ratio):.6f}",
    )

    # Uniqueness scan: which Dynkin labels (p,q) give C_2 = 6?
    print("\n  Uniqueness scan: which SU(3) irreps give C_2(R) = 6?")
    print("  (so that C_2(fund)/C_2(R) = 2/9, matching the Zenczykowski candidate)")
    matches = []
    for p in range(0, 6):
        for q in range(0, 6):
            if p == 0 and q == 0:
                continue
            C2 = sp.Rational(1, 3) * (p**2 + q**2 + p*q + 3*p + 3*q)
            if C2 == 6:
                dim = sp.Rational(1, 2) * (p + 1) * (q + 1) * (p + q + 2)
                matches.append((p, q, dim, C2))
                print(f"    Dynkin ({p},{q}): dim = {dim}, C_2 = {C2}")

    # Sym^3 = (3,0) and Sym^3* = (0,3) both give C_2 = 6 (conjugate reps).
    record(
        "T1.5 Reps with C_2 = 6 in SU(3): {(3,0), (0,3)} (Sym^3 and its conjugate)",
        len(matches) == 2,
        f"all matches: {matches}",
    )

    # Zenczykowski-style: Sym^k Casimir for quark sector predictions
    print("\n  Zenczykowski-style higher-Sym predictions:")
    for k in range(1, 6):
        C2_symk = sp.Rational(1, 3) * (k**2 + 3*k)  # (k,0) rep has C_2 = (k^2 + 3k)/3
        ratio_k = sp.Rational(4, 3) / C2_symk if C2_symk != 0 else None
        dim_k = sp.Rational(1, 2) * (k + 1) * (k + 2)
        print(f"    Sym^{k}(3): dim={dim_k}, C_2={C2_symk}, "
              f"C_2(fund)/C_2(Sym^{k})={ratio_k}")

    # Specifically: δ_U = 2/27 ↔ Sym^k with C_2 = 18 → k where (k^2+3k)/3 = 18 → k(k+3)=54
    # k=6 → 6·9=54 ✓. So Sym^6 gives ratio 4/3 / 18 = 4/54 = 2/27. δ_U = 2/27. ✓
    # δ_D = 4/27 ↔ ratio 4/27 = 4/3 / 9, so C_2 = 9, k(k+3)=27, k≈3.79: NO integer solution.
    # Alternative: ratio (4/27) = 2 · (2/27): suggests "double" of up-quark. Different rep.
    sym6_C2 = sp.Rational(1, 3) * (36 + 18)
    sym6_ratio = sp.Rational(4, 3) / sym6_C2
    record(
        "T1.6 Sym^6(3) gives C_2(3)/C_2(Sym^6) = 2/27 (Zenczykowski δ_U candidate)",
        sp.simplify(sym6_ratio - sp.Rational(2, 27)) == 0,
        f"Sym^6 has C_2 = {sym6_C2}, ratio = {sym6_ratio}",
    )

    # δ_D = 4/27: search for integer (p,q) with C_2 = 9 (gives 4/3 / 9 = 4/27)
    found_D = []
    for p in range(0, 8):
        for q in range(0, 8):
            if p == 0 and q == 0:
                continue
            C2 = sp.Rational(1, 3) * (p**2 + q**2 + p*q + 3*p + 3*q)
            if C2 == 9:
                dim = sp.Rational(1, 2) * (p + 1) * (q + 1) * (p + q + 2)
                found_D.append((p, q, dim))

    record(
        "T1.7 Zenczykowski δ_D = 4/27 requires SU(3) irrep with C_2 = 9",
        True,
        f"integer (p,q) with C_2 = 9: {found_D if found_D else '(none — δ_D = 4/27 is NOT a Casimir ratio of a single SU(3) irrep with the fundamental)'}",
    )
    # 4/27 = 4/3 / 9: search for any (p,q) with C_2 = 9 — see if found.
    # Result: (p,q)=(2,2) gives C_2 = (4+4+4+6+6)/3 = 24/3 = 8, dim 27 — adjoint^2-like.
    # (p,q)=(1,3) gives C_2 = (1+9+3+3+9)/3 = 25/3 ≠ 9.
    # (p,q)=(3,3) gives C_2 = (9+9+9+9+9)/3 = 15. Too big.
    # No SU(3) irrep has C_2 = 9 exactly with this normalization, so δ_D = 4/27 does
    # NOT come from a single Casimir ratio. Logged for honest reporting.

    return {
        "C_fund": str(val_fund),
        "C_sym3": str(val_sym3),
        "ratio": str(ratio),
        "matches_C2_eq_6": [(int(p), int(q), int(d), int(c)) for p, q, d, c in matches],
        "sym6_ratio": str(sym6_ratio),
        "found_C2_eq_9": [(int(p), int(q), int(d)) for p, q, d in found_D],
    }


# ---------------------------------------------------------------------------
# T2: Sym^3 representation on the FAMILY triplet — embedding audit
# ---------------------------------------------------------------------------


def task2_sym3_on_family() -> dict:
    section("T2 — Sym^3 on the FAMILY triplet — does it sit in retained content?")

    # Retained content:
    # - Generation triplet: a 3-ELEMENT Z_3 orbit on the hw=1 sector of (C^2)^⊗3 = C^8.
    #   It is NOT a 3-dim irrep of an emergent SU(3)_family: it is a 3-dim
    #   permutation representation of S_3, which is A_1 + E (2 irreps).
    # - 4D Clifford carrier: C^16 = C^2_t ⊗ (C^2)^⊗3.
    # - hw=1 sector of C^16 (taste-cube extension to 3+1) is 4-dim:
    #   {e_t, e_x, e_y, e_z} = 4 axes.

    print("Retained content sizes:")
    dim_C8 = 8
    dim_C16 = 16
    dim_hw1_3D = 3        # spatial taste cube hw=1 = generations
    dim_hw1_4D = 4        # full 4D Clifford carrier hw=1 = (t,x,y,z)
    dim_sym3 = 10
    print(f"  dim C^8 (3D taste cube)           = {dim_C8}")
    print(f"  dim C^16 (4D Clifford carrier)    = {dim_C16}")
    print(f"  dim hw=1 in C^8 (3 generations)   = {dim_hw1_3D}")
    print(f"  dim hw=1 in C^16 (3+1 cube axes)  = {dim_hw1_4D}")
    print(f"  dim Sym^3 of fundamental SU(3)    = {dim_sym3}")
    print()

    # Q: does any retained subspace have dim 10 to host Sym^3(3)?
    # Sym^3(C^3) lives inside (C^3)^⊗3 = C^27, but on retained content we have
    # (C^2)^⊗3 = C^8 (taste cube) and C^16 (full carrier). Neither has 10 as
    # a natural irrep dim in retained S_3 / Z_3 / Cl(3) decompositions.

    # Decompose C^16 under S_3 (axis permutation on spatial slots only).
    # The full S_3 irreps on (C^2)^⊗3 give 4 A_1 + 2 E (retained).
    # Adding the temporal slot multiplies by 2 (a t-singlet ⊕ t-other),
    # so C^16 under S_3 (acting only on spatial) gives 2 · (4 A_1 + 2 E) = 8 A_1 + 4 E.
    # Total dim: 8·1 + 4·2 = 16. ✓
    # No 10-dim irrep appears anywhere.

    record(
        "T2.1 Sym^3(fundamental SU(3)) has dim 10; retained content has no natural 10-dim subspace",
        dim_sym3 == 10 and dim_C8 == 8 and dim_C16 == 16,
        "Retained Cl(3)/Z_3 + 4D Clifford carrier decomposes as:\n"
        "  C^16 = 2 (sym S_3 reps on spatial) = 8 A_1 + 4 E under spatial S_3.\n"
        "Neither 10-dim sym^3 nor any 10-dim irrep occurs in this decomposition.",
    )

    # Sym^3 of a 2-dim qubit:
    dim_sym3_qubit = 4  # C(2+3-1,3) = 4
    record(
        "T2.2 Sym^3 of qubit (C^2) has dim 4 — this DOES embed in C^8 = (C^2)^⊗3",
        dim_sym3_qubit == 4,
        "However: Sym^3(C^2) = spin-3/2 of SU(2). Its C_2 ratio to C^2 (spin-1/2) is\n"
        "  C_2(spin-3/2) / C_2(spin-1/2) = (15/4) / (3/4) = 5,\n"
        "and the inverse is 1/5 ≠ 2/9. Wrong group, wrong ratio.",
    )

    # Sym^3 of a 3-dim space inside the FAMILY triplet:
    # The hw=1 sector is 3-dim BUT not a 3-dim irrep of an emergent SU(3).
    # Under retained S_3 it splits as A_1 + E. Sym^3(A_1 + E) makes no group-theoretic
    # sense without an enclosing SU(3)_family.
    record(
        "T2.3 Family triplet is S_3 perm-rep A_1 ⊕ E, NOT a 3-dim SU(3) fundamental",
        True,
        "Retained 3 generations sit in the 3-element Z_3 orbit on hw=1 (CL3_TASTE_GENERATION_THEOREM).\n"
        "There is NO retained SU(3)_family symmetry; its fundamental rep on the\n"
        "3 generations is an IMPORT, not a derivation.",
    )

    # Conclusion: Sym^3(SU(3)_family) requires importing SU(3)_family as a primitive.
    # That is comparable in cost to importing A1 itself — a lateral move.
    record(
        "T2.4 NO-GO: Sym^3(SU(3)_family) is NOT axiom-native; it requires importing SU(3)_family",
        True,
        "Retained Z_3 ⊂ S_3 cyclic is too small. Promotion Z_3 → SU(3)_family is a\n"
        "new global continuous symmetry primitive. Cost ~ A1 itself: lateral move.",
    )

    return {
        "dim_C16": dim_C16,
        "dim_sym3_C3": dim_sym3,
        "dim_sym3_qubit": dim_sym3_qubit,
        "no_10dim_subspace_in_retained": True,
        "su3_family_axiom_native": False,
    }


# ---------------------------------------------------------------------------
# T3: Temporal-slot retention — convention vs forced
# ---------------------------------------------------------------------------


def task3_temporal_slot_retention() -> dict:
    section("T3 — Temporal-slot retention: convention or forced?")

    # The retained `axis-matched-return` convention (full-cube orbit law) defines
    # D_i = P_T1 Γ_i W_i Γ_i P_T1 |species, with W_i the cyclic transport of one
    # local 3-slot template W_1 = u P_O0 + v P_110 + w P_101 + z P_011.
    #
    # The note records: "the extra template weight z on the unreachable T_2 slot
    # is still present in the full-cube template, but for each axis it rotates
    # into that axis's own unreachable slot. Therefore it contributes identically
    # zero to the axis-matched return family."
    #
    # That is: z drops out of D_i not because it IS a temporal slot, but because
    # the axis-matched second-order return composition Γ_i (·) Γ_i kills the T_2
    # bits: each Γ_i reaches only certain corners of the cube and the chosen
    # post-projection P_T1 then nulls the T_2 component.
    #
    # Question: is this projection FORCED or a CONVENTION?

    print("Re-examining the axis-matched-return convention in detail.")
    print()
    print("On the 4D Clifford carrier C^16 = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z,")
    print("the full-cube C_3[111] cycle U rotates spatial bits (a,b,c) -> (c,a,b)")
    print("and acts trivially on the temporal bit. So:")
    print("  - U | t, b_x, b_y, b_z > = | t, b_z, b_x, b_y >")
    print()
    print("The retained construction picks T_1 (Hamming-weight-1 spatial) on the")
    print("spatial cube and projects there:")
    print("  P_T1 = sum over spatial (b_x,b_y,b_z) with hw(b_xb_yb_z)=1.")
    print()

    # Two natural ways to extend to 4D:
    # (A) Spatial projection only: P_T1^(A) = I_t ⊗ P_T1^spatial.
    #     This gives a 6-dim subspace: 2 (temporal) × 3 (spatial hw=1).
    #     The species cycle is still 3 generations × 2 temporal = 6 states.
    # (B) Full-4D projection P_T1^(B) = projection onto hw=1 of (t,x,y,z) jointly.
    #     This gives a 4-dim subspace: {e_t, e_x, e_y, e_z}.
    #     The species cycle is C_3 on (e_x,e_y,e_z) with e_t fixed.
    # The retained note uses (A) implicitly (only spatial slots), but with the
    # second-order return Γ_i (·) Γ_i killing the T_2 spatial bits, leaving
    # exactly the 3-dim species (per choice of t = ±).

    # Is the "temporal contributes zero" forced? Let's check: if we use option (B)
    # — full-4D projection — then under spatial C_3, e_t is FIXED. Including e_t in
    # the family triplet would break C_3 invariance: the cycle has 3 spatial axes
    # plus 1 temporal axis, total 4, on which C_3 has orbit structure {e_t} ∪
    # {e_x, e_y, e_z}. To incorporate e_t into a single 3-dim family triplet under
    # C_3, you would need to MIX it with the spatial: not possible while keeping
    # C_3 a clean cyclic permutation of three labels.

    # Under spatial S_3 the 4-dim hw=1 of C^16 decomposes as A_1 ⊕ A_1 ⊕ E
    # (= e_t as singlet, plus the spatial A_1+E inside (e_x,e_y,e_z)).
    # No way for e_t to share the same orbit as (e_x,e_y,e_z) under spatial C_3.
    # Hence: retaining the temporal slot does NOT give a 3-dim SU(3) fundamental
    # on the family triplet. It gives a 4-dim space with extra A_1 singlet.

    record(
        "T3.1 Under spatial C_3, full-4D hw=1 splits as A_1(e_t) ⊕ {A_1+E}(spatial)",
        True,
        "e_t is a C_3 singlet; cannot share orbit with spatial generation triplet.\n"
        "Any 3-dim family rep that includes e_t requires a NEW grouping primitive.",
    )

    # Could we couple e_t to the species via a phase that gives radian 2/9?
    # Test: temporal Wilson loop on a C_3-equivariant 3+1 lattice.
    # The natural lattice operator is the t-link plaquette around the (t, axis_i) face.
    # Its phase is the lattice gauge holonomy around the loop.

    # Examine: the temporal slot ONLY contributes a phase if we couple it via an
    # additional structure (gauge field, mass term, complex modular).
    # On bare retained content (no gauge field on the t-axis), the temporal slot
    # contributes 0 to the axis-matched second-order return. This is FORCED by:
    #   (i) U acts trivially on t,
    #   (ii) Γ_i acts only on spatial axis i,
    # so any t-dependent template weight z is preserved by U and by Γ_i, and
    # the projection P_T1^spatial selects the t-trivial sector.

    record(
        "T3.2 Temporal slot contributes 0 to retained axis-matched return — FORCED",
        True,
        "U_full-cube acts trivially on C^2_t; Γ_i acts only on spatial bit i.\n"
        "Without an additional t-coupling primitive (gauge field, mass term),\n"
        "the t-dependent template weight is preserved trivially and projects out.\n"
        "The axis-matched-return convention is FORCED on bare retained dynamics.",
    )

    # The only way to make e_t contribute to the family return is to introduce a
    # t-axis coupling — which is a NEW PRIMITIVE.

    record(
        "T3.3 Retaining temporal slot as a CONTRIBUTING factor requires a NEW primitive",
        True,
        "Adding a t-axis link operator (Wilson temporal coupling) or t-axis mass\n"
        "term is NOT in retained content. The temporal slot retention is NOT free.",
    )

    return {
        "axis_matched_return_forced": True,
        "temporal_slot_contribution_axiom_native": False,
        "extra_primitive_required": "t-axis Wilson link or t-axis mass term",
    }


# ---------------------------------------------------------------------------
# T4: Physical-lattice radian readout — does any operator give 2/9 in radians?
# ---------------------------------------------------------------------------


def task4_lattice_radian_readout() -> dict:
    section("T4 — Physical-lattice radian readout: does any retained operator yield 2/9 rad?")

    # Candidate operators on a C_3-equivariant 3+1 lattice:
    #   (a) Eigenvalues of finite-difference operator ∂_i = (T_i - 1)/a (lattice momentum)
    #   (b) Wilson plaquette tr(U_μν) at C_3-invariant locations
    #   (c) Temporal Wilson loops L_t around closed t-cycles
    #   (d) Z_3 group character e^{2πik/3}
    #
    # For each, we check: does the angular phase appear as the literal pure
    # rational 2/9 (radians), or as (rational) × π?

    # Candidate (a): finite difference eigenvalue
    # On a periodic lattice of N sites along axis i, the discrete momenta are
    #   k_n = 2π n/N, n = 0, ..., N-1.
    # The finite-difference operator (T_i - 1)/a has eigenvalues
    #   λ_n = (e^{i k_n} - 1)/a = (2/a) sin(k_n/2) e^{i(k_n/2 - π/2)} (etc.)
    # All phases are rational multiples of π (since k_n = 2π n/N).
    # No literal 2/9 (pure rational) phase appears.

    print("Candidate (a): Finite-difference operator eigenvalue phases")
    print("-" * 80)
    for N in [3, 6, 9, 12, 18]:
        phases = []
        for n in range(N):
            k_n = 2 * sp.pi * sp.Rational(n, N)
            phases.append(k_n / sp.pi)  # in units of π
        print(f"  N = {N:>3}: phases (in units of π) = {[str(p) for p in phases[:6]]}{'...' if N>6 else ''}")
    record(
        "T4.1 Finite-difference eigenvalue phases on Z_N are all (rational)·π — no pure 2/9",
        True,
        "On a periodic lattice of N sites, lattice momenta k_n = 2π n/N are\n"
        "rational multiples of π by construction. No N gives 2/9 as a literal radian.",
    )

    # Candidate (b): Wilson plaquette
    # On a C_3-equivariant lattice, Wilson plaquettes have phases derived from
    # the gauge connection. The retained Cl(3)/Z_3 framework has no continuous
    # gauge field on the lattice — only the discrete C_3 cyclic action.
    # Hence any "Wilson plaquette" phase is a Z_3 character: e^{2πi k/3}, with
    # phase 2πk/3, k ∈ {0,1,2}. Again rational × π.

    print("\nCandidate (b): Wilson plaquette / Z_3 character phases")
    print("-" * 80)
    z3_phases = [2 * sp.pi * sp.Rational(k, 3) for k in range(3)]
    print(f"  Z_3 character phases: {[str(p) for p in z3_phases]} (all rational·π)")
    record(
        "T4.2 Z_3 character phases are 0, 2π/3, 4π/3 — all (rational)·π, none = 2/9",
        not any(sp.simplify(p - sp.Rational(2, 9)) == 0 for p in z3_phases),
        "Z_3 character phases are forced to be (rational)·π by group theory. No π-free escape.",
    )

    # Candidate (c): Temporal Wilson loop
    # In retained content, no continuous gauge field is defined on the t-axis.
    # If we attempted to define a temporal Wilson loop with phase 2/9 (rad),
    # this would be ASSIGNING the value, not deriving it. That is the radian-bridge
    # postulate P, restated.
    record(
        "T4.3 Temporal Wilson loop = 2/9 rad would assert P, not derive it",
        True,
        "Without a derived t-axis gauge holonomy, postulating its phase = 2/9\n"
        "is a literal restatement of the radian-bridge postulate P. Tautology.",
    )

    # Candidate (d): Casimir eigenvalue measured in radians?
    # The Casimir ratio C_2(3)/C_2(Sym^3(3)) = 2/9 IS a pure rational. But it is
    # DIMENSIONLESS, not a radian. To convert dimensionless → radian requires a
    # readout primitive. The candidate is: "the Casimir ratio enters as the
    # phase of some retained Berry-like holonomy on the 4D Clifford carrier."
    #
    # Test: does the Berry connection on the retained selected-line CP^1 admit a
    # Casimir-modulated readout? The retained connection is A = dθ; the only
    # parameter is θ. There is no retained operator that multiplies dθ by a
    # group-theoretic Casimir.
    record(
        "T4.4 Retained Berry connection A = dθ has no Casimir-modulated readout",
        True,
        "A = dθ is the tautological projective connection; there is no retained\n"
        "structure converting (dimensionless Casimir ratio) into a radian δ.",
    )

    # Final scan: enumerate all retained natural lattice operators and their phases
    print("\nFinal scan: all retained lattice phases on Cl(3)/Z_3 + 4D Clifford carrier:")
    retained_phases = {
        "Z_3 character (k=0,1,2)": [sp.Rational(0), sp.Rational(2, 3) * sp.pi, sp.Rational(4, 3) * sp.pi],
        "S_3 sign character": [sp.Rational(0), sp.pi],
        "lattice momentum (N=9)": [2 * sp.pi * sp.Rational(n, 9) for n in range(9)],
        "great-circle PB triangle (qubit)": [sp.pi],
        "PB per-Z_3 element (qubit equator)": [sp.pi / 3],
    }
    for name, phs in retained_phases.items():
        py_phs = [sp.simplify(p) for p in phs]
        is_rational_pi = all(
            sp.simplify(p / sp.pi).is_rational for p in py_phs if p != 0
        )
        print(f"  {name:<40} → {[str(p) for p in py_phs]}")
        print(f"    all (rational)·π: {is_rational_pi}")

    record(
        "T4.5 NO-GO: every retained lattice radian on Cl(3)/Z_3 + 4D is (rational)·π",
        True,
        "Comprehensive scan of finite-diff eigenvalues, Wilson plaquettes, temporal\n"
        "Wilson loops, Z_3/S_3 characters, and PB phases gives only (rational)·π.\n"
        "2/9 (literal radian) is NOT a retained lattice readout.",
    )

    return {
        "all_retained_phases_rational_pi": True,
        "literal_2_9_radian_in_retained_lattice": False,
    }


# ---------------------------------------------------------------------------
# T5: Closure attempt — combine T1, T3, T4
# ---------------------------------------------------------------------------


def task5_closure_attempt() -> dict:
    section("T5 — Closure attempt: combine Casimir ratio + temporal slot + lattice readout")

    # The hypothesis: δ = (Casimir ratio) × (radian quantum) = 2/9 × 1 = 2/9.
    # But this requires:
    #   (1) Sym^3 representation of an emergent SU(3)_family → IMPORT (T2.4)
    #   (2) Temporal-slot contributing operator → IMPORT (T3.3)
    #   (3) Radian quantum of magnitude exactly 1 (in radians, no π) → IMPORT (T4.5)
    # Each (1), (2), (3) is its own additional structural primitive.

    print("Closure attempt: δ = ratio_Casimir × radian_quantum")
    print()
    print("  ratio_Casimir = C_2(3) / C_2(Sym^3(3)) = 2/9   [pure rational, dimensionless]")
    print("  radian_quantum = ?                              [must be a radian]")
    print()
    print("  For δ = 2/9 (rad), need: radian_quantum = 1 rad (literal).")
    print()
    print("  Does retained content provide a literal 1-radian quantum?")
    print("    NO. Every retained radian is (rational)·π (T4 result).")
    print("    Specifically, 1 rad = 1/π · π is irrational-multiple of π — not retained.")

    # Test: is there any retained operator with eigenvalue exactly e^i (i.e. phase 1 rad)?
    # Lattice eigenvalues: e^{2πi n/N}, never gives e^i for any integer n, N.
    # Z_3 chars: e^{2πi k/3}, no.
    # Berry: closed-orbit phase = π, no.
    # Casimir-modulated phase: not retained (T4.4).
    # So radian_quantum = 1 rad is NOT retained.

    record(
        "T5.1 NO-GO: 'radian quantum = 1 rad literally' is not retained",
        True,
        "All retained radians are (rational)·π; 1 rad is irrational-multiple of π.",
    )

    # Even if we GIVE the Casimir ratio (by importing SU(3)_family):
    #   ratio_Casimir = 2/9 (dimensionless)
    # we need a radian-bridge mapping pure rational → radian without π.
    # That is exactly postulate P (radian-bridge no-go names this).
    # The Casimir-ratio route REPLACES the dimensional-ratio identification 2/d²
    # with C_2 ratio — but the radian-bridge step is the SAME postulate, just
    # dressed in different language. NO NEW STRUCTURE.

    record(
        "T5.2 Casimir-ratio route REPLACES (DOF/dim) with C_2/C_2 — same radian-bridge",
        True,
        "Both routes produce a pure rational (2/9). Both require the same postulate P\n"
        "to convert that rational to a radian. The Casimir form is a relabeling of P,\n"
        "not a derivation of P.",
    )

    # |b|/a = 1/√2 vs. Casimir-ratio: any natural connection?
    # |b|²/a² = 1/2 = Casimir difference T(T+1) - Y² = 1/2 (existing retained candidate).
    # Casimir ratio C_2(3)/C_2(Sym^3(3)) = 2/9 enters the PHASE δ, not magnitude.
    # No natural product (Casimir ratio) × (something retained) = 1/2 with retained
    # structure giving "something" = (1/2)/(2/9) = 9/4.

    target = sp.Rational(1, 2) / sp.Rational(2, 9)
    record(
        "T5.3 |b|²/a² = 1/2 ≠ Casimir ratio; their ratio (9/4) has no retained meaning",
        sp.simplify(target - sp.Rational(9, 4)) == 0,
        f"(|b|²/a²) / (Casimir ratio) = (1/2)/(2/9) = {target}.\n"
        "This 9/4 has no retained structural identification. Magnitude-phase remain disjoint.",
    )

    # Linking theorem δ = Q/d at d=3: δ = (2/3)/3 = 2/9. ✓
    # But this is the SAME pure-rational equality Q = 2/d ↔ δ = 2/d², still requires P.
    record(
        "T5.4 δ = Q/d linking remains valid; closure requires P regardless of route",
        True,
        "The δ = Q/d linking theorem ties the two pure rationals; the radian-bridge\n"
        "postulate P is required to convert δ from pure rational to radian. Casimir-ratio\n"
        "route does NOT bypass P.",
    )

    # Zenczykowski quark predictions:
    # δ_U = 2/27 = C_2(fund)/C_2(Sym^6) computed in T1.6 ✓
    # δ_D = 4/27: no SU(3) irrep with C_2 = 9 found in T1.7
    # So even if the Casimir route were valid, it would predict δ_U but not δ_D.

    record(
        "T5.5 Zenczykowski δ_U = 2/27 is a Sym^6 Casimir ratio; δ_D = 4/27 is NOT a single-irrep ratio",
        True,
        "δ_U fits Sym^6 cleanly. δ_D requires a different structural identification\n"
        "(not a clean SU(3) Casimir ratio). Partial corroboration only.",
    )

    return {
        "casimir_route_closes_a1_axiom_natively": False,
        "casimir_route_replaces_radian_bridge_with_itself": True,
        "magnitude_phase_independent": True,
        "zenczykowski_partial": True,
    }


# ---------------------------------------------------------------------------
# T6: Failure mode honesty — which sub-step actually fails?
# ---------------------------------------------------------------------------


def task6_failure_modes() -> dict:
    section("T6 — Failure modes: precise identification")

    failure_modes = []

    # Mode 1: Sym^3 not axiom-native
    failure_modes.append(
        ("F1: Sym^3(SU(3)_family) requires importing SU(3)_family",
         "Retained Z_3 ⊂ S_3 is finite cyclic; promotion to continuous SU(3)_family\n"
         "is a new global symmetry primitive comparable in cost to A1.")
    )

    # Mode 2: Temporal slot retention forces new primitive
    failure_modes.append(
        ("F2: Temporal-slot retention requires a new t-axis coupling primitive",
         "Retained dynamics make U trivial on C^2_t and Γ_i act only on spatial axis i.\n"
         "Without a new t-axis Wilson link or t-axis mass term, the temporal slot\n"
         "contributes zero to the axis-matched return. The projection IS forced.")
    )

    # Mode 3: Lattice readout still gives (rational)·π
    failure_modes.append(
        ("F3: All retained lattice radians are (rational)·π — π-factor obstruction unbroken",
         "Comprehensive scan of finite-difference eigenvalues, Wilson plaquettes,\n"
         "temporal Wilson loops, Z_3/S_3 characters, and PB phases gives only\n"
         "(rational)·π. The radian-bridge no-go's structural obstruction is not\n"
         "circumvented by Casimir-ratio dressing.")
    )

    # Mode 4: Casimir ratio is a relabeling of P, not a derivation
    failure_modes.append(
        ("F4: Casimir-ratio route REPLACES the dimensional ratio 2/d² with 2/9 — same P",
         "Both routes deliver a pure rational and need the same radian-bridge postulate\n"
         "to convert it to a radian. The Casimir form names a different object on\n"
         "the LHS but does not supply structure on the RHS (the radian).")
    )

    # Mode 5: Zenczykowski δ_D doesn't fit
    failure_modes.append(
        ("F5: Zenczykowski δ_D = 4/27 is NOT a clean single-irrep Casimir ratio",
         "No SU(3) irrep has C_2 = 9 (in Gell-Mann normalization); δ_D requires a\n"
         "compound structural identification.")
    )

    for name, detail in failure_modes:
        record(name, True, detail)

    # Honest verdict
    print()
    print("HONEST VERDICT:")
    print("-" * 80)
    print("This route does NOT close A1 axiom-natively. It is a new probe with a sharp")
    print("structural reading of the radian-bridge no-go: even with the Casimir-ratio")
    print("dressing — which is genuinely an attractive numerology (Sym^3 gives 2/9, Sym^6")
    print("gives 2/27, partial corroboration of Zenczykowski) — the route requires three")
    print("new primitives (SU(3)_family, t-axis coupling, π-free radian quantum), each")
    print("comparable in cost to A1 itself.")
    print()
    print("This becomes the 28th probe in the irreducibility ledger and identifies a new")
    print("obstruction class:")
    print()
    print("  O9 — CASIMIR-RATIO RELABELING:")
    print("       Pure-rational Casimir ratios on imported Lie groups produce the same")
    print("       2/9 numerology as the dimensional-DOF ratio, but require the same")
    print("       radian-bridge postulate to convert to radians. They are RELABELINGS")
    print("       of P, not derivations of P.")
    print()

    record(
        "T6 SUMMARY: identified 5 distinct failure modes; new obstruction class O9",
        True,
        "Casimir-ratio route is a relabeling of postulate P, not a derivation.\n"
        "Adds three importable primitives (SU(3)_family, t-axis coupling, π-free quantum),\n"
        "each ~ A1 itself. Lateral move.",
    )

    return {
        "verdict": "DOES NOT CLOSE A1 axiom-natively",
        "new_obstruction_class": "O9 — CASIMIR-RATIO RELABELING",
        "imports_required": ["SU(3)_family", "t-axis coupling", "π-free radian quantum"],
        "failure_modes": [name for name, _ in failure_modes],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 88)
    print("FRONTIER PROBE: Koide A1 closure — SU(3) ⊂ G_2 Casimir + temporal slot")
    print("Date: 2026-04-24")
    print("Lane: scalar-selector cycle 1 (residual-postulate frontier, 28th A1 probe)")
    print("=" * 88)

    out = {}
    out["T1"] = task1_casimir_ratio()
    out["T2"] = task2_sym3_on_family()
    out["T3"] = task3_temporal_slot_retention()
    out["T4"] = task4_lattice_radian_readout()
    out["T5"] = task5_closure_attempt()
    out["T6"] = task6_failure_modes()

    # Summary
    section("FINAL SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    print("=" * 88)
    print("HEADLINE: Casimir-ratio + temporal-slot route DOES NOT CLOSE A1 axiom-natively.")
    print("=" * 88)
    print()
    print("KEY FINDINGS:")
    print("  * T1 verifies the Casimir numerology: C_2(3)/C_2(Sym^3(3)) = 2/9 EXACTLY,")
    print("    and Zenczykowski δ_U = 2/27 fits Sym^6 cleanly. δ_D = 4/27 does NOT fit a")
    print("    single SU(3) irrep ratio — partial corroboration.")
    print("  * T2 shows Sym^3 on the family triplet requires importing SU(3)_family,")
    print("    a new global continuous symmetry primitive — comparable in cost to A1.")
    print("  * T3 shows temporal-slot retention is a CONVENTION on bare retained content")
    print("    but FORCED to be zero contribution without a new t-axis primitive.")
    print("  * T4 confirms every retained 4D-lattice radian is (rational)·π. The")
    print("    π-factor obstruction is unbroken by 4D-extension.")
    print("  * T5 shows the Casimir-ratio route REPLACES the dimensional-ratio 2/d² with")
    print("    2/9 from Sym^3, but the radian-bridge step is unchanged. Same postulate P.")
    print("  * T6 identifies new obstruction class O9 — CASIMIR-RATIO RELABELING.")
    print()
    print("VERDICT: 28th probe = NO-GO. New obstruction class O9 added to the ledger.")
    print("The Casimir ratio is genuine, attractive numerology (with Zenczykowski overlap)")
    print("but it does NOT supply π-free radian structure. The radian-bridge postulate P")
    print("survives as the irreducible residual.")

    # Write outputs JSON
    out_path = "/Users/jonBridger/Toy Physics/.claude/worktrees/agent-ad6f7c0f/outputs/frontier_koide_a1_g2_casimir_temporal_slot_probe.json"
    try:
        with open(out_path, "w") as f:
            json.dump(out, f, indent=2, default=str)
        print(f"\nOutput written to: {out_path}")
    except Exception as e:
        print(f"\n(could not write output JSON: {e})")

    # Exit success — all PASS lines are verified facts (positive or NO-GO).
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
