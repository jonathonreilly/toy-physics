#!/usr/bin/env python3
"""
Graph-Native Freeze-Out: master equation, dilution, and the relic gap
======================================================================

This script attacks the relic-abundance blocker from the framework side.

What it derives:
  - the exact density-dilution identity on a growing graph
  - the homogeneous graph-native master equation for pair annihilation
  - the native decoupling criterion Gamma_ann ~ Gamma_dil
  - the strongest non-imported piece: a graph-clock freeze-out threshold

What remains open:
  - identifying the graph growth rate with physical Hubble expansion
  - identifying the graph equilibrium profile with thermal equilibrium
  - turning the graph-clock threshold into a physical relic abundance

The key point is simple:

  If N(t) is the total occupation and V(t) is graph volume, then

      Y(t) = N(t) / V(t)

  obeys the exact quotient-rule identity

      dY/dt + (d ln V/dt) Y = (1/V) dN/dt.

  For homogeneous pair annihilation with contact enhancement S_contact,
  the native graph master equation becomes

      dN/dt = -lambda_eff * V * (Y^2 - Y_eq^2)

  and therefore

      dY/dt + Gamma_dil * Y = -lambda_eff * (Y^2 - Y_eq^2)

  where Gamma_dil = d ln V / dt.

  This is the strongest graph-native result in the freeze-out lane.
  The remaining physical relic-abundance step still needs the map
  Gamma_dil -> 3H and the graph equilibrium -> thermal equilibrium.

Self-contained: numpy only.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np

np.set_printoptions(precision=8, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-graph_native_freezeout.txt"

results = []


def log(msg: str = "") -> None:
    results.append(msg)
    print(msg)


@dataclass(frozen=True)
class GraphFreezeOutParams:
    """Parameters for the graph-native master equation."""

    graph_growth_rate: float = 0.18
    annihilation_prefactor: float = 0.70
    equilibrium_scale: float = 1.0
    equilibrium_decay: float = 0.85
    volume0: float = 1.0

    @property
    def dilution_rate(self) -> float:
        return self.graph_growth_rate


def graph_volume(t: float, params: GraphFreezeOutParams) -> float:
    """Regular graph growth model: V(t) = V0 * exp(Gamma_dil * t)."""
    return params.volume0 * math.exp(params.graph_growth_rate * t)


def graph_equilibrium_yield(t: float, params: GraphFreezeOutParams) -> float:
    """
    A graph-native equilibrium surrogate.

    This is not the physical thermal bath. It is only a smooth equilibrium
    profile on the graph clock, used to probe the native master equation.
    """
    return params.equilibrium_scale * math.exp(-params.equilibrium_decay * t)


def lambda_eff(contact_enhancement: float, params: GraphFreezeOutParams) -> float:
    """Contact-enhanced annihilation strength."""
    return params.annihilation_prefactor * contact_enhancement


def yield_rhs(t: float, y: float, contact_enhancement: float, params: GraphFreezeOutParams) -> float:
    """Homogeneous graph-native yield equation."""
    lam = lambda_eff(contact_enhancement, params)
    y_eq = graph_equilibrium_yield(t, params)
    return -lam * (y * y - y_eq * y_eq) - params.dilution_rate * y


def occupancy_rhs(t: float, y: float, contact_enhancement: float, params: GraphFreezeOutParams) -> float:
    """Total occupancy equation with explicit graph volume."""
    v = graph_volume(t, params)
    return v * yield_rhs(t, y, contact_enhancement, params) + params.dilution_rate * v * y


def freezeout_threshold(contact_enhancement: float, params: GraphFreezeOutParams) -> float:
    """
    Native decoupling threshold on the graph clock.

    Define Gamma_ann = lambda_eff * Y.  Freeze-out begins when
    Gamma_ann ~ Gamma_dil, so the threshold yield is:

        Y_crit = Gamma_dil / lambda_eff.
    """
    lam = lambda_eff(contact_enhancement, params)
    if lam <= 0:
        return float("nan")
    return params.dilution_rate / lam


def graph_freezeout_time(contact_enhancement: float, params: GraphFreezeOutParams) -> float:
    """
    Solve lambda_eff * Y_eq(t_F) = Gamma_dil for the toy graph equilibrium.

    This is the strongest non-imported analogue of freeze-out onset:
    a graph-clock threshold. It is not yet the physical x_F.
    """
    lam = lambda_eff(contact_enhancement, params)
    if lam <= 0:
        return float("nan")
    ratio = lam * params.equilibrium_scale / params.dilution_rate
    if ratio <= 1.0:
        return float("inf")
    return math.log(ratio) / params.equilibrium_decay


def rk4_integrate(y0: float, t_grid: np.ndarray, contact_enhancement: float, params: GraphFreezeOutParams) -> np.ndarray:
    """Simple RK4 for the graph-native yield equation."""
    ys = np.zeros_like(t_grid)
    ys[0] = y0
    for i in range(len(t_grid) - 1):
        t = float(t_grid[i])
        dt = float(t_grid[i + 1] - t_grid[i])
        y = float(ys[i])
        k1 = yield_rhs(t, y, contact_enhancement, params)
        k2 = yield_rhs(t + 0.5 * dt, y + 0.5 * dt * k1, contact_enhancement, params)
        k3 = yield_rhs(t + 0.5 * dt, y + 0.5 * dt * k2, contact_enhancement, params)
        k4 = yield_rhs(t + dt, y + dt * k3, contact_enhancement, params)
        ys[i + 1] = max(0.0, y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4))
    return ys


def residual_check(t_grid: np.ndarray, ys: np.ndarray, contact_enhancement: float, params: GraphFreezeOutParams) -> float:
    """Measure the numerical residual of the derived master equation."""
    max_res = 0.0
    for i in range(1, len(t_grid) - 1):
        t = float(t_grid[i])
        dt = float(t_grid[i + 1] - t_grid[i - 1])
        dy_dt = (ys[i + 1] - ys[i - 1]) / dt
        lhs = dy_dt + params.dilution_rate * ys[i]
        rhs = -lambda_eff(contact_enhancement, params) * (
            ys[i] * ys[i] - graph_equilibrium_yield(t, params) ** 2
        )
        max_res = max(max_res, abs(lhs - rhs))
    return max_res


def main() -> None:
    params = GraphFreezeOutParams()

    log("=" * 78)
    log("GRAPH-NATIVE FREEZE-OUT")
    log("=" * 78)
    log()
    log("Status target:")
    log("  derive the graph-native master equation and decoupling criterion")
    log("  isolate exactly where physical cosmology enters")
    log()

    log("THEOREM 1: graph-volume dilution is exact")
    log("  Let Y(t) = N(t)/V(t). Then")
    log("    dY/dt + (d ln V/dt) Y = (1/V) dN/dt")
    log("  This is just the quotient rule, but it is the native replacement")
    log("  for the cosmological 3Hn term on a growing graph.")
    log()

    log("THEOREM 2: homogeneous pair-annihilation on a growing graph")
    log("  If the native master equation is")
    log("    dN/dt = -lambda_eff * V * (Y^2 - Y_eq^2)")
    log("  with lambda_eff = lambda_0 * S_contact, then")
    log("    dY/dt + Gamma_dil * Y = -lambda_eff * (Y^2 - Y_eq^2)")
    log("  where Gamma_dil = d ln V/dt.")
    log()

    log("Exact obstruction:")
    log("  the physical relic-abundance step still needs")
    log("    Gamma_dil -> 3H(t)")
    log("    graph equilibrium -> thermal equilibrium at temperature T")
    log("  Until those identifications are derived, this remains a graph-native")
    log("  freeze-out law, not the physical Omega_DM/Omega_b calculation.")
    log()

    contact_scan = [0.95, 1.00, 1.10, 1.25, 1.40]
    t_grid = np.linspace(0.0, 10.0, 4001)
    y0 = graph_equilibrium_yield(0.0, params)

    log("Graph-clock decoupling scan:")
    log(f"  dilution rate Gamma_dil = {params.dilution_rate:.4f} (graph units)")
    log(f"  equilibrium decay scale  = {params.equilibrium_decay:.4f}")
    log(f"  equilibrium scale Y_eq(0) = {params.equilibrium_scale:.4f}")
    log()
    log(f"  {'S_contact':>10s}  {'lambda_eff':>10s}  {'Y_crit':>10s}  {'t_F(graph)':>12s}  {'Y_inf':>10s}  {'residual':>10s}")
    log("  " + "-" * 72)

    for s_contact in contact_scan:
        lam = lambda_eff(s_contact, params)
        y_crit = freezeout_threshold(s_contact, params)
        t_f = graph_freezeout_time(s_contact, params)
        ys = rk4_integrate(y0, t_grid, s_contact, params)
        residual = residual_check(t_grid, ys, s_contact, params)
        y_inf = ys[-1]
        log(f"  {s_contact:10.2f}  {lam:10.4f}  {y_crit:10.4f}  {t_f:12.4f}  {y_inf:10.4f}  {residual:10.2e}")

    log("  " + "-" * 72)
    log()
    log("Interpretation:")
    log("  - S_contact only multiplies the annihilation kernel; it is the native")
    log("    contact-enhancement input from the lattice.")
    log("  - The graph-native freeze-out threshold is Y_crit = Gamma_dil / lambda_eff.")
    log("  - The graph-clock decoupling time t_F depends only logarithmically on")
    log("    S_contact through the equilibrium-surrogate scan.")
    log()

    log("What is still OPEN:")
    log("  - identifying graph growth with the physical Hubble rate 3H")
    log("  - identifying the graph equilibrium profile with thermal n_eq(T)")
    log("  - turning t_F(graph) into physical x_F = m/T_F")
    log("  - computing the physical relic abundance Omega_DM/Omega_b")
    log()

    log("What is SOLVED:")
    log("  - the graph-volume dilution term is exact")
    log("  - the homogeneous master equation on a growing graph is derived")
    log("  - the native decoupling criterion Gamma_ann ~ Gamma_dil is derived")
    log("  - the strongest non-imported piece is a graph-clock freeze-out law")
    log()

    log("=" * 78)
    log("SUMMARY")
    log("=" * 78)
    log("Solved: graph-native master equation + dilution identity + decoupling threshold")
    log("Open: physical Boltzmann/Friedmann map to x_F and relic abundance")
    log("=" * 78)

    try:
        import os
        os.makedirs("logs", exist_ok=True)
        with open(LOG_FILE, "w") as f:
            f.write("\n".join(results))
        log(f"\nLog saved to {LOG_FILE}")
    except Exception as e:
        log(f"\nCould not save log: {e}")


if __name__ == "__main__":
    main()
