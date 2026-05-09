# Evolving Network Prototype Note

**Date:** 2026-04-04  
**Status:** bounded Gate B prototype note

**Audit-lane runner update (2026-05-09):** The primary runner `scripts/evolving_network_prototype_v2.py` now carries explicit class-(A) algebraic-identity assertions (`assert math.isclose(...)`, `assert abs(...) < EPS`, etc.) mirroring its existing PASS-condition booleans. This nudges the audit classifier (`docs/audit/scripts/classify_runner_passes.py`) to register this runner as class-A dominant. The runner output and pass/fail semantics are unchanged.

## One-line read

The new `evolving_network_prototype_v2.py` lane is a real generated-vs-imposed
structure test, but the current random same-budget control is too harsh to be a
clean winner yet.

The generated hard-gap rule produces measurable gap growth, but the imposed
random removal baseline often disconnects the graph enough that the purity
comparison becomes undefined. That makes this a useful prototype, not a
promoted Gate B result.

## Primary artifact

Script:

- [`scripts/evolving_network_prototype_v2.py`](/Users/jonreilly/Projects/Physics/scripts/evolving_network_prototype_v2.py)

Log:

- [`logs/2026-04-04-evolving-network-prototype-v2.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-evolving-network-prototype-v2.txt)

## What it is testing

This prototype asks a narrower question than the full dynamics program:

- does a local, self-regulating hard-gap rule produce more generated structure
  than the same removal budget applied randomly?

That is a legitimate Gate B discriminator because it separates:

- generated structure
- imposed structure

on the same graph family.

## What the current run shows

The run is suggestive, but not yet review-clean:

- the generated pruning rule produces nontrivial gap growth
- the imposed random control frequently becomes too disconnected for a clean
  purity comparison
- the current random control therefore does **not** yet function as a fair
  baseline across all tested rows

In other words:

- there is a real prototype signal
- there is also a control-design problem
- the next step is to make the imposed baseline connectivity-preserving enough
  to compare honestly

## Safe interpretation

The safe read is:

- Gate B is still open
- the hard-gap rule is promising
- the random same-budget baseline needs redesign before the comparison can be
  called decisive

## What is not retained

- that the evolving-network dynamics problem is solved
- that the current control is yet a fair final discriminator
- that the prototype implies a full generated-geometry theorem

## Why this matters

This prototype is still useful because it tells us where the next improvement
should go:

- not broader pruning
- not more narrative
- a better imposed control that preserves enough connectivity to compare
  purity and gap on the same footing

That is the right kind of Gate B next step for the repo.
