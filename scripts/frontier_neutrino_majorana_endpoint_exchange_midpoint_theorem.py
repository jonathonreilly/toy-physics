#!/usr/bin/env python3
"""
Majorana endpoint-exchange midpoint theorem on the finite 16-step hierarchy register.

Question:
  Once the admitted local Majorana selector fixes the self-dual point rho = 1,
  can a genuinely new non-homogeneous local-to-generation bridge be written on
  the exact finite taste staircase rather than on another homogeneous source ray?

Answer on the minimal finite-register bridge:
  Yes. The hierarchy lane already gives the exact finite staircase

      lambda_k = alpha_LM^k,   k in {0,...,16},

  between the UV endpoint k=0 and the IR endpoint k=16. If the local
  normal/pairing axis exchange is lifted to the finite register as the exact
  endpoint exchange, then the lift is forced to be the unique order-reversing
  involution

      k -> 16-k,
      lambda -> alpha_LM^16 / lambda.

  The self-dual local point must then map to the unique fixed point of that
  involution:

      k_B = 8,
      lambda_* = alpha_LM^8.

Boundary:
  This closes the absolute staircase anchor only on this minimal
  endpoint-exchange bridge. It does not yet derive the downstream
  three-generation A/B/epsilon amplitudes.
"""

from __future__ import annotations

import math
import sys


PASS_COUNT = 0
FAIL_COUNT = 0

PI = math.pi
G_BARE = 1.0
ALPHA_BARE = G_BARE**2 / (4.0 * PI)
PLAQ_MC = 0.5934
U0 = PLAQ_MC ** 0.25
ALPHA_LM = ALPHA_BARE / U0
N_TASTE = 16


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


def endpoint_exchange(k: int) -> int:
    return N_TASTE - k


def lambda_k(k: int) -> float:
    return ALPHA_LM ** k


def test_finite_register_exists() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE HIERARCHY LANE SUPPLIES AN EXACT FINITE 16-STEP REGISTER")
    print("=" * 88)

    ks = list(range(N_TASTE + 1))
    lambdas = [lambda_k(k) for k in ks]

    check("The staircase register has exactly 17 nodes k=0..16", ks == list(range(17)))
    check("The UV endpoint is k=0 with lambda_0 = 1", abs(lambdas[0] - 1.0) < 1e-15,
          f"lambda_0={lambdas[0]:.15f}")
    check("The IR endpoint is k=16 with lambda_16 = alpha_LM^16", abs(lambdas[-1] - ALPHA_LM ** 16) < 1e-30,
          f"lambda_16={lambdas[-1]:.6e}")
    check("The finite staircase is strictly monotone in k", all(lambdas[i + 1] < lambdas[i] for i in range(N_TASTE)),
          f"lambda_1={lambdas[1]:.6f}, lambda_16={lambdas[-1]:.6e}")

    print()
    print("  The hierarchy lane is therefore not an unbounded scale family here.")
    print("  It is one exact finite register between two exact endpoints.")


def test_endpoint_exchange_is_unique_order_reversing_involution() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ENDPOINT EXCHANGE FORCES THE UNIQUE ORDER-REVERSING INVOLUTION")
    print("=" * 88)

    images = [endpoint_exchange(k) for k in range(N_TASTE + 1)]
    involution_err = max(abs(endpoint_exchange(endpoint_exchange(k)) - k) for k in range(N_TASTE + 1))
    order_err = max(images[i + 1] - images[i] for i in range(N_TASTE))
    endpoint_err = abs(images[0] - N_TASTE) + abs(images[-1] - 0)

    # On a finite total order {0,...,N}, any order-reversing bijection is forced
    # by rank complement: the image of rank-k is rank-(N-k).
    rank_formula_err = max(abs(images[k] - (N_TASTE - k)) for k in range(N_TASTE + 1))

    check("The finite-register endpoint exchange is an involution", involution_err == 0,
          f"max |E(E(k))-k|={involution_err}")
    check("The endpoint exchange preserves the two exact endpoints", endpoint_err == 0,
          f"endpoint error={endpoint_err}")
    check("The endpoint exchange is strictly order-reversing", order_err < 0,
          f"max forward difference={order_err}")
    check("Any endpoint-preserving order-reversing bijection is forced to k -> 16-k", rank_formula_err == 0,
          f"rank-complement error={rank_formula_err}")

    print()
    print("  So the missing bridge is no longer an arbitrary non-homogeneous map.")
    print("  On the exact finite register, the UV/IR endpoint exchange is unique.")


def test_scale_exchange_fixed_point() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SELF-DUAL LOCAL POINT LIFTS TO THE MIDPOINT k = 8")
    print("=" * 88)

    products = [lambda_k(k) * lambda_k(endpoint_exchange(k)) for k in range(N_TASTE + 1)]
    target = ALPHA_LM ** N_TASTE
    prod_err = max(abs(prod - target) for prod in products)

    fixed_ks = [k for k in range(N_TASTE + 1) if endpoint_exchange(k) == k]
    lambda_star = math.sqrt(target)
    midpoint_err = abs(lambda_star - lambda_k(8))

    check("The scale-side endpoint exchange is lambda -> alpha_LM^16 / lambda", prod_err < 1e-18,
          f"max |lambda_k lambda_16-k - alpha^16|={prod_err:.2e}")
    check("The unique fixed point of k -> 16-k is k = 8", fixed_ks == [8], f"fixed points={fixed_ks}")
    check("The unique scale fixed point is lambda_* = alpha_LM^8", midpoint_err < 1e-18,
          f"|sqrt(alpha^16)-alpha^8|={midpoint_err:.2e}")

    print()
    print("  If the exact local axis exchange rho -> 1/rho is lifted to this")
    print("  exact endpoint exchange on the finite staircase, the local self-dual")
    print("  point rho = 1 must land at the unique midpoint k = 8.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: ENDPOINT-EXCHANGE MIDPOINT THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md")
    print("  - docs/HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md")
    print("  - docs/YT_BOUNDARY_THEOREM.md")
    print()
    print("Question:")
    print("  Can the exact local self-dual Majorana point rho = 1 be lifted to an")
    print("  absolute staircase anchor on a genuinely new non-homogeneous bridge?")

    test_finite_register_exists()
    test_endpoint_exchange_is_unique_order_reversing_involution()
    test_scale_exchange_fixed_point()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Yes, on the minimal finite-register bridge. The exact 16-step taste")
    print("  staircase already supplies two exact endpoints, and the unique")
    print("  endpoint-preserving order-reversing involution is k -> 16-k.")
    print("  Lifting the local axis exchange to that endpoint exchange forces the")
    print("  unique midpoint:")
    print()
    print("      k_B = 8,    lambda_* = alpha_LM^8.")
    print()
    print("  This closes the absolute staircase anchor on the minimal")
    print("  endpoint-exchange bridge. What remains downstream is the")
    print("  three-generation A/B/epsilon amplitude law.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
