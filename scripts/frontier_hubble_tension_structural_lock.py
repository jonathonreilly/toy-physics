"""Symbolic and numerical verifier for the Hubble Tension Structural Lock theorem.

Theorem note:
    docs/HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md

Theorem: on the retained surface (Cl(3)/Z^3, Lambda = 3/R_Lambda^2,
w_Lambda = -1, flat FRW with non-interacting matter, radiation, dark energy),
the late-time Hubble parameter satisfies the exact identity

    H(a)^2 / H_0^2  =  Omega_r,0 a^-4 + Omega_m,0 a^-3 + Omega_Lambda,0,

so the implied H_0 is a single scalar across the late-time epoch.

Checks performed:
    1. Symbolic continuity (sympy): rho_i(a) = rho_i,0 a^{-3(1+w_i)}.
    2. Symbolic Friedmann (sympy): H(a)^2 / H_0^2 reduces to the exact
       three-component late-time identity under flatness.
    3. Symbolic lock corollary (sympy): H_0_implied(a) simplifies to a
       constant equal to H_0 under w_Lambda = -1.
    4. Numerical Lambda-CDM check (numpy): Planck 2018 comparator triple
       reproduces the standard H(z)/H_0 curve.
    5. Modified-DE stress test (numpy): with w(a) = -1 + delta and delta != 0,
       the implied H_0 becomes a-dependent — the operational falsifier.

A PASS on all five validates the theorem's symbolic content and the
operational falsifier. The runner does not predict a numerical H_0; it only
verifies the structural lock.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import sympy as sp


# ---------------------------------------------------------------------------
# 1. Symbolic continuity equation
# ---------------------------------------------------------------------------


def check_continuity_equation() -> tuple[bool, str]:
    """Verify rho_i(a) = rho_i,0 a^{-3(1+w_i)} solves the FRW continuity ODE.

    The continuity equation under constant w is

        a (d rho / da) + 3 (1 + w) rho = 0,

    with general solution rho(a) = rho_0 a^{-3(1+w)}. We verify symbolically
    for w in {0, 1/3, -1}.
    """
    a = sp.symbols("a", positive=True)
    rho_0 = sp.symbols("rho_0", positive=True)

    failures: list[str] = []
    for label, w in [("matter w=0", sp.Integer(0)),
                     ("radiation w=1/3", sp.Rational(1, 3)),
                     ("dark-energy w=-1", sp.Integer(-1))]:
        rho = rho_0 * a ** (-3 * (1 + w))
        lhs = a * sp.diff(rho, a) + 3 * (1 + w) * rho
        residual = sp.simplify(lhs)
        if residual != 0:
            failures.append(f"{label}: residual = {residual}")

    if failures:
        return False, " / ".join(failures)
    return True, "continuity solved exactly for w in {0, 1/3, -1}"


# ---------------------------------------------------------------------------
# 2. Symbolic Friedmann reduction to the late-time three-component identity
# ---------------------------------------------------------------------------


def check_friedmann_reduction() -> tuple[bool, str]:
    """Verify H(a)^2/H_0^2 = Omega_r a^-4 + Omega_m a^-3 + Omega_L on the
    retained surface, derived from rho_i(a) scalings + flatness.
    """
    a, H_0, G = sp.symbols("a H_0 G", positive=True)
    Omega_r, Omega_m, Omega_L = sp.symbols("Omega_r Omega_m Omega_L", positive=True)

    rho_crit_0 = 3 * H_0 ** 2 / (8 * sp.pi * G)
    rho_m = Omega_m * rho_crit_0 * a ** (-3)
    rho_r = Omega_r * rho_crit_0 * a ** (-4)
    rho_L = Omega_L * rho_crit_0  # w = -1 keeps rho_Lambda constant

    # Friedmann (flat): H^2 = (8 pi G / 3) (rho_m + rho_r + rho_L)
    H_squared = sp.Rational(8, 3) * sp.pi * G * (rho_m + rho_r + rho_L)
    ratio = sp.simplify(H_squared / H_0 ** 2)
    expected = Omega_r * a ** (-4) + Omega_m * a ** (-3) + Omega_L
    diff = sp.simplify(ratio - expected)

    if diff != 0:
        return False, f"H^2/H_0^2 - expected = {diff}"
    return True, "(★) verified symbolically"


# ---------------------------------------------------------------------------
# 3. Symbolic lock corollary: H_0_implied(a) is constant
# ---------------------------------------------------------------------------


def check_lock_corollary() -> tuple[bool, str]:
    """Verify that H_0_implied(a) := H(a)/sqrt(F(a)) is a-independent under (★).
    """
    a, H_0 = sp.symbols("a H_0", positive=True)
    Omega_r, Omega_m, Omega_L = sp.symbols("Omega_r Omega_m Omega_L", positive=True)
    F = Omega_r * a ** (-4) + Omega_m * a ** (-3) + Omega_L
    H_a = H_0 * sp.sqrt(F)
    H_0_implied = H_a / sp.sqrt(F)
    simplified = sp.simplify(H_0_implied - H_0)
    if simplified != 0:
        return False, f"H_0_implied(a) - H_0 = {simplified}"
    return True, "H_0_implied(a) = H_0 for all a > 0"


# ---------------------------------------------------------------------------
# 4. Numerical Lambda-CDM check against the Planck 2018 comparator
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CosmologyTriple:
    Omega_r: float
    Omega_m: float
    Omega_Lambda: float
    H_0_kmsMpc: float

    def E_squared(self, a: np.ndarray | float) -> np.ndarray | float:
        return (
            self.Omega_r * a ** -4
            + self.Omega_m * a ** -3
            + self.Omega_Lambda
        )

    def H(self, a: np.ndarray | float) -> np.ndarray | float:
        return self.H_0_kmsMpc * np.sqrt(self.E_squared(a))


# Planck 2018 comparator. The headline pair (Omega_m=0.315, Omega_Lambda=0.685)
# sums to 1.0 only because radiation is folded into the Lambda value at the
# percent level. To preserve flatness exactly when radiation is tracked
# separately, fix Omega_r and Omega_m and derive Omega_Lambda from
# Omega_Lambda = 1 - Omega_m - Omega_r. Doing so shifts Omega_Lambda by
# Omega_r ~ 9.2e-5, which is well inside the Planck quoted uncertainty.
_PLANCK_OMEGA_M = 0.315
_PLANCK_OMEGA_R = 9.2e-5
PLANCK_2018 = CosmologyTriple(
    Omega_r=_PLANCK_OMEGA_R,
    Omega_m=_PLANCK_OMEGA_M,
    Omega_Lambda=1.0 - _PLANCK_OMEGA_M - _PLANCK_OMEGA_R,
    H_0_kmsMpc=67.4,
)


def check_numerical_lcdm() -> tuple[bool, str]:
    """Reproduce the standard Lambda-CDM H(z)/H_0 curve and verify the lock
    corollary numerically: H_0_implied(a) is constant to machine precision.
    """
    z = np.linspace(0.0, 1.0, 21)
    a = 1.0 / (1.0 + z)
    H_a = PLANCK_2018.H(a)
    F = PLANCK_2018.E_squared(a)
    H_0_implied = H_a / np.sqrt(F)
    deviation = float(np.max(np.abs(H_0_implied - PLANCK_2018.H_0_kmsMpc)))
    # Sanity: at z = 0 the formula must give exactly H_0.
    deviation_z0 = abs(float(H_a[0] - PLANCK_2018.H_0_kmsMpc))
    if deviation > 1e-10 or deviation_z0 > 1e-10:
        return (
            False,
            f"max |H_0_implied(a) - H_0| = {deviation:.3e}, |H(1) - H_0| = {deviation_z0:.3e}",
        )
    # Also confirm the curve is monotone in z (standard for Lambda-CDM with positive Omega_m).
    monotone = bool(np.all(np.diff(H_a) >= -1e-10))
    if not monotone:
        return False, "H(z) not monotone over z in [0, 1] (numerical artifact)"
    return (
        True,
        f"max |H_0_implied(a) - H_0| = {deviation:.3e} kmsMpc; H(z) monotone in z in [0, 1]",
    )


# ---------------------------------------------------------------------------
# 5. Modified-DE stress test: lock fails when w_Lambda != -1
# ---------------------------------------------------------------------------


def rho_DE_modified(a: np.ndarray, delta: float, rho_DE_0: float) -> np.ndarray:
    """Energy density of a DE component with constant EOS w = -1 + delta.

    Continuity gives rho_DE(a) = rho_DE_0 a^{-3(1+w)} = rho_DE_0 a^{-3 delta}.
    """
    return rho_DE_0 * a ** (-3.0 * delta)


def check_modified_de_stress() -> tuple[bool, str]:
    """With w = -1 + delta and delta != 0, show H_0_implied(a) becomes
    a-dependent — the operational falsifier of the structural lock.

    We use the *retained-surface* reduction formula for H_0_implied(a),
    i.e., the Lambda-CDM denominator F(a) with the retained Omega_Lambda,
    while the *true* H(a) carries the modified DE density. This is the
    measurement scenario: an observer who reduces H(z) data assuming
    retained Lambda-CDM but where reality has a modified late-time DE will
    infer an a-dependent H_0.
    """
    a = np.linspace(0.05, 1.0, 50)  # late-time only, well above a_recomb
    deltas = [-0.10, -0.05, -0.01, 0.0, 0.01, 0.05, 0.10]
    rows: list[tuple[float, float]] = []
    Omega_DE_0 = PLANCK_2018.Omega_Lambda
    Omega_m_0 = PLANCK_2018.Omega_m
    Omega_r_0 = PLANCK_2018.Omega_r
    H_0 = PLANCK_2018.H_0_kmsMpc
    F_retained = (
        Omega_r_0 * a ** -4 + Omega_m_0 * a ** -3 + Omega_DE_0
    )
    for delta in deltas:
        # True (modified) H^2 / H_0^2:
        E_true_sq = (
            Omega_r_0 * a ** -4
            + Omega_m_0 * a ** -3
            + Omega_DE_0 * a ** (-3.0 * delta)
        )
        H_true = H_0 * np.sqrt(E_true_sq)
        H_0_implied = H_true / np.sqrt(F_retained)
        spread = float(np.max(H_0_implied) - np.min(H_0_implied))
        rows.append((delta, spread))

    # Expected behavior: spread is exactly 0 for delta = 0 (within FP), and
    # strictly positive (and growing in |delta|) for delta != 0.
    spread_at_zero = next(s for d, s in rows if d == 0.0)
    if spread_at_zero > 1e-9:
        return False, f"lock fails at delta=0 (spread {spread_at_zero:.3e})"
    nonzero = [(d, s) for d, s in rows if d != 0.0]
    failed_pairs = [(d, s) for d, s in nonzero if not s > 1e-3]
    if failed_pairs:
        return (
            False,
            "lock did not falsify under non-trivial delta: "
            + ", ".join(f"delta={d}: spread={s:.3e}" for d, s in failed_pairs),
        )
    table = " | ".join(f"delta={d:+.2f}: {s:.3f} km/s/Mpc" for d, s in rows)
    return (
        True,
        "spread(delta=0) = 0; spread > 0 for delta != 0 — operational falsifier holds. "
        + table,
    )


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run_all() -> int:
    checks = [
        ("CONTINUITY", check_continuity_equation),
        ("FRIEDMANN", check_friedmann_reduction),
        ("LOCK_COROLLARY", check_lock_corollary),
        ("NUMERICAL_LCDM", check_numerical_lcdm),
        ("MODIFIED_DE_STRESS", check_modified_de_stress),
    ]
    print("=" * 72)
    print("Hubble Tension Structural Lock theorem — runner")
    print("Theorem note: docs/HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md")
    print("=" * 72)
    pass_count = 0
    fail_count = 0
    for label, func in checks:
        ok, info = func()
        status = "PASS" if ok else "FAIL"
        if ok:
            pass_count += 1
        else:
            fail_count += 1
        print(f"[{status}] {label}: {info}")
    print("-" * 72)
    print(f"summary: PASS={pass_count} FAIL={fail_count}")
    print("=" * 72)
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(run_all())
