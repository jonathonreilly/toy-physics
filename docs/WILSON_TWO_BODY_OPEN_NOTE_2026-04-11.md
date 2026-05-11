# Wilson Two-Body Open-Lattice Note

**Date:** 2026-04-11  
**Status:** bounded companion on the current `main` surface; outside flagship core
**Claim type:** bounded_theorem
**Primary runner:** `scripts/frontier_wilson_two_body_open.py`
**Companion runners:**
- `scripts/frontier_wilson_two_body_laws.py` (post-selected law characterizations)

**Audit-conditional perimeter (2026-05-10):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
supplied runner source and stdout close the narrow 8/8 attractive and
clean primary-runner surface. The full source-note conclusion also
depends on distance-falloff, partner-source-scaling, and screening-
mass sweep claims whose companion runner source/stdout are not
supplied and have no one-hop authority in the restricted packet."
This rigorization edit only sharpens the boundary of the conditional
perimeter; nothing here promotes audit status. The supported
content of this note is exactly the §"Open-Boundary Wilson Result"
8/8 attractive / 8/8 clean primary-runner surface at `side=11,13`,
`G=5`, `mu^2=0.22`, `d=3..6` (backed by
[`scripts/frontier_wilson_two_body_open.py`](../scripts/frontier_wilson_two_body_open.py)
and its registered cache); the §"Law Sweeps" distance falloff,
§"Partner-source scaling", §"Screening-Mass Addendum", and
§"Both-Masses Audit" rows are out of the restricted packet's authority
and are bounded companion characterizations carried only by the
secondary `frontier_wilson_two_body_laws.py` and
`frontier_newton_both_masses.py` runners — they are not load-bearing
for the supported perimeter.

## Inputs (registered runners with caches)

The note's load-bearing claims are backed by two registered audit runners:

- `scripts/frontier_wilson_two_body_open.py` (cache:
  `logs/runner-cache/frontier_wilson_two_body_open.txt`) — the
  open-boundary mutual-attraction probe (8/8 attractive, 8/8 clean).
- `scripts/frontier_wilson_two_body_laws.py` (cache:
  `logs/runner-cache/frontier_wilson_two_body_laws.txt`) — the
  post-selected distance-falloff and partner-source-scaling fits, plus
  the screening-mass `mu^2` sweep.

Two runner stems mentioned in earlier sections of this note are no longer
present in `scripts/`:

- `frontier_wilson_two_body.py` — the periodic-box probe; superseded
  structurally by the open-boundary runner above. The narrative paragraph
  describes a small-window observation that matches the open runner's
  same-side window structure but is not a load-bearing entry point for
  the open-surface law characterization.
- `frontier_newton_both_masses.py` — the both-masses observable
  referenced in the "Both-Masses Audit" section. The honest read of this
  section is the failure-mode statement (action-reaction balance fails on
  every row); the supporting numerics are historical context for why the
  lane stops short of a retained Newton derivation, not retained
  calibration.
- `frontier_wilson_newton_law.py` — explicitly flagged in §"Important
  Guardrail" as not the clean next test. No load-bearing claim depends on
  it.

The retained content of this note is the open-boundary attractive-signal
calibration plus the screened-falloff sweep, both backed by the
registered runner caches above. Anything mentioned only in narrative for
historical motivation is not a retained claim of this note.

## Question

Does the Wilson-fermion two-orbital Hartree lane produce a genuine mutual
attraction signal once the staggered parity oscillation is removed, and if so,
how much of a Newton-like law can actually be retained?

## Periodic Wilson Result

`frontier_wilson_two_body.py` gives a real narrow clean window:

- `G=5`
- `d=3,4`
- both `mu^2 = 0` and `mu^2 = 0.22`
- early-time mutual acceleration is clean and attractive with `SNR ~ 4-5`

But it also fails immediately beyond that window:

- `d=5,6` flips sign on the same `side=9` periodic lattice
- all larger `G` become noisy

So the periodic Wilson result is **not** Newton-law closure. It is a clean
short-range window on a small periodic box.

## Open-Boundary Wilson Result

`frontier_wilson_two_body_open.py` removes the periodic-image contamination and
tests the same lane on open 3D Wilson lattices.

Audited surface:

- `side = 11, 13`
- `G = 5`
- `mu^2 = 0.22`
- separations `d = 3,4,5,6`

Result:

- `8/8` configurations attractive
- `8/8` configurations clean (`SNR > 2`)

Representative rows:

- `side=11, d=3`: `a_mut = -0.566674 ± 0.058502` (`SNR=9.69`)
- `side=11, d=6`: `a_mut = -0.056988 ± 0.006457` (`SNR=8.83`)
- `side=13, d=3`: `a_mut = -0.567354 ± 0.058224` (`SNR=9.74`)
- `side=13, d=6`: `a_mut = -0.056692 ± 0.006955` (`SNR=8.15`)

The controls are also much cleaner than in the periodic box:

- `FREE` drift is tiny on the larger open surfaces
- `SELF_ONLY` stays near flat or weakly outward
- `SHARED` closes inward strongly

So the Wilson mutual-attraction signal is real on the open surface.

## Law Sweeps

`frontier_wilson_two_body_laws.py` extends the open-lattice result.

These law fits are a **post-selected characterization surface**:

- the fit rows are the subset already labeled `ATTRACT` and `CLEAN`
- they are useful as bounded calibration on the audited open Wilson surface
- they are **not** a blind law estimate over all sampled rows

### Distance falloff

Surface:

- `side = 11, 13, 15`
- `G = 5`
- `mu^2 = 0.22`
- clean attractive rows only

Fits:

- global clean fit: `|a_mut| ~ d^-3.406` (`R^2 = 0.9935`)
- `side=11`: `d^-3.139` (`R^2 = 0.9968`)
- `side=13`: `d^-3.313` (`R^2 = 0.9960`)
- `side=15`: `d^-3.500` (`R^2 = 0.9939`)

This is a very clean post-selected power-law characterization, but it is
**not** Newtonian `1/r^2`.

### Partner-source scaling

At `side=13`, `d=4`:

- `mB = 0.5`: `a_mut = -0.206150`
- `mB = 1.0`: `a_mut = -0.246222`
- `mB = 1.5`: `a_mut = -0.314107`
- `mB = 2.0`: `a_mut = -0.346657`
- `mB = 3.0`: `a_mut = -0.503814`

Fit:

- `|a_mut| ~ mB^0.483` (`R^2 = 0.9363`)

So the partner-source dependence is monotone and real on the selected clean
surface, but clearly sublinear on that screened surface.

## Both-Masses Audit

`frontier_newton_both_masses.py` now runs the first honest next-step observable
on the same open weak-screening surface:

- `side = 15`
- `G = 5`
- `mu^2 = 0.001`
- `d = 5`
- each orbital gets its own physical mass in **both**
  - the Poisson source
  - the Wilson Hamiltonian diagonal
- the retained observable is early-time mutual momentum transfer
  - `P_A^mut = M_A * <v_A^shared - v_A^self>`
  - `P_B^mut = M_B * <v_B^self - v_B^shared>`

This is materially better than the earlier source-only sweep, but it still does
**not** close a retained `M_A M_B` law.

Direct rerun on that surface:

- anchor slice `P_A^mut` vs `M_B` at `M_A = 1.0`: `R^2 = 0.9445`
- anchor slice `P_B^mut` vs `M_A` at `M_B = 1.0`: `R^2 = 0.9400`
- full-grid normalized `P_A^mut / M_B`: `CV = 35.4%`
- full-grid normalized `P_B^mut / M_A`: `CV = 37.5%`
- action-reaction balance `P_A^mut + P_B^signed`: fails on every row

The structural reason is also clearer now:

- once both inertial masses vary, the shared-minus-self residual is dominated by
  a **common Wilson-gap slowdown**
- that slowdown is not an exchanged momentum channel
- so the residual does not behave like a clean two-body force law

So the honest read is:

- the open Wilson lane supports a real distance-law calibration
- it supports bounded slice-wise source/response structure
- it still does **not** support retained full Newton closure
- the current both-masses observable fails because common propagation slowing
  overwhelms any clean action-reaction signal

## Honest Interpretation

The Wilson lane has improved substantially over the staggered two-body lane:

- mutual attraction survives when tested with a genuine two-orbital control
- the open-lattice surface removes the small-box periodic sign flip
- the signal is clean enough to fit

But the law that emerges is:

- **real**
- **clean**
- **non-Newtonian**

Current best statement:

> Open-boundary Wilson two-orbital Hartree dynamics produces a robust mutual
> attraction channel on the audited `G=5`, `mu^2=0.22` surface, with a clean
> screened distance falloff `|a_mut| ~ d^-3.4` and sublinear partner-source
> scaling `|a_mut| ~ m_B^0.48`.

That is scientifically meaningful, but it is not the Nature-threshold
“emergent Newton law” claim.

## Screening-Mass Addendum

The later `mu^2` sweep narrows the interpretation further:

- `mu^2 = 0.22` gives `alpha = -3.315`
- `mu^2 = 0.05` gives `alpha = -2.392`
- `mu^2 = 0.01` gives `alpha = -1.992`
- `mu^2 = 0.005` gives `alpha = -1.927`
- `mu^2 = 0.001` gives `alpha = -1.871`

So the steep exponent is not a fixed law of the open surface. It is strongly
screening-controlled and softens toward Newton-compatible scaling as `mu^2` is reduced.

## Important Guardrail

`frontier_wilson_newton_law.py` should **not** be treated as the clean next
test in its current form. Despite its header, it still uses a periodic cubic
lattice and circular-mean separation, so it does not actually remove the image
artifact that the open-lattice harness was built to avoid.

## What This Supports

This Wilson result is strongest as:

- a bounded companion mutual-attraction result
- a counterexample to “the two-body lane is pure artifact”
- a launch point for understanding why the discrete mutual channel follows a
  steeper-than-Newton falloff

It does **not** yet support:

- retained full `F ∝ M_1 M_2 / r^2`
- a valid action-reaction law on the both-masses grid
- a promoted Nature-level Newton-law claim

## Exact Next Observable

That next observable has now been run, and it failed honestly.

So the next step is narrower:

- keep the same open weak-screening Wilson surface
- redesign the mutual-channel readout so it suppresses the common slowdown mode
- likely candidates are:
  - local momentum flux through the mid-plane
  - weaker-coupling / lighter-mass windows where the shared-minus-self residual
    stays perturbative
  - a directly antisymmetrized impulse observable instead of centroid-only
    kinematics

Until one of those produces a clean equal-and-opposite signal, the Wilson lane
should be cited as a distance-law calibration plus a failed both-masses closure,
not as a retained Newton derivation.
