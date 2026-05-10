# `S^3` + Anomaly-Forced Time: Axiom-First Spacetime Lift

**Status:** open route survey — kinematic background candidate with explicitly
named missing dynamics theorem. **Not** a full-GR closure.
**Date:** 2026-04-14 (audit-narrowing refresh: 2026-05-10)
**Branch:** `codex/review-active`
**Purpose:** route-2 assessment from
[`FULL_GR_AXIOM_FIRST_PATHS_NOTE.md`](FULL_GR_AXIOM_FIRST_PATHS_NOTE.md)
**Type:** open_gate (route-survey)
**Status authority:** independent audit lane only.
**Authority role:** identifies, but does not close, a candidate axiom-first
GR-lift architecture. Names the missing dynamics-bridge primitive as the
single open theorem target for this route.

## Audit boundary

This note is an open-route survey. It does two things:

1. **Records the kinematic background candidate** `PL S^3 x R` as the unique
   target obtained by composing two existing upstream authorities:
   - the `PL S^3` compactification family (cited; not closed in this note);
   - the anomaly-forced time-direction theorem (cited; not closed in this
     note).
   The composition `PL S^3 x R` itself is a kinematic statement at the level
   of background topology, not a dynamics derivation.
2. **Names the missing dynamics bridge** as the single open theorem target
   needed to lift this route to a full-GR closure. No such bridge is
   constructed inside this note.

Under the rubric, this row is therefore an `open_gate` route survey, not a
positive- or bounded-theorem closure. It is **not** a GR closure on `main`
and it does **not** propose retained or positive-theorem promotion.

**Cited authorities (one-hop deps; cited but not closed in this note):**

- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  (`claim_type: bounded_theorem`) — anomaly-forced single-time-direction
  result. This note imports its `d_t = 1` conclusion as a kinematic input
  to the background candidate.
- [`S3_BOUNDARY_LINK_THEOREM_NOTE.md`](S3_BOUNDARY_LINK_THEOREM_NOTE.md)
  (`claim_type: positive_theorem`, `audit_status: audited_conditional`) —
  PL boundary-link disk theorem on `B_R`, supports the `PL S^3` compactification
  family.
- [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md)
  (`claim_type: bounded_theorem`, `audit_status: audited_conditional`) —
  PL cap-uniqueness, supports the `PL S^3` compactification family.

**Admitted-context derivation gap (real, not import-redirect):**

This note explicitly admits there is no in-atlas theorem that turns the
kinematic background `PL S^3 x R` into tensor/metric dynamics. The route is
blocked by the absence of any one of:

1. an exact spacetime-lift observable from the `S^3` + anomaly stack;
2. an exact action whose Euler-Lagrange equations give the GR field law on
   the lifted background;
3. a uniqueness theorem saying the only compatible dynamical lift is the GR
   one.

This is a **real derivation gap**, not a dependency-citation issue. No
retained, bounded, or proposed theorem on the current atlas closes any of
(1)-(3) for this route.

## Verdict (scope-bounded)

**Kinematically clean, dynamically unclosed.**

The current atlas supports a clean axiom-first kinematic background candidate:

- `S^3` topology is supported by the cited PL boundary-link / cap-uniqueness
  theorems, which themselves are `audited_conditional` (not retained-grade);
- anomaly-forced time is supported by the cited `ANOMALY_FORCES_TIME_THEOREM`
  (bounded_theorem).

Their composition gives the kinematic background candidate

    PL S^3 x R.

The atlas does **not** contain an exact theorem that turns that background
into tensor/metric dynamics. In particular:

- no exact `S^3`-to-curvature law is present;
- no exact anomaly-to-Einstein-field-equation derivation is present;
- no exact discrete variational action is present for this route.

So route 2 is not a full-GR proof path yet. It is a clean kinematic
background candidate with a precise, named, currently-open dynamics theorem.

## What the route would need

The route becomes theorem-grade only if one can derive at least one of:

1. an exact spacetime-lift observable from the `S^3` + anomaly stack
2. an exact action whose Euler-Lagrange equations give the GR field law on
   the lifted background
3. a uniqueness theorem saying the only compatible dynamical lift is the GR
   one

Without one of those, the route remains a background theorem, not a full
gravity closure theorem.

## Route 2 in context

The current `FULL_GR_AXIOM_FIRST_PATHS_NOTE.md` survey treats this as one of
the top three alternatives because it uses only retained topology and
chirality/time tools. That is still correct.

But the route is now sharper than the survey wording alone suggests:

- `S^3` is exact and reusable
- anomaly-forced time is exact and reusable
- the combined lift `PL S^3 x R` is the right kinematic target
- the missing piece is a genuine dynamical bridge

## Full 10-route survey

Against the current atlas and axioms, the 10 candidate architectures are:

1. Exact support-side tensor observable on `A1 x {E_x, T1x}`.
2. Exact support-side Schur / Dirichlet tensor action.
3. Axiom-first spacetime lift from `S^3` and anomaly-forced time.
4. Observable-principle effective-action route.
5. Gauge-matter-first backreaction route.
6. Exact finite-rank source-to-metric theorem.
7. Direct lattice Green / resolvent route to the full metric.
8. Discrete 4D variational action route.
9. Geometric RG / projective-shape flow route.
10. Obstruction-first theorem with a minimal new primitive.

The current ranking still stands:

1. support-side tensor observable
2. `S^3` + anomaly-forced-time spacetime lift
3. exact finite-rank source-to-metric theorem

## Runner result

This row has no registered runner. The route ingredients live on the cited
upstream authorities and are individually audited there:

- PL `S^3` compactification — cited from
  [`S3_BOUNDARY_LINK_THEOREM_NOTE.md`](S3_BOUNDARY_LINK_THEOREM_NOTE.md) and
  [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md) (both
  `audited_conditional`).
- Anomaly-forced time — cited from
  [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  (`bounded_theorem`).
- The atlas does not yet contain an exact dynamics bridge for this route;
  this is the sharp, currently-open blocker.

This row claims **no** runner result of its own.

## Bottom line

Route 2 is **not** a GR closure on `main`. It is a clean axiom-first
**kinematic** background candidate with a precise, currently-open dynamics
theorem. This row is `open_gate` and remains so until one of the named
dynamics-bridge primitives is constructed and audited on a separate row.
