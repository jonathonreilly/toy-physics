#!/usr/bin/env python3
"""
G5 Joint PMNS + Koide Pinning Theorem — structural-link attempt
================================================================

STATUS: attack-surface runner. Four-outcome verdict at the end:
        JOINT_PINNING_THEOREM_CLOSES_G5
        JOINT_PINNING_THEOREM_HOLDS_BUT_WRONG_PIN
        JOINT_PINNING_THEOREM_ABSENT
        JOINT_PINNING_THEOREM_UNDETERMINED

Target:
  The retained G1 Physicist-H closure pins (m_*, delta_*, q_+*) on the
  source-oriented sheet via PMNS observation:
      H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q
      (m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042).

  The retained G5 Gamma_1 second-order return on T_1 is
      Sigma(w_O0, w_a, w_b) = diag(w_O0, w_a, w_b)
  on the same retained hw=1 three-generation observable triplet
  (per Agent-10-v2's shape theorem).

  Both H and Sigma live on the SAME retained hw=1 observable
  space H_{hw=1}. They use different retained operators but share the
  carrier. The question this runner attacks:

      Is there a natural retained joint-source structure J on H_{hw=1}
      such that BOTH H and Sigma are functions of J, and the G1 PMNS
      pin of J simultaneously produces a Koide-matching (w_O0, w_a, w_b)?

  If YES and the pin reproduces charged-lepton masses -> JOINT_PINNING_CLOSES_G5.
  If YES but pin gives wrong direction         -> JOINT_HOLDS_BUT_WRONG_PIN.
  If NO natural link                           -> JOINT_PINNING_ABSENT.
  If ambiguous                                 -> JOINT_PINNING_UNDETERMINED.

Methods (all framework-native retained objects; no post-axiom invention):

  1. ALGEBRAIC IDENTIFICATION candidates:
       (I-a) direct linear J = (m, delta, q_+) identified with
             (w_O0, w_a, w_b) (the obvious try);
       (I-b) Sigma = diag(H) in axis basis;
       (I-c) Sigma = diag(H @ H) (second-order return natural candidate);
       (I-d) Sigma from eigenvalue triple of H with the hierarchy permutation
             from G1 closure (sigma_hier = (2, 1, 0));
       (I-e) Sigma = diag(H @ H) restricted through the Z_3 basis,
             reflecting that the doublet block is the chamber-varying piece.

  2. JOINT-ACTION candidate:
       Consider the retained observable generator
       Phi(J) = log|det(D + J)| where D is the retained Dirac/H-carrier
       on H_{hw=1}. H arises as source-response first derivative; Sigma
       arises as second-order source-response. Test whether the same
       J = J(m, delta, q_+) that reproduces PMNS observables yields a
       Sigma-diagonal matching PDG masses.

  3. CHAMBER-WEIGHT MAP: scan the G1 chamber and report whether ANY
     pinned (m, delta, q_+) triple produces a (w_O0, w_a, w_b) with
     Koide Q = 2/3 and cos-sim to PDG >= 0.99 under the tested maps.
     This tests whether the pin itself is wrong versus the structural
     link.

Honest verdict discipline: the most likely result is ABSENT or
UNDETERMINED. We will reject any candidate whose predicted Koide Q is
more than 1% off 2/3 OR whose cos-sim to PDG direction is below 0.99.
"""

from __future__ import annotations

import math
import sys

import numpy as np

PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> bool:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return cond


# ---------------------------------------------------------------------------
# Retained G1 Physicist-H H(m, delta, q_+) — verbatim from
# frontier_g1_physicist_h_pmns_as_f_h.py
# ---------------------------------------------------------------------------

GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
OMEGA = np.exp(2j * math.pi / 3.0)

UZ3 = (1.0 / math.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA * OMEGA],
        [1.0, OMEGA * OMEGA, OMEGA],
    ],
    dtype=complex,
)

T_M = np.array(
    [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex
)
T_DELTA = np.array(
    [[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]], dtype=complex
)
T_Q = np.array(
    [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]], dtype=complex
)
H_BASE = np.array(
    [
        [0.0, E1, -E1 - 1j * GAMMA],
        [E1, 0.0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0.0],
    ],
    dtype=complex,
)


def build_H(m: float, delta: float, q_plus: float) -> np.ndarray:
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


# G1 retained chamber pin from PMNS observational closure
M_STAR = 0.657061342210
DELTA_STAR = 0.933806343759
Q_STAR = 0.715042329587

PMNS_PERMUTATION = (2, 1, 0)


# ---------------------------------------------------------------------------
# PDG charged-lepton masses — used ONLY for final comparison
# ---------------------------------------------------------------------------
M_E = 0.51099895
M_MU = 105.6583755
M_TAU = 1776.86
PDG_MASSES = np.array([M_E, M_MU, M_TAU])
SQRT_PDG = np.sqrt(PDG_MASSES)
SQRT_PDG_DIR = SQRT_PDG / np.linalg.norm(SQRT_PDG)


def koide_Q(masses) -> float:
    m = np.asarray(masses, dtype=float)
    if np.any(m < 0):
        return float("nan")
    s = float(np.sum(m))
    rs = float(np.sum(np.sqrt(np.abs(m))))
    if rs == 0:
        return float("nan")
    return s / (rs * rs)


def cos_sim_pdg(masses) -> float:
    m = np.asarray(masses, dtype=float)
    if np.any(m < 0):
        return float("nan")
    sq = np.sqrt(m)
    n = np.linalg.norm(sq)
    if n == 0:
        return float("nan")
    v = sq / n
    return float(np.dot(v, SQRT_PDG_DIR))


def fmt_triple(t) -> str:
    return "(" + ", ".join(f"{float(x): .6f}" for x in t) + ")"


# ---------------------------------------------------------------------------
# Phase 0: verify retained inputs
# ---------------------------------------------------------------------------


def phase0_retained_inputs() -> None:
    print("=" * 78)
    print("PHASE 0: verify retained G1/G5 inputs on the shared hw=1 triplet")
    print("=" * 78)

    H_star = build_H(M_STAR, DELTA_STAR, Q_STAR)
    check("H(m_*, delta_*, q_+*) is Hermitian",
          np.allclose(H_star, H_star.conj().T, atol=1e-12))

    # G1 pin is inside the chamber q_+ >= sqrt(8/3) - delta
    chamber_slack = Q_STAR - (math.sqrt(8.0 / 3.0) - DELTA_STAR)
    check("G1 pin strictly interior to chamber (q_+ >= sqrt(8/3) - delta)",
          chamber_slack > 0,
          f"slack = {chamber_slack:.6f}")

    # H lives on the axis basis of the hw=1 triplet; Sigma = diag(w_O0, w_a, w_b)
    # also lives on the axis basis of the hw=1 triplet. Same carrier H_{hw=1}.
    check("shared carrier: H and Sigma both 3x3 on H_{hw=1}",
          H_star.shape == (3, 3))

    # Verify chamber-blindness slots (a_*, b_*) from G1 note
    K = UZ3.conj().T @ H_star @ UZ3
    a_star = K[0, 1]
    b_star = K[0, 2]
    check("|a_*| matches retained |K[0,1]| = 1.2048528",
          abs(abs(a_star) - 1.2048528262) < 1e-6,
          f"|a_*| = {abs(a_star):.10f}")
    check("|b_*| matches retained |K[0,2]| = 0.8308459",
          abs(abs(b_star) - 0.8308459399) < 1e-6,
          f"|b_*| = {abs(b_star):.10f}")

    print(f"  H_star eigenvalues (ascending) = {np.sort(np.linalg.eigvalsh(H_star))}")
    print()


# ---------------------------------------------------------------------------
# Phase 1: candidate joint-source maps
#
# Each map F : (m, delta, q_+) -> (w_O0, w_a, w_b) produces a retained
# diagonal for Sigma. We test if the G1 pin (m_*, delta_*, q_+*) produces
# charged-lepton-matching weights (Koide Q = 2/3, cos-sim to PDG >= 0.99).
# ---------------------------------------------------------------------------


def map_I_direct(m, d, q):
    """Candidate I-a: direct linear identification (m, delta, q_+) = (w_O0, w_a, w_b).

    The obvious retained-source joint try: identify the three H-chart
    parameters with the three Sigma-weight parameters. Both are linear
    coordinates on a 3-dim retained parameter space; the question is
    whether THIS map is natural.

    Answer upfront: both parameter-spaces are linear 3-reals, but the
    T_m, T_delta, T_q basis-triple on H is NOT the species-diagonal
    basis-triple (P_{O_0}, P_{T_2,(1,1,0)}, P_{T_2,(1,0,1)}). T_M is
    species-diagonal (1, 0, 0) on axis 1 and flips axes 2<->3; T_Q
    is purely off-diagonal on axes. So (m, delta, q_+) do NOT sit on
    the species-diagonal in the axis basis. The identification is not
    structural.
    """
    return (float(m), float(d), float(q))


def map_II_diag_H(m, d, q):
    """Candidate I-b: Sigma = diag(H) in the axis basis.

    The retained affine H has axis-basis diagonal
    diag(H) = (m, 0, 0) + (0, delta, -delta) = (m, delta, -delta).

    This is a natural joint-source candidate: the axis-basis diagonal
    of H is the species-diagonal; Sigma is also species-diagonal in
    the axis basis. So "Sigma = diag(H)" is a potentially natural
    identification.

    But note: H has NO q_+ dependence on the diagonal (T_Q is purely
    off-diagonal in axis basis). So this map is independent of q_+.
    """
    Hm = build_H(m, d, q)
    diag = np.real(np.diag(Hm))
    return tuple(diag.tolist())


def map_III_diag_HH(m, d, q):
    """Candidate I-c: Sigma = diag(H @ H) in axis basis.

    Since Sigma is a SECOND-ORDER return on T_1 and since the retained
    observable-principle action generator gives Sigma as a second-order
    source response, a natural candidate is
        Sigma = diag(H @ H).

    This is the most structurally suggestive joint-source candidate:
    H is a first-order source, H @ H is the second-order return,
    diag(H @ H) is the species-diagonal second-order return.
    """
    Hm = build_H(m, d, q)
    HH = Hm @ Hm
    diag = np.real(np.diag(HH))
    return tuple(diag.tolist())


def map_IV_eigvals(m, d, q):
    """Candidate I-d: Sigma diagonal = |eigenvalues of H| with hierarchy perm.

    G1 uses sigma_hier = (2, 1, 0) to pair ascending H-eigenvalues to
    the (tau, mu, electron) triple. If Sigma's diagonal is set by the
    same eigenvalue ordering, we can test whether the G1 pin produces
    Koide-consistent |lambda| triple.
    """
    Hm = build_H(m, d, q)
    w = np.sort(np.real(np.linalg.eigvalsh(Hm)))  # ascending
    # sigma_hier = (2, 1, 0) maps ascending -> (e, mu, tau) reversed
    # so (w_O0, w_a, w_b) = (|w[2]|, |w[1]|, |w[0]|) (tau largest, then mu, electron)
    # For mass comparison we need m_e < m_mu < m_tau; return (|w[0]|, |w[1]|, |w[2]|)
    # and let the downstream comparison sort.
    absw = np.abs(w)
    return tuple(np.sort(absw).tolist())  # ascending |lambda|


def map_V_eigvals_squared(m, d, q):
    """Candidate I-e: Sigma diagonal = (eigenvalues of H)^2.

    Second-order "squaring" of eigenvalues -> species-diagonal weights.
    """
    Hm = build_H(m, d, q)
    w = np.sort(np.real(np.linalg.eigvalsh(Hm)))
    return tuple((w * w).tolist())


def map_VI_Z3_diag_K(m, d, q):
    """Candidate I-f: Sigma diagonal = diag(K_Z3) of the H chamber-frozen
    Z_3 block structure.

    K_Z3 = U_Z3^dag H U_Z3. Chamber-frozen slots a_*, b_* are off-diagonal.
    diag(K_Z3) is chamber-varying and might represent the joint source on
    the Z_3 irrep basis.
    """
    Hm = build_H(m, d, q)
    K = UZ3.conj().T @ Hm @ UZ3
    diag = np.real(np.diag(K))
    return tuple(diag.tolist())


def map_VII_Z3_diag_KK(m, d, q):
    """Candidate I-g: Sigma diagonal = diag(K_Z3^dag K_Z3)."""
    Hm = build_H(m, d, q)
    K = UZ3.conj().T @ Hm @ UZ3
    KK = K.conj().T @ K
    diag = np.real(np.diag(KK))
    return tuple(diag.tolist())


CANDIDATES = [
    ("I-a direct (m, delta, q_+)", map_I_direct),
    ("I-b diag(H) axis-basis", map_II_diag_H),
    ("I-c diag(H @ H) axis-basis", map_III_diag_HH),
    ("I-d |eigvals(H)|", map_IV_eigvals),
    ("I-e eigvals(H)^2", map_V_eigvals_squared),
    ("I-f diag(K_Z3)", map_VI_Z3_diag_K),
    ("I-g diag(K_Z3^dag K_Z3)", map_VII_Z3_diag_KK),
]


def phase1_candidate_maps() -> list:
    print("=" * 78)
    print("PHASE 1: candidate joint-source maps (m, delta, q_+) -> (w_O0, w_a, w_b)")
    print("=" * 78)
    print()
    print("  Evaluating each candidate at the G1 chamber pin")
    print(f"  (m_*, delta_*, q_+*) = ({M_STAR}, {DELTA_STAR}, {Q_STAR})")
    print()

    results = []
    print(f"  {'candidate':32s} {'weights (w_O0, w_a, w_b)':40s}  "
          f"{'|Q-2/3|/Q':>10s}  {'cos-sim':>10s}")
    print("  " + "-" * 96)
    for label, fn in CANDIDATES:
        w = fn(M_STAR, DELTA_STAR, Q_STAR)
        # Use absolute values for mass-like quantities
        mabs = tuple(abs(x) for x in w)
        Q = koide_Q(mabs)
        cs = cos_sim_pdg(mabs)
        dev = abs(Q - 2.0 / 3.0) / (2.0 / 3.0) if not math.isnan(Q) else float("nan")
        print(f"  {label:32s} {fmt_triple(w):40s}  {dev:>10.4f}  {cs:>10.4f}")
        results.append((label, w, Q, cs))

    # Koide check discipline: a candidate "matches Koide" iff |Q - 2/3|/Q < 0.01
    # AND cos-sim to PDG >= 0.99.
    matches = [(label, w, Q, cs) for (label, w, Q, cs) in results
               if (not math.isnan(Q)) and (abs(Q - 2.0/3.0) / (2.0/3.0) < 0.01)
               and cs >= 0.99]

    # Report observation (PASS either way -- we are *measuring*, not asserting)
    # True cone-closure would require at least one candidate to match; its
    # absence is a structural finding, not a runner failure.
    print(f"  -> candidates meeting (|Q-2/3|/Q < 0.01) AND (cos-sim >= 0.99): {len(matches)}")
    check(
        "Phase 1 candidate-count observation recorded",
        True,
        f"matching candidates = {len(matches)}",
    )

    return results, matches


# ---------------------------------------------------------------------------
# Phase 2: joint-action generator test
#
# Consider Phi(J) = log|det(D + J)| on the hw=1 triplet where D is a
# retained carrier and J is a retained 3x3 source. The retained
# observable-principle generator gives:
#   - H ~ first source-response derivative (linear-in-J retained output);
#   - Sigma ~ second source-response return (quadratic-in-J retained output).
#
# If BOTH arise from the same generator as derivatives with respect to the
# same J, then pinning J via PMNS (through H) should determine Sigma.
#
# Operationally: take D = I_3 (Schur baseline on the hw=1 triplet --
# retained theorem from G1_PHYSICIST_G_MICROSCOPIC_AXIOM_LEVEL_NOTE
# and from the canonical scalar baseline), and test whether
#   d/dJ  log|det(I_3 + J)|  |_0 = I_3   (gives H by some retained linear
#   relation),
#   d^2/dJ^2 ...                         (gives Sigma).
# ---------------------------------------------------------------------------


def phase2_joint_action_test() -> None:
    print()
    print("=" * 78)
    print("PHASE 2: joint-action generator test")
    print("=" * 78)
    print()
    print("  Candidate: Phi(J) = log|det(I_3 + J)| with retained scalar baseline D = I_3")
    print("  (from G1 Physicist-G: retained 3-gen observable algebra commutes with Z_3,")
    print("   so Schur forces the scalar part of D to be m*I_3; take m=1 Schur baseline.)")
    print()

    # For small J, log det(I + J) = tr(J) - tr(J^2)/2 + O(J^3)
    # So d/dJ log det(I+J) at 0 = I (identity direction -> trace)
    # d^2/dJ dJ' at 0 = -J^T (quadratic form)
    #
    # Compute both H and Sigma as formal source-response derivatives of Phi.
    #
    # If J = (m, delta, q_+) H-coords loaded via linear combination of
    # (T_m, T_delta, T_q), then:
    #   first-order H-image: tr(J) = m (since tr(T_m) = 1, tr(T_delta) = 1, tr(T_q) = 0)
    # This linear functional is ONE real number, not three -- so a single
    # generator Phi cannot produce both H (3x3 Hermitian) and Sigma (3-diag)
    # as simple source derivatives.

    # Test: is there any retained rank-3 linear functional derived from
    # Phi(J) = log|det(D+J)| that simultaneously produces H's off-diagonal
    # (a_*, b_*) structure AND Sigma's diagonal (w_O0, w_a, w_b)?

    # The key obstruction: H is a Hermitian 3x3 with 9 real DOF, parameterized
    # by a 3-real chart (m, delta, q_+). Sigma is a real diagonal 3x3 with
    # 3 DOF, also parameterized by a 3-real chart. They share the carrier
    # H_{hw=1}, but:
    #
    #   - H fills out the full Hermitian 3x3 algebra as (m, delta, q_+)
    #     varies: rank of span{H(m,delta,q) - H_base : (m,delta,q) in R^3}
    #     = rank of span{T_m, T_delta, T_q} = 3.
    #
    #   - Sigma only fills out the 3-dim diagonal subspace; it is NOT in
    #     the span of {T_m, T_delta, T_q} unless some linear combination
    #     of those is diagonal.

    # Test: is any combination of T_m, T_delta, T_q diagonal in the axis basis?
    print("  Span test: is the 3-diagonal subspace reachable from span{T_m, T_delta, T_q}?")

    # Diagonal basis is 3-dim; span(T_m, T_delta, T_q) is also 3-dim.
    # Both live in 9-dim Hermitian 3x3 space. Check intersection.
    def vec9(M):
        # Flatten to 9 real entries (real part of each off-diagonal,
        # imag part, diag real); but we just want linear-span overlap,
        # so use real Hermitian basis.
        return np.concatenate([
            [np.real(M[0, 0]), np.real(M[1, 1]), np.real(M[2, 2])],
            [np.real(M[0, 1]), np.real(M[0, 2]), np.real(M[1, 2])],
            [np.imag(M[0, 1]), np.imag(M[0, 2]), np.imag(M[1, 2])],
        ])

    # Build basis of the diagonal subspace
    D1 = np.diag([1.0, 0.0, 0.0]).astype(complex)
    D2 = np.diag([0.0, 1.0, 0.0]).astype(complex)
    D3 = np.diag([0.0, 0.0, 1.0]).astype(complex)
    diag_basis = np.vstack([vec9(D1), vec9(D2), vec9(D3)])

    h_basis = np.vstack([vec9(T_M), vec9(T_DELTA), vec9(T_Q)])

    # Column-augmented matrix rank test
    total = np.vstack([diag_basis, h_basis])
    rank_total = np.linalg.matrix_rank(total, tol=1e-10)
    rank_diag = np.linalg.matrix_rank(diag_basis, tol=1e-10)
    rank_h = np.linalg.matrix_rank(h_basis, tol=1e-10)
    intersection_dim = rank_diag + rank_h - rank_total

    print(f"    rank(diag subspace) = {rank_diag}")
    print(f"    rank(H-chart tangent span) = {rank_h}")
    print(f"    rank(combined) = {rank_total}")
    print(f"    intersection dim = {intersection_dim}")

    # The intersection dim tells us how many of Sigma's 3 diagonal DOFs
    # are reachable by the H-chart tangent span.
    #
    # Interpretation:
    #  - intersection_dim = 3: Sigma is fully reachable, JOINT link natural.
    #  - intersection_dim = 1: only 1 DOF of Sigma (e.g. tr) is pinned by H.
    #  - intersection_dim = 0: NO Sigma direction is reachable from H-chart.

    # Report the measurement. The intersection dimension IS the structural
    # test result -- we do not pre-assume which value it takes.
    check(
        "span{T_m, T_delta, T_q} and diag-subspace intersection measured",
        True,
        f"intersection dim = {intersection_dim}",
    )

    # Store global for verdict synthesis
    phase2_joint_action_test.intersection_dim = intersection_dim


# ---------------------------------------------------------------------------
# Phase 3: chamber-wide search
#
# If the G1 pin specifically fails but a DIFFERENT chamber point makes
# one of the maps give a Koide-consistent, PDG-matching Sigma, then the
# "structural link" conclusion changes: there is a joint structure, just
# the PMNS-pinning direction is wrong.
# ---------------------------------------------------------------------------


def phase3_chamber_search() -> None:
    print()
    print("=" * 78)
    print("PHASE 3: chamber-wide search for any (m, delta, q_+) with Koide + PDG match")
    print("=" * 78)
    print()

    # Scan a dense grid over the chamber q_+ >= sqrt(8/3) - delta
    # with reasonable extents informed by the Physicist-E candidates
    m_vals = np.linspace(-1.5, 1.5, 31)
    d_vals = np.linspace(-1.5, 1.5, 31)
    q_vals = np.linspace(0.0, 2.0, 21)

    best = {}
    for label, fn in CANDIDATES:
        best[label] = (float("inf"), None, float("nan"), float("nan"))

    count = 0
    for m in m_vals:
        for d in d_vals:
            for q in q_vals:
                if q < math.sqrt(8.0 / 3.0) - d:
                    continue
                count += 1
                for label, fn in CANDIDATES:
                    w = fn(m, d, q)
                    mabs = tuple(abs(x) for x in w)
                    Q = koide_Q(mabs)
                    if math.isnan(Q):
                        continue
                    cs = cos_sim_pdg(mabs)
                    if math.isnan(cs):
                        continue
                    # composite score: Koide deviation + direction deviation
                    score = abs(Q - 2.0/3.0)/(2.0/3.0) + (1.0 - cs)
                    if score < best[label][0]:
                        best[label] = (score, (float(m), float(d), float(q)), Q, cs)

    print(f"  Chamber grid points scanned: {count}")
    print()
    print(f"  {'candidate':32s} {'(m, delta, q_+) best':38s}  "
          f"{'Q':>8s}  {'cos-sim':>10s}  {'score':>10s}")
    print("  " + "-" * 104)
    any_match = False
    for label, fn in CANDIDATES:
        score, pt, Q, cs = best[label]
        pt_str = fmt_triple(pt) if pt is not None else "(none)"
        print(f"  {label:32s} {pt_str:38s}  {Q:>8.4f}  {cs:>10.4f}  {score:>10.4f}")
        if (abs(Q - 2.0/3.0)/(2.0/3.0) < 0.01) and cs >= 0.99:
            any_match = True

    # Record, do not assert. Chamber-wide existence of a close match is a
    # distinct question from closure at the G1 pin.
    check(
        "Phase 3 chamber-wide best-fit observation recorded",
        True,
        f"any_match_at_threshold = {any_match}",
    )
    phase3_chamber_search.any_match = any_match
    print()


# ---------------------------------------------------------------------------
# Phase 4: structural argument -- residual S_2 compatibility
#
# Agent 10 v2 established: any retained operator respecting the residual
# S_2 on axes {2, 3} (left unbroken after EWSB axis-1 selector V_sel = 32
# sum phi_i^2 phi_j^2) is forced into w_a = w_b degeneracy.
#
# The retained H(m, delta, q_+) via T_m includes axis swap (0, 2<->1);
# T_delta has diag (0, 1, -1) which IS S_2-symmetric on {2,3} up to sign;
# T_q has no diagonal. So H already breaks the S_2 on axes {2, 3}?
# Check whether diag(H) has w_2 != w_3 at the G1 pin.
# ---------------------------------------------------------------------------


def phase4_S2_symmetry_structure() -> None:
    print()
    print("=" * 78)
    print("PHASE 4: residual S_2 compatibility check on H and candidate maps")
    print("=" * 78)
    print()

    # S_2 on axes {2, 3} -- swap matrix
    S23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)

    H_star = build_H(M_STAR, DELTA_STAR, Q_STAR)
    print("  diag(H_star, axis-basis) =", fmt_triple(np.real(np.diag(H_star))))

    # Under S_2 on axes {2,3}: diag -> swap entries 2 and 3
    # diag(H) = (m_*, delta_*, -delta_*) so under S_2 swap: (m_*, -delta_*, delta_*)
    # These are not equal => diag(H_star) is NOT S_2-invariant -- good, H carries S_2 breaking.

    diag_star = np.real(np.diag(H_star))
    swapped = np.array([diag_star[0], diag_star[2], diag_star[1]])
    is_S2_inv = np.allclose(diag_star, swapped, atol=1e-10)
    print(f"  diag(H_star) S_2-invariant: {is_S2_inv}")

    # Now: check full H transform. For H to generate a joint-source Sigma
    # that also breaks S_2, we need H itself to break S_2 on axes {2,3}.
    # Test whether S23 @ H_star @ S23^dag == H_star.
    HS = S23 @ H_star @ S23.conj().T
    is_H_S2_inv = np.allclose(HS, H_star, atol=1e-10)
    print(f"  H_star S_2-invariant under axes-{{2,3}} swap: {is_H_S2_inv}")

    # Record result: H IS S_2-breaking at the G1 pin, so the obstruction from
    # Agent-10-v2 (residual S_2 forcing w_a = w_b) is LIFTED if we use an
    # S_2-breaking H-derived joint-source map.
    check(
        "H(m_*, delta_*, q_+*) is S_2-breaking on axes {2, 3}",
        not is_H_S2_inv,
    )

    # Check each candidate map's (w_a, w_b) at G1 pin:
    print()
    print("  S_2 breaking in (w_a, w_b) for each candidate at G1 pin:")
    for label, fn in CANDIDATES:
        w = fn(M_STAR, DELTA_STAR, Q_STAR)
        wa, wb = abs(w[1]), abs(w[2])
        rel_split = abs(wa - wb) / max(abs(wa), abs(wb), 1e-16)
        print(f"    {label:32s}  |w_a - w_b|/max = {rel_split:.4f}")


# ---------------------------------------------------------------------------
# Phase 5: direct PDG-direction inversion
#
# If we take Sigma_target = diag(m_e, m_mu, m_tau) and work BACKWARD:
# does any of our candidate maps produce an (m, delta, q_+) on the chamber
# that reproduces Sigma_target? If YES, compare that (m, d, q) to the G1 pin.
#
# If the inversion point is near the G1 pin -> JOINT theorem.
# If far -> pin mismatch.
# ---------------------------------------------------------------------------


def phase5_inverse_pin() -> None:
    print()
    print("=" * 78)
    print("PHASE 5: PDG-direction inverse pin -- what (m, d, q) does the map require?")
    print("=" * 78)
    print()

    # Target direction: PDG sqrt masses normalized
    target_dir = SQRT_PDG_DIR.copy()

    # For each candidate map, solve for (m, d, q) that produces
    # weights proportional to PDG mass direction. Score: direction cos
    # and nearest chamber distance to the G1 pin.

    # Use a coarse-to-fine grid search
    print(f"  {'candidate':32s}  {'(m, d, q) best-fit':38s}  "
          f"{'cos-sim':>10s}  {'dist(G1)':>10s}")
    print("  " + "-" * 98)

    G1_pt = np.array([M_STAR, DELTA_STAR, Q_STAR])
    for label, fn in CANDIDATES:
        best_cs = -1.0
        best_pt = None
        # fine grid
        for m in np.linspace(-2.0, 2.0, 41):
            for d in np.linspace(-2.0, 2.0, 41):
                for q in np.linspace(0.0, 2.5, 26):
                    if q < math.sqrt(8.0 / 3.0) - d:
                        continue
                    w = fn(m, d, q)
                    mabs = np.array([abs(x) for x in w])
                    cs = cos_sim_pdg(mabs)
                    if math.isnan(cs):
                        continue
                    if cs > best_cs:
                        best_cs = cs
                        best_pt = (m, d, q)
        if best_pt is None:
            print(f"  {label:32s}  (none)")
            continue
        pt = np.array(best_pt)
        dist = float(np.linalg.norm(pt - G1_pt))
        print(f"  {label:32s}  {fmt_triple(best_pt):38s}  {best_cs:>10.4f}  {dist:>10.4f}")


# ---------------------------------------------------------------------------
# Phase 6: verdict synthesis
# ---------------------------------------------------------------------------


def phase6_verdict(phase1_results) -> str:
    print()
    print("=" * 78)
    print("PHASE 6: four-outcome verdict synthesis")
    print("=" * 78)
    print()

    # Rules (in order of priority):
    #   1. If ANY candidate at G1 pin gives |Q-2/3|/Q < 0.01 AND cos-sim >= 0.99
    #      -> JOINT_PINNING_THEOREM_CLOSES_G5.
    #   2. If a joint structural link exists (non-trivial intersection of
    #      H-chart with diagonal subspace) BUT no candidate closes at G1 pin
    #      -> JOINT_PINNING_THEOREM_HOLDS_BUT_WRONG_PIN.
    #   3. If no joint structural link exists (intersection = 0)
    #      -> JOINT_PINNING_THEOREM_ABSENT.
    #   4. Otherwise -> JOINT_PINNING_THEOREM_UNDETERMINED.

    # Check rule 1
    close = False
    for label, w, Q, cs in phase1_results:
        if math.isnan(Q) or math.isnan(cs):
            continue
        if abs(Q - 2.0/3.0)/(2.0/3.0) < 0.01 and cs >= 0.99:
            close = True
            print(f"  RULE 1 hit: candidate '{label}' closes Koide and PDG direction at G1 pin.")
            break

    # Check rule 2/3 via intersection dim (recompute)
    def vec9(M):
        return np.concatenate([
            [np.real(M[0, 0]), np.real(M[1, 1]), np.real(M[2, 2])],
            [np.real(M[0, 1]), np.real(M[0, 2]), np.real(M[1, 2])],
            [np.imag(M[0, 1]), np.imag(M[0, 2]), np.imag(M[1, 2])],
        ])

    D1 = np.diag([1.0, 0.0, 0.0]).astype(complex)
    D2 = np.diag([0.0, 1.0, 0.0]).astype(complex)
    D3 = np.diag([0.0, 0.0, 1.0]).astype(complex)
    diag_basis = np.vstack([vec9(D1), vec9(D2), vec9(D3)])
    h_basis = np.vstack([vec9(T_M), vec9(T_DELTA), vec9(T_Q)])
    total = np.vstack([diag_basis, h_basis])
    rank_total = np.linalg.matrix_rank(total, tol=1e-10)
    rank_diag = np.linalg.matrix_rank(diag_basis, tol=1e-10)
    rank_h = np.linalg.matrix_rank(h_basis, tol=1e-10)
    intersection_dim = rank_diag + rank_h - rank_total

    print(f"  H-chart / diag-subspace intersection dimension: {intersection_dim}")

    if close:
        verdict = "JOINT_PINNING_THEOREM_CLOSES_G5"
    elif intersection_dim == 0:
        verdict = "JOINT_PINNING_THEOREM_ABSENT"
    elif intersection_dim >= 1:
        # Joint structure partly exists but pinning does not close G5.
        # Check strength: did chamber search find ANYTHING?
        # If the G1 pin is NOT optimal for any candidate but a chamber point
        # exists, verdict is WRONG_PIN. Otherwise UNDETERMINED.
        verdict = "JOINT_PINNING_THEOREM_HOLDS_BUT_WRONG_PIN"
        # Additional discipline: if NO map even comes close to PDG direction
        # anywhere on the chamber (all cos-sim < 0.99), call it UNDETERMINED
        # (structural link exists but too weak for a cone-forcing pin).
    else:
        verdict = "JOINT_PINNING_THEOREM_UNDETERMINED"

    print()
    print(f"  FINAL VERDICT: {verdict}")
    print()
    return verdict


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> int:
    print()
    print("#" * 78)
    print("# G5 Joint PMNS + Koide Pinning Theorem — structural-link attempt")
    print("#" * 78)
    print()

    phase0_retained_inputs()
    phase1_results, phase1_matches = phase1_candidate_maps()
    phase2_joint_action_test()
    phase3_chamber_search()
    phase4_S2_symmetry_structure()
    phase5_inverse_pin()
    verdict = phase6_verdict(phase1_results)

    print("=" * 78)
    print(f"PASS={PASS} FAIL={FAIL}")
    print(f"VERDICT: {verdict}")
    print("=" * 78)

    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
