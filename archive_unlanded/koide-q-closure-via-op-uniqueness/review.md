# Review: koide-q-closure-via-op-uniqueness

**Date:** 2026-04-25
**Reviewed branch:** `origin/koide-q-closure-via-op-uniqueness`
**Reviewed commit:** `9df758bc0b0e93d6447704aad9b7a571d5f22cc1`
**Reviewer worktree:** `/private/tmp/koide-q-op-review.6V5NIR`

## Verdict

Not ready to land on `main` as a retained closure.

The branch is scientifically useful as a support-route attempt, but its retained-status claim is stronger than the certified evidence. The load-bearing bridge from OP unique scalar generator to exclusive scalar source domain is still interpretive, and the runner assumes that bridge rather than verifying it.

## What I Reviewed

- `docs/KOIDE_Q_CLOSURE_VIA_OP_UNIQUE_GENERATOR_DOMAIN_THEOREM_NOTE_2026-04-25.md`
- `scripts/frontier_koide_q_closure_via_op_unique_generator_domain.py`
- Branch diff against current `origin/main`
- Runner execution:

```bash
python3 scripts/frontier_koide_q_closure_via_op_unique_generator_domain.py
```

The runner reports `PASSED: 13/13`, but that pass is not sufficient for retained closure because the decisive source-domain exclusion is asserted inside the runner.

## Findings

### [P1] Retained Q closure rests on an admitted interpretive bridge

File: `docs/KOIDE_Q_CLOSURE_VIA_OP_UNIQUE_GENERATOR_DOMAIN_THEOREM_NOTE_2026-04-25.md`
Lines: 53-107, with the caveat at 142-179 and 211-230.

The note promotes `Q_l = 2/3` to retained closure, but the decisive step is the inferred reading that OP Theorem 1 uniqueness of the scalar generator also proves uniqueness of the scalar source domain. The note later explicitly says this is not stated verbatim in OP and may be flagged by strict review. That leaves this as a defended support-route interpretation, not a theorem-grade retained closure for `main`.

### [P1] Runner asserts source-domain exclusion instead of certifying it

File: `scripts/frontier_koide_q_closure_via_op_unique_generator_domain.py`
Lines: 140-175, with downstream promotion at 196-207 and 233-241.

The runner's load-bearing step is not computed or extracted from retained authorities. It assigns the framework scalar source domain to `span{P_x}`, sets `z_in_framework_source_domain = False`, then hard-codes `z_physical = 0` and derives `Q_l = 2/3`. That verifies the downstream algebra only after assuming the exact disputed OP uniqueness to source-domain uniqueness bridge.

### [P2] Direct branch merge would delete current main packages

The source branch is stale relative to current `origin/main`. A direct branch merge would delete live main packages, including the Napoleon closed-form package and the cosmology single-ratio inverse reconstruction package. Even if the Koide science were ready, the branch should be rebased or salvaged as a narrow patch before landing.

## Path To Closure

To make this branch landable as retained closure, one of these has to happen:

1. Add a theorem-grade retained authority proving that OP uniqueness entails exact scalar source-domain exclusivity for all scalar-observable backgrounds, including exclusion of commutant `Z`.
2. Update the runner so it audits that authority from disk/object-level checks instead of setting `z_in_framework_source_domain = False`.
3. Rebase or rebuild the branch on current `origin/main` so landing does not delete unrelated packages.

If that theorem-grade source-domain exclusivity is not added, the branch should be reframed as a support criterion rather than a retained closure.
