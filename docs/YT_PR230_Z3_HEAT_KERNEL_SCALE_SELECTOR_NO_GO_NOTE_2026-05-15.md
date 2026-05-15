# PR230 Z3 Heat-Kernel Scale-Selector No-Go

**Status:** exact negative boundary / Z3 heat-kernel scale and time selectors
do not derive the PR230 physical neutral transfer

**Claim type:** no-go / exact boundary

**Runner:** `scripts/frontier_yt_pr230_z3_heat_kernel_scale_selector_no_go.py`

**Certificate:** `outputs/yt_pr230_z3_heat_kernel_scale_selector_no_go_2026-05-15.json`

```yaml
actual_current_surface_status: exact negative boundary / Z3 heat-kernel scale and time selectors do not derive the PR230 physical neutral transfer
conditional_surface_status: if a future same-surface action fixes the heat time or diffusion scale and supplies H4 source/canonical-Higgs coupling, the Block102 heat-kernel primitive witness can be reused as mathematical support
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

Block102 showed that the finite `C3/Z3` Dirichlet form gives a real primitive
heat-kernel witness.  The remaining possible shortcut was to treat the
canonical-looking heat kernel as the physical neutral transfer by selecting a
heat time or diffusion scale from symmetry, cone, semigroup, reversibility,
entropy, or spectral-gap criteria.

This block tests that selector step directly.

## Result

The current PR230 surface does not select a physical heat time or scale.

For `Delta = 2I - P - P^T`, every sampled `K_tau = exp(-tau Delta)` with
`tau > 0` is:

- Z3-covariant;
- symmetric and uniformly reversible;
- row- and column-stochastic;
- strictly positive and primitive;
- part of the same semigroup `K_a K_b = K_{a+b}`;
- convergent to the same uniform rank-one projector.

The runner also checks the generator-scale reparametrization:

```text
Delta -> lambda Delta
K(t) = exp(-t lambda Delta) = exp(-(lambda t) Delta)
```

So the heat time and diffusion coefficient are interchangeable unless the
action supplies one of them.  The current PR230 surface supplies neither.

Entropy and discrete spectral-gap criteria do not repair this.  On this
heat-kernel family they increase toward the `tau -> infinity` uniform
projector limit, so using them would either import an external optimization
principle or select a boundary limit, not a derived finite physical transfer.

## Boundary

This is narrower than the older lazy-selector no-go.  The lazy selector closed
directed Markov-family shortcuts.  This block closes the reversible
finite-group heat-kernel scale shortcut left open by Block102.

It does not close the neutral route permanently.  It says the next neutral
artifact must be physical, not only finite-group mathematical:

```text
same-surface action / transfer / off-diagonal generator
+ heat-time or diffusion-scale authority
+ H4 source/canonical-Higgs coupling
```

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not set the heat time or diffusion scale to one, does not treat entropy
or spectral gap as a PR230 action principle, does not write a neutral
primitive-cone certificate, does not identify the Z3 taste triplet or source
with canonical `O_H`, and does not set `kappa_s`, `c2`, `Z_match`, `g2`, `v`,
or source-Higgs overlap to one.

It does not use `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`,
plaquette, or `u0`.

## Exact Next Action

Reopen the neutral route only with a same-surface physical action, transfer
operator, or off-diagonal generator that fixes the heat time/diffusion scale,
plus H4 source/canonical-Higgs coupling.  Otherwise continue through accepted
`O_H`/action plus strict `C_ss/C_sH/C_HH` pole rows, strict W/Z response with
an allowed absolute pin, or strict Schur/scalar-LSZ pole authority.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_z3_heat_kernel_scale_selector_no_go.py
python3 scripts/frontier_yt_pr230_z3_heat_kernel_scale_selector_no_go.py
# SUMMARY: PASS=13 FAIL=0
```
