#!/usr/bin/env python3
"""
Frontier experiment: wave-particle transition under continuous decoherence.

HYPOTHESIS: There is a sharp transition from wave to particle behavior
            at a critical decoherence coupling.
FALSIFICATION: If visibility V decreases linearly with mixing parameter alpha,
               the transition is gradual (no critical point).

Physics: The model produces interference (wave) when no which-path record
exists, and decoherence (particle) when which-path records are created.
We interpolate between these two regimes with a mixing parameter alpha in [0,1]:

    P(y, alpha) = (1 - alpha) * P_interference(y) + alpha * P_whichpath(y)

and measure:
    - Visibility:  V = (P_max - P_min) / (P_max + P_min)  in the central region
    - Coherent visibility: V_coh = (V - V_particle) / (1 - V_particle)
      subtracts the incoherent (single-slit diffraction) baseline
    - Complementarity: V_coh^2 + alpha^2 <= 1  (Englert relation)
"""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from toy_event_physics import two_slit_distribution


def compute_visibility(distribution: dict[int, float], center_half_width: int = 4) -> float:
    """Visibility V = (P_max - P_min) / (P_max + P_min) in the central region."""
    central = {y: p for y, p in distribution.items() if abs(y) <= center_half_width}
    if not central:
        return 0.0
    p_max = max(central.values())
    p_min = min(central.values())
    if p_max + p_min == 0:
        return 0.0
    return (p_max - p_min) / (p_max + p_min)


def run_experiment():
    screen_positions = list(range(-10, 11))

    print("=" * 70)
    print("FRONTIER: Wave-Particle Transition Under Continuous Decoherence")
    print("=" * 70)

    # Step 1: Get the two endpoint distributions
    print("\n[1] Computing interference pattern (alpha=0, no which-path info)...")
    p_wave = two_slit_distribution(
        screen_positions=screen_positions,
        record_created=False,
    )

    print("[2] Computing which-path pattern (alpha=1, full decoherence)...")
    p_particle = two_slit_distribution(
        screen_positions=screen_positions,
        record_created=True,
    )

    # Step 2: Compute endpoint visibilities
    v_wave = compute_visibility(p_wave)
    v_particle = compute_visibility(p_particle)

    print(f"\n  V(wave)     = {v_wave:.4f}  (interference pattern)")
    print(f"  V(particle) = {v_particle:.4f}  (which-path pattern)")
    print(f"  V_drop_max  = {v_wave - v_particle:.4f}")

    # The particle pattern retains single-slit diffraction visibility.
    # To get the COHERENT visibility (interference-only fringes), subtract baseline:
    #   V_coh(alpha) = [V(alpha) - V_particle] / [1 - V_particle]
    # This is 1 at alpha=0 and 0 at alpha=1.

    # Step 3: Sweep alpha from 0 to 1
    alpha_values = [0.0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5,
                    0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0]

    print("\n[3] Sweeping decoherence parameter alpha from 0 to 1...")
    print(f"{'alpha':>8s} {'V_obs':>8s} {'V_coh':>8s} {'V_coh^2+a^2':>12s} {'status':>10s}")
    print("-" * 52)

    results = []
    for alpha in alpha_values:
        # Mixed distribution
        p_mixed = {}
        for y in screen_positions:
            p_mixed[y] = (1 - alpha) * p_wave[y] + alpha * p_particle[y]

        # Renormalize
        total = sum(p_mixed.values())
        if total > 0:
            p_mixed = {y: p / total for y, p in p_mixed.items()}

        v_obs = compute_visibility(p_mixed)

        # Coherent visibility: subtract the incoherent baseline
        if v_particle < 1.0:
            v_coh = (v_obs - v_particle) / (1.0 - v_particle)
        else:
            v_coh = 0.0
        v_coh = max(0.0, v_coh)

        # Englert complementarity: V_coh^2 + D^2 <= 1
        # For our mixing model, the which-path detector has distinguishability = alpha
        # (it provides correct slit label with reliability alpha for symmetric slits)
        complement = v_coh**2 + alpha**2
        status = "OK" if complement <= 1.0 + 1e-9 else "VIOLATION"

        results.append((alpha, v_obs, v_coh, complement))
        print(f"{alpha:8.3f} {v_obs:8.4f} {v_coh:8.4f} {complement:12.4f} {status:>10s}")

    # Step 4: Check for sharp vs gradual transition
    print("\n" + "=" * 70)
    print("ANALYSIS: Sharp vs Gradual Transition")
    print("=" * 70)

    # Check linearity of V_coh(alpha) using actual endpoints
    v_coh_start = results[0][2]
    v_coh_end = results[-1][2]

    max_deviation = 0.0
    max_dev_alpha = 0.0
    for alpha, v_obs, v_coh, c in results:
        # Linear interpolation between actual endpoints
        v_linear = v_coh_start + (v_coh_end - v_coh_start) * alpha
        deviation = abs(v_coh - v_linear)
        if deviation > max_deviation:
            max_deviation = deviation
            max_dev_alpha = alpha

    print(f"\nCoherent visibility V_coh(alpha):")
    print(f"  V_coh(0) = {v_coh_start:.4f},  V_coh(1) = {v_coh_end:.4f}")
    print(f"  Linear reference: V_coh = {v_coh_start:.4f} * (1 - alpha)")
    print(f"  Max deviation from linear: {max_deviation:.6f} at alpha={max_dev_alpha:.3f}")
    print(f"  Relative deviation: {max_deviation / v_coh_start:.4f} ({max_deviation / v_coh_start * 100:.1f}%)")

    # Check if sqrt relationship holds: V_coh = V_coh(0) * sqrt(1 - alpha^2)
    # This would indicate V_coh^2 + alpha^2 = const (circle in V-D space)
    max_sqrt_dev = 0.0
    for alpha, v_obs, v_coh, c in results:
        v_sqrt = v_coh_start * math.sqrt(max(0, 1.0 - alpha**2))
        sqrt_dev = abs(v_coh - v_sqrt)
        if sqrt_dev > max_sqrt_dev:
            max_sqrt_dev = sqrt_dev

    print(f"\n  Circular reference: V_coh = {v_coh_start:.4f} * sqrt(1 - alpha^2)")
    print(f"  Max deviation from circular: {max_sqrt_dev:.6f}")

    is_linear = max_deviation / v_coh_start < 0.05  # less than 5% relative deviation
    is_circular = max_sqrt_dev / v_coh_start < 0.05
    if is_linear:
        print(f"\n  Transition type: GRADUAL (linear in V_coh)")
    elif is_circular:
        print(f"\n  Transition type: CIRCULAR (V_coh^2 + alpha^2 = const)")
    else:
        print(f"\n  Transition type: NONLINEAR (neither linear nor circular)")

    # Step 5: Check complementarity bound
    print("\n" + "=" * 70)
    print("COMPLEMENTARITY CHECK: V_coh^2 + alpha^2 <= 1")
    print("=" * 70)

    all_satisfy = all(c <= 1.0 + 1e-9 for _, _, _, c in results)
    max_complement = max(c for _, _, _, c in results)
    print(f"  All points satisfy bound: {all_satisfy}")
    print(f"  Maximum V_coh^2 + alpha^2 = {max_complement:.6f}")

    # Step 6: Hypothesis verdict
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    if is_linear:
        print("HYPOTHESIS FALSIFIED: The transition is gradual (linear).")
        print("Coherent visibility V_coh decreases linearly with alpha.")
        print("There is no critical coupling -- wave behavior smoothly gives way")
        print("to particle behavior as which-path information increases.")
    else:
        print("HYPOTHESIS NOT CLEARLY FALSIFIED: The transition shows nonlinear character.")
        print(f"Max deviation from linearity: {max_deviation:.6f}")

    if all_satisfy:
        print("\nComplementarity V_coh^2 + alpha^2 <= 1 HOLDS at all points.")
        print("The model respects Englert wave-particle duality.")
    else:
        print("\nWARNING: Complementarity bound VIOLATED at some points!")
        print("This may indicate the coherent visibility extraction is imperfect.")

    # Step 7: Print distributions at endpoints for inspection
    print("\n" + "=" * 70)
    print("ENDPOINT DISTRIBUTIONS")
    print("=" * 70)
    print(f"{'y':>4s} {'P_wave':>10s} {'P_particle':>12s} {'diff':>10s}")
    print("-" * 40)
    for y in screen_positions:
        pw = p_wave.get(y, 0)
        pp = p_particle.get(y, 0)
        print(f"{y:4d} {pw:10.6f} {pp:12.6f} {pw - pp:10.6f}")

    # Step 8: Plot
    print("\n" + "=" * 70)
    print("GENERATING PLOTS")
    print("=" * 70)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(16, 5))

        # Panel 1: Interference patterns at select alpha values
        ax1 = axes[0]
        highlight_alphas = [0.0, 0.2, 0.5, 0.8, 1.0]
        for alpha in highlight_alphas:
            p_mixed = {}
            for y in screen_positions:
                p_mixed[y] = (1 - alpha) * p_wave[y] + alpha * p_particle[y]
            total = sum(p_mixed.values())
            if total > 0:
                p_mixed = {y: p / total for y, p in p_mixed.items()}
            ys = sorted(p_mixed.keys())
            ps = [p_mixed[y] for y in ys]
            ax1.plot(ys, ps, "o-", label=f"alpha={alpha:.1f}", markersize=3)
        ax1.set_xlabel("Screen position y")
        ax1.set_ylabel("P(y)")
        ax1.set_title("Distribution vs decoherence")
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        # Panel 2: V_coh and alpha vs alpha
        ax2 = axes[1]
        alphas = [r[0] for r in results]
        v_cohs = [r[2] for r in results]
        ax2.plot(alphas, v_cohs, "bo-", label="V_coh (coherent visibility)", markersize=5)
        ax2.plot([0, 1], [1, 0], "b--", alpha=0.3, label="Linear: 1 - alpha")
        ax2.plot(alphas, alphas, "rs-", label="D = alpha", markersize=5)
        ax2.set_xlabel("Decoherence parameter alpha")
        ax2.set_ylabel("V_coh, D")
        ax2.set_title("Wave-particle transition")
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(-0.05, 1.05)
        ax2.set_ylim(-0.05, 1.05)

        # Panel 3: Complementarity V_coh^2 + alpha^2
        ax3 = axes[2]
        complements = [r[3] for r in results]
        ax3.plot(alphas, complements, "go-", label="V_coh^2 + alpha^2", markersize=5)
        ax3.axhline(y=1.0, color="r", linestyle="--", label="Bound = 1")
        ax3.fill_between(alphas, complements, 1.0,
                         where=[c <= 1.0 for c in complements],
                         alpha=0.1, color="green")
        ax3.set_xlabel("Decoherence parameter alpha")
        ax3.set_ylabel("V_coh^2 + alpha^2")
        ax3.set_title("Complementarity bound")
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(-0.05, 1.05)
        ax3.set_ylim(0, 1.2)

        plt.tight_layout()
        out_path = os.path.join(os.path.dirname(__file__), "frontier_wave_particle_transition.png")
        plt.savefig(out_path, dpi=150)
        print(f"Plot saved to {out_path}")

    except ImportError:
        print("matplotlib not available -- skipping plot generation.")

    # Step 9: Result card
    print("\n" + "=" * 70)
    print("RESULT CARD")
    print("=" * 70)
    print(f"  V_obs at alpha=0 (pure wave):       {v_wave:.4f}")
    print(f"  V_obs at alpha=1 (pure particle):    {v_particle:.4f}")
    v_coh_0 = results[0][2]
    v_coh_1 = results[-1][2]
    print(f"  V_coh at alpha=0:                    {v_coh_0:.4f}")
    print(f"  V_coh at alpha=1:                    {v_coh_1:.4f}")
    print(f"  Max deviation from linearity:        {max_deviation:.6f}")
    print(f"  Transition type:                     {'Gradual' if is_linear else 'Nonlinear'}")
    print(f"  Complementarity bound satisfied:     {all_satisfy}")
    print(f"  Max V_coh^2 + alpha^2:               {max_complement:.6f}")


if __name__ == "__main__":
    run_experiment()
