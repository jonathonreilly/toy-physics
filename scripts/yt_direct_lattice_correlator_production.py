#!/usr/bin/env python3
"""
Resumable Wilson-staggered top-correlator production harness.

This script is intentionally evidence-conservative.  It implements the
production machinery requested by the direct-correlator y_t lane:

* SU(3) Wilson gauge updates with Cabibbo-Marinari SU(2) subgroup heat-bath
  steps and an optional polar-projection overrelaxation sweep.
* APE smearing of spatial links for the measurement operator.
* Staggered Dirac operator with antiperiodic temporal fermion boundary
  conditions.
* Propagator inversion through conjugate gradient on D^dagger D.
* Point-source staggered correlator measurement, effective-mass fit, jackknife
  statistical errors, and strict-runner certificate emission.

The default command runs a reduced-scope smoke/feasibility measurement because
the requested 12^3x24, 16^3x32, and 24^3x48 production campaign with 1000+
thermalization sweeps and 1000+ saved configurations is not feasible as an
interactive PR update.  Use --production-targets to configure the full campaign;
the emitted certificate will still be rejected by the strict runner unless the
required volumes/statistics are actually present.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import cg


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "outputs" / "yt_direct_lattice_correlator"
DEFAULT_CERTIFICATE = REPO_ROOT / "outputs" / "yt_direct_lattice_correlator_certificate_2026-04-30.json"

NC = 3
NDIM = 4
BETA = 6.0
HBARC_GEV_FM = 0.1973269804
R0_FM = 0.5
R0_OVER_A_BETA6_REFERENCE = 5.37
V_GEV = 246.21965
PDG_TOP_MASS_GEV = 172.56
YT_TARGET = 0.917


def project_su3(mat: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(mat)
    d = np.diag(r)
    phase = np.ones_like(d)
    mask = np.abs(d) > 1.0e-14
    phase[mask] = d[mask] / np.abs(d[mask])
    q = q @ np.diag(np.conj(phase))
    det = np.linalg.det(q)
    q *= np.exp(-1j * np.angle(det) / 3.0)
    return q


def random_su2_quaternion(rng: np.random.Generator) -> np.ndarray:
    q = rng.normal(size=4)
    q /= np.linalg.norm(q)
    return q


def quaternion_to_su2(q: np.ndarray) -> np.ndarray:
    a0, a1, a2, a3 = q
    return np.array(
        [[a0 + 1j * a3, a2 + 1j * a1], [-a2 + 1j * a1, a0 - 1j * a3]],
        dtype=complex,
    )


def su2_heatbath_quaternion(k: float, rng: np.random.Generator) -> np.ndarray:
    if k < 1.0e-10:
        return random_su2_quaternion(rng)
    two_k = 2.0 * k
    a0 = 0.0
    for _ in range(10000):
        r = rng.random()
        if two_k > 100.0:
            a0 = 1.0 + math.log(max(r + (1.0 - r) * math.exp(-2.0 * two_k), 1.0e-300)) / two_k
        else:
            a0 = math.log(r * math.exp(two_k) + (1.0 - r) * math.exp(-two_k)) / two_k
        if -1.0 <= a0 <= 1.0 and rng.random() < math.sqrt(max(1.0 - a0 * a0, 0.0)):
            break
    else:
        a0 = 0.99
    radius = math.sqrt(max(1.0 - a0 * a0, 0.0))
    phi = 2.0 * math.pi * rng.random()
    cos_theta = 2.0 * rng.random() - 1.0
    sin_theta = math.sqrt(max(1.0 - cos_theta * cos_theta, 0.0))
    return np.array(
        [
            a0,
            radius * sin_theta * math.cos(phi),
            radius * sin_theta * math.sin(phi),
            radius * cos_theta,
        ]
    )


def subgroup_indices(subgroup: int) -> tuple[int, int]:
    if subgroup == 0:
        return (0, 1)
    if subgroup == 1:
        return (0, 2)
    return (1, 2)


def extract_su2(mat: np.ndarray, subgroup: int) -> np.ndarray:
    idx = subgroup_indices(subgroup)
    return mat[np.ix_(idx, idx)]


def embed_su2(mat: np.ndarray, subgroup: int) -> np.ndarray:
    out = np.eye(3, dtype=complex)
    idx = subgroup_indices(subgroup)
    for i2, i3 in enumerate(idx):
        for j2, j3 in enumerate(idx):
            out[i3, j3] = mat[i2, j2]
    return out


def project_su2(mat: np.ndarray) -> np.ndarray:
    det = np.linalg.det(mat)
    if abs(det) < 1.0e-30:
        return np.eye(2, dtype=complex)
    v = mat / np.sqrt(det)
    a = (v[0, 0] + np.conj(v[1, 1])) / 2.0
    b = (v[1, 0] - np.conj(v[0, 1])) / 2.0
    norm = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
    if norm < 1.0e-30:
        return np.eye(2, dtype=complex)
    a /= norm
    b /= norm
    return np.array([[a, -np.conj(b)], [b, np.conj(a)]], dtype=complex)


@dataclass(frozen=True)
class Geometry:
    spatial_l: int
    time_l: int

    @property
    def dims(self) -> tuple[int, int, int, int]:
        return (self.time_l, self.spatial_l, self.spatial_l, self.spatial_l)

    @property
    def volume(self) -> int:
        return self.time_l * self.spatial_l**3

    def site_index(self, coords: tuple[int, int, int, int]) -> int:
        t, x, y, z = coords
        l = self.spatial_l
        return ((t * l + x) * l + y) * l + z

    def site_coords(self, index: int) -> tuple[int, int, int, int]:
        l = self.spatial_l
        z = index % l
        index //= l
        y = index % l
        index //= l
        x = index % l
        t = index // l
        return (t, x, y, z)

    def shifted(self, coords: tuple[int, int, int, int], mu: int, step: int) -> tuple[int, int, int, int]:
        out = list(coords)
        out[mu] = (out[mu] + step) % self.dims[mu]
        return (out[0], out[1], out[2], out[3])


class GaugeField:
    def __init__(self, geom: Geometry) -> None:
        self.geom = geom
        self.u = np.zeros((*geom.dims, NDIM, NC, NC), dtype=complex)
        for coords in np.ndindex(*geom.dims):
            self.u[coords] = np.eye(NC, dtype=complex)

    def copy(self) -> "GaugeField":
        other = GaugeField(self.geom)
        other.u = self.u.copy()
        return other

    def staple(self, coords: tuple[int, int, int, int], mu: int) -> np.ndarray:
        acc = np.zeros((NC, NC), dtype=complex)
        xp_mu = self.geom.shifted(coords, mu, +1)
        for nu in range(NDIM):
            if nu == mu:
                continue
            xp_nu = self.geom.shifted(coords, nu, +1)
            xm_nu = self.geom.shifted(coords, nu, -1)
            xp_mu_m_nu = self.geom.shifted(xp_mu, nu, -1)
            acc += (
                self.u[xp_mu][nu]
                @ self.u[xp_nu][mu].conj().T
                @ self.u[coords][nu].conj().T
            )
            acc += (
                self.u[xp_mu_m_nu][nu].conj().T
                @ self.u[xm_nu][mu].conj().T
                @ self.u[xm_nu][nu]
            )
        return acc

    def heatbath_link(self, coords: tuple[int, int, int, int], mu: int, rng: np.random.Generator) -> None:
        staple = self.staple(coords, mu)
        for subgroup in range(3):
            w = self.u[coords][mu] @ staple
            w2 = extract_su2(w, subgroup)
            det_w2 = np.linalg.det(w2)
            scale = math.sqrt(max(float(np.real(det_w2)), 0.0))
            if scale < 1.0e-15:
                r_new = quaternion_to_su2(random_su2_quaternion(rng))
                rotation = r_new
            else:
                k = (BETA / NC) * scale
                r_new = quaternion_to_su2(su2_heatbath_quaternion(k, rng))
                rotation = r_new @ project_su2(w2).conj().T
            self.u[coords][mu] = embed_su2(rotation, subgroup) @ self.u[coords][mu]
        self.u[coords][mu] = project_su3(self.u[coords][mu])

    def heatbath_sweep(self, rng: np.random.Generator) -> None:
        for coords in np.ndindex(*self.geom.dims):
            c = (coords[0], coords[1], coords[2], coords[3])
            for mu in range(NDIM):
                self.heatbath_link(c, mu, rng)

    def overrelax_link(self, coords: tuple[int, int, int, int], mu: int) -> None:
        staple = self.staple(coords, mu)
        target = project_su3(staple.conj().T)
        self.u[coords][mu] = project_su3(target @ self.u[coords][mu].conj().T @ target)

    def overrelax_sweep(self) -> None:
        for coords in np.ndindex(*self.geom.dims):
            c = (coords[0], coords[1], coords[2], coords[3])
            for mu in range(NDIM):
                self.overrelax_link(c, mu)

    def plaquette(self) -> float:
        total = 0.0
        count = 0
        for coords in np.ndindex(*self.geom.dims):
            c = (coords[0], coords[1], coords[2], coords[3])
            for mu in range(NDIM):
                for nu in range(mu + 1, NDIM):
                    xp_mu = self.geom.shifted(c, mu, +1)
                    xp_nu = self.geom.shifted(c, nu, +1)
                    p = (
                        self.u[c][mu]
                        @ self.u[xp_mu][nu]
                        @ self.u[xp_nu][mu].conj().T
                        @ self.u[c][nu].conj().T
                    )
                    total += float(np.trace(p).real / NC)
                    count += 1
        return total / count


def ape_smear_spatial(gauge: GaugeField, alpha: float, steps: int) -> GaugeField:
    out = gauge.copy()
    for _ in range(steps):
        new_u = out.u.copy()
        for coords in np.ndindex(*out.geom.dims):
            c = (coords[0], coords[1], coords[2], coords[3])
            for mu in (1, 2, 3):
                staple = np.zeros((NC, NC), dtype=complex)
                for nu in (1, 2, 3):
                    if nu == mu:
                        continue
                    xp_mu = out.geom.shifted(c, mu, +1)
                    xp_nu = out.geom.shifted(c, nu, +1)
                    xm_nu = out.geom.shifted(c, nu, -1)
                    xp_mu_m_nu = out.geom.shifted(xp_mu, nu, -1)
                    staple += (
                        out.u[c][nu]
                        @ out.u[xp_nu][mu]
                        @ out.u[xp_mu][nu].conj().T
                    )
                    staple += (
                        out.u[xm_nu][nu].conj().T
                        @ out.u[xm_nu][mu]
                        @ out.u[xp_mu_m_nu][nu]
                    )
                new_u[c][mu] = project_su3((1.0 - alpha) * out.u[c][mu] + (alpha / 4.0) * staple)
        out.u = new_u
    return out


def staggered_eta(mu: int, coords: tuple[int, int, int, int]) -> float:
    return -1.0 if sum(coords[:mu]) % 2 else 1.0


def build_staggered_dirac(gauge: GaugeField, mass: float) -> sparse.csr_matrix:
    geom = gauge.geom
    n = geom.volume * NC
    rows: list[int] = []
    cols: list[int] = []
    vals: list[complex] = []
    for site in range(geom.volume):
        coords = geom.site_coords(site)
        for color in range(NC):
            idx = site * NC + color
            rows.append(idx)
            cols.append(idx)
            vals.append(mass)
        for mu in range(NDIM):
            eta = staggered_eta(mu, coords)
            fwd = geom.shifted(coords, mu, +1)
            bwd = geom.shifted(coords, mu, -1)
            fwd_site = geom.site_index(fwd)
            bwd_site = geom.site_index(bwd)
            apbc_fwd = -1.0 if mu == 0 and coords[0] == geom.time_l - 1 else 1.0
            apbc_bwd = -1.0 if mu == 0 and coords[0] == 0 else 1.0
            u_fwd = gauge.u[coords][mu]
            u_bwd = gauge.u[bwd][mu]
            for a in range(NC):
                row = site * NC + a
                for b in range(NC):
                    rows.append(row)
                    cols.append(fwd_site * NC + b)
                    vals.append(apbc_fwd * 0.5 * eta * u_fwd[a, b])
                    rows.append(row)
                    cols.append(bwd_site * NC + b)
                    vals.append(-apbc_bwd * 0.5 * eta * np.conj(u_bwd[b, a]))
    return sparse.csr_matrix((vals, (rows, cols)), shape=(n, n), dtype=complex)


def solve_propagator_normal_eq(D: sparse.csr_matrix, source_index: int, rtol: float, maxiter: int) -> tuple[np.ndarray, int, float]:
    rhs = np.zeros(D.shape[0], dtype=complex)
    rhs[source_index] = 1.0
    dh = D.getH()
    normal = dh @ D
    b = dh @ rhs
    sol, info = cg(normal, b, rtol=rtol, atol=0.0, maxiter=maxiter)
    residual = float(np.linalg.norm(normal @ sol - b) / max(np.linalg.norm(b), 1.0e-30))
    return sol, int(info), residual


def measure_correlator(gauge: GaugeField, mass: float, rtol: float, maxiter: int) -> dict[str, Any]:
    D = build_staggered_dirac(gauge, mass)
    geom = gauge.geom
    corr = np.zeros(geom.time_l, dtype=float)
    infos: list[int] = []
    residuals: list[float] = []
    source_site = geom.site_index((0, 0, 0, 0))
    for source_color in range(NC):
        source_index = source_site * NC + source_color
        sol, info, residual = solve_propagator_normal_eq(D, source_index, rtol, maxiter)
        infos.append(info)
        residuals.append(residual)
        for site in range(geom.volume):
            t = geom.site_coords(site)[0]
            block = sol[site * NC:(site + 1) * NC]
            corr[t] += float(np.vdot(block, block).real)
    corr /= NC
    return {
        "mass": mass,
        "correlator": corr.tolist(),
        "cg_infos": infos,
        "cg_residuals": residuals,
        "max_cg_residual": max(residuals) if residuals else None,
    }


def jackknife_mean_err(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = values.shape[0]
    mean = np.mean(values, axis=0)
    if n <= 1:
        return mean, np.zeros_like(mean)
    jk = np.array([(np.sum(values, axis=0) - values[i]) / (n - 1) for i in range(n)])
    err = np.sqrt((n - 1) * np.mean((jk - np.mean(jk, axis=0)) ** 2, axis=0))
    return mean, err


def fit_mass(corr: np.ndarray, err: np.ndarray) -> dict[str, Any]:
    max_tau = max(2, len(corr) // 2)
    taus = np.arange(1, max_tau + 1)
    means = corr[1:max_tau + 1]
    sig = np.maximum(err[1:max_tau + 1], 1.0e-10)
    best: dict[str, Any] | None = None
    for tau_min in range(1, max(2, max_tau - 1)):
        tau_max = max_tau
        mask = (taus >= tau_min) & (means > 0.0)
        if int(np.sum(mask)) < 2:
            continue
        x = taus[mask].astype(float)
        y = np.log(means[mask])
        yerr = sig[mask] / means[mask]
        w = 1.0 / np.maximum(yerr * yerr, 1.0e-12)
        design = np.vstack([np.ones_like(x), -x]).T
        normal = design.T @ (w[:, None] * design)
        rhs = design.T @ (w * y)
        cov = np.linalg.pinv(normal)
        coeff = cov @ rhs
        residual = y - design @ coeff
        dof = max(1, len(y) - 2)
        chi2 = float(np.sum(w * residual * residual) / dof)
        candidate = {
            "tau_min": int(tau_min),
            "tau_max": int(tau_max),
            "m_lat": float(coeff[1]),
            "m_lat_err": float(math.sqrt(max(cov[1, 1], 0.0))),
            "chi2_dof": chi2,
        }
        if best is None or abs(candidate["chi2_dof"] - 1.0) < abs(best["chi2_dof"] - 1.0):
            best = candidate
    if best is None:
        return {"tau_min": 1, "tau_max": max_tau, "m_lat": float("nan"), "m_lat_err": float("nan"), "chi2_dof": float("nan")}
    return best


def effective_mass(corr: np.ndarray) -> list[dict[str, float]]:
    rows = []
    for tau in range(len(corr) - 1):
        if corr[tau] > 0.0 and corr[tau + 1] > 0.0:
            rows.append({"tau": tau, "m_eff": float(math.log(corr[tau] / corr[tau + 1]))})
    return rows


def physical_mass_gev(m_lat: float) -> float:
    a_inv = R0_OVER_A_BETA6_REFERENCE * HBARC_GEV_FM / R0_FM
    return m_lat * a_inv


def run_volume(args: argparse.Namespace, spatial_l: int, time_l: int, masses: list[float], rng: np.random.Generator) -> dict[str, Any]:
    geom = Geometry(spatial_l, time_l)
    gauge = GaugeField(geom)
    t0 = time.time()
    plaquette_history = []
    for sweep in range(args.therm):
        gauge.heatbath_sweep(rng)
        for _ in range(args.overrelax):
            gauge.overrelax_sweep()
        plaquette_history.append(gauge.plaquette())
        print(f"  therm L={spatial_l} sweep={sweep + 1}/{args.therm} plaquette={plaquette_history[-1]:.6f}")

    measurements: dict[float, list[list[float]]] = {m: [] for m in masses}
    cg_residuals: dict[float, list[float]] = {m: [] for m in masses}
    plaquettes = []
    for cfg in range(args.measurements):
        for _ in range(args.separation):
            gauge.heatbath_sweep(rng)
            for _ in range(args.overrelax):
                gauge.overrelax_sweep()
        plaquettes.append(gauge.plaquette())
        meas_gauge = ape_smear_spatial(gauge, args.ape_alpha, args.ape_steps) if args.ape_steps else gauge
        for mass in masses:
            measured = measure_correlator(meas_gauge, mass, args.cg_rtol, args.cg_maxiter)
            measurements[mass].append(measured["correlator"])
            cg_residuals[mass].append(float(measured["max_cg_residual"]))
        print(f"  meas L={spatial_l} cfg={cfg + 1}/{args.measurements} plaquette={plaquettes[-1]:.6f}")

    mass_scan = []
    selected_fit: dict[str, Any] | None = None
    selected_mass = masses[len(masses) // 2]
    correlator_rows = []
    for mass in masses:
        arr = np.asarray(measurements[mass], dtype=float)
        mean, err = jackknife_mean_err(arr)
        fit = fit_mass(mean, err)
        mass_scan.append(
            {
                "m_bare_lat": mass,
                "m_fit_lat": fit["m_lat"],
                "m_fit_lat_err": fit["m_lat_err"],
                "chi2_dof": fit["chi2_dof"],
                "max_cg_residual": max(cg_residuals[mass]) if cg_residuals[mass] else None,
            }
        )
        if mass == selected_mass:
            selected_fit = fit
            for tau, (c, e) in enumerate(zip(mean, err)):
                correlator_rows.append({"tau": tau, "mean": float(c), "stderr": float(e)})

    if selected_fit is None:
        selected_fit = mass_scan[len(mass_scan) // 2]

    elapsed = time.time() - t0
    return {
        "spatial_L": spatial_l,
        "time_L": time_l,
        "dims": [spatial_l, spatial_l, spatial_l, time_l],
        "a_fm": R0_FM / R0_OVER_A_BETA6_REFERENCE,
        "r0_over_a": R0_OVER_A_BETA6_REFERENCE,
        "boundary_conditions": {
            "gauge_spatial": "periodic",
            "gauge_time": "periodic",
            "fermion_time": "antiperiodic",
        },
        "update_algorithm": "Cabibbo-Marinari heatbath + polar overrelaxation",
        "thermalization_sweeps": args.therm,
        "measurement_sweeps": args.measurements,
        "measurement_separation_sweeps": args.separation,
        "ape_smearing": {"steps": args.ape_steps, "alpha": args.ape_alpha},
        "plaquette_history": [float(x) for x in plaquette_history],
        "plaquette_measurements": [float(x) for x in plaquettes],
        "plaquette_mean": float(np.mean(plaquettes)) if plaquettes else None,
        "mass_parameter_scan": mass_scan,
        "selected_mass_parameter": selected_mass,
        "correlators": correlator_rows,
        "effective_mass": effective_mass(np.array([r["mean"] for r in correlator_rows])),
        "mass_fit": selected_fit,
        "runtime_seconds": elapsed,
    }


def combine_results(ensembles: list[dict[str, Any]]) -> dict[str, Any]:
    masses = []
    mass_errs = []
    for ens in ensembles:
        fit = ens.get("mass_fit", {})
        if isinstance(fit, dict) and math.isfinite(float(fit.get("m_lat", float("nan")))):
            masses.append(float(fit["m_lat"]))
            mass_errs.append(float(fit.get("m_lat_err", 0.0)))
    if not masses:
        m_lat = float("nan")
        stat_lat = float("nan")
        fv_lat = float("nan")
    else:
        m_lat = float(np.mean(masses))
        stat_lat = float(math.sqrt(sum(e * e for e in mass_errs)) / max(len(mass_errs), 1))
        fv_lat = float(np.std(masses, ddof=1)) if len(masses) > 1 else 0.0
    m_running = physical_mass_gev(m_lat) if math.isfinite(m_lat) else float("nan")
    stat = physical_mass_gev(stat_lat) if math.isfinite(stat_lat) else float("nan")
    finite_volume = physical_mass_gev(fv_lat) if math.isfinite(fv_lat) else float("nan")
    # Reduced-run placeholders are deliberately conservative and large.
    finite_spacing = max(0.20 * abs(m_running), 0.0) if math.isfinite(m_running) else float("nan")
    scale_setting = max(0.05 * abs(m_running), 0.0) if math.isfinite(m_running) else float("nan")
    matching = max(0.10 * abs(m_running), 0.0) if math.isfinite(m_running) else float("nan")
    running_bridge = max(0.10 * abs(m_running), 0.0) if math.isfinite(m_running) else float("nan")
    heavy_mass_tuning = max(0.15 * abs(m_running), 0.0) if math.isfinite(m_running) else float("nan")
    components = {
        "statistical": stat,
        "heavy_mass_tuning": heavy_mass_tuning,
        "finite_volume": finite_volume,
        "finite_spacing": finite_spacing,
        "scale_setting": scale_setting,
        "matching": matching,
        "running_bridge": running_bridge,
        "v_input": 0.0001,
    }
    total_mt = math.sqrt(sum(v * v for v in components.values() if math.isfinite(v)))
    y_t = math.sqrt(2.0) * m_running / V_GEV if math.isfinite(m_running) else float("nan")
    y_components = {k: (math.sqrt(2.0) * v / V_GEV if math.isfinite(v) else None) for k, v in components.items()}
    total_y = math.sqrt(sum(v * v for v in y_components.values() if v is not None and math.isfinite(v)))
    return {
        "m_t_running_at_v_GeV": m_running,
        "y_t_v": y_t,
        "m_t_pole_GeV": m_running,
        "uncertainties": y_components,
        "mass_uncertainties_GeV": components,
        "total_y_t_uncertainty": total_y,
        "total_m_t_pole_uncertainty_GeV": total_mt,
        "reduced_scope_delta_to_pdg_GeV": m_running - PDG_TOP_MASS_GEV if math.isfinite(m_running) else None,
        "reduced_scope_delta_to_y_t_target": y_t - YT_TARGET if math.isfinite(y_t) else None,
    }


def parse_volume_spec(spec: str) -> list[tuple[int, int]]:
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "x" in part:
            l_s, l_t = part.lower().split("x", 1)
            out.append((int(l_s), int(l_t)))
        else:
            l_s = int(part)
            out.append((l_s, 2 * l_s))
    return out


def build_certificate(args: argparse.Namespace, ensembles: list[dict[str, Any]]) -> dict[str, Any]:
    result = combine_results(ensembles)
    ratio_y = result["y_t_v"]
    # This is not a measured g_s in reduced scope; the strict runner should reject it.
    ratio = None
    if isinstance(ratio_y, float) and math.isfinite(ratio_y):
        ratio = ratio_y / 1.0
    return {
        "metadata": {
            "authority": "staggered_top_correlator_mass_extraction",
            "phase": "production" if args.production_targets else "reduced_scope",
            "action": "Cl3Z3_SU3_Wilson_staggered",
            "g_bare": 1.0,
            "uses_prior_ward_chain": False,
            "uses_composite_matrix_element_route": False,
            "uses_coupling_definition_route": False,
            "scale_anchor": "Sommer r0 = 0.5 fm external anchor; r0/a reference used for reduced run",
            "running_bridge": "reduced run uses no authoritative SM RGE; production certificate must supply 4/5-loop bridge",
            "evidence_scope": "reduced run is infrastructure evidence only" if not args.production_targets else "user-requested production targets",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
        "v_input": {
            "source": "existing electroweak VEV chain",
            "treatment": "substrate_input_only",
            "v_GeV": V_GEV,
        },
        "ensembles": ensembles,
        "result": result,
        "ratio_check": {
            "y_t_lattice": ratio_y,
            "g_s_lattice": 1.0,
            "g_s_source": "not_measured_reduced_scope",
            "ratio": ratio,
            "uncertainty": result.get("total_y_t_uncertainty"),
            "used_as_definition": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--volumes", default=None, help="Comma-separated Ls x Lt list, e.g. 12x24,16x32,24x48.")
    parser.add_argument("--masses", default="0.45,0.75,1.05", help="Comma-separated staggered bare masses.")
    parser.add_argument("--therm", type=int, default=None, help="Thermalization sweeps.")
    parser.add_argument("--measurements", type=int, default=None, help="Saved configurations per volume.")
    parser.add_argument("--separation", type=int, default=None, help="Sweeps between saved configurations.")
    parser.add_argument("--overrelax", type=int, default=None, help="Overrelaxation sweeps after each heat-bath sweep.")
    parser.add_argument("--ape-steps", type=int, default=1, help="APE smearing steps for measurement links.")
    parser.add_argument("--ape-alpha", type=float, default=0.5, help="APE smearing alpha.")
    parser.add_argument("--cg-rtol", type=float, default=1.0e-8, help="CG relative residual target.")
    parser.add_argument("--cg-maxiter", type=int, default=2000, help="CG max iterations.")
    parser.add_argument("--seed", type=int, default=20260430, help="Random seed.")
    parser.add_argument("--output", type=Path, default=DEFAULT_CERTIFICATE, help="Certificate JSON output path.")
    parser.add_argument(
        "--production-targets",
        action="store_true",
        help="Mark the run as production-targeted. This does not override strict validation thresholds.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.production_targets:
        args.volumes = args.volumes or "12x24,16x32,24x48"
        args.therm = 1000 if args.therm is None else args.therm
        args.measurements = 1000 if args.measurements is None else args.measurements
        args.separation = 20 if args.separation is None else args.separation
        args.overrelax = 4 if args.overrelax is None else args.overrelax
    else:
        args.volumes = args.volumes or "2x4,3x6"
        args.therm = 2 if args.therm is None else args.therm
        args.measurements = 3 if args.measurements is None else args.measurements
        args.separation = 1 if args.separation is None else args.separation
        args.overrelax = 1 if args.overrelax is None else args.overrelax

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    volumes = parse_volume_spec(args.volumes)
    masses = [float(x) for x in args.masses.split(",") if x.strip()]
    rng = np.random.default_rng(args.seed)

    print("=" * 78)
    print("YT direct lattice correlator production harness")
    print("=" * 78)
    print(f"volumes={volumes}")
    print(f"masses={masses}")
    print(f"therm={args.therm}, measurements={args.measurements}, separation={args.separation}")
    print(f"output={args.output}")
    if not args.production_targets:
        print("scope=reduced; strict runner is expected to reject this certificate")

    ensembles = []
    for spatial_l, time_l in volumes:
        ensembles.append(run_volume(args, spatial_l, time_l, masses, rng))

    certificate = build_certificate(args, ensembles)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(certificate, f, indent=2, sort_keys=True)
        f.write("\n")
    stamped = OUTPUT_DIR / f"yt_direct_lattice_correlator_{int(time.time())}.json"
    with stamped.open("w", encoding="utf-8") as f:
        json.dump(certificate, f, indent=2, sort_keys=True)
        f.write("\n")

    result = certificate["result"]
    print("\nRESULT SUMMARY")
    print(f"  m_t proxy       = {result['m_t_pole_GeV']:.6f} GeV")
    print(f"  y_t proxy       = {result['y_t_v']:.8f}")
    print(f"  total dm_t      = {result['total_m_t_pole_uncertainty_GeV']:.6f} GeV")
    print(f"  total dy_t      = {result['total_y_t_uncertainty']:.8f}")
    print(f"  wrote           = {args.output}")
    print(f"  archive copy    = {stamped}")
    print("\nThis reduced certificate is not retained evidence unless the strict runner passes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
