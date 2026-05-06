# PR230 One-Higgs Taste-Axis Completeness Attempt

**Status:** exact negative boundary / one-Higgs taste-axis completeness not
derived from current PR230 taste/EW stack

**Runner:** `scripts/frontier_yt_pr230_one_higgs_taste_axis_completeness_attempt.py`
**Certificate:** `outputs/yt_pr230_one_higgs_taste_axis_completeness_attempt_2026-05-06.json`

## Purpose

This block tests the strongest one-Higgs escape from the source-pole/Higgs
mixing obstruction.

If the current `Cl(3)/Z^3` taste/EW stack proved that exactly one neutral
top-coupled scalar exists on the PR230 source surface, then any orthogonal
neutral scalar correction would vanish and the source-pole readout could be
identified with the canonical Higgs readout.

## Result

The current stack does not derive that completeness theorem.

The taste scalar theorem supplies three trace-zero taste axes `S_i`.  They are
in the same orbit under taste-factor permutations, so the theorem itself does
not select one axis as the electroweak Higgs axis.  The SM one-Higgs and EW
gauge-mass theorems are useful support after a canonical `H` is supplied, but
they do not identify which PR230 taste/source operator is `H`.

The runner also carries the existing orthogonal-coupling witness forward:
with the currently listed neutral scalar labels, an orthogonal `chi` can have
the same allowed top-bilinear labels as the canonical Higgs radial mode.  Thus
`y_chi = 0`, `cos(theta)=1`, or `O_sp = O_H` cannot be imported from one-Higgs
notation or taste-axis naming.

## Boundary

This closes only the shortcut:

```text
taste scalar theorem + SM one-Higgs notation => one-Higgs completeness on PR230
```

It does not rule out future closure from:

- a same-source EW/Higgs action certificate;
- a one-Higgs completeness certificate on the PR230 source surface;
- a canonical `O_H` identity and normalization certificate;
- production `C_ss/C_sH/C_HH` rows with Gram purity;
- a W/Z physical-response packet;
- Schur `A/B/C` rows;
- a neutral primitive/rank-one theorem.

## Non-Claims

This note does not claim retained or proposed-retained `y_t` closure.  It does
not define `O_H` by one-Higgs notation or taste-axis naming, does not set
`y_chi=0`, `cos(theta)=1`, or source-Higgs overlap to one, and does not use
`H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`, plaquette, or `u0`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_one_higgs_taste_axis_completeness_attempt.py
# SUMMARY: PASS=19 FAIL=0
```
