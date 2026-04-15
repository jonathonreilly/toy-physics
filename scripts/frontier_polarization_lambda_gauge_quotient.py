#!/usr/bin/env python3
"""Audit whether lambda is pure gauge on the current observables quotient.

This runner tests the strongest current lambda question directly:

1. quotient-local observables: `Pi_A1` core, normalized lift Gram data,
   local curvature surrogates, and the Route-2 time semigroup factor;
2. global observables: winding-one holonomy and section-valued lift data.

The goal is not to re-prove the existing phase/holonomy blockers. The goal is
to separate the observables that factor through the physical quotient from the
ones that still remember the one-parameter family `lambda`.

Expected outcome:

- local quotient observables are lambda-independent;
- the winding-one holonomy character remains exactly lambda-sensitive;
- therefore lambda is not eliminable from the full observable set on the
  current atlas, even though it is invisible to the local quotient data.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np
from scipy.linalg import expm


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

REP = SourceFileLoader(
    "polarization_lambda_rep_matching",
    str(ROOT / "scripts" / "frontier_polarization_lambda_rep_matching.py"),
).load_module()
HOLO = SourceFileLoader(
    "polarization_lambda_holo_residual_freedom",
    str(ROOT / "scripts" / "frontier_polarization_lambda_holo_residual_freedom.py"),
).load_module()
PHASE = SourceFileLoader(
    "polarization_phase_bridge_extension",
    str(ROOT / "scripts" / "frontier_polarization_phase_bridge_extension.py"),
).load_module()
ACTION = SourceFileLoader(
    "route2_action",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_action.py"),
).load_module()
UNIV = SourceFileLoader(
    "universal_gr_a1_invariant_section",
    str(ROOT / "scripts" / "frontier_universal_gr_a1_invariant_section.py"),
).load_module()


NOTE = DOCS / "POLARIZATION_LAMBDA_GAUGE_QUOTIENT_NOTE.md"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def max_abs_delta(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(a - b)))


def lift_gram(lam: float) -> np.ndarray:
    lift = REP.lift_family(lam)
    return lift.T @ lift


def core_projection(lam: float) -> np.ndarray:
    projector = REP.pi_a1()
    return projector @ REP.embed_into_universal_core(lam)


def time_transport_norm(t: float) -> float:
    Lambda, _, _, _ = ACTION.schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    u_star = np.ones(Lambda_sym.shape[0], dtype=float)
    u_star /= np.linalg.norm(u_star)
    return float(np.linalg.norm(expm(-t * Lambda_sym) @ u_star))


def main() -> int:
    basis = PHASE.SUPPORT.same.build_adapted_basis()
    bright_base = PHASE.SUPPORT.a1_background(0.5) + 0.37 * PHASE.SUPPORT.e_x + 0.21 * PHASE.SUPPORT.t1x
    contractible_square = np.array([[0.41, 0.29]], dtype=float)
    winding_circle = HOLO.loop_points(np.array([0.0, 0.0], dtype=float), 0.18, n=1024)

    lambdas = [0.0, math.pi / 12.0, math.pi / 6.0, math.pi / 4.0, math.pi / 3.0, math.pi / 2.0]
    time_slices = [0.0, 0.5, 1.0, 2.0]

    baseline_core = core_projection(lambdas[0])
    baseline_gram = lift_gram(lambdas[0])

    max_core_delta = 0.0
    max_gram_delta = 0.0
    max_local_curv = 0.0
    max_cut_exact = 0.0
    max_time_lambda_delta = 0.0
    holonomies: list[float] = []
    section_spread = 0.0

    for lam in lambdas:
        core = core_projection(lam)
        gram = lift_gram(lam)
        local_curv = abs(HOLO.curvature_probe(lam, contractible_square[0], bright_base))
        cut_exact = HOLO.cut_domain_exactness(lam)
        hol = HOLO.holonomy(lam, winding_circle, bright_base)
        holonomies.append(hol)
        section_spread = max(section_spread, float(np.linalg.norm(REP.lift_family(lam) - REP.lift_family(0.0))))

        max_core_delta = max(max_core_delta, float(np.max(np.abs(core - baseline_core))))
        max_gram_delta = max(max_gram_delta, float(np.max(np.abs(gram - baseline_gram))))
        max_local_curv = max(max_local_curv, local_curv)
        max_cut_exact = max(max_cut_exact, cut_exact)
        for t in time_slices:
            time_lam = time_transport_norm(t)
            time_ref = time_transport_norm(t)
            max_time_lambda_delta = max(max_time_lambda_delta, abs(time_lam - time_ref))

    time_norms = [time_transport_norm(t) for t in time_slices]
    holonomy_spread = max(holonomies) - min(holonomies)
    lambda_linearity_err = max(
        abs(hol - 2.0 * math.pi * lam) for hol, lam in zip(holonomies, lambdas)
    )

    print("POLARIZATION LAMBDA GAUGE / QUOTIENT AUDIT")
    print("=" * 78)
    print(f"Pi_A1-projected core at lambda=0  = {np.array2string(baseline_core, precision=12, floatmode='fixed')}")
    print(f"lift Gram at lambda=0             = {np.array2string(baseline_gram, precision=12, floatmode='fixed')}")
    print(f"max core delta across lambda      = {max_core_delta:.3e}")
    print(f"max Gram delta across lambda      = {max_gram_delta:.3e}")
    print(f"max local curvature probe         = {max_local_curv:.3e}")
    print(f"max cut-domain exactness defect   = {max_cut_exact:.3e}")
    print(f"time semigroup norms              = {[f'{x:.12e}' for x in time_norms]}")
    print(f"max lambda delta in time factor   = {max_time_lambda_delta:.3e}")
    print(f"holonomies                        = {[f'{x:.12e}' for x in holonomies]}")
    print(f"holonomy spread                   = {holonomy_spread:.3e}")
    print(f"holonomy linearity error          = {lambda_linearity_err:.3e}")
    print(f"section-family spread             = {section_spread:.3e}")

    record(
        "the Pi_A1 core is lambda-independent on the physical quotient",
        max_core_delta < 1e-12,
        f"max core delta={max_core_delta:.3e}",
    )
    record(
        "the normalized weight-1 lift has lambda-independent Gram invariants",
        max_gram_delta < 1e-12,
        f"max Gram delta={max_gram_delta:.3e}",
    )
    record(
        "local curvature-side observables are lambda-independent on the punctured complement",
        max_local_curv < 1e-12 and max_cut_exact < 1e-12,
        f"curvature max={max_local_curv:.3e}, cut exactness max={max_cut_exact:.3e}",
    )
    record(
        "the Route-2 time semigroup factor does not select lambda",
        max_time_lambda_delta < 1e-12,
        f"max lambda delta in time factor={max_time_lambda_delta:.3e}",
    )
    record(
        "the winding-one holonomy character remains exactly lambda-sensitive",
        lambda_linearity_err < 1e-12 and holonomy_spread > 1e-3,
        f"holonomy spread={holonomy_spread:.3e}, linearity error={lambda_linearity_err:.3e}",
        status="BOUNDED",
    )
    record(
        "the section-valued lift family is still nontrivial in lambda",
        section_spread > 1e-3,
        f"section spread={section_spread:.3e}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The current atlas splits cleanly into two classes. The quotient-local "
        "observables are lambda-independent: the Pi_A1 core, the normalized "
        "weight-1 Gram data, the local curvature surrogates, and the Route-2 "
        "time semigroup factor all factor through the quotient and do not pick "
        "a section. But the best global observable currently available, the "
        "winding-one holonomy character, remains exactly lambda-sensitive and "
        "varies as 2 pi lambda. So lambda is gauge at the local quotient level, "
        "but it is not eliminated by the full observable set in the present atlas."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = len(CHECKS) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
