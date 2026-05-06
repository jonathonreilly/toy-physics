# DM Leptogenesis `N_e` Projected-Source-Law Derivation

**Date:** 2026-04-16  
**Branch:** `codex/dm-main-refresh`  
**Script:** `scripts/frontier_dm_leptogenesis_ne_projected_source_law_derivation.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Status

Exact positive derivation transplant from the PMNS microscopic source-response
lane onto the refreshed DM branch.

This note upgrades the flavored-PMNS DM reduction.

The earlier DM reduction said the remaining PMNS-side object was the active
five-real source. That was true if one only used:

- branch/orientation,
- seed averages,
- support pattern,
- and the exact transport selector.

But the PMNS microscopic source-response theorem is stronger than that.

## Question

On the charged-lepton-active branch `N_e`, what is the smallest PMNS-side
object actually needed to derive the transport-relevant flavored DM column?

Do we still need the full active five-real source

`(xi_1, xi_2, eta_1, eta_2, delta)`?

Or is there a smaller exact source-response object that already determines the
relevant column?

## Bottom line

There is a smaller exact object.

On `N_e`, the selected transport column is derivable from the charged-lepton
projected Hermitian source law alone:

`dW_e^H`.

The logic is exact:

1. `dW_e^H` reconstructs the active charged-lepton Hermitian block `H_e`
2. on `N_e`, the PMNS packet is exactly `|U_e|^2^T`
3. the exact DM transport selector `F_K` acts on the three packet columns
4. therefore the selected flavored transport column is algorithmic once
   `dW_e^H` is known

So for the PMNS-assisted DM repair route, we do **not** need the raw active
five-real source as the final target.

We need the projected Hermitian charged-lepton source law.

## Exact reduction

### 1. Projected Hermitian source pack determines `H_e`

For a `3 x 3` Hermitian block, the nine real linear responses

`X -> Re Tr(X H_e)`

on the standard Hermitian basis determine `H_e` exactly.

So the charged-lepton projected Hermitian source law `dW_e^H` fixes `H_e`
exactly.

### 2. `H_e` determines the `N_e` packet

On the one-sided charged-lepton-active branch, the passive side is monomial and
contributes only ordering/permutation data already fixed elsewhere.

Therefore the active packet is exactly

`|U_PMNS|^2 = |U_e|^2^T`.

So `H_e` alone determines the `N_e` packet.

### 3. The exact transport selector determines the column

The DM branch already has the exact one-source flavored selector

`F_K(P) = Σ_alpha Psi_K(P_alpha)`.

Applying this to the three columns of the `N_e` packet selects the relevant
column exactly.

On the canonical `N_e` sample, this reproduces the same near-closing value:

`eta/eta_obs = 0.989512597197`.

## Consequence

This changes the honest last-mile PMNS/DM target.

What is no longer the right final target:

- the raw active five-real source law

What is now the right final target:

- the charged-lepton projected Hermitian source law `dW_e^H`

because once `dW_e^H` is known:

- `H_e` is known
- the `N_e` packet is known
- the transport-relevant column is known

So the remaining PMNS contribution to the DM flavored-repair route is smaller
and more source-response-native than the earlier five-real formulation.

## What this closes

This closes the target-shape question on the PMNS-assisted DM lane more tightly
than the previous active-projector reduction.

The flavored `N_e` repair path no longer needs a theorem for the raw PMNS
corner-source coordinates as such. It needs the projected charged-lepton
Hermitian source law.

## What this does not close

This note does **not** yet evaluate `dW_e^H` from `Cl(3)` on `Z^3`.

It proves only that once `dW_e^H` is available, the selected `N_e` transport
column and the near-closing DM flavored value are both downstream algorithmic.

So the live remaining gap is now:

- derive `dW_e^H` on `E_e` from `Cl(3)` on `Z^3`

not:

- derive the full active five-real PMNS source law.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_ne_projected_source_law_derivation.py
```

## Citations

The auditor's `missing_dependency_edge` flag asked for retained-grade
cited authorities (or an independent derivation) for `dW_e^H` from
`Cl(3)` on `Z^3`, plus the `H_e -> N_e packet` bridge and the exact
transport selector. The runner imports the load-bearing ingredients
from named theorem-side modules, each backed by a dedicated
repo-native theorem note. The corresponding markdown links are
registered as one-hop dependency edges below so the audit-graph chain
becomes traceable.

Runner-side carriers (named so the audit lane sees both halves of the
chain):

- `scripts/dm_leptogenesis_exact_common.py` — supplies `exact_package`
  and the source-side normalisation used by the runner.
- `scripts/frontier_dm_leptogenesis_flavor_column_functional_theorem.py`
  — supplies the transport-relevant flavored column functional and the
  `F_K` action on packet columns.
- `scripts/frontier_dm_leptogenesis_pmns_projector_interface.py`
  — supplies the PMNS-projector interface used by §2 to convert
  `H_e` into the `N_e` packet `|U_PMNS|^2 = |U_e|^2^T`.

Theorem-side authorities (load-bearing one-hop deps):

- [DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md](DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md)
  — supplies the source-side `exact_package` with `gamma`, `E1`, `E2`,
  used as the source-oriented input to the projected-source law.
- [DM_LEPTOGENESIS_FLAVOR_COLUMN_FUNCTIONAL_THEOREM_NOTE_2026-04-16.md](DM_LEPTOGENESIS_FLAVOR_COLUMN_FUNCTIONAL_THEOREM_NOTE_2026-04-16.md)
  — supplies the exact transport selector `F_K` referenced in §"Bottom
  line" item 3 and §"Exact reduction" §3.
- [DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md](DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md)
  — supplies the PMNS-projector interface used to bridge from `H_e`
  to the `N_e` packet (§"Exact reduction" §2).
- [DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md)
  — charged-source response reduction, supplying the
  `dW_e^H -> H_e` reconstruction step in §"Exact reduction" §1.
- [DM_LEPTOGENESIS_NE_ACTIVE_COLUMN_AXIOM_BOUNDARY_NOTE_2026-04-16.md](DM_LEPTOGENESIS_NE_ACTIVE_COLUMN_AXIOM_BOUNDARY_NOTE_2026-04-16.md)
  — axiom-side boundary on the `N_e` active-column problem this note
  reduces.
- [DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md](DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md)
  — sign orientation companion for the projected-source triplet,
  paired with the projected-source law derived here.

These additions are strictly additive: the verdict, the bottom-line
transplant statement, the exact-reduction §§1–4, the consequence
section, and the explicitly recorded "what this does not close" gap
(deriving `dW_e^H` on `E_e` from `Cl(3)` on `Z^3`) are all unchanged.
This PR registers the dependency edges; it does not derive
`dW_e^H` itself.

Until each linked authority is itself audit-clean, this note remains
`audited_conditional` even with the registered edges; the wiring is
the prerequisite for unlock, not the unlock itself.
