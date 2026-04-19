"""
Frontier runner - Koide Berry audit on the actual charged-lepton route.

Companion to `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`.

This runner tests only claims that are actually validated:

  (A) The scale-free Koide locus on the unit sphere is a fixed-latitude circle.
  (B) The ambient-S^2 monopole wedge arithmetic is support-only, not the
      actual physical route.
  (C) On the exact selected line, the normalized Koide amplitudes carry a
      canonical projective C_3 doublet ray with fixed-modulus Fourier
      coefficients, forced doubled projective phase, exact scalar-phase
      bridge, and a unique unphased reference point.
  (D) On that actual selected route, the tautological CP^1 Berry connection
      reproduces the physical phase offset.
  (E) Natural selected-slice eigenline Berry selector laws do not pick the
      physical selected point.
  (F) The retained circulant eigenvectors still carry zero Berry phase on
      their own delta-moduli.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
)
from frontier_higgs_dressed_propagator_v1 import H3
from frontier_koide_selected_line_cyclic_response_bridge import (
    hstar_witness_kappa,
    selected_line_kappa,
)


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SELECTOR = math.sqrt(6.0) / 3.0
KOIDE_RATIO = 2.0 / 3.0
SINGLET_FRACTION = 0.5
OMEGA = np.exp(2j * np.pi / 3.0)

U = (1.0 / math.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA**2],
        [1.0, OMEGA**2, OMEGA],
    ],
    dtype=complex,
)

U_VEC = np.array([1.0, 1.0, 1.0], dtype=float) / SQRT3
E1_VEC = np.array([2.0, -1.0, -1.0], dtype=float) / math.sqrt(6.0)
E2_VEC = np.array([0.0, 1.0, -1.0], dtype=float) / math.sqrt(2.0)


def c3_shift() -> np.ndarray:
    return np.array(
        [
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
        ],
        dtype=complex,
    )


def brannen_vector(delta: float) -> np.ndarray:
    return np.array(
        [1.0 + SQRT2 * math.cos(delta + 2.0 * math.pi * k / 3.0) for k in range(3)],
        dtype=float,
    )


def normalized_brannen(delta: float) -> np.ndarray:
    v = brannen_vector(delta)
    return v / np.linalg.norm(v)


def circulant_family(a: float, rho: float, delta: float) -> np.ndarray:
    c = c3_shift()
    b = rho * np.exp(1j * (2.0 * math.pi / 3.0 + delta))
    return a * np.eye(3, dtype=complex) + b * c + np.conjugate(b) * (c @ c)


def berry_connection(state_fn, x: float, step: float = 1e-7) -> complex:
    psi = state_fn(x)
    psi_f = state_fn(x + step)
    deriv = (psi_f - psi) / step
    return 1j * np.vdot(psi, deriv)


def selected_line_slots(m: float) -> tuple[float, float]:
    x = expm(H3(m, SELECTOR, SELECTOR))
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    return v, w


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def selected_line_small_amp(m: float) -> np.ndarray:
    v, w = selected_line_slots(m)
    u_small, _ = koide_root_pair(v, w)
    return np.array([u_small, v, w], dtype=float)


def normalized_selected_line_state(m: float) -> np.ndarray:
    amp = selected_line_small_amp(m)
    return amp / np.linalg.norm(amp)


def selected_line_fourier_coeffs(m: float) -> np.ndarray:
    return np.conjugate(U).T @ normalized_selected_line_state(m)


def theta_phase(m: float) -> float:
    theta = float(np.angle(selected_line_fourier_coeffs(m)[1]))
    if theta < 0.0:
        theta += 2.0 * math.pi
    return theta


def delta_offset(m: float) -> float:
    return theta_phase(m) - 2.0 * math.pi / 3.0


def projective_doublet_ratio(m: float) -> complex:
    coeffs = selected_line_fourier_coeffs(m)
    return coeffs[2] / coeffs[1]


def canonical_spinor(theta: float) -> np.ndarray:
    return np.array([1.0, np.exp(-2j * theta)], dtype=complex) / math.sqrt(2.0)


def selected_line_scalar_from_delta(delta: float) -> float:
    return -SQRT3 * math.cos(delta + math.pi / 6.0) / (
        math.sqrt(2.0) + math.sin(delta + math.pi / 6.0)
    )


def k2_block(m: float) -> np.ndarray:
    return kz_from_h(active_affine_h(m, SELECTOR, SELECTOR))[1:3, 1:3]


def selected_slice_eigenvector(m: float, branch: int = 0) -> np.ndarray:
    w, v = np.linalg.eigh(k2_block(m))
    idx = np.argsort(w)
    vec = v[:, idx[branch]]
    vec = vec * np.exp(-1j * np.angle(vec[0]))
    if vec[0].real < 0.0:
        vec = -vec
    return vec / np.linalg.norm(vec)


def open_path_geometric_phase(m0: float, m1: float, branch: int = 0, n: int = 700) -> float:
    ms = np.linspace(m0, m1, n)
    vecs = [selected_slice_eigenvector(m, branch) for m in ms]
    vals = []
    mids = []
    for a, b, va, vb in zip(ms[:-1], ms[1:], vecs[:-1], vecs[1:]):
        dm = b - a
        vals.append((1j * np.vdot(va, (vb - va) / dm)).real)
        mids.append((a + b) / 2.0)
    return float(np.angle(np.vdot(vecs[0], vecs[-1])) - np.trapezoid(vals, mids))


print("=" * 72)
print("Cycle 10B revised again -- actual-route Berry audit")
print("=" * 72)


# ---------------------------------------------------------------------------
# (A) Scale-free Koide geometry
# ---------------------------------------------------------------------------

print("\n(A) Actual scale-free Koide geometry")
print("-" * 72)

deltas = np.linspace(0.0, 2.0 * math.pi, 721, endpoint=True)
states = np.array([normalized_brannen(delta) for delta in deltas])

singlet_components = states @ U_VEC
doublet_vectors = states - np.outer(singlet_components, U_VEC)
doublet_norms = np.linalg.norm(doublet_vectors, axis=1)
koide_ratios = np.array([np.dot(state, state) / (np.sum(state) ** 2) for state in states])
positive_mask = np.array([np.all(brannen_vector(delta) > 0.0) for delta in deltas], dtype=bool)

check(
    "(A1) Normalized Brannen family stays on the Koide cone",
    np.max(np.abs(koide_ratios - KOIDE_RATIO)) < 1e-12,
    f"max |K(delta)-2/3| = {np.max(np.abs(koide_ratios - KOIDE_RATIO)):.2e}",
)
check(
    "(A2) The unit Koide locus has fixed singlet amplitude",
    np.max(np.abs(singlet_components - math.sqrt(SINGLET_FRACTION))) < 1e-12,
    f"singlet = {singlet_components[0]:.12f}",
)
check(
    "(A3) The unit Koide locus has fixed doublet radius",
    np.max(np.abs(doublet_norms - math.sqrt(1.0 - SINGLET_FRACTION))) < 1e-12,
    f"doublet radius = {doublet_norms[0]:.12f}",
)
check(
    "(A4) The positive charged-lepton sector is a proper sub-arc, not the full circle",
    0.0 < float(np.mean(positive_mask)) < 1.0,
    f"positive fraction of sampled deltas = {float(np.mean(positive_mask)):.4f}",
)


# ---------------------------------------------------------------------------
# (B) Ambient-S^2 support only
# ---------------------------------------------------------------------------

print("\n(B) Ambient-S^2 monopole support only")
print("-" * 72)

n_flux = 2.0
theta_k = math.acos(math.sqrt(SINGLET_FRACTION))
branch_wedge_holonomy = 2.0 * math.pi * n_flux / 3.0
branch_delta = (branch_wedge_holonomy / (2.0 * math.pi)) / 3.0
latitude_step_holonomy = (n_flux / 2.0) * (1.0 - math.cos(theta_k)) * (2.0 * math.pi / 3.0)
latitude_delta = latitude_step_holonomy / (2.0 * math.pi * 3.0)

check(
    "(B1) The auxiliary ambient-S^2 wedge arithmetic reproduces 2/9",
    abs(branch_delta - 2.0 / 9.0) < 1e-12,
    f"delta_aux = {branch_delta:.12f}",
)
check(
    "(B2) The same monopole connection restricted to the actual Koide latitude does not give 2/9",
    abs(latitude_delta - 2.0 / 9.0) > 1e-3,
    f"delta_lat = {latitude_delta:.12f}",
)


# ---------------------------------------------------------------------------
# (C) Actual selected-line Berry carrier
# ---------------------------------------------------------------------------

print("\n(C) Actual selected-line projective doublet ray")
print("-" * 72)

m_pos = float(brentq(lambda m: selected_line_small_amp(m)[0], -1.3, -1.2))
m_zero = float(brentq(lambda m: selected_line_small_amp(m)[0] - selected_line_small_amp(m)[1], -0.4, -0.2))
_beta_star, kappa_star = hstar_witness_kappa()
m_star = float(brentq(lambda m: selected_line_kappa(m) - kappa_star, -1.165, -1.160))

first_branch_grid = np.linspace(m_pos + 1.0e-4, m_zero - 1.0e-4, 25)
first_branch_dense = np.linspace(m_pos + 1.0e-4, m_zero - 1.0e-4, 200)
first_branch_amplitudes = np.array([selected_line_small_amp(m) for m in first_branch_grid])
first_branch_koide = np.array(
    [np.dot(amp, amp) / (np.sum(amp) ** 2) for amp in first_branch_amplitudes],
    dtype=float,
)
coeffs = np.array([selected_line_fourier_coeffs(m) for m in first_branch_grid])
theta_grid = np.array([theta_phase(m) for m in first_branch_grid], dtype=float)
projective_ratios = np.array([projective_doublet_ratio(m) for m in first_branch_grid], dtype=complex)
delta_dense = np.array([delta_offset(m) for m in first_branch_dense], dtype=float)
scalar_dense = np.array([selected_line_kappa(m) for m in first_branch_dense], dtype=float)
scalar_bridge_dense = np.array(
    [selected_line_scalar_from_delta(delta) for delta in delta_dense],
    dtype=float,
)

check(
    "(C1) The selected first branch stays exactly on the Koide cone",
    np.max(np.abs(first_branch_koide - KOIDE_RATIO)) < 1e-12,
    f"max |Q_sel-2/3| = {np.max(np.abs(first_branch_koide - KOIDE_RATIO)):.2e}",
)
check(
    "(C2) The selected-line Fourier coefficients have fixed moduli and conjugate phases",
    np.max(np.abs(np.abs(coeffs[:, 0]) - 1.0 / math.sqrt(2.0))) < 1e-12
    and np.max(np.abs(np.abs(coeffs[:, 1]) - 0.5)) < 1e-12
    and np.max(np.abs(coeffs[:, 2] - np.conjugate(coeffs[:, 1]))) < 1e-12,
    "coeffs = (1/sqrt(2), 1/2 e^{i theta}, 1/2 e^{-i theta})",
)
check(
    "(C3) The projective C_3 doublet coordinate has the forced doubled phase e^{-2 i theta}",
    np.max(np.abs(projective_ratios - np.exp(-2j * theta_grid))) < 1e-12,
    "ell(theta) = [1 : e^{-2 i theta}]",
)
check(
    "(C4) There is a unique unphased first-branch point with theta = 2 pi / 3",
    abs(delta_offset(m_zero)) < 1e-12 and abs(theta_phase(m_zero) - 2.0 * math.pi / 3.0) < 1e-12,
    f"m_0 = {m_zero:.12f}",
)
check(
    "(C5) The positivity threshold carries the exact offset pi / 12",
    abs(delta_offset(m_pos) - math.pi / 12.0) < 1e-12,
    f"m_pos = {m_pos:.12f}",
)
check(
    "(C6) The selected-line scalar and Berry offset satisfy one exact branch relation",
    np.max(np.abs(scalar_dense - scalar_bridge_dense)) < 1e-12,
    "kappa_sel(delta) = -sqrt(3) cos(delta+pi/6)/(sqrt(2)+sin(delta+pi/6))",
)
check(
    "(C7) On the first branch the selected-line scalar and Berry offset are one-to-one",
    bool(np.all(np.diff(delta_dense) < 0.0)) and bool(np.all(np.diff(scalar_dense) < 0.0)),
    f"delta in ({delta_dense[-1]:.6f}, {delta_dense[0]:.6f})",
)
conn_theta = berry_connection(canonical_spinor, theta_phase(m_star)).real
check(
    "(C8) The tautological equator connection is A = dtheta",
    abs(conn_theta - 1.0) < 1e-6,
    f"A(theta_*) = {conn_theta:.12f}",
)
check(
    "(C9) The current selected-line witness carries the physical 2/9 phase",
    abs(delta_offset(m_star) - 2.0 / 9.0) < 5e-5,
    f"m_* = {m_star:.12f}, delta = {delta_offset(m_star):.12f}",
)
check(
    "(C10) Berry holonomy from the unphased point equals the phase offset",
    abs((theta_phase(m_star) - theta_phase(m_zero)) - delta_offset(m_star)) < 1e-12
    and abs((theta_phase(m_star) - theta_phase(m_zero)) - 2.0 / 9.0) < 5e-5,
    f"hol = {theta_phase(m_star) - theta_phase(m_zero):.12f}",
)


# ---------------------------------------------------------------------------
# (D) Natural selected-slice Berry selectors fail
# ---------------------------------------------------------------------------

print("\n(D) Natural selected-slice Berry selector no-go")
print("-" * 72)

geom_lower_zero = open_path_geometric_phase(m_zero, m_star, branch=0)
geom_lower_pos = open_path_geometric_phase(m_pos, m_star, branch=0)
geom_upper_zero = open_path_geometric_phase(m_zero, m_star, branch=1)
selector_root = float(
    brentq(
        lambda m: open_path_geometric_phase(m_zero, m, branch=0, n=700) - delta_offset(m),
        -0.90,
        -0.85,
    )
)

check(
    "(D1) Lower-eigenline geometric phase from the unphased point is not 2/9 at the witness",
    abs(geom_lower_zero - 2.0 / 9.0) > 1e-2,
    f"gamma = {geom_lower_zero:.12f}",
)
check(
    "(D2) Lower-eigenline geometric phase from threshold is not 2/9 at the witness",
    abs(geom_lower_pos - 2.0 / 9.0) > 1e-2,
    f"gamma = {geom_lower_pos:.12f}",
)
check(
    "(D3) Upper-eigenline geometric phase from the unphased point is not 2/9 at the witness",
    abs(geom_upper_zero - 2.0 / 9.0) > 1e-2,
    f"gamma = {geom_upper_zero:.12f}",
)
check(
    "(D4) Solving gamma_lower(m_0 -> m) = delta(m) selects a different point than the witness",
    abs(selector_root - m_star) > 0.1,
    f"m_sel = {selector_root:.12f}, m_* = {m_star:.12f}",
)


# ---------------------------------------------------------------------------
# (E) Retained circulant moduli still have zero Berry phase
# ---------------------------------------------------------------------------

print("\n(E) Retained circulant moduli carry zero Berry phase")
print("-" * 72)

a_test = 1.2
rho_test = 0.4
max_offdiag = 0.0
for delta in np.linspace(0.0, 2.0 * math.pi, 101, endpoint=False):
    diag_form = np.conjugate(U).T @ circulant_family(a_test, rho_test, delta) @ U
    offdiag = diag_form - np.diag(np.diag(diag_form))
    max_offdiag = max(max_offdiag, float(np.max(np.abs(offdiag))))

check(
    "(E1) A fixed Fourier basis diagonalizes the whole circulant delta-family",
    max_offdiag < 1e-12,
    f"max offdiag = {max_offdiag:.2e}",
)
fixed_basis_connections = [
    berry_connection(lambda delta, vec=vec: vec, 0.4) for vec in (U[:, 0], U[:, 1], U[:, 2])
]
check(
    "(E2) Berry connection of the circulant eigenvectors is zero",
    max(abs(val) for val in fixed_basis_connections) < 1e-9,
    f"max |A_k| = {max(abs(val) for val in fixed_basis_connections):.2e}",
)
state_connections = [
    berry_connection(
        lambda delta: np.array(
            [
                1.0 / math.sqrt(2.0),
                0.5 * np.exp(1j * delta),
                0.5 * np.exp(-1j * delta),
            ],
            dtype=complex,
        ),
        delta,
    )
    for delta in np.linspace(0.0, 2.0 * math.pi, 13)
]
check(
    "(E3) The symmetric-gauge Koide state has zero connection on delta-moduli",
    max(abs(val) for val in state_connections) < 5e-7,
    f"max |A_state| = {max(abs(val) for val in state_connections):.2e}",
)


print()
print("=" * 72)
print(f"PASS={PASS} FAIL={FAIL}")
print("=" * 72)
sys.exit(0 if FAIL == 0 else 1)
