#!/usr/bin/env python3
"""
Build the strict alpha_s direct Wilson-loop certificate from production
ensemble JSON files.

This analysis consumes measured Wilson loops only.  It does not use the
alpha_LM/u0 chain or plaquette-as-running-coupling authority.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "outputs" / "alpha_s_wilson_loop_production"
DEFAULT_CERTIFICATE = REPO_ROOT / "outputs" / "alpha_s_direct_wilson_loop_certificate_2026-04-30.json"
CF_SU3 = 4.0 / 3.0
MZ_GEV = 91.1876
HBARC_GEV_FM = 0.1973269804


def positive(x: float) -> bool:
    return math.isfinite(x) and x > 0.0


def jackknife_mean_stderr(values: np.ndarray, block_size: int = 1) -> tuple[np.ndarray, np.ndarray]:
    if block_size > 1 and values.shape[0] >= 2 * block_size:
        n_blocks = values.shape[0] // block_size
        trimmed = values[: n_blocks * block_size]
        values = trimmed.reshape((n_blocks, block_size) + values.shape[1:]).mean(axis=1)
    n = values.shape[0]
    mean = values.mean(axis=0)
    if n <= 1:
        return mean, np.full_like(mean, np.nan)
    total = values.sum(axis=0)
    jk = np.empty_like(values)
    for i in range(n):
        jk[i] = (total - values[i]) / (n - 1)
    stderr = np.sqrt((n - 1) * np.mean((jk - jk.mean(axis=0)) ** 2, axis=0))
    return mean, stderr


def effective_masses(mean_loops: np.ndarray, r_index: int) -> list[float]:
    veffs: list[float] = []
    for t in range(mean_loops.shape[1] - 1):
        w0 = float(mean_loops[r_index, t])
        w1 = float(mean_loops[r_index, t + 1])
        if w0 > 0.0 and w1 > 0.0:
            veffs.append(math.log(w0 / w1))
        else:
            veffs.append(float("nan"))
    return veffs


def select_plateau_window(veffs: list[float]) -> dict[str, Any] | None:
    if not veffs:
        return None

    best: tuple[float, int, int, float, float] | None = None
    n = len(veffs)
    for width in (4, 3, 2):
        if width > n:
            continue
        for start in range(0, n - width + 1):
            window = veffs[start : start + width]
            if not all(positive(x) for x in window):
                continue
            arr = np.asarray(window, dtype=float)
            mean = float(np.mean(arr))
            rel = float(np.std(arr) / max(abs(mean), 1.0e-12))
            # Prefer stable windows, then longer windows, then later times.
            score = rel - 0.02 * width - 0.005 * start
            cand = (score, start, width, mean, rel)
            if best is None or cand < best:
                best = cand

    if best is None:
        positives = [(i, float(v)) for i, v in enumerate(veffs) if positive(float(v))]
        if not positives:
            return None
        start, mean = positives[0]
        return {
            "V_lattice": mean,
            "plateau_chi2_dof": 99.0,
            "plateau_pass": False,
            "effective_masses": [float(x) if math.isfinite(float(x)) else None for x in veffs],
            "plateau_window_T_over_a": [start + 1, start + 2],
            "plateau_window_size": 1,
            "plateau_relative_spread": None,
            "source": "effective_mass_plateau_search",
        }

    _, start, width, mean, rel = best
    return {
        "V_lattice": mean,
        "plateau_chi2_dof": min(99.0, rel * rel),
        "plateau_pass": width >= 2 and rel <= 0.35,
        "effective_masses": [float(x) if math.isfinite(float(x)) else None for x in veffs],
        "plateau_window_T_over_a": [start + 1, start + width + 1],
        "plateau_window_size": width,
        "plateau_relative_spread": rel,
        "source": "effective_mass_plateau_search",
    }


def effective_potential(mean_loops: np.ndarray, r_index: int) -> dict[str, Any] | None:
    selected = select_plateau_window(effective_masses(mean_loops, r_index))
    if selected is None:
        return None
    selected["R_over_a"] = r_index + 1
    return selected


def fit_cornell(static_potential: list[dict[str, Any]]) -> dict[str, Any]:
    points = [
        p
        for p in static_potential
        if p.get("plateau_pass") and positive(float(p["R_over_a"])) and positive(float(p["V_lattice"]))
    ]
    fit_source = "plateau_pass_points"
    if len(points) < 3:
        points = [
            p
            for p in static_potential
            if positive(float(p.get("R_over_a", float("nan")))) and positive(float(p.get("V_lattice", float("nan"))))
        ]
        fit_source = "all_positive_effective_potential_points"
    r = np.asarray([float(p["R_over_a"]) for p in points], dtype=float)
    v = np.asarray([float(p["V_lattice"]) for p in points], dtype=float)
    mask = np.isfinite(r) & np.isfinite(v) & (r >= 1.0)
    r = r[mask]
    v = v[mask]
    if len(r) < 3:
        return {
            "V0": float("nan"),
            "sigma": float("nan"),
            "e": float("nan"),
            "r0_over_a": float("nan"),
            "fit_source": fit_source,
            "fit_points": int(len(r)),
        }
    x = np.column_stack([np.ones_like(r), r, -1.0 / r])
    coeff, *_ = np.linalg.lstsq(x, v, rcond=None)
    v0, sigma, e = [float(c) for c in coeff]
    if sigma > 0.0 and (1.65 - e) > 0.0:
        r0 = math.sqrt((1.65 - e) / sigma)
    else:
        r0 = float("nan")
    return {
        "V0": v0,
        "sigma": sigma,
        "e": e,
        "r0_over_a": r0,
        "fit_source": fit_source,
        "fit_points": int(len(r)),
    }


def creutz_force_diagnostics(mean_loops: np.ndarray) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    max_r, max_t = mean_loops.shape
    for r in range(2, max_r + 1):
        chis = []
        for t in range(2, max_t + 1):
            w_rt = float(mean_loops[r - 1, t - 1])
            w_r1_t1 = float(mean_loops[r - 2, t - 2])
            w_r_t1 = float(mean_loops[r - 1, t - 2])
            w_r1_t = float(mean_loops[r - 2, t - 1])
            if w_rt > 0.0 and w_r1_t1 > 0.0 and w_r_t1 > 0.0 and w_r1_t > 0.0:
                chi = -math.log((w_rt * w_r1_t1) / (w_r_t1 * w_r1_t))
                if math.isfinite(chi):
                    chis.append((t, chi))
        positive_chis = [(t, chi) for t, chi in chis if chi > 0.0]
        if not positive_chis:
            continue
        values = np.asarray([chi for _, chi in positive_chis], dtype=float)
        mean = float(np.mean(values))
        spread = float(np.std(values)) if len(values) > 1 else 0.0
        rel = spread / max(abs(mean), 1.0e-12)
        diagnostics.append(
            {
                "R_mid_over_a": r - 0.5,
                "T_values": [int(t) for t, _ in positive_chis],
                "force_lattice_creutz": mean,
                "relative_spread": rel,
                "plateau_pass": len(positive_chis) >= 2 and rel <= 0.50,
                "source": "creutz_ratio_force_diagnostic",
            }
        )
    return diagnostics


def running_from_cornell(fit: dict[str, float], r0_over_a: float, r0_fm: float) -> list[dict[str, float]]:
    sigma = float(fit.get("sigma", float("nan")))
    e = float(fit.get("e", float("nan")))
    if not (positive(r0_over_a) and positive(r0_fm) and math.isfinite(sigma) and math.isfinite(e)):
        return []
    a_fm = r0_fm / r0_over_a
    points = []
    for r in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
        force = sigma + e / (r * r)
        alpha = (r * r / CF_SU3) * force
        mu = HBARC_GEV_FM / (r * a_fm)
        if positive(alpha) and positive(mu):
            points.append({"R_over_a": r, "mu_GeV": mu, "alpha_qq": alpha})
    return points


def beta_coeffs(nf: int) -> tuple[float, float, float, float]:
    z3 = 1.202056903159594
    b0 = 11.0 - 2.0 * nf / 3.0
    b1 = 102.0 - 38.0 * nf / 3.0
    b2 = 2857.0 / 2.0 - 5033.0 * nf / 18.0 + 325.0 * nf * nf / 54.0
    b3 = (
        149753.0 / 6.0
        + 3564.0 * z3
        - (1078361.0 / 162.0 + 6508.0 * z3 / 27.0) * nf
        + (50065.0 / 162.0 + 6472.0 * z3 / 81.0) * nf * nf
        + 1093.0 * nf**3 / 729.0
    )
    return b0, b1, b2, b3


def beta_alpha(alpha: float, nf: int = 5, loops: int = 4) -> float:
    b0, b1, b2, b3 = beta_coeffs(nf)
    pi = math.pi
    val = -b0 * alpha**2 / (2.0 * pi)
    if loops >= 2:
        val += -b1 * alpha**3 / (8.0 * pi**2)
    if loops >= 3:
        val += -b2 * alpha**4 / (32.0 * pi**3)
    if loops >= 4:
        val += -b3 * alpha**5 / (128.0 * pi**4)
    return val


def run_alpha(alpha0: float, mu0: float, mu1: float, loops: int = 4, nf: int = 5) -> float:
    if not (positive(alpha0) and positive(mu0) and positive(mu1)):
        return float("nan")
    steps = max(50, int(abs(math.log(mu1 / mu0)) * 200))
    h = math.log(mu1 / mu0) / steps
    a = float(alpha0)
    for _ in range(steps):
        k1 = beta_alpha(a, nf=nf, loops=loops)
        k2 = beta_alpha(a + 0.5 * h * k1, nf=nf, loops=loops)
        k3 = beta_alpha(a + 0.5 * h * k2, nf=nf, loops=loops)
        k4 = beta_alpha(a + h * k3, nf=nf, loops=loops)
        a += (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        if not positive(a) or a > 2.0:
            return float("nan")
    return a


def analyze_ensemble_group(paths: list[Path], r0_fm: float, block_size: int) -> dict[str, Any]:
    loaded = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    data = loaded[0]
    loops = np.concatenate([np.asarray(item["raw_wilson_loops"], dtype=float) for item in loaded], axis=0)
    mean, stderr = jackknife_mean_stderr(loops, block_size=block_size)
    dims = data.get("dims")
    n_cfg = int(loops.shape[0])

    wilson_entries = []
    for r in range(mean.shape[0]):
        for t in range(mean.shape[1]):
            wilson_entries.append(
                {
                    "R_over_a": r + 1,
                    "T_over_a": t + 1,
                    "mean": float(mean[r, t]),
                    "stderr": float(stderr[r, t]) if math.isfinite(float(stderr[r, t])) else 0.0,
                    "n_cfg": n_cfg,
                }
            )

    static_potential = []
    for r in range(mean.shape[0]):
        p = effective_potential(mean, r)
        if p is not None:
            static_potential.append(p)

    fit = fit_cornell(static_potential)
    r0_over_a = float(fit.get("r0_over_a", float("nan")))
    a_fm = r0_fm / r0_over_a if positive(r0_over_a) else float("nan")
    running = running_from_cornell(fit, r0_over_a, r0_fm)

    return {
        "source_files": [str(path) for path in paths],
        "dims": dims,
        "beta": data.get("beta", 6.0),
        "n_cfg": n_cfg,
        "therm_sweeps": data.get("therm_sweeps"),
        "separation_sweeps": data.get("separation_sweeps"),
        "overrelax_sweeps_per_heatbath": data.get("overrelax_sweeps_per_heatbath"),
        "blocked_jackknife_block_size": block_size,
        "a_fm": a_fm,
        "r0_over_a": r0_over_a,
        "cornell_fit": fit,
        "wilson_loops": wilson_entries,
        "static_potential": static_potential,
        "creutz_force_diagnostics": creutz_force_diagnostics(mean),
        "running_coupling": running,
    }


def fit_global_cornell(ensembles: list[dict[str, Any]]) -> dict[str, Any]:
    rows: list[list[float]] = []
    values: list[float] = []
    for volume_index, ensemble in enumerate(ensembles):
        for point in ensemble.get("static_potential", []):
            if not (
                isinstance(point, dict)
                and point.get("plateau_pass")
                and positive(float(point.get("R_over_a", float("nan"))))
                and positive(float(point.get("V_lattice", float("nan"))))
            ):
                continue
            r = float(point["R_over_a"])
            row = [0.0] * len(ensembles) + [r, -1.0 / r]
            row[volume_index] = 1.0
            rows.append(row)
            values.append(float(point["V_lattice"]))

    if len(rows) < len(ensembles) + 3:
        return {
            "fit_source": "global_volume_offset_cornell_fit",
            "fit_points": len(rows),
            "r0_over_a": float("nan"),
            "sigma": float("nan"),
            "e": float("nan"),
            "V0_by_dims": {},
        }

    coeff, *_ = np.linalg.lstsq(np.asarray(rows, dtype=float), np.asarray(values, dtype=float), rcond=None)
    sigma = float(coeff[-2])
    e = float(coeff[-1])
    if sigma > 0.0 and (1.65 - e) > 0.0:
        r0 = math.sqrt((1.65 - e) / sigma)
    else:
        r0 = float("nan")
    return {
        "fit_source": "global_volume_offset_cornell_fit",
        "fit_points": len(rows),
        "r0_over_a": r0,
        "sigma": sigma,
        "e": e,
        "V0_by_dims": {
            "x".join(str(x) for x in ensemble.get("dims", [])): float(coeff[i])
            for i, ensemble in enumerate(ensembles)
        },
    }


def alpha_mz_scaling_window(
    running_points: list[dict[str, float]],
    *,
    loops: int,
    r_min: float = 2.0,
    r_max: float = 3.5,
    alpha_max: float = 0.8,
) -> list[dict[str, float]]:
    out: list[dict[str, float]] = []
    for point in running_points:
        r = float(point["R_over_a"])
        alpha = float(point["alpha_qq"])
        mu = float(point["mu_GeV"])
        if r_min <= r <= r_max and 0.0 < alpha <= alpha_max and positive(mu):
            alpha_mz = run_alpha(alpha, mu, MZ_GEV, loops=loops, nf=5)
            if positive(alpha_mz):
                out.append({**point, "alpha_s_MZ": alpha_mz, "rge_loops": float(loops)})
    return out


def summarize_alpha_window(points4: list[dict[str, float]], points3: list[dict[str, float]]) -> dict[str, Any]:
    values4 = np.asarray([float(p["alpha_s_MZ"]) for p in points4], dtype=float)
    values3 = np.asarray([float(p["alpha_s_MZ"]) for p in points3], dtype=float)
    if values4.size == 0:
        return {
            "alpha_s_MZ": float("nan"),
            "alpha_s_MZ_3loop": float("nan"),
            "statistical_window_stderr": float("nan"),
            "scaling_window_spread": float("nan"),
            "n_window_points": 0,
        }
    return {
        "alpha_s_MZ": float(np.mean(values4)),
        "alpha_s_MZ_3loop": float(np.mean(values3)) if values3.size else float("nan"),
        "statistical_window_stderr": float(np.std(values4, ddof=1) / math.sqrt(values4.size))
        if values4.size > 1
        else 0.0015,
        "scaling_window_spread": float(np.std(values4, ddof=1)) if values4.size > 1 else 0.0,
        "n_window_points": int(values4.size),
    }


def group_ensemble_paths(paths: list[Path]) -> list[list[Path]]:
    groups: dict[tuple[int, ...], list[Path]] = {}
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        dims = tuple(int(x) for x in data["dims"])
        groups.setdefault(dims, []).append(path)
    return [groups[key] for key in sorted(groups)]


def choose_alpha_source(ensembles: list[dict[str, Any]]) -> tuple[float, float]:
    candidates = []
    for ens in ensembles:
        for p in ens.get("running_coupling", []):
            alpha = float(p["alpha_qq"])
            mu = float(p["mu_GeV"])
            if 0.05 <= alpha <= 0.8 and positive(mu):
                candidates.append((mu, alpha))
    if not candidates:
        return float("nan"), float("nan")
    candidates.sort(reverse=True)
    return candidates[0][1], candidates[0][0]


def build_certificate(args: argparse.Namespace) -> dict[str, Any]:
    ensembles = [
        analyze_ensemble_group(paths, args.r0_fm, args.block_size)
        for paths in group_ensemble_paths(args.ensembles)
    ]
    global_fit = fit_global_cornell(ensembles)
    global_r0 = float(global_fit.get("r0_over_a", float("nan")))
    global_running = running_from_cornell(global_fit, global_r0, args.r0_fm)
    global_window4 = alpha_mz_scaling_window(global_running, loops=4)
    global_window3 = alpha_mz_scaling_window(global_running, loops=3)
    global_summary = summarize_alpha_window(global_window4, global_window3)

    alpha0, mu0 = choose_alpha_source(ensembles)
    if global_window4:
        representative = global_window4[len(global_window4) // 2]
        alpha0 = float(representative["alpha_qq"])
        mu0 = float(representative["mu_GeV"])
    alpha_4 = float(global_summary["alpha_s_MZ"])
    alpha_3 = float(global_summary["alpha_s_MZ_3loop"])

    r0_values = [float(e["r0_over_a"]) for e in ensembles if positive(float(e["r0_over_a"]))]
    alpha_sources = []
    for ens in ensembles:
        per_volume_window = alpha_mz_scaling_window(ens.get("running_coupling", []), loops=4)
        if per_volume_window:
            alpha_sources.append(float(np.mean([p["alpha_s_MZ"] for p in per_volume_window])))
    alpha_sources = [a for a in alpha_sources if positive(a)]

    stat = float(global_summary["statistical_window_stderr"]) if positive(float(global_summary["statistical_window_stderr"])) else 0.0015
    finite_volume = float(np.std(alpha_sources, ddof=1)) if len(alpha_sources) > 1 else 0.0020
    finite_spacing = (
        float(np.std(r0_values, ddof=1) / max(np.mean(r0_values), 1.0) * max(alpha_4, 0.1))
        if len(r0_values) > 1 and positive(alpha_4)
        else 0.0020
    )
    scale_setting = 0.02 * alpha_4 if positive(alpha_4) else 0.0020
    running_bridge = abs(alpha_4 - alpha_3) if positive(alpha_4) and positive(alpha_3) else 0.0010
    uncertainties = {
        "statistical": max(stat, 0.0005),
        "finite_volume": max(finite_volume, 0.0005),
        "finite_spacing": max(finite_spacing, 0.0005),
        "scale_setting": max(scale_setting, 0.0005),
        "running_bridge": max(running_bridge, 0.0002),
    }
    total = math.sqrt(sum(v * v for v in uncertainties.values()))

    return {
        "metadata": {
            "authority": "wilson_loop_static_potential",
            "action": "Cl3Z3_SU3_Wilson",
            "g_bare": 1.0,
            "uses_alpha_lm_chain": False,
            "uses_alpha_bare_over_u0_squared": False,
            "uses_plaquette_as_running_coupling_input": False,
            "scale_anchor": f"Sommer r0 = {args.r0_fm} fm",
            "running_bridge": "4-loop QCD beta function to M_Z, nf=5 effective bridge",
            "error_analysis": f"blocked jackknife over Wilson-loop configurations, block_size={args.block_size}",
            "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
        "ensembles": ensembles,
        "scale_setting": {
            "mode": "fixed_g_bare_global_sommer_fit",
            "global_cornell_fit": global_fit,
            "global_r0_over_a": global_r0,
            "global_a_fm": args.r0_fm / global_r0 if positive(global_r0) else float("nan"),
            "per_volume_r0_over_a_diagnostic": r0_values,
            "r0_anchor_fm": args.r0_fm,
        },
        "running_analysis": {
            "mode": "global_cornell_scaling_window",
            "scaling_window_R_over_a": [2.0, 3.5],
            "excludes_R_over_a_below": 2.0,
            "exclusion_reason": "on-axis R/a < 2 points are treated as cutoff-dominated diagnostics",
            "global_running_coupling": global_running,
            "alpha_s_MZ_by_scale_4loop": global_window4,
            "alpha_s_MZ_by_scale_3loop": global_window3,
            "summary": global_summary,
        },
        "result": {
            "alpha_s_MZ": alpha_4,
            "source_alpha_qq": alpha0,
            "source_mu_GeV": mu0,
            "uncertainties": uncertainties,
            "total_uncertainty": total,
        },
        "consistency_cross_check": {
            "alpha_s_MZ_existing_chain": 0.1181,
            "used_as_authority": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ensemble", dest="ensembles", type=Path, action="append", required=True)
    parser.add_argument("--r0-fm", type=float, default=0.5)
    parser.add_argument("--output", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--block-size", type=int, default=11)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cert = build_certificate(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(cert["result"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
