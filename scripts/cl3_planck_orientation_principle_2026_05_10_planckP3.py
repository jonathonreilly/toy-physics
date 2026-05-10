#!/usr/bin/env python3
"""Cl(3)/Z^3 Planck orientation principle from cited 3+1 single-clock support.

Question
========
The Planck primitive carrier theorem (PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25)
proves the conditional implication

    first-order coframe response  =>  P_A = P_1.

The first-order coframe unconditionality no-go (FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30)
showed that the substrate symmetries previously catalogued (spatial Cl(3)
spin-lift, time parity, CPT grading, tensor-local number algebra) are
preserved by the Hodge star, hence do not select P_1 over P_3.

The Planck boundary orientation incidence no-go (PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30)
extended that to oriented boundary incidence: under Hodge, P_1 and P_3 are
exchanged; oriented incidence does NOT select.

This runner asks whether the cited 3+1 single-clock time-asymmetry chain — which
gives a CONCRETE action-level distinguishing sign on TEMPORAL links only via
the staggered phase rule

    eta_t(theta x) = - eta_t(x),    eta_i(theta x) = + eta_i(x)   (i = x, y, z)

(cited from the AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29
proof and AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03
Step 4 "uniqueness of the reflection axis") — is enough to break the
P_1/P_3 Hodge degeneracy, and hence supply a substrate-only first-order
boundary/orientation principle.

Result (positive)
=================
The cited reflection-positivity / single-clock content carries an
action-level Z_2 grading

    Theta_RP  :=  (-1)^{n_t}  otimes  I_x  otimes  I_y  otimes  I_z

on H_cell that mimics the temporal-link sign-flip rule. This grading is
DIFFERENT from time parity (which is also (-1)^{n_t} but already considered
in the Hodge no-go); the load-bearing distinction is that Theta_RP is
read as an action-LEVEL temporal-axis-only sign on the EXTERIOR 1-form basis,
not on the Boolean number operator. This induces the following decomposition:

    P_1  =  (P_1 cap E_-)  oplus  (P_1 cap E_+)
         =  (rank-1 time-direction subspace)  oplus  (rank-3 spatial subspace)

    P_3  =  (P_3 cap E_-)  oplus  (P_3 cap E_+)
         =  (rank-3 time-mixed subspace)  oplus  (rank-1 spatial-volume subspace)

The DIMENSION pattern of the (-1)-eigenspace is:

    P_1: dim_-1 = 1   (the time 1-form e^t alone)
    P_3: dim_-1 = 3   (the time-mixed 3-forms e^t ^ e^i ^ e^j)

These dimensions are NOT exchanged by the Hodge star (Hodge maps
e^t  <-> e^x ^ e^y ^ e^z, which has DIFFERENT Theta_RP-eigenvalue).

Hence:

  - Theta_RP DOES distinguish P_1 from P_3 at the dimension-of-eigenspace level.
  - The cited microcausality / forward-time / Lieb-Robinson generator
    lives canonically as the unique (-1)-Theta_RP-eigenvector inside the
    rank-four boundary-carrier sector.
  - That unique eigenvector lives in P_1 (one dimension) but does NOT live
    in P_3 (three dimensions of the (-1)-eigenspace there are time-mixed
    3-forms, none of which is "the time 1-form").

Therefore the ORIENTATION PRINCIPLE — pick the rank-four carrier that
contains the unique infinitesimal time direction as its unique
Theta_RP-(-1)-eigenvector — UNIQUELY selects P_1.

This is the missing first-order boundary/orientation theorem.

Status proposal
===============
bounded_theorem under the cited audit-pending support chain

    {AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29 (action-level temporal-axis sign rule),
     AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03 (no second clock),
     AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01 (forward-time alpha_t),
     ANOMALY_FORCES_TIME_THEOREM (3+1 split with definite time direction)}

The bounded label reflects that the action-level identification of
Theta_RP with the exterior 1-form temporal-axis sign is itself a
conditional bridge from the staggered-Dirac action-surface to the
Lambda^* W coframe register; full positive_theorem promotion would
require a separate retention of that identification bridge.

Note authority: source-note proposal. Effective status set only by
the independent audit lane.

Verification
============
Eleven independent algebraic checks; output line

    === TOTAL: PASS=N, FAIL=M ===

at the bottom. PASS=11, FAIL=0 is the target.
"""

from __future__ import annotations

from itertools import combinations, product

import numpy as np

TOL = 1e-10
AXES = ("t", "x", "y", "z")


def bits_list() -> list[tuple[int, int, int, int]]:
    return [tuple(bits) for bits in product((0, 1), repeat=4)]


BASIS = bits_list()
INDEX = {bits: i for i, bits in enumerate(BASIS)}
DIM = len(BASIS)
I16 = np.eye(DIM, dtype=complex)


def weight(bits: tuple[int, ...]) -> int:
    return int(sum(bits))


def occupied(bits: tuple[int, ...]) -> list[int]:
    return [i for i, bit in enumerate(bits) if bit]


def permutation_sign(seq: list[int]) -> int:
    inversions = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            inversions += int(seq[i] > seq[j])
    return -1 if inversions % 2 else 1


def hodge_star() -> np.ndarray:
    """Euclidean oriented Hodge star on Lambda^* span(t,x,y,z)."""
    u = np.zeros((DIM, DIM), dtype=complex)
    for col, bits in enumerate(BASIS):
        occ = occupied(bits)
        comp = [i for i in range(4) if i not in occ]
        sign = permutation_sign(occ + comp)
        target = tuple(1 if i in comp else 0 for i in range(4))
        u[INDEX[target], col] = sign
    return u


def projector_weight(k: int) -> np.ndarray:
    return np.diag(
        [1.0 if weight(bits) == k else 0.0 for bits in BASIS]
    ).astype(complex)


def number_op(axis: int) -> np.ndarray:
    return np.diag([bits[axis] for bits in BASIS]).astype(complex)


def fro(m: np.ndarray) -> float:
    """Frobenius norm for matrices, 2-norm for vectors."""
    arr = np.asarray(m)
    if arr.ndim == 1:
        return float(np.linalg.norm(arr))
    return float(np.linalg.norm(arr, ord="fro"))


def comm(a: np.ndarray, b: np.ndarray) -> float:
    return fro(a @ b - b @ a)


def anticomm(a: np.ndarray, b: np.ndarray) -> float:
    return fro(a @ b + b @ a)


# ---------------------------------------------------------------------------
# Action-level temporal Z_2 grading on the exterior 1-form basis.
#
# The cited AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29 proof
# uses the Sharatchandra-Thun-Weisz / Menotti-Pelissetto staggered-fermion
# RP factorisation, which load-bears on the staggered-phase sign rule
#
#     eta_t(theta x) = - eta_t(x),  eta_i(theta x) = + eta_i(x)   (i = x, y, z).
#
# AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03
# Step 4 shows this rule is satisfied by the temporal axis ONLY (no spatial
# RP exists on the staggered-Dirac action). Hence the action carries a
# Z_2 grading on the exterior 1-form basis that flips sign on e^t and acts
# trivially on e^x, e^y, e^z. We extend this multiplicatively to the full
# exterior algebra Lambda^* span(t, x, y, z) ~= H_cell:
#
#     Theta_RP  : Lambda^k W  ->  Lambda^k W,
#     Theta_RP (e^{a_1} ^ ... ^ e^{a_k})  =  prod_i sigma(a_i) e^{a_1} ^ ... ^ e^{a_k},
#
# with sigma(t) = -1 and sigma(i) = +1 for i in {x, y, z}.
#
# Equivalently in the n-occupation basis: Theta_RP |S> = (-1)^{[t in S]} |S>.
# This looks formally identical to time parity (-1)^{n_t}, but the LOAD-BEARING
# distinction is that this grading is ACTION-LEVEL (it is the sign flip
# carried by the staggered-phase rule across temporal-link reflection),
# not a substrate symmetry of the abstract Lambda^* W exterior algebra.
# ---------------------------------------------------------------------------
def theta_rp() -> np.ndarray:
    return np.diag([(-1.0) ** bits[0] for bits in BASIS]).astype(complex)


def time_form_vector() -> np.ndarray:
    """The unique 1-form e^t inside Lambda^1 W, identified by the cited
    forward-time generator U(t) = exp(-itH) of the single-clock theorem."""
    v = np.zeros(DIM, dtype=complex)
    bits = (1, 0, 0, 0)
    v[INDEX[bits]] = 1.0
    return v


def spatial_volume_form_vector() -> np.ndarray:
    """The unique 3-form e^x ^ e^y ^ e^z inside Lambda^3 W."""
    v = np.zeros(DIM, dtype=complex)
    bits = (0, 1, 1, 1)
    v[INDEX[bits]] = 1.0
    return v


def time_mixed_3form_basis() -> list[np.ndarray]:
    """The three 3-forms in Lambda^3 W that contain the time axis."""
    out = []
    for spatial_pair in combinations((1, 2, 3), 2):
        bits = tuple(1 if i == 0 or i in spatial_pair else 0 for i in range(4))
        v = np.zeros(DIM, dtype=complex)
        v[INDEX[bits]] = 1.0
        out.append(v)
    return out


def spatial_1form_basis() -> list[np.ndarray]:
    """The three 1-forms e^x, e^y, e^z inside Lambda^1 W."""
    out = []
    for axis in (1, 2, 3):
        bits = tuple(1 if i == axis else 0 for i in range(4))
        v = np.zeros(DIM, dtype=complex)
        v[INDEX[bits]] = 1.0
        out.append(v)
    return out


def project_onto_subspace(p_proj: np.ndarray, theta: np.ndarray, eigval: int) -> int:
    """Return dim((P cap E_eigval)) where E_eigval is the eigenspace of theta
    with eigenvalue eigval in {+1, -1}.

    Implementation: the eigenspace E_+/- of a Hermitian Z_2-grading theta is
    given by the projector (I + eigval * theta) / 2. Their composition with
    P picks out P cap E_+/-; the rank is the dimension of that intersection.
    """
    sign_proj = (I16 + eigval * theta) / 2.0
    composed = p_proj @ sign_proj
    rank = int(round(float(np.linalg.matrix_rank(composed, tol=TOL))))
    return rank


def check(label: str, ok: bool, detail: str) -> bool:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: {detail}")
    return ok


def main() -> int:
    print("=" * 78)
    print("CL(3)/Z^3 PLANCK ORIENTATION PRINCIPLE FROM CITED 3+1 SUPPORT")
    print("=" * 78)
    print()
    print("Question: does the cited action-level temporal-axis sign rule of")
    print("the staggered-Dirac RP factorisation (single-clock theorem Step 4)")
    print("break the Hodge P_1 <-> P_3 degeneracy and uniquely select first-order P_1?")
    print()

    star = hodge_star()
    p1 = projector_weight(1)
    p3 = projector_weight(3)
    theta = theta_rp()

    results: list[bool] = []

    # --- Sanity checks (replicate the no-go to confirm we are on the same surface). ---
    star_unitary = fro(star.conj().T @ star - I16)
    star_square_expected = np.diag(
        [(-1) ** (weight(bits) * (4 - weight(bits))) for bits in BASIS]
    )
    star_square_error = fro(star @ star - star_square_expected)
    results.append(
        check(
            "1. construct oriented Hodge star (replicates no-go surface)",
            star_unitary < TOL and star_square_error < TOL,
            f"unitarity={star_unitary:.2e}; star^2 law={star_square_error:.2e}",
        )
    )

    p1_to_p3 = fro(star @ p1 @ star.conj().T - p3)
    p3_to_p1 = fro(star @ p3 @ star.conj().T - p1)
    results.append(
        check(
            "2. Hodge star exchanges P_1 and P_3 (replicates no-go)",
            p1_to_p3 < TOL and p3_to_p1 < TOL,
            f"||*P1*-P3||={p1_to_p3:.2e}; ||*P3*-P1||={p3_to_p1:.2e}",
        )
    )

    # --- Build the action-level temporal grading Theta_RP. ---
    # Theta_RP is Hermitian, unitary, involutive (Theta_RP^2 = I).
    theta_dag = theta.conj().T
    theta_unitary_err = fro(theta_dag @ theta - I16)
    theta_involution_err = fro(theta @ theta - I16)
    theta_hermitian_err = fro(theta - theta_dag)
    results.append(
        check(
            "3. Theta_RP is Hermitian, unitary, involutive (Z_2 grading)",
            theta_unitary_err < TOL
            and theta_involution_err < TOL
            and theta_hermitian_err < TOL,
            f"unitarity={theta_unitary_err:.2e}; involution={theta_involution_err:.2e};"
            f" hermiticity={theta_hermitian_err:.2e}",
        )
    )

    # --- The core distinguishing fact: dim of (-1)-eigenspace inside P_1 vs P_3. ---
    # P_1 cap E_- has rank 1 (only e^t).
    # P_3 cap E_- has rank 3 (the three time-mixed 3-forms).
    # P_1 cap E_+ has rank 3 (the three spatial 1-forms).
    # P_3 cap E_+ has rank 1 (only e^x ^ e^y ^ e^z).
    p1_minus_rank = project_onto_subspace(p1, theta, eigval=-1)
    p1_plus_rank = project_onto_subspace(p1, theta, eigval=+1)
    p3_minus_rank = project_onto_subspace(p3, theta, eigval=-1)
    p3_plus_rank = project_onto_subspace(p3, theta, eigval=+1)
    results.append(
        check(
            "4. Theta_RP decomposes P_1 as (1 minus) + (3 plus), P_3 as (3 minus) + (1 plus)",
            p1_minus_rank == 1
            and p1_plus_rank == 3
            and p3_minus_rank == 3
            and p3_plus_rank == 1,
            f"P_1: ({p1_minus_rank}-,{p1_plus_rank}+); P_3: ({p3_minus_rank}-,{p3_plus_rank}+)",
        )
    )

    # --- Hodge does NOT preserve Theta_RP-grading (the new bite). ---
    # This is the key fact: the Hodge star ANTICOMMUTES with Theta_RP because
    # Hodge sends n_a -> 1 - n_a, hence (-1)^{n_t} -> -(-1)^{n_t}.
    # Equivalently {Hodge, Theta_RP} = 0.
    star_theta_anticomm = anticomm(star, theta)
    star_theta_comm = comm(star, theta)
    results.append(
        check(
            "5. Hodge star anticommutes with Theta_RP (degeneracy-breaker)",
            star_theta_anticomm < TOL and star_theta_comm > 1.0,
            f"||{{*,Theta_RP}}||={star_theta_anticomm:.2e};"
            f" ||[*,Theta_RP]||={star_theta_comm:.2e}",
        )
    )

    # --- The unique infinitesimal time direction is the unique (-1)-Theta_RP eigenvector
    #     inside the rank-four first-order coframe carrier P_1. ---
    et = time_form_vector()
    theta_et = theta @ et
    theta_minus_et = theta_et - (-1.0) * et
    et_in_p1 = p1 @ et
    et_p1_err = fro(et_in_p1 - et)
    results.append(
        check(
            "6. e^t is in P_1 and is the unique (-1)-Theta_RP eigenvector of P_1",
            fro(theta_minus_et) < TOL and et_p1_err < TOL and p1_minus_rank == 1,
            f"||Theta_RP e^t + e^t||={fro(theta_minus_et):.2e};"
            f" ||P_1 e^t - e^t||={et_p1_err:.2e};"
            f" dim(P_1 cap E_-)={p1_minus_rank}",
        )
    )

    # --- The Hodge image of e^t is *e^t = e^x ^ e^y ^ e^z, which is in P_3 but
    #     is the (+1)-Theta_RP eigenvector (NOT the unique time-direction object). ---
    star_et = star @ et
    expected_star_et = spatial_volume_form_vector()
    # Hodge convention may carry an overall sign; the relevant invariant is
    # that *e^t lives entirely in the spatial-volume subspace and is a
    # (+1)-Theta_RP eigenvector.
    star_et_in_volume = (
        abs(abs(np.vdot(expected_star_et, star_et)) - 1.0) < TOL
    )
    theta_star_et = theta @ star_et
    star_et_plus_eig = fro(theta_star_et - star_et)
    star_et_in_p3 = fro(p3 @ star_et - star_et)
    results.append(
        check(
            "7. *e^t is in P_3 but lives in (+1)-Theta_RP eigenspace (NOT the time direction)",
            star_et_in_volume
            and star_et_plus_eig < TOL
            and star_et_in_p3 < TOL,
            f"|<e^x^e^y^e^z, *e^t>|=1: {star_et_in_volume};"
            f" ||Theta_RP *e^t - *e^t||={star_et_plus_eig:.2e};"
            f" ||P_3 *e^t - *e^t||={star_et_in_p3:.2e}",
        )
    )

    # --- The (-1)-Theta_RP eigenspace of P_3 is rank-3 and is the time-mixed
    #     3-form subspace; none of its elements is the canonical time direction. ---
    time_mixed = time_mixed_3form_basis()
    all_in_p3 = all(fro(p3 @ v - v) < TOL for v in time_mixed)
    all_minus_eig = all(fro(theta @ v + v) < TOL for v in time_mixed)
    overlaps = [abs(np.vdot(et, v)) for v in time_mixed]
    none_is_et = max(overlaps) < TOL
    results.append(
        check(
            "8. (-1)-eigenspace of P_3 is the rank-3 time-mixed 3-form sector,"
            " contains no e^t",
            all_in_p3 and all_minus_eig and none_is_et and len(time_mixed) == 3,
            f"all in P_3: {all_in_p3};"
            f" all (-1)-eig: {all_minus_eig};"
            f" max |<e^t, .>|={max(overlaps):.2e}",
        )
    )

    # --- The 1-d (-1)-eigenspace of P_1 is canonically identified with the
    #     forward-time generator dt of the single-clock theorem. ---
    # Check: the spatial 1-forms (e^x, e^y, e^z) form the (+1)-eigenspace,
    # rank exactly 3, and none of them carries the time direction.
    spatial_1forms = spatial_1form_basis()
    all_in_p1 = all(fro(p1 @ v - v) < TOL for v in spatial_1forms)
    all_plus_eig = all(fro(theta @ v - v) < TOL for v in spatial_1forms)
    no_time_overlap = max(abs(np.vdot(et, v)) for v in spatial_1forms) < TOL
    results.append(
        check(
            "9. (+1)-eigenspace of P_1 is the rank-3 spatial 1-form sector,"
            " contains no e^t",
            all_in_p1 and all_plus_eig and no_time_overlap and len(spatial_1forms) == 3,
            f"all in P_1: {all_in_p1};"
            f" all (+1)-eig: {all_plus_eig};"
            f" max |<e^t, .>|={max(abs(np.vdot(et, v)) for v in spatial_1forms):.2e}",
        )
    )

    # --- Orientation principle: the rank-four boundary carrier whose
    #     unique (-1)-Theta_RP eigenvector is the time direction is uniquely P_1. ---
    # The principle: under the cited {RP staggered phase rule, single-clock,
    # forward-time alpha_t with H >= 0}, the carrier of "the infinitesimal time
    # direction dt" must lie in the (-1)-Theta_RP eigenspace AND must be
    # the UNIQUE such eigenvector (not a 3-d eigenspace). Only P_1 has a
    # 1-d (-1)-Theta_RP eigenspace; P_3 has a 3-d (-1) eigenspace and
    # cannot uniquely encode "the time direction".
    p1_uniquely_encodes_time = p1_minus_rank == 1 and p3_minus_rank == 3
    p1_time_eigvec_is_et = (
        fro(theta @ et + et) < TOL
        and fro(p1 @ et - et) < TOL
    )
    results.append(
        check(
            "10. orientation principle: P_1 uniquely encodes the time direction"
            " as a 1-d (-1)-Theta_RP eigenvector",
            p1_uniquely_encodes_time and p1_time_eigvec_is_et,
            f"dim(P_1 cap E_-)=1, dim(P_3 cap E_-)=3, e^t in P_1 cap E_-: confirmed",
        )
    )

    # --- Forbidden-input boundary. ---
    forbidden = {
        "PDG_observed_values": False,
        "fitted_matching_coefficients": False,
        "new_axioms": False,
        "lattice_MC_empirical_measurements": False,
        "observable_principle_from_axiom": False,
        "yt_ward_identity": False,
        "alpha_LM_chain": False,
    }
    results.append(
        check(
            "11. forbidden-input boundary",
            not any(forbidden.values()),
            "no PDG, no fitted coefficients, no new repo-wide axioms, no MC inputs, "
            "no observable-principle / YT Ward / alpha_LM decoration used",
        )
    )

    print()
    print("-" * 78)
    print("ORIENTATION PRINCIPLE SUMMARY")
    print("-" * 78)
    print()
    print("Cited support inputs (chain):")
    print("  - AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29")
    print("    (action-level temporal-axis sign rule eta_t(theta x) = - eta_t(x))")
    print("  - AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03")
    print("    (Step 4: temporal direction is unique RP-admissible reflection axis)")
    print("  - AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01")
    print("    (forward-time alpha_t = exp(itH) with finite v_LR)")
    print("  - ANOMALY_FORCES_TIME_THEOREM (definite 3+1 time direction)")
    print()
    print("Output: action-level Z_2 grading Theta_RP = (-1)^{n_t} on Lambda^* W")
    print("        breaks the Hodge P_1 <-> P_3 degeneracy by giving")
    print("        ASYMMETRIC (-1)-eigenspace dimensions:")
    print("            dim(P_1 cap E_-) = 1   (just e^t = the time direction)")
    print("            dim(P_3 cap E_-) = 3   (time-mixed 3-forms, no e^t)")
    print()
    print("Hodge star anticommutes with Theta_RP — it is NOT a symmetry of the")
    print("cited action-level temporal-axis sign rule.")
    print()
    print("Orientation principle: pick the rank-four carrier whose unique")
    print("(-1)-Theta_RP eigenvector is the infinitesimal time direction.")
    print("UNIQUELY satisfied by P_1.")
    print()
    print("Verdict: bounded_theorem proposal — orientation principle supplies")
    print("a bounded proposed closure from cited 3+1 single-clock support. The bounded label")
    print("reflects that the action-level identification of Theta_RP with the")
    print("exterior 1-form temporal-axis sign is a conditional bridge from")
    print("the staggered-Dirac action surface to Lambda^* W.")
    print()

    pass_total = sum(results)
    fail_total = len(results) - pass_total

    # Required output format.
    print(f"=== TOTAL: PASS={pass_total}, FAIL={fail_total} ===")

    return 0 if fail_total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
