#!/usr/bin/env python3
"""Level A: Fresh-ancilla collision model.

Abstract two-branch model with NO DAG complexity. Two branches (slit A
and slit B) undergo m sequential encounters with the mass region.
At each encounter, the system couples to a FRESH 2-state ancilla
(not reused, not shared between branches).

The key: fresh ancilla per encounter gives an EXTENSIVE record channel.
After m encounters, the env space is 2^m. If the coupling creates
different ancilla states for different branches, branch overlap decays
as γ^m where γ < 1.

Model:
  Branch A: system state |ψ_A⟩, encounters mass at angles θ_A1, θ_A2, ...
  Branch B: system state |ψ_B⟩, encounters mass at angles θ_B1, θ_B2, ...

  At encounter k:
    |ψ⟩|0_k⟩ → cos(α_k)|ψ⟩|0_k⟩ + sin(α_k)|ψ⟩|1_k⟩
    where α_k depends on the encounter angle (different for A vs B)

  Branch overlap after m encounters:
    ⟨Ψ_A|Ψ_B⟩ = ∏_k [cos(α_Ak)cos(α_Bk) + sin(α_Ak)sin(α_Bk)]
               = ∏_k cos(α_Ak - α_Bk)

  If α_Ak ≠ α_Bk at each encounter: overlap decays exponentially.

Success criterion: coherence (|overlap|²) decays with m.

PStack experiment: fresh-ancilla-collision-model
"""

from __future__ import annotations
import math
import cmath
import random
import sys


def branch_overlap_fresh_ancilla(m, delta_alphas):
    """Compute branch overlap after m encounters with fresh ancillas.

    delta_alphas[k] = α_Ak - α_Bk at encounter k.
    Overlap = ∏_k cos(delta_alpha_k)
    Coherence = |overlap|²
    """
    overlap = 1.0
    for k in range(m):
        overlap *= math.cos(delta_alphas[k])
    return overlap


def main():
    print("=" * 70)
    print("LEVEL A: FRESH-ANCILLA COLLISION MODEL")
    print("  Abstract two-branch model, no DAG")
    print("  Overlap = ∏_k cos(Δα_k), Coherence = |overlap|²")
    print("=" * 70)
    print()

    # ================================================================
    # Test 1: Fixed angle difference
    # ================================================================
    print("TEST 1: Fixed Δα per encounter")
    print(f"  {'Δα':>8s}  {'m=1':>8s}  {'m=3':>8s}  {'m=5':>8s}  "
          f"{'m=10':>8s}  {'m=20':>8s}  {'decay?':>7s}")
    print(f"  {'-' * 50}")

    for delta_deg in [5, 10, 15, 20, 30, 45, 60, 90]:
        delta = math.radians(delta_deg)
        coherences = {}
        for m in [1, 3, 5, 10, 20]:
            deltas = [delta] * m
            overlap = branch_overlap_fresh_ancilla(m, deltas)
            coherences[m] = overlap ** 2

        decays = coherences[20] < coherences[1] * 0.1
        print(f"  {delta_deg:7d}°  {coherences[1]:8.4f}  {coherences[3]:8.4f}  "
              f"{coherences[5]:8.4f}  {coherences[10]:8.4f}  {coherences[20]:8.4f}  "
              f"{'YES' if decays else 'no':>7s}")

    # ================================================================
    # Test 2: Random angle differences (simulating irregular graph)
    # ================================================================
    print()
    print("TEST 2: Random Δα per encounter (irregular graph analog)")
    print(f"  {'σ_Δα':>8s}  {'m=1':>8s}  {'m=5':>8s}  {'m=10':>8s}  "
          f"{'m=20':>8s}  {'m=50':>8s}  {'γ_eff':>7s}")
    print(f"  {'-' * 52}")

    for sigma_deg in [5, 10, 20, 30, 45]:
        sigma = math.radians(sigma_deg)
        rng = random.Random(42)
        n_trials = 100

        for m_max in [1, 5, 10, 20, 50]:
            coh_sum = 0
            for trial in range(n_trials):
                deltas = [rng.gauss(0, sigma) for _ in range(m_max)]
                overlap = branch_overlap_fresh_ancilla(m_max, deltas)
                coh_sum += overlap ** 2
            if m_max == 1:
                c1 = coh_sum / n_trials

        # Compute effective decay rate
        coherences = {}
        for m_max in [1, 5, 10, 20, 50]:
            coh_sum = 0
            rng = random.Random(42)
            for trial in range(n_trials):
                deltas = [rng.gauss(0, sigma) for _ in range(m_max)]
                overlap = branch_overlap_fresh_ancilla(m_max, deltas)
                coh_sum += overlap ** 2
            coherences[m_max] = coh_sum / n_trials

        # γ_eff = (coherence at m=50 / coherence at m=1) ^ (1/49)
        if coherences[1] > 0 and coherences[50] > 0:
            gamma = (coherences[50] / coherences[1]) ** (1.0/49)
        else:
            gamma = 0

        print(f"  {sigma_deg:7d}°  {coherences[1]:8.4f}  {coherences[5]:8.4f}  "
              f"{coherences[10]:8.4f}  {coherences[20]:8.4f}  {coherences[50]:8.4f}  "
              f"{gamma:7.4f}")

    # ================================================================
    # Test 3: Coherence vs encounter count (scaling check)
    # ================================================================
    print()
    print("TEST 3: Coherence vs m (exponential decay check)")
    print(f"  Δα = 20° fixed")
    print()

    delta = math.radians(20)
    print(f"  {'m':>4s}  {'coherence':>10s}  {'log(coh)':>10s}  {'γ^m fit':>10s}")
    print(f"  {'-' * 38}")

    gamma_theory = math.cos(delta) ** 2  # per-encounter decay
    for m in [1, 2, 3, 5, 8, 10, 15, 20, 30, 50]:
        deltas = [delta] * m
        overlap = branch_overlap_fresh_ancilla(m, deltas)
        coh = overlap ** 2
        log_coh = math.log(coh) if coh > 0 else float('-inf')
        gamma_m = gamma_theory ** m
        print(f"  {m:4d}  {coh:10.6f}  {log_coh:10.4f}  {gamma_m:10.6f}")

    print()
    print(f"  γ_theory = cos²(Δα) = {gamma_theory:.6f}")
    print(f"  Coherence should decay as γ^m = {gamma_theory:.4f}^m")
    print()

    # ================================================================
    # Summary
    # ================================================================
    print("=" * 70)
    print("LEVEL A RESULT")
    print("=" * 70)
    print()
    print("Fresh-ancilla collision model gives EXPONENTIAL coherence decay:")
    print(f"  coherence(m) = cos²(Δα)^m = γ^m")
    print(f"  where γ = cos²(Δα) < 1 whenever Δα ≠ 0")
    print()
    print("This is the standard repeated-interaction result.")
    print("The key property: FRESH ancilla per encounter prevents reconvergence.")
    print()
    print("For the full model:")
    print("  If each mass encounter couples to a fresh ancilla (indexed by")
    print("  encounter slot, not node id), and different branches have")
    print("  different Δα at each encounter, coherence decays with the")
    print("  number of encounters — which grows with graph size.")
    print()
    print("NEXT: Level B — feed real DAG interaction histories into this law.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
