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
- single load-bearing dep at retained-grade on live ledger ✓
  (`cpt_exact_note` is at `effective_status: retained`)
- zero admitted physics inputs ✓ (CPT operator action is structural;
  eigenvalue invariance is basic linear algebra)
- runner produces classifiable PASS lines ✓ (5/5 PASS, including a
  **negative control** demonstrating that without CPT, particle/
  antiparticle spectra do differ)

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "On the framework's retained CPT-invariant Hamiltonian, every particle energy eigenstate has an antiparticle eigenstate with identical energy; in particular, particle/antiparticle rest masses are equal. Holds uniformly for every fermion species in the retained matter content."
admitted_context_inputs:
  - CPT operator action convention on particle/antiparticle states
  - eigenvalue invariance under (anti-)unitary conjugation
upstream_dependencies:
  - cpt_exact_note (effective_status: retained)
runner_classified_passes: 5 PASS at machine precision (Hermiticity, [CPT, H] = 0, identical spectra, 5-trial universality, negative control without CPT shows split spectra)
```

## Expected `effective_status` after audit

If Codex returns `audit_status = audited_clean` and `claim_type =
positive_theorem`:

- chain_clean check: single dep at `retained` → True
- claim_type = positive_theorem → `effective_status = retained`

## Dependency chain status snapshot (2026-05-02 live ledger)

| Dep | Today's `effective_status` | Affects propagation? |
|---|---|---|
| `cpt_exact_note` | `retained` | clean |

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

Expected outcome: `retained`.
