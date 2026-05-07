# PR230 Canonical O_H / WZ Common Accepted-Action Cut

**Status:** exact support/boundary / canonical `O_H` and W/Z accepted-action common-cut certificate; current surface remains open

**Claim type:** open_gate

**Audit status authority:** independent audit lane only

**Runner:** `scripts/frontier_yt_pr230_canonical_oh_wz_common_action_cut.py`

**Certificate:** `outputs/yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json`

## Purpose

This block resumes the PR230 neutral-transfer/eigenoperator campaign after the
source-mixing no-go.  The current neutral primitive route is blocked: current
Z3/taste eigenoperator data do not supply a physical source-radial
off-diagonal transfer/action row.

The requested pivot is therefore to the two highest-value physical routes:

- canonical `O_H` / source-Higgs pole rows;
- W/Z same-source physical response.

The runner asks which certificate vertex is common to both routes and which
data obligations remain route-specific.

## Exact Result

The strict common vertex is a non-shortcut same-surface canonical-Higgs /
accepted EW-Higgs action certificate.

For the source-Higgs route, canonical `O_H` is needed before any
`C_sH/C_HH` label is physical.  Existing support is real but conditional:
the degree-one radial-tangent theorem selects the taste-radial axis only after
a future same-surface action proves that canonical `O_H` is a linear
Z3-covariant radial tangent, and the time-kernel GEVP path is a support
contract until production rows exist.  The refreshed 2026-05-07 pass also
loads the source-Higgs time-kernel production manifest: it defines exact
future commands, but it is still not launched row evidence and still cannot
substitute for canonical `O_H`.

For the W/Z route, the same accepted-action problem appears as a root cut.
The response-ratio algebra is exact support, but the route still needs an
accepted same-source EW/Higgs action, W/Z mass-fit response rows, same-source
top-response rows, matched covariance, and strict non-observed `g2`.

After the shared vertex, the routes fork:

| Route | Route-specific obligations |
|---|---|
| canonical `O_H` / source-Higgs | production `C_ss/C_sH/C_HH` time-kernel or pole rows, Gram purity or orthogonal-neutral exclusion, OS/GEVP pole extraction, FV/IR/threshold and scalar-LSZ authority |
| W/Z response | production W/Z mass-fit response rows, same-source top response, matched top/W or top/Z covariance, strict non-observed `g2` or `sqrt(g2^2+gY^2)` authority |

## Boundary

This is not retained or `proposed_retained` closure.  It does not write the
accepted action certificate, does not relabel `C_sx/C_xx` as `C_sH/C_HH`,
does not treat the formal GEVP smoke as pole authority, and does not use
`H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`, plaquette, `u0`,
or unit conventions for `kappa_s`, `c2`, `Z_match`, or `g2`.

The block also did not touch or relaunch the live chunk worker.

## Load-Bearing Dependencies

- [Neutral transfer/eigenoperator source-mixing no-go](YT_PR230_NEUTRAL_TRANSFER_EIGENOPERATOR_SOURCE_MIXING_NO_GO_NOTE_2026-05-07.md)
- [Degree-one radial-tangent O_H theorem](YT_PR230_DEGREE_ONE_RADIAL_TANGENT_OH_THEOREM_NOTE_2026-05-07.md)
- [Source-Higgs pole-row acceptance contract](YT_PR230_SOURCE_HIGGS_POLE_ROW_ACCEPTANCE_CONTRACT_NOTE_2026-05-06.md)
- [Source-Higgs time-kernel GEVP contract](YT_PR230_SOURCE_HIGGS_TIME_KERNEL_GEVP_CONTRACT_NOTE_2026-05-07.md)
- [Source-Higgs time-kernel production manifest](YT_PR230_SOURCE_HIGGS_TIME_KERNEL_PRODUCTION_MANIFEST_NOTE_2026-05-07.md)
- [OS transfer-kernel artifact gate](YT_PR230_OS_TRANSFER_KERNEL_ARTIFACT_GATE_NOTE_2026-05-07.md)
- [W/Z response-ratio identifiability contract](YT_PR230_WZ_RESPONSE_RATIO_IDENTIFIABILITY_CONTRACT_NOTE_2026-05-07.md)
- [W/Z accepted same-source action minimal certificate cut](YT_PR230_WZ_SAME_SOURCE_ACTION_MINIMAL_CERTIFICATE_CUT_NOTE_2026-05-07.md)

## Exact Next Action

Retire the shared root vertex with a genuine same-surface artifact:
derive or supply a non-shortcut canonical `O_H` / accepted EW-Higgs action
certificate.  If that lands, run production `C_ss/C_sH/C_HH` time-kernel rows
and OS/GEVP pole/overlap gates.  If the W/Z action route lands first, build
W/Z mass-fit response rows, same-source top response, matched covariance, and
strict non-observed `g2`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_canonical_oh_wz_common_action_cut.py
python3 scripts/frontier_yt_pr230_canonical_oh_wz_common_action_cut.py
# SUMMARY: PASS=11 FAIL=0
```

Aggregate refresh after wiring this cut:

```bash
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=97 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=352 FAIL=0
python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=158 FAIL=0
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=312 FAIL=0
python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=67 FAIL=0
```
