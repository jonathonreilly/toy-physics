#!/usr/bin/env python3
"""Pattern A narrow runner for
`GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_ONE_WORD_PACKET_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone finite-linear-algebra identity that, given any
finite dominant-weight box B_N = {(p,q) : 0 <= p,q <= N}, any abstract
strictly-positive conjugation-symmetric diagonal D, and any pair of
nonnegative integer matrices (N_f, N_fbar) related by the swap involution
S as N_fbar = S N_f S, the assembled finite matrix

    M  =  N_f + N_fbar,
    T  =  D M D M^T D,

satisfies:

  (T1)  T_{a,b} >= 0   for all a, b in B_N  (entry-wise nonnegativity);
  (T2)  S T = T S      (conjugation-swap symmetry);
  (T3)  r := T e_(0,0) satisfies r_a >= 0 for all a, with
        r_(0,0) = c_(0,0)^2 * sum_x M_{(0,0), x}^2 * c_x  >  0
        whenever some M_{(0,0), x} > 0; and S r = r.

This is class-A pure finite linear algebra. No Wilson environment
slicing, no `beta = 6` boundary-character identity, no Perron readout,
no physical spatial-environment claim is consumed.

The runner verifies the abstract narrow theorem by:
  (i)  exact integer / abstract-symbolic algebraic identities for S, M,
       D commutation, and swap relations;
  (ii) two instantiations:
       - default reference: c_(p,q) = c_(p,q)(beta=6) / (d_(p,q) c_(0,0)(6))
         from the parent runner's Schur-Weyl Bessel-determinant sum at
         MODE_MAX = 80 on B_4;
       - abstract: c_(p,q) = arbitrary positive symmetric diagonal
         (negative control: the algebra closes for any such D).
  (iii) necessity-of-conjugation-symmetry counterexample: when D is
       perturbed off the symmetric subspace, (T2) fails.

Companion role: this is a Pattern A new narrow claim row carving out
the one-finite-tensor-word packet of
`gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note`
(claim_type=bounded_theorem). The narrow theorem isolates the
finite-linear-algebra fact from any physical Wilson spatial-environment
identification.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from scipy.special import iv

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0

NMAX = 4
BETA = 6.0
ARG = BETA / 3.0
MODE_MAX = 80


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Pattern A narrow theorem: one-finite-tensor-word packet (finite linear algebra)")
# Statement: D positive symmetric diagonal + (N_f, N_fbar) nonnegative
# integer matrices with N_fbar = S N_f S ==> T = D M D M^T D satisfies
# (T1) entrywise nonneg, (T2) S T = T S, (T3) r = T e_0 nonneg with
# strict positivity of trivial-channel entry whenever M has a nonzero
# (0,0)-row entry.
# Pure finite linear algebra. No Wilson environment slicing claim.
# ============================================================================


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def highest_weight_triple(p: int, q: int) -> list[int]:
    return [p + q, q, 0]


def coefficient_matrix(mode: int, lam: list[int]) -> np.ndarray:
    return np.array(
        [[iv(mode + lam[j] + i - j, ARG) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def wilson_character_coefficient(p: int, q: int) -> float:
    lam = highest_weight_triple(p, q)
    total = 0.0
    for mode in range(-MODE_MAX, MODE_MAX + 1):
        total += float(np.linalg.det(coefficient_matrix(mode, lam)))
    return total


def weights_box(nmax: int) -> list[tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


def build_pieri_matrices(nmax: int) -> tuple[np.ndarray, np.ndarray, list[tuple[int, int]], dict[tuple[int, int], int]]:
    """Build SU(3) Pieri multiplicity matrices on B_nmax.

    Fundamental fusion lambda x (1,0):  (p,q) -> (p+1,q), (p-1,q+1), (p,q-1)
    Antifund. fusion lambda x (0,1):    (p,q) -> (p,q+1), (p+1,q-1), (p-1,q)
    Matrix convention: N_f[target, source] = multiplicity coefficient,
    so M @ e_source picks out the targets reachable from source.
    """
    weights = weights_box(nmax)
    index = {w: i for i, w in enumerate(weights)}
    nf = np.zeros((len(weights), len(weights)), dtype=int)
    nfb = np.zeros((len(weights), len(weights)), dtype=int)
    for p, q in weights:
        i = index[(p, q)]
        for a, b in [(p + 1, q), (p - 1, q + 1), (p, q - 1)]:
            if a >= 0 and b >= 0 and (a, b) in index:
                nf[index[(a, b)], i] += 1
        for a, b in [(p, q + 1), (p + 1, q - 1), (p - 1, q)]:
            if a >= 0 and b >= 0 and (a, b) in index:
                nfb[index[(a, b)], i] += 1
    return nf, nfb, weights, index


def swap_matrix(weights: list[tuple[int, int]], index: dict[tuple[int, int], int]) -> np.ndarray:
    s = np.zeros((len(weights), len(weights)), dtype=int)
    for w in weights:
        s[index[(w[1], w[0])], index[w]] = 1
    return s


# ----------------------------------------------------------------------------
section("Part 1: abstract algebraic identities for S (conjugation-swap involution)")
# ----------------------------------------------------------------------------
nf, nfb, weights, index = build_pieri_matrices(NMAX)
S = swap_matrix(weights, index)
N = len(weights)

check(
    "S = S^T (swap is symmetric as a permutation matrix)",
    np.array_equal(S, S.T),
    detail=f"|B_N| = {N}; box dim = {NMAX}",
)
check(
    "S^2 = I (swap is an involution)",
    np.array_equal(S @ S, np.eye(N, dtype=int)),
    detail="S permutes (p,q) <-> (q,p)",
)
e0 = np.zeros(N, dtype=float)
e0[index[(0, 0)]] = 1.0
check(
    "S e_(0,0) = e_(0,0) (the trivial weight is self-conjugate)",
    np.array_equal(S @ e0, e0),
    detail="(0,0) -> (0,0) under (p,q) -> (q,p)",
)


# ----------------------------------------------------------------------------
section("Part 2: swap relation N_fbar = S N_f S for the SU(3) Pieri instance")
# ----------------------------------------------------------------------------
check(
    "S N_f S = N_fbar exactly (integer equality)",
    np.array_equal(S @ nf @ S, nfb),
    detail="Pieri rules under (p,q) <-> (q,p) exchange fund. <-> antifund.",
)
check(
    "S N_fbar S = N_f exactly (integer equality)",
    np.array_equal(S @ nfb @ S, nf),
    detail="follows from S^2 = I",
)
check(
    "N_f entries in {0, 1} (SU(3) Pieri multiplicities are 0 or 1)",
    set(nf.flatten().tolist()).issubset({0, 1}),
    detail=f"distinct entries in N_f: {sorted(set(nf.flatten().tolist()))}",
)
check(
    "N_fbar entries in {0, 1} (SU(3) Pieri multiplicities are 0 or 1)",
    set(nfb.flatten().tolist()).issubset({0, 1}),
    detail=f"distinct entries in N_fbar: {sorted(set(nfb.flatten().tolist()))}",
)


# ----------------------------------------------------------------------------
section("Part 3: reference-instance diagonal D from Wilson character coefficients at beta=6")
# ----------------------------------------------------------------------------
coeffs = np.array([wilson_character_coefficient(p, q) for p, q in weights], dtype=float)
dims = np.array([dim_su3(p, q) for p, q in weights], dtype=float)
c00 = coeffs[index[(0, 0)]]
c_ref = coeffs / (dims * c00)  # normalized c_(p,q)(6) / (d_(p,q) c_(0,0)(6))

print(f"\n  Wilson character coefficients (beta = {BETA}, MODE_MAX = {MODE_MAX}):")
for rep in [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2), (2, 1), (1, 2)]:
    i = index[rep]
    print(f"    c{rep!s:<7}  =  {c_ref[i]:.12f}   dim = {int(dims[i])}")

check(
    "reference-instance c_(p,q) is strictly positive on B_N",
    float(np.min(c_ref)) > 1.0e-12,
    detail=f"min c = {float(np.min(c_ref)):.6e}",
)
swap_idx = np.array([index[(q, p)] for (p, q) in weights])
sym_err = float(np.max(np.abs(c_ref - c_ref[swap_idx])))
check(
    "reference-instance c_(p,q) = c_(q,p) (conjugation symmetry)",
    sym_err < 1.0e-12,
    detail=f"max |c_(p,q) - c_(q,p)| = {sym_err:.3e}",
)


# ----------------------------------------------------------------------------
section("Part 4: (T1) entry-wise nonnegativity of T = D M D M^T D")
# ----------------------------------------------------------------------------
def assemble_T(c_diag: np.ndarray) -> np.ndarray:
    D = np.diag(c_diag)
    M = nf + nfb
    return D @ M @ D @ M.T @ D


T_ref = assemble_T(c_ref)
t_min = float(np.min(T_ref))
check(
    "T is entry-wise nonnegative on the reference (Wilson) instance",
    t_min >= 0.0,
    detail=f"min T_{{a,b}} = {t_min:.6e}",
)

# Abstract-instance: arbitrary positive symmetric diagonal (NOT from Wilson)
rng = np.random.default_rng(20260510)
c_abstract = 0.5 + rng.random(N)
c_abstract = 0.5 * (c_abstract + c_abstract[swap_idx])  # symmetrize
T_abstract = assemble_T(c_abstract)
check(
    "T is entry-wise nonnegative on an arbitrary positive symmetric diagonal (abstract instance)",
    float(np.min(T_abstract)) >= 0.0,
    detail=f"min T_{{a,b}} = {float(np.min(T_abstract)):.6e}; confirms (T1) is a pure-algebra fact",
)


# ----------------------------------------------------------------------------
section("Part 5: (T2) conjugation-swap symmetry S T = T S")
# ----------------------------------------------------------------------------
swap_err_ref = float(np.max(np.abs(S @ T_ref - T_ref @ S)))
check(
    "S T = T S on the reference (Wilson) instance",
    swap_err_ref < 1.0e-12,
    detail=f"max |S T - T S| = {swap_err_ref:.3e}",
)
swap_err_abstract = float(np.max(np.abs(S @ T_abstract - T_abstract @ S)))
check(
    "S T = T S on the abstract positive symmetric instance",
    swap_err_abstract < 1.0e-12,
    detail=f"max |S T - T S| = {swap_err_abstract:.3e}; confirms (T2) holds whenever S D = D S",
)


# ----------------------------------------------------------------------------
section("Part 6: (T3) nonnegative trivial readout, strictly positive trivial-channel amplitude")
# ----------------------------------------------------------------------------
r_ref = T_ref @ e0
check(
    "r = T e_(0,0) is entry-wise nonnegative (reference instance)",
    float(np.min(r_ref)) >= 0.0,
    detail=f"min r_a = {float(np.min(r_ref)):.6e}",
)
# Trivial-channel formula: r_(0,0) = c_(0,0)^2 * sum_x M_{(0,0), x}^2 * c_x
M_total = nf + nfb
trivial_row = M_total[index[(0, 0)], :]
predicted_r00 = c_ref[index[(0, 0)]] ** 2 * float(np.sum(trivial_row.astype(float) ** 2 * c_ref))
actual_r00 = r_ref[index[(0, 0)]]
check(
    "r_(0,0) = c_(0,0)^2 * sum_x M_{(0,0),x}^2 * c_x (closed-form trivial-channel formula)",
    abs(predicted_r00 - actual_r00) < 1.0e-12,
    detail=f"predicted = {predicted_r00:.12f}, actual = {actual_r00:.12f}",
)
check(
    "r_(0,0) > 0 strictly (some M_{(0,0), x} > 0 on the reference instance)",
    actual_r00 > 0.0,
    detail=f"r_(0,0) = c_(0,0)^2 * (c_(1,0) + c_(0,1)) = {actual_r00:.12f}",
)
swap_err_r = float(np.max(np.abs(S @ r_ref - r_ref)))
check(
    "S r = r (the trivial-channel readout is conjugation-swap invariant)",
    swap_err_r < 1.0e-12,
    detail=f"max |S r - r| = {swap_err_r:.3e}",
)

r_abstract = T_abstract @ e0
check(
    "(T3) holds on the abstract positive symmetric instance",
    float(np.min(r_abstract)) >= 0.0 and r_abstract[index[(0, 0)]] > 0.0,
    detail=f"min r = {float(np.min(r_abstract)):.6e}, r_(0,0) = {r_abstract[index[(0, 0)]]:.6e}",
)


# ----------------------------------------------------------------------------
section("Part 7: necessity of conjugation symmetry on D (negative control)")
# ----------------------------------------------------------------------------
# Deliberately break conjugation symmetry on D and confirm (T2) fails.
c_broken = c_ref.copy()
# Perturb (1,0) without perturbing (0,1) — breaks c_(1,0) = c_(0,1)
i10 = index[(1, 0)]
c_broken[i10] = c_broken[i10] * 1.10
T_broken = assemble_T(c_broken)
swap_err_broken = float(np.max(np.abs(S @ T_broken - T_broken @ S)))
check(
    "when c_(1,0) != c_(0,1), (T2) S T = T S FAILS (confirms conjugation-symmetry hypothesis is load-bearing)",
    swap_err_broken > 1.0e-6,
    detail=f"max |S T - T S| with broken symmetry = {swap_err_broken:.6e}; non-trivial deviation confirms load-bearing role",
)


# ----------------------------------------------------------------------------
section("Part 8: scope discipline — narrow theorem does NOT claim spatial-environment identification")
# ----------------------------------------------------------------------------
# Diagnostic print only. The narrow theorem treats (D, N_f, N_fbar) as
# abstract algebraic ingredients on a finite index set. It does not claim
# T equals any physical Wilson spatial-environment slice transfer
# operator. The parent bounded-theorem note states that structural
# identification; this narrow note is silent on it.
print("""
  Scope discipline (diagnostic):
  - This narrow theorem proves a finite-linear-algebra implication
    (T1) + (T2) + (T3) on abstract (D, N_f, N_fbar) ingredients.
  - It does NOT claim that the assembled matrix T equals the
    physical unmarked spatial-environment Wilson slice transfer.
  - It does NOT evaluate z_(p,q)^env(beta) or any Perron state.
  - The reference-instance Wilson coefficients are used only to
    confirm one explicit (D, N_f, N_fbar) satisfies the abstract
    hypotheses; the abstract test in Parts 4, 5, 6 confirms the
    conclusions do not depend on this specific instance.
  - The parent bounded-theorem note continues to carry the
    structural Wilson identification claim and its open
    positive-theorem target (explicit beta=6 Perron solve,
    multi-tensor-word generalization, full untruncated construction).
""")


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let N be a nonnegative integer and B_N = {(p,q) : 0 <= p,q <= N}.
    Let S be the permutation matrix S_{(q,p), (p,q)} = 1.
    Let D = diag(c_(p,q)) be a strictly positive diagonal with
        c_(p,q) = c_(q,p)   for all (p,q) in B_N.
    Let (N_f, N_fbar) be nonnegative integer |B_N| x |B_N| matrices with
        N_fbar = S N_f S.
    Set M = N_f + N_fbar  and  T = D M D M^T D.

  CONCLUSION:
    (T1) entry-wise:  T_{a,b} >= 0  for all a, b in B_N.
    (T2) symmetry:    S T = T S.
    (T3) readout:     r := T e_(0,0) satisfies r_a >= 0 for all a, with
                      r_(0,0) = c_(0,0)^2 * sum_x M_{(0,0),x}^2 c_x  >  0
                      whenever some M_{(0,0), x} > 0;  and  S r = r.

  Runner evidence class:
    (A) — pure finite linear algebra on abstract positive symmetric
    diagonals and abstract nonnegative integer matrices on a finite
    index set. No Wilson environment slicing, no beta=6 boundary
    character identity, no Perron readout, no physical spatial-
    environment claim.

  This narrow theorem isolates the one-finite-tensor-word packet that
  the parent bounded-theorem runner actually checks, from the
  parent's structural Wilson spatial-environment identification.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
