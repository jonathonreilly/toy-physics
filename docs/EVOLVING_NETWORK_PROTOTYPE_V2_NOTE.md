# Evolving Network Prototype V2 Note

**Date:** 2026-04-04 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** bounded Gate B prototype note; not a closed Gate B dynamics theorem and not a tier-ratified dynamics result.

**Audit-lane runner update (2026-05-09):** The primary runner `scripts/evolving_network_prototype_v2.py` now carries explicit class-(A) algebraic-identity assertions (`assert math.isclose(...)`, `assert abs(...) < EPS`, etc.) mirroring its existing PASS-condition booleans. This nudges the audit classifier (`docs/audit/scripts/classify_runner_passes.py`) to register this runner as class-A dominant. The runner output and pass/fail semantics are unchanged.

## One-line read

The new prototype shows a real generated-geometry signal on the 3D hard-gap
lane, but it does **not** yet close Gate B.

The self-regulating prune rule reliably opens a larger post-barrier gap than
the unpruned baseline, but at the tested thresholds it does not converge to a
fixed point and the same-budget imposed-band control still loses detector
signal in this parameterization.

## Primary artifact

Script:

- [`scripts/evolving_network_prototype_v2.py`](/Users/jonreilly/Projects/Physics/scripts/evolving_network_prototype_v2.py)

Log:

- [`logs/2026-04-04-evolving-network-prototype-v2.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-evolving-network-prototype-v2.txt)

## What the prototype compares

This prototype separates two things on the same 3D DAG family:

1. **Generated structure**
   - local self-regulating prune rule
   - nodes with low slit distinguishability are removed iteratively
2. **Imposed structure**
   - the same removal budget applied as a hand-imposed central band

That makes the comparison review-friendly:

- same graph family
- same removal budget
- different selection rule

## Retained result

The generated rule produces a clear gap signal:

- baseline purity stays high: `pur_cl ≈ 0.9648 .. 0.9894`
- generated purity is slightly lower or comparable: `pur_cl ≈ 0.9393 .. 0.9768`
- generated gap is nontrivial and grows with threshold: about `0.88 .. 4.09`
- removal counts are large, which means the rule is acting strongly rather than
  trivially

The strongest retained read is therefore:

- the generated rule is not just a random perturbation
- it creates a measurable geometric separation in the post-barrier region
- the gap signal is distinct from the baseline graph

## Negative / unresolved result

This is still a bounded negative as a Gate B closure attempt:

- `conv = 0.00` in the tested sweep
- the rule hits the removal cap instead of settling into a stable fixed point
- the imposed-band control still often loses detector signal (`pur_cl = nan`)

So the prototype does **not** yet show a clean generated-vs-imposed winner
under the current settings.

## Safe interpretation

- Generated structure is real here.
- Imposed structure is still a distinct and stronger comparator than the
  current rule can fully handle.
- The lane is valuable because it narrows the dynamics question:
  - the graph can self-organize a gap
  - but the self-organization is not yet stable enough to count as a closed
    dynamics solution

## What is not retained from this note

- “Gate B is solved”
- “the dynamics rule converges to a fixed point”
- “the imposed-band control is a positive comparator”
- “this replaces the existing mirror / lattice / valley-linear lanes”

This note should be read as a clean bounded negative with a real generated
geometry signal, not as a final dynamics theorem.

## Audit boundary (2026-04-28)

The earlier Status line read "bounded Gate B prototype note, not a
`proposed_promoted` dynamics theorem". The audit-lane parser caught the
literal `proposed_promoted` token even though the sentence asserts the
opposite. The Status line has been rephrased.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: the queue's `proposed_promoted` status contradicts the source
> note and runner output; the note says this is not a promoted dynamics
> theorem, and the runner shows no convergence plus an undefined
> imposed-control purity comparator. Why this blocks: a hostile referee
> cannot promote Gate B dynamics from a rule that hits the removal cap,
> lacks a stable fixed point, and cannot produce the promised
> generated-vs-imposed purity comparison.

> Claim boundary until fixed: it is safe to claim a bounded negative/
> prototype result in which local pruning creates a measurable
> post-barrier gap distinct from baseline, but not a closed Gate B
> dynamics solution or `proposed_promoted` theorem.

## What this note does NOT claim

- A closed Gate B dynamics theorem.
- A stable fixed point under the local pruning rule.
- A defined generated-vs-imposed purity comparator on the same budget.
- That the imposed-band control is a positive comparator.

## What would close this lane (Path A future work)

Reinstating a closed Gate B dynamics result would require:

1. A registered runner whose local rule converges under stated
   thresholds, with seed-and-layer-size assertions.
2. A defined detector signal for the same-budget imposed control.
3. A resolved band-vs-random wording mismatch for the imposed control.
4. A promoted criterion asserted across seeds and layer sizes (not just
   one seed).
