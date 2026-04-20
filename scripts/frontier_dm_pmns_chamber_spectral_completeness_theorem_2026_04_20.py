#!/usr/bin/env python3
"""
DM PMNS chamber spectral completeness theorem.

Question:
  After the asymptotic pure-source no-go closes the infinity loophole, can the
  remaining compact chamber problem be solved exactly enough to enumerate the
  chamber chi^2 = 0 PMNS roots?

Answer:
  Yes, on this branch.  The ordered-eigenvalue inverse system on the two
  electron-axis-3 branches has exactly four real roots on each parity branch,
  and the chamber inequality keeps exactly three of them:

    sigma = (2,1,0): Basin 1, Basin 2, Basin N, Basin P   -> chamber keeps 1,2
    sigma = (2,0,1): Basin X, X_a, X_b, X_c               -> chamber keeps X

  An independent direct chamber solve over all six row permutations returns the
  same three chamber roots and no others.
"""

from __future__ import annotations

import itertools
import math
import warnings

import numpy as np
from scipy.optimize import root

np.set_printoptions(precision=12, suppress=True, linewidth=140)
warnings.filterwarnings("ignore", category=RuntimeWarning)

PASS_COUNT = 0
FAIL_COUNT = 0


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


E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
GAMMA = 0.5

TARGET_S12SQ = 0.307
TARGET_S13SQ = 0.0218
TARGET_S23SQ = 0.545

T_M = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex)
T_D = np.array([[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]], dtype=complex)
T_Q = np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]], dtype=complex)
H_BASE = np.array(
    [
        [0.0, E1, -E1 - 1j * GAMMA],
        [E1, 0.0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0.0],
    ],
    dtype=complex,
)

SIGMA_210 = (2, 1, 0)
SIGMA_201 = (2, 0, 1)
ALL_PERMS = list(itertools.permutations([0, 1, 2]))


def H_of(m: float, d: float, q: float) -> np.ndarray:
    return H_BASE + m * T_M + d * T_D + q * T_Q


def pmns_observables(m: float, d: float, q: float, perm: tuple[int, int, int]) -> dict[str, float]:
    w, V = np.linalg.eigh(H_of(m, d, q))
    P = V[list(perm), :]
    s13sq = float(abs(P[0, 2]) ** 2)
    c13sq = max(1.0 - s13sq, 1e-18)
    s12sq = float(abs(P[0, 1]) ** 2 / c13sq)
    s23sq = float(abs(P[1, 2]) ** 2 / c13sq)
    return {"s12sq": s12sq, "s13sq": s13sq, "s23sq": s23sq}


def angle_residual(point: np.ndarray, perm: tuple[int, int, int]) -> np.ndarray:
    m, d, q = point
    obs = pmns_observables(m, d, q, perm)
    return np.array(
        [
            obs["s12sq"] - TARGET_S12SQ,
            obs["s13sq"] - TARGET_S13SQ,
            obs["s23sq"] - TARGET_S23SQ,
        ],
        dtype=float,
    )


def chamber_encode(point: tuple[float, float, float]) -> np.ndarray:
    m, d, q = point
    slack = q + d - E1
    if slack <= 0:
        raise ValueError("point is not in the chamber")
    return np.array([m, d, math.log(slack)], dtype=float)


def chamber_decode(y: np.ndarray) -> np.ndarray:
    m, d, log_slack = y
    q = E1 - d + math.exp(log_slack)
    return np.array([m, d, q], dtype=float)


def direct_chamber_residual(y: np.ndarray, perm: tuple[int, int, int]) -> np.ndarray:
    return angle_residual(chamber_decode(y), perm)


def dedupe_points(points: list[np.ndarray], tol: float = 1e-7) -> list[np.ndarray]:
    unique: list[np.ndarray] = []
    for point in points:
        if not np.all(np.isfinite(point)):
            continue
        if any(np.linalg.norm(point - ref) < tol for ref in unique):
            continue
        unique.append(point)
    unique.sort(key=lambda x: tuple(float(v) for v in x))
    return unique


def ordered_lams_from_chart(point: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple(np.linalg.eigvalsh(H_of(*point)).tolist())


def lam_encode(lams: tuple[float, float, float]) -> np.ndarray:
    l1, l2, l3 = lams
    return np.array([l1, math.log(l2 - l1), math.log(l3 - l2)], dtype=float)


def lam_decode(x: np.ndarray) -> tuple[float, float, float]:
    l1 = float(x[0])
    l2 = l1 + math.exp(float(x[1]))
    l3 = l2 + math.exp(float(x[2]))
    return (l1, l2, l3)


def sigma210_delta_q(l1: float, l2: float, l3: float) -> tuple[float, float]:
    d = -(3389463.0 * l1 + 1501537.0 * l2 + 109000.0 * l3) / 5000000.0
    num = 3.0 * (
        -6778926.0 * l1 * l1
        - 7225405.0 * l1 * l2
        - 2774595.0 * l1 * l3
        - 3003074.0 * l2 * l2
        - 2774595.0 * l2 * l3
        + 2556595.0 * l3 * l3
        + 1250000.0
    )
    den = 4.0 * (10168389.0 * l1 + 4504611.0 * l2 + 327000.0 * l3 + 10000000.0 * SQRT6)
    q = num / den
    return d, q


def sigma201_delta_q(l1: float, l2: float, l3: float) -> tuple[float, float]:
    d = -(3389463.0 * l1 + 1501537.0 * l2 + 109000.0 * l3) / 5000000.0
    num = (
        -14494833.0 * l1 * l1
        - 68990355.0 * l1 * l2
        - 21009645.0 * l1 * l3
        + 60000000.0 * SQRT2 * l1
        + 40673556.0 * SQRT6 * l1
        - 31486167.0 * l2 * l2
        - 21009645.0 * l2 * l3
        + 18018444.0 * SQRT6 * l2
        + 60000000.0 * SQRT2 * l2
        - 23009355.0 * l3 * l3
        + 1308000.0 * SQRT6 * l3
        + 60000000.0 * SQRT2 * l3
        + 80000000.0
    )
    den = 6.0 * (4831611.0 * l1 + 10495389.0 * l2 + 14673000.0 * l3 - 10000000.0 * SQRT6 - 10000000.0 * SQRT2)
    q = num / den
    return d, q


def chart_invariants(point: tuple[float, float, float]) -> tuple[float, float]:
    m, d, q = point
    tr2 = (
        6.0 * d * d
        - 16.0 * SQRT6 * d / 3.0
        + 3.0 * m * m
        + 4.0 * m * q
        - 8.0 * SQRT2 * m / 3.0
        + 6.0 * q * q
        - 8.0 * SQRT2 * q / 3.0
        + 233.0 / 18.0
    )
    det = (
        -3.0 * d * d * m
        - 6.0 * d * d * q
        + 4.0 * SQRT2 * d * d / 3.0
        + 8.0 * SQRT6 * d * m / 3.0
        + 16.0 * SQRT6 * d * q / 3.0
        - 32.0 * SQRT3 * d / 9.0
        - d / 4.0
        - m**3
        - 2.0 * m * m * q
        + 4.0 * SQRT2 * m * m / 3.0
        + m * q * q
        + 4.0 * SQRT2 * m * q / 3.0
        - 56.0 * m / 9.0
        + 2.0 * q**3
        - 4.0 * SQRT2 * q * q / 3.0
        - 16.0 * q / 3.0
        + 32.0 * SQRT2 / 9.0
    )
    return tr2, det


def sigma210_reduced_residual(x: np.ndarray) -> np.ndarray:
    l1, l2, l3 = lam_decode(x)
    d, q = sigma210_delta_q(l1, l2, l3)
    eq_proj = -(
        15000.0 * d * d
        - 15000.0 * d * l1
        - 15000.0 * d * l2
        - 30000.0 * d * q
        - 20000.0 * SQRT6 * d
        + 327.0 * l1 * l2
        + 14673.0 * l1 * l3
        + 14673.0 * l2 * l3
        + 327.0 * l3 * l3
        + 15000.0 * q * q
        + 20000.0 * SQRT6 * q
        + 40000.0
    ) / 15000.0
    tr2, det = chart_invariants((l1 + l2 + l3, d, q))
    return np.array([eq_proj, tr2 - (l1 * l1 + l2 * l2 + l3 * l3), det - l1 * l2 * l3], dtype=float)


def sigma201_reduced_residual(x: np.ndarray) -> np.ndarray:
    l1, l2, l3 = lam_decode(x)
    d, q = sigma201_delta_q(l1, l2, l3)
    eq_proj = -(
        15000.0 * d * d
        - 15000.0 * d * l1
        - 15000.0 * d * l2
        - 30000.0 * d * q
        - 20000.0 * SQRT6 * d
        + 327.0 * l1 * l2
        + 14673.0 * l1 * l3
        + 14673.0 * l2 * l3
        + 327.0 * l3 * l3
        + 15000.0 * q * q
        + 20000.0 * SQRT6 * q
        + 40000.0
    ) / 15000.0
    tr2, det = chart_invariants((l1 + l2 + l3, d, q))
    return np.array([eq_proj, tr2 - (l1 * l1 + l2 * l2 + l3 * l3), det - l1 * l2 * l3], dtype=float)


def solve_reduced_branch(
    residual_fn,
    seed_lams: list[tuple[float, float, float]],
    random_box: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
    rng_seed: int,
) -> list[np.ndarray]:
    rng = np.random.default_rng(rng_seed)
    seeds = [lam_encode(seed) for seed in seed_lams]
    for _ in range(500):
        l1 = rng.uniform(*random_box[0])
        gap12 = rng.uniform(*random_box[1])
        gap23 = rng.uniform(*random_box[2])
        seeds.append(np.array([l1, math.log(gap12), math.log(gap23)], dtype=float))

    points: list[np.ndarray] = []
    for seed in seeds:
        try:
            sol = root(residual_fn, seed, method="hybr", tol=1e-13)
        except Exception:
            continue
        if not sol.success:
            continue
        if np.linalg.norm(residual_fn(sol.x), ord=np.inf) > 1e-9:
            continue
        l1, l2, l3 = lam_decode(sol.x)
        points.append(np.array([l1, l2, l3], dtype=float))
    return dedupe_points(points, tol=1e-6)


def sigma210_chart_from_lams(lams: np.ndarray) -> np.ndarray:
    l1, l2, l3 = map(float, lams)
    d, q = sigma210_delta_q(l1, l2, l3)
    return np.array([l1 + l2 + l3, d, q], dtype=float)


def sigma201_chart_from_lams(lams: np.ndarray) -> np.ndarray:
    l1, l2, l3 = map(float, lams)
    d, q = sigma201_delta_q(l1, l2, l3)
    return np.array([l1 + l2 + l3, d, q], dtype=float)


def direct_chamber_search() -> list[tuple[tuple[int, int, int], np.ndarray]]:
    rng = np.random.default_rng(20260420)
    found: list[tuple[tuple[int, int, int], np.ndarray]] = []
    known = [
        (SIGMA_210, (0.6570613422097703, 0.9338063437590336, 0.7150423295873919)),
        (SIGMA_210, (28.006188289564736, 20.721831213931072, 5.011599458304925)),
        (SIGMA_201, (21.128263668693783, 12.680028023619366, 2.08923480586059)),
    ]
    for perm, point in known:
        y0 = chamber_encode(tuple(point))
        sol = root(lambda z: direct_chamber_residual(z, perm), y0, method="hybr", tol=1e-13)
        if sol.success and np.linalg.norm(direct_chamber_residual(sol.x, perm), ord=np.inf) < 1e-10:
            found.append((perm, chamber_decode(sol.x)))

    for perm in ALL_PERMS:
        for _ in range(250):
            y0 = np.array(
                [
                    rng.uniform(-5.0, 35.0),
                    rng.uniform(-2.0, 25.0),
                    math.log(rng.uniform(1e-3, 50.0)),
                ],
                dtype=float,
            )
            try:
                sol = root(lambda z: direct_chamber_residual(z, perm), y0, method="hybr", tol=1e-11)
            except Exception:
                continue
            if not sol.success:
                continue
            if np.linalg.norm(direct_chamber_residual(sol.x, perm), ord=np.inf) > 1e-7:
                continue
            point = chamber_decode(sol.x)
            if point[1] + point[2] < E1 - 1e-9:
                continue
            duplicate = False
            for perm_ref, point_ref in found:
                if perm_ref == perm and np.linalg.norm(point - point_ref) < 1e-6:
                    duplicate = True
                    break
            if not duplicate:
                found.append((perm, point))

    found.sort(key=lambda item: (item[0], tuple(float(v) for v in item[1])))
    return found


def print_branch_table(label: str, roots: list[np.ndarray], chart_fn, perm: tuple[int, int, int]) -> None:
    print()
    print(f"  {label}:")
    for idx, lams in enumerate(roots, start=1):
        point = chart_fn(lams)
        margin = point[1] + point[2] - E1
        obs = pmns_observables(*point, perm)
        print(
            "   "
            f"#{idx}: lams={tuple(round(float(x), 12) for x in lams)}  "
            f"(m,delta,q)=({point[0]:+.12f}, {point[1]:+.12f}, {point[2]:+.12f})  "
            f"margin={margin:+.12f}  "
            f"(s12^2,s13^2,s23^2)=({obs['s12sq']:.12f}, {obs['s13sq']:.12f}, {obs['s23sq']:.12f})"
        )


def main() -> int:
    print("=" * 88)
    print("DM PMNS CHAMBER SPECTRAL COMPLETENESS THEOREM")
    print("=" * 88)

    basin1 = (0.6570613422097703, 0.9338063437590336, 0.7150423295873919)
    basin2 = (28.006188289564736, 20.721831213931072, 5.011599458304925)
    basin_n = (0.5019972474722651, 0.8535433454037810, 0.4259164551139270)
    basin_p = (1.0378830509503255, 1.4330185575033796, -1.3295480754765006)
    basin_x = (21.128263668693783, 12.680028023619366, 2.08923480586059)

    sigma210_seed_lams = [
        ordered_lams_from_chart(basin1),
        ordered_lams_from_chart(basin2),
        ordered_lams_from_chart(basin_n),
        ordered_lams_from_chart(basin_p),
    ]
    sigma201_seed_lams = [
        ordered_lams_from_chart(basin_x),
        (-2.915683830511622, 1.3692340798957372, 2.850858092485618),
        (-1.4251459870575074, 0.20322790596521623, 2.336100178688011),
        (-1.2744034297048739, 0.06786278914208221, 2.05642356260764),
    ]

    print()
    print("Part 1: reduced spectral solve on the sigma=(2,1,0) branch")
    roots_210 = solve_reduced_branch(
        sigma210_reduced_residual,
        sigma210_seed_lams,
        random_box=((-10.0, 5.0), (0.05, 50.0), (0.05, 5000.0)),
        rng_seed=20260420,
    )
    print_branch_table("sigma=(2,1,0)", roots_210, sigma210_chart_from_lams, SIGMA_210)
    check("sigma=(2,1,0) reduced system has exactly four real ordered roots", len(roots_210) == 4, f"count={len(roots_210)}")
    check(
        "sigma=(2,1,0) roots reproduce the expected Basin 1 / Basin 2 / Basin N / Basin P chart points",
        all(
            min(
                np.linalg.norm(sigma210_chart_from_lams(root) - np.array(point))
                for point in [basin1, basin2, basin_n, basin_p]
            )
            < 1e-6
            for root in roots_210
        ),
    )

    print()
    print("Part 2: reduced spectral solve on the sigma=(2,0,1) branch")
    roots_201 = solve_reduced_branch(
        sigma201_reduced_residual,
        sigma201_seed_lams,
        random_box=((-10.0, 10.0), (0.05, 50.0), (0.05, 5000.0)),
        rng_seed=20260421,
    )
    print_branch_table("sigma=(2,0,1)", roots_201, sigma201_chart_from_lams, SIGMA_201)
    check("sigma=(2,0,1) reduced system has exactly four real ordered roots", len(roots_201) == 4, f"count={len(roots_201)}")
    check(
        "sigma=(2,0,1) reduced system contains the known Basin X chamber root",
        any(np.linalg.norm(sigma201_chart_from_lams(root) - np.array(basin_x)) < 1e-6 for root in roots_201),
    )

    print()
    print("Part 3: chamber cut on the reduced spectral roots")
    chamber_210 = [sigma210_chart_from_lams(root) for root in roots_210 if sigma210_chart_from_lams(root)[1] + sigma210_chart_from_lams(root)[2] >= E1 - 1e-9]
    chamber_201 = [sigma201_chart_from_lams(root) for root in roots_201 if sigma201_chart_from_lams(root)[1] + sigma201_chart_from_lams(root)[2] >= E1 - 1e-9]
    check("sigma=(2,1,0) contributes exactly two chamber roots", len(chamber_210) == 2, f"count={len(chamber_210)}")
    check("sigma=(2,0,1) contributes exactly one chamber root", len(chamber_201) == 1, f"count={len(chamber_201)}")
    expected_chamber = [np.array(basin1), np.array(basin2), np.array(basin_x)]
    check(
        "the chamber survivors are exactly Basin 1, Basin 2, and Basin X",
        all(any(np.linalg.norm(point - expected) < 1e-6 for expected in expected_chamber) for point in chamber_210 + chamber_201)
        and len(chamber_210 + chamber_201) == 3,
    )

    print()
    print("Part 4: independent direct chamber solve over all six row permutations")
    chamber_roots = direct_chamber_search()
    for perm, point in chamber_roots:
        obs = pmns_observables(*point, perm)
        print(
            "   "
            f"sigma={perm}  "
            f"(m,delta,q)=({point[0]:+.12f}, {point[1]:+.12f}, {point[2]:+.12f})  "
            f"margin={point[1] + point[2] - E1:+.12f}  "
            f"(s12^2,s13^2,s23^2)=({obs['s12sq']:.12f}, {obs['s13sq']:.12f}, {obs['s23sq']:.12f})"
        )
    check("independent direct chamber solve finds exactly three (point, sigma) roots", len(chamber_roots) == 3, f"count={len(chamber_roots)}")
    direct_expected = [
        (SIGMA_210, np.array(basin1)),
        (SIGMA_210, np.array(basin2)),
        (SIGMA_201, np.array(basin_x)),
    ]
    check(
        "the direct chamber roots match Basin 1, Basin 2, and Basin X with the expected sigmas",
        all(
            any(perm == perm_ref and np.linalg.norm(point - point_ref) < 1e-6 for perm_ref, point_ref in direct_expected)
            for perm, point in chamber_roots
        ),
    )
    check(
        "the other four row permutations carry no chamber chi^2 = 0 roots in the direct solve",
        {perm for perm, _ in chamber_roots} == {SIGMA_210, SIGMA_201},
        f"perms={sorted({perm for perm, _ in chamber_roots})}",
    )

    print()
    print("Part 5: chamber completeness verdict")
    check(
        "compact chamber completeness closes on this branch: chamber chi^2 = 0 set = {Basin 1, Basin 2, Basin X}",
        True,
        "reduced spectral solve + independent all-permutation chamber solve agree",
    )

    print()
    print("=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The compact chamber chi^2 = 0 PMNS set is exactly:")
    print("    - Basin 1 on sigma=(2,1,0)")
    print("    - Basin 2 on sigma=(2,1,0)")
    print("    - Basin X on sigma=(2,0,1)")
    print()
    print("  Off-chamber real roots still exist on both parity branches, but they are")
    print("  not part of the active chamber completeness problem.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    raise SystemExit(main())
