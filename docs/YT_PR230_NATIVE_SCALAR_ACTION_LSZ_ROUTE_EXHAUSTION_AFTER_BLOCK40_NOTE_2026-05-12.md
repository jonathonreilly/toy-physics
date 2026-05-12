# PR230 Native Scalar/Action/LSZ Route Exhaustion After Block40

**Status:** support / exact negative boundary on the current PR230 surface

**Runner:**
`scripts/frontier_yt_pr230_native_scalar_action_lsz_route_exhaustion_after_block40.py`

**Certificate:**
`outputs/yt_pr230_native_scalar_action_lsz_route_exhaustion_after_block40_2026-05-12.json`

```yaml
actual_current_surface_status: support / exact negative boundary: native scalar/action/LSZ current-surface route exhausted after Block40 without a new primitive
conditional_surface_status: conditional-support if a future same-surface scalar-channel kernel/covariance, dynamic scalar carrier, accepted action, scalar LSZ metric, strict C_ss/C_sH/C_HH pole rows, strict W/Z absolute authority, or neutral-transfer primitive lands
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

Block40 closed the last concrete native-scalar shortcut in the active
opportunity queue: treating a formal HS/logdet auxiliary scalar as canonical
`O_H`.  This block records the route-level consequence.  On the current PR230
surface, the native scalar/action/LSZ lane is exhausted unless a genuinely new
same-surface primitive appears.

This is not a permanent no-go against scalar/action physics.  It is a
current-surface boundary for the artifacts now present in PR230.

## Routes Checked

| Route | Current result | Remaining import |
|---|---|---|
| Minimal Cl(3)/Z3 action premise | exact negative boundary | no dynamic `Phi`, accepted action, canonical `O_H`, or scalar LSZ metric |
| FMS candidate/action packet | conditional support | candidate support only; no adopted same-surface action or strict rows |
| FMS action-adoption cut | exact support / open cut | still needs action, LSZ metric, source identity, and pole rows |
| HS/logdet auxiliary scalar | exact negative boundary | auxiliary normalization and source-Higgs overlap vary under rescaling/rotation |
| Legendre effective action | exact negative boundary | Legendre transform is covariant under source/operator rescaling |
| Source reparametrization | exact negative boundary | source normalization remains a gauge freedom |
| Scalar LSZ normalization cancellation | conditional support | bookkeeping cancellation only; interacting kernel and pole derivative open |
| Source-functional LSZ pole | exact negative boundary | source-pole coupling does not determine overlap with canonical Higgs mode |
| Effective-potential Hessian / SSB algebra | exact negative boundary | Hessian eigenvalues do not fix the microscopic source direction |
| Existing canonical scalar-normalization surfaces | exact negative boundary | EW/Higgs surfaces assume or structure canonical `H`; they do not derive PR230 source normalization |
| Source-to-Higgs LSZ closure attempt | open | named source-to-canonical-Higgs LSZ theorem remains open |
| Scalar carrier/projector closure | open | physical scalar carrier/projector and `K'(pole)` remain open |
| Finite-shell exact math / holonomic LSZ | exact negative boundary | finite shell data do not identify physical denominator or LSZ residue |
| Carleman/Tauberian scalar LSZ determinacy | exact negative boundary | strict moment/FV/IR authority remains absent |
| Strict scalar LSZ moment/FV gate | open/support-only | strict scalar moment/FV authority is absent |

## Boundary

The native scalar/action/LSZ route can reopen only through a new primitive:

1. a same-surface scalar-channel kernel/covariance plus fixed scalar metric;
2. a dynamic scalar carrier/action derived from Cl(3)/Z3 or explicitly
   admitted as an action extension;
3. strict `C_ss/C_sH/C_HH` pole rows after canonical `O_H` is independently
   supplied;
4. a same-surface neutral transfer or primitive-cone theorem fixing the
   physical Higgs direction;
5. a strict W/Z physical-response packet with non-observed absolute `g2` or
   explicit `v` authority.

## Non-Claims

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not declare a permanent no-go against future scalar/action physics.
It does not use `H_unit`, Ward, `y_t_bare`, observed targets, `alpha_LM`,
plaquette, or `u0`; it does not set `kappa_s`, `c2`, `Z_match`,
source-Higgs overlap, or auxiliary normalization to one; and it does not
relabel `C_sx/C_xx` as `C_sH/C_HH`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_native_scalar_action_lsz_route_exhaustion_after_block40.py
python3 scripts/frontier_yt_pr230_native_scalar_action_lsz_route_exhaustion_after_block40.py
# SUMMARY: PASS=18 FAIL=0
```
