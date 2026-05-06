# PR230 Genuine Source-Pole Artifact Intake

**Status:** exact-support / genuine same-source `O_sp` artifact intaken; canonical `O_H` bridge open
**Runner:** `scripts/frontier_yt_pr230_genuine_source_pole_artifact_intake.py`
**Certificate:** `outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json`

## Purpose

The refreshed campaign goal is to find the one genuinely admissible artifact
inside the current closure contracts.  The cleanest contract is still
`O_H/C_sH/C_HH` source-Higgs pole rows.  This block identifies the strongest
current artifact inside that contract and records its exact claim boundary.

## Result

The current PR230 surface does contain one genuine source-side object:

```text
O_sp = sqrt(dGamma_ss/dx | pole) O_s
```

from `outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json`.
It is same-surface and same-source, has unit pole residue, is invariant under
source-coordinate rescaling, and analytic source contact terms do not change
the isolated pole residue.  This removes the arbitrary source-unit gauge on
the source-pole side.

This is not top-Yukawa closure.  The current surface still lacks:

- a canonical `O_H` identity/normalization certificate;
- pole-level `C_spH` or `C_sH/C_HH` rows;
- `O_sp`-Higgs Gram purity;
- scalar-LSZ FV/IR/model-class authority;
- retained-route or campaign authorization for `proposed_retained`.

## Cleanest Next Artifact

The next positive artifact is no longer another source-only normalization
argument.  It is an `O_sp`-Higgs pole-residue row file:

```text
Res_C_sp_sp = 1
Res_C_spH
Res_C_HH
```

with same-surface `O_H` identity/normalization and the usual FV/IR,
model-class, and forbidden-import gates.  Since `O_sp` has already fixed the
source-side LSZ normalization, these rows test exactly the remaining overlap
with the canonical Higgs pole.

## Literature Boundary

FMS and Feynman-Hellmann literature is used only as route context:
gauge-invariant Higgs-operator language and source-response measurements are
the right shapes once the same-surface action/operator exists.  They do not
identify the PR230 scalar source with `O_H`, set `kappa_s = 1`, or supply pole
rows.

## Non-Claim

No retained or `proposed_retained` closure is claimed.  This block does not
identify `O_sp` with `O_H`, set `cos(theta) = 1`, use `H_unit`, use the old
`yt_ward_identity`, use observed targets, or use `alpha_LM`/plaquette/`u0`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_genuine_source_pole_artifact_intake.py
# SUMMARY: PASS=14 FAIL=0

python3 scripts/frontier_yt_pr230_negative_route_applicability_review.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=42 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=277 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=97 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=245 FAIL=0
```
