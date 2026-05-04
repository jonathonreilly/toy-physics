# YT Neutral-Scalar Irreducibility Authority Audit

```yaml
actual_current_surface_status: exact negative boundary / neutral-scalar irreducibility authority absent on current PR230 surface
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_neutral_scalar_irreducibility_authority_audit.py`
**Certificate:** `outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json`

## Purpose

This block checks the remaining rank-one neutral-scalar route after the direct
positivity-improving stretch attempt.  The conditional theorem is useful: if a
same-surface neutral scalar transfer sector is positivity improving, then
Perron-Frobenius uniqueness plus isolated-pole factorization would force a
rank-one lowest-pole residue matrix.

The open question is whether the current PR230 repository surface already
contains that missing irreducibility / primitive-cone certificate.

## Result

It does not.

The runner searches for exact positive authority keys such as
`neutral_scalar_irreducibility_theorem_passed`,
`primitive_cone_irreducibility_theorem_passed`, and
`positivity_improving_certificate_present`.  No current output or loop-pack
certificate supplies them as true.  It also reloads the parent no-go/support
certificates:

- positivity-improving rank-one is conditional support only;
- the direct positivity-improvement theorem was not derived;
- gauge-vacuum Perron uniqueness does not certify the neutral scalar block;
- reflection positivity supplies positive spectral weights, not
  irreducibility;
- source-only tomography has rank one and leaves a null direction.

```bash
python3 scripts/frontier_yt_neutral_scalar_irreducibility_authority_audit.py
# SUMMARY: PASS=11 FAIL=0
```

## Premise Contract

A positive future theorem must prove, on the same PR230 Cl(3)/Z3
Wilson-staggered surface, that the neutral scalar transfer sector is a single
primitive cone after the gauge, fermion, scalar-source, and canonical-Higgs
constructions are specified.

It must not import the result from `H_unit`, the Ward readout, observed top
values, `alpha_LM`, plaquette/u0 normalization, static EW algebra, reflection
positivity alone, gauge-only Perron uniqueness, or finite source-only rows.

## Boundary

This is an exact negative boundary for the current authority surface, not a
retained closure theorem.  It knocks the neutral-rank route down to one of the
same real missing inputs already identified by PR230: a same-surface
irreducibility theorem, certified `O_H` with `C_sH/C_HH` pole rows, same-source
W/Z response rows with identity certificates, or Schur `A/B/C` kernel rows.
