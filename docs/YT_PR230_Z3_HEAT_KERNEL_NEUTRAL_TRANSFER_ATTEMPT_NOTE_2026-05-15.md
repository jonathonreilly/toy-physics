# PR230 Z3 Heat-Kernel Neutral-Transfer Attempt

**Status:** exact-support / Z3 heat-kernel primitive transfer is mathematical
support only; PR230 physical H3/H4 closure remains absent

**Claim type:** support / exact boundary

**Runner:** `scripts/frontier_yt_pr230_z3_heat_kernel_neutral_transfer_attempt.py`

**Certificate:** `outputs/yt_pr230_z3_heat_kernel_neutral_transfer_attempt_2026-05-15.json`

```yaml
actual_current_surface_status: exact-support / Z3 heat-kernel primitive transfer is mathematical support only; PR230 physical H3/H4 closure remains absent
conditional_surface_status: if a future same-surface action or transfer certificate identifies exp(-t Delta) at a derived t as the PR230 neutral transfer and also supplies source/canonical-Higgs coupling authority, this finite witness can support the neutral primitive route
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

After the finite-row and package-`v` shortcuts were closed, the clean remaining
neutral route was a genuine H3/H4 artifact.  This block tests a stronger
mathematical primitive than the earlier lazy-transfer shortcut: the canonical
finite-group heat kernel on the Z3 taste triplet.

Let `P` be the cyclic Z3 action on the triplet and define
`Delta = 2 I - P - P^T`.  The heat kernel `K_t = exp(-t Delta)` has a closed
form on the three-cycle.  For every `t > 0`, it is symmetric, stochastic,
strictly positive, commutes with the Z3 action, and is primitive with uniform
rank-one limit.

## Result

The mathematical primitive witness is real:

- `Delta` has spectrum `[0, 3, 3]`;
- `K_t` has diagonal `(1 + 2 exp(-3t))/3` and off-diagonal
  `(1 - exp(-3t))/3`;
- the runner checks `t = 0.25, 1.0, 4.0`, and each `t > 0` row is a positive
  stochastic primitive matrix.

But it is not a retained-route artifact on the actual PR230 surface.  The
current artifacts do not identify this heat kernel as the physical neutral
transfer, do not derive the heat time or diffusion coefficient from the action,
and do not supply H4: coupling to the PR230 source/canonical-Higgs sector.

The attempt therefore strengthens the neutral route map but does not close it.

## Claim Boundary

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not write a neutral primitive-cone certificate, does not treat a
finite-group heat kernel as PR230 physical dynamics, does not select the heat
time by convention, does not identify the Z3 taste triplet or `O_s` with
canonical `O_H`, and does not set `kappa_s`, `c2`, `Z_match`, `g2`, `v`, or any
source-Higgs overlap to one.

The block does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0`.

## Exact Next Action

Reopen the neutral route only with a same-surface physical action or transfer
certificate that selects the heat-kernel time/scale, plus a separate H4
source/canonical-Higgs coupling certificate.  Otherwise continue through one
of the other named strict artifacts: accepted `O_H`/action plus
`C_ss/C_sH/C_HH` pole rows, strict W/Z physical-response rows with an allowed
absolute pin, or strict Schur/scalar-LSZ pole authority.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_z3_heat_kernel_neutral_transfer_attempt.py
python3 scripts/frontier_yt_pr230_z3_heat_kernel_neutral_transfer_attempt.py
# SUMMARY: PASS=16 FAIL=0
```
