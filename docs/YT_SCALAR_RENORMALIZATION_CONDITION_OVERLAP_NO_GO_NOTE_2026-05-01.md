# PR #230 Scalar Renormalization-Condition Source-Overlap No-Go

**Status:** exact negative boundary / scalar renormalization-condition source-overlap no-go
**Runner:** `scripts/frontier_yt_scalar_renormalization_condition_overlap_no_go.py`
**Certificate:** `outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json`

## Question

Can the canonical Higgs kinetic renormalization condition fix the overlap
between the Cl(3)/Z3 additive scalar source and the canonical Higgs field?

## Result

No.  The canonical condition fixes the normalization of an already identified
field `h`, equivalently the `h-h` pole residue.  It does not fix the operator
matrix element:

```text
z_s = <0|O_s|h>
```

The runner constructs countermodels with identical:

```text
Z_h = 1
Higgs pole mass
v
canonical y_h
```

but different `z_s`.  Their source response `dE/ds` and same-source pole
residue `Res C_ss` change together.  The invariant readout

```text
dE/ds / sqrt(Res C_ss)
```

stays fixed, which is exactly why the same-source scalar pole residue is the
needed measurement.  Setting the source overlap to one is not licensed by the
canonical kinetic renormalization condition.

## Claim Boundary

```text
proposal_allowed: false
```

This blocks a shortcut only.  It does not derive `kappa_s`, does not use
`H_unit`, does not use observed top/Higgs/Yukawa values, and does not treat
reduced pilots as production evidence.

## Exact Next Action

Measure or derive the same-source scalar pole residue/overlap.  Canonical Higgs
kinetic normalization is only one side of the source-to-Higgs LSZ bridge.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_scalar_renormalization_condition_overlap_no_go.py
python3 scripts/frontier_yt_scalar_renormalization_condition_overlap_no_go.py
# SUMMARY: PASS=11 FAIL=0
```
