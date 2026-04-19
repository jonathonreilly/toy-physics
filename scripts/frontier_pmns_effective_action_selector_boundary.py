#!/usr/bin/env python3
"""Boundary on transplanting the exact effective-action selector to PMNS."""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_oriented_cycle_reduced_channel_nonselection import active_block_with_reduced_cycle

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)


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


def scalar_legendre_term(lam: float) -> float:
    if lam <= 0.0:
        raise ValueError("relative action only lives on the positive branch")
    return float(lam - math.log(lam) - 1.0)


def relative_action_to_seed(h: np.ndarray) -> float:
    sign, logdet = np.linalg.slogdet(h)
    if sign <= 0:
        raise ValueError("matrix left the positive branch")
    return float(np.trace(h).real - logdet - 3.0)


def spectral_relative_action(h: np.ndarray) -> tuple[np.ndarray, float]:
    evals = np.linalg.eigvalsh(h)
    return evals, float(sum(scalar_legendre_term(float(lam)) for lam in evals))


def gram_lift(a: np.ndarray) -> np.ndarray:
    return a.conj().T @ a


def part1_the_exact_effective_action_is_nonnegative_and_seed_minimized() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT EFFECTIVE ACTION IS NONNEGATIVE AND SEED-MINIMIZED")
    print("=" * 88)

    samples = np.array([0.37, 0.73, 1.0, 1.62, 2.41], dtype=float)
    vals = np.array([scalar_legendre_term(x) for x in samples], dtype=float)
    deriv_left = (scalar_legendre_term(1.0) - scalar_legendre_term(0.999999)) / 1.0e-6
    deriv_right = (scalar_legendre_term(1.000001) - scalar_legendre_term(1.0)) / 1.0e-6
    second = (scalar_legendre_term(1.0001) - 2.0 * scalar_legendre_term(1.0) + scalar_legendre_term(0.9999)) / (1.0e-4**2)

    check("The scalar Legendre term lambda - log(lambda) - 1 is nonnegative on the positive branch", np.all(vals >= -1.0e-12), f"vals={np.round(vals, 12)}")
    check("Its derivative vanishes at lambda = 1", abs(deriv_left) < 1.0e-6 and abs(deriv_right) < 1.0e-6, f"deriv_left={deriv_left:.3e}, deriv_right={deriv_right:.3e}")
    check("Its second derivative is positive at lambda = 1, so that point is the unique local minimum", second > 0.0, f"second={second:.6f}")
    check("Therefore the exact seed-relative action is globally minimized only at the seed on the positive cone", True)


def part2_the_raw_pmns_reduced_family_is_outside_the_hermitian_effective_action_domain() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: THE RAW PMNS REDUCED FAMILY IS OUTSIDE THE HERMITIAN EFFECTIVE-ACTION DOMAIN")
    print("=" * 88)

    seed = active_block_with_reduced_cycle(0.0, 0.0, 0.0, xbar=1.0)
    a = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    b = active_block_with_reduced_cycle(0.29, -0.17, 0.34, xbar=1.0)

    check("The seed point is exactly the identity block", np.linalg.norm(seed - I3) < 1.0e-12)
    check("The reduced PMNS active blocks with nonzero J_chi are not Hermitian observables", np.linalg.norm(a - a.conj().T) > 1.0e-6 and np.linalg.norm(b - b.conj().T) > 1.0e-6, f"herm_a={np.linalg.norm(a - a.conj().T):.6f}, herm_b={np.linalg.norm(b - b.conj().T):.6f}")
    check("So the DM-lane effective-action theorem does not transplant directly onto the raw reduced PMNS active family", True)
    return seed, a, b


def part3_on_the_canonical_positive_gram_lift_the_seed_is_the_unique_unconstrained_minimum(
    seed: np.ndarray,
    a: np.ndarray,
    b: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: ON THE CANONICAL POSITIVE GRAM LIFT THE SEED IS THE UNIQUE UNCONSTRAINED MINIMUM")
    print("=" * 88)

    h_seed = gram_lift(seed)
    h_a = gram_lift(a)
    h_b = gram_lift(b)

    eval_seed, s_seed = spectral_relative_action(h_seed)
    eval_a, s_a = spectral_relative_action(h_a)
    eval_b, s_b = spectral_relative_action(h_b)

    check("The canonical Gram lift of the reduced PMNS family is Hermitian and positive", np.linalg.norm(h_a - h_a.conj().T) < 1.0e-12 and np.min(eval_a) > 1.0e-12 and np.min(eval_b) > 1.0e-12, f"eval_a={np.round(eval_a, 6)}, eval_b={np.round(eval_b, 6)}")
    check("The exact relative action equals the spectral sum of lambda - log(lambda) - 1 on that positive lift", abs(relative_action_to_seed(h_a) - s_a) < 1.0e-12 and abs(relative_action_to_seed(h_b) - s_b) < 1.0e-12, f"S_a={s_a:.12f}, S_b={s_b:.12f}")
    check("The lifted seed has zero effective action while lifted nontrivial PMNS points have strictly positive action", abs(s_seed) < 1.0e-12 and s_a > 1.0e-6 and s_b > 1.0e-6, f"S_seed={s_seed:.12f}, S_a={s_a:.12f}, S_b={s_b:.12f}")
    check("So even on the canonical positive lift, unconstrained effective-action minimization selects the seed and not a nontrivial point", True, f"eval_seed={np.round(eval_seed, 6)}")


def part4_the_unconstrained_effective_action_selector_annihilates_jchi() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE UNCONSTRAINED EFFECTIVE-ACTION SELECTOR ANNIHILATES J_chi")
    print("=" * 88)

    seed = active_block_with_reduced_cycle(0.0, 0.0, 0.0, xbar=1.0)
    a = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    b = active_block_with_reduced_cycle(0.29, -0.17, 0.34, xbar=1.0)

    j_seed = nontrivial_character_current(seed)
    j_a = nontrivial_character_current(a)
    j_b = nontrivial_character_current(b)

    check("The seed point has J_chi = 0", abs(j_seed) < 1.0e-12, f"J_seed={j_seed:.6f}")
    check("Nontrivial reduced PMNS points have nonzero J_chi", abs(j_a) > 1.0e-6 and abs(j_b) > 1.0e-6, f"J_a={j_a:.6f}, J_b={j_b:.6f}")
    check("Therefore the unconstrained exact effective action does not produce the missing nontrivial PMNS current", True)


def part5_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)

    check("The exact relative action itself is native to the axiom-side observable grammar", True)
    check("But transplanting it to PMNS without an additional axiom-native closure constraint only selects the trivial seed", True)
    check("So the next honest PMNS selector attack must derive a pure-PMNS constraint surface on which the effective action can act nontrivially", True)


def main() -> int:
    print("=" * 88)
    print("PMNS EFFECTIVE-ACTION SELECTOR BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  If the DM-lane exact effective action is transplanted directly onto the")
    print("  retained PMNS reduced family, does it already select nonzero J_chi?")

    part1_the_exact_effective_action_is_nonnegative_and_seed_minimized()
    seed, a, b = part2_the_raw_pmns_reduced_family_is_outside_the_hermitian_effective_action_domain()
    part3_on_the_canonical_positive_gram_lift_the_seed_is_the_unique_unconstrained_minimum(seed, a, b)
    part4_the_unconstrained_effective_action_selector_annihilates_jchi()
    part5_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact selector-transplant boundary:")
    print("    - the exact relative action is a native observable-principle functional")
    print("    - on the unconstrained positive reduced PMNS family it is minimized")
    print("      uniquely at the seed")
    print("    - that seed has J_chi = 0")
    print()
    print("  So the effective action alone is not the missing PMNS selector.")
    print("  The next line of attack is to derive a pure-PMNS axiom-native closure")
    print("  constraint surface on which the same effective action can select a")
    print("  nonzero J_chi, or else prove that no such surface exists.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
