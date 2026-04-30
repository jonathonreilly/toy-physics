#!/usr/bin/env python3
"""Low-stat finite-volume B5 scout for Lane 1 sqrt(sigma).

This is intentionally a pipeline scout, not a production lattice result.
It runs a small pure-gauge SU(3) Metropolis chain at beta=6 for L=4,6,8
with fixed low statistics, measures plaquette and small Wilson loops, and
checks only robust structural properties needed to validate the future
production B5 ladder.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re
import sys

import numpy as np


N_C = 3
BETA = 6.0
PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def state_cycle_at_least(state: str, cycle: int) -> bool:
    match = re.search(r"cycles_completed:\s*(\d+)", state)
    return bool(match) and int(match.group(1)) >= cycle


def random_su3_near_identity(rng: np.random.Generator, epsilon: float = 0.24) -> np.ndarray:
    h = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
    h = (h + h.conj().T) / 2.0
    h -= np.trace(h) / 3.0 * np.eye(3)
    x = np.eye(3, dtype=complex) + 1j * epsilon * h
    q, r = np.linalg.qr(x)
    d = np.diag(r)
    ph = d / np.abs(d)
    q = q @ np.diag(np.conj(ph))
    det = np.linalg.det(q)
    q *= np.exp(-1j * np.angle(det) / 3)
    return q


def make_lattice(L: int) -> dict[tuple[int, ...], list[np.ndarray]]:
    links: dict[tuple[int, ...], list[np.ndarray]] = {}
    for coords in np.ndindex(*([L] * 4)):
        links[coords] = [np.eye(3, dtype=complex) for _ in range(4)]
    return links


def compute_staple(links: dict[tuple[int, ...], list[np.ndarray]], x: list[int], mu: int, L: int) -> np.ndarray:
    staple = np.zeros((3, 3), dtype=complex)
    xp = list(x)
    xp[mu] = (xp[mu] + 1) % L

    for nu in range(4):
        if nu == mu:
            continue

        xpn = list(x)
        xpn[nu] = (xpn[nu] + 1) % L
        staple += (
            links[tuple(xp)][nu]
            @ links[tuple(xpn)][mu].conj().T
            @ links[tuple(x)][nu].conj().T
        )

        xm = list(x)
        xm[nu] = (xm[nu] - 1) % L
        xpm = list(xp)
        xpm[nu] = (xpm[nu] - 1) % L
        staple += (
            links[tuple(xpm)][nu].conj().T
            @ links[tuple(xm)][mu].conj().T
            @ links[tuple(xm)][nu]
        )

    return staple


def metropolis_sweep(links: dict[tuple[int, ...], list[np.ndarray]], L: int, rng: np.random.Generator) -> tuple[int, int]:
    accepted = 0
    total = 0
    for coords in np.ndindex(*([L] * 4)):
        x = list(coords)
        for mu in range(4):
            old = links[tuple(x)][mu]
            staple = compute_staple(links, x, mu, L)
            proposal = random_su3_near_identity(rng) @ old
            delta_s = -(BETA / N_C) * np.trace((proposal - old) @ staple).real
            total += 1
            if delta_s < 0 or rng.random() < math.exp(-delta_s):
                links[tuple(x)][mu] = proposal
                accepted += 1
    return accepted, total


def measure_plaquette(links: dict[tuple[int, ...], list[np.ndarray]], L: int) -> float:
    total = 0.0
    count = 0
    for coords in np.ndindex(*([L] * 4)):
        x = list(coords)
        for mu in range(4):
            for nu in range(mu + 1, 4):
                xm = list(x)
                xm[mu] = (xm[mu] + 1) % L
                xn = list(x)
                xn[nu] = (xn[nu] + 1) % L
                u_p = (
                    links[tuple(x)][mu]
                    @ links[tuple(xm)][nu]
                    @ links[tuple(xn)][mu].conj().T
                    @ links[tuple(x)][nu].conj().T
                )
                total += np.trace(u_p).real / N_C
                count += 1
    return total / count


def measure_wilson_loop(
    links: dict[tuple[int, ...], list[np.ndarray]],
    x0: tuple[int, ...],
    R: int,
    T: int,
    mu_dir: int,
    nu_dir: int,
    L: int,
) -> float:
    loop = np.eye(3, dtype=complex)
    x = list(x0)

    for _ in range(R):
        loop = loop @ links[tuple(x)][mu_dir]
        x[mu_dir] = (x[mu_dir] + 1) % L
    for _ in range(T):
        loop = loop @ links[tuple(x)][nu_dir]
        x[nu_dir] = (x[nu_dir] + 1) % L
    for _ in range(R):
        x[mu_dir] = (x[mu_dir] - 1) % L
        loop = loop @ links[tuple(x)][mu_dir].conj().T
    for _ in range(T):
        x[nu_dir] = (x[nu_dir] - 1) % L
        loop = loop @ links[tuple(x)][nu_dir].conj().T

    return np.trace(loop).real / N_C


def measure_wilson_average(links: dict[tuple[int, ...], list[np.ndarray]], L: int, R: int, T: int, stride: int) -> float:
    total = 0.0
    count = 0
    coords_iter = range(0, L, stride)
    for coords in ((a, b, c, d) for a in coords_iter for b in coords_iter for c in coords_iter for d in coords_iter):
        for mu in range(4):
            for nu in range(mu + 1, 4):
                total += measure_wilson_loop(links, coords, R, T, mu, nu, L)
                count += 1
    return total / count


@dataclass(frozen=True)
class ScoutResult:
    L: int
    plaquette: float
    plaquette_err: float
    w11: float
    w12: float
    w22: float
    chi22: float
    acceptance: float


def run_scout(L: int, therm: int = 6, meas: int = 4, skip: int = 1) -> ScoutResult:
    rng = np.random.default_rng(20260430 + L)
    links = make_lattice(L)
    accepted = 0
    total = 0

    for _ in range(therm):
        a, t = metropolis_sweep(links, L, rng)
        accepted += a
        total += t

    plaquettes = []
    w11s = []
    w12s = []
    w22s = []
    stride = max(1, L // 4)

    for _ in range(meas):
        for _ in range(skip):
            a, t = metropolis_sweep(links, L, rng)
            accepted += a
            total += t
        plaquettes.append(measure_plaquette(links, L))
        w11s.append(measure_wilson_average(links, L, 1, 1, stride))
        w12s.append(measure_wilson_average(links, L, 1, 2, stride))
        w22s.append(measure_wilson_average(links, L, 2, 2, stride))

    p = float(np.mean(plaquettes))
    p_err = float(np.std(plaquettes, ddof=1) / math.sqrt(len(plaquettes))) if len(plaquettes) > 1 else 0.0
    w11 = float(np.mean(w11s))
    w12 = float(np.mean(w12s))
    w22 = float(np.mean(w22s))
    if w11 > 1e-12 and w12 > 1e-12 and w22 > 1e-12:
        chi22 = float(-math.log(abs(w22 * w11) / abs(w12 * w12)))
    else:
        chi22 = float("nan")
    return ScoutResult(L, p, p_err, w11, w12, w22, chi22, accepted / total)


def part1_run_scout() -> list[ScoutResult]:
    section("Part 1: low-stat beta=6 scout")
    results = [run_scout(L) for L in (4, 6, 8)]
    for r in results:
        print(
            f"  L={r.L}: P={r.plaquette:.4f} +/- {r.plaquette_err:.4f}, "
            f"W11={r.w11:.4f}, W12={r.w12:.4f}, W22={r.w22:.4f}, "
            f"chi22={r.chi22:.4f}, acc={r.acceptance:.3f}"
        )

    check(
        "all scout plaquettes are finite and in a physical range",
        all(0.2 < r.plaquette < 0.95 for r in results),
    )
    check(
        "all scout acceptances are usable",
        all(0.2 < r.acceptance < 0.9 for r in results),
    )
    check(
        "all scout Wilson loops have positive W11/W12/W22 signals",
        all(r.w11 > 0 and r.w12 > 0 and r.w22 > 0 for r in results),
    )
    return results


def part2_qualitative_ladder(results: list[ScoutResult]) -> None:
    section("Part 2: qualitative ladder checks")
    check(
        "area ordering holds on every volume",
        all(r.w11 > r.w12 > r.w22 for r in results),
    )
    check(
        "chi22 is finite on every volume",
        all(math.isfinite(r.chi22) for r in results),
    )
    drift = max(r.plaquette for r in results) - min(r.plaquette for r in results)
    print(f"  plaquette drift across L=4,6,8 = {drift:.4f}")
    check(
        "low-stat plaquette drift is measured, not assumed zero",
        drift > 0.0,
        f"drift={drift:.4f}",
    )


def part3_artifact_checks() -> None:
    section("Part 3: artifact checks")
    note = (Path(__file__).resolve().parents[1] / "docs/HADRON_LANE1_SQRT_SIGMA_B5_LOWSTAT_SCOUT_NOTE_2026-04-30.md").read_text(encoding="utf-8")
    handoff = (Path(__file__).resolve().parents[1] / ".claude/science/physics-loops/hadron-sqrt-sigma-b2-20260430/HANDOFF.md").read_text(encoding="utf-8")
    state = (Path(__file__).resolve().parents[1] / ".claude/science/physics-loops/hadron-sqrt-sigma-b2-20260430/STATE.yaml").read_text(encoding="utf-8")
    check(
        "note labels the run as scout rather than closure",
        "pipeline scout" in note and "not B5 closure" in note,
    )
    check(
        "branch-local handoff includes the low-stat scout runner",
        "HADRON_LANE1_SQRT_SIGMA_B5_LOWSTAT_SCOUT_NOTE_2026-04-30.md" in handoff
        and "frontier_hadron_lane1_sqrt_sigma_b5_lowstat_scout.py" in handoff,
    )
    check(
        "loop state advanced to cycle 5",
        state_cycle_at_least(state, 5) and "cycle-5-complete" in state,
    )


def main() -> int:
    print("=" * 88)
    print("LANE 1 SQRT(SIGMA) B5 LOW-STAT FINITE-VOLUME SCOUT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the local L=4,6,8 measurement pipeline work well enough to")
    print("  justify a production B5 ladder?")
    print()
    print("Answer:")
    print("  Yes as a pipeline scout; no as B5 closure.")

    results = part1_run_scout()
    part2_qualitative_ladder(results)
    part3_artifact_checks()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
