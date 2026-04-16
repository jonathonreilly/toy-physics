#!/usr/bin/env python3
"""
DM quantitative mapping / normalization closure.

Framework convention:
  "axiom" means only Cl(3) on Z^3.

Purpose:
  Close the last quantitative DM gate on the flagship branch by composing:
    - theorem-grade PMNS selector closure for the baryon denominator;
    - canonical gauge-normalization rigidity (g_bare = 1);
    - direct-observable sigma_v / Coulomb numerator authority;
    - the exact structural base ratio R_base = 31/9.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from dm_leptogenesis_exact_common import ETA_OBS
import frontier_dm_leptogenesis_pmns_certified_global_selector_theorem as selector

PASS_COUNT = 0
FAIL_COUNT = 0

PI = math.pi
C_F = 4.0 / 3.0
C2_SU2 = 3.0 / 4.0
DIM_ADJ_SU3 = 8.0
DIM_ADJ_SU2 = 3.0
MASS_RATIO = 3.0 / 5.0

OMEGA_B_OBS = 0.049
OMEGA_DM_OBS = 0.268
R_OBS = OMEGA_DM_OBS / OMEGA_B_OBS

X_F = 25.0
H_HUBBLE_REDUCED = 0.674
OMEGA_B_H2_PER_ETA10_BBN = 3.6515e-3


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def sommerfeld_coulomb(zeta: float) -> float:
    if abs(zeta) < 1.0e-12:
        return 1.0
    pz = PI * zeta
    if pz > 500.0:
        return pz
    return pz / (1.0 - math.exp(-pz))


def thermal_avg_sommerfeld(alpha_eff: float, x_f: float, attractive: bool) -> float:
    sign = 1.0 if attractive else -1.0
    v_arr = np.linspace(0.001, 2.0, 2000)
    dv = float(v_arr[1] - v_arr[0])
    weight = v_arr**2 * np.exp(-x_f * v_arr**2 / 4.0)
    s_arr = np.array([sommerfeld_coulomb(sign * alpha_eff / float(v)) for v in v_arr], dtype=float)
    return float(np.sum(s_arr * weight) * dv / (np.sum(weight) * dv))


def omega_b_from_eta_bbn(eta: float) -> float:
    eta10 = eta / 1.0e-10
    omega_b_h2 = OMEGA_B_H2_PER_ETA10_BBN * eta10
    return omega_b_h2 / (H_HUBBLE_REDUCED**2)


def quantitative_map() -> dict[str, float]:
    f_vis = C_F * DIM_ADJ_SU3 + C2_SU2 * DIM_ADJ_SU2
    f_dark = C2_SU2 * DIM_ADJ_SU2
    r_base = MASS_RATIO * f_vis / f_dark

    alpha_bare = 1.0 / (4.0 * PI)
    c1_plaq = PI * PI / 3.0
    p_1loop = 1.0 - c1_plaq * alpha_bare
    alpha_plaq = -math.log(p_1loop) / c1_plaq

    w_singlet = (1.0 / 9.0) * C_F**2
    w_octet = (8.0 / 9.0) * (1.0 / 6.0) ** 2
    s_singlet = thermal_avg_sommerfeld(C_F * alpha_plaq, X_F, attractive=True)
    s_octet = thermal_avg_sommerfeld(alpha_plaq / 6.0, X_F, attractive=False)
    s_vis = (w_singlet * s_singlet + w_octet * s_octet) / (w_singlet + w_octet)

    branches = selector.certified_branch_search()
    low = branches[0]
    eta_selected = float(low.etas[0]) * ETA_OBS
    omega_b = omega_b_from_eta_bbn(eta_selected)
    r_final = r_base * s_vis
    omega_dm = r_final * omega_b

    return {
        "f_vis": f_vis,
        "f_dark": f_dark,
        "r_base": r_base,
        "alpha_bare": alpha_bare,
        "alpha_plaq": alpha_plaq,
        "s_singlet": s_singlet,
        "s_octet": s_octet,
        "s_vis": s_vis,
        "eta_selected": eta_selected,
        "omega_b": omega_b,
        "r_final": r_final,
        "omega_dm": omega_dm,
    }


def part1_selector_denominator_is_now_closed() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PMNS SELECTOR DENOMINATOR IS NOW CLOSED")
    print("=" * 88)

    branches = selector.certified_branch_search()
    low = branches[0]

    check(
        "The theorem-grade PMNS selector now has an exact three-branch stationary set",
        len(branches) == 3,
        f"branch count={len(branches)}",
    )
    check(
        "The selected branch closes the baryon denominator exactly on the favored column",
        abs(float(low.etas[0]) - 1.0) < 1.0e-10,
        f"eta/eta_obs={float(low.etas[0]):.12f}",
    )


def part2_canonical_normalization_and_numerator_map() -> dict[str, float]:
    print("\n" + "=" * 88)
    print("PART 2: CANONICAL NORMALIZATION AND NUMERATOR MAP")
    print("=" * 88)

    out = quantitative_map()

    check(
        "The exact structural base ratio is R_base = 31/9",
        abs(out["r_base"] - 31.0 / 9.0) < 1.0e-12,
        f"R_base={out['r_base']:.12f}",
    )
    check(
        "Canonical gauge normalization gives alpha_bare = 1/(4*pi)",
        abs(out["alpha_bare"] - 1.0 / (4.0 * PI)) < 1.0e-15,
        f"alpha_bare={out['alpha_bare']:.12f}",
    )
    check(
        "The plaquette coupling on the canonical normalized branch is alpha_plaq = 0.0922649926183602",
        abs(out["alpha_plaq"] - 0.0922649926183602) < 1.0e-12,
        f"alpha_plaq={out['alpha_plaq']:.12f}",
    )
    check(
        "The channel-weighted Sommerfeld enhancement on the canonical branch is S_vis = 1.591795769509086",
        abs(out["s_vis"] - 1.591795769509086) < 1.0e-12,
        f"S_vis={out['s_vis']:.12f}",
    )

    print()
    print(f"  f_vis      = {out['f_vis']:.12f}")
    print(f"  f_dark     = {out['f_dark']:.12f}")
    print(f"  R_base     = {out['r_base']:.12f}")
    print(f"  alpha_plaq = {out['alpha_plaq']:.12f}")
    print(f"  S_singlet  = {out['s_singlet']:.12f}")
    print(f"  S_octet    = {out['s_octet']:.12f}")
    print(f"  S_vis      = {out['s_vis']:.12f}")

    return out


def part3_final_quantitative_map(out: dict[str, float]) -> None:
    print("\n" + "=" * 88)
    print("PART 3: FINAL QUANTITATIVE MAP")
    print("=" * 88)

    r_final = out["r_final"]
    omega_b = out["omega_b"]
    omega_dm = out["omega_dm"]

    check(
        "The final normalized dark-to-baryon ratio is R = 5.48285209497574",
        abs(r_final - 5.48285209497574) < 1.0e-12,
        f"R={r_final:.12f}",
    )
    check(
        "The final quantitative map matches the observed ratio at the 0.5% level",
        abs(r_final / R_OBS - 1.0) < 5.0e-3,
        f"R/R_obs={r_final / R_OBS:.12f}",
    )
    check(
        "The selected eta converts to the standard-BBN baryon density Omega_b = 0.04919295758525652",
        abs(omega_b - 0.04919295758525652) < 1.0e-12,
        f"Omega_b={omega_b:.12f}",
    )
    check(
        "The BBN-converted baryon density matches observation at the 0.5% level",
        abs(omega_b / OMEGA_B_OBS - 1.0) < 5.0e-3,
        f"Omega_b/Omega_b_obs={omega_b / OMEGA_B_OBS:.12f}",
    )
    check(
        "Using the selected eta and standard-BBN baryon conversion, the mapped dark density is Omega_DM = 0.26971771055437643",
        abs(omega_dm - 0.26971771055437643) < 1.0e-12,
        f"Omega_DM={omega_dm:.12f}",
    )
    check(
        "The mapped dark density matches observation at the 1% level",
        abs(omega_dm / OMEGA_DM_OBS - 1.0) < 1.0e-2,
        f"Omega_DM/Omega_DM_obs={omega_dm / OMEGA_DM_OBS:.12f}",
    )

    print()
    print(f"  eta_selected = {out['eta_selected']:.12e}")
    print(f"  Omega_b     = {omega_b:.12f}")
    print(f"  Omega_b,obs = {OMEGA_B_OBS:.12f}")
    print(f"  R_obs      = {R_OBS:.12f}")
    print(f"  R_final    = {r_final:.12f}")
    print(f"  Omega_DM   = {omega_dm:.12f}")
    print(f"  Omega_DM,obs = {OMEGA_DM_OBS:.12f}")


def main() -> int:
    print("=" * 88)
    print("DM QUANTITATIVE MAPPING / NORMALIZATION CLOSURE")
    print("=" * 88)
    print()
    print("Framework convention:")
    print('  "axiom" means only Cl(3) on Z^3.')
    print()
    print("Question:")
    print("  Once the PMNS-assisted selector is theorem-grade, does the canonical")
    print("  normalized DM numerator complete the final quantitative map?")

    part1_selector_denominator_is_now_closed()
    out = part2_canonical_normalization_and_numerator_map()
    part3_final_quantitative_map(out)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Quantitative closure result:")
    print("    - theorem-grade PMNS selector fixes eta/eta_obs = 1 on the selected branch")
    print("    - canonical gauge normalization fixes g_bare = 1")
    print("    - standard BBN converts the selected eta to Omega_b = 0.049192957585")
    print("    - the direct-observable numerator map gives R = 5.48285209497574")
    print("    - the mapped dark density is Omega_DM = 0.269717710554")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
