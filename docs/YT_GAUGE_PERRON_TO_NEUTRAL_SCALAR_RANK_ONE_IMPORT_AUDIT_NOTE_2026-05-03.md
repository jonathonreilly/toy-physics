# YT Gauge-Perron To Neutral-Scalar Rank-One Import Audit

```yaml
actual_current_surface_status: exact negative boundary / gauge-vacuum Perron theorem does not certify neutral-scalar rank-one purity
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_gauge_perron_to_neutral_scalar_rank_one_import_audit.py`  
**Certificate:** `outputs/yt_gauge_perron_to_neutral_scalar_rank_one_import_audit_2026-05-03.json`

## Purpose

The previous PR #230 block identified a possible positive route: if the
same-surface neutral scalar transfer dynamics are positivity improving, then
Perron-Frobenius uniqueness plus isolated-pole factorization gives a rank-one
lowest-pole residue matrix.

The repository already has a gauge-vacuum Perron theorem for the finite Wilson
plaquette problem:

`docs/GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md`

This audit asks whether that theorem can be imported as the missing
neutral-scalar positivity-improving premise.

## Result

It cannot.

The gauge theorem is scoped to the finite Wilson gauge transfer state and the
local plaquette source operator

```text
J = (chi_(1,0) + chi_(0,1)) / 6.
```

It proves a unique positive gauge Perron state for that plaquette source
problem.  It does not prove positivity improvement in the neutral scalar
transfer block, identify the Legendre/LSZ source-pole operator `O_sp` with the
canonical Higgs operator `O_H`, or remove orthogonal neutral scalar top
couplings.

The runner records a finite counterfamily: keep the same strictly positive
gauge Perron block, then couple it to either a positivity-improving neutral
block with rank-one residue or to a non-improving degenerate neutral block with
rank-two residue.  The gauge Perron data are unchanged, while the neutral
lowest-pole Gram determinant changes from zero to nonzero.

```bash
python3 scripts/frontier_yt_gauge_perron_to_neutral_scalar_rank_one_import_audit.py
# SUMMARY: PASS=14 FAIL=0
```

## Boundary

This closes only the import shortcut.  It does not close PR #230.

The remaining positive routes are unchanged:

- prove same-surface neutral-scalar positivity improvement directly;
- produce certified `O_H` with production `C_sH/C_HH` pole rows;
- produce same-source W/Z response rows with sector-overlap and
  canonical-Higgs identity certificates;
- derive the scalar denominator / `K'(pole)` theorem.

This note does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, the plaquette value, `u0`, or reduced pilots.
