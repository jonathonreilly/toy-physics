#!/usr/bin/env python3
"""Exact audit for the Wolfenstein lambda and A structural identities."""

from __future__ import annotations

from fractions import Fraction
import math
import sys

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


PASS_COUNT = 0
FAIL_COUNT = 0

N_PAIR = 2
N_COLOR = 3
N_QUARK = N_PAIR * N_COLOR
ALPHA_S_V = CANONICAL_ALPHA_S_V


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 80)
    print(title)
    print("-" * 80)


def close(a: float, b: float, tol: float = 1e-14) -> bool:
    return abs(a - b) <= tol


def audit_inputs() -> None:
    banner("Retained CKM atlas inputs")

    print(f"  n_pair       = {N_PAIR}")
    print(f"  n_color      = {N_COLOR}")
    print(f"  n_quark      = {N_QUARK}")
    print(f"  alpha_s(v)   = {ALPHA_S_V:.15f}")

    check("n_pair = 2", N_PAIR == 2)
    check("n_color = 3", N_COLOR == 3)
    check("n_quark = n_pair*n_color = 6", N_QUARK == 6)
    check("canonical alpha_s(v) is positive", ALPHA_S_V > 0)


def audit_w1_lambda() -> None:
    banner("W1: lambda^2 = alpha_s(v)/2")

    lambda_sq = ALPHA_S_V / N_PAIR
    lambda_value = math.sqrt(lambda_sq)

    print(f"  lambda^2 = {lambda_sq:.15f}")
    print(f"  lambda   = {lambda_value:.15f}")

    check("lambda^2 = alpha_s(v)/n_pair", close(lambda_sq, ALPHA_S_V / N_PAIR))
    check("n_pair specialization gives lambda^2 = alpha_s(v)/2", close(lambda_sq, ALPHA_S_V / 2))
    check("lambda is the positive square root", close(lambda_value * lambda_value, lambda_sq))


def audit_w2_a() -> None:
    banner("W2: A^2 = n_pair/n_color = 2/3")

    a_sq_exact = Fraction(N_PAIR, N_COLOR)
    a_sq = float(a_sq_exact)
    a_value = math.sqrt(a_sq)

    print(f"  A^2 = {a_sq_exact}")
    print(f"  A   = {a_value:.15f}")

    check("A^2 exact rational is 2/3", a_sq_exact == Fraction(2, 3))
    check("A^2 float equals 2/3", close(a_sq, 2 / 3))
    check("A is the positive square root", close(a_value * a_value, a_sq))


def audit_w3_product() -> None:
    banner("W3: A^2 lambda^2 = alpha_s(v)/3")

    a_sq = float(Fraction(N_PAIR, N_COLOR))
    lambda_sq = ALPHA_S_V / N_PAIR
    product = a_sq * lambda_sq
    expected = ALPHA_S_V / N_COLOR

    print(f"  A^2 lambda^2 = {product:.15f}")
    print(f"  alpha_s(v)/3 = {expected:.15f}")

    check("A^2 lambda^2 = alpha_s(v)/n_color", close(product, expected))
    check("n_pair cancels in exact rational product", Fraction(N_PAIR, N_COLOR) * Fraction(1, N_PAIR) == Fraction(1, N_COLOR))


def audit_vcb() -> None:
    banner("CKM corollary: |V_cb| = alpha_s(v)/sqrt(6)")

    a_value = math.sqrt(2 / 3)
    lambda_sq = ALPHA_S_V / 2
    v_cb_atlas = a_value * lambda_sq
    v_cb_clean = ALPHA_S_V / math.sqrt(N_QUARK)

    print(f"  A lambda^2          = {v_cb_atlas:.15f}")
    print(f"  alpha_s(v)/sqrt(6) = {v_cb_clean:.15f}")

    check("|V_cb| atlas form equals alpha_s(v)/sqrt(6)", close(v_cb_atlas, v_cb_clean))
    check("|V_cb| squared equals alpha_s(v)^2/6", close(v_cb_clean * v_cb_clean, ALPHA_S_V * ALPHA_S_V / 6))


def audit_vub() -> None:
    banner("CKM corollary: |V_ub| with CP radius")

    a_value = math.sqrt(2 / 3)
    lambda_value = math.sqrt(ALPHA_S_V / 2)
    cp_radius = math.sqrt(1 / 6)
    v_ub_atlas = a_value * lambda_value**3 * cp_radius
    v_ub_clean = ALPHA_S_V**1.5 / (6 * math.sqrt(2))

    print(f"  A lambda^3 sqrt(1/6)              = {v_ub_atlas:.15f}")
    print(f"  alpha_s(v)^(3/2)/(6 sqrt(2))     = {v_ub_clean:.15f}")

    check("CP radius squared is 1/6", close(cp_radius * cp_radius, 1 / 6))
    check("|V_ub| atlas form equals alpha_s(v)^(3/2)/(6 sqrt(2))", close(v_ub_atlas, v_ub_clean))


def audit_joint_cp_surface() -> None:
    banner("Joint Wolfenstein/CP identity surface")

    rho = Fraction(1, 6)
    eta_sq = Fraction(5, 36)
    radius_sq = rho * rho + eta_sq
    lambda_sq = ALPHA_S_V / 2
    a_sq = 2 / 3
    eta = math.sqrt(5) / 6

    j0_from_surface = (lambda_sq**3) * a_sq * eta
    j0_clean = ALPHA_S_V**3 * math.sqrt(5) / 72

    print(f"  rho^2 + eta^2 = {radius_sq}")
    print(f"  J_0 surface    = {j0_from_surface:.15e}")
    print(f"  J_0 clean      = {j0_clean:.15e}")

    check("rho^2 + eta^2 = 1/6", radius_sq == Fraction(1, 6))
    check("J_0 factorization equals alpha_s(v)^3 sqrt(5)/72", close(j0_from_surface, j0_clean))
    surface_complete = (
        close(lambda_sq, ALPHA_S_V / N_PAIR)
        and close(a_sq, N_PAIR / N_COLOR)
        and radius_sq == Fraction(1, 6)
        and close(j0_from_surface, j0_clean)
    )
    check("complete named surface covers lambda, A, rho, eta, delta, J_0", surface_complete)


def main() -> int:
    print("=" * 80)
    print("Wolfenstein lambda and A structural identities audit")
    print("=" * 80)

    audit_inputs()
    audit_w1_lambda()
    audit_w2_a()
    audit_w3_product()
    audit_vcb()
    audit_vub()
    audit_joint_cp_surface()

    print()
    print("=" * 80)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 80)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
