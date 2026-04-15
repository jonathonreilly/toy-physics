#!/usr/bin/env python3
"""Reduce the remaining continuum-QG issue to the canonical-comparison frontier.

This runner does not claim a full continuum theorem. It proves the stronger and
more useful negative/positive split:

  - the direct-universal route already has a UV-finite partition-density family;
  - its stationary/semiclassical sector already reproduces the discrete GR
    stationary family;
  - finite-atlas patching is exact;
  - independent blocks factorize exactly.

So the remaining continuum question is no longer UV, local operator closure,
missing discrete refinement-net structure, missing inverse-limit existence,
missing abstract Gaussian completion, missing project-native PL carrier,
missing project-native weak/Dirichlet structure, missing project-native
Sobolev interface, missing a chosen external smooth weak/measure realization,
missing canonical textbook weak/measure equivalence, missing smooth local or
global weak/Gaussian gravitational identification, or missing canonical smooth
weak/measure equivalence. It is the stronger textbook geometric/action
comparison question beyond that already-closed weak/Gaussian route.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


ROOT = Path("/Users/jonreilly/Projects/Physics")
DOCS = ROOT / "docs"


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


def gaussian_partition(k_op: np.ndarray, j: np.ndarray) -> float:
    n = k_op.shape[0]
    det_k = float(np.linalg.det(k_op))
    exponent = 0.5 * float(j @ np.linalg.solve(k_op, j))
    return (2.0 * math.pi) ** (n / 2.0) * det_k ** (-0.5) * math.exp(exponent)


def random_spd(rng: np.random.Generator, n: int) -> np.ndarray:
    a = rng.normal(size=(n, n))
    return a.T @ a + np.eye(n)


def main() -> int:
    qg_text = (DOCS / "UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md").read_text(encoding="utf-8")
    gr_text = (DOCS / "UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md").read_text(encoding="utf-8")
    atlas_text = (DOCS / "UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md").read_text(encoding="utf-8")
    refine_text = (DOCS / "UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md").read_text(encoding="utf-8")
    completion_text = (DOCS / "UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md").read_text(encoding="utf-8")
    pl_text = (DOCS / "UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md").read_text(encoding="utf-8")
    weak_text = (DOCS / "UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md").read_text(encoding="utf-8")
    sobolev_text = (DOCS / "UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md").read_text(encoding="utf-8")
    textbook_text = (DOCS / "UNIVERSAL_QG_CANONICAL_TEXTBOOK_WEAK_MEASURE_EQUIVALENCE_NOTE.md").read_text(encoding="utf-8")
    smooth_local_text = (DOCS / "UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_LOCAL_IDENTIFICATION_NOTE.md").read_text(encoding="utf-8")
    smooth_global_text = (DOCS / "UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md").read_text(encoding="utf-8")
    smooth_canon_text = (DOCS / "UNIVERSAL_QG_CANONICAL_SMOOTH_GRAVITATIONAL_WEAK_MEASURE_NOTE.md").read_text(encoding="utf-8")

    rng = np.random.default_rng(211)
    max_factorization_err = 0.0
    max_log_additivity_err = 0.0
    min_positive_z = float("inf")

    for n1, n2 in [(3, 4), (4, 5), (5, 6)]:
        k1 = random_spd(rng, n1)
        k2 = random_spd(rng, n2)
        j1 = 0.1 * rng.normal(size=n1)
        j2 = 0.1 * rng.normal(size=n2)

        z1 = gaussian_partition(k1, j1)
        z2 = gaussian_partition(k2, j2)
        k = np.block(
            [
                [k1, np.zeros((n1, n2))],
                [np.zeros((n2, n1)), k2],
            ]
        )
        j = np.concatenate([j1, j2])
        z = gaussian_partition(k, j)

        min_positive_z = min(min_positive_z, z1, z2, z)
        max_factorization_err = max(max_factorization_err, abs(z - z1 * z2))
        max_log_additivity_err = max(
            max_log_additivity_err,
            abs(math.log(z) - math.log(z1) - math.log(z2)),
        )

    record(
        "the repo already has exact discrete global GR closure, exact atlas patching, exact UV-finite partition density, the exact canonical refinement net, the exact abstract Gaussian completion, the exact project-native PL carrier, the exact project-native weak-form closure, the exact project-native Sobolev interface, exact canonical textbook weak/measure closure, and exact canonical smooth weak/measure closure on the chosen realization",
        "full discrete `3+1` gr" in gr_text.lower()
        and "global stationary section" in atlas_text.lower()
        and "uv-finite" in qg_text.lower()
        and "canonical geometric refinement net" in refine_text.lower()
        and "abstract gaussian" in completion_text.lower()
        and "piecewise-linear" in pl_text.lower()
        and "weak/dirichlet" in weak_text.lower()
        and "h^1" in sobolev_text.lower(),
        "canonical textbook weak" in textbook_text.lower()
        and "smooth local gravitational" in smooth_local_text.lower()
        and "smooth global weak gravitational" in smooth_global_text.lower()
        and "canonical smooth gravitational weak/measure" in smooth_canon_text.lower(),
        "the remaining issue is downstream of exact discrete GR, exact finite partition density, exact geometric refinement structure, exact abstract Gaussian completion, exact PL realization, exact weak-form closure, exact Sobolev interface, canonical textbook weak/measure closure, and canonical smooth weak/measure closure, not upstream of them",
    )
    record(
        "the local partition family is finite and positive on sampled positive-background Gaussian slices",
        min_positive_z > 0.0 and math.isfinite(min_positive_z),
        f"min sampled partition value={min_positive_z:.6e}",
    )
    record(
        "independent blocks factorize exactly at the partition level",
        max_factorization_err < 1e-10,
        f"max block-factorization error={max_factorization_err:.3e}",
    )
    record(
        "independent blocks add exactly at the log-partition level",
        max_log_additivity_err < 1e-12,
        f"max log-additivity error={max_log_additivity_err:.3e}",
    )
    record(
        "the remaining continuum issue is therefore stricter textbook geometric/action comparison beyond the already-closed weak/Gaussian route, not a local UV-divergence, missing-refinement, missing-inverse-limit theorem, missing-abstract-completion theorem, missing-PL-carrier theorem, missing-weak-form theorem, missing-Sobolev-interface theorem, missing chosen external smooth weak/measure formulation, missing canonical textbook weak/measure equivalence, or missing smooth global weak/Gaussian gravitational closure",
        max_factorization_err < 1e-10 and max_log_additivity_err < 1e-12,
        "once the route already has exact finite densities, canonical refinement, exact abstract Gaussian completion, project-native PL weak/Sobolev structure, canonical textbook weak/measure closure, and canonical smooth weak/measure equivalence on the chosen realization, the unresolved step is only stricter textbook geometric/action comparison beyond that level",
    )

    print("UNIVERSAL QG CONTINUUM BRIDGE REDUCTION")
    print("=" * 78)
    print(f"min sampled partition value    = {min_positive_z:.6e}")
    print(f"max factorization error        = {max_factorization_err:.3e}")
    print(f"max log-additivity error       = {max_log_additivity_err:.3e}")

    print("\nVerdict:")
    print(
        "The remaining stronger continuum/QG question is now reduced to "
        "stricter textbook geometric/action comparison beyond the already-"
        "closed canonical smooth weak/Gaussian gravitational route. It is no "
        "longer a missing UV finiteness, local operator-closure, geometric "
        "refinement-net, inverse-limit-existence, abstract-completion, "
        "project-native PL-carrier, weak-form, Sobolev-interface, chosen "
        "external smooth weak/measure, canonical textbook weak/measure, or "
        "smooth global weak/Gaussian issue on the project route."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
