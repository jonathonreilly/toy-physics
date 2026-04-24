#!/usr/bin/env python3
"""Validate the retained alpha_LM geometric-mean identity.

This runner is intentionally narrow. It checks the exact algebraic identity

    alpha_LM^2 = alpha_bare * alpha_s(v)

on the retained plaquette/coupling definitions, plus the equivalent
logarithmic and constant-ratio forms. It does not validate the separate
plaquette-value derivation or the downstream running bridge to alpha_s(M_Z).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, log, pi, sqrt

import sympy as sp
from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_ALPHA_S_V,
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
)


TOL = 1e-14


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def retained_values() -> dict[str, float]:
    return {
        "plaquette": CANONICAL_PLAQUETTE,
        "alpha_bare": CANONICAL_ALPHA_BARE,
        "u0": CANONICAL_U0,
        "alpha_lm": CANONICAL_ALPHA_LM,
        "alpha_s_v": CANONICAL_ALPHA_S_V,
    }


def near(left: float, right: float, *, rel_tol: float = TOL, abs_tol: float = TOL) -> bool:
    return isclose(left, right, rel_tol=rel_tol, abs_tol=abs_tol)


def add(checks: list[Check], name: str, passed: bool, detail: str) -> None:
    checks.append(Check(name=name, passed=passed, detail=detail))


def part_retained_numeric(checks: list[Check]) -> None:
    values = retained_values()
    plaquette = values["plaquette"]
    alpha_bare = values["alpha_bare"]
    u0 = values["u0"]
    alpha_lm = values["alpha_lm"]
    alpha_s_v = values["alpha_s_v"]

    add(
        checks,
        "retained plaquette is the packaged value",
        near(plaquette, 0.5934),
        f"<P>={plaquette:.16g}",
    )
    add(
        checks,
        "u0 is the retained plaquette fourth root",
        near(u0, plaquette ** 0.25),
        f"u0={u0:.17g}",
    )
    add(
        checks,
        "alpha_bare is 1/(4*pi)",
        near(alpha_bare, 1.0 / (4.0 * pi)),
        f"alpha_bare={alpha_bare:.17g}",
    )
    add(
        checks,
        "alpha_LM uses one power of u0",
        near(alpha_lm, alpha_bare / u0),
        f"alpha_LM={alpha_lm:.17g}",
    )
    add(
        checks,
        "alpha_s(v) uses two powers of u0",
        near(alpha_s_v, alpha_bare / (u0 * u0)),
        f"alpha_s(v)={alpha_s_v:.17g}",
    )


def part_identity_forms(checks: list[Check]) -> None:
    values = retained_values()
    alpha_bare = values["alpha_bare"]
    u0 = values["u0"]
    alpha_lm = values["alpha_lm"]
    alpha_s_v = values["alpha_s_v"]

    add(
        checks,
        "geometric mean identity at retained value",
        near(alpha_lm * alpha_lm, alpha_bare * alpha_s_v),
        f"alpha_LM^2={alpha_lm * alpha_lm:.17g}, alpha_bare*alpha_s(v)={alpha_bare * alpha_s_v:.17g}",
    )
    add(
        checks,
        "positive root form at retained value",
        near(alpha_lm, sqrt(alpha_bare * alpha_s_v)),
        f"alpha_LM={alpha_lm:.17g}, sqrt(product)={sqrt(alpha_bare * alpha_s_v):.17g}",
    )
    add(
        checks,
        "log-mean form at retained value",
        near(log(alpha_lm), 0.5 * (log(alpha_bare) + log(alpha_s_v))),
        f"log(alpha_LM)={log(alpha_lm):.17g}",
    )
    add(
        checks,
        "lower ratio is 1/u0",
        near(alpha_lm / alpha_bare, 1.0 / u0),
        f"alpha_LM/alpha_bare={alpha_lm / alpha_bare:.17g}",
    )
    add(
        checks,
        "upper ratio is 1/u0",
        near(alpha_s_v / alpha_lm, 1.0 / u0),
        f"alpha_s(v)/alpha_LM={alpha_s_v / alpha_lm:.17g}",
    )
    add(
        checks,
        "the two adjacent ratios match",
        near(alpha_lm / alpha_bare, alpha_s_v / alpha_lm),
        f"ratio={alpha_lm / alpha_bare:.17g}",
    )


def part_symbolic(checks: list[Check]) -> None:
    alpha, u = sp.symbols("alpha u", positive=True, finite=True, nonzero=True)
    alpha_lm = alpha / u
    alpha_s_v = alpha / (u * u)

    add(
        checks,
        "symbolic geometric identity",
        sp.simplify(alpha_lm**2 - alpha * alpha_s_v) == 0,
        str(sp.simplify(alpha_lm**2 - alpha * alpha_s_v)),
    )
    add(
        checks,
        "symbolic lower ratio",
        sp.simplify(alpha_lm / alpha - 1 / u) == 0,
        str(sp.simplify(alpha_lm / alpha - 1 / u)),
    )
    add(
        checks,
        "symbolic upper ratio",
        sp.simplify(alpha_s_v / alpha_lm - 1 / u) == 0,
        str(sp.simplify(alpha_s_v / alpha_lm - 1 / u)),
    )
    add(
        checks,
        "symbolic adjacent-ratio equality",
        sp.simplify(alpha_lm / alpha - alpha_s_v / alpha_lm) == 0,
        str(sp.simplify(alpha_lm / alpha - alpha_s_v / alpha_lm)),
    )
    add(
        checks,
        "symbolic no extra alpha_LM degree of freedom",
        sp.simplify(alpha_lm - sp.sqrt(alpha * alpha_s_v)) == 0,
        str(sp.simplify(alpha_lm - sp.sqrt(alpha * alpha_s_v))),
    )


def part_parametric_scan(checks: list[Check]) -> None:
    alpha_values = [1.0 / (4.0 * pi), 0.01, 0.125]
    u_values = [0.5, 0.75, 0.8776813811986843, 1.0, 1.25, 2.0]

    for alpha in alpha_values:
        for u0 in u_values:
            alpha_lm = alpha / u0
            alpha_s_v = alpha / (u0 * u0)
            passed = (
                near(alpha_lm * alpha_lm, alpha * alpha_s_v)
                and near(alpha_lm / alpha, 1.0 / u0)
                and near(alpha_s_v / alpha_lm, 1.0 / u0)
            )
            add(
                checks,
                f"parametric identity alpha={alpha:.6g}, u0={u0:.6g}",
                passed,
                f"delta={alpha_lm * alpha_lm - alpha * alpha_s_v:.3e}",
            )


def part_boundary_checks(checks: list[Check]) -> None:
    values = retained_values()
    alpha_bare = values["alpha_bare"]
    alpha_lm = values["alpha_lm"]
    alpha_s_v = values["alpha_s_v"]

    perturbed = alpha_lm * (1.0 + 1e-6)
    add(
        checks,
        "perturbing alpha_LM breaks the identity",
        not near(perturbed * perturbed, alpha_bare * alpha_s_v, rel_tol=1e-12, abs_tol=1e-12),
        f"relative perturbation=1e-6",
    )
    add(
        checks,
        "alpha_LM is fixed by alpha_bare and alpha_s(v)",
        near(alpha_lm, sqrt(alpha_bare * alpha_s_v)),
        "no independent alpha_LM knob remains on this definition surface",
    )
    add(
        checks,
        "runner scope excludes alpha_s(M_Z) bridge",
        True,
        "downstream running is separate from this algebraic identity",
    )
    add(
        checks,
        "runner scope excludes plaquette-value derivation",
        True,
        "the theorem uses the retained <P> value but does not derive it",
    )


def main() -> int:
    checks: list[Check] = []
    part_retained_numeric(checks)
    part_identity_forms(checks)
    part_symbolic(checks)
    part_parametric_scan(checks)
    part_boundary_checks(checks)

    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name}: {check.detail}")

    passed = sum(1 for check in checks if check.passed)
    failed = len(checks) - passed
    print(f"\nTOTAL: PASS={passed}, FAIL={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
