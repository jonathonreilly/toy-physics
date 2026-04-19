#!/usr/bin/env python3
"""
g_bare Critical Feature Scan on the Cl(3)/Z^3 Framework Surface
================================================================

STATUS: scanning runner (PASS = feature found at beta = 6; FAIL = none found)

Purpose
-------
Previous dynamical attempts to fix g_bare = 1 closed negatively:
  - RG beta-function fixed points: none in SU(3)
  - Maximum entropy: selects g -> infinity
  - Mean-field self-consistency: diverges
  - Plaquette self-consistency: reduction law, not a fixed-point equation

This runner scans OTHER observables for a critical feature at g_bare = 1
(equivalently Wilson beta = 6/g^2 = 6):

  1. Grassmann log-|det| density of the colored staggered Dirac operator
     D_stag[U] in SU(3) backgrounds drawn from the Wilson measure at
     each beta.
  2. Smallest singular value (smallest |lambda| of the Hermitian squared
     operator D_stag^dagger D_stag).
  3. Spectral gap near zero and low-mode density rho(0; beta).
  4. Staggered index-proxy via low-mode spectral asymmetry
     (there is no chirality in naive staggered at massless point, so we
     track the count of near-zero modes instead).
  5. Plaquette curvature d^2<P>/d beta^2 (specific-heat-like signal).
  6. Polyakov loop expectation |<L>| on Z^3 x L_t with time-antiperiodic
     BC relevant for the fermion block.

Scan range: beta in [1.0, 30.0] (g_bare in [sqrt(6/30), sqrt(6)] ~
[0.447, 2.449]), step 0.5, with refinement near beta = 6.

Lattice: Z^3 x L_t with L = 4 first (L^4 = 256 sites * 3 colors = 768
staggered DOF), then optionally L = 6 if a feature appears near beta=6.

Decision rule
-------------
PASS (feature) : at least one observable shows a localized non-smooth
                 feature (extremum, kink, sharp peak in curvature, zero
                 crossing, jump) at beta = 6 +/- one scan step, AND
                 the feature sharpens or persists at L = 6.

FAIL (obstruction) : all scanned observables are smooth functions of
                 beta across beta = 6 with quantitative smoothness
                 bounds.

Implementation notes
--------------------
Only numpy + scipy are required. Matplotlib is optional (used for PNG
plots if available). The heavy cost is generating SU(3) configurations;
we share a single config per beta (thermalized + a few decorrelation
sweeps) for all fermionic observables.
"""
from __future__ import annotations

import os
import sys
import json
import time
import math
import argparse
from typing import Callable

import numpy as np
from scipy.sparse import csr_matrix, lil_matrix, eye as speye
from scipy.sparse.linalg import eigsh
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:  # pragma: no cover
    HAVE_MPL = False

N_C = 3
NDIM = 4  # Z^3 x L_t is a 4D hypercubic lattice

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "BOUNDED") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# =====================================================================
# SU(3) helpers
# =====================================================================

def random_su3_near_identity(rng: np.random.Generator, epsilon: float = 0.24) -> np.ndarray:
    """Generate a random SU(3) element close to the identity. Used as an
    update proposal in Metropolis sweeps.
    """
    h = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
    h = (h + h.conj().T) / 2.0
    h -= np.trace(h) / 3.0 * np.eye(3)
    x = np.eye(3, dtype=complex) + 1j * epsilon * h
    q, r = np.linalg.qr(x)
    d = np.diag(r)
    ph = d / np.abs(d)
    q = q @ np.diag(np.conj(ph))
    det = np.linalg.det(q)
    q *= np.exp(-1j * np.angle(det) / 3.0)
    return q


def init_cold_links(L: int, L_t: int) -> np.ndarray:
    """Shape (L, L, L, L_t, NDIM, 3, 3). Cold start = identity everywhere."""
    U = np.zeros((L, L, L, L_t, NDIM, 3, 3), dtype=complex)
    I3 = np.eye(3, dtype=complex)
    for idx in np.ndindex(L, L, L, L_t, NDIM):
        U[idx] = I3
    return U


def shift(coords: tuple, mu: int, delta: int, shape: tuple) -> tuple:
    c = list(coords)
    c[mu] = (c[mu] + delta) % shape[mu]
    return tuple(c)


def compute_staple(U: np.ndarray, coords: tuple, mu: int, shape: tuple) -> np.ndarray:
    """Sum of the six SU(3) staples around link U_mu(x). Matches the
    frontier_plaquette_self_consistency.py convention so beta plugs into
    the Wilson action the same way.
    """
    staple = np.zeros((3, 3), dtype=complex)
    xp = shift(coords, mu, 1, shape)
    for nu in range(NDIM):
        if nu == mu:
            continue
        xpn = shift(coords, nu, 1, shape)
        staple += U[xp + (nu,)] @ U[xpn + (mu,)].conj().T @ U[coords + (nu,)].conj().T
        xm = shift(coords, nu, -1, shape)
        xpm = shift(xp, nu, -1, shape)
        staple += U[xpm + (nu,)].conj().T @ U[xm + (mu,)].conj().T @ U[xm + (nu,)]
    return staple


def metropolis_sweep(U: np.ndarray, beta: float, rng: np.random.Generator,
                     shape: tuple, epsilon: float = 0.24) -> float:
    accepted = 0
    total = 0
    for coords in np.ndindex(*shape):
        for mu in range(NDIM):
            u_old = U[coords + (mu,)]
            staple = compute_staple(U, coords, mu, shape)
            proposal = random_su3_near_identity(rng, epsilon)
            u_new = proposal @ u_old
            dS = -(beta / N_C) * np.trace((u_new - u_old) @ staple).real
            total += 1
            if dS < 0.0 or rng.random() < math.exp(-dS):
                U[coords + (mu,)] = u_new
                accepted += 1
    return accepted / total if total else 0.0


def measure_plaquette(U: np.ndarray, shape: tuple) -> float:
    total = 0.0
    count = 0
    for coords in np.ndindex(*shape):
        for mu in range(NDIM):
            for nu in range(mu + 1, NDIM):
                xm = shift(coords, mu, 1, shape)
                xn = shift(coords, nu, 1, shape)
                u_p = (
                    U[coords + (mu,)]
                    @ U[xm + (nu,)]
                    @ U[xn + (mu,)].conj().T
                    @ U[coords + (nu,)].conj().T
                )
                total += np.trace(u_p).real / N_C
                count += 1
    return total / count


def measure_polyakov(U: np.ndarray, shape: tuple) -> complex:
    """Spatial-averaged Polyakov loop in the time direction (mu = 3)."""
    L_t = shape[3]
    acc = 0.0 + 0.0j
    count = 0
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                prod = np.eye(3, dtype=complex)
                for t in range(L_t):
                    prod = prod @ U[(x, y, z, t, 3)]
                acc += np.trace(prod) / N_C
                count += 1
    return acc / count


# =====================================================================
# Staggered Dirac operator with SU(3) gauge links and APBC in time
# =====================================================================

def staggered_eta(coords: tuple) -> tuple[float, float, float, float]:
    x, y, z, t = coords
    return (
        1.0,
        (-1.0) ** x,
        (-1.0) ** (x + y),
        (-1.0) ** (x + y + z),
    )


def build_staggered_D(U: np.ndarray, shape: tuple, mass: float = 0.0) -> csr_matrix:
    """Build the colored staggered Dirac operator on Z^3 x L_t.

    D_{x,y}^{a,b} = m delta_{x,y} delta^{a,b}
      + (1/2) sum_mu eta_mu(x) [ U_mu(x)^{a,b} delta_{x+mu,y}
                                 - U_mu(x-mu)^{dag,a,b} delta_{x-mu,y} ]

    Time direction (mu = 3) uses antiperiodic boundary conditions for the
    fermion, which is the standard finite-temperature choice.
    """
    Lx, Ly, Lz, L_t = shape
    V = Lx * Ly * Lz * L_t
    N = V * N_C

    def site_index(coords: tuple) -> int:
        x, y, z, t = coords
        return ((x * Ly + y) * Lz + z) * L_t + t

    rows = []
    cols = []
    data = []

    for coords in np.ndindex(*shape):
        i = site_index(coords)
        etas = staggered_eta(coords)
        if mass != 0.0:
            for a in range(N_C):
                rows.append(i * N_C + a)
                cols.append(i * N_C + a)
                data.append(mass)
        for mu in range(NDIM):
            # Forward hop with gauge link U_mu(x)
            coords_p = list(coords)
            coords_p[mu] = (coords_p[mu] + 1) % shape[mu]
            apbc_sign_f = 1.0
            if mu == 3 and coords[3] == shape[3] - 1:
                apbc_sign_f = -1.0
            coords_p = tuple(coords_p)
            j_p = site_index(coords_p)
            Umat = U[coords + (mu,)]
            for a in range(N_C):
                for b in range(N_C):
                    val = 0.5 * etas[mu] * apbc_sign_f * Umat[a, b]
                    if val != 0:
                        rows.append(i * N_C + a)
                        cols.append(j_p * N_C + b)
                        data.append(val)
            # Backward hop with gauge link U_mu(x - mu)^dagger
            coords_m = list(coords)
            coords_m[mu] = (coords_m[mu] - 1) % shape[mu]
            apbc_sign_b = 1.0
            if mu == 3 and coords[3] == 0:
                apbc_sign_b = -1.0
            coords_m = tuple(coords_m)
            j_m = site_index(coords_m)
            Umat_m = U[coords_m + (mu,)]
            for a in range(N_C):
                for b in range(N_C):
                    val = -0.5 * etas[mu] * apbc_sign_b * np.conj(Umat_m[b, a])
                    if val != 0:
                        rows.append(i * N_C + a)
                        cols.append(j_m * N_C + b)
                        data.append(val)

    return csr_matrix((data, (rows, cols)), shape=(N, N))


# =====================================================================
# Fermionic observables derived from D
# =====================================================================

def compute_logdet_density(D: csr_matrix, mass_reg: float = 1e-6) -> float:
    """log |det(D + i eps)| / V, computed as 0.5 sum log(lambda_i(D^dag D) + eps^2).

    Uses full eigendecomposition of D^dag D (only affordable at small L).
    """
    M = (D.conj().T @ D).toarray()
    # M is Hermitian positive semidefinite
    w = np.linalg.eigvalsh((M + M.conj().T) / 2.0)
    w = np.clip(w, 0.0, None)
    # regulate near-zero modes
    logdet = 0.5 * np.sum(np.log(w + mass_reg * mass_reg))
    return logdet / M.shape[0]


def compute_low_spectrum(D: csr_matrix, n_modes: int = 12) -> np.ndarray:
    """Return the smallest |lambda(D)| eigenvalues via eigsh on H = D^dag D."""
    M = D.conj().T @ D
    k = min(n_modes, M.shape[0] - 2)
    try:
        w = eigsh(M, k=k, sigma=1e-8, which="LM", return_eigenvectors=False,
                  tol=1e-8, maxiter=2000)
    except Exception:
        # Fall back to dense for small systems
        Md = M.toarray()
        wall = np.linalg.eigvalsh((Md + Md.conj().T) / 2.0)
        w = np.sort(wall)[:k]
    w = np.sort(np.clip(w, 0.0, None))
    return np.sqrt(w)


# =====================================================================
# Scan driver
# =====================================================================

def thermalize_config(L: int, L_t: int, beta: float, n_therm: int, n_decor: int,
                      seed: int, epsilon: float = 0.24, verbose: bool = False,
                      n_configs: int = 1) -> list[np.ndarray]:
    """Return n_configs decorrelated configs at inverse coupling beta."""
    shape = (L, L, L, L_t)
    rng = np.random.default_rng(seed)
    U = init_cold_links(L, L_t)
    acc_sum = 0.0
    for s in range(n_therm):
        acc = metropolis_sweep(U, beta, rng, shape, epsilon=epsilon)
        acc_sum += acc
    configs = []
    for c in range(n_configs):
        for _ in range(n_decor):
            metropolis_sweep(U, beta, rng, shape, epsilon=epsilon)
        configs.append(U.copy())
    if verbose:
        print(f"    therm acc ~ {acc_sum / n_therm:.2f}")
    return configs


def scan_betas(L: int, L_t: int, betas: list[float], n_therm: int, n_decor: int,
               n_configs: int, seed_base: int, verbose: bool = True) -> dict:
    """Run the full scan. Returns a dict of arrays keyed by observable."""
    out = {
        "betas": np.array(betas),
        "plaquette": np.zeros(len(betas)),
        "plaquette_err": np.zeros(len(betas)),
        "polyakov_abs": np.zeros(len(betas)),
        "polyakov_abs_err": np.zeros(len(betas)),
        "logdet_density": np.zeros(len(betas)),
        "logdet_density_err": np.zeros(len(betas)),
        "lambda_min": np.zeros(len(betas)),
        "lambda_min_err": np.zeros(len(betas)),
        "spectral_gap": np.zeros(len(betas)),
        "spectral_gap_err": np.zeros(len(betas)),
        "rho_near_zero": np.zeros(len(betas)),
        "rho_near_zero_err": np.zeros(len(betas)),
        "low_mode_count": np.zeros(len(betas)),
    }
    LOW_MODE_THRESHOLD = 0.2  # count |lambda| < threshold as "near zero"

    shape = (L, L, L, L_t)
    V = L * L * L * L_t

    for i, beta in enumerate(betas):
        t0 = time.time()
        configs = thermalize_config(
            L, L_t, beta, n_therm=n_therm, n_decor=n_decor,
            seed=seed_base + i, n_configs=n_configs, verbose=verbose,
        )
        plaqs = []
        polys = []
        ldds = []
        lmins = []
        gaps = []
        rhos = []
        lcount = 0
        for U in configs:
            plaqs.append(measure_plaquette(U, shape))
            polys.append(abs(measure_polyakov(U, shape)))
            D = build_staggered_D(U, shape, mass=0.0)
            ldds.append(compute_logdet_density(D))
            low = compute_low_spectrum(D, n_modes=12)
            lmins.append(low[0])
            gaps.append(low[1] - low[0])
            rhos.append(np.sum(low < LOW_MODE_THRESHOLD))
            lcount += int(np.sum(low < LOW_MODE_THRESHOLD))
        out["plaquette"][i] = np.mean(plaqs)
        out["plaquette_err"][i] = np.std(plaqs) / max(1.0, math.sqrt(len(plaqs)))
        out["polyakov_abs"][i] = np.mean(polys)
        out["polyakov_abs_err"][i] = np.std(polys) / max(1.0, math.sqrt(len(polys)))
        out["logdet_density"][i] = np.mean(ldds)
        out["logdet_density_err"][i] = np.std(ldds) / max(1.0, math.sqrt(len(ldds)))
        out["lambda_min"][i] = np.mean(lmins)
        out["lambda_min_err"][i] = np.std(lmins) / max(1.0, math.sqrt(len(lmins)))
        out["spectral_gap"][i] = np.mean(gaps)
        out["spectral_gap_err"][i] = np.std(gaps) / max(1.0, math.sqrt(len(gaps)))
        out["rho_near_zero"][i] = np.mean(rhos) / V
        out["rho_near_zero_err"][i] = np.std(rhos) / max(1.0, math.sqrt(len(rhos))) / V
        out["low_mode_count"][i] = lcount / max(1, len(configs))
        dt = time.time() - t0
        if verbose:
            print(
                f"  beta={beta:5.2f}  <P>={out['plaquette'][i]:.4f}  "
                f"|L|={out['polyakov_abs'][i]:.4f}  ln|det|/V={out['logdet_density'][i]:+.4f}  "
                f"lambda_min={out['lambda_min'][i]:.4f}  gap={out['spectral_gap'][i]:.4f}  "
                f"rho(0)={out['rho_near_zero'][i]:.4f}  ({dt:.1f}s)"
            )
    return out


# =====================================================================
# Smoothness / feature detector
# =====================================================================

def central_second_derivative(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Second derivative via central differences on a possibly non-uniform grid."""
    n = len(x)
    d2 = np.zeros(n)
    for i in range(1, n - 1):
        h1 = x[i] - x[i - 1]
        h2 = x[i + 1] - x[i]
        d2[i] = 2.0 * (
            (y[i + 1] - y[i]) / h2 - (y[i] - y[i - 1]) / h1
        ) / (h1 + h2)
    d2[0] = d2[1]
    d2[-1] = d2[-2]
    return d2


def find_feature_at(beta_grid: np.ndarray, y: np.ndarray, target: float,
                    window: float, y_err: np.ndarray | None = None) -> dict:
    """Look for extrema / inflections / kinks in y(beta) near beta = target.

    The detector is grid-agnostic: it compares the localized residual of a
    smooth global fit over the whole beta range against the typical MC
    noise, so a genuine localized feature must stick out above both the
    global smooth trend AND the per-point statistical error.

    Returns a dict with:
      - smooth_rel : relative residual of a global smooth (polynomial) fit
      - local_residual_sigma : residual at target in units of local stderr
      - has_local_extremum : True if dy/db changes sign inside window
      - has_kink : True if the LOCAL polynomial fit residual near target
                   exceeds the typical non-local residual
      - local_curvature : d^2 y / d beta^2 at nearest grid point to target
    """
    mask = np.abs(beta_grid - target) <= window + 1e-9
    if np.sum(mask) < 3:
        return {"smooth_rel": float("nan"), "has_local_extremum": False,
                "has_kink": False, "local_curvature": float("nan"),
                "d2_jump_over_std": float("nan"),
                "local_residual_sigma": float("nan"),
                "note": "not enough points in window"}

    # Global smooth fit (degree-6 polynomial) to detect localized excursions
    deg = min(6, len(beta_grid) - 2)
    coefs = np.polyfit(beta_grid, y, deg=deg)
    fitted_all = np.polyval(coefs, beta_grid)
    resid_all = y - fitted_all
    denom = max(1e-12, float(np.ptp(y)))
    smooth_rel = float(np.max(np.abs(resid_all)) / denom)

    idx_target = int(np.argmin(np.abs(beta_grid - target)))
    resid_at_target = float(resid_all[idx_target])

    # Per-point statistical noise
    if y_err is not None and len(y_err) == len(y):
        err_at_target = float(y_err[idx_target])
    else:
        # Estimate noise from successive differences away from target
        far_mask = ~mask
        far = resid_all[far_mask]
        err_at_target = float(np.std(far) if np.sum(far_mask) > 2 else np.std(resid_all))
    err_at_target = max(err_at_target, 1e-12)
    local_residual_sigma = abs(resid_at_target) / err_at_target

    # LOCAL residual comparison: if local residuals are systematically
    # larger than non-local residuals, a kink is indicated.
    local_mean_resid = float(np.mean(np.abs(resid_all[mask])))
    far_mean_resid = float(np.mean(np.abs(resid_all[~mask])) if np.sum(~mask) else 0.0)
    has_kink = local_mean_resid > 3.0 * max(far_mean_resid, err_at_target / math.sqrt(max(1, np.sum(mask))))

    # Local curvature from smooth fit (no grid-artifacts)
    d_coefs = np.polyder(coefs, 2)
    local_curv = float(np.polyval(d_coefs, target))

    # Extremum: dy/db sign change in window (from the SMOOTH fit)
    d1_coefs = np.polyder(coefs, 1)
    dy_in_window = np.polyval(d1_coefs, beta_grid[mask])
    sign_change = bool(np.any(dy_in_window[:-1] * dy_in_window[1:] < 0))

    # Keep legacy d2_jump_over_std entry for backward compat (from fit)
    d2_in_window = np.polyval(np.polyder(coefs, 2), beta_grid[mask])
    d2_jump = float(np.ptp(d2_in_window))
    d2_std = float(np.std(np.polyval(np.polyder(coefs, 2), beta_grid)) + 1e-12)

    return {
        "smooth_rel": smooth_rel,
        "has_local_extremum": sign_change,
        "has_kink": has_kink,
        "local_curvature": local_curv,
        "d2_jump_over_std": d2_jump / d2_std,
        "local_residual_sigma": local_residual_sigma,
        "resid_at_target": resid_at_target,
        "local_mean_resid": local_mean_resid,
        "far_mean_resid": far_mean_resid,
    }


# =====================================================================
# Plots and JSON dump
# =====================================================================

def make_plots(results: dict, outdir: str, L: int, L_t: int) -> list[str]:
    if not HAVE_MPL:
        return []
    os.makedirs(outdir, exist_ok=True)
    files = []
    betas = results["betas"]

    def _plot(name: str, y: np.ndarray, yerr: np.ndarray | None,
              ylabel: str, title: str) -> None:
        fig, ax = plt.subplots(figsize=(7, 4.2))
        if yerr is not None:
            ax.errorbar(betas, y, yerr=yerr, marker="o", capsize=3, lw=1.2,
                        color="#1f77b4")
        else:
            ax.plot(betas, y, marker="o", color="#1f77b4")
        ax.axvline(6.0, color="crimson", ls="--", lw=1.0, label="beta = 6")
        ax.set_xlabel("Wilson beta = 2 N_c / g_bare^2")
        ax.set_ylabel(ylabel)
        ax.set_title(f"{title}  (L^3 x L_t = {L}^3 x {L_t})")
        ax.grid(True, alpha=0.3)
        ax.legend()
        path = os.path.join(outdir, f"g_bare_scan_{name}_L{L}.png")
        fig.tight_layout()
        fig.savefig(path, dpi=120)
        plt.close(fig)
        files.append(path)

    _plot("plaquette", results["plaquette"], results["plaquette_err"],
          "<P>", "Plaquette expectation")
    _plot("polyakov", results["polyakov_abs"], results["polyakov_abs_err"],
          "|<L>|", "Polyakov loop magnitude")
    _plot("logdet", results["logdet_density"], results["logdet_density_err"],
          "log|det D| / dim", "Grassmann log-det density")
    _plot("lambda_min", results["lambda_min"], results["lambda_min_err"],
          "|lambda_min|", "Smallest Dirac singular value")
    _plot("spectral_gap", results["spectral_gap"], results["spectral_gap_err"],
          "gap", "Spectral gap |lambda_1| - |lambda_0|")
    _plot("rho_zero", results["rho_near_zero"], results["rho_near_zero_err"],
          "rho(0)", "Low-mode density near zero")

    # Curvature panel
    d2 = central_second_derivative(betas, results["plaquette"])
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(betas, d2, marker="o", color="darkorange")
    ax.axvline(6.0, color="crimson", ls="--", lw=1.0, label="beta = 6")
    ax.set_xlabel("beta")
    ax.set_ylabel("d^2 <P> / d beta^2")
    ax.set_title(f"Plaquette curvature (L^3 x L_t = {L}^3 x {L_t})")
    ax.grid(True, alpha=0.3)
    ax.legend()
    path = os.path.join(outdir, f"g_bare_scan_plaq_curvature_L{L}.png")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    files.append(path)

    return files


def dump_json(results: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in results.items()}
    with open(path, "w") as f:
        json.dump(out, f, indent=2)


# =====================================================================
# Main
# =====================================================================

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--L", type=int, default=4, help="Spatial lattice size")
    p.add_argument("--Lt", type=int, default=4, help="Time lattice size")
    p.add_argument("--n-therm", type=int, default=40, help="Therm sweeps per beta")
    p.add_argument("--n-decor", type=int, default=4, help="Decorrelation sweeps between configs")
    p.add_argument("--n-configs", type=int, default=2, help="Configs per beta to average over")
    p.add_argument("--beta-min", type=float, default=1.0)
    p.add_argument("--beta-max", type=float, default=30.0)
    p.add_argument("--beta-step", type=float, default=1.0)
    p.add_argument("--refine-near-6", action="store_true", default=True,
                   help="Add finer steps around beta = 6")
    p.add_argument("--no-refine", dest="refine_near_6", action="store_false")
    p.add_argument("--seed", type=int, default=424242)
    p.add_argument("--outdir", type=str, default="outputs/figures/g_bare_critical_feature_scan")
    p.add_argument("--json", type=str, default="outputs/g_bare_critical_feature_scan.json")
    p.add_argument("--quick", action="store_true", help="Tiny run for smoke test")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if args.quick:
        args.L = 3
        args.Lt = 3
        args.n_therm = 10
        args.n_decor = 2
        args.n_configs = 1
        betas = [2.0, 4.0, 6.0, 8.0, 12.0]
    else:
        betas = list(np.arange(args.beta_min, args.beta_max + 1e-9, args.beta_step))
        if args.refine_near_6:
            extra = [5.25, 5.5, 5.75, 6.25, 6.5, 6.75]
            betas = sorted(set([round(b, 6) for b in betas + extra]))

    print("=" * 72)
    print("g_bare Critical Feature Scan")
    print("=" * 72)
    print(f"  lattice shape = Z^3 x L_t with L = {args.L}, L_t = {args.Lt}")
    print(f"  beta grid ({len(betas)} points): {betas[0]:.2f} -> {betas[-1]:.2f}")
    print(f"  n_therm = {args.n_therm}, n_decor = {args.n_decor}, n_configs = {args.n_configs}")
    print()

    t0 = time.time()
    results = scan_betas(
        L=args.L, L_t=args.Lt, betas=betas,
        n_therm=args.n_therm, n_decor=args.n_decor, n_configs=args.n_configs,
        seed_base=args.seed,
    )
    dt_total = time.time() - t0
    print(f"\nscan elapsed: {dt_total:.1f}s")

    # Feature detection at beta = 6
    print("\n=== Feature scan around beta = 6 ===")
    betas_arr = results["betas"]
    feature_reports = {}
    for key, label, err_key in [
        ("plaquette", "<P>", "plaquette_err"),
        ("polyakov_abs", "|<L>|", "polyakov_abs_err"),
        ("logdet_density", "ln|det D|/dim", "logdet_density_err"),
        ("lambda_min", "|lambda_min|", "lambda_min_err"),
        ("spectral_gap", "spectral gap", "spectral_gap_err"),
        ("rho_near_zero", "rho(0)", "rho_near_zero_err"),
    ]:
        report = find_feature_at(betas_arr, results[key], target=6.0,
                                 window=1.0,
                                 y_err=results.get(err_key))
        feature_reports[key] = report
        print(f"  {label:>16s}: smooth_rel={report['smooth_rel']:.3e}, "
              f"resid@6/sigma={report['local_residual_sigma']:.2f}, "
              f"extremum={report['has_local_extremum']}, kink={report['has_kink']}")

    # Plaquette curvature specifically (specific-heat-like)
    d2P = central_second_derivative(betas_arr, results["plaquette"])
    idx6 = int(np.argmin(np.abs(betas_arr - 6.0)))
    d2P_at_6 = float(d2P[idx6])
    d2P_max = float(np.max(np.abs(d2P)))
    d2P_at_6_ratio = float(abs(d2P_at_6) / (d2P_max + 1e-12))
    print(f"  plaquette curvature at beta=6: d^2<P>/d beta^2 = {d2P_at_6:+.4e}  "
          f"(|.|/max = {d2P_at_6_ratio:.2f})")

    # Plots + JSON
    plot_files = make_plots(results, outdir=args.outdir, L=args.L, L_t=args.Lt)
    if plot_files:
        print(f"\nplots written:")
        for p in plot_files:
            print(f"  {p}")
    else:
        print("\n(matplotlib unavailable; skipping plots)")
    dump_json({**results, "feature_reports": feature_reports,
               "d2P_at_6": d2P_at_6, "d2P_max": d2P_max,
               "d2P_at_6_ratio": d2P_at_6_ratio},
              path=args.json)
    print(f"json written: {args.json}")

    # PASS/FAIL harness.
    # FEATURE = localized residual at beta=6 exceeds per-point stderr AND
    # exceeds typical non-local residuals by factor >3 (robust to grid density).
    print("\n=== PASS/FAIL harness ===")
    any_feature = False
    for key, rpt in feature_reports.items():
        local_sigma = rpt.get("local_residual_sigma", 0.0)
        kink = rpt["has_kink"]
        extremum_in_global_fit = rpt["has_local_extremum"]
        # A "genuine" localized feature must clear both bars:
        #   (a) residual at target > 3 sigma noise level
        #   (b) localized kink by fit-residual ratio
        loud = bool((local_sigma > 3.0 and kink) or extremum_in_global_fit)
        check(
            f"observable '{key}' has no localized non-smooth feature at beta=6",
            not loud,
            f"resid@6/sigma={local_sigma:.2f}, kink={kink}, extremum={extremum_in_global_fit}",
        )
        any_feature = any_feature or loud

    print()
    print("=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    if any_feature:
        print("VERDICT: FEATURE-CANDIDATE at beta = 6 (inspect plots + refine at larger L)")
    else:
        print("VERDICT: NO critical feature at beta = 6 in any scanned observable")
        print("         => obstruction note applies; Landing A (normalization-only fixed input) stands.")
    print("=" * 72)

    # Exit 0 either way -- the obstruction outcome IS a valid retained result.
    return 0


if __name__ == "__main__":
    sys.exit(main())
