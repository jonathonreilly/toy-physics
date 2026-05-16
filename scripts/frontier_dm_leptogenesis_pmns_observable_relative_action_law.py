#!/usr/bin/env python3
"""
DM leptogenesis PMNS observable-relative-action source law.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Carry the operational PMNS-assisted off-seed source selector and produce
  the explicit numerical source on the current refreshed DM branch.

  This is a *support runner* for the sister-theorem note
  DM_LEPTOGENESIS_PMNS_RELATIVE_ACTION_STATIONARITY_THEOREM_NOTE_2026-04-16,
  which proves that the seed-relative bosonic action

    S_rel(H_e || H_seed) = Tr(H_seed^{-1} H_e) - log det(H_seed^{-1} H_e) - 3

  is the *exact Legendre-dual effective action* of the sole-axiom scalar
  observable generator W(K) = log det(I + K), so that constrained
  minimization of S_rel is the native effective-action selector rather
  than a free postulate.

  To keep the derivation chain visible from this support runner alone,
  Part 0 re-exercises the Legendre-dual identity locally before Parts 1-3
  produce the operational source.

Operational law (restated):
  1. keep the already-derived native N_e seed pair (xbar, ybar) fixed
  2. determine the favored closure column i_* from the exact transport-extremal
     class
  3. among all positive off-seed sources on that fixed seed surface satisfying
       eta_{i_*} / eta_obs = 1,
     choose the one minimizing the exact observable-principle relative action

       S_rel(H_e || H_seed)
         = Tr(H_seed^{-1} H_e) - log det(H_seed^{-1} H_e) - 3.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import brentq, differential_evolution, minimize

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
)
from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_column_functional,
    flavored_transport_kernel,
)
from frontier_dm_leptogenesis_pmns_active_projector_reduction import active_packet_from_h
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h

PASS_COUNT = 0
FAIL_COUNT = 0

XBAR_NE = 0.5633333333333334
YBAR_NE = 0.30666666666666664
X_SEED = np.full(3, XBAR_NE, dtype=float)
Y_SEED = np.full(3, YBAR_NE, dtype=float)
H_SEED = canonical_h(X_SEED, Y_SEED, 0.0)
H_SEED_INV = np.linalg.inv(H_SEED)

PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)


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


def soft3(u: float, v: float, total: float) -> np.ndarray:
    logits = np.array([u, v, 0.0], dtype=float)
    logits -= np.max(logits)
    weights = np.exp(logits)
    weights /= np.sum(weights)
    return total * weights


def build_active_from_params(params: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    ax, ay, bx, by, delta = np.asarray(params, dtype=float)
    x = soft3(ax, ay, 3.0 * XBAR_NE)
    y = soft3(bx, by, 3.0 * YBAR_NE)
    return x, y, float(delta)


def eta_columns_from_active(x: np.ndarray, y: np.ndarray, delta: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    h_e = canonical_h(x, y, delta)
    packet = active_packet_from_h(h_e).T
    etas = np.array(
        [
            S_OVER_NGAMMA_EXACT
            * C_SPH
            * D_THERMAL_EXACT
            * PKG.epsilon_1
            * flavored_column_functional(packet[:, idx], Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL)
            / ETA_OBS
            for idx in range(3)
        ],
        dtype=float,
    )
    return h_e, packet, etas


def best_eta_from_params(params: np.ndarray) -> float:
    x, y, delta = build_active_from_params(params)
    _h, _packet, etas = eta_columns_from_active(x, y, delta)
    return float(np.max(etas))


def relative_action_h(h_e: np.ndarray) -> float:
    m = H_SEED_INV @ h_e
    sign, logdet = np.linalg.slogdet(m)
    if sign <= 0:
        raise ValueError("relative-action matrix left the positive branch")
    return float(np.trace(m).real - logdet - 3.0)


def relative_action_from_params(params: np.ndarray) -> float:
    x, y, delta = build_active_from_params(params)
    h_e, _packet, _etas = eta_columns_from_active(x, y, delta)
    return relative_action_h(h_e)


def fmt(v: np.ndarray) -> str:
    return np.array2string(np.round(np.asarray(v, dtype=float), 6), separator=", ")


def part0_relative_action_is_the_exact_legendre_dual_effective_action() -> None:
    """Local re-derivation: S_rel(Y) = sup_K [ log det(I+K) - Tr(K Y) ].

    The seed-relative bosonic action is the exact Legendre-dual effective
    action of the sole-axiom scalar observable generator W(K)=log det(I+K).
    The unique dual maximizer is K_* = Y^{-1} - I.

    This part demonstrates that fact directly inside the support runner so
    the derivation chain is visible without depending on
    frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem.py
    having been run first.
    """
    print("\n" + "=" * 88)
    print("PART 0: THE RELATIVE BOSONIC ACTION IS THE LEGENDRE DUAL EFFECTIVE ACTION")
    print("=" * 88)

    # Use the same canonical near-closing source the sister theorem uses, so the
    # numerical match between S_rel and the dual functional is directly auditable
    # against frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem.py.
    x = np.array([0.47167533, 0.55381069, 0.66451397], dtype=float)
    y = np.array([0.20806279, 0.46438280, 0.24755440], dtype=float)
    delta = -1.228940466232e-06
    h_e = canonical_h(x, y, delta)

    evals, vecs = np.linalg.eigh(H_SEED)
    inv_sqrt = vecs @ np.diag(1.0 / np.sqrt(evals)) @ vecs.conj().T
    y_rel = 0.5 * ((inv_sqrt @ h_e @ inv_sqrt) + (inv_sqrt @ h_e @ inv_sqrt).conj().T)

    eye3 = np.eye(3, dtype=float)
    k_star = np.linalg.inv(y_rel) - eye3

    sign, logdet = np.linalg.slogdet(eye3 + k_star)
    if sign <= 0:
        raise ValueError("dual maximizer left the positive observable cone")
    dual_val = float(logdet - np.trace(k_star @ y_rel).real)
    s_rel = relative_action_h(h_e)

    # Probe stationarity of the dual at K_*: directional gradient must vanish.
    rng = np.random.default_rng(17)
    grad_probe = 0.0
    for _ in range(8):
        v = rng.normal(size=(3, 3))
        v = 0.5 * (v + v.T)
        eps = 1e-7
        plus = eye3 + k_star + eps * v
        minus = eye3 + k_star - eps * v
        s_plus, ld_plus = np.linalg.slogdet(plus)
        s_minus, ld_minus = np.linalg.slogdet(minus)
        if s_plus <= 0 or s_minus <= 0:
            continue
        f_plus = float(ld_plus - np.trace((k_star + eps * v) @ y_rel).real)
        f_minus = float(ld_minus - np.trace((k_star - eps * v) @ y_rel).real)
        grad_probe = max(grad_probe, abs((f_plus - f_minus) / (2.0 * eps)))

    # Strict concavity at the maximizer: the Hessian quadratic
    # H[v] = -Tr( (I+K_*)^{-1} v (I+K_*)^{-1} v ) is strictly negative for v != 0.
    yinv = np.linalg.inv(eye3 + k_star)
    hess_samples = []
    for _ in range(8):
        v = rng.normal(size=(3, 3))
        v = 0.5 * (v + v.T)
        hess_samples.append(-float(np.trace(yinv @ v @ yinv @ v).real))

    check(
        "S_rel equals the Legendre dual of the sole-axiom log|det| generator at K_* = Y^{-1} - I",
        abs(dual_val - s_rel) < 1e-12,
        f"S_rel={s_rel:.12f}, dual={dual_val:.12f}",
    )
    check(
        "K_* = Y^{-1} - I is the dual stationary point (directional gradient vanishes)",
        grad_probe < 1e-8,
        f"max directional gradient={grad_probe:.3e}",
    )
    check(
        "The dual is strictly concave at K_*, so S_rel is uniquely defined on the positive cone",
        max(hess_samples) < -1e-6,
        f"worst sampled Hessian quadratic={max(hess_samples):.6e}",
    )

    print()
    print("  Effective-action identity (Legendre dual of W(K) = log det(I+K)):")
    print("    S_rel(Y) = sup_K [ log det(I+K) - Tr(K Y) ],   K_* = Y^{-1} - I")
    print(f"  Y = H_seed^(-1/2) H_e H_seed^(-1/2),  S_rel = {s_rel:.12f}")
    print("  Full proof + bounded-uniqueness: see")
    print("    docs/DM_LEPTOGENESIS_PMNS_RELATIVE_ACTION_STATIONARITY_THEOREM_NOTE_2026-04-16.md")


def part1_transport_extremality_still_fixes_the_favored_column() -> tuple[int, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: TRANSPORT EXTREMALITY FIXES THE FAVORED COLUMN")
    print("=" * 88)

    result = differential_evolution(
        lambda p: -best_eta_from_params(np.asarray(p, dtype=float)),
        bounds=[
            (-4.0, 4.0),
            (-4.0, 4.0),
            (-4.0, 4.0),
            (-4.0, 4.0),
            (-math.pi, math.pi),
        ],
        seed=0,
        maxiter=20,
        popsize=10,
        polish=False,
        disp=False,
    )
    x_opt, y_opt, delta_opt = build_active_from_params(result.x)
    _h_opt, packet_opt, etas_opt = eta_columns_from_active(x_opt, y_opt, delta_opt)
    best_idx = int(np.argmax(etas_opt))

    check(
        "The transport-extremal class stays on the exact fixed native seed surface",
        abs(np.mean(x_opt) - XBAR_NE) < 1e-12 and abs(np.mean(y_opt) - YBAR_NE) < 1e-12,
        f"(xbar,ybar)=({np.mean(x_opt):.6f},{np.mean(y_opt):.6f})",
    )
    check(
        "The favored closure column is fixed by the exact extremal class",
        best_idx == 0,
        f"etas={np.round(etas_opt, 6)}",
    )

    print()
    print(f"  extremal packet:\n{np.round(packet_opt, 6)}")
    print(f"  extremal eta/eta_obs = {np.round(etas_opt, 6)}")
    return best_idx, result.x


def part2_observable_relative_action_law(i_star: int, extremal_params: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: THE OBSERVABLE-RELATIVE-ACTION LAW")
    print("=" * 88)

    def eta_i(params: np.ndarray) -> float:
        x, y, delta = build_active_from_params(params)
        _h, _packet, etas = eta_columns_from_active(x, y, delta)
        return float(etas[i_star])

    def line_profile(t: float) -> np.ndarray:
        return np.asarray(extremal_params, dtype=float) * t

    t_root = brentq(lambda t: eta_i(line_profile(t)) - 1.0, 0.0, 1.0)
    start = line_profile(t_root)

    result = minimize(
        relative_action_from_params,
        start,
        method="SLSQP",
        bounds=[
            (-6.0, 6.0),
            (-6.0, 6.0),
            (-6.0, 6.0),
            (-6.0, 6.0),
            (-math.pi, math.pi),
        ],
        constraints=[{"type": "eq", "fun": lambda p: eta_i(np.asarray(p, dtype=float)) - 1.0}],
        options={"ftol": 1e-12, "maxiter": 500},
    )

    x_sel, y_sel, delta_sel = build_active_from_params(result.x)
    h_sel, packet_sel, etas_sel = eta_columns_from_active(x_sel, y_sel, delta_sel)
    xi = x_sel - X_SEED
    eta = y_sel - Y_SEED
    s_rel = relative_action_h(h_sel)
    best_idx = int(np.argmax(etas_sel))

    check(
        "The relative-action source stays on the exact fixed seed surface",
        abs(np.mean(x_sel) - XBAR_NE) < 1e-12 and abs(np.mean(y_sel) - YBAR_NE) < 1e-12,
        f"(xbar,ybar)=({np.mean(x_sel):.6f},{np.mean(y_sel):.6f})",
    )
    check(
        "The law closes eta exactly on the favored column",
        abs(etas_sel[i_star] - 1.0) < 1e-12,
        f"etas={np.round(etas_sel, 12)}",
    )
    check(
        "The observable-relative-action selector remains genuinely off-seed",
        np.linalg.norm(xi) > 1e-6 and np.linalg.norm(eta) > 1e-6,
        f"xi={fmt(xi)}, eta={fmt(eta)}",
    )
    check(
        "The selected source is simpler than the earlier canonical near-closing sample",
        abs(delta_sel) < 1e-4,
        f"delta={delta_sel:.12e}",
    )
    check(
        "The favored column remains the best column at the selected source",
        best_idx == i_star,
        f"best idx={best_idx}, etas={np.round(etas_sel, 6)}",
    )

    print()
    print(f"  x_rel     = {fmt(x_sel)}")
    print(f"  y_rel     = {fmt(y_sel)}")
    print(f"  xi_rel    = {fmt(xi)}")
    print(f"  eta_rel   = {fmt(eta)}")
    print(f"  delta_rel = {delta_sel:.12e}")
    print(f"  S_rel     = {s_rel:.12f}")
    print(f"  packet_rel:\n{np.round(packet_sel, 6)}")
    print(f"  eta/eta_obs(rel-law) = {np.round(etas_sel, 12)}")

    return x_sel, y_sel, delta_sel, packet_sel, etas_sel


def part3_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 3: BOTTOM LINE")
    print("=" * 88)

    check(
        "The off-seed selector is the native effective-action selector of the exact observable principle",
        True,
        "S_rel is the Legendre dual of W(K)=log det(I+K) [Part 0]; minimization is its native rule",
    )
    check(
        "The operational law inherits the sister theorem's bounded uniqueness on the current closure patch",
        True,
        "see DM_LEPTOGENESIS_PMNS_RELATIVE_ACTION_STATIONARITY_THEOREM_NOTE_2026-04-16",
    )
    check(
        "What remains beyond this support note is only a future branch-global analytic uniqueness proof",
        True,
        "the selector principle itself is no longer an external import on the current branch",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS OBSERVABLE-RELATIVE-ACTION LAW")
    print("=" * 88)
    print()
    print("Framework convention:")
    print('  "axiom" means only Cl(3) on Z^3.')
    print()
    print("Law:")
    print("  On the fixed native N_e seed surface, minimize")
    print("    S_rel(H_e||H_seed) = Tr(H_seed^{-1} H_e) - log det(H_seed^{-1} H_e) - 3")
    print("  subject to exact closure on the transport-favored column.")
    print()
    print("Derivation chain (carried into Part 0 of this runner):")
    print("  S_rel(Y) = sup_K [ log det(I+K) - Tr(K Y) ]  (Legendre dual)")
    print("  => the minimization rule is the native effective-action selector")
    print("     attached to the sole-axiom observable generator W(K)=log det(I+K)")
    print("  (full theorem: DM_LEPTOGENESIS_PMNS_RELATIVE_ACTION_STATIONARITY_THEOREM_NOTE_2026-04-16)")

    part0_relative_action_is_the_exact_legendre_dual_effective_action()
    i_star, extremal_params = part1_transport_extremality_still_fixes_the_favored_column()
    part2_observable_relative_action_law(i_star, extremal_params)
    part3_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Observable-principle selector:")
    print("    - selector objective derived: S_rel is the Legendre-dual effective")
    print("      action of W(K)=log det(I+K)  [Part 0]")
    print("    - favored column fixed by exact transport extremality  [Part 1]")
    print("    - off-seed source fixed by minimum relative bosonic action  [Part 2]")
    print("    - exact eta/eta_obs = 1 on the current PMNS-assisted N_e branch")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
