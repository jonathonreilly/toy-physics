# YT Positivity-Improving Neutral-Scalar Rank-One Support

```yaml
actual_current_surface_status: conditional-support / positivity-improving neutral-scalar rank-one theorem; premise absent
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_positivity_improving_neutral_scalar_rank_one_support.py`  
**Certificate:** `outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json`

## Purpose

This block attacks the remaining microscopic rank-one route for PR #230.  The
existing commutant, dynamical-rank, and decoupling no-gos show that symmetry
labels, D17 support, source-only rows, and finite orthogonal masses do not
force the neutral scalar response to be one-dimensional.

The next possible theorem is stronger: if the same-surface neutral scalar
transfer matrix is positivity improving, Perron-Frobenius uniqueness gives a
single lowest neutral scalar state.  Combined with isolated-pole factorization,
that would make the lowest-pole residue matrix rank one.

## Theorem Surface

If a future certificate proves:

- positivity-improving transfer-matrix dynamics in the neutral scalar sector;
- a nondegenerate lowest isolated scalar pole;
- finite nonzero source and certified canonical-Higgs overlaps with that pole;

then the lowest-pole residue matrix factorizes as

```text
Res C_ij = z_i z_j
```

and the `O_sp`-Higgs Gram determinant vanishes at that pole.  This would close
the rank-one part of the source-Higgs route after a certified `O_H` and
production same-pole `C_ss/C_sH/C_HH` residues exist.

## Current Result

The runner verifies the conditional theorem surface and records a necessary
counterexample.  A strictly positive finite transfer matrix has a unique
Perron vector and gives a rank-one isolated-pole residue.  A non-improving
block-diagonal transfer matrix can keep two degenerate neutral states and a
rank-two residue matrix.

```bash
python3 scripts/frontier_yt_positivity_improving_neutral_scalar_rank_one_support.py
# SUMMARY: PASS=15 FAIL=0
```

## Boundary

This does not close PR #230.  The current surface does not prove positivity
improving dynamics in the neutral scalar sector.  Reflection positivity alone
is already blocked as insufficient, and the source-Higgs production rows,
canonical `O_H`, pole-isolation/FV/IR controls, and retained-route gate remain
absent.

This note does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, `u0`, or reduced pilots.

## Next Action

Either prove the missing positivity-improving neutral-scalar transfer-matrix
premise on the Cl(3)/Z3 substrate, or supply one of the direct rank-repair
inputs: certified `O_H` with production `C_sH/C_HH` pole rows, or same-source
W/Z response rows with sector-overlap and canonical-Higgs identity
certificates.
