#!/usr/bin/env python3
"""
Invented axiom-native candidate: Z3 phase-lift mixed bridge for the DM odd slot.

Question:
  Is there a minimal axiom-native candidate family that can transfer the exact
  weak-sector Z3 CP source into the unique odd circulant DM slot?

Candidate:
  Yes. On a base even circulant kernel

      K_0 = d I + r (S + S^2),

  define the one-parameter source-lift family

      K_lambda = d I + r (e^{i lambda delta_src} S + e^{-i lambda delta_src} S^2),

  with exact weak-sector source phase delta_src = 2pi/3.

  Then:
    - lambda = 0 reproduces the current retained local bank
    - lambda = 1 is full source transfer
    - the off-diagonal norm r and diagonal d stay fixed
    - the odd slot becomes c_odd = r sin(lambda delta_src)

Boundary:
  This is an invented candidate bridge family, not a derived theorem of the
  current stack. The exact algebra is rigorous. The later character-transfer
  theorem fixes the source-faithful branches to lambda in {-1,0,+1} with
  lambda=+1 the source-oriented branch, but the later circulant mass-basis
  no-go also shows that the entire exact Z3-covariant circulant family is
  still insufficient for the physical leptogenesis tensor.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

S = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
    ],
    dtype=complex,
)
S2 = S @ S
P23 = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ],
    dtype=complex,
)

DELTA_SRC = 2.0 * np.pi / 3.0


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def decompose(k: np.ndarray) -> tuple[float, float, float]:
    return float(np.real(k[0, 0])), float(np.real(k[0, 1])), float(np.imag(k[0, 1]))


def k_phase_lift(d: float, r: float, lam: float) -> np.ndarray:
    phase = lam * DELTA_SRC
    return d * np.eye(3, dtype=complex) + r * (np.exp(1j * phase) * S + np.exp(-1j * phase) * S2)


def cp_tensor(k: np.ndarray) -> float:
    return float(np.imag(k[0, 1] ** 2))


def sheet_roots(d: float, r: float) -> tuple[float, float]:
    disc = max(d * d - 4.0 * r * r, 0.0)
    root = math.sqrt(disc)
    x2 = 0.5 * (d + root)
    y2 = 0.5 * (d - root)
    return math.sqrt(max(x2, 0.0)), math.sqrt(max(y2, 0.0))


def part1_the_family_is_axiom_native_in_its_inputs() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CANDIDATE FAMILY IS AXIOM-NATIVE IN ITS INPUTS")
    print("=" * 88)

    d = 1.1366666666666667
    r = 0.45666666666666667
    k0 = k_phase_lift(d, r, 0.0)
    k1 = k_phase_lift(d, r, 1.0)
    d0, c_even0, c_odd0 = decompose(k0)
    d1, c_even1, c_odd1 = decompose(k1)

    check(
        "lambda=0 reproduces the current even local bank",
        abs(d0 - d) < 1e-12 and abs(c_even0 - r) < 1e-12 and abs(c_odd0) < 1e-12,
        f"(d,c_even,c_odd)=({d0:.6f},{c_even0:.6f},{c_odd0:.2e})",
    )
    check(
        "lambda=1 uses the exact weak-only Z3 source phase delta_src = 2pi/3",
        abs(c_even1 + 0.5 * r) < 1e-12 and abs(c_odd1 - (math.sqrt(3.0) / 2.0) * r) < 1e-12,
        f"(c_even,c_odd)=({c_even1:.6f},{c_odd1:.6f})",
    )

    print()
    print("  So the candidate family uses only:")
    print("    - the exact even local kernel data (d,r)")
    print("    - the exact weak-sector Z3 source phase 2pi/3")
    print("    - one new bridge amplitude lambda")


def part2_the_family_preserves_the_two_higgs_admissible_subcone() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CANDIDATE FAMILY PRESERVES THE TWO-HIGGS ADMISSIBLE SUBCONE")
    print("=" * 88)

    d = 1.1366666666666667
    r = 0.45666666666666667
    admissible = d >= 2.0 * r
    x, y = sheet_roots(d, r)
    ok_all = True
    details = []
    for lam in [0.0, 0.5, 1.0]:
        k = k_phase_lift(d, r, lam)
        dk, c_even, c_odd = decompose(k)
        norm_off = abs(k[0, 1])
        ok = abs(dk - d) < 1e-12 and abs(norm_off - r) < 1e-12
        ok_all &= ok
        details.append(f"lam={lam:.1f}: |h|={norm_off:.6f}, c_even={c_even:.6f}, c_odd={c_odd:.6f}")

    check(
        "The exact base even kernel is already in the admissible subcone",
        admissible,
        f"d={d:.6f}, 2r={2.0*r:.6f}",
    )
    check(
        "The phase-lift family preserves d and the off-diagonal norm r for all lambda",
        ok_all,
        "; ".join(details),
    )
    check(
        "Therefore the same physical two-Higgs moduli (x,y) survive across the family",
        x >= y > 0.0,
        f"x={x:.6f}, y={y:.6f}",
    )

    print()
    print("  So the invented bridge does not change the local two-Higgs support")
    print("  or push the kernel out of the admissible subcone. It only rotates the")
    print("  fixed off-diagonal norm into the odd slot.")


def part3_the_family_is_residual_z2_odd_and_turns_on_cp() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CANDIDATE FAMILY IS RESIDUAL-Z2 ODD AND TURNS ON CP")
    print("=" * 88)

    d = 1.1366666666666667
    r = 0.45666666666666667
    k_half = k_phase_lift(d, r, 0.5)
    k_full = k_phase_lift(d, r, 1.0)
    reflect_half = P23 @ k_half @ P23.conj().T
    reflect_full = P23 @ k_full @ P23.conj().T

    check(
        "Residual-Z2 reflection sends lambda -> -lambda on the phase-lift family",
        np.linalg.norm(reflect_half - k_phase_lift(d, r, -0.5)) < 1e-12
        and np.linalg.norm(reflect_full - k_phase_lift(d, r, -1.0)) < 1e-12,
        "P23 K_lambda P23 = K_-lambda",
    )
    check(
        "Any nonzero lambda turns on the odd slot away from the current zero law",
        abs(decompose(k_half)[2]) > 1e-6 and abs(decompose(k_full)[2]) > 1e-6,
        f"c_odd(1/2)={decompose(k_half)[2]:.6f}, c_odd(1)={decompose(k_full)[2]:.6f}",
    )
    check(
        "The standard CP tensor is nonzero for the full-source candidate lambda=1",
        abs(cp_tensor(k_full)) > 1e-6,
        f"cp={cp_tensor(k_full):.6f}",
    )

    print()
    print("  So this is a real positive candidate activator, not just a naming move.")
    print("  It is the smallest axiom-native family we currently have that actually")
    print("  turns on the exact missing odd slot.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO Z3 PHASE-LIFT MIXED BRIDGE")
    print("=" * 88)
    print()
    print("Status:")
    print("  Invented candidate bridge family beyond the retained local bank.")
    print("  The algebra below is exact. The later character-transfer theorem fixes")
    print("  the source-faithful branches to lambda in {-1,0,+1}, with lambda=+1")
    print("  the source-oriented branch.")
    print()
    print("Question:")
    print("  Is there a smallest axiom-native candidate family that can transfer the")
    print("  exact weak-sector Z3 CP source into the unique DM odd slot?")

    part1_the_family_is_axiom_native_in_its_inputs()
    part2_the_family_preserves_the_two_higgs_admissible_subcone()
    part3_the_family_is_residual_z2_odd_and_turns_on_cp()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Candidate family:")
    print("    K_lambda = d I + r (e^{i lambda delta_src} S + e^{-i lambda delta_src} S^2)")
    print("    with delta_src = 2pi/3")
    print()
    print("  Safe read:")
    print("    - lambda=0 is the exact current stack")
    print("    - lambda=1 is full weak-source transfer")
    print("    - the family preserves the admissible two-Higgs local data")
    print("    - any nonzero lambda turns on the unique odd slot")
    print()
    print("  This is the strongest axiom-native candidate bridge currently on hand,")
    print("  but the later mass-basis no-go shows the whole exact Z3-covariant")
    print("  circulant family is still not the final physical leptogenesis texture.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
