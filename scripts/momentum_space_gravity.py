#!/usr/bin/env python3
"""Momentum-space characterization of gravitational deflection.

The centroid shift saturates and the ray slope oscillates. A Fourier/
angular decomposition should give a cleaner signal.

For each detector column x, the probability distribution P(y) can be
Fourier-transformed to get P(ky). The gravitational effect should
shift the peak of |P(ky)|² to nonzero ky — this is the deflection
in momentum space.

Also: compute the probability current (phase gradient × probability)
to get the local flow direction, which is the "velocity" of the
amplitude distribution at each point.

PStack experiment: momentum-space-gravity
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates, build_rectangular_nodes, derive_local_rule,
    derive_node_field, infer_arrival_times_from_source, build_causal_dag,
)


def propagate_geom_full(nodes, source, node_field, phase_k, atten_power):
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival)
    order = sorted(arrival, key=arrival.get)

    amps = {source: 1.0+0.0j}
    for node in order:
        if node not in amps:
            continue
        a = amps[node]
        for nb in dag.get(node, []):
            L = math.dist(node, nb)
            lf = 0.5*(node_field.get(node, 0.0)+node_field.get(nb, 0.0))
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl-ret
            ea = cmath.exp(1j*phase_k*act)/(L**atten_power)
            if nb not in amps:
                amps[nb] = 0.0+0.0j
            amps[nb] += a*ea
    return amps


def fourier_transform_y(amps, x, screen_ys):
    """DFT of amplitude ψ(y) at fixed x → ψ(ky)."""
    N = len(screen_ys)
    psi = [amps.get((x, y), 0.0+0.0j) for y in screen_ys]
    # DFT
    ft = []
    for n in range(N):
        s = sum(psi[m]*cmath.exp(-2j*math.pi*m*n/N) for m in range(N))
        ft.append(s)
    return ft


def prob_centroid_ky(ft, N):
    """Probability-weighted mean ky index from Fourier amplitudes."""
    probs = [abs(f)**2 for f in ft]
    total = sum(probs)
    if total == 0:
        return 0.0
    # Map indices to ky: index n → ky = 2π*n/N (shifted to [-π, π])
    centroid = 0
    for n, p in enumerate(probs):
        ky = n if n <= N//2 else n - N
        centroid += ky * p
    return centroid / total


def probability_current_y(amps, x, screen_ys):
    """y-component of probability current J_y = Im(ψ* ∂ψ/∂y) at fixed x."""
    currents = []
    for i, y in enumerate(screen_ys):
        psi = amps.get((x, y), 0.0+0.0j)
        if i < len(screen_ys)-1:
            psi_next = amps.get((x, screen_ys[i+1]), 0.0+0.0j)
            dpsi_dy = psi_next - psi  # finite difference
        else:
            dpsi_dy = 0.0+0.0j
        j_y = (psi.conjugate() * dpsi_dy).imag
        currents.append(j_y)
    return currents


def main():
    width = 60
    height = 25
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height+1))
    free_field = {n: 0.0 for n in nodes}

    mass_mn = frozenset((30, y) for y in range(4, 9))
    postulates = RulePostulates(phase_per_action=2.0, attenuation_power=1.0)
    mass_rule = derive_local_rule(persistent_nodes=mass_mn, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)

    print("=" * 70)
    print("MOMENTUM-SPACE GRAVITY CHARACTERIZATION")
    print(f"  Grid: {width}x{2*height+1}, k=2.0, 1/L^p propagator")
    print(f"  Mass at x=30, y=4..8")
    print("=" * 70)
    print()

    free_amps = propagate_geom_full(nodes, source, free_field, 2.0, 1.0)
    mass_amps = propagate_geom_full(nodes, source, mass_field, 2.0, 1.0)

    # ================================================================
    # TEST 1: ky centroid at each detector x
    # ================================================================
    print("TEST 1: Momentum centroid ky vs detector x")
    print()

    N = len(screen_ys)
    print(f"  {'x':>4s}  {'ky_free':>10s}  {'ky_mass':>10s}  {'Δky':>10s}  {'region':>10s}")
    print(f"  {'-' * 48}")

    for x in range(5, width+1, 5):
        ft_free = fourier_transform_y(free_amps, x, screen_ys)
        ft_mass = fourier_transform_y(mass_amps, x, screen_ys)
        ky_free = prob_centroid_ky(ft_free, N)
        ky_mass = prob_centroid_ky(ft_mass, N)
        dky = ky_mass - ky_free
        region = "before" if x < 25 else "near" if x < 35 else "after"
        print(f"  {x:4d}  {ky_free:+10.4f}  {ky_mass:+10.4f}  {dky:+10.4f}  {region:>10s}")

    # ================================================================
    # TEST 2: Probability current J_y at beam center
    # ================================================================
    print()
    print("TEST 2: Probability current J_y (flow direction)")
    print("  Positive J_y = flow toward mass (y>0)")
    print()

    print(f"  {'x':>4s}  {'J_free_net':>12s}  {'J_mass_net':>12s}  {'ΔJ':>12s}  {'toward?':>8s}")
    print(f"  {'-' * 52}")

    for x in range(5, width+1, 5):
        j_free = probability_current_y(free_amps, x, screen_ys)
        j_mass = probability_current_y(mass_amps, x, screen_ys)

        # Net current (sum over y)
        net_free = sum(j_free)
        net_mass = sum(j_mass)
        dj = net_mass - net_free
        toward = "YES" if dj > 0 else "no"
        print(f"  {x:4d}  {net_free:+12.4e}  {net_mass:+12.4e}  {dj:+12.4e}  {toward:>8s}")

    # ================================================================
    # TEST 3: Does Δky stabilize downstream?
    # ================================================================
    print()
    print("TEST 3: Δky (momentum deflection) at fine x resolution past mass")
    print()

    print(f"  {'x':>4s}  {'Δky':>10s}")
    print(f"  {'-' * 18}")

    for x in range(32, 56):
        ft_f = fourier_transform_y(free_amps, x, screen_ys)
        ft_m = fourier_transform_y(mass_amps, x, screen_ys)
        dky = prob_centroid_ky(ft_m, N) - prob_centroid_ky(ft_f, N)
        print(f"  {x:4d}  {dky:+10.4f}")

    # ================================================================
    # TEST 4: Impact parameter dependence of Δky
    # ================================================================
    print()
    print("TEST 4: Δky vs impact parameter b (at x=45)")
    print()

    print(f"  {'b':>4s}  {'Δky':>10s}  {'Δky×b':>10s}")
    print(f"  {'-' * 28}")

    for b in [2, 4, 6, 8, 10, 12, 15, 18, 20]:
        mn = frozenset((30, y) for y in range(b-1, b+2))
        mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
        mf = derive_node_field(nodes, mr)
        m_amps = propagate_geom_full(nodes, source, mf, 2.0, 1.0)

        ft_f = fourier_transform_y(free_amps, 45, screen_ys)
        ft_m = fourier_transform_y(m_amps, 45, screen_ys)
        dky = prob_centroid_ky(ft_m, N) - prob_centroid_ky(ft_f, N)
        print(f"  {b:4d}  {dky:+10.4f}  {dky*b:+10.3f}")

    print()
    print("If Δky stabilizes downstream → well-defined momentum deflection")
    print("If Δky×b = constant → 1/b scaling of deflection angle")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
