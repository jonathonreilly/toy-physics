# Poisson Self-Gravity Mechanism Note

**Date:** 2026-04-05 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** bounded control-only family; the exact-lattice Poisson self-gravity mechanism does not close on the four hard-bar criteria and is not a tier-ratified self-gravity mechanism.

## Purpose

This note is the exact-lattice self-gravity mechanism checkpoint.

The hard bar was:

1. exact identity reduction at `epsilon = 0`
2. matched-null control if the update machinery could induce attenuation
3. per-step and end-to-end Born checks made explicit
4. one observable stronger than raw escape that does not just collapse the
   weak-field law

The retained result does not beat that bar.

## Retained Evidence

The relevant retained notes are:

- [POISSON_SELF_GRAVITY_LOOP_NOTE.md](/Users/jonreilly/Projects/Physics/docs/POISSON_SELF_GRAVITY_LOOP_NOTE.md)
- [POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md](/Users/jonreilly/Projects/Physics/docs/POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md)
- [POISSON_SELF_GRAVITY_LOOP_V3_NOTE.md](/Users/jonreilly/Projects/Physics/docs/POISSON_SELF_GRAVITY_LOOP_V3_NOTE.md)

Those retained controls say:

- `epsilon = 0` is an exact identity loop
- the frozen field snapshot is Born-clean
- the terminal loop effect is tiny
- the weak-field sign stays TOWARD in the control regime
- but the end-to-end loop does not stay machine-clean once the backreaction
  is turned on

## Why This Does Not Beat The Bar

The key limitation is that the outer loop is still too weak and too fragile.

The best retained summary is:

- exact zero-coupling reduction survives
- per-step Born survives
- end-to-end Born does not remain machine-clean
- the nonzero-coupling effect stays tiny
- no stable self-gravity regime emerges on the tested exact-lattice family

That means the family is useful, but only as a control family.

## What Would Be Needed To Reopen It

Reopen only if a future version can show all of:

1. exact identity at zero coupling
2. matched-null stability under the same update machinery
3. per-step and end-to-end Born that both remain clean enough to defend
4. a promoted observable stronger than raw escape that stays nontrivial
5. a stable converged loop with a real effect size, not a tiny control

Until then, this is not a retained self-gravity mechanism.

## Final Verdict

**control-only family**

The exact-lattice Poisson-like backreaction loop is a useful sanity check and
an honest audit target, but it does not yet beat the bounded-control status.
*** Add File: /Users/jonreilly/Projects/Physics/scripts/poisson_self_gravity_mechanism.py
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

## Audit boundary (2026-04-28)

The earlier Status line read "frozen as a control-only family, not a
`proposed_retained` self-gravity mechanism". The audit-lane parser
caught the literal token even though the sentence asserts the opposite.
The Status line has been rephrased.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: The queued proposed-retained row is not a retained mechanism
> claim on its own terms: the source status says control-only and not
> a `proposed_retained` self-gravity mechanism, the evidence notes it
> cites are unaudited or unknown, and the companion script only prints
> a hard-coded verdict.

The companion script's `MechanismVerdict` dataclass embeds the verdict
"control-only family" as a hard-coded constant; it does not run a
mechanism check, only prints what was decided when the dataclass was
written. That keeps the note legible as a frozen control verdict but
does not function as a runner that re-derives the verdict.

## What this note does NOT claim

- A retained self-gravity mechanism on the exact-lattice family.
- Closure on any of the four hard-bar criteria (exact-zero identity,
  matched-null stability, end-to-end Born, stronger-than-escape
  observable).
- That the printed verdict is the result of a runner check; it is a
  hard-coded conclusion.

## What would close this lane (Path A future work)

Reinstating a self-gravity mechanism claim would require:

1. A registered runner that re-derives each of the four hard-bar
   criteria (exact identity at `epsilon = 0`, matched-null stability,
   step-local AND end-to-end Born, stronger-than-escape observable)
   rather than printing a hard-coded `MechanismVerdict`.
2. Audit-clean upstream evidence notes (currently unaudited / unknown).
3. A stable converged loop with a non-tiny effect.
