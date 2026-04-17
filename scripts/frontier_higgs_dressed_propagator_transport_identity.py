#!/usr/bin/env python3
"""
G5 / transport-identity lane — Higgs-Dressed Intermediate Propagator
=====================================================

Attack target (a companion runner, distinct from Agents 9, 12, 13):

  The retained Gamma_1 second-order return on T_1 is

      Sigma(I) = P_{T_1} Gamma_1 (P_{O_0} + P_{T_2}) Gamma_1 P_{T_1} = I_3

  (a companion runner v2 shape theorem). The three species connect via Gamma_1 to
  three distinct intermediate states:

      species 1  ->  O_0 = (0,0,0)
      species 2  ->  (1,1,0) in T_2
      species 3  ->  (1,0,1) in T_2

  a companion runner tested H directly as the charged-lepton mass operator -> NO_NATURAL_MATCH.
  a companion runner tested H lifted POST-HOC to T_2 diagonal weights -> AMBIGUOUS.
  a companion runner proved dim(V_H cap V_D) = 0 on the hw=1 diagonal subspace.

  This runner tests a genuinely new construction: replace the unit-weight
  intermediate projector (P_O0 + P_T2) with a Higgs-dressed weight operator
  W(H) that lives on C^16 and is derived from G1's retained affine Hermitian
  H(m, delta, q_+). Four candidate constructions:

    G-1: Natural Higgs-lift of H onto (O_0 ⊕ T_2) via the Gamma_1 hopping
         map.  Each intermediate state receives the H-value of its
         Gamma_1-preimage species.
    G-2: Higgs propagator (resolvent form) 1 / (H_lift + m_Higgs).
    G-3: Higgs-projected weight M(phi_axis1) dressed at EWSB axis 1.
    G-4: Shifted weight from T_m, T_delta, T_q extended to T_2.

  For each construction we compute

      diag(Sigma_Higgs) = diag(P_{T_1} Gamma_1 W(H) Gamma_1 P_{T_1})

  restricted to the L-taste T_1 species block and ask:

    - Are the three weights distinct?
    - Do they reproduce the observed charged-lepton ratios?
    - Does Koide Q = 2/3 fall out?

  Retained-only construction. No new axiom. PDG charged-lepton masses
  used ONLY in the cos-similarity / Koide comparison.

Verdict: one of
  TRANSPORT_IDENTITY_CLOSES_CL_HIERARCHY
  TRANSPORT_IDENTITY_PARTIAL_MATCH
  TRANSPORT_IDENTITY_NO_MATCH
  TRANSPORT_IDENTITY_UNDERDETERMINED
"""

from __future__ import annotations

import math
import sys
import numpy as np


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


# ----------------------------------------------------------------------
# Cl(3) + chirality carrier on C^16 — identical to the Dirac-bridge runner
# ----------------------------------------------------------------------

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
GAMMA_5_4D = G0 @ G1 @ G2 @ G3

P_L = (I16 + GAMMA_5_4D) / 2.0
P_R = (I16 - GAMMA_5_4D) / 2.0

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


def point_projector(spatial_state):
    p = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        p[INDEX[spatial_state + (t,)], INDEX[spatial_state + (t,)]] = 1.0
    return p


P_O0 = projector(O0_STATES)
P_T1 = projector(T1_STATES)
P_T2 = projector(T2_STATES)
P_O3 = projector(O3_STATES)


def t1_species_basis():
    """3 column vectors, one per species, L-taste (t=0) branch on T_1."""
    cols = []
    for s in T1_STATES:
        e = np.zeros((16, 1), dtype=complex)
        e[INDEX[s + (0,)], 0] = 1.0
        cols.append(e)
    return np.hstack(cols)


BASIS_T1_SPECIES = t1_species_basis()  # 16 x 3


def restrict_species(op16):
    """16x16 -> 3x3 species block via L-taste T_1 subspace."""
    return BASIS_T1_SPECIES.conj().T @ op16 @ BASIS_T1_SPECIES


# ----------------------------------------------------------------------
# retained neutrino-mixing affine Hermitian H(m, delta, q_+) on the T_1 species basis
# ----------------------------------------------------------------------

GAMMA_H = 0.5
E1_H = math.sqrt(8.0 / 3.0)
E2_H = math.sqrt(8.0) / 3.0

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
        [0.0, E1_H, -E1_H - 1j * GAMMA_H],
        [E1_H, 0.0, -E2_H],
        [-E1_H + 1j * GAMMA_H, -E2_H, 0.0],
    ],
    dtype=complex,
)

# retained neutrino-mixing chamber pin from PMNS observation
M_STAR = 0.657061
DELTA_STAR = 0.933806
Q_STAR = 0.715042


def H_chart(m: float, delta: float, q_plus: float) -> np.ndarray:
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


# ----------------------------------------------------------------------
# Gamma_1 hopping structure: which intermediate state does each T_1 species
# reach in one Gamma_1 hop?
# ----------------------------------------------------------------------
#   species 1 = (1,0,0) --Gamma_1--> (0,0,0) = O_0
#   species 2 = (0,1,0) --Gamma_1--> (1,1,0) in T_2
#   species 3 = (0,0,1) --Gamma_1--> (1,0,1) in T_2
# (Verified in Phase 1 below.)
# ----------------------------------------------------------------------

# Species -> intermediate-state spatial label
SPECIES_INTERMEDIATE = {
    0: (0, 0, 0),   # species 1 (electron) -> O_0
    1: (1, 1, 0),   # species 2 (muon)     -> (1,1,0) in T_2
    2: (1, 0, 1),   # species 3 (tau)      -> (1,0,1) in T_2
}

# The third T_2 state is structurally unreachable from T_1 in one Gamma_1 hop
UNREACHABLE_T2 = (0, 1, 1)


# ----------------------------------------------------------------------
# PDG charged-lepton masses — comparison ONLY
# ----------------------------------------------------------------------

M_E = 0.51099895     # MeV
M_MU = 105.6583755   # MeV
M_TAU = 1776.86      # MeV
PDG_MASSES = np.array([M_E, M_MU, M_TAU])
PDG_SQRT_DIRECTION = np.sqrt(PDG_MASSES) / np.linalg.norm(np.sqrt(PDG_MASSES))
PDG_DIRECTION = PDG_MASSES / np.linalg.norm(PDG_MASSES)


def koide_Q(masses):
    m = np.asarray(masses, dtype=float)
    m_abs = np.abs(m)
    if np.any(m_abs <= 1e-30):
        return float("nan")
    s = float(np.sum(m_abs))
    rs = float(np.sum(np.sqrt(m_abs)))
    return s / (rs * rs)


def sqrt_dir(masses):
    m = np.abs(np.asarray(masses, dtype=float))
    sq = np.sqrt(m)
    n = np.linalg.norm(sq)
    if n < 1e-30:
        return None
    return sq / n


def direction_cos(masses):
    sd = sqrt_dir(masses)
    if sd is None:
        return float("nan")
    return float(np.dot(sd, PDG_SQRT_DIRECTION))


def best_permuted_cos(masses):
    from itertools import permutations
    best = -2.0
    best_perm = None
    for perm in permutations(range(3)):
        m_perm = np.array([masses[i] for i in perm])
        c = direction_cos(m_perm)
        if not math.isnan(c) and c > best:
            best = c
            best_perm = perm
    return best, best_perm


def pretty(vals):
    return "[" + ", ".join(f"{v:+.6f}" for v in vals) + "]"


# ----------------------------------------------------------------------
# PHASE 1: verify the retained identity and the Gamma_1 hopping structure
# ----------------------------------------------------------------------

def phase1_verify_structure():
    print("=" * 78)
    print("PHASE 1: retained identity + Gamma_1 hopping-structure check")
    print("=" * 78)

    check("Gamma_1 Hermitian", np.allclose(G1, G1.conj().T))
    check("Gamma_1^2 = I", np.allclose(G1 @ G1, I16))

    # Retained unit-weight second-order return on T_1 species block
    sigma_I_full = P_T1 @ G1 @ (P_O0 + P_T2) @ G1 @ P_T1
    sigma_I = restrict_species(sigma_I_full)
    check(
        "Unit-weight second-order return: species block = I_3",
        np.allclose(sigma_I, np.eye(3), atol=1e-12),
        detail=f"diag = {pretty(np.real(np.diag(sigma_I)))}",
    )

    # Verify Gamma_1 hopping pattern: each species hops to a unique intermediate
    print("  Gamma_1 hopping pattern on T_1 (L-taste):")
    for k, s in enumerate(T1_STATES):
        e = np.zeros((16, 1), dtype=complex)
        e[INDEX[s + (0,)], 0] = 1.0
        hopped = G1 @ e
        nz = np.where(np.abs(hopped.flatten()) > 1e-10)[0]
        target_spatial = None
        for i in nz:
            a, b, c, t = FULL_STATES[i]
            if t == 0:
                target_spatial = (a, b, c)
                break
        print(
            f"    species {k + 1} = {s}  -->  {target_spatial}  "
            f"(expected {SPECIES_INTERMEDIATE[k]})"
        )
        check(
            f"species {k + 1} hops to {SPECIES_INTERMEDIATE[k]}",
            target_spatial == SPECIES_INTERMEDIATE[k],
        )

    # Sanity on H: Hermitian on T_1 species basis
    H_star = H_chart(M_STAR, DELTA_STAR, Q_STAR)
    check("H at G1 pin Hermitian", np.allclose(H_star, H_star.conj().T))

    # Eigen-spectrum at G1 pin
    ev = np.sort(np.real(np.linalg.eigvalsh(H_star)))
    print(f"  Eigenvalues of H at G1 pin: {pretty(ev)}")
    print()
    return sigma_I


# ----------------------------------------------------------------------
# Utilities: lift a 3x3 operator X (on T_1 species basis) to C^16
# ----------------------------------------------------------------------

def lift_to_T1(X3):
    """Lift 3x3 species matrix to 16x16, supported on L-taste T_1."""
    return BASIS_T1_SPECIES @ X3 @ BASIS_T1_SPECIES.conj().T


# The key structural observation: there is a canonical bijection
#     species k  <-->  intermediate state SPECIES_INTERMEDIATE[k]
# induced by Gamma_1. This defines a "species-label transport" from T_1 to
# (O_0 union {(1,1,0), (1,0,1)}).  Any 3x3 operator X on the T_1 species
# basis pulls back to an operator on this 3-dim intermediate subspace.

def intermediate_basis():
    """Basis of the 3-dim intermediate subspace reachable from T_1 via one
    Gamma_1 hop, in L-taste (t=0).  Order matches species labels."""
    cols = []
    for k in range(3):
        s = SPECIES_INTERMEDIATE[k]
        e = np.zeros((16, 1), dtype=complex)
        e[INDEX[s + (0,)], 0] = 1.0
        cols.append(e)
    return np.hstack(cols)


BASIS_INT_SPECIES = intermediate_basis()  # 16 x 3


def lift_to_intermediate(X3):
    """Lift 3x3 operator to 16x16, supported on L-taste Gamma_1-reachable
    intermediate subspace (O_0 at species slot 0, (1,1,0) at slot 1,
    (1,0,1) at slot 2)."""
    return BASIS_INT_SPECIES @ X3 @ BASIS_INT_SPECIES.conj().T


# ----------------------------------------------------------------------
# Construction G-1: natural Higgs-lift of H onto the intermediate subspace
# ----------------------------------------------------------------------
#
#   W_1(H) = lift_to_intermediate( f(H) )
#
# where f(H) is a species-diagonal function of H.  Variants tested:
#   G-1a:  f(H) = diag(eigvals of H)                 (ascending real order)
#   G-1b:  f(H) = |H|_diag (absolute values of eigvals along species order)
#   G-1c:  f(H) = H itself (natural map)
#   G-1d:  f(H) = H^2
#   G-1e:  f(H) = (H H^dag) diagonal
# ----------------------------------------------------------------------

def compute_sigma_with_weight(W16):
    """Return 3x3 species block of P_T1 Gamma_1 W Gamma_1 P_T1."""
    op_full = P_T1 @ G1 @ W16 @ G1 @ P_T1
    return restrict_species(op_full)


def construction_G1_variants(H_star):
    """Return dict of G-1 variant name -> 16x16 weight operator."""
    variants = {}

    # G-1a: eigenvalue-species map (ascending real, aligned with species order)
    # H is a neutrino operator; its eigenvalues in some order correspond to
    # species-indexed propagator weights for the charged-lepton sector.
    w, V = np.linalg.eigh(H_star)
    order = np.argsort(np.real(w))
    w_sorted = np.real(w[order])
    # lift into intermediate subspace as diagonal
    D = np.diag(w_sorted).astype(complex)
    variants["G-1a (eigvals ascending -> int subspace)"] = lift_to_intermediate(D)

    # G-1b: |eigvals|
    D = np.diag(np.abs(w_sorted)).astype(complex)
    variants["G-1b (|eigvals| -> int subspace)"] = lift_to_intermediate(D)

    # G-1c: H itself (Hermitian) pulled back
    variants["G-1c (H itself -> int subspace)"] = lift_to_intermediate(H_star)

    # G-1d: H^2
    variants["G-1d (H^2 -> int subspace)"] = lift_to_intermediate(H_star @ H_star)

    # G-1e: absolute value of H (via polar / |H| = sqrt(H H^dag))
    HH = H_star @ H_star.conj().T
    w2, V2 = np.linalg.eigh(HH)
    sqrt_HH = V2 @ np.diag(np.sqrt(np.abs(w2))) @ V2.conj().T
    variants["G-1e (|H| = sqrt(H H^dag) -> int subspace)"] = lift_to_intermediate(sqrt_HH)

    # G-1f: species-direct: put the three species-preimage entries of H
    #       (i.e. diagonal(H) in the species basis) as intermediate weights.
    #       This is the "transport" reading — intermediate slot k inherits
    #       the species-diagonal H-value of its Gamma_1 preimage species.
    H_diag = np.diag(np.diag(H_star))
    variants["G-1f (species-diagonal of H -> int subspace)"] = lift_to_intermediate(H_diag)

    return variants


# ----------------------------------------------------------------------
# Construction G-2: Higgs resolvent propagator
# ----------------------------------------------------------------------
#
#   W_2 = (H + m_H)^{-1}  (or similar shifted resolvent)
#
# The retained Higgs / EWSB scale is v = 246.28 GeV.  For this structural
# test we parametrize m_shift and test whether any shift produces a
# non-degenerate diagonal that matches observation.
# ----------------------------------------------------------------------

def construction_G2_variants(H_star):
    variants = {}
    # Choose shifts to regularize and to test small/large regimes
    I3 = np.eye(3, dtype=complex)
    # G-2a: resolvent with shift large enough to make (H+m) positive
    eig = np.real(np.linalg.eigvalsh(H_star))
    # pick shift guaranteeing positivity
    for tag, shift in [
        ("G-2a (resolvent shift=2)", 2.0),
        ("G-2b (resolvent shift=10)", 10.0),
        ("G-2c (resolvent shift=0.5)", 0.5),
    ]:
        M = H_star + shift * I3
        ev = np.real(np.linalg.eigvalsh(M))
        if np.min(ev) <= 1e-8:
            # shift not enough — regularize
            M = M + (1.0 - np.min(ev)) * I3
        W3 = np.linalg.inv(M)
        variants[tag] = lift_to_intermediate(W3)

    # G-2d: spectral-resolvent with retained EWSB v scale (dimensionless / unit-scaled)
    #       In a dimensionless retained setting we use the ratio scale
    #       s = v / lambda_max(H) to test whether physically-motivated
    #       shifts produce species-resolved weights.  (The overall scale
    #       drops out of Koide Q and cos-similarity.)
    lam_max = float(np.max(np.abs(eig)))
    for tag, s in [
        ("G-2d (resolvent shift=lam_max+eps)", lam_max + 0.1),
        ("G-2e (resolvent shift=2 lam_max)", 2.0 * lam_max),
    ]:
        M = H_star + s * I3
        W3 = np.linalg.inv(M)
        variants[tag] = lift_to_intermediate(W3)

    return variants


# ----------------------------------------------------------------------
# Construction G-3: Higgs-projected weight via the retained Higgs family
# ----------------------------------------------------------------------
#
#   M(phi) = phi_1 Gamma_1 + phi_2 Gamma_2 + phi_3 Gamma_3    (retained EWSB family)
#   W_3 = (P_O0 + P_T2) M(phi)^2 (P_O0 + P_T2)  at phi = e_1 + epsilon
#
# but dressed by G1's H through a weight field.  Concretely:
#   W_3 = (P_O0 + P_T2) D_H (P_O0 + P_T2)
# where D_H is H lifted to the intermediate subspace via the same hopping
# map as G-1.  This is morally a special case of G-1 with Hermitian
# symmetrization — included as a sanity check that the Higgs projection
# does not re-symmetrize the problem to democratic.
# ----------------------------------------------------------------------

def m_phi_operator(phi):
    return phi[0] * G1 + phi[1] * G2 + phi[2] * G3


def construction_G3_variants(H_star):
    variants = {}

    # G-3a: Higgs family |M(phi)|^2 at axis-1 point — unit-weight baseline
    #       M(e_1) = Gamma_1, so |M|^2 = I.  This reduces to unit weight
    #       and reproduces I_3.  Included for verification.
    M = m_phi_operator((1.0, 0.0, 0.0))
    W = M @ M.conj().T  # = I_16 at phi=e_1
    variants["G-3a (|M(e_1)|^2 bare)"] = (P_O0 + P_T2) @ W @ (P_O0 + P_T2)

    # G-3b: |M(phi)|^2 at (1, eps, eps) -> a companion runner v2 Correction A redux
    eps = 0.1
    M = m_phi_operator((1.0, eps, eps))
    W = M @ M.conj().T
    variants["G-3b (|M(1,eps,eps)|^2)"] = (P_O0 + P_T2) @ W @ (P_O0 + P_T2)

    # G-3c: Higgs-projected H-dressing
    #       Project H into the intermediate subspace and symmetrize with the
    #       Higgs source pattern.
    H_lifted = lift_to_intermediate(H_star)
    M_e1 = m_phi_operator((1.0, 0.0, 0.0))
    W = (P_O0 + P_T2) @ M_e1 @ H_lifted @ M_e1 @ (P_O0 + P_T2)
    # Hermitize
    W = 0.5 * (W + W.conj().T)
    variants["G-3c (Higgs-projected H-dressing)"] = W

    # G-3d: |M|^2 weighted BY H-lift (multiplicative dressing)
    M_e1 = m_phi_operator((1.0, 0.0, 0.0))
    W = H_lifted + (P_O0 + P_T2) @ (M_e1 @ M_e1.conj().T - I16) @ (P_O0 + P_T2)
    # Hermitize
    W = 0.5 * (W + W.conj().T)
    variants["G-3d (H-lift + |M|^2 perturbation at e_1)"] = W

    return variants


# ----------------------------------------------------------------------
# Construction G-4: Shifted weight via T_m, T_delta, T_q extended to T_2
# ----------------------------------------------------------------------
#
#   W_4 = alpha I + beta T_delta^lift + gamma T_q^lift  on intermediate subspace
#
# where T_delta and T_q are G1 tangent generators lifted to the 3-dim
# intermediate subspace via the species-hop map.  This tests whether a
# LINEAR combination of retained tangent generators can produce a matching
# diagonal even though dim(V_H cap V_D) = 0 (a companion runner).
# ----------------------------------------------------------------------

def construction_G4_variants(H_star):
    variants = {}
    I3 = np.eye(3, dtype=complex)

    # Natural combinations — use G1 pin coordinates directly
    base_combos = [
        ("G-4a (alpha I + m* T_m)", I3 + M_STAR * T_M),
        ("G-4b (alpha I + delta* T_d)", I3 + DELTA_STAR * T_DELTA),
        ("G-4c (alpha I + q* T_q)", I3 + Q_STAR * T_Q),
        ("G-4d (T_m + T_delta)", T_M + T_DELTA),
        ("G-4e (T_m + T_q)", T_M + T_Q),
        ("G-4f (T_delta + T_q)", T_DELTA + T_Q),
        ("G-4g (T_m + T_delta + T_q)", T_M + T_DELTA + T_Q),
        ("G-4h (H - H_base = m* T_m + d* T_d + q* T_q)",
         M_STAR * T_M + DELTA_STAR * T_DELTA + Q_STAR * T_Q),
    ]
    for tag, X3 in base_combos:
        # take species-diagonal part for intermediate weights
        D = np.diag(np.diag(X3))
        variants[tag + " [species-diag extracted]"] = lift_to_intermediate(D)
        # also try lifting full X3 (off-diagonal parts contribute off-diag)
        variants[tag + " [full lift]"] = lift_to_intermediate(X3)

    return variants


# ----------------------------------------------------------------------
# Evaluation harness
# ----------------------------------------------------------------------

def evaluate_variant(name, W16):
    """Compute diag of the species block and report Koide / cos-sim."""
    sigma3 = compute_sigma_with_weight(W16)
    diag_raw = np.diag(sigma3)
    # Hermitize the species block
    diag_re = np.real(diag_raw)
    diag_im = np.imag(diag_raw)
    off_max = float(np.max(np.abs(sigma3 - np.diag(diag_raw))))

    # For charged-lepton-mass comparison take absolute values (masses > 0).
    m_abs = np.abs(diag_re)
    # Ensure all three nonzero for Koide
    if np.any(m_abs < 1e-12) or not np.all(np.isfinite(m_abs)):
        Q = float("nan")
        best_c, best_perm = float("nan"), None
    else:
        Q = koide_Q(m_abs)
        best_c, best_perm = best_permuted_cos(m_abs)

    return {
        "name": name,
        "diag_re": diag_re,
        "diag_im": diag_im,
        "off_max": off_max,
        "Q": Q,
        "cos_best": best_c,
        "perm": best_perm,
    }


def report(rows, header):
    print("-" * 78)
    print(f"  {header}")
    print("-" * 78)
    print(f"  {'variant':55s}  {'Q':>9s}  {'cos*':>7s}  {'perm':>10s}")
    for r in rows:
        Qs = f"{r['Q']:.5f}" if not math.isnan(r['Q']) else "  nan  "
        cs = f"{r['cos_best']:.4f}" if not math.isnan(r['cos_best']) else " nan  "
        perm = str(r['perm']) if r['perm'] is not None else "-"
        print(f"  {r['name']:55s}  {Qs:>9s}  {cs:>7s}  {perm:>10s}")
    print()


# ----------------------------------------------------------------------
# Audit helpers
# ----------------------------------------------------------------------

def audit_variant(r, threshold_Q=1e-3, threshold_cos=0.99):
    """Classify a variant's outcome for the four-outcome verdict."""
    if math.isnan(r["Q"]) or math.isnan(r["cos_best"]):
        return "degenerate-or-zero"
    distinct = len(set(round(x, 6) for x in np.abs(r["diag_re"]))) == 3
    q_match = abs(r["Q"] - 2.0 / 3.0) < threshold_Q
    dir_match = r["cos_best"] >= threshold_cos
    if q_match and dir_match and distinct:
        return "MATCH"
    if distinct and (q_match or dir_match):
        return "PARTIAL"
    if distinct:
        return "distinct-but-no-match"
    return "degenerate"


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    print("=" * 78)
    print("G5 / AVENUE G — HIGGS-DRESSED INTERMEDIATE PROPAGATOR")
    print("=" * 78)
    print()

    # Phase 1: structural sanity
    sigma_I = phase1_verify_structure()

    # Build H at G1 pin
    H_star = H_chart(M_STAR, DELTA_STAR, Q_STAR)

    # Phase 2: build W(H) variants
    all_variants = {}
    all_variants.update(construction_G1_variants(H_star))
    all_variants.update(construction_G2_variants(H_star))
    all_variants.update(construction_G3_variants(H_star))
    all_variants.update(construction_G4_variants(H_star))

    # Phase 3: evaluate each variant
    print("=" * 78)
    print("PHASE 2/3: W(H) variants and their Sigma_Higgs diagonals")
    print("=" * 78)
    print()
    print(f"  PDG direction (sqrt-unit):  {pretty(PDG_SQRT_DIRECTION)}")
    print(f"  PDG Koide Q (target):       {koide_Q(PDG_MASSES):.6f} ~ 2/3")
    print()

    results = []
    for name, W16 in all_variants.items():
        r = evaluate_variant(name, W16)
        results.append(r)
        print(f"  {r['name']}")
        print(f"    diag(Sigma) re  = {pretty(r['diag_re'])}")
        print(f"    diag(Sigma) im  = {pretty(r['diag_im'])}")
        print(f"    off-diag |max|  = {r['off_max']:.4e}")
        print(f"    Koide Q         = {r['Q']!s:>12}    "
              f"cos*_PDG = {r['cos_best']!s:>10}   perm = {r['perm']}")
        print()

    # Split results by construction
    def results_for(prefix):
        return [r for r in results if r["name"].startswith(prefix)]

    g1 = results_for("G-1")
    g2 = results_for("G-2")
    g3 = results_for("G-3")
    g4 = results_for("G-4")

    report(g1, "Construction G-1 summary (natural H-lift)")
    report(g2, "Construction G-2 summary (Higgs resolvent)")
    report(g3, "Construction G-3 summary (Higgs-projected weight)")
    report(g4, "Construction G-4 summary (T_m, T_delta, T_q lifts)")

    # Phase 4: verdict logic
    print("=" * 78)
    print("PHASE 4: FOUR-OUTCOME VERDICT")
    print("=" * 78)

    classifications = [(r["name"], audit_variant(r)) for r in results]

    # Log each
    for name, clz in classifications:
        print(f"    {clz:25s}  {name}")

    any_match = any(c == "MATCH" for _, c in classifications)
    any_partial = any(c == "PARTIAL" for _, c in classifications)

    # Best cos-sim across all variants
    cos_list = [r["cos_best"] for r in results if not math.isnan(r["cos_best"])]
    Q_list = [r["Q"] for r in results if not math.isnan(r["Q"])]
    best_cos = max(cos_list) if cos_list else float("nan")
    best_Q_dev = min(abs(q - 2.0 / 3.0) for q in Q_list) if Q_list else float("nan")
    print()
    print(f"  Best cos-sim across all variants:   {best_cos:.6f}")
    print(f"  Best |Q - 2/3| across all variants: {best_Q_dev:.6f}")

    # Four-outcome verdict as defined by the task brief:
    #   CLOSES_CL_HIERARCHY:      a retained W matches observation (cos-sim > 0.99 AND Q ~ 2/3)
    #                   at G1's chamber pin alone.
    #   PARTIAL_MATCH:  3 distinct weights and Q ~ 2/3 but direction miss > 1%
    #                   with no retained systematic budget to cover the miss.
    #   UNDERDETERMINED: W that matches observation exists BUT requires a
    #                   retained assumption beyond G1's pin.
    #   NO_MATCH:       every W is species-democratic OR gives a clearly
    #                   non-Koide-consistent triple.
    print()
    if any_match:
        verdict = "TRANSPORT_IDENTITY_CLOSES_CL_HIERARCHY"
    elif any_partial:
        verdict = "TRANSPORT_IDENTITY_PARTIAL_MATCH"
    else:
        # No W variant reproduces Koide Q ~ 2/3 within 1% AND the observed
        # direction; all are either democratic or distinct-but-non-Koide.
        # This is the NO_MATCH outcome: the Higgs-dressed propagator
        # construction on C^16 does not close G5.
        verdict = "TRANSPORT_IDENTITY_NO_MATCH"

    # Structural consistency checks
    # (a) unit-weight baseline reproduces I_3 (Phase 1) — sanity for construction
    check(
        "Baseline unit-weight Sigma = I_3 (consistency)",
        np.allclose(sigma_I, np.eye(3), atol=1e-12),
    )
    # (b) Every W-variant produced a finite species-block
    check(
        "All W(H) variants give finite 3x3 blocks",
        all(np.all(np.isfinite(r["diag_re"])) for r in results),
    )
    # (c) At least one G-1 variant produced distinct diagonal (the core claim)
    has_distinct_G1 = any(
        (len(set(round(x, 6) for x in np.abs(r["diag_re"]))) == 3)
        for r in g1
    )
    check(
        "Some G-1 variant produces three distinct species weights",
        has_distinct_G1,
    )

    print()
    print(f"  Verdict: {verdict}")
    print()
    print("  Justification:")
    print("  - G-1: natural Higgs-lift via Gamma_1 hopping pulls H eigenvalues /")
    print("    species-diagonal entries into the intermediate subspace. Tests")
    print("    whether the transport map species -> intermediate state yields")
    print("    three distinct weights matching observation.")
    print("  - G-2: Higgs resolvent (H + shift)^{-1} tests whether a propagator-")
    print("    style dressing produces the required splitting.")
    print("  - G-3: Higgs-projected weight at EWSB axis 1 tests whether the")
    print("    retained Higgs family re-symmetrizes the H-lift.")
    print("  - G-4: T_m, T_delta, T_q lifts test whether retained tangent")
    print("    generators, extended to the intermediate subspace, carry the")
    print("    required S_2-breaking shape.")
    print()

    print("=" * 78)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print(f"VERDICT: {verdict}")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
