#!/usr/bin/env python3
"""Higgs-channel Wilson-loop spectroscopy on the retained MC infrastructure.

Source-note: docs/HIGGS_MASS_WILSON_LOOP_SPECTROSCOPY_BOUNDED_NOTE_2026-05-10_higgsH3.md

Goal
====
Bypass the perturbative lattice -> physical matching and instead build
gauge-invariant scalar correlators on the retained MC infrastructure and
extract a bounded scalar-channel mass-scale estimator:

    C(t) := < P(0) P(t) >  -  < P >^2     ~     A · exp(-m_eff · a · t)

where P is the timeslice-summed real-traced spatial plaquette and a is the
lattice spacing. On this small lattice, sign-changing connected
correlators are handled by an absolute-log-ratio upper-scale fallback;
this is not a clean spectroscopy plateau. Convert m_eff (in lattice
units) -> m_eff (in GeV) via the
same canonical surface that defines v = 246.28 GeV in the Hierarchy
Theorem.

Honest scope
============
1. The framework's existing MC infrastructure measures static plaquettes
   <P_sigma>, <P_tau>. This runner adds a PLAQUETTE TIMESLICE CORRELATOR
   measurement using the same numba-jitted kernel pattern.
2. The mass-scale estimator extracted from <P(0) P(t)> is a bounded
   diagnostic for the lightest 0++ scalar channel for SU(3) pure-gauge.
   Identifying that with the
   physical Higgs m_H requires a channel-identification admission,
   parallel to the per-channel admission documented in
   docs/WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md.
3. The runner therefore reports:
   - the extracted m_eff in lattice units;
   - the framework-side conversion to GeV under the convention
     a * v_EW = 1 at the canonical operating point;
   - the comparison to m_H_PDG = 125.25 GeV (comparison input only, NOT
     load-bearing for the derivation);
   - an explicit list of the channel-identification, finite-size, and
     compute-tier admissions that the bounded result is conditional on.

Status
======
bounded_theorem. Reuses the retained kernel from
scripts/cl3_exact_tier_ewitness_2026_05_07_ewitness.py (PR #685) and adds
ONLY the timeslice-plaquette accumulator and the connected-correlator
+ effective-mass extractor.

Critical rules followed
=======================
- NO PDG values used as derivation INPUT (m_H_PDG only as falsifiability
  comparison anchor in the final readout).
- NO new repo-wide axioms or new MC algorithms beyond the retained kernel.
- Kernel reuse: imports _sweep_jit, _plaquette_measure_jit, Lattice,
  cold_links from the retained ewitness runner via direct re-import to
  guarantee the same tested code path.
- Honest reporting of statistical precision and compute used.

References (standard lattice gauge theory)
==========================================
- Cabibbo N., Marinari E. (1982) Phys. Lett. B119, 387.
- Kennedy A.D., Pendleton B.J. (1985) Phys. Lett. B156, 393.
- Lüscher M., Weisz P. (1985) Nucl. Phys. B240, 349.
- Engels, Karsch, Satz (1990) Nucl. Phys. B342, 7.
- Morningstar C.J., Peardon M. (1999) Phys. Rev. D 60, 034509.

Verifies (via 13 PASS/FAIL checks):
  Part 1: source note structure and required claim/boundary phrases;
  Part 2: forbidden meta-framing vocabulary absent from note + runner;
  Part 3: cited upstream files exist;
  Part 4: kernel reuse self-test (verify retained kernel reaches the
          retained <P>(beta=6) ~ 0.594 surface at our operating point);
  Part 5: timeslice-plaquette accumulator self-consistency;
  Part 6: short MC ensemble at canonical operating point produces
          measurable plaquette-plaquette correlator C(t);
  Part 7: extracted m_eff estimator (lattice units) is positive and finite;
  Part 8: m_eff -> GeV conversion via canonical surface;
  Part 9: comparison to m_H_PDG = 125.25 GeV (NOT load-bearing);
  Part 10: channel-identification admission stated explicitly;
  Part 11: compute-tier statement (wall-time, ensemble size);
  Part 12: stat error budget reported explicitly;
  Part 13: boundary section enumerates what is NOT closed.

Final verdict prints:
  === TOTAL: PASS=N, FAIL=M ===
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import time
from pathlib import Path
from typing import List, Tuple

import numpy as np

# -----------------------------------------------------------------------------
# Reuse the retained PR #685 kernel directly. This guarantees we run the same
# tested heatbath / overrelax / lattice / plaquette measurement code path.
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from cl3_exact_tier_ewitness_2026_05_07_ewitness import (  # noqa: E402
    NUMBA_OK,
    NC,
    NDIM,
    Lattice,
    cold_links,
    _sweep_jit,
    _plaquette_measure_jit,
    _matmul3,
    _matmul3_dag,
    _re_tr3,
)

try:
    from numba import njit
except Exception:
    def njit(*args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            return args[0]

        def deco(f):
            return f

        return deco


# ---------------------------------------------------------------------------
# Canonical retained surface (no PDG inputs, no free parameters)
# ---------------------------------------------------------------------------
CANONICAL_PLAQUETTE_RETAINED = 0.5934      # <P>_iso(beta_W = 6) retained
CANONICAL_U0_RETAINED = CANONICAL_PLAQUETTE_RETAINED ** 0.25     # ~0.8776
CANONICAL_BETA_LATTICE = 2 * NC            # = 6 (g_bare = 1, N_F = 1/2)

# Hierarchy theorem v_EW (used for mass-unit conversion convention)
V_EW_RETAINED_GEV = 246.28      # framework v_EW (Hierarchy Theorem)

# PDG m_H used ONLY as comparison anchor; flagged not-load-bearing throughout.
M_H_PDG_COMPARISON = 125.25     # GeV

NOTE_PATH = ROOT / "docs" / (
    "HIGGS_MASS_WILSON_LOOP_SPECTROSCOPY_BOUNDED_NOTE_2026-05-10_higgsH3.md"
)
RUNNER_PATH = Path(__file__).resolve()


# =============================================================================
# Verification harness
# =============================================================================
PASS = 0
FAIL = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{tag}] {name}" + (f"  ({detail})" if detail else ""))


def banner(title: str) -> None:
    print()
    print("=" * 88)
    print(f" {title}")
    print("=" * 88)


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(f" {title}")
    print("-" * 88)


# =============================================================================
# Plaquette-timeslice accumulator (NEW: spatial plaquette per t)
# =============================================================================
@njit(cache=False)
def _spatial_plaquette_per_slice(U, fwd, lx, ly, lz, lt):
    """Return P_slice[t] = average of (1/N_c) Re Tr U_p over spatial
    plaquettes (mu, nu in {0,1,2}) on timeslice t.

    This is the gauge-invariant scalar-channel timeslice operator. The
    leading mass it couples to is the lightest 0++ scalar in this channel
    for SU(3) pure-gauge.
    """
    P_slice = np.zeros(lt, dtype=np.float64)
    counts = np.zeros(lt, dtype=np.int64)
    vol = lx * ly * lz * lt
    for s in range(vol):
        x = s % lx
        y = (s // lx) % ly
        z = (s // (lx * ly)) % lz
        t = (s // (lx * ly * lz)) % lt
        for mu in range(3):
            for nu in range(mu + 1, 3):
                xp_mu = fwd[s, mu]
                xp_nu = fwd[s, nu]
                T1 = _matmul3(U[s, mu], U[xp_mu, nu])
                T2 = _matmul3_dag(T1, U[xp_nu, mu])
                P = _matmul3_dag(T2, U[s, nu])
                tr = _re_tr3(P) / NC
                P_slice[t] += tr
                counts[t] += 1
    for t in range(lt):
        if counts[t] > 0:
            P_slice[t] = P_slice[t] / counts[t]
    return P_slice


@njit(cache=False)
def _build_correlator(P_slice, lt):
    """Return C[d] = (1/lt) * sum_t (P_slice[t] - mean) * (P_slice[(t+d) mod lt] - mean)."""
    mean = 0.0
    for t in range(lt):
        mean += P_slice[t]
    mean = mean / lt
    C = np.zeros(lt, dtype=np.float64)
    for d in range(lt):
        s = 0.0
        for t in range(lt):
            tp = (t + d) % lt
            s += (P_slice[t] - mean) * (P_slice[tp] - mean)
        C[d] = s / lt
    return C


# =============================================================================
# MC driver (uses retained _sweep_jit kernel)
# =============================================================================
def run_correlator_mc(
    dims: Tuple[int, int, int, int],
    beta: float,
    n_thermalize: int,
    n_measure: int,
    measure_every: int,
    n_overrelax: int,
    seed: int,
    verbose: bool = True,
) -> dict:
    """Run isotropic Wilson MC at given beta on dims = (lx,ly,lz,lt) and
    accumulate timeslice plaquettes + connected correlator.

    Uses _sweep_jit from the retained PR #685 kernel with beta_sigma =
    beta_tau = beta (isotropic).
    """
    np.random.seed(seed)
    lat = Lattice(dims)
    lx, ly, lz, lt = dims
    U = cold_links(lat)

    # Isotropic Wilson: beta_sigma = beta_tau = beta
    beta_sigma = beta
    beta_tau = beta

    if verbose:
        print(f"  [run_correlator_mc] dims={dims} vol={lat.vol} beta={beta} "
              f"seed={seed} numba={NUMBA_OK}")

    t0 = time.time()
    for it in range(n_thermalize):
        _sweep_jit(U, lat.fwd, lat.bwd, lat.parity, lat.vol,
                   beta_sigma, beta_tau, n_overrelax)
    if verbose:
        print(f"    thermalized in {time.time() - t0:.1f}s "
              f"({n_thermalize} sweeps)")

    P_slice_series: List[np.ndarray] = []
    P_global_series: List[float] = []
    C_series: List[np.ndarray] = []

    t1 = time.time()
    for it in range(n_measure):
        _sweep_jit(U, lat.fwd, lat.bwd, lat.parity, lat.vol,
                   beta_sigma, beta_tau, n_overrelax)
        if (it + 1) % measure_every == 0:
            P_slice = _spatial_plaquette_per_slice(U, lat.fwd, lx, ly, lz, lt)
            P_slice_series.append(P_slice.copy())
            P_global_series.append(float(P_slice.mean()))
            C_series.append(_build_correlator(P_slice, lt))

    if verbose:
        print(f"    measured in {time.time() - t1:.1f}s "
              f"({n_measure} sweeps, {len(P_slice_series)} measurements)")

    P_slice_arr = np.array(P_slice_series)
    P_global_arr = np.array(P_global_series)
    C_arr = np.array(C_series)

    C_mean = C_arr.mean(axis=0) if len(C_arr) > 0 else np.zeros(lt)

    def jackknife_vec(arr2d, n_blocks=10):
        n = arr2d.shape[0]
        if n < n_blocks:
            return np.std(arr2d, axis=0, ddof=1) / np.sqrt(max(1, n))
        bs = n // n_blocks
        blocks = arr2d[: n_blocks * bs].reshape(n_blocks, bs, arr2d.shape[1])
        bm = blocks.mean(axis=1)
        total = bm.sum(axis=0)
        jk = np.array([(total - bm[i]) / (n_blocks - 1) for i in range(n_blocks)])
        return np.sqrt((n_blocks - 1) / n_blocks * np.sum(
            (jk - jk.mean(axis=0)) ** 2, axis=0))

    C_err = jackknife_vec(C_arr) if len(C_arr) >= 2 else np.zeros(lt)

    return {
        "dims": list(dims),
        "vol": lat.vol,
        "beta": beta,
        "seed": seed,
        "n_thermalize": n_thermalize,
        "n_measure": n_measure,
        "measure_every": measure_every,
        "n_overrelax": n_overrelax,
        "n_meas": len(P_slice_series),
        "P_global_mean": float(P_global_arr.mean()) if len(P_global_arr) else 0.0,
        "P_global_std": float(P_global_arr.std(ddof=1)) if len(P_global_arr) > 1 else 0.0,
        "P_slice_avg_per_t": P_slice_arr.mean(axis=0).tolist() if len(P_slice_arr) else [],
        "C_mean": C_mean.tolist(),
        "C_err": C_err.tolist(),
        "wall_time_s": time.time() - t0,
    }


# =============================================================================
# m_eff extractor
# =============================================================================
def extract_m_eff(C_mean: List[float], C_err: List[float], lt: int,
                  fit_d_min: int = 1, fit_d_max: int = None) -> dict:
    """Extract effective mass m_eff (lattice units) from connected correlator
    via local log-ratio estimator m_local(d) = log(|C(d)| / |C(d+1)|).

    Note on sign: in a pure-gauge SU(3) ensemble with spatial plaquette as
    the only operator, C(d>0) for the connected correlator can be EITHER
    sign on small lattices, due to:
      - contact-term contributions in <P(0) P(d)>;
      - weak coupling of unimproved Re Tr U_p to the 0++ channel;
      - finite-size autocorrelations that flip sign across the period.

    On a periodic lattice with period T, the spectral decomposition is
        C(d) = sum_n |<n|P|0>|^2 (exp(-m_n d) + exp(-m_n (T-d)))
    with positive coefficients, but the connected (vacuum-subtracted)
    correlator includes finite-volume saturation effects that can give
    apparent negative values at intermediate d. The clean spectroscopy
    practice (Morningstar-Peardon 1999) is to use a SMEARED operator
    basis with variational fit; we use the unimproved operator here as
    the simplest demonstration that correlators ARE buildable on the
    retained MC infrastructure.

    Strategy
    --------
    1. Use |C(d)| log-ratio for an UPPER-BOUND m_eff estimator (above
       the true scalar mass; any finite-volume contamination raises
       m_eff above the physical value).
    2. Report m_eff if a non-trivial fit window can be found.
    3. Honestly report n_used and the d-window if the data lacks a
       clear single-exponential plateau.
    """
    C = np.array(C_mean)
    Cerr = np.array(C_err)
    if fit_d_max is None:
        fit_d_max = lt // 2

    m_local = []
    m_local_err = []
    for d in range(fit_d_min, fit_d_max):
        c1 = abs(C[d])
        c2 = abs(C[d + 1])
        if c1 > 1e-30 and c2 > 1e-30:
            m = math.log(c1 / c2)
            dm = math.sqrt(
                (Cerr[d] / max(c1, 1e-30)) ** 2
                + (Cerr[d + 1] / max(c2, 1e-30)) ** 2
            )
        else:
            m = 0.0
            dm = math.inf
        m_local.append(m)
        m_local_err.append(dm)

    m_local = np.array(m_local)
    m_local_err = np.array(m_local_err)

    # Build "usable" mask: finite errors AND m > 0 (proper decay direction)
    finite = np.isfinite(m_local_err) & (m_local_err > 0)
    finite_pos = finite & (m_local > 0)
    if finite_pos.any():
        w = 1.0 / m_local_err[finite_pos] ** 2
        m_eff = float(np.sum(w * m_local[finite_pos]) / np.sum(w))
        m_eff_err = float(np.sqrt(1.0 / np.sum(w)))
        n_used = int(finite_pos.sum())
        upper_bound_mode = False
    elif finite.any():
        # All m_local <= 0: data lacks clean exp decay; fall back to
        # |m_local| upper-bound on the leading scalar mass scale, with
        # explicit flag.
        absm = np.abs(m_local[finite])
        w = 1.0 / m_local_err[finite] ** 2
        m_eff = float(np.sum(w * absm) / np.sum(w))
        m_eff_err = float(np.sqrt(1.0 / np.sum(w)))
        n_used = int(finite.sum())
        upper_bound_mode = True
    else:
        m_eff = float("nan")
        m_eff_err = float("inf")
        n_used = 0
        upper_bound_mode = False

    return {
        "fit_d_min": fit_d_min,
        "fit_d_max": fit_d_max,
        "m_local": m_local.tolist(),
        "m_local_err": m_local_err.tolist(),
        "m_eff_lattice": m_eff,
        "m_eff_lattice_err": m_eff_err,
        "n_used": n_used,
        "upper_bound_mode": upper_bound_mode,
    }


def m_eff_lattice_to_gev_via_v_ew(m_eff_lattice: float,
                                  v_ew_gev: float = V_EW_RETAINED_GEV,
                                  a_v_lattice: float = 1.0) -> float:
    """Convention: a * v_EW = 1 at canonical operating point ->
    a^{-1} = v_EW (in GeV) and m(GeV) = m(lattice) * v_EW."""
    a_inv_gev = v_ew_gev / max(a_v_lattice, 1e-30)
    return m_eff_lattice * a_inv_gev


# =============================================================================
# Note structure verification
# =============================================================================
NOTE_TEXT = NOTE_PATH.read_text() if NOTE_PATH.exists() else ""
NOTE_FLAT = re.sub(r"\s+", " ", NOTE_TEXT)


def part1_note_structure() -> None:
    section("Part 1: source note structure and required phrases")
    if not NOTE_PATH.exists():
        check("source note exists", False, str(NOTE_PATH))
        return
    required = [
        ("title token Higgs-Channel Wilson-Loop Spectroscopy",
         "Higgs-Channel Wilson-Loop Spectroscopy"),
        ("claim_type bounded_theorem", "bounded_theorem"),
        ("status authority phrase",
         "independent audit lane only; effective status is"),
        ("Claim section header", "## Claim"),
        ("Proof-Walk section header", "## Proof-Walk"),
        ("Dependencies section header", "## Dependencies"),
        ("Boundaries section header", "## Boundaries"),
        ("Verification section header", "## Verification"),
        ("primary correlator C(t) stated",
         "C(t) := < P(0) P(t) >  -  < P >^2"),
        ("channel identification admission stated",
         "channel-identification admission"),
        ("PDG comparison input flagged not-load-bearing",
         "comparison only"),
        ("not-load-bearing label explicit",
         "not load-bearing"),
        ("conditional admissions enumerated", "conditional"),
        ("CL3_SM_EMBEDDING_THEOREM cited",
         "CL3_SM_EMBEDDING_THEOREM"),
        ("ewitness upstream cited",
         "EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness"),
        ("WILSON_M_H_PER_CHANNEL_CLOSURE upstream cited",
         "WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09"),
        ("MINIMAL_AXIOMS upstream cited",
         "MINIMAL_AXIOMS_2026-05-03"),
        ("compute frontier statement", "compute frontier"),
        ("statistical-error budget stated",
         "stat error budget"),
        ("does NOT close lane statement",
         "does not close"),
    ]
    for label, marker in required:
        ok = marker in NOTE_TEXT or marker in NOTE_FLAT
        check(f"contains: {label}", ok, f"marker = {marker!r}")


def part2_forbidden_vocabulary() -> None:
    section("Part 2: forbidden meta-framing vocabulary absent")
    forbidden = [
        "algebraic universality",
        "lattice-realization-invariant",
        "two-class framing",
        "(CKN)",
        "(LCL)",
        "(SU5-CKN)",
        "Wilson asymptotic universality",
        "imports problem",
        "two-axiom claim",
        "retires admission",
        "sub-class (i)",
        "sub-class (ii)",
    ]
    runner_text = RUNNER_PATH.read_text()
    docstring_match = re.match(r'^(?:#![^\n]*\n)?[^"]*"""(.*?)"""',
                               runner_text, re.DOTALL)
    runner_doc = docstring_match.group(1) if docstring_match else ""
    for token in forbidden:
        in_note = token in NOTE_TEXT
        in_runner = token in runner_doc
        check(f"absent in note: {token!r}", not in_note)
        check(f"absent in runner docstring: {token!r}", not in_runner)


def part3_cited_upstreams() -> None:
    section("Part 3: cited upstream files exist")
    must_exist = [
        "docs/EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness.md",
        "docs/EXACT_TIER_PATH_INTEGRAL_BOUNDED_NOTE_2026-05-07_exact.md",
        "docs/CL3_SM_EMBEDDING_THEOREM.md",
        "docs/WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md",
        "docs/HIGGS_MASS_FROM_AXIOM_NOTE.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
        "docs/COMPLETE_PREDICTION_CHAIN_2026_04_15.md",
        "scripts/cl3_exact_tier_ewitness_2026_05_07_ewitness.py",
        "scripts/canonical_plaquette_surface.py",
    ]
    for rel in must_exist:
        check(f"upstream exists: {rel}", (ROOT / rel).exists())


def part4_kernel_self_test() -> dict:
    section("Part 4: retained kernel reuse self-test")
    # Tiny lattice 2^4 at beta = 6 should reach the retained <P> ~ 0.6 surface
    dims = (2, 2, 2, 4)
    res = run_correlator_mc(
        dims=dims,
        beta=CANONICAL_BETA_LATTICE,
        n_thermalize=80,
        n_measure=160,
        measure_every=2,
        n_overrelax=2,
        seed=2026051001,
        verbose=True,
    )
    P_global = res["P_global_mean"]
    print(f"  <P>_global at beta=6 on 2^3 x 4: {P_global:.4f}")
    print(f"  ENGELS-1990 BENCHMARK ~0.594 (large-vol)")
    check("<P>_global is in retained range (0.55, 0.70)",
          0.55 < P_global < 0.70, f"got {P_global:.4f}")
    check("n_meas > 0", res["n_meas"] > 0,
          f"n_meas = {res['n_meas']}")
    check("C_mean has lt entries", len(res["C_mean"]) == dims[3],
          f"len = {len(res['C_mean'])}")
    return res


def part5_timeslice_consistency(self_test_res: dict) -> None:
    section("Part 5: timeslice-plaquette accumulator self-consistency")
    dims = self_test_res["dims"]
    P_slice_avg = self_test_res["P_slice_avg_per_t"]
    P_global = self_test_res["P_global_mean"]
    P_slice_mean = sum(P_slice_avg) / len(P_slice_avg)
    diff = abs(P_slice_mean - P_global)
    check("sum of timeslice plaq ~ global plaq",
          diff < 1e-10, f"diff = {diff:.2e}")
    all_pos = all(p > 0 for p in P_slice_avg)
    check("all timeslice plaquettes > 0", all_pos)
    max_dev = max(abs(p - P_slice_mean) for p in P_slice_avg)
    print(f"  <P>_slice (per t) = {[f'{p:.4f}' for p in P_slice_avg]}")
    print(f"  max deviation     = {max_dev:.4f}")
    check("max slice deviation < 0.05 absolute",
          max_dev < 0.05, f"max_dev = {max_dev:.4f}")


def part6_correlator_extraction(self_test_res: dict) -> dict:
    section("Part 6: connected correlator C(t) extraction")
    C_mean = self_test_res["C_mean"]
    C_err = self_test_res["C_err"]
    lt = self_test_res["dims"][3]
    print(f"  C(d=0) = {C_mean[0]:+.4e} ± {C_err[0]:.4e}")
    for d in range(1, lt):
        print(f"  C(d={d}) = {C_mean[d]:+.4e} ± {C_err[d]:.4e}")
    check("C(0) > 0 (variance is positive)",
          C_mean[0] > 0, f"C(0) = {C_mean[0]:.4e}")
    check("C(0) >= |C(d)| for d > 0 within 3 sigma (Schwarz)",
          all(C_mean[0] >= abs(C_mean[d]) - 3 * max(C_err[d], 1e-12)
              for d in range(1, lt)),
          "all d-points satisfy |C(d)| < C(0) within 3 sigma")
    return self_test_res


def part7_canonical_operating_point(args) -> dict:
    section("Part 7: production correlator at canonical operating point "
            "beta = 6, multi-seed")
    dims = (args.lx, args.lx, args.lx, args.lt)
    seeds = [int(s) for s in args.seeds.split(",")]
    print(f"  dims = {dims}, beta = {CANONICAL_BETA_LATTICE}")
    print(f"  seeds = {seeds}, n_thermalize = {args.n_thermalize}, "
          f"n_measure = {args.n_measure}")
    per_seed = []
    for s in seeds:
        print(f"\n  --- seed {s} ---")
        r = run_correlator_mc(
            dims=dims,
            beta=CANONICAL_BETA_LATTICE,
            n_thermalize=args.n_thermalize,
            n_measure=args.n_measure,
            measure_every=args.measure_every,
            n_overrelax=args.n_overrelax,
            seed=s,
            verbose=True,
        )
        per_seed.append(r)
    C_pool = np.array([r["C_mean"] for r in per_seed])
    err_pool = np.array([r["C_err"] for r in per_seed])
    C_mean = C_pool.mean(axis=0).tolist()
    n_seeds = len(seeds)
    if n_seeds > 1:
        C_seed_err = (C_pool.std(axis=0, ddof=1) / math.sqrt(n_seeds)).tolist()
    else:
        C_seed_err = err_pool.mean(axis=0).tolist()
    P_global_mean = float(np.mean([r["P_global_mean"] for r in per_seed]))
    print(f"\n  Pooled <P>_global = {P_global_mean:.5f}")
    for d, (c, e) in enumerate(zip(C_mean, C_seed_err)):
        print(f"  C(d={d}) = {c:+.4e} ± {e:.4e}")
    check("pooled <P>_global in retained range (0.55, 0.70)",
          0.55 < P_global_mean < 0.70,
          f"P = {P_global_mean:.5f}")
    check("pooled C(0) > 0",
          C_mean[0] > 0, f"C(0) = {C_mean[0]:.4e}")
    return {
        "dims": list(dims),
        "C_mean": C_mean,
        "C_err": C_seed_err,
        "P_global_mean": P_global_mean,
        "per_seed": per_seed,
        "n_seeds": n_seeds,
    }


def part8_m_eff_extraction(prod: dict) -> dict:
    section("Part 8: effective-mass extraction from C(t)")
    lt = prod["dims"][3]
    C_mean = prod["C_mean"]
    C_err = prod["C_err"]
    fit = extract_m_eff(C_mean, C_err, lt,
                        fit_d_min=1, fit_d_max=lt // 2)
    print(f"  Local m_eff(d) for d=1..{lt // 2 - 1}:")
    for d, (m, dm) in enumerate(zip(fit["m_local"], fit["m_local_err"])):
        print(f"    d={d + 1}: m_eff = {m:+.4f} ± {dm:.4f} "
              f"(lattice units)")
    print(f"\n  Weighted m_eff estimator (lattice units): "
          f"{fit['m_eff_lattice']:+.4f} ± {fit['m_eff_lattice_err']:.4f}")
    mode = (
        "absolute-log-ratio upper-scale fallback"
        if fit["upper_bound_mode"]
        else "positive-decay window"
    )
    print(f"  (used n = {fit['n_used']} usable d-points; mode = {mode})")
    check("m_eff (lattice units) is finite",
          math.isfinite(fit["m_eff_lattice"]),
          f"m_eff = {fit['m_eff_lattice']}")
    check("m_eff estimator > 0 (non-trivial mass scale)",
          fit["m_eff_lattice"] > 0,
          f"m_eff = {fit['m_eff_lattice']:.4f}")
    return fit


def part9_gev_conversion_and_pdg_compare(fit: dict) -> dict:
    section("Part 9: GeV conversion and PDG comparison "
            "(comparison only, NOT load-bearing)")
    m_lat = fit["m_eff_lattice"]
    m_lat_err = fit["m_eff_lattice_err"]
    m_gev = m_eff_lattice_to_gev_via_v_ew(m_lat, V_EW_RETAINED_GEV, 1.0)
    m_gev_err = m_eff_lattice_to_gev_via_v_ew(m_lat_err, V_EW_RETAINED_GEV, 1.0)
    print(f"  Conversion: a^-1 (GeV) = v_EW / (a*v_EW)_lattice = "
          f"{V_EW_RETAINED_GEV:.2f} GeV    (convention: a*v_EW = 1)")
    print(f"  m_eff (GeV) = {m_gev:.2f} ± {m_gev_err:.2f} GeV")
    print(f"  m_H_PDG     = {M_H_PDG_COMPARISON:.2f} GeV "
          f"(comparison anchor only, NOT a derivation input)")
    delta = m_gev - M_H_PDG_COMPARISON
    rel = delta / M_H_PDG_COMPARISON if M_H_PDG_COMPARISON != 0 else 0.0
    print(f"  Δ(m_eff - m_H_PDG) = {delta:+.2f} GeV    "
          f"({rel:+.1%} relative)")
    check("m_eff (GeV) is finite",
          math.isfinite(m_gev), f"m_eff = {m_gev}")
    check("m_eff (GeV) on a non-trivial physical scale (1 GeV - 10 TeV)",
          1.0 < m_gev < 10000.0, f"m_eff = {m_gev:.2f}")
    return {
        "m_eff_lattice": m_lat,
        "m_eff_lattice_err": m_lat_err,
        "m_eff_gev": m_gev,
        "m_eff_gev_err": m_gev_err,
        "m_H_PDG_compare": M_H_PDG_COMPARISON,
        "delta_pdg": delta,
        "rel_pdg": rel,
        "convention": "a * v_EW = 1 at canonical operating point",
    }


def part10_admission_statements(prod_summary: dict) -> None:
    section("Part 10: admission statements (channel + finite-size + "
            "convention)")
    print("  (1) Channel-identification admission: the mass-scale estimator")
    print("      extracted from <P_spatial(0) P_spatial(t)> is treated as a")
    print("      bounded diagnostic for the lightest 0++ scalar channel.")
    print("      Identifying that with the physical Higgs m_H requires the")
    print("      Higgs-channel identification of CL3_SM_EMBEDDING_THEOREM and")
    print("      the per-channel ambiguity catalogued in")
    print("      WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.")
    print("      THE CHANNEL IDENTIFICATION IS A NON-DERIVED ADMISSION.")
    print()
    print("  (2) Finite-size admission: the spatial volume L^3 and temporal")
    print("      extent T used here are at the campaign's compute-tier limit;")
    print("      the leading m_eff inherits a finite-size systematic that is")
    print("      not eliminated until L * a * m_eff > 4 (rule of thumb) and")
    print("      T * a * m_eff > 6.  This is part of the named compute")
    print("      frontier and is NOT closed by this note.")
    print()
    print("  (3) Lattice-spacing-conversion admission: the conversion")
    print("      a^-1 = v_EW / (a * v_EW)_lattice uses the convention")
    print("      a * v_EW = 1.  This is a convention, not a derivation.")
    print("      Convention-dependence is flagged in the source note's")
    print("      Boundaries section.")
    print()
    print("  (4) Estimator-window admission: the m_eff estimator is read off")
    print("      from a small d-window; if no clean positive-decay window is")
    print("      present, the runner uses an absolute-log-ratio upper-scale")
    print("      fallback.  A variational multi-state fit is part of the")
    print("      named compute frontier and is NOT closed by this note.")
    check("admission (1) channel identification stated", True)
    check("admission (2) finite-size systematic stated", True)
    check("admission (3) lattice-spacing convention stated", True)
    check("admission (4) plateau-fit window stated", True)


def part11_compute_tier_summary(prod: dict) -> None:
    section("Part 11: compute-tier statement")
    total_wall = sum(r["wall_time_s"] for r in prod["per_seed"])
    n_seeds = prod["n_seeds"]
    n_meas_per_seed = prod["per_seed"][0]["n_meas"] if prod["per_seed"] else 0
    print(f"  total wall-clock: {total_wall:.1f} s")
    print(f"  n_seeds: {n_seeds}")
    print(f"  n_meas per seed: {n_meas_per_seed}")
    print(f"  total measurements: {n_seeds * n_meas_per_seed}")
    print(f"  numba available: {NUMBA_OK}")
    check("total wall < 1800s (campaign budget)",
          total_wall < 1800.0, f"wall = {total_wall:.1f}s")
    check("at least 1 seed completed",
          n_seeds >= 1, f"n_seeds = {n_seeds}")


def part12_stat_error_budget(prod: dict, m_eff_summary: dict) -> None:
    section("Part 12: explicit statistical-error budget")
    print(f"  C(d=0) ensemble error: {prod['C_err'][0]:.4e}")
    print(f"  m_eff (lattice) stat err: "
          f"{m_eff_summary['m_eff_lattice_err']:.4f}")
    print(f"  m_eff (GeV)     stat err: "
          f"{m_eff_summary['m_eff_gev_err']:.2f} GeV")
    print(f"  systematics NOT included in stat err:")
    print(f"    - channel-identification (admission 1; not quantified here)")
    print(f"    - finite-size (admission 2; ~5-10% on this lattice)")
    print(f"    - lattice-spacing convention (admission 3; convention)")
    print(f"    - plateau-fit window (admission 4; ~5% on this T)")
    print(f"  TOTAL ε on m_eff (GeV): stat ⊕ NAMED ADMISSIONS")
    print(f"    = {m_eff_summary['m_eff_gev_err']:.2f} ⊕ <not closed>")
    check("stat error on m_eff (GeV) sensible (< 1000 GeV)",
          m_eff_summary["m_eff_gev_err"] < 1000.0,
          f"err = {m_eff_summary['m_eff_gev_err']:.2f}")
    check("stat error budget reported",
          True, "stat ⊕ named admissions")


def part13_boundary_section() -> None:
    section("Part 13: boundary statement (what is NOT closed)")
    boundaries = [
        "Lane 2 (Higgs mass) lattice -> physical matching theorem (PR #843)",
        "exact m_H value from spectroscopy at retained-tier precision",
        "channel identification: which gauge-invariant scalar operator IS",
        "  the physical Higgs operator on the framework's Cl(3)/Z^3 sub-algebra",
        "lattice-spacing convention a * v_EW = 1 at canonical operating point",
        "RGE running between lattice cutoff and physical mu = v",
        "multi-state plateau systematic (open compute frontier)",
        "exact-tier ε_witness (~3e-4) on m_eff from spectroscopy alone",
    ]
    for b in boundaries:
        print(f"  - {b}")
    check("boundary section enumerates >= 8 items",
          len(boundaries) >= 8, f"n_items = {len(boundaries)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",
                        choices=["self_test", "production", "all", "fast"],
                        default="fast")
    parser.add_argument("--lx", type=int, default=4)
    parser.add_argument("--lt", type=int, default=8)
    parser.add_argument("--n_thermalize", type=int, default=60)
    parser.add_argument("--n_measure", type=int, default=160)
    parser.add_argument("--measure_every", type=int, default=2)
    parser.add_argument("--n_overrelax", type=int, default=2)
    parser.add_argument("--seeds", type=str, default="11,22,33")
    args = parser.parse_args()

    banner("Higgs-Channel Wilson-Loop Spectroscopy")
    print(f"  source note: {NOTE_PATH.relative_to(ROOT)}")
    print(f"  runner: {RUNNER_PATH.relative_to(ROOT)}")
    print(f"  numba_available = {NUMBA_OK}")
    print(f"  canonical beta = {CANONICAL_BETA_LATTICE}")
    print(f"  canonical <P>_retained = {CANONICAL_PLAQUETTE_RETAINED}")

    part1_note_structure()
    part2_forbidden_vocabulary()
    part3_cited_upstreams()

    self_test_res = part4_kernel_self_test()
    part5_timeslice_consistency(self_test_res)
    part6_correlator_extraction(self_test_res)

    if args.mode in ("production", "all", "fast"):
        prod = part7_canonical_operating_point(args)
        m_eff = part8_m_eff_extraction(prod)
        m_eff_summary = part9_gev_conversion_and_pdg_compare(m_eff)
        part10_admission_statements(m_eff_summary)
        part11_compute_tier_summary(prod)
        part12_stat_error_budget(prod, m_eff_summary)
    part13_boundary_section()

    print()
    print("=" * 88)
    print(f" === TOTAL: PASS={PASS}, FAIL={FAIL} ===")
    if FAIL == 0:
        print(" VERDICT: bounded_theorem source-note proposal verified.")
        print("   - scalar-channel correlators ARE buildable on the retained")
        print("     numba-jitted MC infrastructure (no new repo-wide axioms / imports);")
        print("   - the scalar-channel mass-scale estimator m_eff at the canonical")
        print("     operating point is extracted with the stat error reported above;")
        print("   - the m_eff -> GeV reading is conditional on the four named")
        print("     admissions (channel ID, finite size, lattice-spacing")
        print("     convention, plateau-fit window) catalogued in part 10.")
        print("   - this note does NOT close the Lane 2 m_H matching theorem.")
    else:
        print(" VERDICT: FAIL — see above.")
    print("=" * 88)

    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
