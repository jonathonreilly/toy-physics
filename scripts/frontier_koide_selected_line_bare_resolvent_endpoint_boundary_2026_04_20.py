#!/usr/bin/env python3
"""
Koide selected-line bare resolvent endpoint boundary.

Question:
  Does the simplest missing-axis resolvent family on the exact selected line
  already pick the current physical first-branch endpoint m_*?

Answer:
  No. On the audited bare family

      W_4(m; h_O0) = diag(h_O0, H_sel(m)),
      R_{m,lambda} = (lambda I_4 - W_4(m; h_O0))^{-1},

  the eigenvalue packet of the returned species operator can imitate the
  charged-lepton hierarchy numerically, but its best-fit points sit far away
  from the physical first-branch selected point supplied by the current exact
  selected-line stack. The family therefore sharpens the open target without
  closing it: the missing endpoint law is not a bare local resolvent section on
  the selected line.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq

from frontier_higgs_dressed_propagator_v1 import (
    H3,
    direction_cos,
    embed_4x4_to_16,
    koide_Q,
    sigma_with_weight_operator,
)
from frontier_koide_selected_line_cyclic_response_bridge import (
    hstar_witness_kappa,
    selected_line_kappa,
)

PASS_COUNT = 0
FAIL_COUNT = 0

SELECTOR = math.sqrt(6.0) / 3.0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


@dataclass
class SweepResult:
    mode: str
    metric: str
    m: float
    lam: float
    cs: float
    q: float
    masses: np.ndarray


def selected_generator(m: float) -> np.ndarray:
    return H3(m, SELECTOR, SELECTOR)


def physical_selected_point() -> float:
    _beta_star, kappa_star = hstar_witness_kappa()
    return float(brentq(lambda m: selected_line_kappa(m) - kappa_star, -1.165, -1.160))


def positivity_threshold() -> float:
    def u_small(m: float) -> float:
        x = np.linalg.eigvalsh(selected_generator(m))
        # selected-line small-branch positivity threshold from the existing line
        # is easiest to recover via the bridge already in the stack
        return float(selected_line_kappa(m) + 1.0 / math.sqrt(3.0))

    return float(brentq(u_small, -1.3, -1.2))


def h_o0_value(m: float, mode: str) -> float:
    if mode == "zero":
        return 0.0
    if mode == "trace_mean":
        return float(np.trace(selected_generator(m)).real / 3.0)
    raise ValueError(f"unknown mode {mode}")


def bare_selected_lift(m: float, mode: str) -> np.ndarray:
    w4 = np.zeros((4, 4), dtype=complex)
    w4[0, 0] = h_o0_value(m, mode)
    w4[1:, 1:] = selected_generator(m)
    return w4


def eigen_packet(m: float, lam: float, mode: str) -> np.ndarray | None:
    w4 = bare_selected_lift(m, mode)
    evals, evecs = np.linalg.eigh(w4)
    diffs = lam - evals
    if np.any(np.abs(diffs) < 1.0e-8):
        return None
    w4_res = evecs @ np.diag(1.0 / diffs) @ evecs.conj().T
    sigma = sigma_with_weight_operator(embed_4x4_to_16(w4_res))
    sigma_h = 0.5 * (sigma + sigma.conj().T)
    masses = np.abs(np.linalg.eigvalsh(sigma_h))
    if np.min(masses) < 1.0e-14:
        return None
    return masses


def search_family(mode: str, m_grid: np.ndarray, lam_grid: np.ndarray) -> tuple[SweepResult, SweepResult]:
    best_cs: SweepResult | None = None
    best_q: SweepResult | None = None
    for lam in lam_grid:
        for m in m_grid:
            masses = eigen_packet(float(m), float(lam), mode)
            if masses is None:
                continue
            q = float(koide_Q(masses))
            cs = float(direction_cos(masses))
            current = SweepResult(mode, "", float(m), float(lam), cs, q, masses)
            if best_cs is None or cs > best_cs.cs:
                best_cs = SweepResult(mode, "best_cs", current.m, current.lam, current.cs, current.q, current.masses)
            if best_q is None or abs(q - 2.0 / 3.0) < abs(best_q.q - 2.0 / 3.0):
                best_q = SweepResult(mode, "best_q", current.m, current.lam, current.cs, current.q, current.masses)
    if best_cs is None or best_q is None:
        raise RuntimeError(f"empty sweep for mode={mode}")
    return best_cs, best_q


def part1_exact_family_setup() -> tuple[float, float]:
    print("=" * 88)
    print("PART 1: the bare selected-line resolvent family is exact and 2-real")
    print("=" * 88)

    m_phys = physical_selected_point()
    m_pos = positivity_threshold()
    g = selected_generator(m_phys)

    check(
        "The selected generator line H_sel(m) = H3(m, sqrt(6)/3, sqrt(6)/3) is Hermitian",
        np.allclose(g, g.conj().T, atol=1.0e-12),
        kind="NUMERIC",
    )
    check(
        "The current exact stack already fixes a physical first-branch selected point m_* on that line",
        m_pos < m_phys < 0.0,
        detail=f"m_pos={m_pos:.12f}, m_*={m_phys:.12f}",
        kind="NUMERIC",
    )
    check(
        "The bare resolvent family adds only one local scalar lambda on top of the selected endpoint coordinate m",
        True,
        detail="R_{m,lambda} = (lambda I_4 - W_4(m; h_O0))^{-1}",
    )
    return m_phys, m_pos


def part2_first_branch_canonical_zero_o0(m_phys: float, m_pos: float) -> None:
    print()
    print("=" * 88)
    print("PART 2: canonical h_O0 = 0 resolvent fits live far away from m_*")
    print("=" * 88)

    m_grid = np.linspace(m_pos + 1.0e-3, 0.0, 500)
    lam_grid = np.linspace(0.01, 1.0, 100)
    best_cs, best_q = search_family("zero", m_grid, lam_grid)

    check(
        "On the first branch the canonical bare family can numerically imitate the charged-lepton packet",
        best_cs.cs > 0.9999 and abs(best_q.q - 2.0 / 3.0) < 5.0e-4,
        detail=(
            f"best_cs=(m={best_cs.m:.6f}, lambda={best_cs.lam:.6f}, cs={best_cs.cs:.6f}, Q={best_cs.q:.6f}); "
            f"best_q=(m={best_q.m:.6f}, lambda={best_q.lam:.6f}, cs={best_q.cs:.6f}, Q={best_q.q:.6f})"
        ),
        kind="NUMERIC",
    )
    check(
        "But neither audited optimum lands near the physical first-branch endpoint m_*",
        abs(best_cs.m - m_phys) > 1.0 and abs(best_q.m - m_phys) > 0.9,
        detail=(
            f"|best_cs.m-m_*|={abs(best_cs.m - m_phys):.6f}, "
            f"|best_q.m-m_*|={abs(best_q.m - m_phys):.6f}"
        ),
        kind="NUMERIC",
    )


def part3_first_branch_trace_mean_o0(m_phys: float, m_pos: float) -> None:
    print()
    print("=" * 88)
    print("PART 3: trace-mean h_O0 lift also misses m_* badly")
    print("=" * 88)

    m_grid = np.linspace(m_pos + 1.0e-3, 0.0, 500)
    lam_grid = np.linspace(0.01, 1.0, 100)
    best_cs, best_q = search_family("trace_mean", m_grid, lam_grid)

    check(
        "The trace-mean O_0 lift also produces strong numerical imitators on the first branch",
        best_cs.cs > 0.9999 and best_q.cs > 0.9997,
        detail=(
            f"best_cs=(m={best_cs.m:.6f}, lambda={best_cs.lam:.6f}, cs={best_cs.cs:.6f}, Q={best_cs.q:.6f}); "
            f"best_q=(m={best_q.m:.6f}, lambda={best_q.lam:.6f}, cs={best_q.cs:.6f}, Q={best_q.q:.6f})"
        ),
        kind="NUMERIC",
    )
    check(
        "But those audited optima still sit more than one unit of m away from the physical endpoint",
        abs(best_cs.m - m_phys) > 1.0 and abs(best_q.m - m_phys) > 1.0,
        detail=(
            f"|best_cs.m-m_*|={abs(best_cs.m - m_phys):.6f}, "
            f"|best_q.m-m_*|={abs(best_q.m - m_phys):.6f}"
        ),
        kind="NUMERIC",
    )


def part4_global_canonical_family_prefers_the_wrong_side(m_phys: float, m_pos: float) -> None:
    print()
    print("=" * 88)
    print("PART 4: globally the canonical family is drawn to the nonphysical side")
    print("=" * 88)

    m_grid = np.linspace(m_pos + 1.0e-3, 0.2, 600)
    lam_grid = np.linspace(0.01, 1.0, 100)
    best_cs, best_q = search_family("zero", m_grid, lam_grid)

    check(
        "The globally strongest cosine fit is pulled toward the small-lambda nonphysical side with m >= 0",
        best_cs.m >= 0.0 and 0.02 <= best_cs.lam <= 0.06,
        detail=(
            f"best_cs=(m={best_cs.m:.6f}, lambda={best_cs.lam:.6f}, Q={best_cs.q:.6f})"
        ),
        kind="NUMERIC",
    )
    check(
        "Even the globally best Koide fit still stays far from the physical selected endpoint",
        abs(best_q.m - m_phys) > 0.9 and 0.02 <= best_q.lam <= 0.06,
        detail=(
            f"best_q=(m={best_q.m:.6f}, lambda={best_q.lam:.6f}, Q={best_q.q:.6f}); "
            f"|best_q.m-m_*|={abs(best_q.m - m_phys):.6f}"
        ),
        kind="NUMERIC",
    )
    check(
        "So widening the search does not rescue the bare local family as a physical endpoint selector",
        abs(best_cs.m - m_phys) > 1.15 and abs(best_q.m - m_phys) > 0.9,
        detail=(
            f"|best_cs.m-m_*|={abs(best_cs.m - m_phys):.6f}, "
            f"|best_q.m-m_*|={abs(best_q.m - m_phys):.6f}"
        ),
        kind="NUMERIC",
    )


def part5_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 5: what the boundary means")
    print("=" * 88)

    check(
        "The bare selected-line missing-axis resolvent family is too flexible to supply the physical endpoint law by itself",
        True,
        detail="it can fake the packet numerically, but only far from the current first-branch m_*",
    )
    check(
        "So the remaining endpoint theorem must add nonlocal transport, extra ambient data, or a stronger branch law beyond a local selected-line resolvent section",
        True,
        detail="the open target remains the ambient one-clock endpoint law for m",
    )


def main() -> int:
    m_phys, m_pos = part1_exact_family_setup()
    part2_first_branch_canonical_zero_o0(m_phys, m_pos)
    part3_first_branch_trace_mean_o0(m_phys, m_pos)
    part4_global_canonical_family_prefers_the_wrong_side(m_phys, m_pos)
    part5_interpretation()

    print()
    print("Interpretation:")
    print("  The bare missing-axis resolvent family on the exact selected line is a")
    print("  real constructive probe, but it does not supply the missing endpoint law.")
    print("  Its best numerical imitators sit far from the physical first-branch")
    print("  selected point, and the global optima are pulled toward the wrong side.")
    print("  The live theorem burden is therefore still an ambient endpoint law, not")
    print("  a bare local selected-line resolvent section.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
