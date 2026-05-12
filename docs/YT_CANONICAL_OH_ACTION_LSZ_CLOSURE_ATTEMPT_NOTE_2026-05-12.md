# PR #230 Canonical O_H Action/LSZ Closure Attempt

**Status:** exact negative boundary / canonical `O_H` action-LSZ closure primitive absent  
**Runner:** `scripts/frontier_yt_canonical_oh_action_lsz_closure.py`  
**Certificate:** `outputs/yt_canonical_oh_action_lsz_closure_2026-05-12.json`  
**Agent 4 interface:** `outputs/yt_canonical_oh_action_lsz_source_higgs_interface_2026-05-12.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: exact support for source-Higgs rows after a future accepted same-surface EW/Higgs action and O_H LSZ-pinning certificate is supplied
same_surface_cl3_z3_derived: false
accepted_current_surface: false
proposal_allowed: false
bare_retained_allowed: false
```

## Target

This block tries the narrow positive route requested for PR #230:

```text
accepted Cl(3)/Z3 action + LSZ primitives  ->  canonical Higgs radial O_H
```

The source-Higgs route needs an operator certificate that can support strict
`C_ss/C_sH/C_HH` pole rows.  The allowed source-side support is the existing
Legendre/LSZ source-pole operator `O_sp`; it is not treated as `O_H`.

## Assumptions And Imports

Allowed premises:

- the `Cl(3)` local algebra and `Z^3` substrate;
- the current staggered/Grassmann source surface and uniform scalar source
  coordinate `s`;
- the accepted Legendre/LSZ source-pole construction for `O_sp`;
- the source-Higgs contract witness as a future row acceptance surface;
- the FMS literature packet as methodology context only.

Forbidden as load-bearing inputs:

- `H_unit`;
- `yt_ward_identity`;
- `y_t_bare`;
- `alpha_LM`;
- plaquette or `u0`;
- observed target selectors;
- alias imports or static EW notation treated as proof.

## First-Principles Check

LSZ normalization fixes the source-pole side:

```text
O_sp(q) = sqrt(dGamma_ss/dx | pole) O_s(q),
Res(C_sp,sp) = 1.
```

But LSZ normalization alone does not identify the physical Higgs axis.  A
canonical unit-residue neutral basis can still contain

```text
O_sp = cos(theta) O_H + sin(theta) O_chi.
```

For `theta != 0`, `Res(C_sp,sp)=1` and `Res(C_HH)=1` remain true, while
`Res(C_sp,H)=cos(theta)` and the source-Higgs Gram determinant is
`1 - cos(theta)^2`.  The rotation is killed only by an action identity pinning
the source-pole direction to the canonical Higgs radial field, or by pole-level
`C_sH/C_HH` Gram purity after a certified `O_H` exists.

## Result

The positive action/LSZ closure does not pass on the current PR #230 surface.
The current action surface has the SU(3)/staggered top harness and a guarded
source-Higgs measurement shell, but no accepted same-surface dynamic EW/Higgs
action, no action-derived canonical `O_H` identity, and no LSZ normalization
certificate for `O_H`.

The existing EW Higgs gauge-mass and SM one-Higgs notes remain useful support
after canonical `H` is supplied.  They do not define the PR230 source-pole
operator as canonical `O_H`.  The FMS packet gives a future implementation
shape, not current-surface authority.

## Agent 4 Interface

The exact source-Higgs interface is emitted as:

```text
outputs/yt_canonical_oh_action_lsz_source_higgs_interface_2026-05-12.json
```

It requires a future operator certificate with:

- same-surface Cl(3)/Z3 and same source-coordinate flags;
- an accepted same-surface EW/Higgs action certificate;
- an action-derived `O_H` definition, not a diagonal vertex by fiat;
- canonical normalization fields: kinetic convention, field rescaling,
  `v/sqrt(2)` convention, sign convention, and pole-residue target;
- LSZ residue convention for `Res(C_ss)`, `Res(C_sH)`, and `Res(C_HH)`;
- non-shortcut identity and normalization certificates;
- firewall flags excluding `H_unit`, Ward, observed targets, `alpha_LM`,
  plaquette/u0, `y_t_bare`, and alias imports.

Only after that certificate exists should Agent 4 produce strict
`C_ss/C_sH/C_HH` pole rows for the builder and Gram-purity postprocessor.

## Narrow Obstruction

The remaining primitive is:

```text
same-surface accepted EW/Higgs action and LSZ pinning theorem
```

It must prove that the PR230 source-pole direction is the canonical Higgs
radial direction, or equivalently supply the accepted `O_H` certificate
consumed by the source-Higgs row pipeline.

## Verification

```bash
python3 scripts/frontier_yt_canonical_oh_action_lsz_closure.py
# SUMMARY: PASS=20 FAIL=0
```

The runner records that no degree-one radial-tangent gate was available under
the current script namespace.  The FMS construction, source-Higgs contract,
assembly, and campaign gates remain the live checks for this boundary.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not define `O_H` by fiat, does not launch live chunk work, and does not
use `H_unit`, `yt_ward_identity`, `y_t_bare`, `alpha_LM`, plaquette/u0,
observed targets, or alias imports.
