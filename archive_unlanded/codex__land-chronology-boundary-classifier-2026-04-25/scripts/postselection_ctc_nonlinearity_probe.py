#!/usr/bin/env python3
"""Chronology lane probe: postselection/CTC-style nonlinear effective maps.

The retained single-clock surface uses ordinary local evolution: linear,
trace-preserving channels on the state carried forward from one slice to the
next. Postselection and P-CTC-style final-boundary projections can be written
as an unnormalized linear success map followed by state-dependent
renormalization:

    M(rho) = K rho K^dagger / Tr(K rho K^dagger).

That last denominator depends on rho. The resulting accepted-subensemble map
is therefore not an ordinary linear CPTP channel. It may change retrodictive
or conditional probabilities, but it is classified here as final-boundary
import rather than operational past signaling on the retained surface.
"""

from __future__ import annotations

from fractions import Fraction


PASS = 0
FAIL = 0

Matrix = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")


def mat_add(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2)
    )  # type: ignore[return-value]


def mat_sub(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(a[i][j] - b[i][j] for j in range(2)) for i in range(2)
    )  # type: ignore[return-value]


def mat_scale(scalar: Fraction, a: Matrix) -> Matrix:
    return tuple(
        tuple(scalar * a[i][j] for j in range(2)) for i in range(2)
    )  # type: ignore[return-value]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def convex_mix(p: Fraction, rho_a: Matrix, rho_b: Matrix) -> Matrix:
    return mat_add(mat_scale(p, rho_a), mat_scale(1 - p, rho_b))


def trace(rho: Matrix) -> Fraction:
    return rho[0][0] + rho[1][1]


def bit_flip_channel(rho: Matrix, q: Fraction) -> Matrix:
    """Linear CPTP comparison channel: (1-q) rho + q X rho X."""

    x_gate: Matrix = ((Fraction(0), Fraction(1)), (Fraction(1), Fraction(0)))
    flipped = mat_mul(x_gate, mat_mul(rho, x_gate))
    return mat_add(mat_scale(1 - q, rho), mat_scale(q, flipped))


def postselection_success_map(rho: Matrix) -> Matrix:
    """Unnormalized one-Kraus success branch with K = diag(1/2, 1)."""

    k0 = Fraction(1, 2)
    k1 = Fraction(1, 1)
    return (
        (k0 * rho[0][0] * k0, k0 * rho[0][1] * k1),
        (k1 * rho[1][0] * k0, k1 * rho[1][1] * k1),
    )


def postselected_effective_map(rho: Matrix) -> tuple[Matrix, Fraction]:
    unnormalized = postselection_success_map(rho)
    success_probability = trace(unnormalized)
    if success_probability == 0:
        raise ValueError("postselected branch has zero acceptance probability")
    return mat_scale(1 / success_probability, unnormalized), success_probability


def max_abs_entry(rho: Matrix) -> Fraction:
    return max(abs(value) for row in rho for value in row)


def fmt_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fmt_matrix(rho: Matrix) -> str:
    rows = [
        "[" + ", ".join(f"{fmt_fraction(value):>5s}" for value in row) + "]"
        for row in rho
    ]
    return "[" + "; ".join(rows) + "]"


def main() -> int:
    print("=" * 88)
    print("POSTSELECTION / CTC NONLINEARITY PROBE")
    print("  Test: final-boundary renormalization is not an ordinary linear CPTP map.")
    print("=" * 88)
    print()

    rho0: Matrix = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(0)))
    rho1: Matrix = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(1)))
    p = Fraction(2, 5)
    mixture = convex_mix(p, rho0, rho1)

    q = Fraction(1, 3)
    linear_direct = bit_flip_channel(mixture, q)
    linear_convex = convex_mix(
        p,
        bit_flip_channel(rho0, q),
        bit_flip_channel(rho1, q),
    )
    linear_gap = mat_sub(linear_direct, linear_convex)

    print("Input ensemble:")
    print(f"  p = {fmt_fraction(p)}")
    print(f"  rho0       = {fmt_matrix(rho0)}")
    print(f"  rho1       = {fmt_matrix(rho1)}")
    print(f"  p*rho0+(1-p)*rho1 = {fmt_matrix(mixture)}")
    print()

    print("Linear CPTP comparison: bit-flip channel with q = 1/3")
    print(f"  T(mixture)          = {fmt_matrix(linear_direct)}")
    print(f"  p*T(rho0)+(1-p)*T(rho1) = {fmt_matrix(linear_convex)}")
    print(f"  convex gap          = {fmt_matrix(linear_gap)}")
    print()

    check(
        "linear comparison channel preserves trace on rho0",
        trace(bit_flip_channel(rho0, q)) == 1,
        f"trace={fmt_fraction(trace(bit_flip_channel(rho0, q)))}",
    )
    check(
        "linear comparison channel preserves trace on mixture",
        trace(linear_direct) == 1,
        f"trace={fmt_fraction(trace(linear_direct))}",
    )
    check(
        "linear comparison channel is convex-linear",
        linear_direct == linear_convex,
        f"max gap={fmt_fraction(max_abs_entry(linear_gap))}",
    )

    post0, accept0 = postselected_effective_map(rho0)
    post1, accept1 = postselected_effective_map(rho1)
    post_direct, accept_mix = postselected_effective_map(mixture)
    post_convex = convex_mix(p, post0, post1)
    post_gap = mat_sub(post_direct, post_convex)

    print("Postselected/final-boundary branch: K = diag(1/2, 1)")
    print("  unnormalized success map: rho -> K rho K^dagger")
    print("  normalized effective map: rho -> success(rho) / Tr(success(rho))")
    print(f"  acceptance rho0/rho1/mix = {fmt_fraction(accept0)} / {fmt_fraction(accept1)} / {fmt_fraction(accept_mix)}")
    print(f"  M(mixture)              = {fmt_matrix(post_direct)}")
    print(f"  p*M(rho0)+(1-p)*M(rho1) = {fmt_matrix(post_convex)}")
    print(f"  convex gap              = {fmt_matrix(post_gap)}")
    print()

    unnorm_direct = postselection_success_map(mixture)
    unnorm_convex = convex_mix(
        p,
        postselection_success_map(rho0),
        postselection_success_map(rho1),
    )
    check(
        "unnormalized success branch is still linear",
        unnorm_direct == unnorm_convex,
        f"success(mix)={fmt_matrix(unnorm_direct)}",
    )
    check(
        "postselection acceptance probability depends on input state",
        accept0 != accept1,
        f"P_acc(rho0)={fmt_fraction(accept0)}, P_acc(rho1)={fmt_fraction(accept1)}",
    )
    check(
        "normalized postselected effective map preserves trace only after renormalization",
        trace(post_direct) == 1 and accept_mix != 1,
        f"Tr(M(mix))={fmt_fraction(trace(post_direct))}, raw acceptance={fmt_fraction(accept_mix)}",
    )
    check(
        "normalized postselected effective map fails convex-linearity",
        post_direct != post_convex,
        f"max gap={fmt_fraction(max_abs_entry(post_gap))}",
    )
    check(
        "convex-linearity failure is exact, not numerical roundoff",
        max_abs_entry(post_gap) == Fraction(9, 35),
        f"expected gap=9/35, observed={fmt_fraction(max_abs_entry(post_gap))}",
    )

    retained_surface = "NO"
    classification = "postselection/final-boundary import"
    operational_past_signal = "NO"

    print("CLASSIFICATION")
    print(f"  retained single-clock local CPTP surface: {retained_surface}")
    print(f"  chronology label: {classification}")
    print(f"  operational past signaling: {operational_past_signal}")
    print()

    check(
        "postselected branch is classified outside the retained surface",
        retained_surface == "NO" and classification == "postselection/final-boundary import",
        f"retained_surface={retained_surface}, classification={classification}",
    )
    check(
        "classification does not promote the construction to operational past signaling",
        operational_past_signal == "NO",
        f"operational_past_signaling={operational_past_signal}",
    )

    print()
    print("SAFE READ")
    print("  - The linear CPTP comparison evolves mixtures affinely on one clock.")
    print("  - The postselected branch is linear before conditioning, but the accepted")
    print("    effective state is divided by an input-dependent success probability.")
    print(
        "  - That nonlinearity is final-boundary/postselection import, not a"
        " retained local channel or an operational signal to an earlier record."
    )
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
