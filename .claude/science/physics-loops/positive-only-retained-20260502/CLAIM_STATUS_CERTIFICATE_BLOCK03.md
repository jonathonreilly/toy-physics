# Claim Status Certificate — Block 03 (CPT particle/antiparticle mass equality)

**Date:** 2026-05-02
**Block:** 03 — Particle/antiparticle mass equality from retained CPT
**Slug:** `positive-only-retained-20260502`
**Branch:** `physics-loop/positive-only-block03-cpt-mass-equality-20260502`
**Note:** [docs/CPT_PARTICLE_ANTIPARTICLE_MASS_EQUALITY_THEOREM_NOTE_2026-05-02.md](../../../../docs/CPT_PARTICLE_ANTIPARTICLE_MASS_EQUALITY_THEOREM_NOTE_2026-05-02.md)
**Runner:** [scripts/cpt_particle_antiparticle_mass_equality_check.py](../../../../scripts/cpt_particle_antiparticle_mass_equality_check.py)
**Log:** [outputs/cpt_particle_antiparticle_mass_equality_check_2026-05-02.txt](../../../../outputs/cpt_particle_antiparticle_mass_equality_check_2026-05-02.txt)

## Strict-bar gate

- claim_type: positive_theorem ✓
- load-bearing dependency disclosed: PENDING
  (`cpt_exact_note`; retained-grade closure awaits the independent audit lane
  after graph strengthening)
- zero admitted physics inputs ✓ (CPT operator action is structural;
  eigenvalue invariance is basic linear algebra)
- runner produces classifiable PASS lines ✓ (5/5 PASS, including a
  **negative control** demonstrating that without CPT, particle/
  antiparticle spectra do differ)

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "On the framework's declared CPT-invariant Hamiltonian, every CPT-exchanged particle-sector energy eigenstate has an antiparticle-sector eigenstate with identical energy; in particular, rest masses of CPT-exchanged pairs are equal."
admitted_context_inputs:
  - CPT operator action convention on particle/antiparticle states
  - eigenvalue invariance under (anti-)unitary conjugation
upstream_dependencies:
  - cpt_exact_note
runner_classified_passes: 5 PASS at machine precision (Hermiticity, [CPT, H] = 0, identical spectra, 5-trial universality, negative control without CPT shows split spectra)
```

## Audit-pending disposition

This certificate does not assign an audit verdict or an effective status. The
claim is now scoped to CPT-exchanged sectors; retained-family status is computed
only after independent audit and dependency closure.

## Dependency chain status snapshot (2026-05-02 live ledger)

| Dep | Today's effective status | Affects propagation? |
|---|---|---|
| `cpt_exact_note` | pipeline-derived; may be audit-pending after graph strengthening | pending independent audit/propagation |

## Review-loop disposition

- branch-local self-review: `pass` (5/5 runner tests including
  negative control; theorem proof matches Steps 1-4 closure on
  retained CPT identity).
- formal Codex audit: pending under new prompt template.

## Audit hand-off

What an auditor needs to evaluate this note:

1. The note itself.
2. The cited authority `CPT_EXACT_NOTE.md`.
3. The runner script and its output (note: runner includes negative
   control to demonstrate that CPT IS load-bearing — without it, the
   conclusion fails).
4. The new audit prompt template.

The intended outcome is a retained-family theorem if the independent audit
ratifies the scoped CPT-exchanged-sector argument and the dependency remains
clean.
