# PR230 Kinetic Taste-Mixing Bridge Attempt

**Status:** exact negative boundary / current staggered kinetic taste symmetry
does not supply the PR230 source-Higgs bridge

**Runner:** `scripts/frontier_yt_pr230_kinetic_taste_mixing_bridge_attempt.py`
**Certificate:** `outputs/yt_pr230_kinetic_taste_mixing_bridge_attempt_2026-05-06.json`

## Purpose

This block checks a loophole left open by the static source-coordinate
transport no-go.

The static result says the PR230 uniform additive mass source `I_8` cannot be
transported to the trace-zero taste-Higgs axes `S_i` by unit-preserving,
trace-preserving, or taste-equivariant maps.  This runner asks whether the
staggered kinetic dynamics itself could generate the missing source-Higgs row:

```text
C_sH = <O_source O_H>
```

without a new source-coordinate theorem, `H_unit`, Ward readout, observed
selector, or unit-overlap convention.

## Result

It cannot on the current PR230 surface.

The current source operator is taste-even:

```text
F_i I_8 F_i = I_8.
```

The candidate taste-Higgs axes from the taste scalar theorem are taste-odd:

```text
F_i S_i F_i = -S_i.
```

With no certified Higgs/taste background source switched on, the Wilson-
staggered action and measure are taste-flip invariant.  Any taste-even
transfer polynomial therefore has zero Hilbert-Schmidt cross row with one
trace-zero taste insertion.  The runner constructs a representative
flip-averaged transfer and verifies

```text
C_sH = 0
```

to numerical precision on all three taste axes.

## Boundary

This closes only the shortcut that hidden kinetic mixing already supplies a
source-Higgs row on the current PR230 surface.  It does **not** rule out:

- a same-source EW/Higgs action with an explicit symmetry-breaking Higgs/taste
  background;
- a same-surface canonical `O_H` identity and normalization certificate;
- production `C_ss/C_sH/C_HH` rows with pole isolation and Gram purity;
- a W/Z physical-response bypass;
- Schur `A/B/C` neutral-kernel rows;
- a neutral primitive/rank-one theorem.

## Non-Claims

This note does not claim retained or proposed-retained `y_t` closure.  It does
not define `y_t_bare`, does not use `H_unit` or `yt_ward_identity`, does not use
observed targets, `alpha_LM`, plaquette, or `u0`, and does not set
source-Higgs overlap, `kappa_s`, `c2`, `Z_match`, or `cos(theta)` to one.

## Verification

```bash
python3 scripts/frontier_yt_pr230_kinetic_taste_mixing_bridge_attempt.py
# SUMMARY: PASS=21 FAIL=0
```
