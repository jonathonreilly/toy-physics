# Neutral-Scalar Primitive-Cone Certificate Gate

**Runner:** `scripts/frontier_yt_neutral_scalar_primitive_cone_certificate_gate.py`
**Certificate:** `outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json`
**Status:** exact-support / open.  This does not authorize
`proposed_retained`.

## Purpose

This note records the positive contract for the neutral-rank non-chunk route
in PR #230.  If the neutral top-coupled scalar transfer sector were proved
primitive and positivity-improving, the existing conditional Perron/rank-one
support could remove the orthogonal neutral scalar ambiguity.

The current surface does not prove that theorem.  This gate makes the missing
input explicit.

## Future Certificate

The gate accepts:

`outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json`

The future certificate must provide:

- same-surface `Cl(3)/Z^3` neutral scalar sector data;
- declared neutral-sector basis;
- a square nonnegative neutral transfer matrix;
- a strongly connected directed graph of positive matrix entries;
- a finite positive primitive power of the transfer matrix;
- certified isolated lowest neutral pole;
- positive source-pole and canonical-Higgs overlaps;
- certified null of orthogonal neutral contamination;
- firewall rejection of observed selectors, H-unit/Ward authority,
  `alpha_LM`, plaquette/u0, and unit-overlap shortcuts.

## Witnesses

The runner includes two finite transfer witnesses:

- a primitive positive matrix, showing what a valid future certificate must
  look like;
- a reducible positive diagonal matrix, showing why positivity preservation
  alone does not imply neutral-sector irreducibility.

This isolates the actual blocker.  Reflection positivity, gauge Perron
support, symmetry labels, source-only rows, and conditional rank-one support
are not enough; the missing premise is a same-surface primitive-cone theorem
or certified measurement rows that remove the orthogonal sector.

## Non-Claims

This artifact does not:

- claim neutral rank-one closure;
- claim retained or `proposed_retained` top-Yukawa closure;
- define `y_t_bare`;
- use the H-unit/Ward route, observed targets, `alpha_LM`, plaquette/u0, or
  unit-overlap shortcuts;
- replace source-Higgs, W/Z, Schur, or scalar-LSZ production evidence.

## Next Action

Supply the strict primitive-cone certificate, or use another real positive
surface: same-surface `O_H/C_sH/C_HH` rows, W/Z response rows, Schur `A/B/C`
kernel rows, or certified scalar-LSZ production output.
