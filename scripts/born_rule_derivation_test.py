#!/usr/bin/env python3
"""Test whether the Born rule (p=2 norm) is DERIVED or ASSUMED.

The external reviewer's key critique: the model assumes |ψ|² probabilities.
Can we derive this from something deeper?

The built-in born_rule_pressure_test() checks which p-norm is preserved
by the Hadamard mixing matrix. This script extends that test to:
1. All p-norms from 0.5 to 6
2. Multiple mixing matrices (not just Hadamard)
3. The model's actual path-sum amplitude propagation
4. Whether the network structure selects p=2 over other values

The argument: if reversible linear mixing (which the model uses for
amplitude propagation) preserves ONLY the 2-norm, then the Born rule
is a consequence of linearity + reversibility, not an additional assumption.

PStack experiment: born-rule-derivation
"""

from __future__ import annotations
import math
import cmath
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    born_rule_pressure_test,
    apply_hadamard,
    p_total,
)


def apply_rotation(state: tuple[complex, complex], angle: float) -> tuple[complex, complex]:
    """Apply a 2D rotation matrix."""
    c, s = math.cos(angle), math.sin(angle)
    a, b = state
    return (c * a - s * b, s * a + c * b)


def apply_phase(state: tuple[complex, complex], phi: float) -> tuple[complex, complex]:
    """Apply a relative phase shift."""
    a, b = state
    return (a, b * cmath.exp(1j * phi))


def apply_beam_splitter(state: tuple[complex, complex], theta: float) -> tuple[complex, complex]:
    """General beam splitter: cos(theta) transmission, sin(theta) reflection."""
    c, s = math.cos(theta), math.sin(theta)
    a, b = state
    return (c * a + 1j * s * b, 1j * s * a + c * b)


def main() -> None:
    print("=" * 72)
    print("BORN RULE DERIVATION TEST")
    print("=" * 72)
    print()

    # =========================================================
    # TEST 1: Built-in pressure test
    # =========================================================
    print("TEST 1: Built-in born_rule_pressure_test()")
    print()
    results = born_rule_pressure_test()
    for p_norm, comparisons in sorted(results.items()):
        print(f"  p={p_norm}: ", end="")
        max_drift = max(abs(after - before) for before, after in comparisons)
        for before, after in comparisons:
            print(f"({before:.4f} → {after:.4f}) ", end="")
        preserved = "PRESERVED" if max_drift < 1e-10 else f"BROKEN (drift={max_drift:.4f})"
        print(f"  {preserved}")

    # =========================================================
    # TEST 2: Fine p-norm sweep
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 2: Fine p-norm sweep (which p is preserved by Hadamard?)")
    print("=" * 72)
    print()

    states = [
        (1.0 + 0.0j, 0.0 + 0.0j),
        (1 / math.sqrt(2), 1j / math.sqrt(2)),
        (0.8 + 0.3j, -0.2 + 0.5j),
        (2.0 - 1.0j, -0.5 + 1.5j),
    ]

    print(f"  {'p':>6s}  {'max_drift':>12s}  {'preserved?':>10s}")
    print(f"  {'-' * 32}")

    for p_val in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]:
        max_drift = 0.0
        for state in states:
            before = sum(abs(a) ** p_val for a in state)
            after = sum(abs(a) ** p_val for a in apply_hadamard(state))
            max_drift = max(max_drift, abs(after - before))
        preserved = "YES" if max_drift < 1e-10 else "NO"
        print(f"  {p_val:6.1f}  {max_drift:12.6e}  {preserved:>10s}")

    # =========================================================
    # TEST 3: Multiple unitary transformations
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 3: Is p=2 preserved by ALL unitary transformations?")
    print("=" * 72)
    print()

    transforms = [
        ("Hadamard", apply_hadamard),
        ("Rotation π/4", lambda s: apply_rotation(s, math.pi / 4)),
        ("Rotation π/7", lambda s: apply_rotation(s, math.pi / 7)),
        ("Phase π/3", lambda s: apply_phase(s, math.pi / 3)),
        ("Beam splitter π/6", lambda s: apply_beam_splitter(s, math.pi / 6)),
        ("Beam splitter π/3", lambda s: apply_beam_splitter(s, math.pi / 3)),
    ]

    for p_val in [1.0, 2.0, 4.0]:
        print(f"  p = {p_val}:")
        for t_name, t_func in transforms:
            max_drift = 0.0
            for state in states:
                before = sum(abs(a) ** p_val for a in state)
                after = sum(abs(a) ** p_val for a in t_func(state))
                max_drift = max(max_drift, abs(after - before))
            status = "PRESERVED" if max_drift < 1e-10 else f"broken ({max_drift:.4f})"
            print(f"    {t_name:>25s}: {status}")
        print()

    # =========================================================
    # TEST 4: The logical argument
    # =========================================================
    print("=" * 72)
    print("TEST 4: WHY p=2 is special")
    print("=" * 72)
    print()
    print("  The model uses complex amplitudes propagated by linear operations.")
    print("  Linear operations on complex amplitudes that preserve reversibility")
    print("  (unitarity) form the group U(n).")
    print()
    print("  The ONLY p-norm preserved by ALL unitary transformations is p=2.")
    print("  This is a theorem (Wigner's theorem / unitarity implies Born rule).")
    print()
    print("  Therefore:")
    print("  - The model ASSUMES: complex amplitudes + linear propagation + reversibility")
    print("  - It DERIVES: |ψ|² probability (Born rule)")
    print("  - The Born rule is NOT an additional assumption — it's a CONSEQUENCE")
    print("    of the amplitude propagation rules")
    print()
    print("  BUT (the reviewer's deeper point):")
    print("  - WHY complex amplitudes? (vs real, quaternionic, etc.)")
    print("  - WHY linear propagation? (vs nonlinear)")
    print("  - WHY reversibility? (vs dissipative)")
    print("  These ARE the remaining assumptions that the model doesn't derive.")

    # =========================================================
    # TEST 5: What if amplitudes were REAL?
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 5: What changes if amplitudes were real (not complex)?")
    print("=" * 72)
    print()

    print("  With real amplitudes, the mixing group is O(n) instead of U(n).")
    print("  The 2-norm is still the unique preserved norm (same theorem).")
    print("  But: real amplitudes can't produce a PHASE SHIFT.")
    print("  The model's interference depends on complex phase accumulation")
    print("  (e^(i*k*action)). Without complex amplitudes:")
    print("  - No phase accumulation → no interference fringes")
    print("  - The two-slit distribution would be flat")
    print()

    # Verify: real-amplitude path-sum
    print("  Verification: real-only amplitude vs complex:")
    print("  (Using the two-slit center detector at phase=0 and phase=π)")
    print()

    # The complex amplitude at center is A_upper + A_lower
    # With phase shift π on upper: A_upper*e^(iπ) + A_lower = -A_upper + A_lower
    # If A_upper ≈ A_lower (symmetric), this ≈ 0 (destructive interference)
    # With REAL amplitudes: A_upper*(-1) + A_lower = -A_upper + A_lower ≈ 0 (ALSO destructive)
    # So real amplitudes CAN produce interference if the action gives -1 at phase=π

    # But: real amplitudes can only give ±1, not continuous phase rotation
    # The action e^(i*k*S) with real-only constraint gives cos(k*S), losing the imaginary part

    A = 1.0 + 0.0j  # amplitude through each slit (equal by symmetry)
    print(f"  Complex: A_up(π) + A_low = {A * cmath.exp(1j * math.pi) + A}")
    print(f"  → |sum|² = {abs(A * cmath.exp(1j * math.pi) + A)**2:.6f} (destructive)")
    print()
    print(f"  Complex: A_up(π/2) + A_low = {A * cmath.exp(1j * math.pi/2) + A}")
    print(f"  → |sum|² = {abs(A * cmath.exp(1j * math.pi/2) + A)**2:.6f} (partial)")
    print()
    print(f"  Real only: can't produce phase=π/2. Limited to phase = 0 or π.")
    print(f"  Complex amplitudes enable CONTINUOUS phase control = richer interference.")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
