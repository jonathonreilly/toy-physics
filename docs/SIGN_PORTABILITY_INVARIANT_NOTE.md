# Sign Portability Invariant Note

**Date:** 2026-04-06 (status line narrowed 2026-04-28 per audit-lane verdict)
**Status:** bounded conditional comparison invariant across reported sign-law families; the comparison runner is not registered in the audit ledger and the cited family notes are not registered as one-hop dependencies. Not a tier-ratifiable portability theorem or independent order parameter.

## Artifact Chain

- [`scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py`](/Users/jonreilly/Projects/Physics/scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py)
- [`logs/2026-04-06-sign-portability-invariant.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-sign-portability-invariant.txt)
- registered runner-cache output: [`logs/runner-cache/SIGN_PORTABILITY_INVARIANT_COMPARE.txt`](/Users/jonreilly/Projects/Physics/logs/runner-cache/SIGN_PORTABILITY_INVARIANT_COMPARE.txt)
- first-principles derivation within one family (load-bearing dependency for the four gates):
  [`docs/SIGN_PORTABILITY_INVARIANT_FAMILY_SECOND_GROWN_DERIVATION_THEOREM_NOTE_2026-05-09.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_FAMILY_SECOND_GROWN_DERIVATION_THEOREM_NOTE_2026-05-09.md)
- retained family notes: [`archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md), [`docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md), [`docs/SECOND_GROWN_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SECOND_GROWN_FAMILY_SIGN_NOTE.md), [`docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md), [`docs/FOURTH_FAMILY_QUADRANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FOURTH_FAMILY_QUADRANT_NOTE.md)
- holdout confirmation: [`archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_RADIAL_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_RADIAL_NOTE.md), [`archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_RADIAL_FM_TRANSFER_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_RADIAL_FM_TRANSFER_NOTE.md), [`docs/FIFTH_FAMILY_RADIAL_BOUNDARY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIFTH_FAMILY_RADIAL_BOUNDARY_NOTE.md)

### Primary runner behavior (2026-05-09)

`scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py` runs in two blocks.

**Block 1 — derivation within one family.** The runner re-runs the
second grown family at a small two-row subset (`drift=0.0, seed=0` and
`drift=0.2, seed=1`) by importing the family construction and
measurement code directly. It checks the four invariant gates on each
row at the same row-level thresholds used in Block 2. This block is
the numerical-side companion to the algebraic / leading-order proofs
in
[`SIGN_PORTABILITY_INVARIANT_FAMILY_SECOND_GROWN_DERIVATION_THEOREM_NOTE_2026-05-09.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_FAMILY_SECOND_GROWN_DERIVATION_THEOREM_NOTE_2026-05-09.md).

**Block 2 — cross-family corollary check.** As before, the runner
reads the registered per-row outputs of each one-hop family runner
(the runner-cache files when populated, the dated logs in `logs/` as
fallback) and asserts the four common thresholds that the note
proposes as the signed-control fixed point:

- G1 zero-source cancellation: `|zero| <= 1e-12` on every row
- G2 neutral same-point cancellation: `|neutral| <= 1e-12` on every row
- G3 plus/minus antisymmetry: `|plus+minus| / max(|plus|,|minus|) <= 5e-3`
  on every row
- G4 unit-slope tolerance: `|exp-1| <= 5e-3` on every row the family
  runner itself accepted (sign orientation OK)

Rows the family runner rejected for sign orientation are surfaced as
explicit basin/seed exclusions in the runner output, per family. The
runner exits 0 only when both blocks pass; otherwise it exits 1. The
claim scope of this note is unchanged: it remains a bounded
conditional comparison invariant, not a tier-ratifiable portability
theorem. The improvement is that the load-bearing step (existence of
the signed-control fixed point in at least one family) is now backed
by a derivation rather than by a cross-note comparison.

## Question

What is the smallest invariant that explains why signed-source transfer now
survives across the retained structured families?

## Comparison

| family | exact controls | sign orientation | weak-field response | basin shape |
| --- | --- | --- | --- | --- |
| Grown transfer basin | exact zero-source and neutral same-point cancellation | retained on nearby rows | `F~M = 1.000` | narrow and selective |
| Alternative connectivity family | exact zero-source and neutral same-point cancellation | retained on passing rows | `F~M = 0.999994` | bounded but broadest of the retained sign-law families |
| Second grown-family sign | exact zero-source and neutral same-point cancellation | retained on all tested rows | mean exponent `1.000072` | independent basin, still narrow in architecture space |
| Third grown-family sign | exact zero-source and neutral same-point cancellation | retained on passing rows | mean exponent `0.999842` | bounded drift basin |
| Fourth family quadrant | exact zero-source and neutral same-point cancellation | retained on passing rows; mixed at `drift=0.2` | alpha near `1.0` | narrow and seed-selective |

## Out-Of-Band Confirmation

The later fifth-family radial holdout agrees on the same control surface:

| family | exact controls | sign orientation | weak-field response | basin shape |
| --- | --- | --- | --- | --- |
| Fifth family radial | exact zero-source and neutral same-point cancellation | retained on sampled rows; flips at the interior boundary | mean exponent `0.999439` | narrow holdout confirmation |

## Safe Read

Across the retained sign-law basins, the thing that survives is not the
geometry family itself.

What survives is the signed-control fixed point:

- exact zero-source cancellation
- exact neutral same-point cancellation
- plus/minus antisymmetry
- weak-field response pinned near unit slope

The family construction only changes basin width and selectivity.
Some families are broad, some are narrow, and some are seed-selective, but the
sign-law fixed point remains the same.

### Load-bearing step (corollary structure)

The load-bearing claim "across the retained sign-law basins, the
signed-control fixed point survives" is not a free-standing cross-note
comparison.  It is now backed by a first-principles derivation within
ONE retained sign-law family (the second grown family), in
[`SIGN_PORTABILITY_INVARIANT_FAMILY_SECOND_GROWN_DERIVATION_THEOREM_NOTE_2026-05-09.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_FAMILY_SECOND_GROWN_DERIVATION_THEOREM_NOTE_2026-05-09.md).

That note derives the four gates from the action and the
source-construction map: G1 and G2 as exact algebraic identities at
finite source strength, G3 and G4 as leading-order weak-field identities
with explicit bounded second-order remainders.

The cross-family invariance asserted in the comparison table above is
then a **corollary**: any other retained sign-law family that shares the
three structural inputs (linear-in-charge source-to-field map with
deterministic anchor selection, forward-only DAG propagation with
`act = L (1 + lf)`, and centroid readout `sum |amps|^2 z / sum |amps|^2`
over the detector layer) inherits the same four gates by the same proof
steps, with a family-specific remainder constant `C_F`. The five core
families and the holdout family in this note all satisfy these
structural inputs, so the runner's family-by-family threshold check is
verifying the corollary numerically rather than asserting an unbacked
cross-note pattern.

## Exact Mismatch

- basin width is not invariant
- seed selectivity is not invariant
- complex-action selectivity is not part of this invariant
- the `gamma = 0` branch analog is not the same control surface as the
  zero-source signed branch

## Final Verdict

**bounded conditional comparison positive:** signed-source transfer is
portable across the reported structured sign-law families under the
registered runner thresholds, with the signed-control fixed point as the
comparison invariant and basin width as the family-dependent variable. This
does not promote the note to a tier-ratifiable portability theorem.

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, high criticality, 124 transitive
descendants):

> Issue: the `proposed_retained` portability invariant is a
> cross-family comparison, but the audit packet provides no
> registered one-hop family notes and no primary runner/output for
> `SIGN_PORTABILITY_INVARIANT_COMPARE.py`. Why this blocks: a hostile
> auditor cannot verify that the named families are themselves
> retained, that their exact controls and weak-field exponents use
> compatible protocols, or that the claimed signed-control fixed
> point is independent of basin width/seed selectivity rather than a
> summary label imposed after filtering passing rows.

> Claim boundary until fixed: it is safe to say the source note
> proposes a conditional comparison invariant across reported
> sign-law families; it is not yet an audited portability theorem or
> independent order parameter.

## What this note does NOT claim

- A tier-ratifiable portability theorem.
- An independent order parameter beyond the cross-family comparison.
- That the in-family derivation theorem note is itself fully
  unconditional: per the audit ledger that theorem is
  `audited_conditional` on a row-wise lower bound for the detector
  denominator and the plus-source linear response (G4 conditional).
  Block 1 of the runner therefore verifies G1/G2/G3/G4 numerically at
  the working source strength but does not promote the theorem note
  beyond its own conditional status.

## Audit dependency repair links

The one-hop dependencies of this note are wired by markdown links in the
artifact chain above and are regenerated into the audit ledger by the
pipeline. The live audit ledger owns their effective statuses. The
cross-family comparison block of the runner reads the same family
runner-cache outputs that their own runners produce.

| dep claim_id | family runner | runner-cache file |
| --- | --- | --- |
| `sign_portability_invariant_family_second_grown_derivation_theorem_note_2026-05-09` | (this runner, derivation block) | n/a (in-process) |
| `alt_connectivity_family_basin_note` | `scripts/ALT_CONNECTIVITY_FAMILY_BASIN.py` | `logs/runner-cache/ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP.txt` |
| `second_grown_family_sign_note` | `scripts/SECOND_GROWN_FAMILY_SIGN_SWEEP.py` | `logs/runner-cache/SECOND_GROWN_FAMILY_SIGN_SWEEP.txt` |
| `third_grown_family_sign_note` | `scripts/THIRD_GROWN_FAMILY_SIGN_SWEEP.py` | `logs/runner-cache/THIRD_GROWN_FAMILY_SIGN_SWEEP.txt` |
| `fourth_family_quadrant_note` | `scripts/FOURTH_FAMILY_QUADRANT_SWEEP.py` | `logs/runner-cache/FOURTH_FAMILY_QUADRANT_SWEEP.txt` |
| `fifth_family_radial_boundary_note` | `scripts/FIFTH_FAMILY_RADIAL_FAILURE_AUDIT.py` | `logs/runner-cache/FIFTH_FAMILY_RADIAL_SWEEP.txt` |

The "Grown transfer basin" entry in the cross-family table above is
verified via the dated log
`logs/2026-04-06-nonlabel-grown-drift-basin-sweep.txt` (the
runner-cache file `GROWN_TRANSFER_BASIN_SWEEP.txt` exists but is
empty in the current cache); the underlying basin authority is the
`grown_transfer_basin_note` row in the audit ledger, which is
referenced by the artifact chain but the relevant rows are also
recoverable from `alt_connectivity_family_basin_note` and the second
grown family. The cross-family threshold check in Block 2 is therefore
identical regardless of which path is used to populate the basin row.

## What would close this lane (Path A future work)

Promoting from bounded conditional to retained would require:

1. ~~Registering the comparison runner/log.~~ Done: the runner
   `scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py` is the registered
   runner for this note in the audit ledger, with cached output at
   `logs/runner-cache/SIGN_PORTABILITY_INVARIANT_COMPARE.txt`.
2. ~~Adding the family and holdout notes as one-hop dependencies with
   their current audit statuses.~~ Done: the six dependencies above
   are the audit ledger `deps` list for this row.
3. ~~Making the runner assert common thresholds for zero-source
   cancellation, neutral same-point cancellation, antisymmetry,
   unit-slope tolerance, and basin/seed exclusions.~~ Done: Block 2
   of the runner reads each family's per-row records and asserts the
   four common gates `ZERO_TOL=1e-12`, `NEUTRAL_TOL=1e-12`,
   `ANTISYM_TOL=5e-3`, `EXP_TOL=5e-3`, with rejected rows surfaced
   as explicit basin/seed exclusions per family.
4. Closing the residual G4 lower-bound condition on the in-family
   derivation theorem note (an open item on that note, not on this
   one). Until that lower-bound is supplied, the cross-family
   unit-slope corollary remains conditional on the same nonzero
   linear response assumption.
