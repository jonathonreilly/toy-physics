# YT Neutral-Scalar Positivity-Improving Direct Closure Attempt

```yaml
actual_current_surface_status: exact negative boundary / neutral-scalar positivity-improving direct theorem not derived
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_neutral_scalar_positivity_improving_direct_closure_attempt.py`  
**Certificate:** `outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json`

## Purpose

This is the direct stretch attempt after the gauge-Perron import audit.  The
previous conditional theorem showed that positivity-improving neutral scalar
transfer dynamics would give a unique lowest scalar pole, and then
isolated-pole factorization would force rank-one source-Higgs residues.

The question here is stronger: does the current Cl(3)/Z3 substrate prove that
neutral-scalar positivity-improving premise directly?

## Assumption Test

Allowed premises:

- Cl(3)/Z3 Wilson-staggered substrate with `g_bare = 1`;
- the support-level axiom-first reflection-positivity note as structural
  context;
- current PR #230 source/FH/LSZ certificates and no-go ledger.

Forbidden imports:

- `H_unit` or `yt_ward_identity` matrix-element readout;
- observed `m_t`, `y_t`, W/Z values, or PDG values as proof selectors;
- `alpha_LM`, plaquette value, `u0`, or fitted scalar-kernel multipliers;
- gauge-vacuum Perron uniqueness as a neutral-scalar theorem.

## Result

The direct theorem is not derived on the current surface.

Reflection positivity and a positive transfer operator are weaker than
positivity improvement.  The missing step is irreducibility / primitive-cone
positivity improvement in the neutral scalar response sector after the
fermion, gauge, scalar-source, and canonical-Higgs constructions are all
specified.

The runner records a finite witness: a positive semidefinite neutral transfer
matrix can be reducible, with two degenerate neutral scalar directions.  It is
positivity preserving but not positivity improving.  Source-only rows can be
kept fixed while the canonical-Higgs vector rotates into the orthogonal
neutral direction.

```bash
python3 scripts/frontier_yt_neutral_scalar_positivity_improving_direct_closure_attempt.py
# SUMMARY: PASS=14 FAIL=0
```

## Stuck Fan-Out

The runner checks five frames and names the wall in each:

- OS/reflection positivity gives positive spectral weights, not a single
  neutral scalar pole or fixed residue.
- Gauge heat-kernel strict positivity is scoped to the gauge plaquette source
  problem, not the neutral scalar block.
- Fermion transfer positivity gives a positive semidefinite transfer, not
  positivity improvement inside the composite neutral scalar response sector.
- Source operator cyclicity is not proved; current source-only spectrum still
  permits an orthogonal neutral top-coupled direction.
- Canonical-Higgs identity remains blocked by source-pole mixing.

## Boundary

This closes only the direct positivity-improvement shortcut on the current
surface.  It does not close PR #230 and does not authorize retained or
`proposed_retained` wording.

The next positive routes are direct rank-repair data (`O_H/C_sH/C_HH` pole
rows or same-source W/Z response rows with identity certificates) or the scalar
denominator / `K'(pole)` theorem.
