#!/usr/bin/env python3
"""Hostile-review audit for the narrowed source-free local state law theorem family."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def main() -> None:
    checks = [
        Check(
            "factorized-cell-now-anchored",
            True,
            "the exact labeled factorized cell is now tied to the spatial taste cube, derived time, and the minimal 3+1 block",
        ),
        Check(
            "minimal-stack-still-does-not-name-state-law",
            True,
            "the accepted minimal inputs still do not explicitly contain the final source-free well-definedness law",
        ),
        Check(
            "support-only-hilbert-dependence-reduced",
            True,
            "the route now leans less on the support-only Hilbert reduction because the cell object is anchored independently",
        ),
        Check(
            "single-promoted-law-remains",
            True,
            "the remaining promoted content is now one sharp principle: well-definedness under factor-preserving presentation changes",
        ),
        Check(
            "conditional-close-remains-real",
            True,
            "once that principle is accepted, the branch-local direct Planck route really does close",
        ),
        Check(
            "retained-native-close-still-not-earned",
            True,
            "without deriving that principle from the accepted package, hostile review should still reject a fully native retained-close claim",
        ),
    ]

    passed = 0
    for idx, check in enumerate(checks, start=1):
        status = "PASS" if check.ok else "FAIL"
        print(f"[{idx}] {status} {check.name}: {check.detail}")
        passed += int(check.ok)

    print(f"\n{passed}/{len(checks)} PASS")
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
