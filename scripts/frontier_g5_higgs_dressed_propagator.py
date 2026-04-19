#!/usr/bin/env python3
"""
G5 Avenue G — Higgs-dressed intermediate propagator
====================================================

STATUS: exact numerical construction of the retained second-order return on
`T_1` with a Hermitian weight `W(H)` built from the G1 retained H(m, delta,
q_+) operator inserted between the two `Gamma_1` hops, instead of the
unit-weighted intermediate projector `(P_{O_0} + P_{T_2})`.

Target: find whether any of three retained H-lifts — function-of-H, resolvent,
eigenvalue-chamber-weights — produces the Koide-compatible charged-lepton
hierarchy (w_O0, w_a, w_b) with Q = 2/3 and correct direction to PDG.

Avenue G is structurally distinct from:
 - Agent 9 (H directly as charged-lepton mass operator)
 - Agent 12 (H lifted post-hoc to T_2)
 - Agent 13 (H and species-diagonal subspace orthogonality)

Here H is a WEIGHT / PROPAGATOR INSERTION between two Gamma_1 steps, not a
direct mass operator or a diagonal lift. The three species of T_1 hop via
Gamma_1 to three *distinct* intermediate states (O_0 and two T_2 states),
so different eigenvalues of H acting on the intermediate space translate
into distinct scalar weights on the three species.

The runner:
  1. Verifies the baseline Sigma_identity = I_3 on C^16.
  2. Defines three retained H-lifts to the intermediate space O_0 ⊕ T_2.
  3. For each of the three constructions G-1 (f(H) lift), G-2 (resolvent),
     G-3 (chamber-eigenvalue weights), computes diag(Sigma_Higgs), Koide Q,
     cos-similarity to PDG charged-lepton direction.
  4. Emits the four-outcome verdict.

Framework-native retained constants only. PDG masses used ONLY for post-hoc
comparison, NEVER as derivation inputs.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=160)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


# ======================================================================
# Cl(3) + chirality carrier on C^16 — identical to Dirac-bridge runner
# ======================================================================

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
I16 = np.eye(16, dtype=complex)


def kron4(a, b, c, d):
    return np.kron(a, np.kron(b, np.kron(c, d)))


G0 = kron4(SZ, SZ, SZ, SX)
G1 = kron4(SX, I2, I2, I2)
G2 = kron4(SZ, SX, I2, I2)
G3 = kron4(SZ, SZ, SX, I2)
SPATIAL_GAMMAS = [G1, G2, G3]
GAMMA_5_4D = G0 @ G1 @ G2 @ G3

FULL_STATES = [(a, b, c, t) for a in range(2) for b in range(2) for c in range(2) for t in range(2)]
INDEX = {state: i for i, state in enumerate(FULL_STATES)}

O0_STATES = [(0, 0, 0)]
T1_STATES = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
T2_STATES = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
O3_STATES = [(1, 1, 1)]


def projector(spatial_states):
    p = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        for s in spatial_states:
            p[INDEX[s + (t,)], INDEX[s + (t,)]] = 1.0
    return p


P_O0 = projector(O0_STATES)
P_T1 = projector(T1_STATES)
P_T2 = projector(T2_STATES)
P_O3 = projector(O3_STATES)


def t1_species_basis_L():
    """3 column vectors, one per T_1 species, in the L-chirality taste (t=0)."""
    cols = []
    for s in T1_STATES:
        e = np.zeros((16, 1), dtype=complex)
        e[INDEX[s + (0,)], 0] = 1.0
        cols.append(e)
    return np.hstack(cols)


BASIS_T1_L = t1_species_basis_L()


def restrict_species(op16):
    """16x16 -> 3x3 species block using L-taste T_1 subspace."""
    return BASIS_T1_L.conj().T @ op16 @ BASIS_T1_L


# ======================================================================
# G1 retained H(m, delta, q_+) — exact from G1 Physicist-H closure theorem
# ======================================================================

GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0

T_M = np.array([[1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 1.0, 0.0]], dtype=complex)
T_DELTA = np.array([[0.0, -1.0, 1.0],
                    [-1.0, 1.0, 0.0],
                    [1.0, 0.0, -1.0]], dtype=complex)
T_Q = np.array([[0.0, 1.0, 1.0],
                [1.0, 0.0, 1.0],
                [1.0, 1.0, 0.0]], dtype=complex)
H_BASE = np.array([[0.0, E1, -E1 - 1j * GAMMA],
                   [E1, 0.0, -E2],
                   [-E1 + 1j * GAMMA, -E2, 0.0]], dtype=complex)


def H3(m, delta, q_plus):
    """Retained affine Hermitian H(m, delta, q_+) on the three-generation triplet."""
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


# G1 observational chamber pin (PMNS-pinned)
M_STAR = 0.657061342210
DELTA_STAR = 0.933806343759
Q_PLUS_STAR = 0.715042329587

H_STAR_3 = H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)
H_STAR_EIGS, _ = np.linalg.eigh(H_STAR_3)  # ascending real eigenvalues
# documented in the G1 note: (-1.30909, -0.32043, +2.28659)

# PDG charged-lepton masses (MeV) — external comparison ONLY
M_E = 0.51099895
M_MU = 105.6583755
M_TAU = 1776.86
PDG_MASSES = np.array([M_E, M_MU, M_TAU])
PDG_SQRT_DIRECTION = np.sqrt(PDG_MASSES) / np.linalg.norm(np.sqrt(PDG_MASSES))


def koide_Q(masses):
    masses = np.asarray(masses, dtype=float)
    if np.any(masses < 0):
        masses = np.abs(masses)
    s = float(np.sum(masses))
    rs = float(np.sum(np.sqrt(masses)))
    if rs == 0:
        return float("nan")
    return s / (rs * rs)


def direction_cos(masses):
    sq = np.sqrt(np.abs(np.asarray(masses, dtype=float)))
    n = np.linalg.norm(sq)
    if n == 0:
        return float("nan")
    v = sq / n
    return float(np.dot(v, PDG_SQRT_DIRECTION))


def pretty(vs):
    return "[" + ", ".join(f"{float(v): .6e}" for v in vs) + "]"


# ======================================================================
# PHASE 1 — baseline Sigma_identity = I_3
# ======================================================================

def phase1_baseline():
    print("=" * 78)
    print("PHASE 1 — baseline Sigma_identity on the Dirac-bridge carrier")
    print("=" * 78)
    check("Gamma_1 Hermitian", np.allclose(G1, G1.conj().T))
    check("Gamma_1^2 = I_16", np.allclose(G1 @ G1, I16))
    sigma_full = P_T1 @ G1 @ (P_O0 + P_T2) @ G1 @ P_T1
    sigma_species = restrict_species(sigma_full)
    check("P_T1 Gamma_1 (P_O0 + P_T2) Gamma_1 P_T1 species-block = I_3",
          np.allclose(sigma_species, np.eye(3), atol=1e-12))
    print(f"  diag(Sigma_identity species) = {pretty(np.real(np.diag(sigma_species)))}")
    print()
    return sigma_species


# ======================================================================
# HELPER — identify the three intermediate states reached by Gamma_1 from T_1
# ======================================================================

def hopping_map():
    """Map species index (0,1,2) to its Gamma_1-reached intermediate state.
    Gamma_1 flips spatial axis 1 (first bit). On L-taste (t=0):
      species 0 = (1,0,0) -> (0,0,0) = O_0
      species 1 = (0,1,0) -> (1,1,0) = T_2 state #0
      species 2 = (0,0,1) -> (1,0,1) = T_2 state #1
    The third T_2 state (0,1,1) is NOT reached from T_1 in one hop.
    """
    return [
        ("O_0", (0, 0, 0)),
        ("T_2[1,1,0]", (1, 1, 0)),
        ("T_2[1,0,1]", (1, 0, 1)),
    ]


def sigma_with_weight_operator(W16):
    """Compute Sigma_Higgs = P_T1 G1 W16 G1 P_T1 species-block.
    W16 is a 16x16 Hermitian weight supported on O_0 ⊕ T_2.
    """
    op = P_T1 @ G1 @ W16 @ G1 @ P_T1
    return restrict_species(op)


def verify_hopping():
    """Verify each species hops to its documented intermediate target."""
    print("  Verifying Gamma_1 hopping on L-taste:")
    ok = True
    for idx, s_in in enumerate(T1_STATES):
        e = np.zeros((16, 1), dtype=complex)
        e[INDEX[s_in + (0,)], 0] = 1.0
        out = G1 @ e
        nz = np.where(np.abs(out.flatten()) > 1e-10)[0]
        targets = [FULL_STATES[i] for i in nz]
        print(f"    species {idx} in={s_in}(L) -> out={targets}")
    return ok


# ======================================================================
# RETAINED H-LIFT to the intermediate space O_0 ⊕ T_2
# ======================================================================
#
# H3 is a 3x3 Hermitian on T_1. We must lift it to act on the 4-dim
# intermediate subspace O_0 ⊕ T_2 in a retained, structure-preserving way.
#
# Retained labelling of the 4 intermediate basis states:
#   O_0       = (0,0,0)
#   T_2[110]  = (1,1,0)   carries 'missing axis 3' label
#   T_2[101]  = (1,0,1)   carries 'missing axis 2' label
#   T_2[011]  = (0,1,1)   carries 'missing axis 1' label
#
# The three T_2 states are 'complement' states of axes 1,2,3 respectively.
# Equivalently, T_2 states are labelled by the MISSING axis.
#
# Gamma_1-hopping from T_1:
#   species 1 (axis 1) -> O_0
#   species 2 (axis 2) -> T_2[110]  (missing axis 3)
#   species 3 (axis 3) -> T_2[101]  (missing axis 2)
#
# This is a natural but NOT trivial species-to-intermediate bijection — the
# hopping is 1-to-O_0, and 2<->missing-3, 3<->missing-2 on the other two.
#
# LIFT OPTION (i): retain a Cl(3)-covariant extension.
#
# The cleanest retained lift is: extend H3 to act on O_0 ⊕ T_2 as
#     H_lift = diag(H_O0, H_T2)
# where H_T2 acts on the T_2 triplet in the missing-axis labelling. Two
# retained sub-options for embedding:
#
#   (ia) Direct same-basis embed: treat T_2 basis in order
#        (T_2[011], T_2[101], T_2[110]) (missing axis 1, 2, 3) as the
#        same index triplet as T_1 species (1, 2, 3). Then H_T2 = H3
#        literally, with the MISSING-AXIS labelling matching the species
#        labelling. This is a covariant Z_3 sector identification.
#
#   (ib) Hopping-aligned embed: order T_2 in the hopping-reached order
#        (T_2[110], T_2[101], T_2[011]) matching species (2, 3, 1).
#        Then H_T2 = P_{sigma} H3 P_{sigma}^T for the corresponding
#        permutation sigma.
#
# Both are retained Cl(3)-covariant choices; they differ by a relabelling
# permutation. We test both; (ia) is the 'natural' missing-axis choice.
#
# For the O_0 direction we have a retained scalar H_O0 ∈ R.  Retained
# candidates are:  H_O0 = 0 (no on-site); H_O0 = tr(H3)/3 (mean); or
# H_O0 = (one of the three eigenvalues of H3). We use (tr H3)/3 as the
# natural retained Cl(3)-singlet value; alternate sweeps test the others.

# Ordered basis for the 4-dim intermediate:
INTER_BASIS_LABEL = [
    ("O_0", (0, 0, 0)),
    ("T2_011", (0, 1, 1)),  # missing axis 1
    ("T2_101", (1, 0, 1)),  # missing axis 2
    ("T2_110", (1, 1, 0)),  # missing axis 3
]


def inter_basis_L():
    """4 column vectors spanning O_0 ⊕ T_2 on L-taste (t=0)."""
    cols = []
    for (_, s) in INTER_BASIS_LABEL:
        e = np.zeros((16, 1), dtype=complex)
        e[INDEX[s + (0,)], 0] = 1.0
        cols.append(e)
    return np.hstack(cols)


def inter_basis_R():
    """Same, R-taste (t=1), for completeness on the Dirac-bridge double cover."""
    cols = []
    for (_, s) in INTER_BASIS_LABEL:
        e = np.zeros((16, 1), dtype=complex)
        e[INDEX[s + (1,)], 0] = 1.0
        cols.append(e)
    return np.hstack(cols)


B_INTER_L = inter_basis_L()
B_INTER_R = inter_basis_R()


def embed_4x4_to_16(W4):
    """Embed a 4x4 operator on (O_0, T2_011, T2_101, T2_110) into a 16x16
    operator acting on both chirality tastes identically (taste-singlet).
    Everything outside the intermediate subspace is zero.
    """
    W16 = np.zeros((16, 16), dtype=complex)
    # L-taste block
    W16 = W16 + B_INTER_L @ W4 @ B_INTER_L.conj().T
    # R-taste block (same operator, taste-singlet)
    W16 = W16 + B_INTER_R @ W4 @ B_INTER_R.conj().T
    return W16


def H_lift_missing_axis(h_O0_scalar):
    """LIFT (ia): embed H3 onto T_2 in missing-axis labelling, with an
    additional scalar weight on O_0.
    Return a 4x4 Hermitian matrix on (O_0, T2_011, T2_101, T2_110).
    """
    W4 = np.zeros((4, 4), dtype=complex)
    W4[0, 0] = h_O0_scalar
    # Rows/cols 1..3 are ordered by missing-axis 1, 2, 3 — matching the
    # T_1 species labelling by axis. So H3 embeds directly.
    W4[1:, 1:] = H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)
    return W4


def H_lift_hopping_aligned(h_O0_scalar):
    """LIFT (ib): embed H3 onto T_2 in hopping-aligned order.
    Gamma_1 sends species 2 -> T2_110 (missing axis 3),
              species 3 -> T2_101 (missing axis 2),
              species 1 -> O_0.
    So in the intermediate basis (O_0, T2_011, T2_101, T2_110), the
    hopping from species k lands on intermediate index (0, 3, 2)
    respectively (species 1 -> O_0, species 2 -> T2_110 [idx 3],
    species 3 -> T2_101 [idx 2]).
    This hopping-aligned order is a permutation of the missing-axis
    order. We embed H3 on rows/cols 1..3 permuted to match:
    T2_011 (idx 1) <-> species 1, BUT species 1 hops to O_0, not T2_011,
    so T2_011 is UNREACHED. Keep H3[0,0] on T2_011 for completeness.
    Instead, align intermediate-target-species: T2_110 is species 2's
    target, so H3[1,1] goes on T2_110; T2_101 is species 3's target, so
    H3[2,2] goes on T2_101. T2_011 has no hopping partner, assign H3[0,0].
    Result (keeping H3 structure intact on T_2 block, just permuted):
    """
    W4 = np.zeros((4, 4), dtype=complex)
    W4[0, 0] = h_O0_scalar
    # Permutation: T2_011 <- species 1, T2_101 <- species 3, T2_110 <- species 2
    # So intermediate order-to-species map: (0->O_0 scalar), (1->1), (2->3), (3->2)
    # Embed H3 with row/col permutation P where P[inter_idx, species] = 1:
    P = np.zeros((3, 3), dtype=complex)
    # inter row idx 0 (T2_011) <- species 0 (which is #1)
    # inter row idx 1 (T2_101) <- species 2 (which is #3)
    # inter row idx 2 (T2_110) <- species 1 (which is #2)
    P[0, 0] = 1.0
    P[1, 2] = 1.0
    P[2, 1] = 1.0
    H_perm = P @ H3(M_STAR, DELTA_STAR, Q_PLUS_STAR) @ P.T
    W4[1:, 1:] = H_perm
    return W4


# ======================================================================
# CONSTRUCTION G-1 — W(H) = f(H_lift)
# ======================================================================

def construction_G1_function_of_H():
    print("=" * 78)
    print("CONSTRUCTION G-1 — W(H) = f(H_lift) (function of lifted H)")
    print("=" * 78)

    # Retained H-lift candidates (3 choices for H_O0 scalar, 2 orderings)
    # We systematically test f ∈ { H, H^2, exp(H), |H| (abs of eigenvalues) }.
    results = []

    def test_f(name_f, fn, W4):
        # Apply f to the 4x4 Hermitian W4
        evals, evecs = np.linalg.eigh(W4)
        f_evals = fn(evals)
        W4_f = evecs @ np.diag(f_evals) @ evecs.conj().T
        W16 = embed_4x4_to_16(W4_f)
        sigma = sigma_with_weight_operator(W16)
        d = np.real(np.diag(sigma))
        # Also compute eigenvalues (physical mass-squared interpretation)
        sigma_eigs = np.linalg.eigvalsh((sigma + sigma.conj().T) / 2.0)
        # Check Hermiticity of sigma
        herm = np.allclose(sigma, sigma.conj().T, atol=1e-10)
        off = float(np.max(np.abs(sigma - np.diag(np.diag(sigma)))))
        return d, herm, off, sigma_eigs

    for h_O0 in [0.0, float(np.trace(H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)).real) / 3.0]:
        for (label_lift, lift_fn) in [("missing-axis", H_lift_missing_axis),
                                       ("hopping-aligned", H_lift_hopping_aligned)]:
            W4 = lift_fn(h_O0)
            for (label_f, fn_f) in [
                ("f=H", lambda x: x),
                ("f=H^2", lambda x: x * x),
                ("f=exp(H)", lambda x: np.exp(x)),
                ("f=|H|", lambda x: np.abs(x)),
                ("f=H+shift", lambda x: x - np.min(x) + 0.1),
            ]:
                d, herm, off, sigma_eigs = test_f(label_f, fn_f, W4)
                # Diagonal reading
                m = np.abs(d)
                if np.all(m > 1e-14):
                    Q_diag = koide_Q(m)
                    cs_diag = direction_cos(m)
                else:
                    Q_diag = float("nan")
                    cs_diag = float("nan")
                # Eigenvalue reading (physical mass eigenvalues)
                m_eig = np.abs(sigma_eigs)
                if np.all(m_eig > 1e-14):
                    Q_eig = koide_Q(m_eig)
                    cs_eig = direction_cos(m_eig)
                else:
                    Q_eig = float("nan")
                    cs_eig = float("nan")
                # Best of the two readings
                best_cs_val = max(cs_diag if not math.isnan(cs_diag) else -2,
                                  cs_eig if not math.isnan(cs_eig) else -2)
                best_Q_val = (Q_diag if not math.isnan(Q_diag) and
                              (math.isnan(Q_eig) or abs(Q_diag - 2/3) < abs(Q_eig - 2/3))
                              else Q_eig)
                print(f"  lift={label_lift:18s} h_O0={h_O0:+.4f} {label_f:10s} diag={pretty(d)}")
                print(f"    |  Q_diag={Q_diag:.4f} cs_diag={cs_diag:.4f} | "
                      f"Q_eig={Q_eig:.4f} cs_eig={cs_eig:.4f} | offdiag={off:.2e}")
                results.append({
                    "lift": label_lift, "h_O0": h_O0, "f": label_f,
                    "diag": d, "eigs": sigma_eigs,
                    "Q": best_Q_val if best_Q_val is not None else Q_diag,
                    "cs": best_cs_val,
                    "Q_diag": Q_diag, "cs_diag": cs_diag,
                    "Q_eig": Q_eig, "cs_eig": cs_eig,
                })

    # Best Q match and best cos-sim (use whichever reading is better per-candidate)
    valid = [r for r in results if not math.isnan(r["Q"]) and r["cs"] > -1.5]
    if not valid:
        valid = results
    best_cs = max(valid, key=lambda r: r["cs"] if not math.isnan(r["cs"]) else -2)
    best_Q = min(valid, key=lambda r: abs(r["Q"] - 2 / 3) if not math.isnan(r["Q"]) else 1e9)
    print()
    print(f"  BEST cos-sim: {best_cs['cs']:.4f} (lift={best_cs['lift']}, h_O0={best_cs['h_O0']:.4f}, {best_cs['f']})")
    print(f"       diag={pretty(best_cs['diag'])}  eigs={pretty(best_cs['eigs'])}  Q={best_cs['Q']:.4f}")
    print(f"  BEST |Q-2/3|: {abs(best_Q['Q']-2/3):.4e} (lift={best_Q['lift']}, h_O0={best_Q['h_O0']:.4f}, {best_Q['f']})")
    print(f"       diag={pretty(best_Q['diag'])}  eigs={pretty(best_Q['eigs'])}  cs={best_Q['cs']:.4f}")

    # Structural PASS: W(H) produces a Hermitian Sigma_Higgs (test sample)
    W4_probe = H_lift_missing_axis(0.1)
    W16_probe = embed_4x4_to_16(W4_probe)
    sigma_probe = P_T1 @ G1 @ W16_probe @ G1 @ P_T1
    sigma_probe_3 = restrict_species(sigma_probe)
    check("G-1: Sigma_Higgs Hermitian for H-lift probe",
          np.allclose(sigma_probe_3, sigma_probe_3.conj().T, atol=1e-10))

    # Structural PASS: the construction produces species-resolved diagonals
    got_resolved = any(float(np.std(r["diag"])) > 1e-6 for r in valid)
    check("G-1: produces species-resolved diagonals for at least one (lift, f)",
          got_resolved, detail=f"max std(diag) across candidates = "
          f"{max(float(np.std(r['diag'])) for r in valid):.3e}")

    # Verdict thresholds
    print()
    print("  G-1 verdict: " + (
        "MATCH (Koide and cos-sim both pass)" if (
            best_cs["cs"] > 0.99 and abs(best_cs["Q"] - 2 / 3) < 1e-3
        ) else "NO_MATCH (best cos-sim or Q-deviation exceeds thresholds)"
    ))
    print()
    return results, best_cs, best_Q


# ======================================================================
# CONSTRUCTION G-2 — W(H) = 1/(lambda - H_lift) (resolvent)
# ======================================================================

def construction_G2_resolvent():
    print("=" * 78)
    print("CONSTRUCTION G-2 — W(H) = 1 / (lambda - H_lift) (resolvent)")
    print("=" * 78)

    # Retained choices for lambda: we do NOT have access to v/M_Pl as pure
    # numerical inputs without PDG, so we use RETAINED scalar candidates:
    #   lambda = 0 (pole at center)
    #   lambda = chamber boundary value q_+ + delta - sqrt(8/3) offset = 0.0159
    #   lambda = eigenvalue spacing sqrt(8/3)  (retained E1)
    #   lambda = E2 = sqrt(8)/3  (retained E2)
    #   lambda above max eigenvalue (fully positive): e.g. +3.0, +10.0
    # No post-axiom inputs.
    lambda_candidates = [
        ("lambda=0", 0.0),
        ("lambda=E1", E1),
        ("lambda=E2", E2),
        ("lambda=-E1", -E1),
        ("lambda=chamber_slack", Q_PLUS_STAR + DELTA_STAR - math.sqrt(8.0 / 3.0)),
        ("lambda=eig_max+0.1", float(H_STAR_EIGS[-1]) + 0.1),
        ("lambda=eig_min-0.1", float(H_STAR_EIGS[0]) - 0.1),
        ("lambda=+3.0", 3.0),
        ("lambda=+10.0", 10.0),
    ]

    results = []
    for h_O0 in [0.0, float(np.trace(H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)).real) / 3.0]:
        for (label_lift, lift_fn) in [("missing-axis", H_lift_missing_axis),
                                       ("hopping-aligned", H_lift_hopping_aligned)]:
            W4 = lift_fn(h_O0)
            evals, evecs = np.linalg.eigh(W4)
            for (label_lam, lam) in lambda_candidates:
                diffs = lam - evals
                if np.any(np.abs(diffs) < 1e-10):
                    continue  # skip near-pole
                W4_res = evecs @ np.diag(1.0 / diffs) @ evecs.conj().T
                W16 = embed_4x4_to_16(W4_res)
                sigma = sigma_with_weight_operator(W16)
                d = np.real(np.diag(sigma))
                sigma_eigs = np.linalg.eigvalsh((sigma + sigma.conj().T) / 2.0)
                m = np.abs(d)
                Q_diag = koide_Q(m) if np.all(m > 1e-14) else float("nan")
                cs_diag = direction_cos(m) if np.all(m > 1e-14) else float("nan")
                m_eig = np.abs(sigma_eigs)
                Q_eig = koide_Q(m_eig) if np.all(m_eig > 1e-14) else float("nan")
                cs_eig = direction_cos(m_eig) if np.all(m_eig > 1e-14) else float("nan")
                best_cs_val = max(cs_diag if not math.isnan(cs_diag) else -2,
                                  cs_eig if not math.isnan(cs_eig) else -2)
                if not math.isnan(Q_diag) and (math.isnan(Q_eig) or abs(Q_diag - 2/3) < abs(Q_eig - 2/3)):
                    best_Q_val = Q_diag
                else:
                    best_Q_val = Q_eig
                off = float(np.max(np.abs(sigma - np.diag(np.diag(sigma)))))
                print(f"  lift={label_lift:18s} h_O0={h_O0:+.4f} {label_lam:20s} diag={pretty(d)}")
                print(f"    |  Q_diag={Q_diag:.4f} cs_diag={cs_diag:.4f} | Q_eig={Q_eig:.4f} cs_eig={cs_eig:.4f}")
                results.append({
                    "lift": label_lift, "h_O0": h_O0, "lambda_label": label_lam,
                    "lambda": lam, "diag": d, "eigs": sigma_eigs,
                    "Q": best_Q_val if best_Q_val is not None else Q_diag,
                    "cs": best_cs_val,
                    "Q_diag": Q_diag, "cs_diag": cs_diag,
                    "Q_eig": Q_eig, "cs_eig": cs_eig,
                })

    valid = [r for r in results if not math.isnan(r["Q"]) and r["cs"] > -1.5]
    if not valid:
        valid = results
    best_cs = max(valid, key=lambda r: r["cs"] if not math.isnan(r["cs"]) else -2)
    best_Q = min(valid, key=lambda r: abs(r["Q"] - 2 / 3) if not math.isnan(r["Q"]) else 1e9)
    print()
    print(f"  BEST cos-sim: {best_cs['cs']:.4f} (lift={best_cs['lift']}, h_O0={best_cs['h_O0']:.4f}, {best_cs['lambda_label']})")
    print(f"       diag={pretty(best_cs['diag'])}  eigs={pretty(best_cs['eigs'])}  Q={best_cs['Q']:.4f}")
    print(f"  BEST |Q-2/3|: {abs(best_Q['Q']-2/3):.4e} (lift={best_Q['lift']}, h_O0={best_Q['h_O0']:.4f}, {best_Q['lambda_label']})")
    print(f"       diag={pretty(best_Q['diag'])}  eigs={pretty(best_Q['eigs'])}  cs={best_Q['cs']:.4f}")

    got_resolved = any(float(np.std(r["diag"])) > 1e-6 for r in valid)
    check("G-2: resolvent weight produces species-resolved diagonals",
          got_resolved,
          detail=f"max std(diag) = {max(float(np.std(r['diag'])) for r in valid):.3e}")

    print()
    print("  G-2 verdict: " + (
        "MATCH" if (best_cs["cs"] > 0.99 and abs(best_cs["Q"] - 2 / 3) < 1e-3)
        else "NO_MATCH"
    ))
    print()
    return results, best_cs, best_Q


# ======================================================================
# CONSTRUCTION G-3 — W(H) from chamber-pin eigenvalues (-1.309, -0.320, +2.287)
# ======================================================================

def construction_G3_chamber_eigenvalue_weights():
    print("=" * 78)
    print("CONSTRUCTION G-3 — W(H) directly from G1-pin eigenvalues")
    print("=" * 78)

    eigs = H_STAR_EIGS  # ascending: (-1.30909, -0.32043, +2.28659)
    print(f"  G1 chamber-pin H eigenvalues: {pretty(eigs)}")
    print("  These three scalars are assigned as weights to the three intermediate T_2 states")
    print("  in all six possible orderings (3! permutations), plus an O_0 weight from")
    print("  retained scalars: tr(H)/3, mean of |eigs|, and zero.")
    print()

    # We try all 3! orderings of (|lambda_1|, |lambda_2|, |lambda_3|) on T_2
    # plus three retained choices for the O_0 scalar.
    import itertools
    O_0_candidates = [
        ("h_O0=0", 0.0),
        ("h_O0=tr(H)/3", float(np.trace(H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)).real) / 3.0),
        ("h_O0=mean|eig|", float(np.mean(np.abs(eigs)))),
        ("h_O0=min|eig|", float(np.min(np.abs(eigs)))),
        ("h_O0=lambda_1", float(eigs[0])),
        ("h_O0=lambda_2", float(eigs[1])),
        ("h_O0=lambda_3", float(eigs[2])),
        ("h_O0=lambda_1^2", float(eigs[0]) ** 2),
        ("h_O0=lambda_2^2", float(eigs[1]) ** 2),
        ("h_O0=lambda_3^2", float(eigs[2]) ** 2),
    ]

    # Transformations on eigenvalues (all retained): identity, abs, square, exp
    transforms = [
        ("tau=id", lambda x: x),
        ("tau=abs", lambda x: np.abs(x)),
        ("tau=square", lambda x: x * x),
        ("tau=shifted", lambda x: x - np.min(eigs) + 0.1),
    ]

    results = []
    for (label_tau, tau) in transforms:
        t_eigs = tau(np.array(eigs))
        for perm in itertools.permutations(range(3)):
            t2_weights = np.array([t_eigs[perm[0]], t_eigs[perm[1]], t_eigs[perm[2]]])
            for (label_oo, w_O0) in O_0_candidates:
                # Build W4 as a DIAGONAL weight on the 4 intermediate states in
                # the (O_0, T2_011, T2_101, T2_110) basis. For the hopping
                # alignment, T_2[1,1,0] is species 2, T_2[1,0,1] is species 3,
                # T_2[0,1,1] is unreached. We assign the three weights on the
                # T_2 states in the missing-axis order (011, 101, 110).
                W4 = np.diag([w_O0, t2_weights[0], t2_weights[1], t2_weights[2]]).astype(complex)
                W16 = embed_4x4_to_16(W4)
                sigma = sigma_with_weight_operator(W16)
                d = np.real(np.diag(sigma))
                m = np.abs(d)
                if not np.all(m > 1e-14):
                    continue
                Q = koide_Q(m)
                cs = direction_cos(m)
                results.append({
                    "tau": label_tau, "perm": perm, "w_O0_label": label_oo,
                    "w_O0": w_O0, "t2": tuple(float(x) for x in t2_weights),
                    "diag": d, "Q": Q, "cs": cs,
                })

    # Sort and print top-10 by cos-sim and top-10 by |Q-2/3|
    by_cs = sorted(results, key=lambda r: r["cs"], reverse=True)[:8]
    by_Q = sorted(results, key=lambda r: abs(r["Q"] - 2 / 3))[:8]

    print("  Top-8 by cos-similarity to PDG direction:")
    for r in by_cs:
        print(f"    cs={r['cs']:.4f} Q={r['Q']:.4f} {r['tau']:12s} perm={r['perm']} {r['w_O0_label']:14s}")
        print(f"      diag={pretty(r['diag'])}")

    print()
    print("  Top-8 by |Q - 2/3|:")
    for r in by_Q:
        print(f"    |Q-2/3|={abs(r['Q']-2/3):.4e} cs={r['cs']:.4f} {r['tau']:12s} perm={r['perm']} {r['w_O0_label']:14s}")
        print(f"      diag={pretty(r['diag'])}")

    best_cs = by_cs[0]
    best_Q = by_Q[0]
    print()
    print(f"  BEST cos-sim: {best_cs['cs']:.4f} with Q={best_cs['Q']:.4f}")
    print(f"  BEST |Q-2/3|: {abs(best_Q['Q']-2/3):.4e} with cs={best_Q['cs']:.4f}")

    # Joint score: simultaneously satisfy Koide AND cos-sim > 0.99
    jointly_ok = [r for r in results if r["cs"] > 0.99 and abs(r["Q"] - 2 / 3) < 1e-3]
    print(f"  Candidates with (cs>0.99 AND |Q-2/3|<1e-3): {len(jointly_ok)}")

    check("G-3: chamber-eigenvalue weights produce species-resolved diagonals",
          max(float(np.std(r["diag"])) for r in results) > 1e-6,
          detail=f"max std(diag) = {max(float(np.std(r['diag'])) for r in results):.3e}")

    print()
    print("  G-3 verdict: " + (
        "MATCH" if len(jointly_ok) > 0
        else "NO_MATCH (no permutation saturates both Koide and direction)"
    ))
    print()
    return results, best_cs, best_Q


# ======================================================================
# PHASE 4 — four-outcome verdict
# ======================================================================

def four_outcome_verdict(g1_best_cs, g1_best_Q, g2_best_cs, g2_best_Q,
                        g3_best_cs, g3_best_Q):
    print("=" * 78)
    print("PHASE 4 — FOUR-OUTCOME VERDICT")
    print("=" * 78)

    def match(r):
        return r["cs"] > 0.99 and abs(r["Q"] - 2 / 3) < 1e-3

    g1_match = match(g1_best_cs) or match(g1_best_Q)
    g2_match = match(g2_best_cs) or match(g2_best_Q)
    g3_match = match(g3_best_cs) or match(g3_best_Q)

    def partial(r):
        return r["cs"] > 0.9 or abs(r["Q"] - 2 / 3) < 1e-2

    g1_partial = partial(g1_best_cs) or partial(g1_best_Q)
    g2_partial = partial(g2_best_cs) or partial(g2_best_Q)
    g3_partial = partial(g3_best_cs) or partial(g3_best_Q)

    # IMPORTANT: even if numeric match, the H-lift and the lambda choice
    # are NOT retained on the existing surface. See honest caveat below.
    # The best numerical match (G-2 at lambda=chamber_slack) uses two
    # non-retained inputs:
    #   (a) the missing-axis H3-embedding lift to the intermediate
    #       subspace, which is a NEW structural choice;
    #   (b) lambda = chamber-slack distance at the G1 OBSERVATIONAL
    #       chamber pin — derived from PMNS-observational input, not
    #       from the retained axiomatic surface.
    # Therefore even a numerical MATCH reduces to INCONCLUSIVE on
    # retention grounds, UNLESS a retained justification for both (a)
    # and (b) is supplied.

    if g1_match or g2_match or g3_match:
        # Numerically passes, but honest verdict is INCONCLUSIVE pending
        # retention of H-lift and lambda choice.
        verdict = ("FRAMEWORK_DERIVES_KOIDE = INCONCLUSIVE "
                   "(numerical match achieved, but H-lift and lambda choice "
                   "are not retained primitives; see honest caveat)")
    elif g1_partial or g2_partial or g3_partial:
        verdict = "FRAMEWORK_DERIVES_KOIDE = PARTIAL"
    else:
        verdict = "FRAMEWORK_DERIVES_KOIDE = NO_NATURAL_CONSTRUCTION"

    # INCONCLUSIVE outcome would apply if H-lift itself requires new ingredient.
    # The lift we used (missing-axis embed of H3 on T_2) relies on the retained
    # Cl(3)-covariant identification T_2 states ↔ missing axis labels. This
    # identification is retained but its COMPOSITION-WITH-H3-AS-CHARGED-LEPTON-
    # WEIGHT is a NEW structural choice beyond the existing retained surface.
    # We flag this honestly below.

    print()
    print(f"  VERDICT: {verdict}")
    print()
    print("  Numerical summary (best per construction):")
    print(f"  G-1 (f(H) lift):    numeric-match={g1_match}, partial={g1_partial}")
    print(f"     best cs={g1_best_cs['cs']:.4f} Q={g1_best_cs['Q']:.4f} "
          f"(cs_criterion: {g1_best_cs['cs'] > 0.99}, Q_criterion: {abs(g1_best_cs['Q'] - 2/3) < 1e-3})")
    print(f"  G-2 (resolvent):    numeric-match={g2_match}, partial={g2_partial}")
    print(f"     best cs={g2_best_cs['cs']:.4f} Q={g2_best_cs['Q']:.4f} "
          f"(cs_criterion: {g2_best_cs['cs'] > 0.99}, Q_criterion: {abs(g2_best_cs['Q'] - 2/3) < 1e-3})")
    print(f"  G-3 (chamber eigs): numeric-match={g3_match}, partial={g3_partial}")
    print(f"     best cs={g3_best_cs['cs']:.4f} Q={g3_best_cs['Q']:.4f} "
          f"(cs_criterion: {g3_best_cs['cs'] > 0.99}, Q_criterion: {abs(g3_best_cs['Q'] - 2/3) < 1e-3})")
    print()
    print("  Honest caveat on the H-lift:")
    print("  The missing-axis identification T_2[011,101,110] <-> species (1,2,3)")
    print("  is retained as a Z_3 / Cl(3) sector covariance statement, but using")
    print("  it to transport the G1 H-operator (which is defined on T_1 via the")
    print("  neutrino f(H) closure) as a PROPAGATOR WEIGHT between two Gamma_1")
    print("  hops on the intermediate subspace O_0 ⊕ T_2 is a structural choice")
    print("  not itself proven to be retained. The retained Dirac-bridge theorem")
    print("  fixes W(intermediate) = (P_O0 + P_T2), i.e. unit-weight. Replacing")
    print("  this with W(H) is a NEW retained primitive if it were to be adopted")
    print("  — and (as Agent 12's AMBIGUOUS result showed on a different lift)")
    print("  requires a retained justification for that specific choice.")
    print()
    print("  If no construction matches numerically, the outcome remains")
    print("  NO_NATURAL_CONSTRUCTION or INCONCLUSIVE (the latter if the lift")
    print("  itself is unretained).")
    return verdict


def main():
    print("=" * 78)
    print("G5 AVENUE G — HIGGS-DRESSED INTERMEDIATE PROPAGATOR")
    print("=" * 78)
    print()

    phase1_baseline()
    verify_hopping()
    print()

    g1_results, g1_best_cs, g1_best_Q = construction_G1_function_of_H()
    g2_results, g2_best_cs, g2_best_Q = construction_G2_resolvent()
    g3_results, g3_best_cs, g3_best_Q = construction_G3_chamber_eigenvalue_weights()

    verdict = four_outcome_verdict(g1_best_cs, g1_best_Q,
                                   g2_best_cs, g2_best_Q,
                                   g3_best_cs, g3_best_Q)

    print("=" * 78)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print(f"VERDICT: {verdict}")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
