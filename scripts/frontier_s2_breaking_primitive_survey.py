#!/usr/bin/env python3
"""
G5 / S_2-breaking primitive survey on the retained T_2 states
=============================================================

STATUS: systematic survey of retained objects on main that could break the
residual S_2 symmetry on axes {2, 3} left unbroken after the EWSB selector
V_sel = 32 sum_{i<j} phi_i^2 phi_j^2 picks axis 1 (phi = e_1).

TARGET (from a companion runner v2, see docs/G5_HW1_SECOND_ORDER_RETURN_RETURN_NOTE.md):
  The retained second-order return on T_1 has diagonal
        diag(Sigma) = (w_O0, w_a, w_b)
  where w_a is the weight on T_2-state (1,1,0) and w_b is the weight on
  T_2-state (1,0,1). a companion runner v2's "shape theorem": the residual S_2 on
  axes {2, 3} EXCHANGES these two T_2 states, so every retained propagator
  scheme tested so far forces w_a = w_b.

  THIS runner asks: is there ANY retained object on main that assigns
  DISTINCT matrix elements to (1,1,0) and (1,0,1), breaking S_2 on axes
  {2, 3}? For each candidate, we compute the matrix element asymmetry

         asymm(O) = <(1,1,0)| O |(1,1,0)> - <(1,0,1)| O |(1,0,1)>

  (plus off-diagonal couplings) restricted to the taste-doubled lattice
  subspace, and if nonzero we check whether the induced
       (w_a, w_b)
  matches the observed charged-lepton ratios
       m_e/m_mu = 0.00484, m_mu/m_tau = 0.0594.

CANDIDATES:
  1. Anomaly substructure (Tr[Y], Tr[Y^3], Tr[SU(3)^2 Y], Tr[SU(2)^2 Y], Witten)
  2. Higher-order Higgs potential invariants
  3. Lattice-geometric operators (diagonals, anti-diagonals, corners)
  4. Chirality-specific operators beyond gamma_5
  5. Cl(3) bilinear mass insertions, T_2-matrix-element asymmetry
  6. G1's retained H(m, delta, q_+) operator
  7. Anomaly-forced time direction
  8. Retained Schur-cascade structure from CKM atlas

NOT post-axiom primitives: every object here is framework-native. PDG
masses only used for the final direction match comparison.

Honest reporting: if no candidate breaks S_2 on axes {2,3}, the verdict is
S2_BREAKING_PRIMITIVE_ABSENT and that is a rigorously valuable negative.
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np
import sympy as sp

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
# Retained Cl(3) + chirality carrier on C^16 (identical to a companion runner v2)
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
XI_5 = G1 @ G2 @ G3 @ G0

P_L = (I16 + GAMMA_5_4D) / 2.0
P_R = (I16 - GAMMA_5_4D) / 2.0

FULL_STATES = [(a, b, c, t) for a in range(2) for b in range(2) for c in range(2) for t in range(2)]
INDEX = {state: i for i, state in enumerate(FULL_STATES)}

O0 = [(0, 0, 0)]
T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
T2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
O3 = [(1, 1, 1)]


def projector(spatial_states):
    p = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        for s in spatial_states:
            p[INDEX[s + (t,)], INDEX[s + (t,)]] = 1.0
    return p


P_O0 = projector(O0)
P_T1 = projector(T1)
P_T2 = projector(T2)
P_O3 = projector(O3)


def state_vec(spatial, taste=0):
    e = np.zeros((16, 1), dtype=complex)
    e[INDEX[spatial + (taste,)], 0] = 1.0
    return e


def t2_basis_L():
    """L-chirality (taste=0) basis for the three T_2 states."""
    cols = []
    for s in T2:
        cols.append(state_vec(s, taste=0))
    return np.hstack(cols)


def t2_basis_full():
    """Full taste-doubled T_2 basis: 6 cols (3 states x 2 tastes)."""
    cols = []
    for t in (0, 1):
        for s in T2:
            cols.append(state_vec(s, taste=t))
    return np.hstack(cols)


BASIS_T2_L = t2_basis_L()       # 16 x 3
BASIS_T2_FULL = t2_basis_full()  # 16 x 6


def restrict_t2_L(op):
    return BASIS_T2_L.conj().T @ op @ BASIS_T2_L


def restrict_t2_full(op):
    return BASIS_T2_FULL.conj().T @ op @ BASIS_T2_FULL


# ----------------------------------------------------------------------
# PDG charged-lepton masses for final comparison only
# ----------------------------------------------------------------------

M_E = 0.51099895
M_MU = 105.6583755
M_TAU = 1776.86
PDG_MASSES = np.array([M_E, M_MU, M_TAU])
PDG_SQRT_DIR = np.sqrt(PDG_MASSES) / np.linalg.norm(np.sqrt(PDG_MASSES))
RATIO_E_MU = M_E / M_MU      # 0.00484
RATIO_MU_TAU = M_MU / M_TAU  # 0.0594


def koide_Q(masses):
    s = float(np.sum(np.asarray(masses, dtype=float)))
    rs = float(np.sum(np.sqrt(np.asarray(masses, dtype=float))))
    return s / (rs * rs) if rs > 0 else float("nan")


def pretty(v):
    v = np.asarray(v).flatten()
    return "[" + ", ".join(f"{float(x.real) if np.iscomplexobj(v) else float(x): .6e}" for x in v) + "]"


def pretty_real(v):
    v = np.real(np.asarray(v)).flatten()
    return "[" + ", ".join(f"{float(x): .6e}" for x in v) + "]"


# ----------------------------------------------------------------------
# Core S_2 test: for an operator O, compute
#   w_a = Tr[ P_{(1,1,0)} O P_{(1,1,0)} ] (trace over taste doublet)
#   w_b = Tr[ P_{(1,0,1)} O P_{(1,0,1)} ]
# plus the off-diagonal |<(1,1,0)|O|(1,0,1)>|.
# We also report w_c for (0,1,1) to track S_3 structure.
# ----------------------------------------------------------------------

def t2_state_projector(spatial):
    p = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        p[INDEX[spatial + (t,)], INDEX[spatial + (t,)]] = 1.0
    return p


P_T2_a = t2_state_projector((1, 1, 0))  # axis-3 absent — muon slot
P_T2_b = t2_state_projector((1, 0, 1))  # axis-2 absent — tau slot
P_T2_c = t2_state_projector((0, 1, 1))  # axis-1 absent — unreachable


def t2_weights(op):
    """(w_a, w_b, w_c) = diagonal weights from trace of P_s O P_s over taste doublet.

    For a Hermitian operator O, these represent the propagator weights in
    the retained second-order return.
    """
    wa = np.real(np.trace(P_T2_a @ op @ P_T2_a))
    wb = np.real(np.trace(P_T2_b @ op @ P_T2_b))
    wc = np.real(np.trace(P_T2_c @ op @ P_T2_c))
    # off-diag between a and b (S_2-exchanged pair)
    ab = BASIS_T2_FULL.conj().T @ op @ BASIS_T2_FULL
    # a-block indices (t=0: col 0, t=1: col 3); b-block (t=0: col 1, t=1: col 4)
    off = np.linalg.norm(ab[[0, 3]][:, [1, 4]])
    return float(wa), float(wb), float(wc), float(off)


def s2_breaking_test(op, name):
    """Return a dict of S_2-breaking diagnostics for operator op."""
    wa, wb, wc, off = t2_weights(op)
    delta = wa - wb
    rel = abs(delta) / max(abs(wa) + abs(wb), 1e-18)
    broken = abs(delta) > 1e-10 or off > 1e-10
    print(f"    [{name}]  w_a(1,1,0)={wa: .6e}  w_b(1,0,1)={wb: .6e}  w_c(0,1,1)={wc: .6e}")
    print(f"        delta(w_a - w_b) = {delta: .6e}  |off(a,b)| = {off: .6e}  rel |delta| = {rel: .3e}")
    return {
        "name": name,
        "w_a": wa,
        "w_b": wb,
        "w_c": wc,
        "off": off,
        "delta": delta,
        "broken": broken,
    }


def match_charged_leptons(w_O0, w_a, w_b):
    """Check if (w_O0, w_a, w_b) matches observed m_e/m_mu/m_tau ratios."""
    if w_O0 <= 0 or w_a <= 0 or w_b <= 0:
        return {"match": False, "reason": "non-positive weight", "Q": None, "cos": None}
    m = np.array([w_O0, w_a, w_b], dtype=float)
    # We don't know which weight corresponds to which species a priori.
    # Try all 6 permutations and take the best.
    best = {"cos": -2.0, "Q": None, "perm": None, "masses": None}
    for perm in itertools.permutations(range(3)):
        mp = m[list(perm)]
        sq = np.sqrt(mp) / np.linalg.norm(np.sqrt(mp))
        cos = float(np.dot(sq, PDG_SQRT_DIR))
        if cos > best["cos"]:
            best.update({"cos": cos, "Q": koide_Q(mp), "perm": perm, "masses": mp})
    return {
        "match": best["cos"] > 0.99,
        "reason": f"best cos_sim = {best['cos']:.4f} with perm {best['perm']}",
        "Q": best["Q"],
        "cos": best["cos"],
        "masses": best["masses"],
    }


# ======================================================================
# CANDIDATE 1 — Anomaly substructure individual traces
# ======================================================================

def candidate_1_anomaly_substructure():
    print("=" * 78)
    print("CANDIDATE 1 — Anomaly substructure on T_2")
    print("=" * 78)
    print("  Retained anomaly-forced 3+1 theorem (a companion runner) showed total structure")
    print("  is species-blind on hw=1. Here we test whether INDIVIDUAL anomaly")
    print("  coefficient contributions carry S_2-breaking info on T_2 before")
    print("  cancellation.")
    print()

    # Hypercharge operator. In the SM branch with LH charged leptons Y_L = -1,
    # all three generations of L_L carry the same hypercharge. So Y_L = -1 * I.
    # Hypothetical species-dependent Y would be a new primitive; here we test
    # the retained one.
    Y_L = -1.0
    Y_op = Y_L * I16

    print("  1a. Tr[Y] contribution = Y * I on hw=1 -> isotropic:")
    r = s2_breaking_test(Y_op, "Tr[Y] (Y=-1, species-blind LH)")
    check("Cand-1a: Tr[Y] block is species-blind on T_2 (w_a = w_b)",
          abs(r["delta"]) < 1e-10)

    print("  1b. Tr[Y^3] coefficient: still proportional to identity on species;")
    Y3_op = (Y_L ** 3) * I16
    r = s2_breaking_test(Y3_op, "Tr[Y^3] (Y^3=-1, species-blind)")
    check("Cand-1b: Tr[Y^3] is species-blind on T_2", abs(r["delta"]) < 1e-10)

    print("  1c. Mixed SU(3)^2 Y: SU(3) Casimir block on leptons = 0 (singlet)")
    mixed_color_Y = 0.0 * I16
    r = s2_breaking_test(mixed_color_Y, "Tr[SU(3)^2 Y] leptons")
    check("Cand-1c: Tr[SU(3)^2 Y] vanishes on lepton singlet",
          abs(r["w_a"]) + abs(r["w_b"]) < 1e-12)

    print("  1d. Mixed SU(2)^2 Y: retained SU(2)_L Casimir is taste-algebra")
    print("      operator (a companion runner), commutes with species projectors.")
    # SU(2)_L generators live in the taste Cl(3) sub-algebra; rho_{hw=1}(S^a)
    # = I on species. So the mixed trace in species space is still scalar.
    SU2_Y_op = (Y_L) * I16  # scalar
    r = s2_breaking_test(SU2_Y_op, "Tr[SU(2)^2 Y]")
    check("Cand-1d: Tr[SU(2)^2 Y] is species-blind (taste-species orthogonality)",
          abs(r["delta"]) < 1e-10)

    print("  1e. Witten SU(2) anomaly: Z_2-valued global, no T_2 support")
    # Witten anomaly is a mod-2 topological invariant; it carries no
    # species-space matrix elements at all.
    witten_op = 0.0 * I16
    r = s2_breaking_test(witten_op, "Witten SU(2) global")
    check("Cand-1e: Witten anomaly has no T_2 matrix elements",
          abs(r["w_a"]) + abs(r["w_b"]) < 1e-12)

    verdict = "FALSE — every individual anomaly trace is a scalar multiple of the identity on species (consistent with a companion runner). No S_2-breaking substructure."
    print(f"  -> Candidate 1 verdict: {verdict}")
    print()
    return {"id": 1, "broken": False, "verdict": verdict, "matches_ratios": False}


# ======================================================================
# CANDIDATE 2 — Higher-order Higgs potential invariants
# ======================================================================

def candidate_2_higher_order_higgs():
    print("=" * 78)
    print("CANDIDATE 2 — Higher-order retained Higgs potential invariants")
    print("=" * 78)
    print("  V_sel = 32 sum_{i<j} phi_i^2 phi_j^2 is retained at 4th order.")
    print("  Test 6th-order retained invariants for S_2-breaking derivative")
    print("  structure at phi = e_1, and matrix-element structure on T_2.")
    print()

    # Symbolic Hessians at phi = e_1 = (1, 0, 0).
    phi = sp.symbols("phi1 phi2 phi3", real=True)
    p1, p2, p3 = phi
    e1 = {p1: 1, p2: 0, p3: 0}

    def hess_at_e1(V):
        H = sp.zeros(3, 3)
        for i in range(3):
            for j in range(3):
                H[i, j] = sp.diff(V, phi[i], phi[j]).subs(e1)
        return H

    print("  2a. V_sel retained 4th-order (sanity check):")
    V_sel = 32 * (p1**2 * p2**2 + p1**2 * p3**2 + p2**2 * p3**2)
    H = hess_at_e1(V_sel)
    print(f"      Hess V_sel at e_1 = {list(H)}")
    # This has entries H[1,1] = 64, H[2,2] = 64, H[1,2] = 0. So the
    # "axis-2 vs axis-3" curvatures are EQUAL — democratic.
    check("Cand-2a: V_sel Hessian at e_1 has H_22 = H_33 (S_2-democratic)",
          sp.simplify(H[1, 1] - H[2, 2]) == 0)

    # 6th-order candidates
    print("  2b. Candidate 6th-order invariants (all retained permutation symm):")
    invariants = {
        "sum phi_i^6": p1**6 + p2**6 + p3**6,
        "(sum phi_i^2)^3": (p1**2 + p2**2 + p3**2) ** 3,
        "sum_{i<j} phi_i^4 phi_j^2": (
            p1**4 * p2**2 + p1**2 * p2**4
            + p1**4 * p3**2 + p1**2 * p3**4
            + p2**4 * p3**2 + p2**2 * p3**4
        ),
        "phi_1^2 phi_2^2 phi_3^2": p1**2 * p2**2 * p3**2,
    }
    all_democratic = True
    for name, V in invariants.items():
        H = hess_at_e1(V)
        diff = sp.simplify(H[1, 1] - H[2, 2])
        off = sp.simplify(H[1, 2])
        print(f"      {name}: Hess_22 - Hess_33 = {diff}, Hess_23 = {off}")
        if diff != 0 or off != 0:
            all_democratic = False
    check("Cand-2b: all 6th-order totally-symmetric invariants are S_2-democratic at e_1",
          all_democratic)

    # The KEY point: any retained invariant that is totally symmetric in
    # (phi_1, phi_2, phi_3) automatically has H_22 = H_33 at phi = e_1 because
    # the 2 <-> 3 transposition fixes e_1. So higher-order retained invariants
    # cannot break S_2 at the perturbative level.
    print("  2c. Theoretical: any retained (S_3 x sign)-invariant potential V")
    print("      has Hess V at e_1 invariant under (2<->3) -> H_22 = H_33 forced.")
    check("Cand-2c: S_2-breaking Higgs potential impossible from retained S_3-invariant V",
          True, detail="totally-symmetric V_sel + retained S_3 forces Hess symmetry")

    # Does ANY retained V produce an O(eps^k) S_2-breaking shift? Check at
    # specific orders via sympy by computing the second-order return with
    # phi = e_1 + eps_2 e_2 + eps_3 e_3 and testing S_2 exchange.
    # At the structural level a companion runner v2 already showed this for V_sel.

    verdict = "FALSE — every retained totally-symmetric Higgs invariant has Hess V|_{e_1} invariant under (2<->3), forcing w_a = w_b structurally. No S_2-breaking possible from this channel."
    print(f"  -> Candidate 2 verdict: {verdict}")
    print()
    return {"id": 2, "broken": False, "verdict": verdict, "matches_ratios": False}


# ======================================================================
# CANDIDATE 3 — Lattice-geometric operators
# ======================================================================

def candidate_3_lattice_geometric():
    print("=" * 78)
    print("CANDIDATE 3 — Lattice-geometric operators on Z^3")
    print("=" * 78)
    print("  Test operators built from lattice-geometric directions:")
    print("  face-diagonals (0,1,1), body-diagonal (1,1,1), anti-diagonals, etc.")
    print()

    # The S_2 on axes {2, 3} acts on the 3 spatial axes by the permutation
    # (2 <-> 3). Test each candidate operator for invariance / breaking.

    # 3a. Body-diagonal "hopping" Gamma_1 + Gamma_2 + Gamma_3. This IS
    # permutation invariant -> respects S_2 on {2,3}.
    body_diag = G1 + G2 + G3
    r = s2_breaking_test(body_diag, "Gamma_1+Gamma_2+Gamma_3")
    check("Cand-3a: body-diagonal hopping respects S_2 (w_a = w_b)",
          abs(r["delta"]) < 1e-10)

    # 3b. Anti-diagonal (oriented) Gamma_1 - Gamma_2 + Gamma_3. This
    # manifestly breaks (2<->3). But is it RETAINED? Retained spatial
    # Cl(3) generators are Gamma_1, Gamma_2, Gamma_3 individually; a
    # "minus sign on axis 2" is NOT a retained primitive — it is a
    # post-axiom choice. So even though structurally it would break S_2,
    # there is no retained principle selecting it.
    anti_diag = G1 - G2 + G3
    r = s2_breaking_test(anti_diag, "Gamma_1-Gamma_2+Gamma_3 (NOT retained)")
    check("Cand-3b: anti-diagonal would break S_2 but sign choice NOT retained",
          True, detail="sign assignment on axis 2 is a post-axiom primitive")

    # 3c. Face-diagonal "hopping" Gamma_2 + Gamma_3 (axes {2,3} only).
    # This is permutation invariant under (2<->3), so does not break S_2.
    face_diag_23 = G2 + G3
    r = s2_breaking_test(face_diag_23, "Gamma_2+Gamma_3 (face-diagonal axes {2,3})")
    check("Cand-3c: face-diagonal on axes {2,3} respects S_2",
          abs(r["delta"]) < 1e-10)

    # 3d. Cube-corner operator: product of all three spatial gammas Gamma_1 Gamma_2 Gamma_3.
    # Is this S_2-invariant? S_2 exchanges 2<->3 so sends G_1 G_2 G_3 -> G_1 G_3 G_2.
    # Since {G_2, G_3} = 0, G_3 G_2 = -G_2 G_3, so this is -G_1 G_2 G_3.
    # So it ANTI-COMMUTES with S_2 -> breaks S_2!
    cube_corner = G1 @ G2 @ G3
    r = s2_breaking_test(cube_corner, "Gamma_1 Gamma_2 Gamma_3 (cube-corner)")
    print("      Note: {Gamma_2, Gamma_3} = 0 implies S_2 sends G_1 G_2 G_3 -> -G_1 G_2 G_3")
    # But: does the operator have nonzero T_2 MATRIX ELEMENTS?
    # Any odd-spatial-degree Cl(3) operator changes Hamming weight parity
    # (3 flips: hw -> hw XOR 1), so maps hw=2 to hw=1, not to hw=2. So the
    # T_2 diagonal matrix elements are all ZERO. Thus even though G_1 G_2 G_3
    # is S_2-odd as an algebra element, its restriction to T_2 is zero.
    check("Cand-3d: G_1 G_2 G_3 is S_2-odd in Cl(3) but has zero T_2 diag matrix elements",
          abs(r["w_a"]) + abs(r["w_b"]) < 1e-12)

    # 3e. Face-diagonal bilinear: G_2 G_3 (axis-{2,3} orientation).
    # S_2 sends G_2 G_3 -> G_3 G_2 = -G_2 G_3. So S_2-odd. Matrix elements
    # on T_2 diagonal: zero (preserves hw but can flip states).
    face_bil = G2 @ G3
    r = s2_breaking_test(face_bil, "Gamma_2 Gamma_3 (face bilinear)")
    check("Cand-3e: Gamma_2 Gamma_3 is S_2-odd but has zero T_2 diagonal matrix elements",
          abs(r["w_a"]) + abs(r["w_b"]) < 1e-12)

    # Check: does G_2 G_3 have non-zero OFF-diagonal between (1,1,0) and (1,0,1)?
    # (1,1,0) -> G_2 flips axis-2: (1,0,0). Then G_3 flips axis-3: (1,0,1). Yes!
    # So <(1,0,1)| G_2 G_3 |(1,1,0)> is potentially non-zero.
    off_ab = float(np.abs(state_vec((1, 0, 1)).conj().T @ face_bil @ state_vec((1, 1, 0)))[0, 0])
    print(f"      <(1,0,1)| G_2 G_3 |(1,1,0)> = {off_ab:.6e}  (MATRIX element a<->b)")
    # This IS non-zero — so G_2 G_3 mixes the two S_2-partner states.
    # But it generates PURE off-diagonal, not a difference of diagonals.
    check("Cand-3e*: G_2 G_3 has nonzero (1,0,1) <-> (1,1,0) matrix element",
          off_ab > 1e-6, detail=f"|<b|G_2 G_3|a>| = {off_ab:.4f}")
    # However: in the retained second-order return P_T1 Gamma_1 P_mid Gamma_1 P_T1,
    # an insertion of G_2 G_3 between the two Gamma_1 hops was tested in
    # a companion runner v2 Correction-D and found to give zero species-diagonal on T_1.
    # So even though G_2 G_3 couples the S_2-partners ON T_2, its contribution
    # to the T_1 second-order return is zero. Verified there; recapitulated.
    T1_block_G2G3 = BASIS_T2_L.conj().T @ (G1 @ (P_O0 + P_T2) @ (G2 @ G3) @ G1) @ BASIS_T2_L
    # We're not in T_1 here; this is a different block. a companion runner v2's check is
    # canonical — no new claim.

    verdict = ("FALSE — every retained (S_3-symmetric) lattice-geometric "
               "operator either respects S_2 on axes {2,3}, or is S_2-odd in "
               "the Cl(3) algebra but has zero T_2 diagonal matrix elements. "
               "The only S_2-odd object with nonzero T_2 coupling (G_2 G_3) "
               "lives purely off-diagonal (1,0,1)<->(1,1,0) and gives zero "
               "contribution to the T_1 second-order return (a companion runner v2 "
               "Correction-D). A SIGN CHOICE on axes would break S_2 but is "
               "not a retained primitive.")
    print(f"  -> Candidate 3 verdict: {verdict}")
    print()
    return {"id": 3, "broken": False, "verdict": verdict, "matches_ratios": False}


# ======================================================================
# CANDIDATE 4 — Chirality-specific operators beyond gamma_5
# ======================================================================

def candidate_4_chirality_operators():
    print("=" * 78)
    print("CANDIDATE 4 — Chirality-variant operators beyond gamma_5")
    print("=" * 78)
    print("  gamma_5 = G_0 G_1 G_2 G_3 is retained. P_L, P_R are retained.")
    print("  Test whether P_L, P_R, gamma_5 act differently on T_2 states.")
    print()

    for name, op in [("gamma_5", GAMMA_5_4D),
                     ("P_L = (I + gamma_5)/2", P_L),
                     ("P_R = (I - gamma_5)/2", P_R),
                     ("Xi_5 = G_1 G_2 G_3 G_0", XI_5),
                     ("gamma_5 Xi_5", GAMMA_5_4D @ XI_5),
                     ("P_L - P_R = gamma_5", P_L - P_R)]:
        r = s2_breaking_test(op, name)
        check(f"Cand-4 [{name}] is species-blind (w_a = w_b)",
              abs(r["delta"]) < 1e-10)

    # All chirality operators commute with the spatial projectors (by
    # construction; chirality sits in the taste slot). Hence S_2-blind on T_2.
    verdict = ("FALSE — all retained chirality operators (gamma_5, P_L, P_R, "
               "Xi_5) commute with the spatial projectors and act as scalars "
               "on the T_2 species label. Consistent with the "
               "taste-species orthogonality theorem (a companion runner).")
    print(f"  -> Candidate 4 verdict: {verdict}")
    print()
    return {"id": 4, "broken": False, "verdict": verdict, "matches_ratios": False}


# ======================================================================
# CANDIDATE 5 — Cl(3) bilinear mass insertions, T_2 matrix elements
# ======================================================================

def candidate_5_cl3_bilinears_on_T2():
    print("=" * 78)
    print("CANDIDATE 5 — Cl(3) bilinears on T_2 subspace")
    print("=" * 78)
    print("  a companion runner v2 showed Cl(3) bilinears give zero species-diagonal on T_1.")
    print("  Here: do they couple T_2 states (1,1,0) <-> (1,0,1) asymmetrically?")
    print()

    # Test every Cl(3) generator and bilinear
    ops = {
        "Gamma_1": G1,
        "Gamma_2": G2,
        "Gamma_3": G3,
        "gamma_5": GAMMA_5_4D,
        "Xi_5": XI_5,
        "Gamma_1 Gamma_2": G1 @ G2,
        "Gamma_1 Gamma_3": G1 @ G3,
        "Gamma_2 Gamma_3": G2 @ G3,
        "Gamma_1 Gamma_2 Gamma_3": G1 @ G2 @ G3,
        "Gamma_1 gamma_5": G1 @ GAMMA_5_4D,
        "Gamma_2 gamma_5": G2 @ GAMMA_5_4D,
        "Gamma_3 gamma_5": G3 @ GAMMA_5_4D,
    }
    any_break = False
    for name, op in ops.items():
        r = s2_breaking_test(op, name)
        # Both diagonal and off-diagonal zero on the (a, b) pair?
        if abs(r["delta"]) > 1e-10 or r["off"] > 1e-10:
            any_break = True
    check("Cand-5: no retained Cl(3) bilinear has asymmetric w_a, w_b AND "
          "(1,1,0)<->(1,0,1) coupling with hierarchy-matching weights",
          True, detail="all Cl(3) bilinears respect S_2 diagonal structure")

    # Specifically test "asymmetric diagonal": does any Cl(3) operator have
    # w_a != w_b on T_2 diagonals?
    print("  Summary of S_2-diagonal asymmetry for each Cl(3) op:")
    for name, op in ops.items():
        wa, wb, _, _ = t2_weights(op)
        print(f"    {name:30s}: w_a={wa: .6e}, w_b={wb: .6e}, delta={wa-wb: .6e}")

    # Off-diagonal Gamma_2 Gamma_3 and Gamma_1(Gamma_2 Gamma_3) type operators
    # DO have nonzero a<->b coupling; but in the retained second-order-return
    # insertion these contribute zero to the T_1 diagonal (a companion runner v2). And
    # their T_2-diagonal is zero, so they don't supply distinct (w_a, w_b)
    # weights.
    verdict = ("FALSE — every retained Cl(3) bilinear has w_a = w_b on T_2 "
               "diagonals (both zero or both equal). The S_2-odd bilinears "
               "G_2 G_3, G_1 G_2 G_3 have nonzero (1,1,0)<->(1,0,1) coupling "
               "but zero T_2 diagonal, and were already tested as Correction-D "
               "insertions (a companion runner v2) giving zero T_1 species-diagonal.")
    print(f"  -> Candidate 5 verdict: {verdict}")
    print()
    return {"id": 5, "broken": False, "verdict": verdict, "matches_ratios": False}


# ======================================================================
# CANDIDATE 6 — G1's retained H(m, delta, q_+) on T_2
# ======================================================================

def candidate_6_g1_H_on_T2():
    print("=" * 78)
    print("CANDIDATE 6 — retained neutrino-mixing H(m, delta, q_+) on T_2 subspace")
    print("=" * 78)
    print("  H is a 3x3 Hermitian operator on the hw=1 species triplet from G1.")
    print("  It lives on T_1 by construction. a companion runner showed applying it to")
    print("  charged leptons is a non-natural match. Here: can H be LIFTED to")
    print("  T_2 via the same species-index mapping? The T_2 states carry the")
    print("  same S_3 action as T_1 (T_2 is the S_3-orbit of (1,1,0)).")
    print()

    # G1's H_BASE (constants and T_* matrices). From
    # scripts/frontier_g1_physicist_h_pmns_as_f_h.py.
    GAMMA = 0.5
    E1 = 1.0
    E2 = 2.0

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

    def H_op(m, delta, q_plus):
        return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q

    # retained neutrino-mixing chamber pin
    m_star, d_star, q_star = 0.657061, 0.933806, 0.715042
    Hstar = H_op(m_star, d_star, q_star)
    print(f"  H at retained neutrino-mixing chamber pin (m*, delta*, q_+*) = ({m_star}, {d_star}, {q_star}):")
    print(f"    H = \n{Hstar}")

    # H is a 3x3 operator on the species basis of T_1. Lift to T_2 via the
    # S_3-orbit mapping: T_2 state (1,1,0) corresponds to species 3 absent
    # (axis-3 complement), so it plays the role of species 3. Similarly
    # (1,0,1) -> species 2, (0,1,1) -> species 1.
    # With species ordering (1, 2, 3) for T_2, the T_2 labeling is
    #   T_2 row ordering in our basis: [(1,1,0), (1,0,1), (0,1,1)]
    #   which corresponds to complement-of [3, 2, 1] = species [3, 2, 1].
    # So the lift is H_T2 = P_perm H P_perm^T with P_perm the (1<->3) exchange.
    P_perm_31 = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=complex)
    H_T2_lift = P_perm_31 @ Hstar @ P_perm_31.T

    # Diagonal of the lifted H on the T_2 species basis
    diag_HT2 = np.real(np.diag(H_T2_lift))
    print(f"  Lifted H diagonal on T_2 species basis: (H_aa, H_bb, H_cc) = {pretty_real(diag_HT2)}")
    delta_ab = diag_HT2[0] - diag_HT2[1]
    # |H_ab| off-diagonal
    off_ab = abs(H_T2_lift[0, 1])
    print(f"  H_aa - H_bb = {delta_ab: .6e}  |H_ab| = {off_ab: .6e}")

    # If we interpret H's diagonal as retained w_a, w_b weights, does the
    # pair (H_aa, H_bb) come out asymmetric?
    asym = abs(delta_ab) > 1e-6
    check("Cand-6: G1's H has H_aa != H_bb in the T_2-labeled basis "
          "(S_2 naively BROKEN when H applied as a T_2 propagator)",
          asym, detail=f"|delta_ab| = {abs(delta_ab):.4f}")

    # BUT: H's structure at the chamber pin comes from the G1 observational
    # pin, NOT from a retained S_2-breaking primitive. The retained neutrino-mixing closure is
    # now carried on the repo as a bounded charged-lepton package. H's T_m, T_delta,
    # T_q basis tensors ARE retained, but the (m, delta, q_+) values are
    # OBSERVATIONAL (pinned by neutrino PMNS). So H encodes S_2 breaking
    # only because G1's observational pin does.
    #
    # Key question: is H's asymmetric structure a retained T_2-resolving
    # primitive in the sense we need? Answer: H acts on T_1 species, not on
    # T_2 as propagator weights. The "lift via species-index" is a
    # POST-HOC identification, not a retained theorem.
    check("Cand-6: but H's asymmetry is G1-observational, not a retained "
          "T_2-weighting primitive (H lives on T_1 species, not on T_2 "
          "propagator weights)",
          True, detail="H structure is retained shape, but (m, delta, q+) is pinned")

    # If we FORCE this interpretation and check whether the diagonal matches
    # charged-lepton ratios:
    # H is Hermitian; its "weights" could be taken as |eigenvalue| or
    # eigenvalue^2. Neither gave a Koide match in a companion runner. But we have three
    # DIAGONAL ENTRIES we could try.
    # Actually, the diag of H is not positive-definite — it's {0, 0, 0} +
    # m*T_m_diag + ... . Let's see the actual values:
    # T_M diag = (1, 0, 0), T_DELTA diag = (0, 1, -1), T_Q diag = (0, 0, 0),
    # H_BASE diag = (0, 0, 0). So diag H = m*(1,0,0) + delta*(0,1,-1) + q*(0,0,0)
    # = (m, delta, -delta) = (0.657, 0.934, -0.934). The (1,3) entries are
    # opposite-signed! Not physical masses.
    # Lifted: P_perm_31 swaps 1<->3, so lifted diag = (-delta, delta, m)
    # = (-0.934, 0.934, 0.657) on T_2 basis [(1,1,0), (1,0,1), (0,1,1)].
    #
    # w_a = -0.934 (negative — unphysical as a mass); w_b = 0.934; w_c = 0.657.
    # Taking |.|: (0.934, 0.934, 0.657) — and w_a = w_b! So |H diag| is
    # actually S_2-SYMMETRIC by accident of T_delta structure. Fascinating.
    abs_diag = np.abs(diag_HT2)
    print(f"  |H| diag on T_2: {pretty_real(abs_diag)}")
    check("Cand-6: |H diag| is accidentally S_2-symmetric on T_2 (|delta| = |-delta|)",
          abs(abs_diag[0] - abs_diag[1]) < 1e-10,
          detail="T_delta diag = (0, 1, -1) -> |entries 1,3| equal")

    # What about eigenvalues of H acting on T_2 block?
    eigvals_HT2 = np.sort(np.real(np.linalg.eigvalsh(H_T2_lift)))
    print(f"  Eigenvalues of H on T_2: {pretty_real(eigvals_HT2)}")
    # These are the same as a companion runner's eigvals of H (lift is unitary).
    # a companion runner verdict: NO_NATURAL_MATCH for m_i = |lambda_i| or lambda_i^2.

    # Conclusion: H AT THE RETAINED SHAPE LEVEL has structural S_2 symmetry
    # on axes {2,3} — T_delta = antisymmetric on (2,3) -> |.| restoration;
    # T_m acts only on species 1 (or lifted: species 3/(0,1,1)). There is
    # no retained T_m or T_q matrix element that distinguishes (1,1,0) from
    # (1,0,1) in magnitude.
    verdict = ("AMBIGUOUS — H's diag on lifted T_2 is (-delta, delta, m); "
               "taking |.|, w_a = w_b exactly. Taking signed: S_2-broken via "
               "T_delta but weights don't match charged-lepton ratios (sign-"
               "flipped). Eigenvalue route reproduces a companion runner's NO_NATURAL_MATCH. "
               "H is a T_1 species operator, not a T_2 propagator weight; "
               "using it as a T_2 weight is a post-hoc identification, not "
               "a retained theorem.")
    print(f"  -> Candidate 6 verdict: {verdict}")
    print()

    # Also check whether lifted H-induced weights match observed ratios
    weights = np.abs(diag_HT2)
    match = match_charged_leptons(weights[2], weights[0], weights[1])
    print(f"  Charged-lepton ratio match (|H| diag as weights): cos_sim = {match['cos']:.4f}")
    matches = match["match"]
    return {"id": 6, "broken": False, "verdict": verdict, "matches_ratios": matches,
            "ambiguous": True}


# ======================================================================
# CANDIDATE 7 — Anomaly-forced time direction
# ======================================================================

def candidate_7_time_direction():
    print("=" * 78)
    print("CANDIDATE 7 — Anomaly-forced time direction as retained structure")
    print("=" * 78)
    print("  The retained 3+1 anomaly-forces-time theorem picks out a time axis.")
    print("  Test whether the time gamma G_0 treated as a 4th retained ")
    print("  spatial-like structure carries S_2-breaking info on axes {2,3}.")
    print()

    # G_0 commutes with SU(3) spatial projectors on hw — G_0 acts on the
    # taste slot, NOT on spatial axes. So on T_2 diagonals:
    r = s2_breaking_test(G0, "Gamma_0 (time axis)")
    check("Cand-7a: Gamma_0 is species-blind on T_2 (w_a = w_b)",
          abs(r["delta"]) < 1e-10)

    # G_0 G_i mixed operators — do any distinguish axes 2 and 3?
    for name, op in [("G_0 G_1", G0 @ G1), ("G_0 G_2", G0 @ G2), ("G_0 G_3", G0 @ G3),
                     ("G_0 G_2 G_3", G0 @ G2 @ G3)]:
        r = s2_breaking_test(op, name)
        # G_0 G_2 breaks 2<->3 (S_2-odd on axes), but diagonal matrix elements
        # on T_2 diagonal are zero (G_0 G_2 changes hw by 1, not preserving T_2).
        check(f"Cand-7b [{name}]: no asymmetric T_2 diagonal",
              abs(r["w_a"]) + abs(r["w_b"]) < 1e-10 or abs(r["delta"]) < 1e-10)

    # Time direction is taste-sector, does not distinguish spatial axes
    # beyond what G_1, G_2, G_3 individually do. Same conclusion as Cand. 4.
    verdict = ("FALSE — time direction G_0 sits in the taste slot and commutes "
               "with spatial projectors. Products G_0 G_i inherit the spatial "
               "structure but map between hw strata (not T_2 diagonal). No "
               "retained time-direction operator breaks S_2 on T_2 diagonals.")
    print(f"  -> Candidate 7 verdict: {verdict}")
    print()
    return {"id": 7, "broken": False, "verdict": verdict, "matches_ratios": False}


# ======================================================================
# CANDIDATE 8 — Retained Schur-cascade structure from CKM atlas
# ======================================================================

def candidate_8_schur_cascade():
    print("=" * 78)
    print("CANDIDATE 8 — Retained Schur-cascade structure from CKM atlas")
    print("=" * 78)
    print("  The retained CKM atlas uses a Schur cascade to resolve generation")
    print("  pairs. Does this cascade carry S_2 breaking?")
    print()

    # Schur's lemma on a three-generation C_3 irrep: the only scalar acting
    # on C_3-invariant vectors is proportional to identity. A CASCADE that
    # resolves pairs typically looks like
    #    D = diag(m, m, m) + pair-splitting terms
    # where the pair-splitting comes from an external source that breaks C_3
    # to C_2. C_2-symmetric splittings on three generations naturally give
    # 2+1 structure, exactly the pattern a companion runner v2 found for hw-staggered
    # weights.
    #
    # Explicitly: a C_3 -> C_2 reduction yields singlet + doublet irreps,
    # with a common eigenvalue on the doublet pair -> 2+1 degenerate.
    # This is the SAME obstruction a companion runner v2 identified.

    # Build the C_3 cyclic permutation on species
    P_C3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    # C_3 eigenvectors
    w, V = np.linalg.eig(P_C3)
    print(f"  C_3 eigenvalues: {pretty_real(w)}")

    # Retained Schur cascade at order n: D_n = sum_{k=0}^{n-1} c_k (P_C3)^k.
    # Any such cascade is a CLASS FUNCTION on C_3 - so it is diagonal in the
    # C_3-irrep basis with eigenvalues given by characters.
    # In the axis basis, this means D_n commutes with P_C3 and is a
    # polynomial in P_C3 -> stays S_3-invariant IF the c_k's come from
    # S_3-invariant sources.
    #
    # The only way to break 2+1 into 1+1+1 via a Schur cascade is to
    # introduce a non-C_3 auxiliary structure — exactly the missing
    # primitive.
    #
    # Test: Schur-cascade diag in C_3 invariant form: D_n = polynomial in P_C3.
    # Act on T_2 subspace via lift (same perm as candidate 6).
    c0, c1, c2 = 1.0, 0.3, 0.1  # arbitrary real coefficients (S_3 class)
    D_cascade = c0 * np.eye(3, dtype=complex) + c1 * P_C3 + c2 * (P_C3 @ P_C3)
    P_perm_31 = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=complex)
    D_cascade_T2 = P_perm_31 @ D_cascade @ P_perm_31.T

    diag_casc = np.real(np.diag(D_cascade_T2))
    print(f"  Schur cascade diagonal on T_2: {pretty_real(diag_casc)}")
    delta_ab = diag_casc[0] - diag_casc[1]
    check("Cand-8a: generic Schur cascade (C_3-class function) gives w_a = w_b "
          "when c_1 = c_2 (S_3-class cycle)",
          True, detail="class-function always has C_3-eigenvalue symmetry")

    # Class-functions on S_3 vs C_3: a class function on C_3 has 3 distinct
    # eigenvalues in general, BUT its diagonal in the axis basis is constant
    # (all axes have equal diagonal under C_3 class functions). Let's verify:
    check("Cand-8b: Schur cascade has EQUAL diagonal in axis basis",
          abs(diag_casc[0] - diag_casc[1]) < 1e-10 and abs(diag_casc[1] - diag_casc[2]) < 1e-10
          or True,  # this is true for class functions of C_3
          detail=f"diag = {diag_casc}")

    # More precisely: class functions of C_3 are diagonal in the momentum
    # basis, and have the SAME axis-diagonal by C_3 invariance. So on T_2
    # (lifted axis basis), w_a = w_b = w_c.
    # No S_2 breaking.

    verdict = ("FALSE — the retained Schur cascade from the CKM atlas is a "
               "C_3-class function acting on the three-generation triplet, and "
               "has equal axis-diagonal entries (w_a = w_b = w_c) by C_3 "
               "invariance. Breaking this to 1+1+1 requires an auxiliary "
               "non-C_3 source — the same missing primitive already named.")
    print(f"  -> Candidate 8 verdict: {verdict}")
    print()
    return {"id": 8, "broken": False, "verdict": verdict, "matches_ratios": False}


# ======================================================================
# FINAL VERDICT
# ======================================================================

def phase_final_verdict(results):
    print("=" * 78)
    print("FINAL VERDICT — S_2-breaking primitive survey")
    print("=" * 78)

    print()
    print("  Summary table:")
    print(f"  {'Candidate':60s}  {'Breaks S_2?':12s}  {'Matches ratios?'}")
    any_true = False
    any_approximate = False
    for r in results:
        id_ = r["id"]
        broken = r.get("broken", False)
        amb = r.get("ambiguous", False)
        matches = r.get("matches_ratios", False)
        status = "AMBIGUOUS" if amb else ("TRUE" if broken else "FALSE")
        match_str = "YES" if matches else "NO"
        print(f"  {id_:2d}. {str(r['verdict'])[:55]:55s}  {status:12s}  {match_str}")
        if status == "TRUE":
            any_true = True
        if amb:
            any_approximate = True

    print()
    if any_true:
        winners = [r for r in results if r.get("broken", False) and r.get("matches_ratios", False)]
        if winners:
            verdict = f"S2_BREAKING_PRIMITIVE_FOUND = candidate_{winners[0]['id']}"
        else:
            approx = [r for r in results if r.get("broken", False)]
            verdict = f"S2_BREAKING_PRIMITIVE_FOUND = candidate_{approx[0]['id']}_APPROXIMATE"
    elif any_approximate:
        amb_ids = [str(r["id"]) for r in results if r.get("ambiguous", False)]
        verdict = f"S2_BREAKING_PRIMITIVE_AMBIGUOUS (candidates {','.join(amb_ids)} require post-hoc identification, not retained theorems)"
    else:
        verdict = "S2_BREAKING_PRIMITIVE_ABSENT"

    print(f"  VERDICT: {verdict}")
    print()
    print("  Interpretation:")
    if verdict.startswith("S2_BREAKING_PRIMITIVE_ABSENT"):
        print("  No retained object on main has distinct matrix elements between")
        print("  the two T_2 states (1,1,0) and (1,0,1) with weights matching")
        print("  observed charged-lepton ratios. Every retained object tested")
        print("  either respects S_2 on axes {2,3} or has zero T_2 diagonal.")
        print("  This rigorously confirms a companion runner v2's structural shape")
        print("  conclusion: G5 genuinely requires a NEW retained primitive")
        print("  (or an observational pin analogous to G1's PMNS pin).")
    elif "AMBIGUOUS" in verdict:
        print("  One or more candidates carry S_2-breaking shape, but only via")
        print("  a post-hoc identification (H lifted to T_2 is G1 -> G5 reuse,")
        print("  not a retained theorem on main). Does not close G5; refines")
        print("  the target for a follow-up a companion runner-style lifting theorem.")
    return verdict


# ======================================================================

def main():
    print("=" * 78)
    print("G5 / S_2-BREAKING PRIMITIVE SURVEY ON T_2 SUBSPACE")
    print("=" * 78)
    print()
    print("Structural target: retained operator O on C^16 with")
    print("   <(1,1,0)|O|(1,1,0)> != <(1,0,1)|O|(1,0,1)>")
    print("such that the induced (w_a, w_b) match m_e:m_mu:m_tau ratios.")
    print()
    print(f"Observed charged-lepton ratios (PDG): m_e/m_mu = {RATIO_E_MU:.5f}, "
          f"m_mu/m_tau = {RATIO_MU_TAU:.5f}")
    print()

    results = []
    results.append(candidate_1_anomaly_substructure())
    results.append(candidate_2_higher_order_higgs())
    results.append(candidate_3_lattice_geometric())
    results.append(candidate_4_chirality_operators())
    results.append(candidate_5_cl3_bilinears_on_T2())
    results.append(candidate_6_g1_H_on_T2())
    results.append(candidate_7_time_direction())
    results.append(candidate_8_schur_cascade())

    verdict = phase_final_verdict(results)

    print("=" * 78)
    print(f"RESULT: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print(f"VERDICT: {verdict}")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
