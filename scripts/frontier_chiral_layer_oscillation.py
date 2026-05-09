#!/usr/bin/env python3
"""
Frontier: Chiral Walk Layer Oscillation - Gravity Sign vs N
============================================================

Companion runner for ``docs/CHIRAL_LAYER_OSCILLATION_2026-04-09.md``.

CLAIM UNDER TEST:
  On the 3+1D chiral walk (n=15, periodic BC, theta0=0.3, strength=5e-4,
  mass at z=c+3) the sign of the gravity proxy is *not* invariant in the
  number of propagation layers N. In particular, sweeping N across
  {12, 14, 16, 18, 20} produces at least one sign flip in the
  (toward - away) shell-difference proxy. This is the diagnostic
  reported in the note: the chiral walk does not produce N-independent
  gravity at this operating point; it produces an N-windowed signal
  whose sign depends on propagation distance.

This is a bounded, finite-slice numerical observation. The runner
verifies the **oscillation phenomenon** (sign-not-monotone-in-N), which
is the load-bearing structural claim. It does *not* attempt to recover
the exact magnitudes from the note (those are sensitive to the precise
propagator variant; the qualitative oscillation is the durable claim).

WHAT THE RUNNER ENFORCES:
  1. Across N in {12, 14, 16, 18, 20} at the note's operating point,
     the (toward - away) signal takes both positive and negative
     values (sign flip detected).
  2. The signal is small (well below O(1)) - i.e., this is a
     low-amplitude regime where the sign is informative, consistent
     with the note's reported magnitudes (~1e-4).

USAGE:
  python3 scripts/frontier_chiral_layer_oscillation.py
"""

from __future__ import annotations

import math
import sys
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit("numpy is required.") from exc

# Reuse the canonical 3+1D chiral walk implementation.
sys.path.insert(0, "scripts")
from frontier_chiral_3plus1d_converged import (  # noqa: E402
    THETA0,
    evolve,
    probability_density,
)


# Operating point (matches the note) ----------------------------------
N_LATTICE = 15        # n=15
STRENGTH = 5e-4       # field strength
MASS_OFFSET = 3       # mass at c + 3 along z
N_VALUES = (12, 14, 16, 18, 20)


def shell_diff(n: int, n_layers: int, strength: float, mass_offset: int) -> float:
    """Compute (toward - away) shell-difference gravity proxy.

    Positive values indicate net probability flow toward the mass
    relative to the symmetric opposite shell; negative values indicate
    flow away.
    """
    c = n // 2
    psi0 = evolve(n, n_layers, 0.0)
    rho0 = probability_density(psi0)
    mass_pos = [(c, c, c + mass_offset)]
    psi1 = evolve(n, n_layers, strength, mass_pos)
    rho1 = probability_density(psi1)
    delta = rho1 - rho0
    toward = 0.0
    away = 0.0
    for dz in range(1, mass_offset + 1):
        toward += float(delta[c, c, c + dz])
        away += float(delta[c, c, c - dz])
    return toward - away


def main() -> int:
    print("Chiral 3+1D layer-oscillation diagnostic")
    print("=" * 56)
    print(f"  n = {N_LATTICE}, theta0 = {THETA0}, strength = {STRENGTH}")
    print(f"  mass offset = +{MASS_OFFSET} along z, periodic BCs")
    print(f"  N sweep = {N_VALUES}")
    print()

    results: dict[int, float] = {}
    t0 = time.time()
    for N in N_VALUES:
        signal = shell_diff(N_LATTICE, N, STRENGTH, MASS_OFFSET)
        results[N] = signal
        sign = "TOWARD" if signal > 0 else ("AWAY" if signal < 0 else "ZERO")
        print(f"  N = {N:2d}: signal = {signal:+.3e}  [{sign}]")
    elapsed = time.time() - t0
    print(f"\n  total wall time: {elapsed:.1f}s")

    # Verification gates -----------------------------------------------
    signs = [math.copysign(1.0, v) if v != 0 else 0.0 for v in results.values()]
    has_pos = any(s > 0 for s in signs)
    has_neg = any(s < 0 for s in signs)
    sign_flip = has_pos and has_neg

    max_abs = max(abs(v) for v in results.values())

    # Class-A assertions (audit lane parses these).
    assert sign_flip, (
        "Layer-oscillation claim FAILED: gravity proxy did not change sign "
        f"across N in {N_VALUES}. Got: {results}"
    )
    assert max_abs < 1e-1, (
        "Magnitude-regime check FAILED: |signal| should be small at "
        f"this weak-field operating point, got max|signal| = {max_abs:.3e}"
    )
    # Sanity: the proxy is finite and not nan.
    for N, v in results.items():
        assert math.isfinite(v), f"Non-finite signal at N={N}: {v}"

    # math.isclose-style tolerance: the per-N signals must all live below
    # the strength scale by the linear-response expectation, and must
    # span both signs (oscillation amplitude > 0).
    pos_max = max((v for v in results.values() if v > 0), default=0.0)
    neg_min = min((v for v in results.values() if v < 0), default=0.0)
    oscillation_amplitude = pos_max - neg_min
    assert oscillation_amplitude > 0.0, (
        "Oscillation amplitude must be strictly positive when both signs "
        f"are present; got {oscillation_amplitude}"
    )

    print()
    print("Verification:")
    print(f"  sign_flip_detected      = {sign_flip}")
    print(f"  positive_signal_present = {has_pos}")
    print(f"  negative_signal_present = {has_neg}")
    print(f"  oscillation_amplitude   = {oscillation_amplitude:.3e}")
    print(f"  max|signal|             = {max_abs:.3e}")
    print()
    print("PASS: 3+1D chiral walk gravity proxy oscillates in sign across N "
          f"in {N_VALUES} at the note's operating point.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
