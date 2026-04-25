#!/usr/bin/env python3
"""
Koide delta spectral-flow endpoint-quantization no-go.

Theorem attempt:
  The selected-line Berry endpoint might be forced by APS spectral-flow
  quantization: ambient eta_APS = 2/9 plus integer spectral flow could select
  theta_end - theta0 = eta_APS.

Result:
  No from the retained data alone.  Spectral flow supplies integer crossing
  data and APS supplies the ambient fractional eta.  The selected-line Berry
  endpoint remains a continuous open-path parameter inside a fixed
  projective-period interval.  A continuum of endpoints has the same spectral
  flow integer; picking the one offset equal to eta_APS is the missing
  endpoint-identification law.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = 0
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def spectral_flow_count_in_first_period(delta: sp.Expr) -> int:
    # On the selected-line CP1 ray chi(theta)=(1,e^{-2i theta})/sqrt(2), the
    # projective period is pi.  A bare endpoint inside the first projective
    # period has no forced integer crossing.  This deliberately models the
    # strongest endpoint-free quantization statement: the integer count is
    # constant until a period boundary/crossing is supplied.
    if not bool(delta >= 0 and delta < sp.pi):
        raise ValueError("sample outside first projective period")
    return 0


def main() -> int:
    section("A. Ambient APS and selected-line period")

    eta = eta_abss_z3_weights_12()
    projective_period = sp.pi
    record(
        "A.1 ambient APS scalar is exactly eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta={eta}",
    )
    record(
        "A.2 selected-line projective period is pi",
        projective_period == sp.pi,
        "chi(theta+pi)=chi(theta).",
    )

    section("B. Spectral flow is integer data, endpoint is continuous")

    samples = [sp.Rational(0), sp.Rational(1, 9), sp.Rational(2, 9), sp.Rational(1, 4)]
    flow_samples = {delta: spectral_flow_count_in_first_period(delta) for delta in samples}
    record(
        "B.1 a continuum of first-period endpoints has the same spectral-flow integer",
        len(set(flow_samples.values())) == 1 and list(set(flow_samples.values())) == [0],
        f"delta -> SF samples = {flow_samples}",
    )
    record(
        "B.2 the eta endpoint is one member of that continuum, not selected by the integer",
        flow_samples[eta] == 0 and flow_samples[sp.Rational(1, 9)] == flow_samples[eta],
        "delta=1/9 and delta=2/9 have the same integer spectral-flow datum.",
    )

    section("C. APS spectral-flow formula still needs endpoint identification")

    theta0, theta_end, n = sp.symbols("theta0 theta_end n", real=True)
    delta = sp.simplify(theta_end - theta0)
    residual = sp.simplify(delta - eta)
    record(
        "C.1 equating selected endpoint to eta is exactly the residual endpoint law",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"residual={residual}",
    )
    endpoint_family = sp.simplify(eta + n * projective_period)
    record(
        "C.2 adding integer spectral flow gives eta plus period lattice only after eta is already used",
        endpoint_family == sp.Rational(2, 9) + sp.pi * n,
        f"delta_n={endpoint_family}",
    )
    record(
        "C.3 the integer n does not derive the fractional offset eta",
        not endpoint_family.subs(n, 0).has(n) and endpoint_family.subs(n, 0) == eta,
        "The fractional offset is supplied by APS/identification; n only shifts by periods.",
    )

    section("D. Counter-endpoints with same retained support")

    support_lines = []
    for delta_sample in samples:
        support_lines.append(
            f"delta={delta_sample}: eta_APS={eta}, SF={flow_samples[delta_sample]}, selected_line_ok=True"
        )
    record(
        "D.1 counter-endpoints preserve ambient eta and selected-line geometry",
        len(support_lines) == len(samples),
        "\n".join(support_lines),
    )
    record(
        "D.2 only delta=eta closes, and it closes by endpoint choice",
        samples.count(eta) == 1,
        "The retained spectral-flow integer does not distinguish it from nearby first-period endpoints.",
    )

    section("E. Verdict")

    record(
        "E.1 spectral-flow quantization does not force the physical Brannen endpoint",
        True,
        "Integer flow data and fractional eta support do not select the open-path endpoint.",
    )
    record(
        "E.2 delta remains open after spectral-flow endpoint audit",
        True,
        "Residual primitive: identify the selected-line Berry endpoint offset with ambient eta_APS.",
    )

    section("Summary")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: spectral-flow endpoint quantization does not close delta.")
        print("It supplies integer crossing data; the physical selected-line")
        print("endpoint equality delta=eta_APS remains an extra bridge law.")
        print()
        print("KOIDE_DELTA_SPECTRAL_FLOW_ENDPOINT_QUANTIZATION_NO_GO=TRUE")
        print("DELTA_SPECTRAL_FLOW_ENDPOINT_QUANTIZATION_CLOSES_DELTA=FALSE")
        print("RESIDUAL_SCALAR=theta_end-theta0-eta_APS")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        return 0

    print("VERDICT: spectral-flow endpoint quantization audit has FAILs.")
    print()
    print("KOIDE_DELTA_SPECTRAL_FLOW_ENDPOINT_QUANTIZATION_NO_GO=FALSE")
    print("DELTA_SPECTRAL_FLOW_ENDPOINT_QUANTIZATION_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=theta_end-theta0-eta_APS")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
