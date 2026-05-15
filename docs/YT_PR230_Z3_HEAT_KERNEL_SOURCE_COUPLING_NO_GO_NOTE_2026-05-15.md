# PR230 Z3 Heat-Kernel Source-Coupling No-Go

**Status:** exact negative boundary / Z3 heat-kernel source-coupling data do
not supply PR230 H4 source/canonical-Higgs coupling

**Claim type:** no-go / exact boundary

**Runner:** `scripts/frontier_yt_pr230_z3_heat_kernel_source_coupling_no_go.py`

**Certificate:** `outputs/yt_pr230_z3_heat_kernel_source_coupling_no_go_2026-05-15.json`

```yaml
actual_current_surface_status: exact negative boundary / Z3 heat-kernel source-coupling data do not supply PR230 H4 source/canonical-Higgs coupling
conditional_surface_status: if a future same-surface action, transfer operator, or off-diagonal generator fixes the source-triplet coupling eta and also supplies canonical O_H/source-Higgs pole authority, the Block102 heat-kernel primitive support can be reused
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

Blocks102-103 left one finite-group shortcut to test.  The `C3/Z3` heat
kernel gives a genuine primitive triplet witness, but PR230 closure needs H4:
the source/canonical-Higgs coupling connecting the PR230 source singlet to the
neutral triplet and ultimately to canonical `O_H`.

This block asks whether the heat-kernel construction itself supplies that
coupling.

## Result

It does not on the current PR230 surface.

The source-plus-triplet block extension

```text
T_0 = diag(1, K_tau)
```

keeps the triplet heat-kernel facts: symmetry, stochasticity, reversibility,
and Z3 covariance.  It is not enough.  The source row and column remain
isolated, all source-triplet entries are zero, and the four-state transfer is
reducible rather than primitive.

One can make a formal source-plus-triplet matrix primitive by adding a positive
source-triplet coupling `eta`:

```text
T_eta =
  [[1-3 eta, eta, eta, eta],
   [eta, (1-eta)K_00, (1-eta)K_01, (1-eta)K_02],
   [eta, (1-eta)K_10, (1-eta)K_11, (1-eta)K_12],
   [eta, (1-eta)K_20, (1-eta)K_21, (1-eta)K_22]]
```

For sampled `0 < eta < 1/3`, this matrix is symmetric, stochastic, positive,
Z3-covariant, and primitive.  That is a consistency witness, not a closure:
`eta` is an independent source-triplet/action datum.  Current PR230 artifacts
do not derive or measure `eta`, do not identify the source or triplet with
canonical `O_H`, and do not provide physical `C_sH/C_HH` pole rows.

## Boundary

Block102 supplied a finite primitive mathematical witness.  Block103 ruled out
selecting the physical heat time or diffusion scale from heat-kernel symmetry,
cone, semigroup, reversibility, entropy, or spectral-gap data.  Block104 adds
the H4 boundary:

```text
finite Z3 heat kernel
  + no source-triplet eta
  + no canonical O_H identity
  + no physical C_sH/C_HH pole rows
  = no PR230 source/canonical-Higgs closure
```

The neutral route is therefore not admitted by heat-kernel structure alone.  A
future neutral artifact must supply same-surface source-triplet coupling or
off-diagonal generator authority, plus canonical-Higgs/source-overlap or strict
physical pole-row authority.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not set `eta`, heat time, diffusion scale, `kappa_s`, `c2`,
`Z_match`, `g2`, `v`, or source-Higgs overlap to one.  It does not identify a
source singlet, taste triplet, `O_s`, or `O_sp` with canonical `O_H`, and it
does not relabel `C_sx/C_xx` rows as physical `C_sH/C_HH` rows.

It does not use `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`,
plaquette, or `u0`.

## Exact Next Action

Reopen the neutral route only with a same-surface source-triplet
coupling/action row, off-diagonal generator, or primitive-cone certificate
that fixes `eta` and H4 source/canonical-Higgs coupling.  Otherwise continue
through accepted `O_H`/action plus strict `C_ss/C_sH/C_HH` pole rows, strict
W/Z response with an allowed absolute pin, or strict Schur/scalar-LSZ pole
authority.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_z3_heat_kernel_source_coupling_no_go.py
python3 scripts/frontier_yt_pr230_z3_heat_kernel_source_coupling_no_go.py
# SUMMARY: PASS=13 FAIL=0
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=325 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=427 FAIL=0
python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=200 FAIL=0
python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=79 FAIL=0
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=111 FAIL=0
```
