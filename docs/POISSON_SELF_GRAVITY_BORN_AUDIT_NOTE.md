# Poisson Self-Gravity Born Audit Note

**Date:** 2026-04-05  
**Status:** bounded - bounded or caveated result note
Poisson-like backreaction loop

**Status authority and audit hygiene (2026-05-10):**
The audit lane has classified this note `audited_conditional` (verdict
2026-05-10). The zero-coupling exact reduction (`epsilon = 0`) and the
frozen-snapshot Born check are sound and survive to machine precision.
The audit-conditional perimeter is on the nonzero-coupling row, where
the runner reports `stepConv = False` and `endConv = False` at
`max_iters = 6`. The supplied runner therefore provides a
finite-six-iteration capped diagnostic, not a converged-loop theorem,
and the unconverged-return code path uses amplitudes propagated before
the last relaxation. Read all "end-to-end Born drift" content in this
note as a capped-iteration diagnostic only; the nonzero-coupling row
is not a converged full nonlinear-loop result. This rigorization edit
makes the conditional perimeter explicit; nothing here promotes
audit_status.

## Artifact chain

- [`scripts/poisson_self_gravity_born_audit.py`](../scripts/poisson_self_gravity_born_audit.py)
- [`logs/runner-cache/poisson_self_gravity_born_audit.txt`](../logs/runner-cache/poisson_self_gravity_born_audit.txt)

## Question

Does the iterated Poisson-like self-gravity loop preserve Born only at the
level of each frozen propagation step, or also end-to-end through the full
loop?

This audit is intentionally narrow:

- one exact 3D lattice family at `h = 0.25`
- one three-slit source set on the input layer
- one screened Poisson-like backreaction loop
- one exact `epsilon = 0` reduction check
- one step-local Born check on a frozen loop snapshot
- one end-to-end Born check through the full iterated loop

## What Born means here

The audit separates two distinct questions:

1. **Step-local Born**
   - freeze the converged field snapshot
   - test the usual three-slit Sorkin `I3/P` on that fixed field

2. **End-to-end Born**
   - run the full nonlinear loop separately for `a`, `b`, `c`, `ab`, `ac`,
     `bc`, and `abc`
   - compute the final detector `I3/P` from the converged loop outputs

That distinction matters because the outer map is nonlinear even if each fixed
field propagation step is linear.

## Frozen result

Representative retained row:

- `epsilon = 0.05`
- source strength `s = 0.004`

Reduction check:

- exact `epsilon = 0` reduction survives exactly

Frozen Born audit row:

| `epsilon` | source strength | step-local Born | end-to-end Born | step converged | end converged |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.05` | `0.0040` | `8.834e-16` | `6.830e-05` | `False` | `False` |

## Safe read

The strict conclusion is:

- the frozen field snapshot remains Born-clean to machine precision
- the full iterated loop does **not** stay machine-clean end-to-end on the
  tested nonzero coupling
- the loop therefore preserves Born only at the per-step / frozen-snapshot
  level on this audit
- the nonzero backreaction map is nonlinear enough to generate a small but
  real end-to-end Born drift

## Honest limitation

This is a narrow audit, not a universal theorem.

- it uses one exact lattice family
- it uses one representative nonzero coupling row
- it demonstrates the key distinction the audit was meant to separate

## Branch verdict

Treat this as:

- **per-step Born survives**
- **end-to-end Born does not remain machine-clean on the tested loop**

So the retained control is still useful, but the iterated backreaction map is
not Born-safe as a full nonlinear evolution.

The "end-to-end" reading above is bounded by the runner's `max_iters = 6`
cap. Both `stepConv` and `endConv` are `False` on the cached run, so the
end-to-end I3/P value is what the loop produces after six iterations,
not a converged steady-state observable. Larger `max_iters` or a slit-
subset-by-subset convergence pass is needed before the end-to-end Born
reading can be sharpened to a converged-loop statement.

## Cited Lane sibling status (audit-explicit)

This audit note has no audit-graph dependencies (`deps = []`); it is a
narrow numerical audit on its own runner. The cited Lane siblings and
their current ledger statuses are:

| Sibling row | `audit_status` | `effective_status` | `claim_type` |
|---|---|---|---|
| [`POISSON_SELF_GRAVITY_LOOP_NOTE`](POISSON_SELF_GRAVITY_LOOP_NOTE.md) | audited_conditional | audited_conditional | bounded_theorem |
| `poisson_self_gravity_loop_v3_note` | audited_conditional | audited_conditional | bounded_theorem |
| `poisson_self_gravity_mechanism_note` | unaudited | unaudited | bounded_theorem |
| `gate_b_poisson_self_gravity_note` | audited_clean | retained_no_go | no_go |

The retained-no-go sibling (`gate_b_poisson_self_gravity_note`) is the
load-bearing closure on the broader Poisson-like self-gravity branch.
This audit's bounded reading is consistent with that no-go: the
zero-coupling reduction is exact (consistent with linearity in the
limit), the frozen-snapshot step-local Born is machine-clean (consistent
with each propagation step being linear), and the end-to-end Born
deviates at finite coupling (consistent with the iterated nonlinear
map not preserving Born as a full evolution). No audit-graph cycle is
introduced by these cite-only references.

## Audit-aware repair path

Per `audit_ledger.json`, `notes_for_re_audit_if_any` for
`poisson_self_gravity_born_audit_note`:

> runner_artifact_issue: cheapest repair is to make the runner enforce
> convergence for all seven slit subsets and recompute final amplitudes
> from the returned field, or split out a separate finite-six-iteration
> diagnostic claim.

Two routes match this audit-stated repair path:

1. **Enforced-convergence runner.** Lift `max_iters` and add a runtime
   assertion that every slit subset (`a`, `b`, `c`, `ab`, `ac`, `bc`,
   `abc`) reaches `stepConv = True` and `endConv = True` before the
   detector probabilities are read. Then recompute final detector
   amplitudes from the returned field rather than from the pre-last-
   relaxation propagated amplitudes. This would let the "end-to-end
   Born drift at nonzero coupling" reading promote from a
   capped-iteration diagnostic to a converged-loop theorem.
2. **Scope split.** Keep this note as a finite-six-iteration diagnostic
   and move any converged-loop Born statement to a separate note that
   ships a runner with hard-bar PASS assertions on convergence (compare
   the `--quick` mode and five hard-bar pattern in the sibling
   `poisson_self_gravity_loop` runner).

Neither route is attempted in this rigorization edit; both are open.
