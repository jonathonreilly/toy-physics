# PR230 Source-Coordinate Transport Gate

**Status:** exact negative boundary / source-coordinate transport to canonical O_H not derivable on the current PR230 surface

```yaml
actual_current_surface_status: exact negative boundary / source-coordinate transport to canonical O_H not derivable on current PR230 surface
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_pr230_source_coordinate_transport_gate.py`
**Certificate:** `outputs/yt_pr230_source_coordinate_transport_gate_2026-05-06.json`

## Purpose

This block tests the pure source-coordinate repair left after the
taste-condensate shortcut failed.  The question is whether the PR230 uniform
additive mass source can be transported, by an allowed same-surface coordinate
change, into the canonical trace-zero taste/Higgs axis needed for `O_H`.

The answer on the current surface is no.

## Algebra

The PR230 FH/LSZ source line is the one-dimensional uniform mass source

```text
m_bare -> m_bare + s
```

with linear insertion `I_8` on the taste block.  The existing taste/Higgs axes
are trace-zero shift involutions `S_i`.

The runner verifies:

- `Tr(S_i) = 0`;
- `<I_8, S_i> = 0` for every taste axis;
- the projection of `I_8` onto `span(S_i)` is zero;
- analytic scalar reparametrizations keep the linear tangent proportional to
  `I_8`;
- Cl/taste automorphisms fix `I_8`;
- a nonzero linear taste-axis tangent is a new source coupling, not a
  reparametrization of the current source line;
- a singular or zero-Jacobian map cannot provide LSZ/canonical linear
  normalization.

## Boundary

This does not block future two-source or action-first work.  It blocks only the
current shortcut that tries to obtain canonical `O_H` by relabeling the
existing one-dimensional uniform source coordinate.

The route reopens with a real source-coordinate transport certificate, direct
canonical `O_H/C_sH/C_HH` pole rows, strict W/Z response rows, Schur `A/B/C`
rows, or a neutral primitive/off-diagonal-generator certificate accepted by the
aggregate gates.

## Non-Claims

This note does not claim retained or `proposed_retained` PR230 closure.  It
does not identify `O_sp` with `O_H`, does not add a trace-zero source axis and
call it current-surface derivation, and does not use `H_unit`,
`yt_ward_identity`, observed targets, `alpha_LM`, plaquette, `u0`,
`kappa_s=1`, `c2=1`, or `Z_match=1`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_source_coordinate_transport_gate.py
# SUMMARY: PASS=21 FAIL=0
```
