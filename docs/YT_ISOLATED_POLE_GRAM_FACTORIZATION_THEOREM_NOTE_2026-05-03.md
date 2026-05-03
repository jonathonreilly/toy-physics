# YT Isolated-Pole Gram Factorization Theorem

```yaml
actual_current_surface_status: exact-support / isolated-pole Gram factorization theorem
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_isolated_pole_gram_factorization_theorem.py`  
**Certificate:** `outputs/yt_isolated_pole_gram_factorization_theorem_2026-05-03.json`

## Statement

For a same-sector Euclidean two-point matrix with a nondegenerate isolated
scalar pole,

```text
C_ij(p^2) = z_i z_j / (p^2 + m_*^2) + regular terms,
```

the residue matrix at that pole factorizes:

```text
Res C_ij = z_i z_j.
```

Therefore every `2 x 2` pole-residue Gram determinant vanishes.  For the
PR #230 source-Higgs route,

```text
Delta = Res(C_ss) Res(C_HH) - Res(C_sH)^2 = 0.
```

Using the existing Legendre/LSZ normalized source-pole operator
`O_sp = O_s / sqrt(Res(C_ss))`, the same statement is

```text
Res(C_sp,H) = Res(C_sH) / sqrt(Res(C_ss))
Delta_spH = Res(C_HH) - Res(C_sp,H)^2 = 0
|rho_spH| = 1.
```

This is exact support for the future `O_sp`-Higgs Gram-purity gate.  It says
that once the source side and a certified canonical `O_H` are shown to overlap
with the same nondegenerate isolated pole, Gram purity follows from spectral
factorization rather than from a fitted assumption.

## Assumptions

- same Hilbert space and same scalar superselection sector;
- nondegenerate isolated pole separated from continuum and other poles;
- finite nonzero overlap of each operator with that pole;
- pole residues extracted at the same pole on the same ensemble/surface.

The runner also records a necessary-assumption counterexample: if two
independent states are degenerate at the same pole, the residue matrix can be
rank two and the Gram determinant need not vanish.

## PR #230 Boundary

This does not close PR #230.  It does not supply a canonical `O_H`, does not
create `C_sH` or `C_HH` production pole rows, does not prove pole isolation or
finite-volume/IR control, and does not identify the source pole with the
canonical Higgs radial mode.  It also does not use `H_unit`,
`yt_ward_identity`, observed top/Yukawa/W/Z values, `alpha_LM`, plaquette, or
`u0`.

## Verification

```bash
python3 scripts/frontier_yt_isolated_pole_gram_factorization_theorem.py
# SUMMARY: PASS=12 FAIL=0
```

## Next Action

Use this theorem as the exact support layer for future source-Higgs rows:
supply a certified `O_H`, production same-pole `C_ss/C_sH/C_HH` residues with
nondegenerate pole isolation, then rerun the `O_sp`-normalized Gram
postprocessor and retained-route gate.
