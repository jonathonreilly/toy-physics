#!/usr/bin/env python3
"""
Direct staggered-correlator top-Yukawa audit gate.

This runner intentionally separates two modes:

* Scout mode (--scout): tiny-lattice infrastructure smoke test. It exercises a
  Wilson-link update skeleton, a gauge-dressed heavy staggered correlator, an
  effective-mass plateau readout, and a single-exponential fitter. Scout output
  is not theorem evidence.

* Strict mode (default): production-certificate validator. It fails until a
  production staggered-correlator certificate exists and demonstrates a direct
  mass extraction followed by y_t(v) = sqrt(2) m_t(v) / v.

The strict gate rejects certificates that use the prior Ward / H_unit /
matrix-element route or the alpha_LM / plaquette coupling chain as authority.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE = REPO_ROOT / "outputs" / "yt_direct_lattice_correlator_certificate_2026-04-30.json"

PDG_TOP_MASS_GEV = 172.56
PDG_TOP_MASS_SIGMA_GEV = 0.31
LEGACY_ATLAS_TOP_MASS_GEV = 172.69
YT_V_TARGET = 0.917
YT_V_MAX_UNCERTAINTY = 0.010
MT_MAX_UNCERTAINTY_GEV = 1.0
DEFAULT_V_GEV = 246.21965
RATIO_TARGET = 1.0 / math.sqrt(6.0)

PRODUCTION_UPDATE_ALGORITHMS = {
    "HMC",
    "RHMC",
    "HMC_SU3_WILSON_STAGGERED",
    "RHMC_SU3_WILSON_STAGGERED",
    "CABIBBO-MARINARI HEATBATH",
    "CABIBBO-MARINARI HEATBATH + POLAR OVERRELAXATION",
    "CABIBBO-MARINARI HEAT-BATH",
    "CABIBBO-MARINARI HEAT-BATH + POLAR OVERRELAXATION",
}

FORBIDDEN_AUTHORITY_FRAGMENTS = (
    "h_unit",
    "ward_identity",
    "ward_yukawa",
    "matrix_element_yukawa",
    "composite_yukawa_definition",
    "bare_yukawa",
    "alpha_lm",
    "alpha_bare_over_u0",
    "plaquette_yukawa",
)


class Gate:
    def __init__(self) -> None:
        self.pass_count = 0
        self.fail_count = 0

    def check(self, name: str, condition: bool, detail: str = "", kind: str = "STRICT-GATE") -> bool:
        status = "PASS" if condition else "FAIL"
        if condition:
            self.pass_count += 1
        else:
            self.fail_count += 1
        suffix = f"  ({detail})" if detail else ""
        print(f"  [{status}] [{kind}] {name}{suffix}")
        return condition


def positive_finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value)) and float(value) > 0.0


def finite_nonnegative(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value)) and float(value) >= 0.0


def load_certificate(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("certificate root must be a JSON object")
    return data


def collect_forbidden_paths(obj: Any, prefix: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_l = str(key).lower()
            if any(fragment in key_l for fragment in FORBIDDEN_AUTHORITY_FRAGMENTS):
                hits.append(f"{prefix}.{key}")
            hits.extend(collect_forbidden_paths(value, f"{prefix}.{key}"))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            hits.extend(collect_forbidden_paths(value, f"{prefix}[{i}]"))
    elif isinstance(obj, str):
        value_l = obj.lower()
        if any(fragment in value_l for fragment in FORBIDDEN_AUTHORITY_FRAGMENTS):
            hits.append(prefix)
    return hits


def spatial_l_from_ensemble(ensemble: dict[str, Any]) -> int | None:
    if isinstance(ensemble.get("spatial_L"), int):
        return int(ensemble["spatial_L"])
    dims = ensemble.get("dims")
    if isinstance(dims, list) and len(dims) >= 3 and all(isinstance(v, int) and v > 0 for v in dims[:3]):
        if len(set(dims[:3])) == 1:
            return int(dims[0])
    return None


def production_update_algorithm(algorithm: Any) -> bool:
    algorithm_u = str(algorithm).upper().strip()
    algorithm_norm = algorithm_u.replace("_", " ")
    allowed_norm = {item.replace("_", " ") for item in PRODUCTION_UPDATE_ALGORITHMS}
    if algorithm_u in PRODUCTION_UPDATE_ALGORITHMS or algorithm_norm in allowed_norm:
        return True
    return "CABIBBO-MARINARI" in algorithm_norm and "HEAT" in algorithm_norm


def validate_metadata(gate: Gate, data: dict[str, Any]) -> None:
    metadata = data.get("metadata", {})
    gate.check("metadata block exists", isinstance(metadata, dict))
    if not isinstance(metadata, dict):
        return

    gate.check(
        "certificate declares staggered top-correlator authority",
        metadata.get("authority") == "staggered_top_correlator_mass_extraction",
        f"authority={metadata.get('authority')!r}",
    )
    gate.check(
        "certificate declares production phase",
        metadata.get("phase") == "production",
        f"phase={metadata.get('phase')!r}",
    )
    gate.check(
        "certificate declares Cl3Z3 Wilson-staggered surface at g_bare = 1",
        metadata.get("action") in {"Cl3Z3_Wilson_staggered", "Cl3Z3_SU3_Wilson_staggered"}
        and abs(float(metadata.get("g_bare", float("nan"))) - 1.0) < 1e-12,
        f"action={metadata.get('action')!r}, g_bare={metadata.get('g_bare')!r}",
    )
    gate.check(
        "prior Ward/composite/coupling-definition routes are not authority",
        metadata.get("uses_prior_ward_chain") is False
        and metadata.get("uses_composite_matrix_element_route") is False
        and metadata.get("uses_coupling_definition_route") is False,
        "all three flags must be false",
    )

    v_input = data.get("v_input", {})
    gate.check("v input is declared as substrate input only", isinstance(v_input, dict))
    if isinstance(v_input, dict):
        gate.check(
            "v input has substrate-only treatment and finite value",
            v_input.get("treatment") == "substrate_input_only" and positive_finite(v_input.get("v_GeV")),
            f"treatment={v_input.get('treatment')!r}, v={v_input.get('v_GeV')!r}",
        )

    forbidden = collect_forbidden_paths(data)
    gate.check(
        "certificate does not contain forbidden authority markers",
        not forbidden,
        ", ".join(forbidden[:8]) if forbidden else "no forbidden markers",
    )


def validate_ensembles(gate: Gate, data: dict[str, Any]) -> None:
    ensembles = data.get("ensembles")
    gate.check("certificate contains production ensembles", isinstance(ensembles, list) and len(ensembles) > 0)
    if not isinstance(ensembles, list):
        return

    spatial_ls: set[int] = set()
    spacing_labels: set[str] = set()
    bc_ok = 0
    hmc_ok = 0
    production_stats_ok = 0
    mass_scan_points = 0
    correlator_channels = 0
    plateau_ok = 0

    for ensemble in ensembles:
        if not isinstance(ensemble, dict):
            continue
        spatial_l = spatial_l_from_ensemble(ensemble)
        if spatial_l is not None:
            spatial_ls.add(spatial_l)
        a_fm = ensemble.get("a_fm")
        r0_over_a = ensemble.get("r0_over_a")
        if positive_finite(a_fm):
            spacing_labels.add(f"a={float(a_fm):.6f}")
        if positive_finite(r0_over_a):
            spacing_labels.add(f"r0/a={float(r0_over_a):.6f}")

        bc = ensemble.get("boundary_conditions", {})
        if (
            isinstance(bc, dict)
            and bc.get("gauge_spatial") == "periodic"
            and bc.get("gauge_time") == "periodic"
            and bc.get("fermion_time") == "antiperiodic"
        ):
            bc_ok += 1

        if production_update_algorithm(ensemble.get("update_algorithm", "")):
            hmc_ok += 1

        therm = ensemble.get("thermalization_sweeps")
        meas = ensemble.get("measurement_sweeps")
        separation = ensemble.get("measurement_separation_sweeps")
        if (
            isinstance(therm, int)
            and therm >= 1000
            and isinstance(meas, int)
            and meas >= 1000
            and isinstance(separation, int)
            and separation >= 20
        ):
            production_stats_ok += 1

        scan = ensemble.get("mass_parameter_scan", [])
        if isinstance(scan, list):
            mass_scan_points += len(scan)

        correlators = ensemble.get("correlators", [])
        if isinstance(correlators, list):
            for corr in correlators:
                if not isinstance(corr, dict):
                    continue
                tau = corr.get("tau")
                mean = corr.get("mean")
                stderr = corr.get("stderr")
                if isinstance(tau, int) and tau >= 0 and positive_finite(mean) and finite_nonnegative(stderr):
                    correlator_channels += 1

        fit = ensemble.get("mass_fit", {})
        if isinstance(fit, dict):
            tau_min = fit.get("tau_min")
            tau_max = fit.get("tau_max")
            chi2 = fit.get("chi2_dof")
            mass = fit.get("m_lat")
            if (
                isinstance(tau_min, int)
                and isinstance(tau_max, int)
                and tau_max > tau_min
                and positive_finite(chi2)
                and float(chi2) <= 2.0
                and positive_finite(mass)
            ):
                plateau_ok += 1

    gate.check(
        "production set includes 12^3, 16^3, and 24^3 spatial volumes",
        {12, 16, 24}.issubset(spatial_ls),
        f"spatial_L={sorted(spatial_ls)}",
    )
    gate.check(
        "scale control includes at least two independent spacing anchors",
        len(spacing_labels) >= 2,
        f"spacing labels={sorted(spacing_labels)}",
    )
    gate.check(
        "all production ensembles use required boundary conditions",
        bc_ok == len(ensembles),
        f"ok={bc_ok}/{len(ensembles)}",
    )
    gate.check(
        "all production ensembles use an accepted production update algorithm",
        hmc_ok == len(ensembles),
        f"ok={hmc_ok}/{len(ensembles)}",
    )
    gate.check(
        "all production ensembles meet thermalization/statistics floor",
        production_stats_ok == len(ensembles),
        f"ok={production_stats_ok}/{len(ensembles)}",
    )
    gate.check(
        "heavy mass parameter scan/tuning evidence is present",
        mass_scan_points >= 3,
        f"scan points={mass_scan_points}",
    )
    gate.check(
        "correlator data contain enough time-slice measurements",
        correlator_channels >= 24,
        f"qualified correlator points={correlator_channels}",
    )
    gate.check(
        "mass fits report plateau windows with acceptable chi2/dof",
        plateau_ok >= len(ensembles),
        f"plateau_ok={plateau_ok}/{len(ensembles)}",
    )


def validate_result(gate: Gate, data: dict[str, Any]) -> None:
    result = data.get("result", {})
    gate.check("result block exists", isinstance(result, dict))
    if not isinstance(result, dict):
        return

    v_input = data.get("v_input", {})
    v_gev = float(v_input.get("v_GeV", DEFAULT_V_GEV)) if isinstance(v_input, dict) else DEFAULT_V_GEV
    m_run = result.get("m_t_running_at_v_GeV")
    y_t = result.get("y_t_v")
    m_pole = result.get("m_t_pole_GeV")
    y_unc = result.get("total_y_t_uncertainty")
    mt_unc = result.get("total_m_t_pole_uncertainty_GeV")
    uncertainties = result.get("uncertainties", {})

    gate.check("m_t(v), m_t(pole), and y_t(v) are finite positive numbers",
               positive_finite(m_run) and positive_finite(m_pole) and positive_finite(y_t),
               f"m_run={m_run!r}, m_pole={m_pole!r}, y_t={y_t!r}")
    gate.check(
        "uncertainty budget includes all required components",
        isinstance(uncertainties, dict)
        and {
            "statistical",
            "heavy_mass_tuning",
            "finite_volume",
            "finite_spacing",
            "scale_setting",
            "matching",
            "running_bridge",
            "v_input",
        }
        <= set(uncertainties),
        f"components={sorted(uncertainties) if isinstance(uncertainties, dict) else 'missing'}",
    )
    gate.check(
        "total uncertainties are finite and sub-percent scale",
        positive_finite(y_unc)
        and positive_finite(mt_unc)
        and float(y_unc) <= YT_V_MAX_UNCERTAINTY
        and float(mt_unc) <= MT_MAX_UNCERTAINTY_GEV,
        f"dy={y_unc!r}, dmt={mt_unc!r}",
    )

    if positive_finite(m_run) and positive_finite(y_t) and positive_finite(v_gev):
        computed_y = math.sqrt(2.0) * float(m_run) / v_gev
        tolerance = max(5.0e-5, 0.05 * float(y_unc)) if positive_finite(y_unc) else 5.0e-5
        gate.check(
            "y_t(v) is computed from measured m_t(v) and substrate v",
            abs(float(y_t) - computed_y) <= tolerance,
            f"reported={float(y_t):.8f}, computed={computed_y:.8f}, v={v_gev:.5f}",
        )

    if positive_finite(m_pole) and positive_finite(mt_unc):
        combined = math.sqrt(PDG_TOP_MASS_SIGMA_GEV**2 + float(mt_unc) ** 2)
        gate.check(
            "m_t(pole) agrees with current PDG average within one combined sigma",
            abs(float(m_pole) - PDG_TOP_MASS_GEV) <= combined,
            f"m_t={float(m_pole):.4f}, PDG={PDG_TOP_MASS_GEV:.2f}+/-{PDG_TOP_MASS_SIGMA_GEV:.2f}",
        )
        gate.check(
            "m_t(pole) remains compatible with historical 172.69 GeV cross-check",
            abs(float(m_pole) - LEGACY_ATLAS_TOP_MASS_GEV) <= max(float(mt_unc), 0.5),
            f"m_t={float(m_pole):.4f}, legacy={LEGACY_ATLAS_TOP_MASS_GEV:.2f}",
            kind="CONSISTENCY-ONLY",
        )

    if positive_finite(y_t) and positive_finite(y_unc):
        gate.check(
            "y_t(v) agrees with stated SM running comparator",
            abs(float(y_t) - YT_V_TARGET) <= float(y_unc),
            f"y_t={float(y_t):.6f}, target={YT_V_TARGET:.6f}, sigma={float(y_unc):.6f}",
        )


def validate_ratio_check(gate: Gate, data: dict[str, Any]) -> None:
    ratio = data.get("ratio_check", {})
    gate.check("measured y_t/g_s ratio block exists", isinstance(ratio, dict))
    if not isinstance(ratio, dict):
        return

    value = ratio.get("ratio")
    uncertainty = ratio.get("uncertainty")
    gate.check(
        "ratio block declares independent measured quantities, not a definition",
        ratio.get("used_as_definition") is False
        and ratio.get("g_s_source") == "independent_direct_measurement"
        and positive_finite(ratio.get("y_t_lattice"))
        and positive_finite(ratio.get("g_s_lattice")),
        f"used_as_definition={ratio.get('used_as_definition')!r}, g_s_source={ratio.get('g_s_source')!r}",
    )
    gate.check(
        "measured y_t/g_s agrees with 1/sqrt(6) within uncertainty",
        positive_finite(value)
        and positive_finite(uncertainty)
        and float(uncertainty) <= 0.02
        and abs(float(value) - RATIO_TARGET) <= float(uncertainty),
        f"ratio={value!r}, target={RATIO_TARGET:.8f}, sigma={uncertainty!r}",
    )


def print_missing_certificate(path: Path) -> None:
    print("\nSTRICT GATE BLOCKED")
    print(f"  Missing production staggered-correlator certificate: {path}")
    print("\nRequired certificate schema, in outline:")
    print("  metadata.authority = 'staggered_top_correlator_mass_extraction'")
    print("  metadata.phase = 'production'")
    print("  metadata.action in {'Cl3Z3_Wilson_staggered', 'Cl3Z3_SU3_Wilson_staggered'}")
    print("  metadata.g_bare = 1.0")
    print("  metadata.uses_prior_ward_chain = false")
    print("  metadata.uses_composite_matrix_element_route = false")
    print("  metadata.uses_coupling_definition_route = false")
    print("  v_input.treatment = 'substrate_input_only'")
    print("  ensembles[] with spatial_L in {12,16,24}, accepted production updates, correlators[], mass_fit{}")
    print("  thermalization_sweeps >= 1000, measurement_sweeps >= 1000, separation >= 20")
    print("  result.m_t_running_at_v_GeV, result.y_t_v, result.m_t_pole_GeV, full uncertainties")
    print("  ratio_check with independently measured y_t_lattice/g_s_lattice, used_as_definition=false")


def template() -> dict[str, Any]:
    return {
        "metadata": {
            "authority": "staggered_top_correlator_mass_extraction",
            "phase": "production",
            "action": "Cl3Z3_SU3_Wilson_staggered",
            "g_bare": 1.0,
            "uses_prior_ward_chain": False,
            "uses_composite_matrix_element_route": False,
            "uses_coupling_definition_route": False,
            "scale_anchor": "Sommer r0 or explicitly equivalent physical length anchor",
            "running_bridge": "standard SM/QCD RGE with stated loop order and thresholds",
        },
        "v_input": {
            "source": "existing electroweak VEV chain",
            "treatment": "substrate_input_only",
            "v_GeV": DEFAULT_V_GEV,
        },
        "ensembles": [],
        "result": {
            "m_t_running_at_v_GeV": None,
            "y_t_v": None,
            "m_t_pole_GeV": None,
            "uncertainties": {
                "statistical": None,
                "heavy_mass_tuning": None,
                "finite_volume": None,
                "finite_spacing": None,
                "scale_setting": None,
                "matching": None,
                "running_bridge": None,
                "v_input": None,
            },
            "total_y_t_uncertainty": None,
            "total_m_t_pole_uncertainty_GeV": None,
        },
        "ratio_check": {
            "y_t_lattice": None,
            "g_s_lattice": None,
            "g_s_source": "independent_direct_measurement",
            "ratio": None,
            "uncertainty": None,
            "used_as_definition": False,
        },
    }


def random_su3_near_identity(rng: np.random.Generator, epsilon: float = 0.16) -> np.ndarray:
    h = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
    h = (h + h.conj().T) / 2.0
    h -= np.trace(h) * np.eye(3) / 3.0
    x = np.eye(3, dtype=complex) + 1j * epsilon * h
    q, r = np.linalg.qr(x)
    d = np.diag(r)
    phases = d / np.abs(d)
    q = q @ np.diag(np.conj(phases))
    det = np.linalg.det(q)
    q *= np.exp(-1j * np.angle(det) / 3.0)
    return q


def cold_links(lattice_size: int, time_extent: int) -> dict[tuple[int, int, int, int], list[np.ndarray]]:
    links: dict[tuple[int, int, int, int], list[np.ndarray]] = {}
    for coords in np.ndindex(lattice_size, lattice_size, lattice_size, time_extent):
        links[coords] = [np.eye(3, dtype=complex) for _ in range(4)]
    return links


def shifted(x: tuple[int, int, int, int], mu: int, step: int, lattice_size: int, time_extent: int) -> tuple[int, int, int, int]:
    y = list(x)
    period = time_extent if mu == 3 else lattice_size
    y[mu] = (y[mu] + step) % period
    return (y[0], y[1], y[2], y[3])


def compute_staple(
    links: dict[tuple[int, int, int, int], list[np.ndarray]],
    x: tuple[int, int, int, int],
    mu: int,
    lattice_size: int,
    time_extent: int,
) -> np.ndarray:
    staple = np.zeros((3, 3), dtype=complex)
    xp = shifted(x, mu, +1, lattice_size, time_extent)
    for nu in range(4):
        if nu == mu:
            continue
        xpn = shifted(x, nu, +1, lattice_size, time_extent)
        xm = shifted(x, nu, -1, lattice_size, time_extent)
        xpm = shifted(xp, nu, -1, lattice_size, time_extent)
        staple += (
            links[xp][nu]
            @ links[xpn][mu].conj().T
            @ links[x][nu].conj().T
        )
        staple += (
            links[xpm][nu].conj().T
            @ links[xm][mu].conj().T
            @ links[xm][nu]
        )
    return staple


def hmc_skeleton_sweep(
    links: dict[tuple[int, int, int, int], list[np.ndarray]],
    lattice_size: int,
    time_extent: int,
    beta: float,
    rng: np.random.Generator,
) -> tuple[int, int, float]:
    accepted = 0
    total = 0
    max_delta_h = 0.0
    for coords in np.ndindex(lattice_size, lattice_size, lattice_size, time_extent):
        x = (coords[0], coords[1], coords[2], coords[3])
        for mu in range(4):
            old = links[x][mu]
            staple = compute_staple(links, x, mu, lattice_size, time_extent)
            proposal = random_su3_near_identity(rng) @ old
            delta_h = -(beta / 3.0) * np.trace((proposal - old) @ staple).real
            max_delta_h = max(max_delta_h, abs(float(delta_h)))
            total += 1
            if delta_h < 0.0 or rng.random() < math.exp(-min(float(delta_h), 700.0)):
                links[x][mu] = proposal
                accepted += 1
    return accepted, total, max_delta_h


def temporal_transporter_trace(
    links: dict[tuple[int, int, int, int], list[np.ndarray]],
    spatial: tuple[int, int, int],
    tau: int,
    time_extent: int,
) -> float:
    w = np.eye(3, dtype=complex)
    x = (spatial[0], spatial[1], spatial[2], 0)
    for _ in range(tau):
        w = w @ links[x][3]
        x = (x[0], x[1], x[2], (x[3] + 1) % time_extent)
    return float(np.trace(w).real / 3.0)


def measure_heavy_staggered_correlator(
    links: dict[tuple[int, int, int, int], list[np.ndarray]],
    lattice_size: int,
    time_extent: int,
    mass_lat: float,
) -> list[float]:
    values: list[float] = []
    for tau in range(1, time_extent // 2 + 1):
        traces = []
        for spatial in np.ndindex(lattice_size, lattice_size, lattice_size):
            traces.append(temporal_transporter_trace(links, (spatial[0], spatial[1], spatial[2]), tau, time_extent))
        gauge_factor = max(1.0e-12, abs(float(np.mean(traces))))
        forward = math.exp(-mass_lat * tau)
        backward = math.exp(-mass_lat * (time_extent - tau))
        oscillating = 0.03 * ((-1.0) ** tau) * math.exp(-(mass_lat + 0.9) * tau)
        values.append(gauge_factor * (forward + backward + oscillating))
    return values


def effective_masses(correlator: list[float]) -> list[float]:
    masses: list[float] = []
    for left, right in zip(correlator, correlator[1:]):
        if left > 0.0 and right > 0.0:
            masses.append(math.log(left / right))
    return masses


def fit_single_exponential(
    taus: np.ndarray,
    means: np.ndarray,
    stderr: np.ndarray,
    tau_min: int,
    tau_max: int,
) -> tuple[float, float, float]:
    mask = (taus >= tau_min) & (taus <= tau_max) & (means > 0.0)
    if int(np.sum(mask)) < 2:
        return float("nan"), float("nan"), float("nan")
    x = taus[mask].astype(float)
    y = np.log(means[mask])
    sigma = np.maximum(stderr[mask] / means[mask], 1.0e-6)
    weights = 1.0 / (sigma * sigma)
    design = np.vstack([np.ones_like(x), -x]).T
    normal = design.T @ (weights[:, None] * design)
    rhs = design.T @ (weights * y)
    cov = np.linalg.inv(normal)
    coeff = cov @ rhs
    residual = y - design @ coeff
    dof = max(1, len(y) - 2)
    chi2_dof = float(np.sum(weights * residual * residual) / dof)
    mass = float(coeff[1])
    mass_err = float(math.sqrt(max(cov[1, 1], 0.0)))
    return mass, mass_err, chi2_dof


def run_scout(args: argparse.Namespace) -> int:
    gate = Gate()
    rng = np.random.default_rng(args.seed)
    volumes = [int(v) for v in args.scout_volumes.split(",") if v.strip()]

    print("=" * 78)
    print("Direct staggered-correlator y_t infrastructure scout")
    print("=" * 78)
    print("SCOUT ONLY: this does not certify m_t or y_t.")
    print(
        f"spatial_L={volumes}, therm={args.scout_therm}, meas={args.scout_meas}, "
        f"mass_lat={args.mass_lat:.3f}, beta=6"
    )

    all_masses: list[float] = []
    total_potential_points = 0
    all_generated = True
    all_finite = True

    for lattice_size in volumes:
        time_extent = max(args.time_extent, 2 * lattice_size)
        links = cold_links(lattice_size, time_extent)
        accepted = 0
        total = 0
        max_delta_h = 0.0
        for _ in range(args.scout_therm):
            a, n, dh = hmc_skeleton_sweep(links, lattice_size, time_extent, 6.0, rng)
            accepted += a
            total += n
            max_delta_h = max(max_delta_h, dh)

        samples: list[list[float]] = []
        for _ in range(args.scout_meas):
            a, n, dh = hmc_skeleton_sweep(links, lattice_size, time_extent, 6.0, rng)
            accepted += a
            total += n
            max_delta_h = max(max_delta_h, dh)
            samples.append(measure_heavy_staggered_correlator(links, lattice_size, time_extent, args.mass_lat))

        arr = np.asarray(samples, dtype=float)
        means = np.mean(arr, axis=0)
        stderr = np.std(arr, axis=0, ddof=1) / math.sqrt(max(len(samples), 1)) if len(samples) > 1 else np.zeros_like(means)
        finite = bool(np.all(np.isfinite(means)) and np.all(means > 0.0))
        all_finite = all_finite and finite
        all_generated = all_generated and total > 0
        eff = effective_masses([float(v) for v in means])
        taus = np.arange(1, len(means) + 1)
        tau_max = min(len(means), max(2, len(means) - 1))
        mass, mass_err, chi2_dof = fit_single_exponential(taus, means, stderr + 1.0e-6, 1, tau_max)
        if math.isfinite(mass):
            all_masses.append(mass)
        acc_rate = accepted / total if total else 0.0
        total_potential_points += len(means)

        print(
            f"  L={lattice_size}^3 x {time_extent}: acc={acc_rate:.3f}, "
            f"C1={means[0]:.6e}, C2={means[1] if len(means) > 1 else float('nan'):.6e}, "
            f"m_fit={mass:.5f}+/-{mass_err:.5f}, chi2/dof={chi2_dof:.3f}"
        )
        gate.check(
            f"L={lattice_size} HMC skeleton generated configurations",
            total > 0 and 0.0 < acc_rate < 1.0 and math.isfinite(max_delta_h),
            f"updates={total}, acceptance={acc_rate:.3f}, max_deltaH={max_delta_h:.3f}",
            kind="SCOUT-ONLY",
        )
        gate.check(
            f"L={lattice_size} correlator and effective masses are finite",
            finite and len(means) >= 4 and bool(eff) and all(math.isfinite(v) for v in eff),
            f"time_slices={len(means)}, m_eff[0:3]={[round(v, 5) for v in eff[:3]]}",
            kind="SCOUT-ONLY",
        )
        gate.check(
            f"L={lattice_size} single-exponential fitter recovers mass scale",
            math.isfinite(mass)
            and math.isfinite(mass_err)
            and mass_err >= 0.0
            and 0.2 * args.mass_lat <= mass <= 5.0 * args.mass_lat,
            f"fit={mass:.5f}, injected_scout_scale={args.mass_lat:.5f}",
            kind="SCOUT-ONLY",
        )

    if all_masses:
        mean_mass = float(np.mean(all_masses))
        scout_v_lat = math.sqrt(2.0) * args.mass_lat / YT_V_TARGET
        scout_y = math.sqrt(2.0) * mean_mass / scout_v_lat
    else:
        mean_mass = float("nan")
        scout_y = float("nan")

    gate.check(
        "scout covers multiple volumes with enough correlator points",
        len(set(volumes)) >= 2 and all_generated and all_finite and total_potential_points >= 8,
        f"volumes={volumes}, correlator_points={total_potential_points}",
        kind="SCOUT-ONLY",
    )
    gate.check(
        "mass-to-yukawa arithmetic path is finite",
        math.isfinite(scout_y) and scout_y > 0.0,
        f"diagnostic_y={scout_y:.5f} from mean scout mass={mean_mass:.5f}",
        kind="SCOUT-ONLY",
    )

    print(f"\nSCOUT SUMMARY: PASS={gate.pass_count}  FAIL={gate.fail_count}")
    if gate.fail_count:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--certificate",
        type=Path,
        default=DEFAULT_CERTIFICATE,
        help="Path to a production staggered-correlator JSON certificate.",
    )
    parser.add_argument("--print-template", action="store_true", help="Print the strict certificate template and exit.")
    parser.add_argument("--scout", action="store_true", help="Run tiny-lattice infrastructure smoke test.")
    parser.add_argument("--scout-volumes", default="4,6", help="Comma-separated spatial L values for --scout.")
    parser.add_argument("--scout-therm", type=int, default=1, help="Thermalization sweeps for --scout.")
    parser.add_argument("--scout-meas", type=int, default=3, help="Measurement sweeps for --scout.")
    parser.add_argument("--time-extent", type=int, default=8, help="Minimum temporal extent for --scout.")
    parser.add_argument("--mass-lat", type=float, default=0.75, help="Injected scout heavy mass scale.")
    parser.add_argument("--seed", type=int, default=20260430, help="Random seed for --scout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.print_template:
        print(json.dumps(template(), indent=2, sort_keys=True))
        return 0
    if args.scout:
        return run_scout(args)

    gate = Gate()
    print("=" * 78)
    print("Direct staggered-correlator y_t(v) strict audit gate")
    print("=" * 78)
    print(f"certificate: {args.certificate}")

    try:
        data = load_certificate(args.certificate)
    except FileNotFoundError:
        print_missing_certificate(args.certificate)
        gate.check("production staggered-correlator certificate is present", False, str(args.certificate))
        print(f"\nSUMMARY: PASS={gate.pass_count}  FAIL={gate.fail_count}")
        return 1
    except Exception as exc:
        gate.check("production staggered-correlator certificate can be parsed", False, repr(exc))
        print(f"\nSUMMARY: PASS={gate.pass_count}  FAIL={gate.fail_count}")
        return 1

    validate_metadata(gate, data)
    validate_ensembles(gate, data)
    validate_result(gate, data)
    validate_ratio_check(gate, data)

    print(f"\nSUMMARY: PASS={gate.pass_count}  FAIL={gate.fail_count}")
    if gate.fail_count:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    print("Strict gate passed: direct staggered-correlator y_t route is ready for audit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
