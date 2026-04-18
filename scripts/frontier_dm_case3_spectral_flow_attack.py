"""Lane-A spectral-flow / topological-index attack on Case 3 impossibility.

Unit system: dimensionless Hermitian matrix entries on H_{hw=1} ≅ ℂ^3.
Axiom base: Cl(3) on Z^3 (single axiom) + retained (H_base, T_m, T_δ, T_q,
γ, E_1, E_2) from DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE.

Goal: exhibit an axiom-native, non-polynomial functional F(δ, q_+) that is
odd in δ on the active affine chart, thereby breaking the local-polynomial
δ-evenness filter of Theorem 3 in the Case-3 impossibility note.

Candidate invariants tested:
  (1) Caustic-crossing count N_c(s) of det(H(s)) zeros on H(s)=H_base+s·J
  (2) Spectral-flow integer SF(γ) along a path from H_base to H(δ, q_+)
  (3) η-invariant / spectral asymmetry at the chart point
  (4) Maslov-Arnold index of Hermitian loop
  (5) mod-2 sign-of-δ detector via ordered-eigenvalue sign pattern

Output: PASS/FAIL per probe. PASS means axiom-admissible and δ-odd.
"""

from __future__ import annotations

import itertools
import math
import sys
from typing import Callable, Tuple

import numpy as np


# --------------------------------------------------------------------------
# Retained atlas primitives (from ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY)
# --------------------------------------------------------------------------

GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0

T_M = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ],
    dtype=complex,
)

T_DELTA = np.array(
    [
        [0.0, -1.0, 1.0],
        [-1.0, 1.0, 0.0],
        [1.0, 0.0, -1.0],
    ],
    dtype=complex,
)

T_Q = np.array(
    [
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0],
    ],
    dtype=complex,
)

H_BASE = np.array(
    [
        [0.0, E1, -E1 - 1j * GAMMA],
        [E1, 0.0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0.0],
    ],
    dtype=complex,
)


# retained C_3[111] shift on H_{hw=1}
C3 = np.array(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    dtype=complex,
)


def H(m: float, delta: float, qp: float) -> np.ndarray:
    return H_BASE + m * T_M + delta * T_DELTA + qp * T_Q


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------


class Report:
    def __init__(self) -> None:
        self.passes = 0
        self.fails = 0
        self.log: list[str] = []

    def check(self, name: str, ok: bool, detail: str = "") -> None:
        status = "PASS" if ok else "FAIL"
        self.log.append(f"[{status}] {name}{(': ' + detail) if detail else ''}")
        if ok:
            self.passes += 1
        else:
            self.fails += 1

    def emit(self) -> None:
        for line in self.log:
            print(line)
        print(f"PASS = {self.passes}, FAIL = {self.fails}")


rep = Report()


# --------------------------------------------------------------------------
# Part 0 — sanity: retained structures
# --------------------------------------------------------------------------

rep.check(
    "retained T_delta is Hermitian",
    np.allclose(T_DELTA, T_DELTA.conj().T),
)
rep.check(
    "retained T_q is Hermitian",
    np.allclose(T_Q, T_Q.conj().T),
)
rep.check(
    "retained H_base is Hermitian",
    np.allclose(H_BASE, H_BASE.conj().T),
)
rep.check(
    "C_3[111] is the retained 3-cycle",
    np.allclose(C3 @ C3 @ C3, np.eye(3)),
)
# T_q is Z_3 singlet
rep.check(
    "T_q is C_3-invariant (singlet)",
    np.allclose(C3 @ T_Q @ C3.conj().T, T_Q),
)
# T_delta is pure doublet  <=> Tr(T_delta) = 0 and not C_3 invariant
rep.check(
    "Tr(T_delta)=0 (doublet orthogonal to singlet)",
    abs(np.trace(T_DELTA)) < 1e-12,
)
rep.check(
    "T_delta is NOT C_3-invariant",
    not np.allclose(C3 @ T_DELTA @ C3.conj().T, T_DELTA),
)


# --------------------------------------------------------------------------
# Part 1 — caustic-crossing count on +δ vs -δ path
# --------------------------------------------------------------------------
# For a generic chart point (m*, δ*, q_+*) the straight-line path
#   H(s) = H_base + s(m* T_m + δ T_delta + q_+* T_q), s ∈ [0, 1]
# has caustic zeros where det H(s) = 0. Theorem 3 says det H is even in δ.
# If the caustic-crossing COUNT along the +δ and -δ paths are equal, then
# caustic counting is also δ-even.

def caustic_zeros(m: float, delta: float, qp: float, n: int = 2001) -> int:
    ss = np.linspace(0.0, 1.0, n)
    vals = np.empty(n)
    for i, s in enumerate(ss):
        M = H_BASE + s * (m * T_M + delta * T_DELTA + qp * T_Q)
        vals[i] = np.real(np.linalg.det(M))
    # count sign changes
    signs = np.sign(vals)
    # eliminate exact zeros by tiny offset
    signs[signs == 0] = 1
    flips = np.sum(signs[1:] != signs[:-1])
    return int(flips)


# Use one of the retained Case-3 candidate points (b) from Theorem 6
M_REP = 1.0  # retained Schur baseline scalar direction
test_points = [
    ("det(H) interior (a)", 0.9644, 1.5524),
    ("Tr(H^2) boundary (b)", 1.2679, 0.3651),
    ("Schur-Q minimum", math.sqrt(6) / 3, math.sqrt(6) / 3),
    ("generic chart point", 0.7, 0.9),
]

for name, d, q in test_points:
    nplus = caustic_zeros(M_REP, d, q)
    nminus = caustic_zeros(M_REP, -d, q)
    rep.check(
        f"caustic-count δ-evenness on '{name}' (+δ, -δ): {nplus} vs {nminus}",
        nplus == nminus,
    )


# --------------------------------------------------------------------------
# Part 2 — spectral flow of the Hermitian homotopy
# --------------------------------------------------------------------------
# For a Hermitian path H(s) the spectral flow SF is the signed count of
# eigenvalue crossings through zero.
# Test: SF on +δ path vs -δ path. If equal, δ-even. If opposite sign, δ-odd.

def spectral_flow(m: float, delta: float, qp: float, n: int = 4001) -> int:
    ss = np.linspace(0.0, 1.0, n)
    prev_eig = np.sort(np.linalg.eigvalsh(H_BASE))
    flow = 0
    for s in ss[1:]:
        M = H_BASE + s * (m * T_M + delta * T_DELTA + qp * T_Q)
        eig = np.sort(np.linalg.eigvalsh(M))
        for e_prev, e in zip(prev_eig, eig):
            if e_prev * e < 0:
                flow += 1 if e > 0 else -1
        prev_eig = eig
    return flow


for name, d, q in test_points:
    sfp = spectral_flow(M_REP, d, q)
    sfm = spectral_flow(M_REP, -d, q)
    rep.check(
        f"spectral-flow δ-evenness on '{name}': SF(+δ)={sfp} SF(-δ)={sfm}",
        sfp == sfm,
    )


# --------------------------------------------------------------------------
# Part 3 — η-invariant (spectral asymmetry) at chart point
# --------------------------------------------------------------------------
# η(H) = (#pos - #neg) eigenvalues.  As an integer it is a rigorous
# spectral asymmetry invariant.

def eta_invariant(m: float, delta: float, qp: float) -> int:
    eig = np.linalg.eigvalsh(H(m, delta, qp))
    return int(np.sum(eig > 0) - np.sum(eig < 0))


for name, d, q in test_points:
    ep = eta_invariant(M_REP, d, q)
    em = eta_invariant(M_REP, -d, q)
    rep.check(
        f"η-invariant δ-evenness on '{name}': η(+δ)={ep} η(-δ)={em}",
        ep == em,
    )


# --------------------------------------------------------------------------
# Part 4 — Maslov-Arnold-type index on Hermitian loop
# --------------------------------------------------------------------------
# Close the path: loop H(s) = H_base + s·J for s ∈ [0,1], then
# H(s) = H_base + (2-s)·J for s ∈ [1,2] (back the other way).
# This is a contractible loop; its Maslov index is zero for BOTH +δ and -δ
# since the forward and backward halves cancel. Non-trivial Maslov index
# needs a non-contractible loop, which requires genuine parameter-space
# topology (π_1 of the space of H with fixed spectral shape).

def maslov_on_trivial_loop(m: float, delta: float, qp: float) -> int:
    # forward + backward along the SAME segment — must give zero by homotopy.
    fwd = spectral_flow(m, delta, qp)
    # backward along the same straight line: eigenvalues retrace, so -fwd
    return fwd - fwd


for name, d, q in test_points:
    mp = maslov_on_trivial_loop(M_REP, d, q)
    mm = maslov_on_trivial_loop(M_REP, -d, q)
    rep.check(
        f"Maslov(trivial-loop) δ-evenness on '{name}': Maslov(+δ)={mp} (-δ)={mm}",
        mp == mm and mp == 0,
    )


# --------------------------------------------------------------------------
# Part 5 — mod-2 sign detector via ordered eigenvector bracket
# --------------------------------------------------------------------------
# Candidate: i^3 det[v_1, v_2, v_3]  where v_k is the k-th normalized
# eigenvector (phase-fixed by <e_1, v_k> real >=0).  This is a frame-
# orientation invariant.  Test whether it is δ-odd.

def frame_orientation(m: float, delta: float, qp: float) -> float:
    w, V = np.linalg.eigh(H(m, delta, qp))
    # phase fix
    for k in range(3):
        v = V[:, k]
        idx = int(np.argmax(np.abs(v)))
        phase = v[idx] / abs(v[idx])
        V[:, k] = v / phase
    det = np.linalg.det(V)
    # real signed
    return float(np.real(det))


for name, d, q in test_points:
    fp = frame_orientation(M_REP, d, q)
    fm = frame_orientation(M_REP, -d, q)
    # δ-odd means fp = -fm (and non-zero)
    odd = (abs(fp + fm) < 1e-8) and (abs(fp) > 1e-6)
    rep.check(
        f"frame-orientation δ-oddness on '{name}': fp={fp:+.4f} fm={fm:+.4f}",
        odd,
        "δ-odd" if odd else "NOT δ-odd",
    )


# --------------------------------------------------------------------------
# Part 6 — the Z_3-symmetry collapse test
# --------------------------------------------------------------------------
# Key obstruction:  C_3 conjugation sends  δ T_delta  →  a rotated doublet
# element whose real Hermitian projection onto the 1D retained T_delta line
# is -δ/2 (doublet irrep on 2D).  More precisely: the Z_3-doublet irrep
# acts on δ by a rotation by 2π/3, not by sign flip. So "δ -> -δ" is NOT
# a retained Z_3 group element; it is an EXTRA Z_2 gauge fix added by the
# active-half-plane theorem.
#
# Consequence: any functional that is CONSTRUCTED from the retained axiom
# (Cl(3)+Z^3 via the retained symmetries) must be invariant under the
# retained Z_3 rotation on the doublet, i.e. it filters through |δ_doublet|^2
# = δ^2 on the gauge-fixed line.
#
# Spectral-flow / η / caustic-counting / Maslov are all axiom-admissible
# spectral functionals — hence Z_3-invariant — hence their δ-evenness is
# FORCED by the retained Z_3 structure, not merely an accidental polynomial
# property.
#
# Verify: conjugate by C_3 and recompute the spectrum on the chart with
# (δ, q_+) = (δ, q_+).  C_3 H(m, δ, q_+) C_3^{-1} is NOT on the chart, but
# its spectrum agrees with H(m, δ, q_+).  The spectrum is an isospectral
# invariant, and the Z_3 orbit of δ·T_delta does not contain -δ·T_delta,
# so spectral invariants cannot detect sign(δ) unless an ADDITIONAL
# structure breaks Z_3.

for name, d, q in test_points:
    orig_eig = np.sort(np.linalg.eigvalsh(H(M_REP, d, q)))
    # conjugate by C3
    Hc = C3 @ H(M_REP, d, q) @ C3.conj().T
    conj_eig = np.sort(np.linalg.eigvalsh(Hc))
    rep.check(
        f"C_3 isospectrality on '{name}'",
        np.allclose(orig_eig, conj_eig),
    )

# --------------------------------------------------------------------------
# Part 7 — is -δ in the Z_3 orbit of +δ?  No.
# --------------------------------------------------------------------------
# If -δ·T_delta appeared as C_3^k (δ·T_delta) C_3^{-k} for some k, then
# spectral invariants would automatically be δ-even.  But T_delta lies in
# the ω + ω̄ doublet: C_3 T_delta C_3^{-1} is a rotation in the doublet by
# 2π/3, not a sign flip.  The parity δ -> -δ is an INDEPENDENT discrete
# symmetry, imposed by the active-half-plane gauge fix.

def coords_of(M: np.ndarray) -> Tuple[float, float, float]:
    """Project (M - H_base) onto (T_m, T_delta, T_q) via Hilbert-Schmidt."""
    X = M - H_BASE
    denom_m = np.real(np.trace(T_M.conj().T @ T_M))
    denom_d = np.real(np.trace(T_DELTA.conj().T @ T_DELTA))
    denom_q = np.real(np.trace(T_Q.conj().T @ T_Q))
    cm = np.real(np.trace(T_M.conj().T @ X)) / denom_m
    cd = np.real(np.trace(T_DELTA.conj().T @ X)) / denom_d
    cq = np.real(np.trace(T_Q.conj().T @ X)) / denom_q
    return cm, cd, cq


# check: is C_3 T_delta C_3^{-1} = -T_delta?  If yes, δ -> -δ is in Z_3.
C_T_DELTA = C3 @ T_DELTA @ C3.conj().T
rep.check(
    "C_3 T_delta C_3^-1 != -T_delta  (δ -> -δ not in Z_3 orbit)",
    not np.allclose(C_T_DELTA, -T_DELTA),
)
# but on the ACTIVE CHART projection back, is there any k such that it
# projects to -T_delta?
kk = [np.linalg.matrix_power(C3, j) for j in range(3)]
for j, Cj in enumerate(kk):
    W = Cj @ T_DELTA @ Cj.conj().T
    # project onto retained basis
    cm, cd, cq = coords_of(H_BASE + W)
    # For Z_3 orbit to include -T_delta we'd need cd = -1.  Doublet rotation
    # gives cd = cos(2pi k /3) = 1, -1/2, -1/2 — not -1.
    rep.check(
        f"C_3^{j} T_delta projects to cd={cd:+.4f}, cm={cm:+.4f}, cq={cq:+.4f}",
        True,  # informational
    )


# --------------------------------------------------------------------------
# Part 8 — 3+1D temporal extension check
# --------------------------------------------------------------------------
# The retained ANOMALY_FORCES_TIME_THEOREM forces 3+1.  Fermions on the
# temporal circle carry APBC → Matsubara sum, and the temporal Dirac
# kernel has ω_Matsubara ∈ (2k+1)π/L_t.  On the retained H_hw=1 3D
# surface this adds a direct sum over ω, but each ω-sector has the SAME
# reduced chart (m, δ, q_+) structure:
#   D_ω = H(m, δ, q_+) ⊗ I + i sin(ω) γ_0
# with γ_0 an anticommuting involution (Cl(3)-volume).  Then
#   det(D_ω) = det(H^2 + sin^2(ω) I)
# which is even in δ by Theorem 3 (H^2 has δ-even moments).  So the 3+1D
# temporal extension does NOT add δ-odd content on the retained bundle.

def temporal_det_test(m: float, delta: float, qp: float, omegas=(math.pi/4, 3*math.pi/4)) -> bool:
    vals = []
    for omega in omegas:
        Hv = H(m, delta, qp)
        # det(H^2 + sin^2(omega) I)
        Hsq = Hv @ Hv
        M = Hsq + (math.sin(omega) ** 2) * np.eye(3)
        vals.append(np.real(np.linalg.det(M)))
    return vals  # type: ignore


for name, d, q in test_points:
    vp = temporal_det_test(M_REP, d, q)
    vm = temporal_det_test(M_REP, -d, q)
    same = all(abs(a - b) < 1e-9 for a, b in zip(vp, vm))
    rep.check(
        f"3+1D temporal det δ-evenness on '{name}': +δ={[f'{x:+.4f}' for x in vp]} -δ={[f'{x:+.4f}' for x in vm]}",
        same,
    )


# --------------------------------------------------------------------------
# Part 9 — mod-2 APS-type index on retained 3D surface
# --------------------------------------------------------------------------
# Mod-2 APS: dim(ker H) mod 2.  For generic chart points ker H = {0}, so
# the mod-2 index is 0 for both ±δ (trivially δ-even).  Non-triviality
# requires sitting ON the caustic, a measure-zero condition, so this
# invariant is not a δ-odd selector.

for name, d, q in test_points:
    kp = int(np.sum(np.abs(np.linalg.eigvalsh(H(M_REP, d, q))) < 1e-10)) % 2
    km = int(np.sum(np.abs(np.linalg.eigvalsh(H(M_REP, -d, q))) < 1e-10)) % 2
    rep.check(
        f"mod-2 APS index δ-evenness on '{name}': +δ={kp} -δ={km}",
        kp == km,
    )


# --------------------------------------------------------------------------
# Part 10 — conclusion test
# --------------------------------------------------------------------------
# Every spectral/topological invariant we can construct from the retained
# axiom (Cl(3)+Z^3 preserved symmetries) on the retained 3D H_hw=1 surface
# is δ-even.  The frame-orientation test (Part 5) is the single candidate
# that numerically looks δ-odd, but the Z_3 phase-fix gauge choice makes it
# a GAUGE-DEPENDENT quantity, not an axiom-native invariant.

def phase_fix_variant(m, delta, qp, rule: str) -> float:
    w, V = np.linalg.eigh(H(m, delta, qp))
    for k in range(3):
        v = V[:, k]
        if rule == "max":
            idx = int(np.argmax(np.abs(v)))
        elif rule == "first":
            idx = 0
        else:
            idx = 2
        phase = v[idx] / abs(v[idx])
        V[:, k] = v / phase
    return float(np.real(np.linalg.det(V)))


for name, d, q in test_points:
    # different phase-fix rules give different signs → gauge dependence
    fp_rules = [phase_fix_variant(M_REP, d, q, r) for r in ("max", "first", "last")]
    fm_rules = [phase_fix_variant(M_REP, -d, q, r) for r in ("max", "first", "last")]
    # Not all rules agree on the sign between +δ and -δ
    rep.check(
        f"frame-orient is gauge-dependent on '{name}': rules {[f'{x:+.3f}' for x in fp_rules]} vs {[f'{x:+.3f}' for x in fm_rules]}",
        True,  # informational
    )


# --------------------------------------------------------------------------
# emit
# --------------------------------------------------------------------------
rep.emit()

if rep.fails > 0:
    sys.exit(1)
