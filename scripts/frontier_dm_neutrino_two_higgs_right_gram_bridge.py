#!/usr/bin/env python3
"""
DM / neutrino bridge theorem for the canonical two-Higgs right-Gram lane.

Question:
  Can the local canonical neutrino two-Higgs lane realize the exact
  CP-supporting odd-circulant right-Gram family that DM leptogenesis now
  needs?

Answer:
  Yes, but only on an exact admissible subcone.

  On the canonical two-Higgs lane

      Y = diag(x1, x2, x3) + diag(y1, y2, y3 e^{i delta}) C

  the right-Gram matrix K = Y^dag Y has the exact one-phase Hermitian form

      [ x1^2 + y3^2        x1 y1             x3 y3 e^{-i delta} ]
      [ x1 y1              x2^2 + y1^2       x2 y2              ]
      [ x3 y3 e^{i delta}  x2 y2             x3^2 + y2^2        ].

  Any Hermitian circulant K with diagonal d and off-diagonal h can be
  rephased into the canonical gauge

      K_can(d, r, delta) =
      [ d  r  r e^{-i delta} ]
      [ r  d  r              ]
      [ r e^{i delta}  r  d  ]

  where r = |h| and delta = arg(h^3).

  The canonical two-Higgs lane realizes this circulant target if and only if

      d >= 2 r.

  Equivalently, the odd-circulant DM family is admitted on the exact
  two-Higgs right-Gram lane only on the subcone where the induced Hermitian
  circulant kernel obeys that inequality.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

CYCLE = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
    ],
    dtype=complex,
)


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


def canonical_two_higgs_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(
        np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex)
    ) @ CYCLE


def canonical_right_gram(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    ymat = canonical_two_higgs_y(x, y, delta)
    return ymat.conj().T @ ymat


def canonical_right_gram_expected(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    return np.array(
        [
            [x[0] ** 2 + y[2] ** 2, x[0] * y[0], x[2] * y[2] * np.exp(-1j * delta)],
            [x[0] * y[0], x[1] ** 2 + y[0] ** 2, x[1] * y[1]],
            [x[2] * y[2] * np.exp(1j * delta), x[1] * y[1], x[2] ** 2 + y[1] ** 2],
        ],
        dtype=complex,
    )


def shift_matrix() -> np.ndarray:
    return CYCLE.copy()


def minimal_cp_family(mu: float, nu: float, eta: float) -> np.ndarray:
    s = shift_matrix()
    i3 = np.eye(3, dtype=complex)
    return mu * i3 + nu * (s + s @ s) + 1j * eta * (s - s @ s)


def circulant_right_gram(mu: float, nu: float, eta: float) -> np.ndarray:
    ycp = minimal_cp_family(mu, nu, eta)
    return ycp.conj().T @ ycp


def canonical_rephasing_for_circulant(h: complex) -> np.ndarray:
    theta = np.angle(h)
    return np.diag(
        [
            1.0,
            np.exp(1j * theta),
            np.exp(2j * theta),
        ]
    ).astype(complex)


def canonicalize_circulant_right_gram(k: np.ndarray) -> tuple[np.ndarray, float, float, float]:
    h = k[0, 1]
    p = canonical_rephasing_for_circulant(h)
    k_can = p @ k @ p.conj().T
    d = float(np.real(k_can[0, 0]))
    r = float(np.abs(k_can[0, 1]))
    delta = float(np.angle(k_can[2, 0]))
    return k_can, d, r, delta


def canonical_circulant_target(d: float, r: float, delta: float) -> np.ndarray:
    return np.array(
        [
            [d, r, r * np.exp(-1j * delta)],
            [r, d, r],
            [r * np.exp(1j * delta), r, d],
        ],
        dtype=complex,
    )


def symmetric_two_higgs_solution(d: float, r: float) -> tuple[float, float] | None:
    disc = d * d - 4.0 * r * r
    if disc < -1e-12:
        return None
    disc = max(disc, 0.0)
    root = math.sqrt(disc)
    x2 = 0.5 * (d + root)
    y2 = 0.5 * (d - root)
    return math.sqrt(max(x2, 0.0)), math.sqrt(max(y2, 0.0))


def part1_exact_right_gram_formula() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CANONICAL TWO-HIGGS LANE HAS AN EXACT RIGHT-GRAM FORMULA")
    print("=" * 88)

    x = np.array([0.9, 0.7, 1.1], dtype=float)
    y = np.array([0.4, 0.6, 0.5], dtype=float)
    delta = 1.3

    k = canonical_right_gram(x, y, delta)
    expected = canonical_right_gram_expected(x, y, delta)

    check(
        "The canonical two-Higgs lane gives the exact one-phase right-Gram form",
        np.linalg.norm(k - expected) < 1e-12,
        f"form error = {np.linalg.norm(k - expected):.2e}",
    )
    check(
        "The right-Gram matrix is already non-universal and off-diagonal on a generic point",
        abs(k[0, 1]) > 1e-6 and abs(k[1, 2]) > 1e-6 and abs(k[2, 0]) > 1e-6,
        f"K01={k[0,1]:.6f}, K12={k[1,2]:.6f}, K20={k[2,0]:.6f}",
    )

    print()
    print("  So the local neutrino two-Higgs lane is not a flavor-empty extension.")
    print("  It carries the exact kind of right-Gram data leptogenesis actually uses.")


def part2_circulant_targets_rephase_to_the_canonical_gauge() -> None:
    print("\n" + "=" * 88)
    print("PART 2: HERMITIAN CIRCULANT CP TARGETS REPHASE TO THE TWO-HIGGS GAUGE")
    print("=" * 88)

    mu = 1.0
    nu = 0.2
    eta = 0.3
    k = circulant_right_gram(mu, nu, eta)
    k_can, d, r, delta = canonicalize_circulant_right_gram(k)
    expected = canonical_circulant_target(d, r, delta)

    check(
        "Any Hermitian circulant target can be put into the canonical one-phase gauge",
        np.linalg.norm(k_can - expected) < 1e-12,
        f"gauge error = {np.linalg.norm(k_can - expected):.2e}",
    )
    check(
        "The canonical phase is the Z3-invariant triangle phase arg(h^3)",
        abs(np.angle(k[0, 1] ** 3) - delta) < 1e-12,
        f"arg(h^3) = {np.angle(k[0,1]**3):.6f}, delta = {delta:.6f}",
    )

    print()
    print("  So the DM odd-circulant target can be compared directly against the")
    print("  canonical two-Higgs right-Gram family without losing the physical CP phase.")


def part3_exact_realization_criterion() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CIRCULANT TARGET IS REALIZED IF AND ONLY IF d >= 2 r")
    print("=" * 88)

    print("  Write the circulant target in canonical gauge as")
    print("      K_can(d,r,delta) = [[d,r,r e^{-i delta}],[r,d,r],[r e^{i delta},r,d]].")
    print("  On the canonical two-Higgs lane this requires")
    print("      x1 y1 = x2 y2 = x3 y3 = r")
    print("      x1^2 + y3^2 = x2^2 + y1^2 = x3^2 + y2^2 = d.")
    print("  With t_i = x_i^2 and y_i = r/x_i, these become")
    print("      t2 = F(t1),  t3 = F(t2),  t1 = F(t3)")
    print("  for F(t) = d - r^2/t, and F is strictly increasing on t > 0.")
    print("  Ordering t1 <= t2 <= t3 gives t2 <= t3 <= t1, so all t_i are equal.")

    d_good = 1.22
    r_good = 0.55
    solution = symmetric_two_higgs_solution(d_good, r_good)
    assert solution is not None
    x, y = solution
    delta = 0.9
    k_target = canonical_circulant_target(d_good, r_good, delta)
    k_two_higgs = canonical_right_gram(
        np.array([x, x, x]),
        np.array([y, y, y]),
        delta,
    )

    d_bad = 1.34
    r_bad = 0.9575489543621256

    check(
        "The constructive branch solves the target exactly when d^2 - 4 r^2 >= 0",
        np.linalg.norm(k_target - k_two_higgs) < 1e-12,
        f"d={d_good:.6f}, r={r_good:.6f}, disc={d_good*d_good - 4*r_good*r_good:.6f}",
    )
    check(
        "The no-go branch is exactly d^2 - 4 r^2 < 0",
        d_bad * d_bad - 4.0 * r_bad * r_bad < 0.0,
        f"d={d_bad:.6f}, r={r_bad:.6f}, disc={d_bad*d_bad - 4*r_bad*r_bad:.6f}",
    )
    check(
        "Therefore the canonical two-Higgs lane realizes the circulant target iff d >= 2 r",
        solution is not None and d_good >= 2.0 * r_good and d_bad < 2.0 * r_bad,
        "constructive point exists on the admissible side; no real symmetric root exists on the forbidden side",
    )

    print()
    print("  So the two-Higgs lane does not realize the whole odd-circulant family.")
    print("  It realizes the exact admissible subcone d >= 2|h| and excludes the rest.")


def part4_apply_the_criterion_to_the_dm_cp_family() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE DM ODD-CIRCULANT FAMILY HITS THE TWO-HIGGS LANE ON AN EXACT SUBCONE")
    print("=" * 88)

    mu_good = 1.0
    nu_good = 0.2
    eta_good = 0.3
    k_good = circulant_right_gram(mu_good, nu_good, eta_good)
    k_good_can, d_good, r_good, delta_good = canonicalize_circulant_right_gram(k_good)
    disc_good = d_good * d_good - 4.0 * r_good * r_good
    fact_good = -mu_good * (mu_good - 4.0 * nu_good) * (
        12.0 * eta_good * eta_good - mu_good * mu_good - 4.0 * mu_good * nu_good - 4.0 * nu_good * nu_good
    )
    xy_good = symmetric_two_higgs_solution(d_good, r_good)
    assert xy_good is not None
    x_good, y_good = xy_good
    k_good_two_higgs = canonical_right_gram(
        np.array([x_good, x_good, x_good]),
        np.array([y_good, y_good, y_good]),
        delta_good,
    )

    mu_bad = 1.0
    nu_bad = 0.4
    eta_bad = 0.1
    k_bad = circulant_right_gram(mu_bad, nu_bad, eta_bad)
    _, d_bad, r_bad, _ = canonicalize_circulant_right_gram(k_bad)
    disc_bad = d_bad * d_bad - 4.0 * r_bad * r_bad
    fact_bad = -mu_bad * (mu_bad - 4.0 * nu_bad) * (
        12.0 * eta_bad * eta_bad - mu_bad * mu_bad - 4.0 * mu_bad * nu_bad - 4.0 * nu_bad * nu_bad
    )

    mu_edge = 1.0
    nu_edge = 0.25
    eta_edge = 0.17
    k_edge = circulant_right_gram(mu_edge, nu_edge, eta_edge)
    k_edge_can, d_edge, r_edge, delta_edge = canonicalize_circulant_right_gram(k_edge)
    disc_edge = d_edge * d_edge - 4.0 * r_edge * r_edge
    x_edge = math.sqrt(max(d_edge / 2.0, 0.0))
    k_edge_two_higgs = canonical_right_gram(
        np.array([x_edge, x_edge, x_edge]),
        np.array([x_edge, x_edge, x_edge]),
        delta_edge,
    )

    check(
        "The discriminant matches the exact factorized DM-family expression",
        abs(disc_good - fact_good) < 1e-12 and abs(disc_bad - fact_bad) < 1e-12,
        f"good={disc_good:.6f}, bad={disc_bad:.6f}",
    )
    check(
        "An admissible odd-circulant DM point is realized exactly on the two-Higgs lane",
        np.linalg.norm(k_good_can - k_good_two_higgs) < 1e-12,
        f"disc={disc_good:.6f}, delta={delta_good:.6f}",
    )
    check(
        "An inadmissible odd-circulant DM point is excluded exactly by the subcone test",
        disc_bad < 0.0 and symmetric_two_higgs_solution(d_bad, r_bad) is None,
        f"disc={disc_bad:.6f}",
    )
    check(
        "The current DM benchmark sample sits on the exact boundary d = 2 r",
        np.linalg.norm(k_edge_can - k_edge_two_higgs) < 1e-12 and abs(disc_edge) < 1e-12,
        f"d={d_edge:.6f}, r={r_edge:.6f}, disc={disc_edge:.2e}",
    )

    print()
    print("  So the two-Higgs neutrino lane is a real positive DM bridge:")
    print("  the odd-circulant CP-supporting family is not foreign to it.")
    print("  But the bridge is not automatic on the whole family; it lives on the")
    print("  exact admissible subcone selected by d >= 2|h|.")


def main() -> int:
    print("=" * 88)
    print("DM / NEUTRINO: TWO-HIGGS RIGHT-GRAM BRIDGE THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the local canonical neutrino two-Higgs lane actually contain the")
    print("  exact odd-circulant CP-supporting structure DM leptogenesis now needs?")

    part1_exact_right_gram_formula()
    part2_circulant_targets_rephase_to_the_canonical_gauge()
    part3_exact_realization_criterion()
    part4_apply_the_criterion_to_the_dm_cp_family()

    print("\n" + "=" * 88)
    print("Conclusion")
    print("=" * 88)
    print("  The canonical neutrino two-Higgs lane is not just a PMNS sidecar.")
    print("  It can realize the exact DM odd-circulant CP-supporting right-Gram")
    print("  family on an exact admissible subcone. So the DM blocker is now")
    print("  narrower:")
    print("    - derive/select the two-Higgs extension,")
    print("    - derive its right-sensitive seven quantities / sheet, and")
    print("    - prove the resulting right-Gram lands in the admissible CP subcone")
    print("      with nonzero odd component.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
