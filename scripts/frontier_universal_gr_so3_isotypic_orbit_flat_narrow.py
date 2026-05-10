#!/usr/bin/env python3
"""Verify the narrow SO(3) isotypic orbit-flat theorem on Sym^2(R^4).

Claim scope: under spatial-block SO(3) action R = 1 ⊕ R_3 on
Sym^2(R^4) with isotropic spatial diagonal weight d = (d_0, d_s, d_s, d_s):

  (T1) Pi_A1(R^T h R) = Pi_A1(h) pointwise, where Pi_A1 selects lapse
       and spatial trace (rank-2 SO(3)-trivial subspace).
  (T2) ||Pi_perp(R^T h R)||^2_d = ||Pi_perp(h)||^2_d (orbit-flat
       complement energy).
  (T3) Pi_perp(R^T h R) ≠ Pi_perp(h) generically (coordinates move).

  Corollary: no quadratic energy E_{α,β}[h] = α ||Pi_A1||^2 + β
  ||Pi_perp||^2 selects a unique complement-frame section.

Load-bearing step is class (A) algebraic identity on block matrix
relations and orthogonal-invariance of Frobenius norm.
"""

from pathlib import Path
import sys
import json

try:
    import sympy as sp
    from sympy import Matrix, eye, zeros, simplify, sqrt, expand, trigsimp, pi, cos, sin, Rational, Symbol
except ImportError:
    print("FAIL: sympy required for exact symbolic identities")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("FAIL: numpy required for numerical sampling")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "UNIVERSAL_GR_SO3_ISOTYPIC_ORBIT_FLAT_NARROW_THEOREM_NOTE_2026-05-10.md"
LEDGER_PATH = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

PASS = 0
FAIL = 0


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
section("Part 1: note structure and scope discipline")
# ============================================================================
note_text = NOTE_PATH.read_text()
required = [
    "SO(3) Isotypic Orbit-Flat Narrow Theorem on `Sym^2(R^4)`",
    "Claim type:** positive_theorem",
    "R = 1 ⊕ R_3",
    "Pi_A1(h')",
    "||Pi_perp(h')||^2_d",
    "MINIMAL_AXIOMS_2026-05-03",  # plain-text pointer; no markdown link to keep dep graph clean
    "class (A)",
    "isotropic spatial weight",
    "zero load-bearing dependencies",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)

forbidden = [
    "no-go for the universal GR route as a whole",
    "the quadratic functional E is the physical Einstein-Hilbert action",
    "closes the full universal-GR route",
]
for f in forbidden:
    check(f"narrow scope avoids forbidden claim: {f!r}",
          f not in note_text)


# ============================================================================
section("Part 2: symbolic (T1) — Pi_A1 is pointwise SO(3)-invariant")
# ============================================================================
h_syms = sp.symbols('h00 h01 h02 h03 h11 h22 h33 h12 h13 h23')
h00, h01, h02, h03, h11, h22, h33, h12, h13, h23 = h_syms
h_sym = Matrix([
    [h00, h01, h02, h03],
    [h01, h11, h12, h13],
    [h02, h12, h22, h23],
    [h03, h13, h23, h33],
])

phi, theta_, psi = sp.symbols('phi theta psi', real=True)


def Rx(a):
    return Matrix([[1, 0, 0],
                   [0, sp.cos(a), -sp.sin(a)],
                   [0, sp.sin(a), sp.cos(a)]])


def Ry(a):
    return Matrix([[sp.cos(a), 0, sp.sin(a)],
                   [0, 1, 0],
                   [-sp.sin(a), 0, sp.cos(a)]])


def Rz(a):
    return Matrix([[sp.cos(a), -sp.sin(a), 0],
                   [sp.sin(a), sp.cos(a), 0],
                   [0, 0, 1]])


R3 = Rz(phi) * Ry(theta_) * Rx(psi)
R = Matrix.zeros(4, 4)
R[0, 0] = 1
R[1:, 1:] = R3

# Confirm R3 ∈ SO(3)
ortho_residual = simplify(R3.T * R3 - eye(3))
check("R3 is orthogonal (R3^T R3 = I) symbolically",
      ortho_residual == zeros(3, 3),
      detail="Z-Y-X Euler-angle parameterization")

# Confirm det(R3) = 1 (special orthogonal)
det_R3 = simplify(R3.det())
check("det(R3) = 1 symbolically",
      det_R3 == 1,
      detail="orientation preserving")

# Pi_A1 projector
def pi_A1_sym(M: Matrix) -> Matrix:
    s = M[1, 1] + M[2, 2] + M[3, 3]
    out = Matrix.zeros(4, 4)
    out[0, 0] = M[0, 0]
    out[1, 1] = s / 3
    out[2, 2] = s / 3
    out[3, 3] = s / 3
    return out


h_rot_sym = R.T * h_sym * R
h_rot_sym = h_rot_sym.applyfunc(trigsimp)

A1_orig = pi_A1_sym(h_sym)
A1_rot = pi_A1_sym(h_rot_sym)
A1_diff = (A1_rot - A1_orig).applyfunc(lambda x: simplify(expand(x)))
check("(T1) Pi_A1(R^T h R) - Pi_A1(h) ≡ 0 symbolically",
      A1_diff == zeros(4, 4),
      detail="rank-2 SO(3)-trivial block is pointwise invariant")

# Spatial trace invariance (load-bearing identity)
tr_orig = h_sym[1, 1] + h_sym[2, 2] + h_sym[3, 3]
tr_rot = trigsimp(h_rot_sym[1, 1] + h_rot_sym[2, 2] + h_rot_sym[3, 3])
check("tr(h_ij)' = tr(h_ij) symbolically (spatial trace invariant)",
      simplify(expand(tr_orig - tr_rot)) == 0)

# Lapse invariance
check("h'_{00} = h_{00} symbolically (lapse invariant)",
      simplify(expand(h_rot_sym[0, 0] - h_sym[0, 0])) == 0)


# ============================================================================
section("Part 3: symbolic (T2) — complement energy is orbit-flat")
# ============================================================================
d0, d_s = sp.symbols('d_0 d_s', positive=True)


def energy_isotropic(M: Matrix) -> sp.Expr:
    weights = [1 / d0, 1 / d_s, 1 / d_s, 1 / d_s]
    e = 0
    for i in range(4):
        for j in range(4):
            e += M[i, j] * M[i, j] * weights[i] * weights[j]
    return e


# Total energy invariant
E_total_orig = energy_isotropic(h_sym)
E_total_rot = energy_isotropic(h_rot_sym)
delta_total = simplify(expand(E_total_orig - E_total_rot))
check("||h'||^2_d = ||h||^2_d symbolically (isotropic weight, total)",
      delta_total == 0,
      detail="spatial SO(3) preserves diagonal weight diag(1/d_0, 1/d_s, 1/d_s, 1/d_s)")

# SO(3)-trivial block energy is trivially invariant since Pi_A1 is pointwise fixed.
E_A1_orig = energy_isotropic(pi_A1_sym(h_sym))
E_A1_rot = energy_isotropic(pi_A1_sym(h_rot_sym))
delta_A1 = simplify(expand(E_A1_orig - E_A1_rot))
check("||Pi_A1(h')||^2_d = ||Pi_A1(h)||^2_d symbolically",
      delta_A1 == 0)

# Complement energy invariance
def pi_perp_sym(M: Matrix) -> Matrix:
    return M - pi_A1_sym(M)


E_perp_orig = energy_isotropic(pi_perp_sym(h_sym))
E_perp_rot = energy_isotropic(pi_perp_sym(h_rot_sym))
delta_perp = simplify(expand(E_perp_orig - E_perp_rot))
check("(T2) ||Pi_perp(h')||^2_d = ||Pi_perp(h)||^2_d symbolically",
      delta_perp == 0,
      detail="orbit-flat under isotropic spatial weight")


# ============================================================================
section("Part 4: symbolic anisotropic control — premise is load-bearing")
# ============================================================================
# With anisotropic spatial weight, complement energy should NOT be invariant
# in general. Construct a concrete witness.
d1, d2, d3 = sp.symbols('d_1 d_2 d_3', positive=True)


def energy_anisotropic(M: Matrix) -> sp.Expr:
    weights = [1 / d0, 1 / d1, 1 / d2, 1 / d3]
    e = 0
    for i in range(4):
        for j in range(4):
            e += M[i, j] * M[i, j] * weights[i] * weights[j]
    return e


# Concrete witness: h_13 = h_31 = 1 only; rotation R_y(π/4).
# This rotation mixes the 1- and 3-axes; under anisotropic d with d_1 ≠ d_3
# the complement energy must not be invariant.
h_concrete = Matrix([
    [0, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [0, 1, 0, 0],
])
check("anisotropic-control: concrete h has only h_13 = h_31 = 1",
      h_concrete[1, 3] == 1 and h_concrete[3, 1] == 1
      and sum(int(h_concrete[i, j] != 0) for i in range(4) for j in range(4)) == 2)

# R_y(π/4) acts as: e_1 -> cos·e_1 + sin·e_3, e_3 -> -sin·e_1 + cos·e_3, e_2 fixed
R_y_45 = Matrix([
    [1, 0, 0, 0],
    [0, sp.cos(pi/4), 0, sp.sin(pi/4)],
    [0, 0, 1, 0],
    [0, -sp.sin(pi/4), 0, sp.cos(pi/4)],
])
h_concrete_rot = R_y_45.T * h_concrete * R_y_45
h_concrete_rot = simplify(h_concrete_rot)

E_perp_aniso_orig = simplify(energy_anisotropic(pi_perp_sym(h_concrete)))
E_perp_aniso_rot = simplify(energy_anisotropic(pi_perp_sym(h_concrete_rot)))
delta_perp_aniso = simplify(E_perp_aniso_orig - E_perp_aniso_rot)
# Check non-zero in general (with d_1 ≠ d_3)
delta_at_aniso = simplify(delta_perp_aniso.subs({d0: 1, d1: 2, d2: 3, d3: 5}))
delta_at_iso = simplify(delta_perp_aniso.subs({d0: 1, d1: 2, d2: 2, d3: 2}))
check("anisotropic control: complement energy NOT invariant when d_1 ≠ d_3",
      delta_at_aniso != 0,
      detail=f"delta(d=(1,2,3,5)) = {sp.nsimplify(delta_at_aniso).evalf(10)}")
check("anisotropic control: complement energy IS invariant when d_1 = d_2 = d_3",
      delta_at_iso == 0,
      detail="confirms isotropy is the load-bearing premise")


# ============================================================================
section("Part 5: shift sector covariance and spatial-traceless mixing")
# ============================================================================
# Shift covector h_0i transforms as a 3-vector under R_3.
# Concrete: h_01 = h_10 = 1, all else 0; R_3 = R_z(π/2).
# R_z(90°): e_1 -> e_2, e_2 -> -e_1, e_3 fixed. So h_01 should map to h'_02.
h_shift = Matrix([
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])
# Z-axis rotation by 90° using exact integers: cos=0, sin=1
R_z_90 = Matrix([
    [1, 0, 0, 0],
    [0, 0, -1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
])
# Verify R_z_90 ∈ SO(3)
check("R_z(90°) is in SO(3) (orthogonal, det=+1)",
      simplify(R_z_90.T * R_z_90 - eye(4)) == zeros(4, 4) and R_z_90.det() == 1)

h_shift_rot = R_z_90.T * h_shift * R_z_90
h_shift_rot = simplify(h_shift_rot)
# Under h' = R^T h R: h'_{0,j} = sum_k R_{k,j} h_{0,k}.
# With R_z(90°) and h_{0,1}=1 (else zero): h'_{0,2} = R_{1,2}·h_{0,1} = (-1)·1 = -1, h'_{0,1} = R_{1,1}·1 = 0.
# So h'_{0,2} ∈ {±1} and h'_{0,1} = 0 — shift index has rotated from 1 to 2 (vector covariance).
check("concrete witness: h_01=1 + R_z(90°) gives h'_01=0 and |h'_02|=1 (vector covariance)",
      h_shift_rot[0, 1] == 0 and abs(h_shift_rot[0, 2]) == 1,
      detail=f"h'_01={h_shift_rot[0,1]}, h'_02={h_shift_rot[0,2]}, h'_03={h_shift_rot[0,3]}")

# Energy preserved exactly: Pi_A1(h_shift) = 0 since lapse = 0 and spatial trace = 0.
# So Pi_perp = h_shift. Complement energy = 2 * 1 / (d_0 * d_s) (from h_01 and h_10).
E_shift_orig = simplify(energy_isotropic(pi_perp_sym(h_shift)))
E_shift_rot = simplify(energy_isotropic(pi_perp_sym(h_shift_rot)))
expected_E = 2 / (d0 * d_s)
check("concrete witness: complement energy preserved at shift example",
      simplify(E_shift_orig - E_shift_rot) == 0,
      detail=f"E(orig)={E_shift_orig}, E(rot)={E_shift_rot}, expected={expected_E}")
check("concrete witness: shift example has expected energy 2/(d_0 d_s)",
      simplify(E_shift_orig - expected_E) == 0)


# ============================================================================
section("Part 6: numerical (T1, T2, T3) on random samples")
# ============================================================================
rng = np.random.default_rng(20260510)
n_samples = 200
d_vals = np.array([2.0, 3.5, 3.5, 3.5])  # isotropic spatial


def random_so3(rng):
    """Random R3 in SO(3) via QR of Gaussian, then enforce det = +1."""
    A = rng.normal(size=(3, 3))
    Q, _ = np.linalg.qr(A)
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q


def pi_A1_np(M):
    out = np.zeros_like(M)
    s = M[1, 1] + M[2, 2] + M[3, 3]
    out[0, 0] = M[0, 0]
    out[1, 1] = s / 3
    out[2, 2] = s / 3
    out[3, 3] = s / 3
    return out


def pi_perp_np(M):
    return M - pi_A1_np(M)


def energy_np(M, d):
    inv_d = 1.0 / d
    e = 0.0
    for i in range(4):
        for j in range(4):
            e += M[i, j] * M[i, j] * inv_d[i] * inv_d[j]
    return e


max_A1_delta = 0.0
max_perp_energy_delta = 0.0
max_perp_coord_delta = 0.0
max_total_energy_delta = 0.0
moved_count = 0

for _ in range(n_samples):
    # Random symmetric h
    h_np = rng.normal(size=(4, 4))
    h_np = 0.5 * (h_np + h_np.T)
    # Random R3
    R3_np = random_so3(rng)
    R_np = np.eye(4)
    R_np[1:, 1:] = R3_np
    # Rotate
    h_rot_np = R_np.T @ h_np @ R_np

    A1_o = pi_A1_np(h_np)
    A1_r = pi_A1_np(h_rot_np)
    perp_o = pi_perp_np(h_np)
    perp_r = pi_perp_np(h_rot_np)

    max_A1_delta = max(max_A1_delta, float(np.max(np.abs(A1_r - A1_o))))
    max_perp_coord_delta = max(max_perp_coord_delta, float(np.max(np.abs(perp_r - perp_o))))

    E_t_o = energy_np(h_np, d_vals)
    E_t_r = energy_np(h_rot_np, d_vals)
    E_p_o = energy_np(perp_o, d_vals)
    E_p_r = energy_np(perp_r, d_vals)
    max_total_energy_delta = max(max_total_energy_delta, abs(E_t_r - E_t_o))
    max_perp_energy_delta = max(max_perp_energy_delta, abs(E_p_r - E_p_o))

    if float(np.max(np.abs(perp_r - perp_o))) > 1e-3:
        moved_count += 1


check(f"(T1) numerical: max |Pi_A1(h') - Pi_A1(h)| < 1e-12 over {n_samples} samples",
      max_A1_delta < 1e-12,
      detail=f"observed max_A1_delta = {max_A1_delta:.3e}")

check(f"(T2) numerical: max |E_perp(h') - E_perp(h)| < 1e-12 over {n_samples} samples",
      max_perp_energy_delta < 1e-12,
      detail=f"observed max_perp_energy_delta = {max_perp_energy_delta:.3e}")

check(f"total energy invariant: max |E(h') - E(h)| < 1e-12 over {n_samples} samples",
      max_total_energy_delta < 1e-12,
      detail=f"observed max_total_energy_delta = {max_total_energy_delta:.3e}")

check(f"(T3) numerical: complement coordinates move on >50% of samples",
      moved_count >= n_samples // 2,
      detail=f"observed moved_count = {moved_count}/{n_samples}, max_perp_coord_delta = {max_perp_coord_delta:.3e}")


# ============================================================================
section("Part 7: corollary on quadratic energy class")
# ============================================================================
# E_{α,β}[h] = α ||Pi_A1||^2 + β ||Pi_perp||^2 must be SO(3)-invariant for
# all (α, β).
n_alpha = 200
max_E_alpha_delta = 0.0
for _ in range(n_alpha):
    h_np = rng.normal(size=(4, 4))
    h_np = 0.5 * (h_np + h_np.T)
    R3_np = random_so3(rng)
    R_np = np.eye(4)
    R_np[1:, 1:] = R3_np
    h_rot_np = R_np.T @ h_np @ R_np
    alpha = rng.normal()
    beta = rng.normal()
    E_o = alpha * energy_np(pi_A1_np(h_np), d_vals) + beta * energy_np(pi_perp_np(h_np), d_vals)
    E_r = alpha * energy_np(pi_A1_np(h_rot_np), d_vals) + beta * energy_np(pi_perp_np(h_rot_np), d_vals)
    max_E_alpha_delta = max(max_E_alpha_delta, abs(E_r - E_o))

check(f"corollary: E_{{α,β}}[h'] = E_{{α,β}}[h] for {n_alpha} random (α, β, h, R)",
      max_E_alpha_delta < 1e-12,
      detail=f"max |E_α,β delta| = {max_E_alpha_delta:.3e}")


# ============================================================================
section("Part 8: context references exist")
# ============================================================================
ledger = json.loads(LEDGER_PATH.read_text())
rows = ledger['rows']

# MINIMAL_AXIOMS is meta/context (no upstream); not in ledger as a
# positive theorem. Check it exists as the framework baseline memo.
axioms_path = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"
check("MINIMAL_AXIOMS_2026-05-03.md exists",
      axioms_path.exists(),
      detail="framework baseline memo for physical Cl(3) local algebra and Z^3 spatial substrate")

axioms_text = axioms_path.read_text() if axioms_path.exists() else ""
check("baseline memo names the canonical Cl(3) and Z^3 framework",
      "Cl(3)" in axioms_text and "Z^3" in axioms_text and "framework axioms" in axioms_text)

# Confirm parent universal-GR notes exist
parent_paths = [
    ROOT / "docs" / "UNIVERSAL_GR_CONSTRAINT_ACTION_STATIONARITY_NOTE.md",
    ROOT / "docs" / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md",
]
for p in parent_paths:
    check(f"cross-ref note exists: {p.name}", p.exists())


# ============================================================================
print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
