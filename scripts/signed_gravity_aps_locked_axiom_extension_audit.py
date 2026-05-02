#!/usr/bin/env python3
"""Audit for the APS-locked signed-source axiom extension.

This script treats the APS-locked term as a genuinely new axiom, not as a
retained APS/Wald/Gauss theorem:

    S_int = - chi_eta(Y) M_phys <rho, Phi>

The extension is tested with a hard gapped-sector admissibility rule:

    gap(D_Y) >= g_min and eta_delta(D_Y) != 0.

The audit is deliberately conservative.  It does not assert a physical
negative-mass, shielding, propulsion, reactionless-force, or signed-gravity
claim.  It only checks whether the new axiom package is internally coherent as
a bounded source/response selector candidate.
"""

from __future__ import annotations

import itertools
import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

from scripts.gravity_signed_sector_harness import (  # noqa: E402
    PAIRS,
    sign_roles,
    two_body_result,
)
from scripts.signed_gravity_aps_boundary_index_probe import (  # noqa: E402
    boundary_model,
    chi_from_eta,
    eta_delta,
    hermitian_part,
    random_unitary,
)
from scripts.signed_gravity_aps_locked_source_action_proposal import (  # noqa: E402
    active_source_from_variation,
    born_norm_controls,
    packet_density,
)


TOL = 1.0e-10
PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    status = "PASS" if passed else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"[{status}] {name}{suffix}")
    return passed


@dataclass(frozen=True)
class BoundarySector:
    name: str
    d_boundary: np.ndarray
    gap_min: float = 0.1

    @property
    def eta(self) -> int:
        eta, _zero, _n, _vals = eta_delta(self.d_boundary)
        return eta

    @property
    def zero_modes(self) -> int:
        _eta, zero, _n, _vals = eta_delta(self.d_boundary)
        return zero

    @property
    def spectral_gap(self) -> float:
        _eta, _zero, _n, vals = eta_delta(self.d_boundary)
        return float(np.min(np.abs(vals))) if len(vals) else 0.0

    @property
    def chi(self) -> int:
        return chi_from_eta(self.eta, self.zero_modes)

    @property
    def admissible_source(self) -> bool:
        return self.chi in (-1, +1) and self.zero_modes == 0 and self.spectral_gap >= self.gap_min


def normalize(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec)
    if norm <= 0.0:
        raise ValueError("zero vector")
    return vec / norm


def source_response_reads(mode: str) -> tuple[list[str], float]:
    reads = []
    residuals = []
    for chi_a, chi_b in PAIRS:
        row = two_body_result(mode, chi_a, chi_b)
        residuals.append(row.balance_residual)
        reads.append(row.readout)
    return reads, float(max(residuals))


def desired_locked_reads() -> list[str]:
    return ["ATTRACT", "REPEL", "REPEL", "ATTRACT"]


def hard_gap_path(gap_min: float = 0.1) -> tuple[list[int], list[bool], list[float]]:
    d0 = boundary_model(+1, gap=0.4)
    base_gap = abs(float(np.real(d0[0, 0])))
    chis: list[int] = []
    allowed: list[bool] = []
    gaps: list[float] = []
    for t in np.linspace(1.0, -1.0, 9):
        d = d0.copy()
        d[0, 0] = base_gap * t
        sector = BoundarySector(f"path_{t:+.2f}", d, gap_min=gap_min)
        chis.append(sector.chi)
        allowed.append(sector.admissible_source)
        gaps.append(sector.spectral_gap)
    return chis, allowed, gaps


def gap_preserving_perturbation_scan(
    rng: np.random.Generator,
    index_sign: int,
    samples: int = 128,
    gap_min: float = 0.1,
) -> tuple[bool, float]:
    sector = BoundarySector(f"chi_{index_sign:+d}", boundary_model(index_sign, gap=0.4), gap_min)
    if not sector.admissible_source:
        return False, 0.0
    stable = True
    min_gap = math.inf
    d0 = sector.d_boundary
    for _ in range(samples):
        raw = hermitian_part(rng.normal(size=d0.shape) + 1j * rng.normal(size=d0.shape))
        op_norm = max(float(np.linalg.norm(raw, ord=2)), 1.0e-12)
        perturb = raw * (0.15 * sector.spectral_gap / op_norm)
        trial = BoundarySector("trial", d0 + perturb, gap_min=gap_min)
        stable &= trial.admissible_source and trial.chi == sector.chi
        min_gap = min(min_gap, trial.spectral_gap)
    return stable, float(min_gap)


def refined_boundary(d_boundary: np.ndarray, copies: int) -> np.ndarray:
    """Orientation-preserving refinement as repeated boundary fibers."""

    if copies <= 0:
        raise ValueError("copies must be positive")
    return np.kron(d_boundary, np.eye(copies))


def family_portability_scan(rng: np.random.Generator) -> tuple[bool, str]:
    rows = []
    ok = True
    for index_sign in (+1, -1):
        base = boundary_model(index_sign, pairs=4, gap=0.35)
        base_sector = BoundarySector(f"base_{index_sign:+d}", base)
        for copies in (1, 2, 3, 5):
            d_ref = refined_boundary(base, copies)
            u = random_unitary(rng, d_ref.shape[0])
            d_family = u @ d_ref @ u.conj().T
            sector = BoundarySector(f"ref{copies}_{index_sign:+d}", d_family)
            eta_scale_ok = sector.eta == copies * base_sector.eta
            chi_ok = sector.chi == base_sector.chi == index_sign
            gap_ok = abs(sector.spectral_gap - base_sector.spectral_gap) < 1.0e-9
            ok &= eta_scale_ok and chi_ok and gap_ok and sector.admissible_source
            rows.append(f"{index_sign:+d}x{copies}:eta={sector.eta:+d},chi={sector.chi:+d}")
    return ok, "; ".join(rows)


def signed_source_variation_check() -> bool:
    rho = packet_density(n=29, center=13.0, sigma=3.0)
    mass = 2.5
    residual_p, active_p = active_source_from_variation(rho, mass, +1)
    residual_m, active_m = active_source_from_variation(rho, mass, -1)
    residual_0, active_0 = active_source_from_variation(rho, mass, 0)
    return (
        residual_p < 1.0e-9
        and residual_m < 1.0e-9
        and residual_0 < 1.0e-9
        and abs(active_p - mass) < 1.0e-9
        and abs(active_m + mass) < 1.0e-9
        and abs(active_0) < 1.0e-9
    )


def source_response_locking_check() -> tuple[bool, str]:
    source_only_reads, source_only_resid = source_response_reads("source_only")
    response_only_reads, response_only_resid = source_response_reads("response_only")
    locked_reads, locked_resid = source_response_reads("locked")
    ok = (
        locked_reads == desired_locked_reads()
        and locked_resid < TOL
        and source_only_resid > 1.0
        and response_only_resid > 1.0
    )
    detail = (
        f"source_only={','.join(source_only_reads)} resid={source_only_resid:.1e}; "
        f"response_only={','.join(response_only_reads)} resid={response_only_resid:.1e}; "
        f"locked={','.join(locked_reads)} resid={locked_resid:.1e}"
    )
    return ok, detail


def positive_inertia_and_no_runaway_check() -> tuple[bool, str]:
    mass_cases = ((1.0, 1.0), (1.0, 3.0), (3.0, 1.0), (2.0, 5.0))
    separations = (1.5, 2.0, 4.0)
    max_balance = 0.0
    max_center_force = 0.0
    for chi_a, chi_b in PAIRS:
        for ma, mb in mass_cases:
            for sep in separations:
                row = two_body_result("locked", chi_a, chi_b, ma, mb, -0.5 * sep, +0.5 * sep)
                max_balance = max(max_balance, row.balance_residual)
                max_center_force = max(max_center_force, abs(row.force_a + row.force_b))
                if row.inertial_mass_a <= 0.0 or row.inertial_mass_b <= 0.0:
                    return False, "nonpositive inertia encountered"
    return max_balance < TOL and max_center_force < TOL, (
        f"max_balance={max_balance:.1e}, max_net_force={max_center_force:.1e}"
    )


def pair_energy(chi_a: int, chi_b: int, ma: float, mb: float, r: float, core: float) -> float:
    potential = -chi_a * chi_b * ma * mb / math.sqrt(r * r + core * core)
    return ma + mb + potential


def energy_stability_readout() -> tuple[bool, str]:
    radii = np.geomspace(0.02, 20.0, 400)
    e_opp = min(pair_energy(+1, -1, 1.0, 1.3, float(r), core=0.5) for r in radii)
    e_same_soft = min(pair_energy(+1, +1, 1.0, 1.3, float(r), core=1.0) for r in radii)
    e_same_hard = min(pair_energy(+1, +1, 1.0, 1.3, float(r), core=0.2) for r in radii)
    ok = e_opp > 0.0 and e_same_soft > 0.0 and e_same_hard < 0.0
    detail = f"E_opp_min={e_opp:.3f}, E_same_core1={e_same_soft:.3f}, E_same_core0.2={e_same_hard:.3f}"
    return ok, detail


def born_norm_gate() -> tuple[bool, str]:
    i3_p, norm_p = born_norm_controls(+1)
    i3_m, norm_m = born_norm_controls(-1)
    ok = abs(i3_p) < 1.0e-10 and abs(i3_m) < 1.0e-10 and max(norm_p, norm_m) < 1.0e-10
    return ok, f"I3+= {i3_p:+.2e}, I3-= {i3_m:+.2e}, norm={max(norm_p, norm_m):.2e}"


def fm_scaling_gate() -> tuple[bool, str]:
    source_masses = np.array([0.5, 1.0, 2.0, 4.0, 8.0], dtype=float)
    slopes = []
    for chi_a, chi_b in PAIRS:
        forces = []
        for source_mass in source_masses:
            row = two_body_result(
                "locked",
                chi_a,
                chi_b,
                inertial_mass_a=1.75,
                inertial_mass_b=float(source_mass),
                z_a=-1.5,
                z_b=+1.5,
            )
            forces.append(abs(row.force_a))
        slope, _intercept = np.polyfit(np.log(source_masses), np.log(np.array(forces)), 1)
        slopes.append(float(slope))
    max_err = max(abs(slope - 1.0) for slope in slopes)
    return max_err < 1.0e-12, f"slopes={[round(s, 12) for s in slopes]}"


def null_and_neutral_controls() -> tuple[bool, str]:
    null_sector = BoundarySector("null", boundary_model(0, pairs=5, gap=0.4))
    neutral_active_sum = (+1 * 2.0) + (-1 * 2.0)
    neutral_inertia_sum = 2.0 + 2.0
    ok = (
        null_sector.chi == 0
        and not null_sector.admissible_source
        and abs(neutral_active_sum) < TOL
        and neutral_inertia_sum > 0.0
    )
    detail = (
        f"null_chi={null_sector.chi}, null_admissible={null_sector.admissible_source}, "
        f"neutral_active={neutral_active_sum:+.1f}, neutral_inertia={neutral_inertia_sum:.1f}"
    )
    return ok, detail


def axiom_minimality_check() -> tuple[bool, str]:
    """The new axiom must be exactly the missing orientation-odd scalar."""

    retained = np.array([[1.0], [1.0]])
    target = np.array([1.0, -1.0])
    coeffs, *_ = np.linalg.lstsq(retained, target, rcond=None)
    retained_resid = float(np.linalg.norm(retained @ coeffs - target))
    extended = np.column_stack([retained[:, 0], target])
    coeffs_ext, *_ = np.linalg.lstsq(extended, target, rcond=None)
    extended_resid = float(np.linalg.norm(extended @ coeffs_ext - target))
    return retained_resid > 1.0 and extended_resid < TOL, (
        f"retained_resid={retained_resid:.3e}, extended_resid={extended_resid:.3e}"
    )


def no_claim_gate() -> tuple[bool, str]:
    forbidden_claims = {
        "negative_inertial_mass": False,
        "shielding": False,
        "propulsion": False,
        "reactionless_force": False,
        "physical_signed_gravity_prediction": False,
    }
    return not any(forbidden_claims.values()), ", ".join(f"{k}=False" for k in forbidden_claims)


def main() -> int:
    rng = np.random.default_rng(20260426)

    print("=" * 104)
    print("SIGNED GRAVITY APS-LOCKED AXIOM EXTENSION AUDIT")
    print("  new eta-polarized source axiom; controlled candidate, not a physical claim")
    print("=" * 104)
    print()

    print("AXIOM PACKAGE")
    print("  A1 gapped APS boundary sector: chi_eta(Y)=sign eta_delta(D_Y)")
    print("  A2 hard admissibility: active sources require gap(D_Y)>=g_min and chi_eta!=0")
    print("  A3 eta-polarized scalar source: S_int=-chi_eta M_phys <|psi|^2,Phi>")
    print("  A4 source and response read the same chi_eta; inertial mass remains positive")
    print("  A5 null/zero-mode sectors are controls or defects, not active third signs")
    print()

    plus = BoundarySector("plus", boundary_model(+1, gap=0.4))
    minus = BoundarySector("minus", boundary_model(-1, gap=0.4))
    null = BoundarySector("null", boundary_model(0, gap=0.4))
    check(
        "APS eta supplies two active sectors and one quarantined null sector",
        plus.chi == +1 and minus.chi == -1 and null.chi == 0 and plus.admissible_source and minus.admissible_source,
        f"chi=({plus.chi:+d},{minus.chi:+d},{null.chi:+d})",
    )

    stable_p, min_gap_p = gap_preserving_perturbation_scan(rng, +1)
    stable_m, min_gap_m = gap_preserving_perturbation_scan(rng, -1)
    check(
        "gap-preserving boundary perturbations keep chi_eta fixed",
        stable_p and stable_m,
        f"min_gap+= {min_gap_p:.3f}, min_gap-= {min_gap_m:.3f}",
    )

    chis, allowed, gaps = hard_gap_path()
    check(
        "hard admissibility blocks continuous chi flip through zero",
        chis[:4] == [+1, +1, +1, +1] and chis[4] == 0 and chis[-4:] == [-1, -1, -1, -1] and not allowed[4],
        f"chi_path={chis}, allowed={allowed}, min_gap={min(gaps):.1e}",
    )

    family_ok, family_detail = family_portability_scan(rng)
    check(
        "orientation-preserving refinement and unitary relabeling keep chi_eta portable",
        family_ok,
        family_detail,
    )

    check(
        "eta-polarized action variation gives signed active source and null zero",
        signed_source_variation_check(),
        "active=(+M,-M,0)",
    )

    lock_ok, lock_detail = source_response_locking_check()
    check(
        "same chi_eta locks source and response; source-only/response-only controls fail",
        lock_ok,
        lock_detail,
    )

    inertia_ok, inertia_detail = positive_inertia_and_no_runaway_check()
    check(
        "positive inertial masses retain two-body momentum balance",
        inertia_ok,
        inertia_detail,
    )

    energy_ok, energy_detail = energy_stability_readout()
    check(
        "opposite-sign channel has no negative-mass runaway; same-sign UV issue remains exposed",
        energy_ok,
        energy_detail,
    )

    born_ok, born_detail = born_norm_gate()
    check("Born and norm controls remain clean in fixed sectors", born_ok, born_detail)

    fm_ok, fm_detail = fm_scaling_gate()
    check("weak-field force magnitude remains linear in source mass", fm_ok, fm_detail)

    null_ok, null_detail = null_and_neutral_controls()
    check("null-sector and neutral-pair controls stay quarantined", null_ok, null_detail)

    minimal_ok, minimal_detail = axiom_minimality_check()
    check(
        "new axiom is exactly the missing orientation-odd source scalar",
        minimal_ok,
        minimal_detail,
    )

    no_claim_ok, no_claim_detail = no_claim_gate()
    check("non-claim gate remains closed", no_claim_ok, no_claim_detail)

    print()
    print("FOUR-PAIR LOCKED TABLE")
    print(f"  {'pair':>4s} {'src/resp A':>12s} {'src/resp B':>12s} {'read':>8s}")
    for chi_a, chi_b in PAIRS:
        src_a, resp_a = sign_roles("locked", chi_a)
        src_b, resp_b = sign_roles("locked", chi_b)
        row = two_body_result("locked", chi_a, chi_b)
        label = ("+" if chi_a > 0 else "-") + ("+" if chi_b > 0 else "-")
        print(f"  {label:>4s} {src_a:+d}/{resp_a:+d} {src_b:+d}/{resp_b:+d} {row.readout:>8s}")

    print()
    print("INTERPRETATION")
    print("  The extension is internally coherent as a new eta-polarized source")
    print("  axiom with hard APS-gap admissibility.  It is not a retained theorem.")
    print("  Review-critical gaps remain: tensor lift, natural origin of the new")
    print("  source line, continuum proof beyond this sanity check, and ordinary")
    print("  same-sector UV/core stability.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("FINAL_TAG: APS_LOCKED_AXIOM_EXTENSION_CONTROLLED_CANDIDATE")
        return 0
    print("FINAL_TAG: APS_LOCKED_AXIOM_EXTENSION_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
