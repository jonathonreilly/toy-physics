# DM Leptogenesis `N_e` Charged Source-Response Reduction

**Date:** 2026-04-16  
**Branch:** `codex/dm-main-refresh`  
**Script:** `scripts/frontier_dm_leptogenesis_ne_charged_source_response_reduction.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Status

**support** — structural Schur-pushforward identities plus a consistency
check at a stipulated canonical `N_e` benchmark sample.

This note records two parts:

1. (structural, retained-grade)  Algebraic identities showing that, *given*
   a charged-lepton projected Hermitian source law `dW_e^H`, the
   PMNS-assisted flavored DM chain is algorithmic from there on.
2. (consistency check at a stipulated sample)  At the same canonical off-seed
   `N_e` sample used by the sibling
   [DM Leptogenesis PMNS Microscopic D Last-Mile](DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md),
   the chain reproduces the documented residual factor of `1.0106x` against
   the observed `eta`.

This note does **not** evaluate `dW_e^H` from the sole axiom. It does not
prove the residual factor `1.0106x` as a derived number. Both `dW_e^H` and
the canonical `(x, y, delta)` triple are stipulated inputs, as in the sibling
last-mile note.

The bounded scope is recorded explicitly in
[DM Leptogenesis N_e Active-Column Axiom Boundary](DM_LEPTOGENESIS_NE_ACTIVE_COLUMN_AXIOM_BOUNDARY_NOTE_2026-04-16.md),
which shows the selected `N_e` transport column is **not** fixed by the
currently native PMNS data on its own.

## Question

After the PMNS projector-interface, active-block localization, exact flavored
column selector, and `N_e` projected-source-law derivation, what is the
smallest remaining PMNS-side object on the DM branch?

And, at the stipulated canonical `N_e` sample, what residual miss survives
once `dW_e^H` is supplied?

## Bottom line

The PMNS-assisted flavored DM route reduces to one object:

- the charged-lepton projected Hermitian source law `dW_e^H`.

The structural content (Parts 1 and 2 below) is:

1. `dW_e^H` is the exact charged-sector Schur pushforward of the microscopic
   charge-`-1` source-response law
2. `dW_e^H` reconstructs `H_e` exactly
3. on `N_e`, `H_e` determines the transport packet `|U_e|^2^T`
4. the exact DM transport selector then picks the relevant column algorithmically

These four steps are algebraically exact at retained grade and are the load-
bearing reduction content of this note.

The numerical comparison to the old one-flavor `5.3x` miss is a
**consistency check at a stipulated input**, not a derivation. At the
canonical off-seed `(x, y, delta) = ((0.24, 0.38, 1.07), (0.09, 0.22, 0.61),
1.10)` sample (the same one used by the LAST_MILE sibling note), the chain
reproduces

- `eta/eta_obs = 0.989512704600`
- residual miss factor `eta_obs/eta = 1.010598444417`

which is the same `~1.05%`-low value already documented in the LAST_MILE
sibling. Changing the canonical `(x, y, delta)` input would in general give
a different residual; the value is tied to the chosen benchmark, not derived.

## Structural reduction (algebraic, retained-grade)

The following four steps are algebraically exact identities. They do **not**
evaluate any of `D_-`, `dW_e^H`, or `H_e` from the sole axiom; they record
the algorithmic chain assuming `dW_e^H` (equivalently `H_e`) is supplied.

### 1. `dW_e^H` is an exact charged-sector Schur pushforward

On the charge-preserving microscopic class,

`D = D_0 ⊕ D_- ⊕ D_+`.

A source supported on the charged-lepton support `E_e ⊂ E_-` factors exactly
through the charge-`-1` Schur complement

`L_e = Schur_{E_e}(D_-)`.

So `dW_e^H` is not an ad hoc PMNS data object. It is the charged-sector
microscopic source-response law on the retained support.

### 2. `dW_e^H` reconstructs `H_e`

The nine Hermitian linear responses on the charged support reconstruct `H_e`
exactly.

### 3. `H_e` determines the `N_e` packet

On the charged-lepton-active branch,

`|U_PMNS|^2 = |U_e|^2^T`.

So once `H_e` is known, the full `N_e` transport packet is already fixed.

### 4. Exact transport selects the column

The exact one-source flavored selector

`F_K(P) = Σ_alpha Psi_K(P_alpha)`

then acts algorithmically on the packet from step 3. At the stipulated
canonical `(x, y, delta)` benchmark of step 3, it selects the middle column
and yields the consistency value

- `eta/eta_obs = 0.989512704600`

matching the LAST_MILE sibling's `ETA_NE_CANONICAL`. The selected column
itself is **not** fixed by sole-axiom data (see
[Active-Column Axiom Boundary](DM_LEPTOGENESIS_NE_ACTIVE_COLUMN_AXIOM_BOUNDARY_NOTE_2026-04-16.md)).

## Comparison to the old `5.3x` miss (at stipulated canonical sample)

The exact theorem-native one-flavor branch gave (also as a documented
sibling-cluster authority value):

- `eta/eta_obs = 0.188785929502`
- miss factor `eta_obs/eta = 5.297004933778`

At the stipulated canonical off-seed sample
`(x, y, delta) = ((0.24, 0.38, 1.07), (0.09, 0.22, 0.61), 1.10)` (matching
the LAST_MILE sibling), the PMNS-assisted `dW_e^H`-conditioned route gives:

- `eta/eta_obs = 0.989512704600`
- miss factor `eta_obs/eta = 1.010598444417`

This is the same value as the LAST_MILE sibling's canonical-off-seed
benchmark `ETA_NE_CANONICAL = 0.9895125971972334` (agreement is consistency
between two routines acting on the same stipulated input; it is not
derivation of either number).

The improvement factor at this sample is

- `5.241453678302`,

and the residual miss is only about

- `1.05%`.

These numbers are tied to the stipulated benchmark `(x, y, delta)`. They are
**not** derived from `Cl(3)` on `Z^3`; the sibling
[Active-Column Axiom Boundary](DM_LEPTOGENESIS_NE_ACTIVE_COLUMN_AXIOM_BOUNDARY_NOTE_2026-04-16.md)
shows the selected `N_e` column varies with the active five-real source data
and is not fixed by the currently native PMNS laws.

## Consequence

What this note clarifies about the PMNS-assisted DM repair route:

- the structural reduction `dW_e^H -> H_e -> packet -> selected column ->
  eta` is exact (Parts 1 and 2)
- the remaining unevaluated object is `dW_e^H` itself (equivalently `D_-`
  and its Schur pushforward)

What this note does **not** establish:

- the residual miss `1.01x` as a derived prediction
- the selected `N_e` column from sole-axiom data alone (see
  [Active-Column Axiom Boundary](DM_LEPTOGENESIS_NE_ACTIVE_COLUMN_AXIOM_BOUNDARY_NOTE_2026-04-16.md))
- the raw active five-real PMNS source from sole-axiom data alone

The remaining frontier object is therefore unchanged: evaluate the
charged-lepton projected Hermitian source law `dW_e^H` from `Cl(3)` on
`Z^3`, equivalently evaluate `D_-` and its Schur pushforward. Once that is
done, the remaining PMNS-assisted DM chain (Parts 1 and 2 above) is
algorithmic at the resulting value.

## What this does not close

This note does **not** evaluate `D_-` or `dW_e^H` from the sole axiom. The
canonical `(x, y, delta)` triple used in Part 3 is a stipulated benchmark
matching the LAST_MILE sibling, not a sole-axiom derivation. The
`build_charge_preserving_operator_with_target_le(...)` step in the runner
back-solves an operator `D_-` whose Schur pushforward realises a chosen
target `H_e`; this is a *construction-by-target*, not a derivation of `D_-`
from `Cl(3)` on `Z^3`. The structural claims (Parts 1 and 2) are the
load-bearing content; the `1.01x` value (Part 3) is a stipulated-sample
consistency check.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_ne_charged_source_response_reduction.py
```
