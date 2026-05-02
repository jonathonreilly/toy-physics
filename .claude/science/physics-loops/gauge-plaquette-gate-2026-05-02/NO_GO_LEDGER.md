# No-Go Ledger

## Routes considered and explicitly rejected

### Route R1: prove the residual environment data closes here

**Status:** rejected.

This would require deriving the explicit `rho_(p,q)(6)` coefficients of
the residual source-sector environment operator. That work is
non-trivial and tracked in
`gauge_vacuum_plaquette_residual_environment_identification_theorem_note`
and `gauge_vacuum_plaquette_spatial_environment_character_measure_theorem_note`.
Attempting this here would conflict with their separate audit lanes,
and any failed attempt would muddy the bounded scope of the
factorization theorem proper.

The bounded-theorem move precisely allows the factorization to retain
without forcing the residual environment to close.

### Route R2: convert to a no-go theorem on the local-only Perron value

**Status:** rejected.

The runner's support check
`abs(local_value - 0.5934) > 1.0e-2` shows that the local-only Perron
value (0.452) does not equal the same-surface comparator (0.5934).
A no-go theorem from this would say "the local mixed-kernel factor
alone does not reproduce P(6)". That is true but is not what the
note claims; the note already states P(6) closure as out of scope and
the local-vs-full distinction is recorded in the SUPPORT bucket.

Promoting that disagreement to a no-go theorem at this row would
misclassify the work — the row's positive content is an exact
factorization, not a negative impossibility result. The right home
for any "no constant lift" no-go is
`gauge_vacuum_plaquette_constant_lift_obstruction_note`, which is
already a `retained_no_go` separately.

### Route R3: leave as `open_gate`, narrow scope only inside the note

**Status:** rejected as insufficient.

The 2026-05-02 conservative re-audit chose `open_gate` based on the
title-as-scope reading. Leaving the audit verdict as `open_gate`
while only changing the note prose would not change
`effective_status`, so 246 transitive descendants would remain
blocked. This route does not deliver the claim-state movement the
loop requires.

### Route R4 (chosen): tighten note + cross-family bounded-theorem audit

**Status:** executed.

The chosen route is the minimal-edit honest move: the note's
load-bearing math is unchanged (the runner is unchanged, the
character expansion proof is unchanged), only the title-level
classification is sharpened so the bounded character is explicit.
A cross-family auditor (Anthropic Claude vs prior Codex auditors) then
ratifies the bounded-theorem reading and the pipeline propagates
`retained_bounded`.

This route is the textbook `claim_type-flip-via-tightened-scope`
audit move under `docs/audit/README.md`'s scope-aware fields.
