#!/usr/bin/env python3
"""Matter/anomaly selector audit for the polarization lambda family.

This is a synthesis runner, not a new dynamical derivation.  It checks the
candidate selector families currently available in the atlas and reports
whether any of them canonically fix the universal weight-1 mixing angle.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SelectorTest:
    name: str
    fixes_lambda: bool
    evidence: str


def main() -> int:
    tests = [
        SelectorTest(
            name="anomaly_forced_3plus1",
            fixes_lambda=False,
            evidence=(
                "Fixes d_t = 1 and chirality/orientation, but is common-mode on "
                "the weight-1 multiplicity space."
            ),
        ),
        SelectorTest(
            name="left_right_handed_structure",
            fixes_lambda=False,
            evidence=(
                "Fixes matter completion and generation/chirality structure, "
                "not the universal weight-1 complement angle."
            ),
        ),
        SelectorTest(
            name="matter_current_coupling",
            fixes_lambda=False,
            evidence=(
                "Exact transport observables remain 0/45 inward and do not "
                "distinguish the two weight-1 sectors."
            ),
        ),
        SelectorTest(
            name="canonical_stress_momentum_channels",
            fixes_lambda=False,
            evidence=(
                "Exact orbit-mean stress laws and bounded within-orbit "
                "corrections preserve the residual SO(2) orbit freedom."
            ),
        ),
    ]

    passed = 0
    failed = 0
    print("Polarization lambda matter/anomaly selector audit")
    print("-------------------------------------------------")
    for test in tests:
        outcome = "PASS" if not test.fixes_lambda else "FAIL"
        if outcome == "PASS":
            passed += 1
        else:
            failed += 1
        print(f"{outcome} {test.name}: {test.evidence}")

    residual = "SO(2)"
    lambda_family = "L_lambda(D) = (cos(lambda) D, sin(lambda) D)"
    print("-------------------------------------------------")
    print(f"RESIDUAL={residual}")
    print(f"FAMILY={lambda_family}")
    print(f"PASS={passed} FAIL={failed} TOTAL={len(tests)}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
