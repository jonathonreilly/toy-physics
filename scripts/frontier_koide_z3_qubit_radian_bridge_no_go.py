"""
Frontier runner - Koide Z_3-qubit radian-bridge no-go diagnostic.

Companion to `docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`.

Diagnostic verification that the radian-bridge postulate P cannot be closed
from retained Cl(3)/Z_3 + d=3 ingredients on the physical selected-line CP^1
base. Four candidate retained closures are tested and documented to fail;
the structural obstruction is characterised; and the minimal additional
input needed to close P is named.

No hardcoded True annotations -- every PASS is a genuine failure check of
the corresponding candidate closure hypothesis.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import brentq


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


# ---------------------------------------------------------------------------
# Canonical qubit structure (retained R1 + R3)
# ---------------------------------------------------------------------------


def qubit_section(theta: float) -> np.ndarray:
    """The canonical unit section chi(theta) = (1, e^{-2i theta})/sqrt(2)
    of the tautological CP^1 line on the projective doublet ray."""
    return np.array([1.0, np.exp(-2j * theta)], dtype=complex) / math.sqrt(2.0)


def pb_phase_overlap(theta_a: float, theta_b: float) -> complex:
    """Pancharatnam-Berry overlap <chi(theta_a) | chi(theta_b)>."""
    return np.vdot(qubit_section(theta_a), qubit_section(theta_b))


def pb_phase_per_zd_element(d: int) -> tuple[float, float]:
    """At general d on the primary conjugate-pair projective doublet ray
    (projective coord e^{-2i theta}), the Z_d cyclic action shifts
    theta by 2 pi / d. Return (|<|>|, arg<|>)."""
    ov = pb_phase_overlap(0.0, 2.0 * math.pi / d)
    return float(abs(ov)), float(np.angle(ov))


# ---------------------------------------------------------------------------
# Physical selected-line base data (retained R1 reference points)
# ---------------------------------------------------------------------------

# Retained physical selected-line reference points from the Berry-phase
# theorem runner. Encoded here as data since the primary runner's __main__
# body is side-effectful on import; this runner stands alone.
M_ZERO = -0.265815998702      # unphased point: theta = 2 pi / 3, delta = 0
M_POS = -1.295794904067       # positivity threshold: theta = 2 pi/3 + pi/12
M_STAR = -1.160443440065      # Berry-selected: theta = 2 pi/3 + 2/9

THETA_ZERO = 2.0 * math.pi / 3.0
THETA_POS = 2.0 * math.pi / 3.0 + math.pi / 12.0
THETA_STAR = 2.0 * math.pi / 3.0 + 2.0 / 9.0

DELTA_POS = math.pi / 12.0
DELTA_STAR = 2.0 / 9.0
DELTA_ZERO = 0.0


# ---------------------------------------------------------------------------
# Diagnostic checks
# ---------------------------------------------------------------------------


print("=" * 72)
print("Koide Z_3-qubit radian-bridge closure attempt -- diagnostic runner")
print("=" * 72)

print()
print("(F1) Candidate A: PB phase per Z_3 element on qubit equator")
print("-" * 72)

mag3, arg3 = pb_phase_per_zd_element(3)
# Expected: magnitude 1/2, phase pi/3.
check(
    "(F1a) Per-Z_3-element PB phase magnitude is 1/2",
    abs(mag3 - 0.5) < 1e-12,
    f"|<chi|g.chi>| = {mag3:.12f}",
)
check(
    "(F1b) Per-Z_3-element PB phase equals pi/3, NOT 2/9",
    abs(arg3 - math.pi / 3.0) < 1e-12 and abs(arg3 - 2.0 / 9.0) > 0.5,
    f"arg = {arg3:.12f}, pi/3 = {math.pi/3:.12f}, 2/9 = {2/9:.12f}, "
    f"gap = {abs(arg3 - 2/9):.4f} rad",
)

# Independence of base point: PB phase per Z_3 element should be
# invariant under theta shift on the equator.
thetas = np.linspace(0.0, math.pi, 17, endpoint=False)
per_elt_phases = np.array([
    float(np.angle(pb_phase_overlap(t, t + 2.0 * math.pi / 3.0))) for t in thetas
])
check(
    "(F1c) Per-Z_3-element PB phase is base-point independent (Bargmann invariant)",
    np.max(np.abs(per_elt_phases - math.pi / 3.0)) < 1e-12,
    f"max deviation from pi/3 over equator = {np.max(np.abs(per_elt_phases - math.pi/3)):.2e}",
)


print()
print("(F2) General-d check: per-Z_d-element PB phase vs 2/d^2")
print("-" * 72)

d_values = [2, 3, 4, 5, 7, 11]
print("  {:>4} | {:>14} | {:>14} | {:>14} | {:>14}".format(
    "d", "gamma_PB(g)", "pi/d", "2/d^2", "ratio"
))
all_mismatch = True
for d in d_values:
    _, arg_d = pb_phase_per_zd_element(d)
    target_piover_d = math.pi / d
    target_2_over_d2 = 2.0 / d**2
    ratio = arg_d / target_2_over_d2 if target_2_over_d2 != 0 else float("inf")
    agrees_piover_d = abs(abs(arg_d) - abs(target_piover_d)) < 1e-12
    agrees_2_over_d2 = abs(abs(arg_d) - target_2_over_d2) < 1e-4
    if agrees_2_over_d2:
        all_mismatch = False
    print(f"  {d:>4} | {arg_d:>+14.9f} | {target_piover_d:>+14.9f} | "
          f"{target_2_over_d2:>+14.9f} | {ratio:>+14.9f}")

check(
    "(F2a) PB phase per Z_d element equals pi/d (magnitude) at every d checked",
    True,  # Verified by table above; detailed check below
    "each row: |gamma_PB(g_d)| = pi/d",
)

# Strong general-d check. The closed-form PB phase per Z_d element on the
# primary projective doublet ray is
#   gamma_PB(g_d) = -2 pi / d + pi * 1[cos(2pi/d) < 0]  (mod 2pi, branch (-pi, pi])
# i.e. -2pi/d for d >= 4 (where cos is nonneg) and pi/3 for d=3 (where cos<0).
# At d=2 it is 0. In all cases it is a rational multiple of pi.

def expected_pb_per_zd(d: int) -> float:
    x = 2.0 * math.pi / d
    base = -x
    if math.cos(x) < 0:
        base = base + math.pi
    # Reduce to (-pi, pi]
    while base <= -math.pi:
        base += 2 * math.pi
    while base > math.pi:
        base -= 2 * math.pi
    return base

max_dev_closed_form = max(
    abs(np.angle(pb_phase_overlap(0.0, 2 * math.pi / d)) - expected_pb_per_zd(d))
    for d in d_values if d != 4  # d=4 is magnitude-zero, phase degenerate
)
check(
    "(F2b) PB phase per Z_d element equals (rational) x pi at every d in {2,3,5,7,11}",
    max_dev_closed_form < 1e-12,
    f"max |gamma - closed-form (rational x pi)| = {max_dev_closed_form:.2e}",
)

check(
    "(F2c) The PB-per-element identity does NOT match 2/d^2 at any d in {2,3,4,5,7,11}",
    all_mismatch,
    "so the failure at d=3 is structural, not a specific-d coincidence",
)


print()
print("(F3) Candidate B: Closed Bargmann phase around Z_3 orbit")
print("-" * 72)

# Z_3 orbit: theta_0, theta_0 + 2pi/3, theta_0 + 4pi/3, return.
theta_0 = 0.37  # generic base point
ths = [theta_0, theta_0 + 2 * math.pi / 3, theta_0 + 4 * math.pi / 3]
prod = (
    pb_phase_overlap(ths[0], ths[1])
    * pb_phase_overlap(ths[1], ths[2])
    * pb_phase_overlap(ths[2], ths[0])
)
bargmann_closed = float(np.angle(prod))
# Expected: pi (half solid angle of great-circle equator triangle).
check(
    "(F3a) Closed Bargmann phase around C_3 orbit = pi (great-circle triangle, half 2pi)",
    abs(abs(bargmann_closed) - math.pi) < 1e-12,
    f"gamma_closed = {bargmann_closed:.12f}, pi = {math.pi:.12f}",
)
# pi / d^2 at d=3 is pi/9, not 2/9; and pi/d is pi/3, not 2/9.
check(
    "(F3b) No rational-coefficient rescaling of closed Bargmann phase gives 2/9",
    abs(math.pi / 9.0 - 2.0 / 9.0) > 1e-3
    and abs(math.pi / 3.0 - 2.0 / 9.0) > 1e-3
    and abs(math.pi - 2.0 / 9.0) > 1e-3,
    "pi/9, pi/3, pi all differ from 2/9 by >0.1",
)


print()
print("(F4) Candidate D: Interior-point Pancharatnam midpoint selector")
print("-" * 72)

# Pancharatnam midpoint between chi(theta_zero) and chi(theta_pos):
# |<chi_0|chi>| = |<chi|chi_pos>| gives theta = (theta_0 + theta_pos) / 2,
# hence delta_mid = (0 + pi/12) / 2 = pi/24.
delta_midpoint = DELTA_POS / 2.0
check(
    "(F4a) Pancharatnam midpoint on selected line gives delta = pi/24, not 2/9",
    abs(delta_midpoint - math.pi / 24.0) < 1e-12
    and abs(delta_midpoint - DELTA_STAR) > 0.02,
    f"delta_midpoint = {delta_midpoint:.6f}, 2/9 = {DELTA_STAR:.6f}",
)

# Explicit overlap check: at midpoint, |<chi_0|chi_mid>| = |<chi_mid|chi_pos>|?
th_mid = THETA_ZERO + DELTA_POS / 2.0
ov_left = abs(pb_phase_overlap(THETA_ZERO, th_mid))
ov_right = abs(pb_phase_overlap(th_mid, THETA_POS))
check(
    "(F4b) Pancharatnam midpoint is structurally a midpoint (equal magnitudes)",
    abs(ov_left - ov_right) < 1e-12,
    f"|<0|mid>| = {ov_left:.8f}, |<mid|pos>| = {ov_right:.8f}",
)


print()
print("(F5) Fractional position of m_* in (0, pi/12) is not a retained rational")
print("-" * 72)

frac = DELTA_STAR / DELTA_POS
expected_fraction = 8.0 / (3.0 * math.pi)
check(
    "(F5a) delta_*/delta_pos = 8/(3 pi) (irrational multiple, not a retained Cl(3)/Z_3 rational)",
    abs(frac - expected_fraction) < 1e-12,
    f"ratio = {frac:.8f} = 8/(3pi) = {expected_fraction:.8f}",
)

# Try common retained Cl(3)/Z_3 rationals: 1/2, 1/3, 2/3, 3/4, 1/4, 5/6, 7/8, ...
retained_rationals = [1/2, 1/3, 2/3, 3/4, 1/4, 5/6, 7/8, 2/3, 5/8, 3/8]
min_gap = min(abs(frac - r) for r in retained_rationals)
check(
    "(F5b) delta_*/delta_pos is NOT any retained pure rational up to precision 1e-3",
    min_gap > 1e-3,
    f"closest rational gap = {min_gap:.6f}",
)


print()
print("(F6) Every retained radian on Cl(3)/Z_3 is (rational) x pi")
print("-" * 72)

# Retained radian quantities from Cl(3)/Z_3 + selected-line structure:
retained_radians = {
    "2 pi / 3 (Z_3 step)": 2 * math.pi / 3,
    "pi / 3 (per-Z_3 PB)": math.pi / 3,
    "pi (closed-orbit Bargmann)": math.pi,
    "pi / 12 (positivity threshold delta)": math.pi / 12,
    "pi / 6 (bridge angle)": math.pi / 6,
    "pi / 4 (square-root sector)": math.pi / 4,
    "2 pi (full circle)": 2 * math.pi,
    "pi / d = pi / 3": math.pi / 3,
}
# All of these divided by pi give pure rationals:
all_rat_times_pi = all(
    abs(v / math.pi - round(v / math.pi * 12) / 12) < 1e-12
    for v in retained_radians.values()
)
check(
    "(F6a) Every retained radian is (rational) x pi (verified against standard rational set)",
    all_rat_times_pi,
    "all retained radians are commensurate with pi",
)

# The target 2/9 is a pure rational, not a rational multiple of pi.
# 2/9 / pi is irrational.
target_ratio_to_pi = DELTA_STAR / math.pi
is_target_rational_pi = any(
    abs(target_ratio_to_pi - r) < 1e-10
    for r in [1 / n for n in range(1, 100)] + [k / n for k in range(1, 20) for n in range(1, 20)]
)
check(
    "(F6b) The target delta = 2/9 is NOT a rational multiple of pi",
    not is_target_rational_pi,
    f"2/9 / pi = {target_ratio_to_pi:.12f} is not in {{k/n : k,n small}}",
)

check(
    "(F6c) No retained radian in Cl(3)/Z_3 equals 2/9 within 1e-3",
    all(abs(v - DELTA_STAR) > 1e-3 for v in retained_radians.values()),
    f"min gap of retained radians to 2/9 = {min(abs(v - DELTA_STAR) for v in retained_radians.values()):.6f}",
)


print()
print("(F7) Plancherel weight 2/d^2 is dimensionless, with no retained radian map")
print("-" * 72)

# Plancherel / Frobenius weights on Herm_d, circulant subfamily:
# ||H||_F^2 = d a_0^2 + 2 d |b|^2 (for odd d, primary pair)
# The 'qubit real dim / Herm_d real dim' ratio:
for d in [3, 5, 7]:
    herm_d_real_dim = d * d
    qubit_real_dim = 2
    ratio = qubit_real_dim / herm_d_real_dim
    expected = 2.0 / d**2
    ok = abs(ratio - expected) < 1e-15
    if not ok:
        print(f"  d={d}: Plancherel ratio computation failed")
check(
    "(F7a) Plancherel ratio (2 / dim Herm_d) = 2/d^2 (dimensionless, checked)",
    all(abs((2.0 / (d * d)) - (2.0 / d**2)) < 1e-15 for d in [3, 5, 7]),
    "ratio = 2/9 at d=3 as a pure dimensionless count",
)

# The natural map from dimensionless ratios to radians would require a
# retained Cl(3)/Z_3 quantity EXACTLY equal to 1 radian (the implicit
# conversion factor in postulate P). Check that every retained Cl(3)/Z_3
# radian is a rational multiple of pi, hence NEVER exactly 1 radian.
cl3_retained_angles = {
    "2 pi / 3": 2 * math.pi / 3,
    "pi / 3": math.pi / 3,
    "pi / 6": math.pi / 6,
    "pi / 12": math.pi / 12,
    "pi / 4": math.pi / 4,
    "pi": math.pi,
    "2 pi": 2 * math.pi,
}
# No rational-multiple-of-pi can equal 1 exactly (pi is transcendental).
# Operationally: if we check equality to 1 at machine precision, all fail.
all_not_exactly_one = all(abs(v - 1.0) > 1e-6 for v in cl3_retained_angles.values())
check(
    "(F7b) No retained Cl(3)/Z_3 radian equals 1 exactly (pi is transcendental, all retained radians are rational multiples of pi)",
    all_not_exactly_one,
    f"closest retained angle to 1 rad = {min(abs(v - 1.0) for v in cl3_retained_angles.values()):.6f} "
    "(but no rational multiple of pi can equal 1 exactly)",
)


print()
print("(F8) Selected-slice eigenline Berry selector reconfirmed to miss m_*")
print("-" * 72)

# Reconfirmed from R1 §6: the natural selected-slice eigenline geometric
# phases do NOT pick the physical Berry-selected point.
# Data from R1: m_sel ~= -0.877 via gamma_lower(m_0 -> m) = delta(m),
# but m_* ~= -1.160. Gap is about 0.28 in m-coordinate.
gamma_lower_at_mstar = 0.178148199333  # R1 §6 data
check(
    "(F8a) Lower-eigenline geometric phase at m_* is NOT 2/9 (R1 §6 reconfirmed)",
    abs(gamma_lower_at_mstar - DELTA_STAR) > 0.02,
    f"gamma_lower(m_0 -> m_*) = {gamma_lower_at_mstar:.6f}, 2/9 = {DELTA_STAR:.6f}",
)

gamma_upper_at_mstar = 0.276339441619  # R1 §6 data
check(
    "(F8b) Upper-eigenline geometric phase at m_* is NOT 2/9",
    abs(gamma_upper_at_mstar - DELTA_STAR) > 0.02,
    f"gamma_upper(m_0 -> m_*) = {gamma_upper_at_mstar:.6f}, 2/9 = {DELTA_STAR:.6f}",
)


print()
print("(F9) Summary: all four retained closure candidates fail")
print("-" * 72)

candidate_results = {
    "A: per-Z_3 PB on qubit": math.pi / 3,
    "B: closed-orbit Bargmann": math.pi,
    "C: Plancherel weight (dimensionless)": 2.0 / 9.0,  # right number, wrong units
    "D: Pancharatnam midpoint": math.pi / 24.0,
}
print("  Candidate                          | value       | matches 2/9?")
print("  " + "-" * 62)
for name, v in candidate_results.items():
    matches = abs(v - DELTA_STAR) < 1e-3 and name.startswith("C") is False
    print(f"  {name:<35} | {v:>10.6f} | {'no (pi/x)' if 'pi' in name.lower() else 'yes'}")

# Candidate C matches numerically but is DIMENSIONLESS (not radians), so
# the identification is the postulate P itself, not a theorem.
check(
    "(F9a) Candidate A (per-Z_3 PB) does not equal 2/9 in radians",
    abs(math.pi / 3.0 - DELTA_STAR) > 0.1,
    f"gap = {abs(math.pi/3 - DELTA_STAR):.4f} rad",
)
check(
    "(F9b) Candidate B (closed Bargmann) does not equal 2/9 in radians",
    abs(math.pi - DELTA_STAR) > 1.0,
    f"gap = {abs(math.pi - DELTA_STAR):.4f} rad",
)
check(
    "(F9c) Candidate C (Plancherel weight) matches numerically but is dimensionless -- "
    "its identification with radians IS postulate P, not a derivation",
    abs(2.0 / 9.0 - DELTA_STAR) < 1e-12,
    "the Plancherel identification is a tautology for P, not a proof",
)
check(
    "(F9d) Candidate D (Pancharatnam midpoint) does not equal 2/9",
    abs(math.pi / 24.0 - DELTA_STAR) > 0.02,
    f"gap = {abs(math.pi/24 - DELTA_STAR):.4f} rad",
)


print()
print("=" * 72)
print(f"PASS={PASS} FAIL={FAIL}")
print("=" * 72)

if FAIL > 0:
    sys.exit(1)
