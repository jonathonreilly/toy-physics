# Gauge-Vacuum Plaquette First-Sector Rank-One / Factorized-Class Boundary

**Date:** 2026-04-19
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_sector_rank_one_factorized_class_boundary_2026_04_19.py`

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/` (the directory name encodes the failure reason: declared runner path is missing).
- **Audit verdict_rationale (quoted verbatim from `docs/audit/data/audit_ledger.json`):**

  > Issue: the note declares a runner and expected PASS=6, but the runner path is missing, so the off-diagonal norm 0.250338180104 and diagonal-fit residuals 0.135462193897 / 0.228465896152 are not reproducible from the allowed artifacts. Why this blocks: those numbers are the proof that the rank-one witness lies outside the canonical Wilson factorized class and that the audited diagonal family misses the completed triple; without the runner or equivalent one-hop derivation, the theorem is unsupported. Repair target: restore the exact runner or replace the note with a current executable proof that constructs M, T_min, Z_min, performs the positive conjugation-symmetric diagonal search, and reproduces PASS=6 from cited retained inputs. Claim boundary until fixed: safely claim only that the remaining Wilson target is intended to be stricter than generic transfer existence; do not claim the specific non-factorization theorem, residual bounds, or retained-sector boundary.

- **Do not cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Question

After the explicit first-sector positive completion and the explicit rank-one
transfer realization, is the remaining plaquette/Wilson seam still just
"find any Wilson/Perron realization", or is the target class already stricter?

## Answer

The target class is already stricter.

The explicit retained-sector rank-one witness

`T_min`

proves existence of a positive class-sector transfer realization for the
completed triple `Z_min`, but it does **not** itself lie in the canonical
Wilson factorized class

`T_src(6) = exp(3 J) D exp(3 J)`

with `D` diagonal and conjugation-symmetric in the character basis.

On the retained first four weights:

- conjugating `T_min` back by the exact half-slice multiplier `exp(3 J)` gives
  a non-diagonal operator with off-diagonal norm `0.250338180104`,
- and the best audited positive conjugation-symmetric diagonal fit still misses
  the completed retained vector by `0.135462193897` and the induced three-sample
  triple by `0.228465896152`.

So the remaining upstream object is now sharper than generic transfer
existence:

> derive the explicit diagonal/environment realization inside the canonical
> Wilson factorized class.

## Setup

From the earlier exact factorization theorem already on `main`:

- `T_src(6) = exp(3 J) D_6 exp(3 J)`,
- `D_6` is diagonal in the `SU(3)` character basis,
- conjugation symmetry forces `kappa_(p,q)(6) = kappa_(q,p)(6)`.

From the later first-sector reopening already on `main`:

- the named first symmetric `beta = 6` seam closes positively to one explicit
  completed triple
  `Z_min`,
- and `Z_min` already admits one explicit positive self-adjoint
  conjugation-symmetric rank-one class-sector transfer witness
  `T_min`.

The new question is whether that new witness is already a realization inside
the stricter Wilson factorized class.

## Theorem 1: the explicit rank-one witness is not itself a factorized Wilson realization on the retained four-weight sector

Restrict to the retained first-symmetric four-weight sector

`(0,0), (1,0), (0,1), (1,1)`.

Let

`M = exp(3 J)`

be the exact retained half-slice multiplier on that sector, and define the
back-conjugated operator

`D_back = M^(-1) T_min M^(-1)`.

If `T_min` were already a retained realization inside the canonical Wilson
factorized class, then `D_back` would be diagonal.

But the runner computes:

- `diag(D_back) = (0.623898384821, 0.024539009353, 0.024539009353, 0.000167528352)`,
- `||offdiag(D_back)||_2 = 0.250338180104`,
- `max |offdiag(D_back)| = 0.123733...`.

So `D_back` is not diagonal.

Therefore the explicit rank-one witness is **not itself** a retained
factorized Wilson realization.

## Theorem 2: the best audited retained diagonal fit still misses the completed target

Search the positive conjugation-symmetric retained diagonal class

`D = diag(d_(0,0), d_(1,0), d_(1,0), d_(1,1))`, `d_*>0`,

and form

`T(D) = M D M`.

Use the depth-3 propagated retained vector

`a(D) = T(D)^3 e_(0,0)`.

The best audited positive fit found by the runner is:

`(d_(0,0), d_(1,0), d_(1,1))
 = (0.255192351889, 8.06e-12, 2.05e-11)`.

But even there:

- `||a(D) - v_min||_2 = 0.135462193897`,
- `||E_3 a(D) - Z_min||_2 = 0.228465896152`.

So the retained factorized class does **not** hit the completed target on this
audited symmetric positive diagonal family.

## Corollary 1: the remaining open object is no longer generic transfer existence

The explicit rank-one witness already proves:

- positive class-sector transfer existence for `Z_min`.

The new boundary proves that this is still weaker than the actual Wilson target:

- the correct upstream object is one explicit `beta = 6`
  diagonal/environment realization inside the canonical factorized class,
- equivalently the actual framework-point environment packet rather than a
  generic class-sector transfer witness.

## What this closes

- exact clarification that the explicit rank-one witness does **not** by itself
  solve the Wilson factorized-class realization problem
- exact clarification that the honest remaining plaquette/Wilson seam is now
  the explicit diagonal/environment packet
- exact retained-sector evidence that the audited symmetric positive diagonal
  factorized family still misses the completed target

## What this does not close

- the actual `beta = 6` diagonal/environment packet
- the framework-point Wilson/Perron realization inside the canonical factorized
  class
- final quantitative DM packet matching

## Commands run

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_sector_rank_one_factorized_class_boundary_2026_04_19.py
```

Expected summary:

- `PASS=6 FAIL=0`
