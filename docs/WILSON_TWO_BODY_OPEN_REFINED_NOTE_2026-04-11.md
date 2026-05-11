# Wilson Two-Body Open-Lattice Refinement Note

**Date:** 2026-04-11  
**Status:** bounded companion refinement note
**Claim type:** bounded_theorem
**Scripts:**  
- `frontier_wilson_two_body_open_refined.py`

**Audit-conditional perimeter (2026-05-08):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
restricted packet contains no cited retained authority, no runner
stdout, and no runner source for the reported sweep and fits. The
missing step is an auditable computation or certificate showing the
25 run outputs and regression exponents from the stated Wilson
setup." This rigorization edit only sharpens the boundary of the
conditional perimeter; nothing here promotes audit status. The
supported content of this note is the structural framing: the open-
lattice Wilson refinement protocol, the post-selected-only fit
methodology (already declared in §"Fits"), and the qualitative
conclusion that the law remains non-Newtonian under refinement. The
numerical rows (25 run table, side-by-side fits at side ∈ {11..19},
representative `a_mut` values, side-binned exponents -3.139..-3.837,
the §"Screening Addendum" `mu^2`-controlled crossover) are not
independently reproduced from a registered runner stdout in the
audit packet; they are bounded retained values cited from the
companion runner `scripts/frontier_wilson_two_body_open_refined.py`
which is referenced in the source-note header but is not in the
restricted packet's load-bearing one-hop set. A future runner-cache
deposit producing the 25-run table and the per-side regression
exponents would close the missing-stdout gap; that is the prescribed
repair path.

## Question

Does the clean open-lattice Wilson two-body mutual-attraction law soften toward
Newtonian `d^-2` scaling when the open surface is enlarged, or does it remain a
distinct non-Newtonian universality class?

## Setup

This note extends the audited open-boundary Wilson lane from:

- `frontier_wilson_two_body_open.py`
- `frontier_wilson_two_body_laws.py`

using larger open 3D surfaces and the same two-orbital Hartree mutual-channel
observable.

Fixed parameters:

- `G = 5`
- `mu^2 = 0.22`
- symmetric center placement
- `SHARED`, `SELF_ONLY`, `FREE`, `FROZEN` controls
- early mutual acceleration from separation(t)

Surfaces tested:

- `side = 11, 13, 15, 17, 19`
- separations `d = 3` up to the largest interior separation on each side

## Result

Every tested configuration remained attractive and clean.

Across all 25 runs:

- `25/25` attractive
- `25/25` clean (`SNR > 2`)

Representative rows:

- `side=11, d=3`: `a_mut = -0.566674`, `SNR=9.69`
- `side=13, d=6`: `a_mut = -0.056692`, `SNR=8.15`
- `side=17, d=8`: `a_mut = -0.015413`, `SNR=8.08`
- `side=19, d=9`: `a_mut = -0.008356`, `SNR=8.06`

## Fits

These fits are again a **post-selected characterization surface** on the
audited open Wilson lane:

- only rows already labeled `ATTRACT` and `CLEAN` enter the fit
- the result is useful as bounded open-surface calibration
- it is **not** a blind law estimate over every sampled row

Clean attractive rows only:

- global fit over all tested sides: `|a_mut| ~ d^-3.669` (`R^2 = 0.9896`)
- `side=11`: `d^-3.139` (`R^2 = 0.9968`)
- `side=13`: `d^-3.313` (`R^2 = 0.9960`)
- `side=15`: `d^-3.500` (`R^2 = 0.9939`)
- `side=17`: `d^-3.671` (`R^2 = 0.9920`)
- `side=19`: `d^-3.837` (`R^2 = 0.9899`)
- combined `side >= 15`: `d^-3.725` (`R^2 = 0.9900`)

## Interpretation

The refinement sweep does **not** show a crossover toward Newtonian `d^-2`
scaling.

Instead:

- the law remains a clean power law
- the exponent stays well steeper than `-2`
- the larger-side fits drift slightly steeper, not softer

Best current statement:

> Open-boundary Wilson two-orbital Hartree dynamics supports a robust
> mutual-attraction channel whose distance law remains non-Newtonian under
> refinement, with a clean power-law falloff near `|a_mut| ~ d^-3.7` on the
> audited larger open surfaces.

## Caveats

- This is still a Hartree two-orbital construction, not a fully interacting
  many-body Newton-law derivation.
- The fit is taken from the clean attractive subset only, as in the audited
  open-lattice lane, so it should be read as a post-selected characterization
  rather than a blind law estimate.
- The result speaks to the open 3D Wilson surface at `G=5`, `mu^2=0.22`; it
  does not yet establish a universal law across couplings or masses.

## Screening Addendum

This note is still accurate for the fixed `mu^2 = 0.22` surface it audited.
The later screening sweep narrows the interpretation:

- the steep exponent at `mu^2 = 0.22` is real on that surface
- the exponent moves monotonically with `mu^2`:
  - `-3.290` at `mu^2 = 0.22`
  - `-2.732` at `mu^2 = 0.10`
  - `-2.394` at `mu^2 = 0.05`
  - `-1.996` at `mu^2 = 0.01`
  - `-1.872` at `mu^2 = 0.001`
  - `-1.857` at `mu^2 = 0.0`
- so the steep law is not a fixed universality class independent of screening

See `WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*)
for the screening-controlled crossover.

## Conclusion

The open-lattice Wilson distance law is best read as a screened-law result:
the default `mu^2 = 0.22` surface is steep and clean, but the exponent moves
toward Newtonian scaling as screening is removed.
