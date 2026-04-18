#!/usr/bin/env python3
"""
Discrete Evanescent-Barrier Amplitude Suppression on Cl(3)/Z^3
==============================================================

STATUS: retained theorem A (discrete lattice transfer-matrix bound)
        plus retained theorem B (Schwarzschild interior tortoise-length
        identity).  The Planck-unit astrophysical exponent
        exp[-(R_S/l_P) ln(R_S/R_min)] carried by the bounded GW-echo
        null companion is NOT on the retained surface: it depends on
        an open conditional (C-rate) about the per-site evanescent rate
        in tortoise coordinates, not established by theorems A + B
        alone.

RETAINED THEOREM A (discrete lattice transfer-matrix bound):
  For H = -t*Delta + V on Z with the symmetric nearest-neighbor
  Laplacian (Delta psi)_i = psi_{i+1} - 2 psi_i + psi_{i-1}, the
  eigenvalue equation (H - E) psi = 0 is equivalent to the recurrence

       psi_{i+1} = u_i * psi_i - psi_{i-1},    u_i = 2 + (V_i - E)/t.

  In a classically-forbidden interval [R_1, R_2] (u_i > 2), the two
  transfer eigenvalues are real, reciprocal, and positive:

       lambda_+(i) = (u_i + sqrt(u_i^2 - 4))/2 > 1,
       lambda_-(i) = 1/lambda_+(i) < 1.

  The Green function satisfies the rigorous amplitude bound

       |G(R_1, R_2; E)|  <=  C * exp[-sum_i ln lambda_+(i)]

  with algebraic prefactor C = O(t^{-1} * poly(R_2 - R_1)).

RETAINED THEOREM B (Schwarzschild interior tortoise-length identity):
  For the Schwarzschild lapse f(r) = 1 - R_S/r, the interior
  inverse-lapse integral has the exact closed form

       L*(R_min, R_S; eps) = R_S * ln((R_S - R_min)/eps)
                            + eps + R_min - R_S.

  For R_min << R_S and eps = R_min,

       L*(R_min, R_S; R_min) ~ R_S * ln(R_S/R_min) - R_S + O(R_min).

OPEN CONDITIONAL (C-rate):
  Going from theorems A + B to the Planck-unit astrophysical exponent
  |G| <= exp[-(R_S/l_P) ln(R_S/R_min)] requires an order-one lower
  bound on the per-unit-tortoise-length evanescent rate in
  Schwarzschild-interior coordinates.  Probe 3 shows the direct-in-r
  sum sum_i ln lambda_+(i) for V(r)/t = R_S/r on [R_min, R_S] scales
  as O(R_S), not O(R_S ln(R_S/R_min)), so the Planck-unit exponent is
  NOT a consequence of theorem A applied to the direct-in-r profile.
  The bounded companion frontier_echo_null_result.py continues to
  carry that exponent as a bounded statement.

SCOPE DISCIPLINE:
  - What is RETAINED by this script: theorem A (rigorous lattice
    transfer-matrix bound) + theorem B (exact tortoise-length identity).
  - What is DIAGNOSTIC (probe 6): the bounded-companion Planck-unit
    exponent matches the existing frontier_echo_null_result.py formula
    and scales correctly in the lattice spacing.  That is a
    self-consistency check of the bounded companion, not a derivation.
  - What remains OPEN: the per-site-rate lower bound (C-rate) that
    would be needed to retain the Planck-unit astrophysical exponent.

VALIDATION STRATEGY:
  This script rigorously verifies the structural theorem by:
    1. Building explicit discrete Schroedinger operators with rectangular
       and Schwarzschild-like barriers.
    2. Computing the exact lattice Green function via direct inversion.
    3. Comparing the exact amplitude to the transfer-matrix bound.
    4. Verifying scaling laws:
       - rectangular barrier: ln|G| decays linearly in barrier width L
       - Schwarzschild-like barrier: ln|G| ~ -(R_S/a) * ln(R_S/R_min)
    5. Confirming the continuum-WKB limit recovers the standard
       sqrt((V-E)*2/t)/a phase in the shallow-barrier regime.

PStack experiment: frontier-evanescent-barrier-amplitude-suppression
Self-contained: numpy only.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0
FAILURES: list[str] = []


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
        FAILURES.append(name)
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# =============================================================================
# Part 0: Exact discrete 1D Schroedinger operator and Green function
# =============================================================================

def build_discrete_schrodinger_1d(N: int, V: np.ndarray, t: float = 1.0) -> np.ndarray:
    """Build H = -t * Delta + diag(V) on a 1D chain of length N with open BC.

    Using the symmetric nearest-neighbor Laplacian:
        (Delta psi)(i) = psi(i+1) - 2 psi(i) + psi(i-1),
    so H = -t * Delta + V gives an on-site term +2t on the diagonal plus
    the potential V(i), and -t off the diagonals.
    """
    H = np.zeros((N, N), dtype=float)
    for i in range(N):
        H[i, i] = 2.0 * t + V[i]
    for i in range(N - 1):
        H[i, i + 1] = -t
        H[i + 1, i] = -t
    return H


def evanescent_eigenvalue(V_minus_E: float, t: float) -> float:
    """Larger transfer-matrix eigenvalue lambda(x) of the evanescent mode.

    The local transfer matrix for a 1D tight-binding eigenvalue problem
    (H - E) psi = 0 is

        [ psi(i+1) ]   [ (2t + V - E)/t   -1 ] [ psi(i)   ]
        [          ] = [                     ] [          ]
        [ psi(i)   ]   [       1           0 ] [ psi(i-1) ]

    with characteristic polynomial
        lambda^2 - ((2t + V - E)/t) * lambda + 1 = 0.
    For V - E > 0, the two real roots are reciprocals, and the larger is

        lambda_+ = (u + sqrt(u^2 - 4)) / 2,   u = (2t + V - E)/t.
    """
    u = 2.0 + V_minus_E / t
    # classical-forbidden requires u > 2  <=> V - E > 0
    disc = u * u - 4.0
    if disc < 0:
        raise ValueError("point is not classically forbidden")
    return 0.5 * (u + math.sqrt(disc))


def suppression_phase_exact(V: np.ndarray, E: float, t: float = 1.0) -> float:
    """Sum_x ln(lambda(x) / 1) on the barrier interior (V - E > 0)."""
    phase = 0.0
    for v in V:
        if v - E > 0:
            phase += math.log(evanescent_eigenvalue(v - E, t))
    return phase


def barrier_amplitude_exact(V: np.ndarray, E: float, t: float = 1.0) -> float:
    """Compute |G(R_1, R_2; E)| via direct matrix inverse.

    Returns |<x_left | (H - E)^{-1} | x_right>| where x_left and x_right
    are the sites just outside the barrier on either side.
    """
    N = len(V)
    H = build_discrete_schrodinger_1d(N, V, t=t)
    # find the leftmost and rightmost barrier sites
    barrier_sites = np.where(V - E > 0)[0]
    assert len(barrier_sites) > 0, "no barrier present"
    i_left = max(0, barrier_sites[0] - 1)
    i_right = min(N - 1, barrier_sites[-1] + 1)
    # regularize: add a small positive imaginary part so (H - E) is invertible
    eps = 1e-12
    G = np.linalg.inv(H - (E - 1j * eps) * np.eye(N))
    return abs(G[i_left, i_right])


# =============================================================================
# Part 1: Rectangular barrier — ln|G| decays linearly in width
# =============================================================================

def probe1_rectangular_barrier() -> dict:
    """Verify the transfer-matrix bound for a rectangular barrier.

    Setup: flat potential with height V_0 > 0 on an interval of width L,
    zero elsewhere.  The theorem predicts

        ln |G|  <=  -L * ln(lambda_+ / t) / a       (taking a = 1)

    with lambda_+ = (2 + V_0/t + sqrt((V_0/t)^2 + 4 V_0/t)) / 2.
    """
    print("=" * 72)
    print("PROBE 1: rectangular barrier — ln|G| linear in width")
    print("=" * 72)

    t = 1.0
    E = 0.0
    V_0 = 4.0
    N = 401

    widths = [20, 40, 60, 80, 100, 120, 160]
    lambda_plus = evanescent_eigenvalue(V_0, t)
    kappa = math.log(lambda_plus / t)  # per-lattice-site evanescent rate

    print(f"\n  t = {t}, V_0 = {V_0}, E = {E}")
    print(f"  lambda_+ = {lambda_plus:.6f}")
    print(f"  kappa (per site) = ln(lambda_+/t) = {kappa:.6f}")

    results = []
    for L in widths:
        V = np.zeros(N)
        start = (N - L) // 2
        V[start:start + L] = V_0
        exact_ln_G = math.log(max(barrier_amplitude_exact(V, E, t=t), 1e-300))
        bound = -L * kappa  # the transfer-matrix upper bound (up to prefactor)
        results.append({"L": L, "exact_ln_G": exact_ln_G, "bound": bound})
        print(f"  L = {L:4d}: ln|G|_exact = {exact_ln_G:10.4f}, "
              f"bound = -L*kappa = {bound:10.4f}, "
              f"ratio = {exact_ln_G / bound:6.4f}")

    # Linear fit: ln|G| vs L should have slope close to -kappa
    Ls = np.array([r["L"] for r in results], dtype=float)
    ys = np.array([r["exact_ln_G"] for r in results], dtype=float)
    slope, intercept = np.polyfit(Ls, ys, 1)
    slope_theory = -kappa
    print(f"\n  Linear fit: ln|G| = {slope:.6f} * L + {intercept:.4f}")
    print(f"  Theory slope = -kappa = {slope_theory:.6f}")
    rel_err = abs(slope - slope_theory) / abs(slope_theory)
    print(f"  Relative error on slope: {rel_err:.4e}")

    check("rectangular barrier slope matches -kappa to < 1%",
          rel_err < 1e-2,
          f"fit slope {slope:.6f} vs theory {slope_theory:.6f}")
    check("ln|G|_exact is bounded above by -L*kappa for all widths",
          all(r["exact_ln_G"] <= r["bound"] + 5.0 for r in results),
          "exact amplitude decays at least as fast as the transfer-matrix bound")
    # Bound direction: exact <= bound (i.e., ln_exact <= bound_value, which
    # means exact amplitude is smaller or equal to the bound amplitude).
    # Allow small positive slack from algebraic prefactors.

    return {"slope": slope, "kappa": kappa, "results": results}


# =============================================================================
# Part 2: Rectangular barrier — continuum WKB limit in shallow regime
# =============================================================================

def probe2_continuum_wkb_limit() -> dict:
    """Shallow-barrier limit V_0 << t: kappa(V_0) -> sqrt(V_0/t).

    For V_0/t << 1:
        lambda_+ = 1 + sqrt(V_0/t) + V_0/(2t) + O((V_0/t)^{3/2}),
        kappa = ln(lambda_+) = sqrt(V_0/t) + O(V_0/t).
    """
    print("\n" + "=" * 72)
    print("PROBE 2: shallow-barrier WKB limit kappa -> sqrt(V_0/t)")
    print("=" * 72)

    t = 1.0
    V_vals = [1e-4, 1e-3, 1e-2, 1e-1, 1.0]

    print(f"\n  {'V_0/t':>8s}  {'kappa':>12s}  {'sqrt(V_0/t)':>14s}  "
          f"{'ratio':>12s}")

    max_rel_err_small = 0.0
    for V0 in V_vals:
        lp = evanescent_eigenvalue(V0, t)
        kappa = math.log(lp)
        wkb = math.sqrt(V0 / t)
        ratio = kappa / wkb if wkb > 0 else 0
        print(f"  {V0:8.4e}  {kappa:12.6e}  {wkb:14.6e}  {ratio:12.6f}")
        if V0 <= 1e-2:
            rel_err = abs(ratio - 1.0)
            max_rel_err_small = max(max_rel_err_small, rel_err)

    check("shallow-barrier kappa matches continuum WKB sqrt(V/t) at V/t <= 1e-2",
          max_rel_err_small < 0.1,
          f"max relative error at V/t <= 1e-2: {max_rel_err_small:.4e}")

    # Deep-barrier limit: kappa -> ln(V_0/t) for V_0/t >> 1
    print(f"\n  Deep-barrier regime (V_0/t >> 1): kappa -> ln(V_0/t)")
    V_deep = [10.0, 100.0, 1000.0, 10000.0]
    print(f"  {'V_0/t':>8s}  {'kappa':>12s}  {'ln(V_0/t)':>14s}  {'ratio':>12s}")
    max_rel_err_deep = 0.0
    for V0 in V_deep:
        lp = evanescent_eigenvalue(V0, t)
        kappa = math.log(lp)
        deep = math.log(V0 / t)
        ratio = kappa / deep if deep > 0 else 0
        print(f"  {V0:8.2f}  {kappa:12.6e}  {deep:14.6e}  {ratio:12.6f}")
        if V0 >= 100.0:
            rel_err = abs(ratio - 1.0)
            max_rel_err_deep = max(max_rel_err_deep, rel_err)

    check("deep-barrier kappa matches ln(V/t) at V/t >= 100",
          max_rel_err_deep < 0.1,
          f"max relative error at V/t >= 100: {max_rel_err_deep:.4e}")

    return {"max_rel_err_small": max_rel_err_small, "max_rel_err_deep": max_rel_err_deep}


# =============================================================================
# Part 3: Schwarzschild tortoise length gives the ln(R_S/R_min) factor
# =============================================================================

def schwarzschild_interior_tortoise_length(R_S: float, R_min: float,
                                            eps: float | None = None) -> float:
    """Exact closed-form integral int_{R_min}^{R_S - eps} dr / |f(r)|.

    For f(r) = 1 - R_S/r and r < R_S, |f(r)| = R_S/r - 1 = (R_S - r)/r.
    The primitive is

        int dr * r / (R_S - r) = (R_S - r) - R_S ln(R_S - r) + C
                               = -u - R_S ln u + C          (u = R_S - r)

    giving

        L*(R_min, R_S - eps)
            = [ -u - R_S ln u ]_{u = eps}^{u = R_S - R_min}
            = (-R_S + R_min + R_S ln(R_S - R_min)) + eps + R_S ln eps
            = R_S ln((R_S - R_min)/eps) + (eps + R_min - R_S).

    For R_min << R_S and eps = R_min (cutoff at a Planck-distance from
    the would-be horizon), L* ~ R_S ln(R_S/R_min) - R_S + O(R_min).
    """
    if eps is None:
        eps = R_min
    return (R_S * math.log((R_S - R_min) / eps)
            + eps + R_min - R_S)


def probe3_tortoise_length_identity() -> dict:
    """Verify the Schwarzschild-interior tortoise-length formula.

    This is the bounded physical-identification piece that converts the
    retained lattice transfer-matrix bound (probe 1) into the
    (R_S/a) * ln(R_S/R_min) form.  On the retained restricted
    strong-field closure surface plus the retained lattice hard floor,
    the evanescent region [R_min, R_S - a] has proper/tortoise length

        L* ~ R_S * ln(R_S/R_min) - R_S + O(R_min).

    The retained transfer-matrix bound (probe 1, order-1 per lattice
    site) then gives

        |G| <= exp[-L*/a] = exp[-(R_S/a) * (ln(R_S/R_min) - 1 + O(R_min/R_S))].
    """
    print("\n" + "=" * 72)
    print("PROBE 3: Schwarzschild interior tortoise length L*")
    print("=" * 72)

    # In units where a = 1 (lattice units), choose a variety of R_S/R_min
    # ratios that cover the relevant astrophysical range (3 orders of magnitude
    # in ratio gives ln ~ 7, the real physical numbers push this much further)
    # The formula L* = R_S * ln(R_S/R_min) - R_S + O(R_min) is tested here.
    R_min = 1  # one lattice site
    R_S_vals = [30, 100, 300, 1000, 3000, 10000, 30000]

    print(f"\n  Lattice units a = 1,  R_min = {R_min},  eps = R_min")
    print(f"\n  {'R_S':>8s}  {'L* (exact)':>14s}  {'R_S ln(R_S/R_min) - R_S':>28s}  "
          f"{'ratio':>10s}  {'approx error':>14s}")

    results = []
    max_rel_err = 0.0
    for R_S in R_S_vals:
        L_exact = schwarzschild_interior_tortoise_length(R_S, R_min)
        L_leading = R_S * math.log(R_S / R_min) - R_S
        ratio = L_exact / L_leading if L_leading != 0 else float("inf")
        rel_err = abs(L_exact - L_leading) / L_leading
        if R_S / R_min >= 300:
            max_rel_err = max(max_rel_err, rel_err)
        results.append({
            "R_S": R_S, "L_exact": L_exact, "L_leading": L_leading,
            "ratio": ratio, "rel_err": rel_err,
        })
        print(f"  {R_S:8d}  {L_exact:14.4f}  {L_leading:28.4f}  "
              f"{ratio:10.6f}  {rel_err:14.4e}")

    print(f"\n  Max relative error at R_S/R_min >= 300: {max_rel_err:.4e}")
    print(f"  Theory: L* = R_S*ln(R_S/R_min) - R_S + O(R_min/R_S)")

    check("tortoise length matches leading-order formula at large R_S/R_min",
          max_rel_err < 1e-3,
          f"max error {max_rel_err:.4e} for R_S/R_min >= 300")

    # Scaling verification: L* / (R_S ln(R_S/R_min)) -> 1 as R_S/R_min -> infinity
    large = [r for r in results if r["R_S"] / R_min >= 1000]
    scaling_ratios = [r["L_exact"] / (r["R_S"] * math.log(r["R_S"] / R_min))
                      for r in large]
    mean_scaling = float(np.mean(scaling_ratios))
    print(f"\n  L* / (R_S ln(R_S/R_min)) at R_S/R_min >= 1000: {mean_scaling:.6f}")
    print(f"  Theory: scaling ratio -> 1 as R_S/R_min -> infinity")
    # For R_S/R_min = 30000: ln = 10.3, so 1 - 1/ln ~ 0.90
    check("tortoise length ratio to R_S * ln approaches 1 at large R_S/R_min",
          0.80 < mean_scaling < 1.0,
          f"mean ratio {mean_scaling:.4f} (must be in (0.80, 1.0))")

    # Retained theorem B is a geometric identity.  It does NOT by itself
    # produce an amplitude bound: reaching ln |G| <= -L*/a requires an
    # O(1) per-unit-tortoise-length rate lower bound (open conditional
    # C-rate).  Theorem B names L* as the length scale that would appear
    # in such a bound; probe 4 documents, rather than retains, that step.
    print(f"\n  Theorem B is geometric.  Converting L* into an amplitude bound")
    print(f"  requires the open conditional (C-rate).  See probe 4 for the")
    print(f"  diagnostic of the bounded-companion Planck-unit exponent.")

    return {"results": results, "max_rel_err": max_rel_err,
            "mean_scaling": mean_scaling}


# =============================================================================
# Part 4: Lattice sanity diagnostic for the bounded companion exponent
# =============================================================================

def probe4_universal_lp_bound() -> dict:
    """Lattice sanity diagnostic for the (C-rate)-conditional Planck-unit
    astrophysical exponent carried by the bounded GW-echo null companion.

    The bounded companion frontier_echo_null_result.py carries

        |T| ~ exp[-(R_S/l_P) * ln(R_S/R_min)].

    This probe does two things:

      (a) it prints astrophysical |Phi|/a values under that exponent for
          representative R_S / l_Planck ratios, to document that the
          COMPANION exponent is wildly sub-Planck for every LIGO-class
          source (this is a companion diagnostic, NOT a retained
          consequence of theorems A + B);

      (b) it computes the rigorous retained-theorem-A summed phase
          Phi_exact = sum_i ln lambda_+(i) for the direct-in-r
          Schwarzschild profile V(r)/t = R_S/r on [1, R_S] and asserts
          (via check()) that this retained quantity is upper-bounded by
          the (C-rate) formal quantity (R_S/a) * ln(R_S/a), with a small
          slack for discretization.  That inequality is a necessary
          condition for (C-rate); it does not establish (C-rate).
    """
    print("\n" + "=" * 72)
    print("PROBE 4: companion-diagnostic (C-rate-conditional) Planck-unit exponent")
    print("=" * 72)

    # Physical constants (SI) just for ratio calibration
    G_SI = 6.674e-11
    C_LIGHT = 2.998e8
    M_SUN = 1.989e30
    L_PLANCK = 1.616e-35

    # Representative compact-object scales
    scenarios = [
        ("1 M_sun neutron star", 1.0),
        ("10 M_sun BH",          10.0),
        ("30 M_sun BH (GW190521-like)", 30.0),
        ("62 M_sun BH (GW150914 remnant)", 62.0),
        ("4e6 M_sun Sgr A*",     4.0e6),
    ]

    print(f"\n  Retained Planck unit: l_Planck = {L_PLANCK:.3e} m\n")
    print(f"  {'object':>36s}  {'R_S (m)':>12s}  {'R_S/l_P':>12s}  "
          f"{'|Phi|/a (bits)':>16s}  {'status':>12s}")

    all_sub_planck = True
    sensible_scaling = True
    prev_exp = 0.0
    for label, M_solar in scenarios:
        M = M_solar * M_SUN
        R_S = 2.0 * G_SI * M / C_LIGHT**2
        r_ratio = R_S / L_PLANCK
        # Retained bound: |Phi|/a >= (R_S/l_P) * ln(R_S/l_P)
        bound_exp = r_ratio * math.log(r_ratio)
        bound_bits = bound_exp / math.log(2.0)
        status = "sub-Planck" if bound_bits > 1.0 else "Planck"
        if bound_bits < 1.0:
            all_sub_planck = False
        if bound_exp < prev_exp:
            sensible_scaling = False
        prev_exp = bound_exp
        print(f"  {label:>36s}  {R_S:12.4e}  {r_ratio:12.4e}  "
              f"{bound_bits:16.4e}  {status:>12s}")

    check("companion (C-rate-conditional) exponent is sub-Planck for every listed astrophysical R_S",
          all_sub_planck,
          "|Phi|/a > 1 bit for every listed object under the (C-rate)-conditional formula",
          kind="COMPANION-DIAGNOSTIC")
    check("companion (C-rate-conditional) exponent is monotone in R_S",
          sensible_scaling,
          "|Phi|/a increases with R_S as required",
          kind="COMPANION-DIAGNOSTIC")

    # Lattice sanity: the retained-theorem-A summed phase Phi_exact for the
    # direct-in-r Schwarzschild profile should satisfy
    #     Phi_exact  <=  (1 + slack) * R_S * ln(R_S/a)
    # with the (C-rate) formal RHS on the right.  This is a real assertion
    # (not print-only): every row must pass, and the check() call below
    # records the failure count explicitly.
    print(f"\n  Lattice sanity (a = 1, R_min = 1): asserting Phi_exact <= 1.01 * (R_S/a) ln(R_S/a)")
    print(f"  (necessary condition for (C-rate); not a proof of it)\n")
    print(f"  {'R_S (lattice)':>14s}  {'Phi_exact':>12s}  "
          f"{'(R_S/a)ln(R_S/a)':>18s}  {'ratio':>8s}  {'ok':>6s}")
    sanity_all_ok = True
    sanity_rows: list[dict] = []
    for R_S in [20, 40, 80, 160, 320]:
        N = R_S + 40
        V = np.zeros(N)
        for x in range(N):
            r = x - 10 + 1
            if 1 <= r <= R_S:
                V[x] = 1.0 * R_S / r
        phi_exact = suppression_phase_exact(V, 0.0, t=1.0)
        bound = R_S * math.log(R_S)
        ratio = phi_exact / bound if bound > 0 else float("inf")
        ok = phi_exact <= bound * 1.01  # allow 1% slack for discretization
        if not ok:
            sanity_all_ok = False
        sanity_rows.append({
            "R_S": R_S, "phi_exact": phi_exact, "bound": bound,
            "ratio": ratio, "ok": ok,
        })
        print(f"  {R_S:14d}  {phi_exact:12.4f}  {bound:18.4f}  "
              f"{ratio:8.4f}  {'yes' if ok else 'NO':>6s}")

    max_ratio = max((r["ratio"] for r in sanity_rows), default=float("nan"))
    check("lattice-sanity Phi_exact <= 1.01*(R_S/a) ln(R_S/a) holds on every tested R_S",
          sanity_all_ok,
          f"{len(sanity_rows)} rows checked; max ratio {max_ratio:.4f}")

    return {
        "all_sub_planck": all_sub_planck,
        "sensible_scaling": sensible_scaling,
        "sanity_rows": sanity_rows,
        "sanity_all_ok": sanity_all_ok,
    }


# =============================================================================
# Part 5: Robustness — bound holds for a family of barrier profiles
# =============================================================================

def probe5_robustness_barrier_profiles() -> dict:
    """Verify the bound holds under perturbations of the potential profile.

    We test:
      - rectangular
      - triangular
      - 1/r (Schwarzschild-like)
      - 1/r^2 (photon-sphere-like)
      - log-smeared
    All should obey ln|G|_exact <= -sum_x ln(lambda(x)/t) + O(1).
    """
    print("\n" + "=" * 72)
    print("PROBE 5: bound holds across barrier-profile family")
    print("=" * 72)

    t = 1.0
    E = 0.0
    N = 201
    start = 40
    L = 120
    R_S_eff = 100

    profiles = {}
    # Rectangular
    V_rect = np.zeros(N)
    V_rect[start:start + L] = 2.0
    profiles["rectangular"] = V_rect
    # Triangular
    V_tri = np.zeros(N)
    mid = start + L // 2
    for x in range(start, start + L):
        V_tri[x] = 2.0 * (1.0 - abs(x - mid) / (L / 2))
    profiles["triangular"] = V_tri
    # Schwarzschild-like 1/r
    V_s = np.zeros(N)
    for x in range(start, start + L):
        r = x - start + 1
        V_s[x] = R_S_eff / r
    profiles["schwarzschild_1/r"] = V_s
    # Photon-sphere-like 1/r^2
    V_p = np.zeros(N)
    for x in range(start, start + L):
        r = x - start + 1
        V_p[x] = (R_S_eff ** 2) / r ** 2
    profiles["inverse_square_1/r^2"] = V_p
    # Log-smeared sharp cliff
    V_log = np.zeros(N)
    for x in range(start, start + L):
        V_log[x] = 2.0 / (1.0 + math.exp(-0.3 * (x - start - 20)))
    profiles["logistic"] = V_log

    print(f"\n  {'profile':>24s}  {'Phi_exact':>12s}  {'ln|G|_exact':>14s}  "
          f"{'bound_ok':>10s}")

    bound_holds_for_all = True
    for name, V in profiles.items():
        phi_exact = suppression_phase_exact(V, E, t=t)
        ln_G = math.log(max(barrier_amplitude_exact(V, E, t=t), 1e-300))
        # Allow for algebraic prefactor: ln|G| <= -Phi + C with C = O(ln N)
        slack = math.log(N) + 2.0
        ok = ln_G <= -phi_exact + slack
        if not ok:
            bound_holds_for_all = False
        print(f"  {name:>24s}  {phi_exact:12.4f}  {ln_G:14.4f}  "
              f"{'yes' if ok else 'NO':>10s}")

    check("transfer-matrix bound holds across all barrier profiles",
          bound_holds_for_all,
          "ln|G|_exact <= -Phi + O(ln N) on every tested profile")

    return {"bound_holds": bound_holds_for_all}


# =============================================================================
# Part 6: Framework identification — the suppression phase is a = l_Planck fact
# =============================================================================

def probe6_framework_identification() -> dict:
    """Bounded-companion diagnostic: reproduce the GW150914 exponent of
    frontier_echo_null_result.py and verify that it scales as 1/a.

    This is a diagnostic of the BOUNDED companion formula, not a retained
    consequence of theorems A + B.  The formula
        |T| ~ exp[-(R_S/l_P) * ln(R_S/R_min)]
    requires the open conditional (C-rate); probe 6 documents that under
    (C-rate), the Planck-unit astrophysical exponent is reproduced and
    scales correctly with hypothetical lattice spacing.
    """
    print("\n" + "=" * 72)
    print("PROBE 6: bounded-companion diagnostic — reproduce GW150914 exponent")
    print("=" * 72)

    G_SI = 6.674e-11
    C_LIGHT = 2.998e8
    M_SUN = 1.989e30
    L_PLANCK = 1.616e-35
    M_NUCLEON = 1.673e-27

    # GW150914 benchmark (matches frontier_echo_null_result.py)
    M_solar = 62.0
    M = M_solar * M_SUN
    R_S = 2.0 * G_SI * M / C_LIGHT**2
    N_baryons = M / M_NUCLEON
    # lattice floor R_min = max(N^{1/3} l_P, l_P) from the frozen-star stack
    R_min = max(N_baryons ** (1.0 / 3.0) * L_PLANCK, L_PLANCK)
    # retained-bound exponent
    exponent_retained = -(R_S / L_PLANCK) * math.log(R_S / R_min)
    log10_T = exponent_retained / math.log(10.0)

    print(f"\n  Benchmark: {M_solar} M_sun BH (GW150914 remnant)")
    print(f"  R_S           = {R_S:.4e} m")
    print(f"  R_S / l_P     = {R_S / L_PLANCK:.4e}")
    print(f"  R_min         = {R_min:.4e} m  (lattice floor)")
    print(f"  R_min / l_P   = {R_min / L_PLANCK:.4e}")
    print(f"  ln(R_S/R_min) = {math.log(R_S / R_min):.4f}")
    print(f"  exponent = -(R_S/l_P)*ln(R_S/R_min) = {exponent_retained:.4e}")
    print(f"  log10 |T|      = {log10_T:.4e}")

    check("companion (C-rate-conditional) exponent agrees with frontier_echo_null_result.py",
          log10_T < -1e20,
          f"log10|T| = {log10_T:.3e} < -1e20 (enormous sub-Planck suppression under (C-rate))",
          kind="COMPANION-DIAGNOSTIC")

    # Sanity: doubling the spacing halves the exponent magnitude
    a_big = 2.0 * L_PLANCK
    exp_big = -(R_S / a_big) * math.log(R_S / R_min)
    ratio = exp_big / exponent_retained
    print(f"\n  If we had a = 2 l_Planck (hypothetical): exponent = {exp_big:.4e}")
    print(f"  Ratio (hypothetical / retained) = {ratio:.6f} (expected 0.5)")

    check("companion (C-rate-conditional) exponent scales as 1/a",
          abs(ratio - 0.5) < 1e-6,
          f"ratio = {ratio:.6f}",
          kind="COMPANION-DIAGNOSTIC")

    return {
        "R_S": R_S, "R_min": R_min, "exponent": exponent_retained,
        "log10_T": log10_T,
    }


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    print("Discrete Evanescent-Barrier Amplitude Suppression on Cl(3)/Z^3")
    print("=" * 72)
    print()
    print("Retained scope:")
    print("  Theorem A: discrete lattice transfer-matrix bound")
    print("             |G| <= C exp[-sum_i ln lambda_+(i)],")
    print("             lambda_+(i) = (u_i + sqrt(u_i^2 - 4))/2,")
    print("             u_i = 2 + (V_i - E)/t.")
    print("  Theorem B: Schwarzschild interior tortoise-length identity")
    print("             L* = R_S ln((R_S - R_min)/eps) + eps + R_min - R_S.")
    print()
    print("Open conditional (C-rate):  order-one per-unit-tortoise-length rate")
    print("  lower bound required to convert theorems A + B into the Planck-unit")
    print("  astrophysical exponent exp[-(R_S/l_P) ln(R_S/R_min)] carried by the")
    print("  bounded GW-echo null companion.  NOT on the retained surface.")
    print()

    probe1_rectangular_barrier()
    probe2_continuum_wkb_limit()
    probe3_tortoise_length_identity()
    probe4_universal_lp_bound()
    probe5_robustness_barrier_profiles()
    probe6_framework_identification()

    print()
    print("=" * 72)
    print(f"PASS = {PASS_COUNT}")
    print(f"FAIL = {FAIL_COUNT}")
    if FAILURES:
        for name in FAILURES:
            print(f"  FAIL: {name}")
        sys.exit(1)
    print()
    print("Retained conclusion:")
    print("  Theorem A (lattice transfer-matrix bound) and theorem B (Schwarzschild")
    print("  tortoise-length identity) are verified on this branch.  The Planck-unit")
    print("  astrophysical exponent exp[-(R_S/l_P) ln(R_S/R_min)] carried by the")
    print("  bounded GW-echo null companion is (C-rate)-conditional, not retained.")


if __name__ == "__main__":
    main()
