# Cosmology Scale Identification and Reduction

**Date:** 2026-04-15 (audit-prep runner-registration + cite-chain rigorize 2026-05-16)
**Status:** bounded/conditional cosmology-lane synthesis on `main`. Current ledger
`audit_status: unaudited`, `effective_status: unaudited`, `claim_type:
bounded_theorem` (previous `audited_conditional` verdict from 2026-05-05
was invalidated when criticality increased and the row is queued for
re-audit; the prior verdict's `missing_bridge_theorem` repair target
drives this rigorize pass). Bounded scope is unchanged; runner
registration + extended cite-chain are graph-bookkeeping only.
**Primary runner:** `scripts/frontier_cosmology_scale_identification.py`
**Claim type:** bounded_theorem
**Claim scope:** the algebraic reduction recorded in §§1–3 — `Lambda = 3/R_Lambda^2 = 3 H_inf^2/c^2`,
`d ln rho_Lambda / d ln a = 0 ==> w = -1`, and `Omega_Lambda = (H_inf/H_0)^2 = (R_H(now)/R_Lambda)^2` —
on the post-closure GR/QG surface, treating the upstream same-surface scale identification and
matter-content bridge as cite-chain dependencies (see "Audit dependency repair links" below) rather
than as first-principles closures within this packet.
**Upstream authorities (current ledger statuses, not assertions of retainedness):**
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
(unaudited),
[`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md)
(audited_conditional),
[`OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`](OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md)
(unaudited),
[`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md)
(unaudited),
[`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
(unaudited).

## Verdict

The cosmology lane is tighter than the older companion notes made it look.

On the current post-closure gravity/QG stack:

1. the cosmological-constant companion and the `w = -1` companion now sit on
   the same fixed-gap vacuum surface;
2. the natural scale is the de Sitter curvature radius
   `R_Lambda = sqrt(3/Lambda) = c/H_inf`, not the present-day Hubble radius
   `c/H_0`;
3. therefore the remaining remaining blocker for promoting the cosmology package is
   not a second independent `Lambda` or `w` theorem, but the matter-content
   bridge behind present-day `Omega_Lambda`.

So the active cosmology lane is now:

> fixed-gap vacuum scale closed up to cosmological scale identification;
> present-day vacuum fraction reduced to matter-content closure.

## Exact Content

### 1. Fixed-gap vacuum scale

The retained topology route already gives

`lambda_1(S^3_R) = 3/R^2`.

The direct-universal gravity/QG route already closes one canonical textbook
continuum gravitational weak/stationary action family on the chosen smooth
realization of `PL S^3 x R`. On the de Sitter vacuum sector of that same
surface, the curvature radius `R_Lambda` and asymptotic de Sitter Hubble scale
`H_inf` satisfy

`H_inf = c / R_Lambda`,

so the vacuum relation is exactly

`Lambda = 3 / R_Lambda^2 = 3 H_inf^2 / c^2`.

This is the right same-surface scale identification for the cosmological
constant companion.

### 2. `w = -1` is the same mechanism

Once the fixed spectral-gap radius is constant,

`rho_Lambda = Lambda c^2 / (8 pi G)`

is constant as well. Therefore

`d ln rho_Lambda / d ln a = 0`,

and the dark-energy equation of state is

`w = -1`

exactly.

So `w = -1` is no longer a separate cosmology blocker. It is the EOS face of
the same fixed-gap vacuum-scale theorem.

### 3. Present-day `Omega_Lambda` reduces to matter content

Using the present critical density

`rho_crit = 3 H_0^2 / (8 pi G)`,

the vacuum fraction is exactly

`Omega_Lambda = rho_Lambda / rho_crit = Lambda c^2 / (3 H_0^2)`.

Substituting the fixed-gap/de-Sitter relation gives

`Omega_Lambda = H_inf^2 / H_0^2 = (R_H(now) / R_Lambda)^2`,

with `R_H(now) = c/H_0`.

So the `O(1)` difference between `R_Lambda` and `c/H_0` is not a second
cosmological-constant discrepancy. It is just the present-day matter fraction.

Under flatness,

`Omega_Lambda = 1 - Omega_m - Omega_r`.

Therefore the remaining promotion blocker for the cosmology package is the
matter-content bridge, i.e. closure of the `Omega_m` side of the story. On the
current package surface that is exactly the still-open DM relic mapping lane.

## What This Changes

Before this note, the cosmology companion portfolio looked like three loosely
related bounded items:

- `Lambda`
- `w = -1`
- `Omega_Lambda`

After this note, the clean interpretation is:

- `Lambda`: fixed-gap vacuum scale
- `w = -1`: same fixed-gap scale viewed as EOS
- `Omega_Lambda`: present-vs-asymptotic vacuum fraction, hence a matter-bridge
  question

That is a better active lane because it removes fake multiplicity in the
blockers.

## Honest Remaining Gap

What is **not** yet closed on the same surface:

1. a first-principles derivation of the cosmological scale matching that picks
   out the vacuum/de-Sitter scale without using observed `H_0`, and
2. the matter-content bridge that fixes `Omega_m` internally enough to promote
   `Omega_Lambda`.

In practical package terms, the second item is the main remaining gate,
because the current bounded DM/baryon chain already lands close to the needed
matter fraction.

## Canonical Validation

- [frontier_cosmology_scale_identification.py](../scripts/frontier_cosmology_scale_identification.py)
- [frontier_cosmological_constant_spectral_gap.py](../scripts/frontier_cosmological_constant_spectral_gap.py)
- [frontier_dark_energy_eos.py](../scripts/frontier_dark_energy_eos.py)
- [frontier_omega_lambda_derivation.py](../scripts/frontier_omega_lambda_derivation.py)

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authorities
the load-bearing scale-identification step relies on, in response to the
2026-05-05 audit verdict's `missing_bridge_theorem` repair target (audit
row: `cosmology_scale_identification_and_reduction_note`). It does not
promote this note or change the audited claim scope, which remains a
bounded synthesis reducing `Lambda`, `w = -1`, and present-day
`Omega_Lambda` to a fixed-gap de Sitter scale identification plus an
explicitly-open matter-content bridge.

One-hop authorities cited (extended 2026-05-16 to also wire the
matter-content bridge candidate authority that reduces `Omega_m` to the
single ratio `H_inf/H_0`):

- [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
  — current ledger status `unaudited` (audit row:
  `cosmological_constant_spectral_gap_identity_theorem_note`). This is
  the upstream candidate authority for the fixed-gap-to-de-Sitter
  scale matching `Lambda = 3/R_Lambda^2 = 3 H_inf^2 / c^2` used in §1
  of this note. That note carries a two-leg structural identity proof
  (Leg A vacuum-Einstein trace contraction; Leg B Lichnerowicz-Obata)
  meeting at `3/R^2`, and its companion runner reports PASS=22/0.
- [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md) — current
  ledger status `audited_conditional` (audit row: `s3_cap_uniqueness_note`).
  This is the upstream conditional authority for the topology side of the
  retained `lambda_1(S^3_R) = 3/R^2` spectral-gap input cited in §1.
- [`OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`](OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md)
  — current ledger status `unaudited` (audit row:
  `omega_lambda_matter_bridge_theorem_note_2026-04-22`). This is the
  upstream candidate authority for the §3 matter-content bridge: it
  derives the exact structural identity `Omega_Lambda = (H_inf/H_0)^2`
  on the same-surface retained vacuum sector, and under flat FRW
  collapses `Omega_m = 1 - (H_inf/H_0)^2 - Omega_r` to a single open
  ratio `H_inf/H_0`. Its companion runner is
  `scripts/frontier_omega_lambda_matter_bridge.py`. This citation
  reduces the `missing_bridge_theorem` repair target for `Omega_m`
  from "no upstream authority cited" to "one upstream authority cited,
  itself currently `unaudited`, that collapses the bridge to a single
  open ratio". The remaining un-discharged piece is a retained derivation
  of `H_inf/H_0` (or equivalently `R_Lambda H_0 / c`), which is
  explicitly named as the open registration target in §"Honest Remaining
  Gap" item 1.
- [`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md)
  — current ledger status `unaudited` (audit row:
  `cosmological_constant_result_2026-04-12`). This is the upstream
  bounded numerical companion for the cosmological-constant value used
  as the comparator anchor in the runner's `LAMBDA_OBS` and
  `OMEGA_LAMBDA_OBS` inputs. The bounded numerical comparison is
  unaffected by this rigorize pass.
- [`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
  — current ledger status `unaudited` (audit row:
  `dark_energy_eos_retained_corollary_theorem_note`). This is the
  upstream candidate authority for the §2 `w = -1` corollary; it is
  the same-surface EOS face of the fixed-gap vacuum-scale theorem.
- The `H_inf` versus observed `H_0` first-principles matching (§"Honest
  Remaining Gap" item 1) remains the residual `missing_bridge_theorem`
  registration target after the §3 matter-content bridge candidate
  authority above is cited. The cited matter-bridge authority collapses
  `Omega_m` to that single ratio but does not derive the ratio itself.

Because the cited one-hop authorities are themselves either
`audited_conditional` or `unaudited`, this note's effective status is
capped at `audited_conditional` under the standard cite-chain rule,
matching the live audit verdict. The residual single-ratio gap above
is a real open class D (gap) entry and is flagged explicitly so later
audit sweeps can wire it to a retained authority once one exists.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` (since
invalidated by a criticality bump and currently re-queued as
`unaudited`) with two specific complaints:

1. "No cited authority or runner is provided, so the claimed same-surface
   identification cannot be verified as a retained first-principles
   derivation."
2. The matter-content bridge for `Omega_m` is left open without an
   explicit upstream registration.

This rigorize pass (2026-05-16) addresses (1) by adding a `**Primary
runner:**` header line so the audit citation-graph extractor picks up
`scripts/frontier_cosmology_scale_identification.py` as the row's
registered runner artifact (live runner reports PASS=7/0, see "Runner
results" section below), and by explicitly naming five upstream
candidate authorities in the header + cite-chain section. It addresses
(2) by adding
[`OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`](OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md)
as the one-hop matter-bridge candidate authority — this collapses the
matter-content bridge to a single open ratio `H_inf/H_0` on the same-
surface vacuum sector, which is the strongest available upstream
authority on the current package surface.

The substantive observation that the algebraic reduction is internally
consistent — `Lambda = 3/R_Lambda^2`, `rho_Lambda` constant gives
`w = -1`, and `Omega_Lambda = H_inf^2/H_0^2` follows under flatness —
is unchanged by this pass. None of the cited upstream candidate
authorities currently carry a retained-grade ledger status; effective
status remains `audited_conditional` under the cite-chain rule, and the
note's `audit_status` is unchanged. The residual gap (a retained
derivation of `H_inf/H_0`) is unchanged and remains an explicit class D
(gap) entry.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation + runner
registration) plus class D (residual-gap registration). It does not
change any algebraic content, claim type, or load-bearing step
classification. It addresses the two specific complaints in the audit
verdict's `verdict_rationale` field (no runner cited; no matter-bridge
authority cited) by registering an existing live runner and an existing
candidate authority. Mirrors the live cite-chain pattern used by the
`DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md` cluster
(commit `02ad4fadd`) and the runner-registration header pattern used by
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
and
[`OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`](OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md).

## Runner results

`scripts/frontier_cosmology_scale_identification.py` (the registered
primary runner) verifies seven algebraic checks on the post-closure
GR/QG surface, using the observed `H_0 = 67.4 km/s/Mpc`, `Lambda_obs =
1.1056 x 10^-52 m^-2`, `Omega_Lambda_obs = 0.685`, and the current
derived `Omega_b = 0.0492`, `Omega_DM/Omega_b = 5.3753`, `Omega_r =
9.15 x 10^-5` as inputs:

1. **de Sitter scale identification** — `Lambda = 3 H_inf^2 / c^2 = 3 /
   R_Lambda^2` exactly (algebraic identity in `R_Lambda`).
2. **`w = -1` from fixed gap** — fixed `R_Lambda` means
   `d ln rho_Lambda / d ln a = 0` and hence `w = -1` exactly.
3. **present `Omega_Lambda` from scale ratio** — three equivalent forms
   `Lambda c^2 / (3 H_0^2)`, `(H_inf/H_0)^2`, `(R_H(now)/R_Lambda)^2`,
   and `rho_Lambda / rho_crit` all agree to machine precision.
4. **observed `Omega_Lambda` consistency** — the algebraic form lands
   within 2% of the Planck 2018 `Omega_Lambda = 0.685` anchor when
   evaluated at the observed inputs.
5. **matter-bridge reduction** — the flat-FRW identity
   `Omega_m = 1 - Omega_Lambda - Omega_r` holds exactly.
6. **current derived `Omega_m` feeds `Omega_Lambda`** — the current
   bounded DM/baryon chain derives `Omega_m = 0.3137` and hence
   `Omega_Lambda = 0.6862`, within `5 x 10^-3` of the Planck anchor.
7. **no separate `w` blocker remains** — `w = -1` and `Lambda` live on
   the same fixed-gap/de-Sitter scale surface; they are not independent
   blockers.

Result: `SUMMARY: PASS=7 FAIL=0`. The runner verifies the algebraic
identities the note relies on; it does not (and is not intended to)
derive the same-surface scale matching or the matter-content bridge
from first principles. Those remain the cite-chain dependencies above.
