# DM Leptogenesis Full Microscopic Reduction

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Branch:** `codex/dm-main-refresh`  
**Script:** `scripts/frontier_dm_leptogenesis_full_microscopic_reduction.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Status

Conditional reduction theorem for the PMNS-assisted flavored DM route on
the refreshed branch. The "if-D-is-supplied-then" chain is exact; the
supply of `D` itself is not closed from `Cl(3)` on `Z^3` in this note or
its runner.

## Question

After the PMNS projector-interface theorem, active-block reduction, exact
flavored selector, `N_e` projected-source-law derivation, and charged
source-response reduction, what is the smallest remaining science object on the
PMNS-assisted DM repair route?

## Bottom line

It is the actual microscopic charge-preserving operator `D`.

The exact **conditional** chain is:

`D` (supplied; not derived in this note or runner)
`-> D_-`
`-> dW_e^H`
`-> H_e`
`-> |U_e|^2^T`
`->` selected transport column
`-> eta`

So once a full microscopic charge-preserving operator `D` with the
required Schur structure is **supplied**, the PMNS-assisted near-closing
DM value follows algorithmically. The runner verifies the algorithmic
chain by engineering a particular `D` (the active block is constructed
as `am = target_le + bm fm^{-1} bm^H` so the Schur identity reproduces
the canonical target). It does not derive `D` from `Cl(3)` on `Z^3`.

The remaining target is the actual microscopic value law of `D` from
`Cl(3)` on `Z^3` — the same target the 2026-05-05 audit recorded as the
missing step, and the same target the
[`DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md)
catalogues across the sibling charged-source-response row.

## Exact result (conditional on a supplied charge-preserving D)

On the canonical charged-lepton-active sample used by the PMNS-assisted DM
lane, **assuming** a charge-preserving `D` is supplied whose
`charge -1`-block Schur complement `Schur_{E_e}(D_-)` equals the canonical
target `H_e = canonical_h(0.24, 0.38, 1.07; 0.09, 0.22, 0.61; 1.10)`, the
runner verifies the following algebraic identities:

- from full `D`, the charge-`-1` sector `D_-` is extracted canonically
- `dW_e^H` factors exactly through the Schur value `L_e = Schur_{E_e}(D_-)`
- `L_e` equals the canonical charged-lepton Hermitian block `H_e` **by
  construction** of `build_full_charge_preserving_operator(target_le)`
  (the active block `am` is built as `target_le + bm fm^{-1} bm^H` so the
  Schur identity recovers `target_le`)
- `H_e` gives the `N_e` packet via the standard left-diagonalizer
- the exact DM flavored selector picks the middle near-closing column

So the PMNS-assisted route is no longer blocked on:

- projector construction
- column selection
- PMNS pair reconstruction
- charged Hermitian source response reduction

It is blocked only on:

- the actual full microscopic operator values of `D` from `Cl(3)` on `Z^3`

The runner does **not** derive that supply of `D`; it engineers a
particular `D` such that the Schur structural identity reduces to the
canonical target `H_e`. The downstream chain is then deterministic
arithmetic of that target.

## Numerical comparison to the old `5.3x` miss (engineered-target arithmetic)

The miss-factor comparison below is the deterministic image of the
engineered canonical target `target_le` through the imported transport
package. It is not a derivation of either numerator or denominator from
`Cl(3)` on `Z^3`; both are arithmetic of the engineered Schur target plus
the upstream-imported one-flavor literature value `0.188785929502`.

Exact theorem-native one-flavor branch (imported):

- `eta/eta_obs = 0.188785929502`
- miss factor `eta_obs/eta = 5.297004933778`

Full-`D` PMNS-assisted route (engineered target):

- `eta/eta_obs = 0.989512704600`
- miss factor `eta_obs/eta = 1.010598444417`

So **if** the canonical engineered target `H_e` is the right one (which is
exactly the open derivation), the PMNS-assisted full-microscopic route
would reduce the old miss by a factor of about

- `5.241453678303`

and leave only a residual

- `1.04872954%`

low. The headline `1.0106x` residual is therefore a conditional-on-target
statement, not an independent percent-level closure of the DM repair
route from the sole axiom.

## Consequence

The PMNS-assisted DM route is now reduced as far as it can honestly go without
deriving the full microscopic operator values themselves.

The remaining exact target is:

- the actual microscopic value law of the full charge-preserving operator `D`
  from `Cl(3)` on `Z^3`

not:

- a new transport law
- a new PMNS carrier
- a new flavored column theorem
- a new charged-Hermitian reduction

## Honest auditor read (added 2026-05-16, science-fix-loop iter30)

The 2026-05-05 cross-family audit verdict on this note recorded:

- `audit_status`: `audited_numerical_match` (`terminal_audit`)
- `load_bearing_step_class`: `G`
- `chain closes`: **False** — "The runner constructs `D` from the target
  `H_e` so that the Schur complement reproduces `H_e` by design. The
  missing step is an independent derivation of the microscopic value
  law of `D` from `Cl(3)` on `Z^3`."

That verdict stands. The runner's `build_full_charge_preserving_operator(
target_le)` writes the active block as `am = target_le + bm fm^{-1}
bm^H`, so `Schur(D_-) = target_le` by construction; the downstream
chain is then deterministic arithmetic of the engineered target. The
DM transport status terminal-synthesis meta note
([`DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md))
catalogues this row's sibling
[`DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md)
under the same auditor's repair note: "Re-check whether a later runner
derives `canonical_h` / `D_-` directly from `Cl(3)` on `Z^3` instead of
constructing a block with the desired Schur complement." The same
repair note applies here.

The companion last-mile note
[`DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md)
reduces the open object further to the off-seed `5`-real corner-breaking
source `(xi_1, xi_2, eta_1, eta_2, delta)`, but does not derive those
five real values from the framework axiom either.

The honest classification of this note is therefore:

- **conditional bounded theorem.** Given a charge-preserving `D` with
  `Schur_{E_e}(D_-) = canonical_h(...)` on the canonical sample, the
  algebraic chain to the near-closing PMNS-assisted eta is deterministic
  and the runner verifies each step.
- the existence and microscopic value law of such a `D` from `Cl(3)` on
  `Z^3` is the open theorem; this note does not close it.
- the runner's `1.0106x` residual is a conditional-on-engineered-target
  statement; it is not a percent-level closure of the DM repair route
  from the sole axiom.
- the audit lane's `audited_numerical_match` verdict stands.

### Runner check-class breakdown (post-iter30 honest scoping)

The runner's ten passing checks are now self-classified as:

| Class | Count | Meaning |
|---|---|---|
| C standalone-from-Cl(3) on Z^3 | 0 | derived from the sole axiom with no imported or engineered load-bearing object |
| D conditional-on-supplied-D | 7 | algebraic identities that hold for any `D` with the assumed block structure, or arithmetic of supplied values |
| E engineered-target | 3 | identities that hold because `D` is built to satisfy them (charge-commutator on the engineered block-diagonal `D`, the `L_e = H_e` equality, and the selector eta value that flows deterministically from the engineered target through the imported transport kernel) |

The runner's numerical outputs are unchanged. This is a graph-bookkeeping
addendum: it acknowledges the engineered-target classification of the
load-bearing equality recorded by the 2026-05-05 audit and aligns the
runner's per-check labels with what the audit lane already recorded. It
does not promote the note, does not modify the runner numerics, and does
not introduce any new vocabulary. The audit lane still owns the verdict.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_full_microscopic_reduction.py
```
