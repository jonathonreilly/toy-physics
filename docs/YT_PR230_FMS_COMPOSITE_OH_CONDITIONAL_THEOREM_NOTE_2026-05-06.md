# PR230 FMS Composite `O_H` Conditional Theorem

**Date:** 2026-05-06
**Status:** conditional-support / FMS composite `O_H` theorem; current PR230
surface lacks same-surface EW/Higgs action and source-overlap pole rows
**Claim type:** route_support
**Runner:** `scripts/frontier_yt_pr230_fms_composite_oh_conditional_theorem.py`
**Certificate:** `outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json`

```yaml
actual_current_surface_status: conditional-support / FMS composite O_H theorem; current PR230 surface lacks same-surface EW/Higgs action and source-overlap pole rows
conditional_surface_status: exact-support if a future PR230 same-surface EW/Higgs action supplies a dynamic Higgs doublet Phi, nonzero radial background v, canonical Higgs LSZ normalization, and C_ss/C_sH/C_HH pole rows
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
```

## Theorem

If a same-surface PR230 EW/Higgs action supplies a dynamic Higgs doublet
`Phi`, a nonzero radial background `v`, and a canonical radial field `h`, then
the gauge-invariant composite

```text
O_H = Phi^dagger Phi - <Phi^dagger Phi>
```

has the local FMS expansion

```text
Phi^dagger Phi = ((v+h)^2 + pi^a pi^a)/2
O_H = v h + h^2/2 + pi^a pi^a/2 .
```

Thus `O_H` has a one-Higgs pole overlap proportional to `v`.  At an isolated
Higgs pole,

```text
Res C_HH = v^2 Z_h .
```

This is the correct action-first composite-operator bridge.  It is not a
current PR230 closure proof because the PR230 surface does not yet provide the
same-surface EW/Higgs action, the canonical `O_H` certificate, or the
`C_ss/C_sH/C_HH` pole rows that would tie the PR230 source to this composite.

## What This Retires

The result replaces the loose slogan "use FMS" with an explicit theorem
contract.  The useful part is the linear term `v h`: if the future action
derives `v != 0` and the canonical radial field, then the degree-one radial
premise needed by the taste-radial selector is physically supplied by the
action, not by a label or symmetry shortcut.

## What Remains

The current branch still lacks all load-bearing artifacts needed to use the
theorem for `y_t`:

- same-surface EW/Higgs action with dynamic `Phi` on `Cl(3)/Z^3`;
- nonzero radial background and canonical Higgs LSZ normalization;
- canonical/gauge-invariant composite `O_H` certificate;
- same-ensemble `C_ss/C_sH/C_HH` pole rows, or an equivalent source-overlap
  theorem;
- finite-volume, IR, isolated-pole, and Gram-purity checks.

The normalization is not set to one.  The composite pole residue is
`v^2 Z_h`, and the source overlap still depends on `Res C_sH`.  A source with
the same `C_ss` and the same `C_HH` can have a different `C_sH`, so the source
overlap cannot be inferred from the composite definition alone.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not use FMS literature as proof authority, does not identify the
current taste-radial source with canonical `O_H`, does not treat finite
`C_sx/C_xx` rows as canonical-Higgs pole rows, does not set `kappa_s`, `c2`, or
`Z_match` to one, and does not use `H_unit`, `yt_ward_identity`, observed
targets, `alpha_LM`, plaquette, or `u0`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_fms_composite_oh_conditional_theorem.py
# SUMMARY: PASS=15 FAIL=0
```
