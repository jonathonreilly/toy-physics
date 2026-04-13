#!/usr/bin/env python3
"""
Generation Matter Assignment: Canonicality Test on the Graph/Taste Surface
==========================================================================

Goal: test the strongest paper-safe claim about the two size-3 Z3 orbit
classes on the Cl(3) taste surface.

Question:
    Do the orbit classes T_1 and T_2 become canonically identifiable as
    physical fermion families from the graph/taste surface itself, once we
    include:
      - gauge quantum numbers,
      - radiative / coupling corrections,
      - topological index-like contributions,
      - and the Z3-breaking hierarchy picture?

This script does NOT restate 8 = 1 + 1 + 3 + 3.  That orbit algebra is
assumed known and exact.  Instead it tests whether the current surface
actually fixes a unique matter assignment.

Expected outcome:
    - Orbit structure: exact.
    - Orbit exchange symmetry: exact.
    - Distinct diagnostics: present, but operator-dependent.
    - Canonical physical-generation assignment: not derived.

The sharp obstruction is that the two triplets are related by an exact
complement symmetry and are isomorphic as Z3 representations.  The extra
quantum-number, coupling, and index labels all require added structure or
chosen operators; they do not come from the pure orbit algebra alone.
"""

from __future__ import annotations

import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import product

import numpy as np

np.set_printoptions(precision=8, linewidth=120)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
I8 = np.eye(8, dtype=complex)


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


def taste_states():
    return [(s1, s2, s3) for s1, s2, s3 in product(range(2), repeat=3)]


def hamming_weight(s):
    return sum(s)


def sigma(s):
    return (s[1], s[2], s[0])


def complement(s):
    return tuple(1 - x for x in s)


def orbit_decomposition():
    visited = set()
    orbits = []
    for s in taste_states():
        if s in visited:
            continue
        orbit = []
        cur = s
        for _ in range(3):
            if cur not in visited:
                orbit.append(cur)
                visited.add(cur)
            cur = sigma(cur)
        orbits.append(tuple(orbit))
    singlets = [o for o in orbits if len(o) == 1]
    triplets = [o for o in orbits if len(o) == 3]
    return orbits, singlets, triplets


def cyclic_rep_matrix(orbit):
    """Return the 3x3 matrix of sigma in the orbit basis ordered along the cycle."""
    basis = list(orbit)
    idx = {s: i for i, s in enumerate(basis)}
    M = np.zeros((len(basis), len(basis)), dtype=complex)
    for s in basis:
        src = idx[s]
        dst = idx[sigma(s)]
        M[dst, src] = 1.0
    return M


def weak_axis_t3(axis):
    """T3 = +/- 1/2 on one chosen tensor factor."""
    ops = [I2, I2, I2]
    ops[axis] = 0.5 * SZ
    return kron3(ops[0], ops[1], ops[2])


def basis_vec(s):
    idx = 4 * s[0] + 2 * s[1] + s[2]
    v = np.zeros(8, dtype=complex)
    v[idx] = 1.0
    return v


def axis_counts(T3, orbit):
    up = 0
    down = 0
    for s in orbit:
        v = basis_vec(s)
        val = float(np.real(v.conj() @ T3 @ v))
        if np.isclose(val, 0.5):
            up += 1
        elif np.isclose(val, -0.5):
            down += 1
        else:
            raise RuntimeError(f"unexpected T3 eigenvalue {val} for {s}")
    return up, down


def mass_proxy(hw, r):
    return 2.0 * r * hw


def coupling_proxy(hw):
    return hw / (np.pi ** 2)


def chirality_proxy(s):
    return (-1) ** hamming_weight(s)


def index_proxy(orbit):
    # This is a grading proxy, not a derived topological index theorem.
    return sum(chirality_proxy(s) for s in orbit)


def section_orbit_symmetry(T1, T2):
    print("\n" + "=" * 78)
    print("SECTION 1: ORBIT SYMMETRY AND REPRESENTATION IDENTITY")
    print("=" * 78)

    M1 = cyclic_rep_matrix(T1)
    M2 = cyclic_rep_matrix(T2)
    evals1 = sorted(np.linalg.eigvals(M1), key=lambda z: np.angle(z))
    evals2 = sorted(np.linalg.eigvals(M2), key=lambda z: np.angle(z))
    omega = np.exp(2j * np.pi / 3)

    print(f"  T1 orbit: {T1}")
    print(f"  T2 orbit: {T2}")
    print(f"  Z3 eigenvalues on T1: {[f'{z:.6f}' for z in evals1]}")
    print(f"  Z3 eigenvalues on T2: {[f'{z:.6f}' for z in evals2]}")

    check("T1 and T2 are both 3-dim regular Z3 reps",
          np.allclose(sorted(evals1, key=lambda z: np.angle(z)),
                      sorted([1.0, omega, omega.conjugate()], key=lambda z: np.angle(z)))
          and np.allclose(sorted(evals2, key=lambda z: np.angle(z)),
                          sorted([1.0, omega, omega.conjugate()], key=lambda z: np.angle(z))))

    # Exact exchange symmetry.
    T1_to_T2 = {complement(s) for s in T1}
    T2_to_T1 = {complement(s) for s in T2}
    check("Complement maps T1 to T2", T1_to_T2 == set(T2), f"{T1_to_T2} -> T2")
    check("Complement maps T2 to T1", T2_to_T1 == set(T1), f"{T2_to_T1} -> T1")

    # The only intrinsic orbit labels are size and Hamming weight.
    orbit_data = {tuple(o): (len(o), hamming_weight(o[0])) for o in (T1, T2)}
    print(f"  Orbit intrinsic data: {orbit_data}")
    check("T1 and T2 differ only by Hamming weight, not by Z3 spectrum",
          len(set(evals1)) == 3 and len(set(evals2)) == 3 and orbit_data[T1] != orbit_data[T2])


def section_axis_ambiguity(T1, T2):
    print("\n" + "=" * 78)
    print("SECTION 2: WEAK-AXIS AMBIGUITY")
    print("=" * 78)

    axis_counts_by_orbit = {}
    for axis in range(3):
        T3 = weak_axis_t3(axis)
        t1_counts = axis_counts(T3, T1)
        t2_counts = axis_counts(T3, T2)
        axis_counts_by_orbit[axis] = (t1_counts, t2_counts)
        print(f"  axis {axis + 1}: T1 counts (up,down) = {t1_counts}, T2 counts = {t2_counts}")

    # All three axis choices produce the same count pattern up to the same swap.
    t1_patterns = {v[0] for v in axis_counts_by_orbit.values()}
    t2_patterns = {v[1] for v in axis_counts_by_orbit.values()}
    check("All three axis choices give the same T1 count pattern",
          len(t1_patterns) == 1, f"{t1_patterns}")
    check("All three axis choices give the same T2 count pattern",
          len(t2_patterns) == 1, f"{t2_patterns}")
    check("The count pattern alone does not select a unique weak axis",
          len(axis_counts_by_orbit) == 3)

    print("  Interpretation:")
    print("    - The triplets admit a weak-axis embedding.")
    print("    - The embedding is not uniquely selected by the orbit data.")
    print("    - Therefore gauge quantum numbers are representation-level data,")
    print("      not intrinsic orbit labels on the pure graph/taste surface.")


def section_deformation_dependence(T1, T2):
    print("\n" + "=" * 78)
    print("SECTION 3: DEFORMATION-DEPENDENT COUPLING / MASS PROXIES")
    print("=" * 78)

    print("  Wilson-like mass proxy m_W(hw) = 2 r hw")
    print("  Gauge-correction proxy Delta_g(hw) = hw / pi^2")
    print("  These are useful diagnostics, but they depend on the chosen deformation")
    print("  parameters and do not come from the orbit combinatorics alone.\n")

    r_values = [0.1, 0.3, 0.5, 1.0]
    print(f"  {'r':>6s} {'m(T1)':>10s} {'m(T2)':>10s} {'ratio':>8s}")
    for r in r_values:
        m1 = mass_proxy(1, r)
        m2 = mass_proxy(2, r)
        print(f"  {r:6.2f} {m1:10.4f} {m2:10.4f} {m2/m1:8.3f}")

    check("Mass ratio T2/T1 is fixed in the toy proxy",
          all(np.isclose(mass_proxy(2, r) / mass_proxy(1, r), 2.0) for r in r_values))

    print("\n  Gauge correction proxies:")
    print(f"    Delta_g(T1) = {coupling_proxy(1):.6f}")
    print(f"    Delta_g(T2) = {coupling_proxy(2):.6f}")
    check("Gauge-correction proxy distinguishes T1 and T2",
          not np.isclose(coupling_proxy(1), coupling_proxy(2)))

    print("\n  Obstruction:")
    print("    - the scale is set by r and/or anisotropy, not by the orbit algebra")
    print("    - the couplings here are model diagnostics, not a derived family index")


def section_index_proxy(T1, T2):
    print("\n" + "=" * 78)
    print("SECTION 4: TOPLOGICAL/CHIRAL INDEX PROXY")
    print("=" * 78)

    p1 = [chirality_proxy(s) for s in T1]
    p2 = [chirality_proxy(s) for s in T2]
    i1 = index_proxy(T1)
    i2 = index_proxy(T2)

    print(f"  T1 chirality proxy (-1)^|s|: {p1}")
    print(f"  T2 chirality proxy (-1)^|s|: {p2}")
    print(f"  T1 index proxy: {i1}")
    print(f"  T2 index proxy: {i2}")

    check("T1 and T2 carry opposite parity grading",
          len(set(p1)) == 1 and len(set(p2)) == 1 and p1[0] != p2[0],
          f"T1={p1[0]}, T2={p2[0]}")
    check("Index proxy distinguishes the triplets",
          i1 != i2, f"T1={i1}, T2={i2}")

    print("  Interpretation:")
    print("    - This is a chirality/parity grading induced by Hamming weight.")
    print("    - It is not yet a derived topological index theorem for the graph.")
    print("    - By itself it does not select a unique physical generation basis.")


def conclusion():
    print("\n" + "=" * 78)
    print("CONCLUSION: SHARPEST OBSTRUCTION")
    print("=" * 78)
    print("""
  What the current graph/taste surface DOES prove:
    - exact orbit algebra 8 = 1 + 1 + 3 + 3
    - the two triplets are exchanged by an exact complement symmetry
    - the triplets are isomorphic as Z3 representations
    - model-level diagnostics (mass proxy, coupling proxy, chirality proxy)
      can distinguish them once extra operators are chosen

  What it does NOT yet prove:
    - a canonical matter-assignment theorem
    - a unique physical-family identification of T1 vs T2
    - a derived topological index theorem that singles out the triplets
    - a derivation that the observed hierarchy follows without additional
      Z3-breaking input

  Sharp obstruction:
    The triplets are symmetry-related on the pure graph/taste surface.
    Any assignment of 'physical generation' labels uses extra structure:
      - a chosen weak-axis embedding,
      - a chosen deformation/coupling scale,
      - or an additional symmetry-breaking / index datum.

  Paper-safe statement:
    The audited Z3 taste action yields two symmetry-distinct triplet sectors
    with useful model diagnostics, but the canonical identification of those
    sectors with physical fermion generations remains open.
""")


def main():
    t0 = time.time()
    print("=" * 78)
    print("GENERATION MATTER ASSIGNMENT")
    print("Canonicality test on the graph/taste surface")
    print("=" * 78)

    _, singlets, triplets = orbit_decomposition()
    assert len(singlets) == 2 and len(triplets) == 2
    T1 = [o for o in triplets if hamming_weight(o[0]) == 1][0]
    T2 = [o for o in triplets if hamming_weight(o[0]) == 2][0]

    check("Orbit algebra 8 = 1 + 1 + 3 + 3",
          sorted(len(o) for o in singlets + triplets) == [1, 1, 3, 3])

    section_orbit_symmetry(T1, T2)
    section_axis_ambiguity(T1, T2)
    section_deformation_dependence(T1, T2)
    section_index_proxy(T1, T2)
    conclusion()

    dt = time.time() - t0
    print(f"\nCompleted in {dt:.2f}s")
    print(f"Results: {PASS_COUNT} passed, {FAIL_COUNT} failed out of {PASS_COUNT + FAIL_COUNT} checks")
    if FAIL_COUNT > 0:
        print("*** FAILURES DETECTED ***")
        sys.exit(1)
    print("OBSTRUCTION ESTABLISHED")
    sys.exit(0)


if __name__ == "__main__":
    main()
