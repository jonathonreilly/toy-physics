# FH/LSZ Pade-Stieltjes Bounds Gate

**Runner:** `scripts/frontier_yt_fh_lsz_pade_stieltjes_bounds_gate.py`
**Certificate:** `outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json`
**Status:** exact-support / open.  This does not authorize
`proposed_retained`.

## Purpose

This note records the next non-chunk scalar-LSZ physics block for PR #230.  It
tests whether finite Stieltjes/Pade moment theory can replace production
pole-fit compute for the scalar LSZ residue.

The result is a sharp boundary:

- A same-surface positive Stieltjes moment sequence, isolated scalar pole,
  certified threshold gap, FV/IR control, and tight positive residue interval
  would be enough to make a non-MC scalar-LSZ certificate.
- The current PR #230 surface does not contain that certificate.  Existing
  finite source/shell rows are not moment bounds and cannot be promoted into
  a Pade/Stieltjes residue theorem.

## Contract

The future certificate accepted by the gate is:

`outputs/yt_fh_lsz_pade_stieltjes_bounds_certificate_2026-05-05.json`

It must certify:

- same-surface `Cl(3)/Z^3` scalar data;
- the Stieltjes moment-certificate gate has passed;
- at least six positive moments;
- certified scalar pole location;
- certified continuum threshold gap;
- FV/IR control;
- a positive pole-residue interval with relative width at most `0.02`;
- analytic-continuation or microscopic scalar-denominator authority;
- no observed-target selector, H-unit/Ward authority, `alpha_LM`,
  plaquette/u0 chain, or unit shortcut.

## Witness

The runner builds a positive Stieltjes witness with a pole plus positive
continuum.  When the continuum threshold is separated from the pole and enough
moments are supplied, the linear truncated moment problem gives tight
upper/lower bounds on the pole residue.  When the continuum can approach the
pole, finite moment bounds remain broad.

This is exactly the scalar-LSZ obstruction in PR #230: Pade/Stieltjes theory is
a valid positive route only after the missing moment/threshold/FV certificate
exists.  It is not an authority for reinterpreting finite source/shell rows as
canonical Higgs LSZ normalization.

## Non-Claims

This artifact does not:

- claim scalar-LSZ closure;
- claim retained or `proposed_retained` top-Yukawa closure;
- define `y_t_bare`;
- use the H-unit/Ward route, `alpha_LM`, plaquette/u0, observed targets, or
  unit-normalization shortcuts;
- replace production chunk evidence by a mathematical assumption.

## Next Action

Either produce the strict Pade/Stieltjes bounds certificate from same-surface
scalar data, derive a microscopic scalar-denominator theorem that implies it,
or continue production chunks until the postprocessor can emit a certified
moment/threshold/FV package.
