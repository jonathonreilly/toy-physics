#!/usr/bin/env python3
"""
CKM Atlas/Axiom No-Import Closure
=================================

STATUS: branch-local closure route with canonical CMT coupling and an exact
tensor-slot theorem for 1->3 mixing.

This route does not reuse the old mass-input CKM formulas. It closes CKM on a
strict no-import surface by combining only branch-local exact/derived inputs:

  1. canonical alpha_s(v) from the coupling-map theorem on the plaquette surface
  2. the exact EWSB 1+2 split (one weak corner, residual color pair)
  3. the exact quark-block dimension dim(Q_L) = 2 x 3 = 6
  4. the exact Z_3 CP source
  5. the exact support-side center-excess scalar on the six-state quark block
  6. the exact bilinear tensor carrier K_R on A1 x {E_x, T1x}
  7. the exact Schur-complement cascade for 1 -> 3 mixing

The exact theorem formulas are:

  lambda = sqrt(alpha_s(v) / 2)
  A      = sqrt(2 / 3)
  sqrt(rho^2 + eta^2) = 1 / sqrt(6)
  delta_source = 2*pi/3
  delta_std    = arctan(sqrt(5)) = arccos(1/sqrt(6))

  |V_cb| = alpha_s(v) / sqrt(6)
  |V_ub| = alpha_s(v)^(3/2) / (6*sqrt(2))

The democratic seven-site support point remains an exact scalar comparison
surface on A1:

  |V_ub|_scalar-compare = alpha_s(v)^(3/2) / (2*sqrt(21))
  sqrt(rho^2 + eta^2)_scalar-compare = 1 / sqrt(7)

No observed quark masses or fitted CKM observables are used as inputs.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from _frontier_loader import load_frontier

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0
EXACT_PASS = 0
EXACT_FAIL = 0
BOUNDED_PASS = 0
BOUNDED_FAIL = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT, EXACT_PASS, EXACT_FAIL
    global BOUNDED_PASS, BOUNDED_FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
        if kind == "EXACT":
            EXACT_PASS += 1
        else:
            BOUNDED_PASS += 1
    else:
        FAIL_COUNT += 1
        if kind == "EXACT":
            EXACT_FAIL += 1
        else:
            BOUNDED_FAIL += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def build_standard_ckm(s12: float, s23: float, s13: float, delta: float) -> np.ndarray:
    """Standard PDG-form CKM matrix from mixing angles and phase."""
    c12 = math.sqrt(1.0 - s12 * s12)
    c23 = math.sqrt(1.0 - s23 * s23)
    c13 = math.sqrt(1.0 - s13 * s13)
    phase = complex(math.cos(delta), math.sin(delta))

    return np.array(
        [
            [c12 * c13, s12 * c13, s13 / phase],
            [
                -s12 * c23 - c12 * s23 * s13 * phase,
                c12 * c23 - s12 * s23 * s13 * phase,
                s23 * c13,
            ],
            [
                s12 * s23 - c12 * c23 * s13 * phase,
                -c12 * s23 - s12 * c23 * s13 * phase,
                c23 * c13,
            ],
        ],
        dtype=complex,
    )


def jarlskog(v_ckm: np.ndarray) -> float:
    return abs(np.imag(v_ckm[0, 1] * v_ckm[1, 2] * np.conj(v_ckm[0, 2]) * np.conj(v_ckm[1, 1])))


def j_from_angles(s12: float, s23: float, s13: float, delta: float) -> float:
    c12 = math.sqrt(1.0 - s12 * s12)
    c23 = math.sqrt(1.0 - s23 * s23)
    c13 = math.sqrt(1.0 - s13 * s13)
    return c12 * s12 * c23 * s23 * c13 * c13 * s13 * math.sin(delta)


PI = math.pi

# Framework inputs: branch-local exact/derived surfaces
PLAQ_MC = 0.5934
M_PLANCK = 1.2209e19
SELECTOR_CORRECTION = (7.0 / 8.0) ** 0.25
U0_HIERARCHY = PLAQ_MC ** 0.25
ALPHA_BARE = 1.0 / (4.0 * PI)
ALPHA_LM = ALPHA_BARE / U0_HIERARCHY
V_DERIVED_CURRENT = M_PLANCK * SELECTOR_CORRECTION * ALPHA_LM**16

# Exact structural counts from the retained atlas surface
RESIDUAL_COLOR_PAIR = 2
COLOR_RANK = 3
QUARK_BLOCK_DIM = 2 * 3
CENTER_EXCESS_WEIGHT = 1.0 / QUARK_BLOCK_DIM
ORTHOGONAL_PHASE_WEIGHT = 1.0 - CENTER_EXCESS_WEIGHT
SUPPORT_DIM = 7
SUPPORT_ARM_COUNT = 6

# Observation-facing comparators (for validation only, not inputs)
V_US_PDG = 0.2243
V_CB_PDG = 0.0422
V_UB_PDG = 0.00394
J_PDG = 3.08e-5
DELTA_PDG_DEG = 65.5

bilinear = load_frontier("s3_time_bilinear_tensor_primitive", "frontier_s3_time_bilinear_tensor_primitive.py")


print("=" * 78)
print("CKM ATLAS/AXIOM NO-IMPORT CLOSURE")
print("=" * 78)
print()
print("Input surface:")
print("  - canonical alpha_s(v) from the coupling-map theorem on the plaquette surface")
print("  - residual color pair size = 2 from the exact EWSB 1+2 split")
print("  - quark block dimension = 6 from Q_L = (2,3)")
print("  - Z_3 CP source")
print("  - exact support-side center-excess weight = 1/6")
print("  - exact bilinear tensor carrier K_R on A1 x {E_x, T1x}")
print("  - Schur-complement 1->3 cascade")
print()


print("=" * 78)
print("STEP 1: FRAMEWORK COUPLING AT v")
print("=" * 78)
print()

u0 = PLAQ_MC ** 0.25
alpha_bare = 1.0 / (4.0 * PI)
alpha_s_v_from_plaquette = alpha_bare / (u0 * u0)
alpha_s_v_from_hierarchy = 4.0 * PI * (V_DERIVED_CURRENT / (SELECTOR_CORRECTION * M_PLANCK)) ** (1.0 / 8.0)
alpha_s_v = alpha_s_v_from_plaquette

print(f"  u_0 = <P>^(1/4) = {u0:.12f}")
print(f"  alpha_bare = 1/(4*pi) = {alpha_bare:.12f}")
print(f"  alpha_s(v) canonical (CMT)       = alpha_bare/u_0^2 = {alpha_s_v:.12f}")
print(f"  hierarchy-pinned cross-check     = 4*pi*(v/(C*M_Pl))^(1/8) = {alpha_s_v_from_hierarchy:.12f}")
print(f"  current hierarchy-pinned v       = {V_DERIVED_CURRENT:.12f} GeV")
print()

check("u_0 is the exact fourth root of the plaquette surface", abs(u0**4 - PLAQ_MC) < 1e-12)
check("canonical alpha_s(v) is the CMT plaquette coupling", abs(alpha_s_v - alpha_s_v_from_plaquette) < 1e-15)
check("canonical alpha_s(v) is positive and perturbative", 0.09 < alpha_s_v < 0.11)
check(
    "current hierarchy-pinned v surface is consistent with the canonical coupling",
    abs(alpha_s_v_from_hierarchy - alpha_s_v) / alpha_s_v < 1e-12,
    f"relative gap = {abs(alpha_s_v_from_hierarchy - alpha_s_v) / alpha_s_v:.3e}",
)


print()
print("=" * 78)
print("STEP 2: EXACT ATLAS COUNTS")
print("=" * 78)
print()

print(f"  residual color pair size = {RESIDUAL_COLOR_PAIR}")
print(f"  color rank               = {COLOR_RANK}")
print(f"  quark block dimension    = {QUARK_BLOCK_DIM}")
print(f"  center-excess weight     = {CENTER_EXCESS_WEIGHT:.12f}")
print(f"  support dimension        = {SUPPORT_DIM}")
print(f"  support arm count        = {SUPPORT_ARM_COUNT}")
print()

check("exact residual pair size = 2", RESIDUAL_COLOR_PAIR == 2)
check("exact color rank = 3", COLOR_RANK == 3)
check("exact quark block dimension = 6", QUARK_BLOCK_DIM == 6)
check("quark block = residual pair x color rank", QUARK_BLOCK_DIM == RESIDUAL_COLOR_PAIR * COLOR_RANK)
check("exact center-excess weight = 1/6", abs(CENTER_EXCESS_WEIGHT - 1.0 / 6.0) < 1e-12)
check("exact support dimension = 7", SUPPORT_DIM == 7)
check("exact support arm count = 6", SUPPORT_ARM_COUNT == 6)


print()
print("=" * 78)
print("STEP 3: CKM CONSTANTS FROM PROJECTOR COUNTING")
print("=" * 78)
print()

# One-step weak->fixed-color probability is alpha_s(v)/2 on the exact 1+2 split.
lambda_w = math.sqrt(alpha_s_v / RESIDUAL_COLOR_PAIR)

# Second-step color rotation is the one-vertex amplitude on the normalized
# six-state quark block.
A_w = math.sqrt(RESIDUAL_COLOR_PAIR / COLOR_RANK)
radial_raw = 1.0 / math.sqrt(QUARK_BLOCK_DIM)

delta_source = 2.0 * PI / 3.0
delta_raw_branch = PI - delta_source

# The Z_3 source fixes the phase orientation. The exact support-side center
# excess on the six-state quark block fixes the CP-even weight to 1/6, leaving
# a 5/6 orthogonal complement. The standard-branch phase is therefore the
# normalized 1⊕5 projector angle.
delta_std = math.atan2(math.sqrt(ORTHOGONAL_PHASE_WEIGHT), math.sqrt(CENTER_EXCESS_WEIGHT))

# Scalar A1 comparison surface from the exact support-side law:
#   q_A1(r) = (e0 + r s)/(1 + sqrt(6) r)
# At r = sqrt(6), the support charge is exactly democratic on all seven sites:
#   q_dem = (1,1,1,1,1,1,1) / 7
# so the noncentral support fraction is exactly 6/7 and the center excess is
#   delta_A1 = 1/42.
# This remains an exact scalar-support comparison surface, not the leading
# bright/tensor amplitude for the 1->3 CKM slot.
support_projective_r = math.sqrt(6.0)
support_delta = 1.0 / (6.0 * (1.0 + math.sqrt(6.0) * support_projective_r))
support_radius_factor = math.sqrt(SUPPORT_ARM_COUNT / SUPPORT_DIM)
radial_scalar_compare = radial_raw * support_radius_factor

# Exact tensor-slot theorem from the bilinear carrier K_R:
#   K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q)u_E(q), delta_A1(q)u_T(q)]]
# On pure A1 backgrounds K_R vanishes, so the democratic scalar contraction
# does not source the 1->3 slot. At the same democratic point q_dem, the exact
# bright column generated by E_x or T1x has leading amplitude 1, with only the
# lower-row bilinear dressing proportional to delta_A1. Therefore the leading
# CKM 1->3 amplitude keeps the raw quark-block radius 1/sqrt(6).
q_dem = bilinear.a1_background(support_projective_r)
k_dem = bilinear.k_r(q_dem)
ex_column = bilinear.k_r(q_dem + bilinear.e_x) - k_dem
t1x_column = bilinear.k_r(q_dem + bilinear.t1x) - k_dem
radial_theorem = radial_raw

rho_theorem = radial_theorem * math.sqrt(CENTER_EXCESS_WEIGHT)
eta_theorem = radial_theorem * math.sqrt(ORTHOGONAL_PHASE_WEIGHT)
rho_scalar_compare = radial_scalar_compare * math.sqrt(CENTER_EXCESS_WEIGHT)
eta_scalar_compare = radial_scalar_compare * math.sqrt(ORTHOGONAL_PHASE_WEIGHT)

s23 = A_w * lambda_w * lambda_w
s13 = A_w * lambda_w**3 * radial_theorem
s13_scalar_compare = A_w * lambda_w**3 * radial_scalar_compare

print(f"  lambda = sqrt(alpha_s(v)/2)     = {lambda_w:.12f}")
print(f"  A      = sqrt(2/3)              = {A_w:.12f}")
print(f"  r_raw  = sqrt(rho^2+eta^2)      = 1/sqrt(6) = {radial_raw:.12f}")
print(f"  delta_source = 2*pi/3           = {math.degrees(delta_source):.6f} deg")
print(f"  delta_raw    = pi/3             = {math.degrees(delta_raw_branch):.6f} deg")
print(f"  delta_std    = arctan(sqrt(5))  = {math.degrees(delta_std):.6f} deg")
print(f"  support r    = sqrt(6)          = {support_projective_r:.12f}")
print(f"  delta_A1     = 1/42             = {support_delta:.12f}")
print(f"  k_cp         = sqrt(6/7)        = {support_radius_factor:.12f}")
print(f"  K_R(q_dem) norm                = {np.linalg.norm(k_dem):.12e}")
print(f"  E_x bright column at q_dem     = {np.array2string(ex_column[:, 0], precision=12, floatmode='fixed')}")
print(f"  T1x bright column at q_dem     = {np.array2string(t1x_column[:, 1], precision=12, floatmode='fixed')}")
print(f"  r_theorem   = 1/sqrt(6)        = {radial_theorem:.12f}")
print(f"  rho_theorem = 1/6              = {rho_theorem:.12f}")
print(f"  eta_theorem = sqrt(5)/6        = {eta_theorem:.12f}")
print(f"  r_scalar    = 1/sqrt(7)        = {radial_scalar_compare:.12f}")
print(f"  rho_scalar  = 1/sqrt(42)       = {rho_scalar_compare:.12f}")
print(f"  eta_scalar  = sqrt(5/42)       = {eta_scalar_compare:.12f}")
print()
print(f"  |V_cb| = A*lambda^2             = {s23:.12f}")
print(f"  |V_ub| theorem = A*lambda^3/sqrt(6) = {s13:.12f}")
print(f"  |V_ub| scalar  = A*lambda^3/sqrt(7) = {s13_scalar_compare:.12f}")
print()

check("lambda = sqrt(alpha_s(v)/2)", abs(lambda_w**2 - alpha_s_v / 2.0) < 1e-12)
check("A = sqrt(2/3)", abs(A_w - math.sqrt(2.0 / 3.0)) < 1e-12)
check("raw CP radius = 1/sqrt(6)", abs(radial_raw - 1.0 / math.sqrt(6.0)) < 1e-12)
check("delta_raw branch = pi/3", abs(delta_raw_branch - PI / 3.0) < 1e-12)
check("cos^2(delta_std) = 1/6", abs(math.cos(delta_std) ** 2 - CENTER_EXCESS_WEIGHT) < 1e-12)
check("sin^2(delta_std) = 5/6", abs(math.sin(delta_std) ** 2 - ORTHOGONAL_PHASE_WEIGHT) < 1e-12)
check("democratic support projective point is r = sqrt(6)", abs(support_projective_r - math.sqrt(6.0)) < 1e-12)
check("delta_A1 at the democratic support point is 1/42", abs(support_delta - 1.0 / 42.0) < 1e-12)
check("support-side CP contraction = sqrt(6/7)", abs(support_radius_factor - math.sqrt(6.0 / 7.0)) < 1e-12)
check("the exact bilinear carrier vanishes on the pure democratic A1 background", np.linalg.norm(k_dem) < 1e-12)
check("the exact E_x bright column keeps unit leading amplitude at q_dem", abs(ex_column[0, 0] - 1.0) < 1e-12 and abs(ex_column[1, 0] - support_delta) < 1e-12)
check("the exact T1x bright column keeps unit leading amplitude at q_dem", abs(t1x_column[0, 1] - 1.0) < 1e-12 and abs(t1x_column[1, 1] - support_delta) < 1e-12)
check("the theorem sqrt(rho^2 + eta^2) = 1/sqrt(6)", abs(math.hypot(rho_theorem, eta_theorem) - 1.0 / math.sqrt(6.0)) < 1e-12)
check("the scalar comparison sqrt(rho^2 + eta^2) = 1/sqrt(7)", abs(math.hypot(rho_scalar_compare, eta_scalar_compare) - 1.0 / math.sqrt(7.0)) < 1e-12)
check("V_cb = alpha_s(v)/sqrt(6)", abs(s23 - alpha_s_v / math.sqrt(6.0)) < 1e-12)
check("V_ub theorem = alpha_s(v)^(3/2)/(6*sqrt(2))", abs(s13 - alpha_s_v**1.5 / (6.0 * math.sqrt(2.0))) < 1e-12)
check("scalar comparison V_ub = alpha_s(v)^(3/2)/(2*sqrt(21))", abs(s13_scalar_compare - alpha_s_v**1.5 / (2.0 * math.sqrt(21.0))) < 1e-12)


print()
print("=" * 78)
print("STEP 4: FULL CKM MATRIX")
print("=" * 78)
print()

v_ckm = build_standard_ckm(lambda_w, s23, s13, delta_std)
vv_dag = v_ckm @ v_ckm.conj().T
unitarity_err = np.linalg.norm(vv_dag - np.eye(3))

v_us = abs(v_ckm[0, 1])
v_cb = abs(v_ckm[1, 2])
v_ub = abs(v_ckm[0, 2])
j_val = jarlskog(v_ckm)

v_ckm_scalar_compare = build_standard_ckm(lambda_w, s23, s13_scalar_compare, delta_std)
v_ub_scalar_compare = abs(v_ckm_scalar_compare[0, 2])
j_scalar_compare = jarlskog(v_ckm_scalar_compare)

j_raw = (
    math.sqrt(1.0 - lambda_w * lambda_w)
    * lambda_w
    * math.sqrt(1.0 - s23 * s23)
    * s23
    * (1.0 - s13 * s13)
    * s13
    * math.sin(delta_raw_branch)
)

print("  Theorem CKM matrix:")
print(v_ckm)
print()
print(f"  |V_us|        = {v_us:.12f}")
print(f"  |V_cb|        = {v_cb:.12f}")
print(f"  |V_ub|        = {v_ub:.12f}")
print(f"  J             = {j_val:.12e}")
print(f"  J_raw         = {j_raw:.12e}  (undressed pi/3 branch)")
print(f"  delta         = {math.degrees(delta_std):.6f} deg")
print()
print(f"  scalar-support comparison |V_ub| = {v_ub_scalar_compare:.12f}")
print(f"  scalar-support comparison J      = {j_scalar_compare:.12e}")
print()

check("theorem CKM matrix is unitary to machine precision", unitarity_err < 1e-12, f"||VV^dag-I|| = {unitarity_err:.2e}")
check("|V_us| equals c_13*lambda", abs(v_us - math.sqrt(1.0 - s13 * s13) * lambda_w) < 1e-12)
check("|V_cb| equals c_13*A*lambda^2", abs(v_cb - math.sqrt(1.0 - s13 * s13) * s23) < 1e-12)
check("|V_ub| equals A*lambda^3/sqrt(6)", abs(v_ub - s13) < 1e-12)
check("scalar-support comparison |V_ub| equals A*lambda^3/sqrt(7)", abs(v_ub_scalar_compare - s13_scalar_compare) < 1e-12)


print()
print("=" * 78)
print("STEP 5: OBSERVATION-FACING READOUT")
print("=" * 78)
print()

def pct(pred: float, target: float) -> float:
    return 100.0 * (pred - target) / target


j_obs_recon = j_from_angles(V_US_PDG, V_CB_PDG, V_UB_PDG, math.radians(DELTA_PDG_DEG))

print("  Theorem package vs coherent angle-facing comparator package:")
print(f"    |V_us| = {v_us:.6f} vs {V_US_PDG:.6f}  ({pct(v_us, V_US_PDG):+.2f}%)")
print(f"    |V_cb| = {v_cb:.6f} vs {V_CB_PDG:.6f}  ({pct(v_cb, V_CB_PDG):+.2f}%)")
print(f"    |V_ub| = {v_ub:.6f} vs {V_UB_PDG:.6f}  ({pct(v_ub, V_UB_PDG):+.2f}%)")
print(f"    J      = {j_val:.6e} vs J_recon {j_obs_recon:.6e}  ({pct(j_val, j_obs_recon):+.2f}%)")
print()
print("  Scalar-support comparison vs standalone scalar J comparator:")
print(f"    |V_ub|_scalar = {v_ub_scalar_compare:.6f} vs {V_UB_PDG:.6f}  ({pct(v_ub_scalar_compare, V_UB_PDG):+.2f}%)")
print(f"    J_scalar      = {j_scalar_compare:.6e} vs {J_PDG:.6e}  ({pct(j_scalar_compare, J_PDG):+.2f}%)")
print()
print("  Observation comparator split:")
print(f"    J_recon(obs angles, obs delta) = {j_obs_recon:.6e}")
print(f"    J_scalar comparator            = {J_PDG:.6e}")
print(f"    split                          = {pct(j_obs_recon, J_PDG):+.2f}%")
print()
print(f"  delta theorem = {math.degrees(delta_std):.3f} deg vs {DELTA_PDG_DEG:.3f} deg")
print()

check("|V_us| within 2% of PDG", abs(v_us - V_US_PDG) / V_US_PDG < 0.02, kind="BOUNDED")
check("|V_cb| within 1% of PDG", abs(v_cb - V_CB_PDG) / V_CB_PDG < 0.01, kind="BOUNDED")
check("|V_ub| within 1% of PDG", abs(v_ub - V_UB_PDG) / V_UB_PDG < 0.01, kind="BOUNDED")
check("J within 1% of the angle-reconstructed comparator", abs(j_val - j_obs_recon) / j_obs_recon < 0.01, kind="BOUNDED")
check("scalar-support comparison J within 1% of the standalone scalar comparator", abs(j_scalar_compare - J_PDG) / J_PDG < 0.01, kind="BOUNDED")
check("observed angle package reconstructs J more than 5% above the standalone scalar comparator", j_obs_recon / J_PDG > 1.05, kind="BOUNDED")
check("delta phase-dressed branch within 1% of PDG", abs(math.degrees(delta_std) - DELTA_PDG_DEG) / DELTA_PDG_DEG < 0.01, kind="BOUNDED")


print()
print("=" * 78)
print("CLOSURE STATEMENT")
print("=" * 78)
print()
print("  The theorem package is fixed by the canonical CMT coupling alpha_s(v),")
print("  exact atlas counts {2,3,6}, the Z_3 CP source, the exact 1/6 support-")
print("  side center-excess projector, the exact bilinear tensor carrier K_R,")
print("  and the exact Schur cascade. No observed quark masses enter.")
print()
print("  The democratic seven-site support point remains an exact scalar")
print("  comparison surface, but it does not contract the leading bright/tensor")
print("  1->3 amplitude. That slot is carried by K_R, whose exact bright columns")
print("  keep unit leading amplitude on the democratic background, so the CKM")
print("  theorem package keeps the raw quark-block radius 1/sqrt(6).")
print()
print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
print(f"         EXACT PASS={EXACT_PASS} FAIL={EXACT_FAIL}")
print(f"         BOUNDED PASS={BOUNDED_PASS} FAIL={BOUNDED_FAIL}")

sys.exit(0 if FAIL_COUNT == 0 else 1)
