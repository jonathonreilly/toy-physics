# Source-Higgs Gram-Purity Postprocessor

**Status:** open / `O_sp`-Higgs postprocessor awaiting production certificate
**Runner:** `scripts/frontier_yt_source_higgs_gram_purity_postprocessor.py`
**Certificate:** `outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json`

## Purpose

This is the executable postprocessor for the selected PR #230 source-overlap
route.  It now uses the Legendre/LSZ source-pole operator from
`outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json` as the
normalized source side:

```text
O_sp = sqrt(dGamma_ss/dx | pole) O_s,        Res(C_sp,sp) = 1.
```

When a future production certificate supplies same-surface pole residues for
`C_ss`, `C_sH`, and `C_HH`, the runner computes both the raw source-Higgs Gram
rows and the `O_sp`-Higgs rows:

```text
Delta = Res(C_ss) Res(C_HH) - Res(C_sH)^2
rho_sH = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH))

Res(C_sp,H) = Res(C_sH) / sqrt(Res(C_ss))
Delta_spH = Res(C_HH) - Res(C_sp,H)^2
rho_spH = Res(C_sp,H) / sqrt(Res(C_HH))
```

and checks whether `Delta_spH = 0` and `|rho_spH| = 1` within the declared
tolerance or supplied residue uncertainties.  This is the explicit test for
`O_sp = +/- O_H` at the isolated pole; it removes source-coordinate
normalization from the source side but does not assume the identity.

## Required Input

The future candidate certificate must supply:

- production phase metadata;
- same-ensemble and same-source-coordinate flags;
- the Legendre/LSZ `O_sp` source-side normalization certificate;
- a certified same-surface canonical-Higgs operator identity;
- `Res_C_ss`, `Res_C_sH`, and `Res_C_HH`;
- no `H_unit` by fiat;
- no observed-target selectors;
- retained-route authorization before any proposed-retained wording.

## Current Result

No candidate `O_H/C_sH/C_HH` production certificate is present, so the runner
records the route as open.  This is expected and is not a failure of the route;
it is the claim firewall before the missing canonical-Higgs pole rows exist.

## Claim Boundary

This postprocessor does not claim retained or `proposed_retained` `y_t`
closure.  It does not define `O_H` by fiat, does not treat `H_unit` as `O_H`,
does not set `kappa_s = 1` or `cos(theta) = 1`, and does not use
`yt_ward_identity`, observed targets, `alpha_LM`, plaquette, or `u0`.  It also
does not identify `O_sp` with `O_H` unless the `O_sp`-Higgs Gram-purity gate
passes.
