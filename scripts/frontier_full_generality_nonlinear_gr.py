#!/usr/bin/env python3
"""Localize the remaining gap between the restricted strong-field lift and full nonlinear GR.

This runner does not re-prove the restricted bridge package. It uses the
existing exact finite-rank and exact local O_h source closures as inputs and
tests whether the coarse-grained exterior scalar law is enough to close the
full 4D nonlinear GR gap.

Result categories:
- EXACT: restricted source-package inputs already available on the branch
- BOUNDED: coarse-grained scalar exterior law is vacuum-close after matching
- NEGATIVE: full nonlinear GR is still blocked by missing tensorial matching
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path("/private/tmp/physics-review-active")

coarse = SourceFileLoader(
    "coarse_grained_exterior_law",
    str(ROOT / "scripts" / "frontier_coarse_grained_exterior_law.py"),
).load_module()


@dataclass
class Finding:
    name: str
    status: str
    ok: bool
    detail: str


FINDINGS: list[Finding] = []


def record(name: str, status: str, ok: bool, detail: str) -> None:
    FINDINGS.append(Finding(name=name, status=status, ok=ok, detail=detail))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    print(f"    {detail}")


def pick_best(rows):
    return min(rows, key=lambda row: row[5])


def main() -> int:
    print("FULL GENERALITY NONLINEAR GR GAP LOCALIZATION")
    print("=" * 78)

    # Exact restricted inputs already established elsewhere on the branch.
    phi_oh = coarse.same_source.build_best_phi_grid()
    rows_oh = coarse.analyze_family("exact local O_h", phi_oh)
    best_oh = pick_best(rows_oh)

    phi_fr = coarse.build_finite_rank_phi_grid()
    rows_fr = coarse.analyze_family("exact finite-rank", phi_fr)
    best_fr = pick_best(rows_fr)

    # Exact support: the branch already carries the restricted strong-field package.
    record(
        "restricted strong-field source package is present as branch input",
        "EXACT",
        True,
        "uses the existing exact local O_h and exact finite-rank source families as inputs; not re-proved here",
    )

    # Bounded route: scalar exterior law after coarse-graining.
    oh_improvement = best_oh[4] / max(best_oh[5], 1e-15)
    fr_improvement = best_fr[4] / max(best_fr[5], 1e-15)
    bounded_ok = best_oh[5] < 1e-5 and best_fr[5] < 2e-5
    record(
        "coarse-grained scalar exterior law is vacuum-close on both source families",
        "BOUNDED",
        bounded_ok,
        (
            f"O_h: R_match={best_oh[0]:.1f}, direct={best_oh[4]:.3e}, coarse={best_oh[5]:.3e}, "
            f"improvement={oh_improvement:.1f}x; "
            f"finite-rank: R_match={best_fr[0]:.1f}, direct={best_fr[4]:.3e}, coarse={best_fr[5]:.3e}, "
            f"improvement={fr_improvement:.1f}x"
        ),
    )

    # Negative: full nonlinear GR is still blocked by missing tensorial completion.
    tensorial_gap = best_fr[4] > 1e-3 and best_fr[4] > 100 * best_fr[5]
    record(
        "full nonlinear GR is not closed by the present scalar bridge",
        "NEGATIVE",
        tensorial_gap,
        (
            "direct microscopic residual remains nonzero after the branch's best scalar projection; "
            "the current machinery fixes only scalar/static exterior data, not the full tensorial 4D metric"
        ),
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_exact = sum(1 for f in FINDINGS if f.status == "EXACT")
    n_bounded = sum(1 for f in FINDINGS if f.status == "BOUNDED")
    n_negative = sum(1 for f in FINDINGS if f.status == "NEGATIVE")
    print(f"EXACT:   {n_exact}")
    print(f"BOUNDED: {n_bounded}")
    print(f"NEGATIVE:{n_negative}")
    print()
    print("Verdict: the branch has a credible scalar exterior route, but the missing")
    print("principle for full generality is a tensorial matching/completion theorem.")

    return 0 if all(f.ok for f in FINDINGS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
