# PR230 HS/Logdet Scalar-Action Normalization No-Go

**Status:** support / exact negative boundary on the current PR230 surface

**Runner:** `scripts/frontier_yt_pr230_hs_logdet_scalar_action_normalization_no_go.py`

**Certificate:**
`outputs/yt_pr230_hs_logdet_scalar_action_normalization_no_go_2026-05-12.json`

```yaml
actual_current_surface_status: support / exact negative boundary: HS-logdet auxiliary scalar action normalization does not derive canonical O_H on the current PR230 surface
conditional_surface_status: conditional-support if a future same-surface four-fermion/kernel covariance, dynamic scalar carrier, accepted action, canonical LSZ metric, and strict C_ss/C_sH/C_HH pole rows are supplied
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

This block attacks a tempting shortcut left open after the lane-1
action-premise and logdet-neutral-mixing audits:

```text
source/logdet data + formal Hubbard-Stratonovich rewrite
=> canonical same-surface O_H action/LSZ authority
```

The shortcut does not close on the current PR230 surface.  A formal auxiliary
field can be an exact rewriting of a source functional while still leaving the
auxiliary field normalization, scalar LSZ metric, and source-Higgs overlap
undetermined.

## Counterfamily 1: HS Rescaling

For one source current `J`,

```text
exp(1/2 K J^2) = integral dphi exp[-phi^2/(2K) + J phi].
```

The field redefinition `chi = a phi` gives the same integrated source
functional:

```text
integral dchi exp[-chi^2/(2 a^2 K) + (J/a) chi].
```

The product that reconstructs the source functional is invariant:

```text
(source coupling)^2 * (auxiliary propagator) = K.
```

But the auxiliary propagator, source coupling, and LSZ-like field norm vary
with `a`.  Source-only/logdet data therefore do not select a canonical Higgs
normalization.

## Counterfamily 2: Neutral Rotation

If a second neutral auxiliary direction is not fixed by a same-surface action,
the source-only row remains unchanged while the candidate Higgs overlap varies:

```text
H(theta) = cos(theta) phi_x + sin(theta) phi_n
C_ss fixed
C_sH proportional to cos(theta)
C_sH^2/(C_ss C_HH) = cos^2(theta)
```

Thus source-only rows cannot replace strict `C_ss/C_sH/C_HH` rows or a
primitive neutral-transfer theorem.

## Parent Boundaries Used

This block consumes, without promoting, the existing current-surface
boundaries:

- lane-1 action premise remains blocked;
- source-only logdet Hessian does not define the second neutral source;
- HS/RPA pole condition needs a scalar-channel kernel theorem;
- scalar-kernel enhancement and pole-derivative authority remain imports;
- scalar carrier/projector closure remains open;
- canonical `O_H` hard residual remains open;
- full retained-route and campaign gates still reject proposal language.

## Boundary

The result is an exact negative boundary for the HS/logdet shortcut, not a
permanent no-go against all scalar/action routes.  It retires if a later
artifact supplies one of:

1. a native Cl(3)/Z3 derivation of a scalar action and LSZ metric;
2. a two-source same-surface determinant functional with certified canonical
   `O_H`;
3. strict `C_ss/C_sH/C_HH` pole rows after `O_H` is independently supplied;
4. a neutral primitive transfer theorem that fixes the physical Higgs
   direction.

## Non-Claims

This block does not claim retained or `proposed_retained` y_t closure.  It
does not define `y_t_bare`, does not use `H_unit`, Ward identity, observed
top/Higgs/y_t targets, `alpha_LM`, plaquette, or `u0`, and does not set the
auxiliary normalization, source-Higgs overlap, `c2`, `Z_match`, or `kappa_s`
to one.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_hs_logdet_scalar_action_normalization_no_go.py
python3 scripts/frontier_yt_pr230_hs_logdet_scalar_action_normalization_no_go.py
# SUMMARY: PASS=18 FAIL=0
```
