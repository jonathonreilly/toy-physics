# Claim Status Certificate — Block 02 (Pauli exclusion principle)

**Date:** 2026-05-02
**Block:** 02 — Pauli exclusion from retained spin-statistics
**Slug:** `positive-only-retained-20260502`
**Branch:** `physics-loop/positive-only-block02-pauli-exclusion-20260502`
**Note:** [docs/PAULI_EXCLUSION_FROM_SPIN_STATISTICS_THEOREM_NOTE_2026-05-02.md](../../../../docs/PAULI_EXCLUSION_FROM_SPIN_STATISTICS_THEOREM_NOTE_2026-05-02.md)
**Runner:** [scripts/pauli_exclusion_check.py](../../../../scripts/pauli_exclusion_check.py)
**Log:** [outputs/pauli_exclusion_check_2026-05-02.txt](../../../../outputs/pauli_exclusion_check_2026-05-02.txt)

## Strict-bar gate

This block was admitted to the campaign queue only after passing the
positive_theorem-retained-only pre-screen:

- claim_type: positive_theorem ✓ (no narrow scope; unconditional
  on retained matter content)
- every load-bearing dep at retained-grade on live ledger ✓ (single
  one-hop dep `axiom_first_spin_statistics_theorem_note_2026-04-29`
  is at `effective_status: retained`)
- zero admitted physics inputs ✓ (vacuum definition is structural;
  basic linear algebra only)
- runner produces classifiable PASS lines ✓ (5/5 PASS, including
  explicit Jordan-Wigner construction of fermionic Fock space and
  exhaustive Hilbert-basis occupation-number verification)

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "(a^†_φ)² = 0 on H_phys for any fermionic mode |φ⟩; equivalently the two-fermion same-mode state a^†_φ a^†_φ |0⟩ is the zero vector; occupation number n_φ ∈ {0, 1}."
admitted_context_inputs:
  - QFT vacuum definition (a_φ |0⟩ = 0)
  - basic finite-dim linear algebra
upstream_dependencies:
  - axiom_first_spin_statistics_theorem_note_2026-04-29 (effective_status: retained)
runner_classified_passes: 5 PASS at machine precision (anticommutator sanity {a^†_i, a^†_j} = 0; (a^†_φ)² = 0; same-mode state = 0; n_φ² = n_φ; full 4-state Hilbert basis with all occupations in {0, 1})
```

## Expected `effective_status` after audit

If Codex returns `audit_status = audited_clean` and `claim_type =
positive_theorem`:

- chain_clean check: single dep at `retained` → True
- claim_type = positive_theorem → `effective_status = retained`

Block 02 has the **shortest possible clean chain** of any block in the
strict-bar campaign — single one-hop dependency on a retained note.
This is the "easy retained" candidate.

## Dependency chain status snapshot (2026-05-02 live ledger)

| Dep | Today's `effective_status` | Affects propagation? |
|---|---|---|
| `axiom_first_spin_statistics_theorem_note_2026-04-29` | `retained` | clean |

Chain is fully clean.

## Review-loop disposition

- branch-local self-review: `pass` (5/5 runner tests at machine
  precision; theorem proof is two-line Steps 1-3 application of
  retained spin-statistics).
- formal Codex audit: pending under new prompt template.

## Audit hand-off

What an auditor needs to evaluate this note:

1. The note itself.
2. The cited authority `AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`.
3. The runner script and its output.
4. The new audit prompt template.

Expected outcome: `retained` (single retained-grade dep, no admitted
physics, single-line consequence).
