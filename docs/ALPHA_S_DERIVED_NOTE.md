# `alpha_s(M_Z)` Same-Surface-Derived Authority (bounded)

**Date:** 2026-04-15 (status amended 2026-05-01)
**Status:** bounded - same-surface quantitative lane on `main`. The
            framework-side carrier is `alpha_s(v)` from the canonical
            plaquette/`u_0` chain; the `M_Z` readout is then the standard
            QCD running bridge applied to that boundary. Author tier
            amended 2026-05-01 from `proposed_retained` to `bounded` to
            match the explicit bounded scope of
            [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
            and the explicit bounded scope of the registered low-energy
            running bridge in
            [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md).
**Primary runner:** `scripts/frontier_yt_zero_import_chain.py` ([scripts/frontier_yt_zero_import_chain.py](../scripts/frontier_yt_zero_import_chain.py))
**Bridge runner:** `scripts/frontier_qcd_low_energy_running_bridge.py`
**Current package carrier:** `scripts/frontier_complete_prediction_chain.py`
**Historical support runner:** `scripts/frontier_alpha_s_determination.py`

**Audit replacement gate (plain-text pointer, not a one-hop authority for this
bounded lane):** `ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md`
with runner `scripts/frontier_alpha_s_direct_wilson_loop.py`.

## Status amendment 2026-05-01 (audit-driven scope sharpening)

The 2026-04-29 Codex audit pass returned `audited_conditional` with the
rationale:

> the restricted inputs do not include the retained low-energy running
> bridge needed to turn alpha_s(v) into alpha_s(M_Z), and the plaquette
> dependency itself says the exact analytic beta=6 insertion is not
> closed... Repair target: cite and audit the running-bridge
> theorem/threshold map and close or explicitly scope the plaquette
> beta=6 insertion status.

This note responds to both repair targets:

1. **Running bridge.** A one-hop running-bridge authority is now
   registered as
   [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md),
   with its own runner `scripts/frontier_qcd_low_energy_running_bridge.py`.
   The bridge note carries `bounded` author tier and explicitly scopes
   the v -> M_Z transfer as standard SM 2-loop RGE plus quark-mass
   threshold matching, not as a framework-native derivation.
2. **Plaquette `beta = 6` scope.** The upstream
   [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
   has been amended on 2026-05-01 to carry `bounded` author tier
   explicitly, with an explicit window for the residual analytic
   insertion gap.

The honest author tier for this note is therefore `bounded`, not
`proposed_retained`. The numerical lane `alpha_s(M_Z) = 0.1181` remains
in place as the bounded same-surface readout under the documented
one-hop bridge.

## Authority Role

This note records the standalone strong-coupling lane used on the current
`main` package surface, scoped explicitly as `bounded` (see status
amendment above).

The current package treats `alpha_s(M_Z)` as its own bounded quantitative
lane, not merely as a hidden subcomponent of a larger synthesis memo.
The bridge from the framework-side `alpha_s(v)` to the `M_Z` readout is
the registered standard-infrastructure running bridge; see
[`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md).

## Audit-Clean Replacement Route

As of the 2026-05-01 amendment this note carries `bounded` author tier
rather than `proposed_retained`. That records the honest scope: the
chain works on the canonical same-surface plaquette plus the registered
standard-infrastructure running bridge, but it does not produce an
audit-clean framework-native closed derivation of `alpha_s(M_Z)`.

The audit-clean replacement target is the direct Wilson-loop route in
`ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md`.
That route is a future replacement gate, not a load-bearing authority for this
bounded same-surface lane. It measures `alpha_s` from Wilson-loop expectation values, the
static potential, Sommer-scale setting, and the standard QCD running
bridge. It explicitly forbids using the `alpha_LM/u_0` or
`alpha_bare/u_0^2` chain as authority.

Until that direct Wilson-loop gate passes with production data and the
audit ledger ratifies it, the chain below is the bounded same-surface
quantitative lane, and the `alpha_LM/u_0` calculation should be used only
as a consistency cross-check for the direct route.

## Safe Statement

The current bounded lane gives:

- `alpha_s(v) = alpha_bare / u_0^2 = 0.1033` (boundary value on the
  same-surface plaquette/`u_0` chain)
- `alpha_LM^2 = alpha_bare * alpha_s(v)` as an exact algebraic
  coupling-chain identity (decoration of upstream coupling definitions)
- one-decade low-energy transfer from `v` to `M_Z` on the registered
  bounded-scope running bridge
  ([`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md))
- `alpha_s(M_Z) = 0.1181`

That is the current bounded same-surface-derived `alpha_s` result on
`main`. The bounded scope is documented explicitly: the upstream
plaquette analytic insertion at `beta = 6` is open work, and the bridge
from `v` to `M_Z` is standard SM 2-loop RGE infrastructure
(Machacek-Vaughn 1984; Arason et al. 1992) plus PDG quark-mass
thresholds, not a framework-native derivation.

## Canonical Chain

```
Cl(3) on Z^3
  |-> g_bare = 1
  |-> <P> = 0.5934  (same-surface MC-evaluated; bounded analytic scope -
  |                  see PLAQUETTE_SELF_CONSISTENCY_NOTE.md status amendment)
  |-> u_0 = <P>^(1/4)
  |
  |-> hierarchy theorem:
  |     alpha_LM = alpha_bare / u_0
  |     v = 246.282818290129 GeV
  |
  |-> vertex-power theorem:
        alpha_s(v) = alpha_bare / u_0^2 = 0.1033
        alpha_LM^2 = alpha_bare * alpha_s(v)
  |
  |-> low-energy transfer (bounded; standard QCD infrastructure):
        see QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md
        alpha_s(M_Z) = 0.1181
```

## Package Role

This is a bounded standalone quantitative lane, not a theorem-core row.
Its quantitative anchor is the canonical same-surface plaquette evaluation in
[PLAQUETTE_SELF_CONSISTENCY_NOTE.md](PLAQUETTE_SELF_CONSISTENCY_NOTE.md).
Its bridge to `M_Z` is the registered standard-infrastructure running bridge
in [QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md).

The framework-side quantity is `alpha_s(v)`. The quoted `alpha_s(M_Z)` row is
the same lane after the bounded one-decade running bridge below `v`.

It remains distinct from:

- the retained hierarchy / `v` lane
- the EW normalization lane
- the Yukawa / top lane
- the Higgs / vacuum lane

## Validation Snapshot

- current zero-input route:
  `alpha_s(M_Z) = 0.1181`
- comparison value:
  `0.1179`
- deviation:
  `+0.2%`

Primary reruns on the current package surface:

- `frontier_yt_zero_import_chain.py`
- `frontier_complete_prediction_chain.py`

Historical support, not canonical authority:

- `frontier_alpha_s_determination.py`

## Bridge-support progress 2026-05-09 (upstream plaquette insertion)

The 2026-05-05 audit pass on this row continues to read `audited_conditional`
because the upstream plaquette dependency
([`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md))
explicitly leaves the analytic `beta = 6` insertion open and the running
bridge ([`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md))
imports standard SM RGE plus PDG threshold infrastructure. Both upstream
authorities sit at `audited_conditional` on the current ledger, and this
row inherits that conditional verdict.

A first concrete piece of the upstream plaquette repair target landed
audited_clean on 2026-05-09 in
[`GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md`](GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md),
which delivers a bounded finite-box computation of the normalized
single-link SU(3) Wilson boundary character coefficients
`rho_(p,q)(6)` for `0 <= p,q <= 4` by two independent methods (a
Schur-Weyl Bessel-determinant sum and direct Weyl integration with
Vandermonde squared), with cross-method agreement to `4.136e-15`
absolute / `7.952e-14` relative error.

That audited_clean coefficient-table delivery does not by itself
close either the upstream analytic `beta = 6` insertion gap or the
load-bearing `B`-class value-transfer step of this row. The honest
read remains:

- the row is correctly carried as `bounded` (matching the load-bearing
  step class `B` that the audit recorded);
- the upstream plaquette path now has a first audited_clean component
  on its repair target, but the parent plaquette row continues to
  carry `audited_conditional` because the all-weight closure and the
  spatial Wilson tensor-transfer / Perron problem remain open;
- the running-bridge dependency continues to import standard SM RGE
  plus PDG threshold infrastructure as documented in
  [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md);
- effective-status propagation continues to cap this row at
  `audited_conditional` until both upstream authorities reach
  independent retained-grade audit.

This subsection is informational reuse-discipline only; it does not
promote the audit verdict and does not amend the load-bearing step.
