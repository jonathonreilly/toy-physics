# DM Neutrino Two-Higgs Continuity Sheet Theorem

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
subcone  
**Script:** `scripts/frontier_dm_neutrino_two_higgs_continuity_sheet_theorem.py`

## Question

Once the DM odd-circulant right-Gram target lands on the canonical local
two-Higgs neutrino lane, does the residual local `x <-> y` sheet remain
physically open?

## Bottom line

No, not on the DM lane.

The earlier two-Higgs right-Gram bridge theorem already proved that on the
CP-admissible circulant subcone `d >= 2 r`, the realization is forced onto the
symmetric local slice

- `x_1 = x_2 = x_3 = x`
- `y_1 = y_2 = y_3 = y`

with

- `d = x^2 + y^2`
- `r = x y`

So the only remaining local ambiguity is the swap

`(x,y) <-> (y,x)`.

But the retained DM branch already has one exact local anchor: the universal
Dirac bridge `Y = y_0 I`.

On the two symmetric sheets:

```text
x_+^2 = (d + sqrt(d^2 - 4 r^2))/2
y_+^2 = (d - sqrt(d^2 - 4 r^2))/2

x_- = y_+
y_- = x_+
```

As `r -> 0` with `d > 0` fixed:

- the `+` sheet tends to `sqrt(d) I`
- the `-` sheet tends to a pure cycle-supported monomial class

So continuity to the retained universal bridge picks the `+` sheet uniquely.

## Inputs

This theorem combines:

- the DM two-Higgs right-Gram bridge theorem
- the retained universal Dirac bridge on the DM denominator lane

The point is to remove the residual local sheet ambiguity without importing an
extra admitted PMNS-side right-Gram scalar.

## Exact two-sheet law

On the circulant target

`K_can(d,r,delta)`,

the symmetric two-Higgs realization gives

- `d = x^2 + y^2`
- `r = x y`

Therefore the roots are

```text
x^2, y^2 = (d +- sqrt(d^2 - 4 r^2))/2
```

so the local ambiguity is exactly the swap `x <-> y`.

There is no larger residual family left on this DM subcone.

## Why continuity fixes the sheet

At vanishing deformation `r -> 0`, the DM lane already has the retained local
identity-supported bridge `Y = y_0 I`.

The two symmetric sheets behave differently:

- `x_+ -> sqrt(d)`, `y_+ -> 0`
- `x_- -> 0`, `y_- -> sqrt(d)`

So only the `+` sheet is continuous to the retained universal bridge.

The swapped sheet instead approaches a pure cycle-supported monomial limit,
which is not the retained DM identity-supported bridge.

## Theorem-level statement

**Theorem (DM continuity fixes the residual two-Higgs sheet on the circulant
subcone).** Assume the exact DM two-Higgs right-Gram bridge and the retained
universal Dirac bridge `Y = y_0 I`. Then on the CP-admissible circulant
subcone `d >= 2 r`:

1. the canonical local two-Higgs realization is forced onto the symmetric slice
2. the residual ambiguity is exactly the swap `x <-> y`
3. only the sheet with
   `x^2 = (d + sqrt(d^2 - 4 r^2))/2`,
   `y^2 = (d - sqrt(d^2 - 4 r^2))/2`
   tends continuously to the retained universal bridge as `r -> 0`

Therefore the DM lane fixes the residual local two-Higgs sheet intrinsically by
continuity to the retained universal bridge.

## What this closes

This closes the second live DM-side local ambiguity on the circulant route.

The branch no longer needs to say:

- "the sheet is still open"
- "we still need an admitted right-Gram modulus just to pick the two-Higgs
  sheet"

on this DM circulant subcone.

## What this does not close

This note does **not** derive:

- the two-Higgs extension from the bare axiom
- the values of `d`, `r`, or `delta`
- the odd-circulant coefficient law itself

So it does not close the whole denominator. It closes the local sheet.

## Safe wording

**Can claim**

- on the DM circulant subcone, the local two-Higgs sheet is fixed by continuity
  to the retained universal bridge
- the physical symmetric-sheet coefficients are explicit

**Cannot claim**

- the branch already derives the circulant subcone parameters from the bare
  axiom
- the whole two-Higgs local data law is fully closed

## Command

```bash
python3 scripts/frontier_dm_neutrino_two_higgs_continuity_sheet_theorem.py
```

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_two_higgs_continuity_sheet_theorem.py
```

Last run (2026-05-10): `PASS=6 FAIL=0` on the present worktree. The
runner exercises class A finite-dimensional algebra: the
`d = x^2 + y^2`, `r = x y` symmetric-slice identity; the explicit
two-sheet roots `x_+^2 = (d + sqrt(d^2 - 4 r^2))/2`,
`y_+^2 = (d - sqrt(d^2 - 4 r^2))/2`; and the small-`r` asymptotic
behavior on the `+` and `-` sheets that distinguishes them by
continuity to the retained universal Dirac bridge `Y = y_0 I`.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authority
candidates the load-bearing sheet-continuity step relies on, in
response to the 2026-05-05 audit verdict's `missing_dependency_edge`
repair target (audit row:
`dm_neutrino_two_higgs_continuity_sheet_theorem_note_2026-04-15`). It
does not promote this note or change the audited claim scope, which
remains the conditional algebraic sheet selection on the assumed
symmetric two-Higgs circulant subcone with the imported retained
universal identity-supported bridge.

One-hop authority candidates cited:

- [`DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
  — currently `retained` (audit row:
  `dm_neutrino_dirac_bridge_theorem_note_2026-04-15`). Sibling retained
  authority on the local Dirac-structure algebra carrying the
  identity-supported universal bridge `Y = y_0 I` to which the present
  note's `+` sheet tends continuously as `r -> 0`. Under the cite-chain
  rule a `retained` one-hop authority on the universal Dirac bridge
  supports the continuity selection but does not by itself promote the
  present row, since the two-Higgs right-Gram bridge premise remains a
  class A import.
- [`DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md`](DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md)
  — currently `unaudited` (audit row:
  `dm_neutrino_two_higgs_right_gram_bridge_note_2026-04-15`). Sibling
  candidate authority establishing the symmetric two-Higgs slice
  `x_1 = x_2 = x_3 = x`, `y_1 = y_2 = y_3 = y` with `d = x^2 + y^2`,
  `r = x y` on the CP-admissible circulant subcone `d >= 2 r`, which is
  the slice the present note's continuity selection lives on. Because
  this sibling is `unaudited`, it does not by itself lift the present
  note's effective status under the cite-chain rule.
- [`CHARGED_LEPTON_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md`](CHARGED_LEPTON_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md)
  — currently `retained` (audit row:
  `charged_lepton_two_higgs_canonical_reduction_note`). Adjacent
  retained authority on the canonical two-Higgs reduction in the
  charged-lepton sector, supplying the analogous canonical
  `Y = A + B C` form with `C` the forward `3`-cycle and `A, B`
  diagonal that the present note's symmetric-sheet identity
  parallels on the DM lane.
- [`DM_NEUTRINO_TWO_HIGGS_CLOSURE_ATTACKS_NOTE_2026-04-15.md`](DM_NEUTRINO_TWO_HIGGS_CLOSURE_ATTACKS_NOTE_2026-04-15.md)
  — currently `audited_conditional` (audit row:
  `dm_neutrino_two_higgs_closure_attacks_note_2026-04-15`). Sibling
  bounded-grade authority enumerating closure attacks on the DM
  two-Higgs lane that this continuity sheet selection complements.

Open class D registration targets named by the 2026-05-05 audit
verdict as `missing_dependency_edge`:

- A retained-grade DM two-Higgs right-Gram bridge authority
  establishing the symmetric-slice and circulant-subcone premises as
  one-hop authorities remains required to lift the algebraic
  sheet-selection conclusion to chain closure.
- A retained-grade DM universal Dirac bridge authority specialized to
  the DM denominator lane (rather than the broader retained Dirac
  bridge) remains required to lift the small-`r` continuity premise.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with
load-bearing-step class A and `chain_closes=False`, observing that the
sheet-continuity statement closes conditional on the symmetric
two-Higgs realization and the identity-supported bridge, but that
those bridge premises are imported and not supplied as retained-grade
authorities in the restricted packet. The runner
`scripts/frontier_dm_neutrino_two_higgs_continuity_sheet_theorem.py`
is registered with `runner_check_breakdown = {A: 6, B: 0, C: 0, D: 0,
total_pass: 6}` and genuinely checks the quadratic sheet algebra and
small-`r` support behavior (`PASS=6 FAIL=0` on 2026-05-10), but its
checks remain class A algebra over the canonical matrices and chosen
sample parameters. The cite chain above wires the retained universal
Dirac-bridge authority and the candidate two-Higgs right-Gram bridge
sibling, the retained charged-lepton canonical reduction parallel, and
the bounded closure-attacks sibling, and explicitly registers the two
missing-dependency-edge targets named by the verdict's
`notes_for_re_audit_if_any` field. Effective status remains
`audited_conditional`. The note's `audit_status` is unchanged by this
addendum.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) plus class D
(open-target registration). It does not change any algebraic content,
runner output, or load-bearing step classification. It records the
upstream authority candidates the audit verdict expected, the runner
that exercises the conditional sheet selection, and the
missing-dependency-edge targets named by the verdict's
`notes_for_re_audit_if_any` field. It mirrors the live cite-chain
pattern used by the
`PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md` cluster
(commit `44da750e2`) and the
`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` cluster
(commit `8e84f0c23`). Vocabulary is repo-canonical only.
