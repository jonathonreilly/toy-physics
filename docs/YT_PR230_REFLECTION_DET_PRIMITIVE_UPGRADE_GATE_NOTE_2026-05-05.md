# PR230 Reflection + Determinant Primitive-Upgrade Gate

**Date:** 2026-05-05  
**Status:** exact negative boundary / reflection plus determinant positivity
does not upgrade PR230 to a neutral primitive-cone bridge  
**Runner:** `scripts/frontier_yt_pr230_reflection_det_primitive_upgrade_gate.py`  
**Certificate:** `outputs/yt_pr230_reflection_det_primitive_upgrade_gate_2026-05-05.json`

## Question

The current PR230 non-chunk lane has two nearby positivity inputs:

- OS/reflection positivity, which supports a positive spectral representation;
- the staggered-Wilson determinant-positivity bridge, which supports a
  positive fermion measure on the symmetric-canonical surface.

This note tests whether combining them supplies the missing neutral scalar
primitive-cone theorem needed to identify the source-created scalar pole with
the canonical Higgs readout.

## Verdict

No.  The combination is useful support, but it is not closure.

Both inputs are positivity-preservation statements.  PR230 needs a stronger
neutral-sector statement:

```text
same-surface neutral scalar transfer is irreducible / positivity improving
```

or an explicit observable bridge:

```text
canonical O_H plus C_sH/C_HH pole rows
same-source W/Z response rows
Schur A/B/C rows
strict production FH/LSZ plus matching
```

## Reducible Positive Witness

The runner constructs a finite neutral-sector witness:

```text
T = [[0.93, 0.00],
     [0.00, 0.89]]
```

with positive spectral weights and positive determinant flag.  This witness is
reflection-positive and determinant-positive in the relevant support sense,
but its transfer graph is not strongly connected and no finite power is
strictly positive.  A source vector can see only the first block while an
orthogonal neutral top-coupled direction survives in the second block.

Therefore positive measure plus OS positivity cannot be promoted into
primitive-cone irreducibility.

## Audit Boundary

This gate is deliberately negative.  It prevents a clean but invalid
shortcut:

```text
positive measure -> positive spectral representation -> unique Higgs pole
```

The last implication is the missing theorem.  It requires positivity
improvement or direct bridge rows, not just positivity preservation.

## Non-Claims

This note does not claim retained or proposed-retained top-Yukawa closure.  It
does not define `y_t_bare`, does not use `H_unit` or
`yt_ward_identity`, does not use observed top/Yukawa values or
`alpha_LM`/plaquette/`u0` inputs, and does not identify source-only `C_ss`
rows with canonical `O_H`.

## Next Action

Keep determinant and reflection positivity as support only.  The positive
closure route still needs one actual bridge object: a same-surface neutral
primitive-cone certificate, canonical `O_H` with `C_sH/C_HH` rows,
same-source W/Z response rows, Schur `A/B/C` rows, or strict production
FH/LSZ plus matching.

## Verification

```bash
python3 scripts/frontier_yt_pr230_reflection_det_primitive_upgrade_gate.py
# SUMMARY: PASS=14 FAIL=0
```
