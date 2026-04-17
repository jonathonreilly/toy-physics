#!/usr/bin/env python3
"""Mechanism summary for the exact-lattice Poisson-like self-gravity lane.

This is a lightweight report script, not a new numerical harness.
It prints the strict retained verdict:

- exact zero-coupling reduction survives
- per-step Born survives on the frozen field snapshot
- end-to-end Born does not stay machine-clean
- the loop effect stays tiny
- therefore the family remains control-only
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MechanismVerdict:
    exact_zero_coupling_identity: bool
    matched_null_needed: bool
    step_local_born_clean: bool
    end_to_end_born_clean: bool
    loop_effect_size: str
    weak_field_sign: str
    verdict: str


VERDICT = MechanismVerdict(
    exact_zero_coupling_identity=True,
    matched_null_needed=True,
    step_local_born_clean=True,
    end_to_end_born_clean=False,
    loop_effect_size="tiny control effect",
    weak_field_sign="TOWARD in the control regime",
    verdict="control-only family",
)


def main() -> None:
    print("POISSON SELF-GRAVITY MECHANISM")
    print("  exact-lattice self-gravity lane")
    print("  strict retained verdict: control-only")
    print()
    print("HARD BAR CHECK")
    print(f"  exact zero-coupling identity: {VERDICT.exact_zero_coupling_identity}")
    print(f"  matched null needed:         {VERDICT.matched_null_needed}")
    print(f"  step-local Born clean:       {VERDICT.step_local_born_clean}")
    print(f"  end-to-end Born clean:       {VERDICT.end_to_end_born_clean}")
    print(f"  loop effect size:            {VERDICT.loop_effect_size}")
    print(f"  weak-field sign:             {VERDICT.weak_field_sign}")
    print()
    print("FINAL VERDICT")
    print(f"  {VERDICT.verdict}")
    print()
    print("REOPEN ONLY IF A FUTURE VERSION SHOWS:")
    print("  1. exact identity at epsilon = 0")
    print("  2. matched-null stability under the same update machinery")
    print("  3. per-step and end-to-end Born both defensible")
    print("  4. a stronger observable than raw escape")
    print("  5. a stable converged loop with a non-tiny effect")


if __name__ == "__main__":
    main()
