#!/usr/bin/env python3
"""Analytical prediction for the k-oscillation period in lensing slope.

The k-sweep showed slope oscillates with period ~1.5 in k·H.
Can we predict this from the propagator structure?

MODEL: The Kubo coefficient is proportional to the imaginary part
of a path integral. The dominant contribution comes from paths near
the mass (at x_src). Each path accumulates phase k·L_total where
L_total depends on the path's angle.

For the SLOPE (power-law exponent), what oscillates is the relative
contribution of paths at different impact parameters b. Paths at
smaller b pass closer to the mass, accumulate more field-induced phase,
and therefore oscillate faster with k than paths at larger b.

The key quantity is the field-induced phase shift at impact parameter b:
  δφ(b) = k · Σ_edges (L · f) ≈ k · H · N_eff · <f>

where <f> ≈ s/(b·ε_eff) is the average field over the ~N_eff edges
near the mass.

The SLOPE oscillates when the RELATIVE phase between b=3 and b=6
changes by π:
  Δ(δφ) = k · H · N_eff · s · (1/3 - 1/6) / ε_eff ≈ k · H · stuff

Let's compute this numerically for the actual configuration.
"""

from __future__ import annotations
import math


def main():
    H = 0.25
    NL = 61  # int(15/0.25) + 1
    x_src = 5.0  # NL//3 * H = 20 * 0.25
    beta = 0.8
    sigma_theta = 1.0 / math.sqrt(2 * beta)

    print("=" * 70)
    print("ANALYTICAL k-OSCILLATION PREDICTION")
    print(f"  H={H}, NL={NL}, x_src={x_src}, β={beta}")
    print(f"  σ_θ = {sigma_theta:.3f} rad ({math.degrees(sigma_theta):.1f}°)")
    print("=" * 70)

    # MODEL 1: Single-edge phase difference
    # Paths at angle θ have edge length L = H/cos(θ)
    # Phase per edge: k·H/cos(θ) vs k·H (straight)
    # Δφ per edge = k·H·(sec(θ)-1)
    sec_theta = 1.0 / math.cos(sigma_theta)
    delta_per_edge = sec_theta - 1
    print(f"\n  MODEL 1: Single-edge geometric phase")
    print(f"    sec(σ_θ) - 1 = {delta_per_edge:.4f}")
    print(f"    Total over {NL} layers: N·H·(sec(θ)-1) = {NL * H * delta_per_edge:.2f}")
    print(f"    Period: Δ(k·H) = 2π / (N·(sec(θ)-1)) = {2*math.pi / (NL * delta_per_edge):.4f}")
    print(f"    → Too fast (predicts {2*math.pi / (NL * delta_per_edge):.2f}, observed ~1.5)")

    # MODEL 2: Field-induced phase at the mass location
    # The Kubo coefficient involves the derivative damp/ds.
    # dphi/ds = -i·k·L/r at each edge near the mass.
    # The total field-induced phase over edges near the mass is:
    #   δφ(b) ≈ k · Σ (H/cos(θ)) / r(b)
    # For edges at x near x_src, r ≈ b (impact parameter).
    # The sum has ~1/σ_θ "contributing" edges (those within angle σ_θ).
    # But actually, the field extends over many layers.

    # Effective number of layers "near" the mass:
    # The field f = s/r falls off as 1/r from the mass.
    # Significant contribution from layers where |x - x_src| < b.
    # For b=3: N_eff ≈ 2·b/H = 24 layers
    # For b=6: N_eff ≈ 2·b/H = 48 layers

    print(f"\n  MODEL 2: Field-induced phase")
    for b in [3.0, 4.0, 5.0, 6.0]:
        # Field-induced phase: sum of k·H·f over layers near mass
        # f ≈ s / √((x-x_src)² + b²) at each layer
        total_phase = 0.0
        for layer in range(NL):
            x = layer * H
            r = math.sqrt((x - x_src)**2 + b**2) + 0.1
            # Phase contribution from this layer (forward edge)
            total_phase += H / r  # ∝ k·H·(H/r), the k is factored out
        print(f"    b={b:.0f}: Σ(H/r) = {total_phase:.4f}  (× k gives total field phase)")

    # The Kubo slope depends on how kubo(b) ∝ b^α varies with k.
    # kubo(b) ∝ Im[Σ_paths exp(i·k·L_path) · (field derivative)]
    # The field derivative at b: ∂/∂s [exp(i·k·L·f)] = i·k·L/r · exp(i·k·L·f)
    # So kubo ∝ k · Σ (H/r) · exp(i·k·Σ(Lf))
    # The oscillation in the SLOPE comes from the b-dependent phase:
    #   φ_field(b) = k · Σ_layers H·f(b) = k · Σ H/(√((x-x_src)²+b²)+0.1)

    # Compute the phase difference between b=3 and b=6:
    phase_3 = sum(H / (math.sqrt((l*H - x_src)**2 + 9) + 0.1) for l in range(NL))
    phase_6 = sum(H / (math.sqrt((l*H - x_src)**2 + 36) + 0.1) for l in range(NL))
    delta_phase = phase_3 - phase_6

    print(f"\n  Field phase sums:")
    print(f"    Σ(H/r) at b=3: {phase_3:.4f}")
    print(f"    Σ(H/r) at b=6: {phase_6:.4f}")
    print(f"    Difference: {delta_phase:.4f}")
    print(f"    → When k · {delta_phase:.4f} shifts by π, the slope oscillates")
    print(f"    → Predicted period: Δk = π/{delta_phase:.4f} = {math.pi/delta_phase:.2f}")
    print(f"    → In k·H units: Δ(k·H) = {math.pi/delta_phase * H:.4f}")

    # MODEL 3: Direct computation using actual k values
    # At each k, compute the phase of Σ exp(i·k·Σ_field(b)) for b=3 and b=6
    # and see when they go in/out of phase
    print(f"\n  MODEL 3: Phase tracking vs k·H")
    print(f"  {'k·H':>6s}  {'φ(b=3)':>10s}  {'φ(b=6)':>10s}  {'Δφ':>10s}  {'cos(Δφ)':>10s}")
    print(f"  {'-'*55}")

    for kH in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
        k = kH / H
        p3 = k * phase_3
        p6 = k * phase_6
        dp = p3 - p6
        # Wrap to [-π, π]
        dp_wrapped = dp % (2 * math.pi)
        if dp_wrapped > math.pi:
            dp_wrapped -= 2 * math.pi
        print(f"  {kH:6.1f}  {p3 % (2*math.pi):10.3f}  {p6 % (2*math.pi):10.3f}  "
              f"{dp_wrapped:10.3f}  {math.cos(dp_wrapped):10.3f}")

    # Summary
    print(f"\n{'=' * 70}")
    print("PREDICTED vs OBSERVED")
    print("=" * 70)
    print(f"  Model 1 (geometric phase): period = {2*math.pi / (NL * delta_per_edge):.2f} in k·H → too fast")
    print(f"  Model 2 (field phase diff): period = {math.pi/delta_phase * H:.2f} in k·H")
    print(f"  Observed: period ≈ 1.5 in k·H")
    predicted = math.pi / delta_phase * H
    if abs(predicted - 1.5) < 0.3:
        print(f"  → Model 2 MATCHES (predicted {predicted:.2f} vs observed ~1.5)")
    else:
        print(f"  → Model 2 gives {predicted:.2f}, observed ~1.5 (off by {abs(predicted-1.5):.2f})")

    # Also compute for general b pairs
    print(f"\n  Period for different b-pair contrasts:")
    for b1, b2 in [(3, 4), (3, 5), (3, 6), (4, 6)]:
        p1 = sum(H / (math.sqrt((l*H - x_src)**2 + b1**2) + 0.1) for l in range(NL))
        p2 = sum(H / (math.sqrt((l*H - x_src)**2 + b2**2) + 0.1) for l in range(NL))
        dp = p1 - p2
        period = math.pi / dp * H if dp > 0 else float('inf')
        print(f"    b={b1} vs b={b2}: ΔΣ(H/r) = {dp:.4f}, period = {period:.3f} in k·H")


if __name__ == "__main__":
    main()
