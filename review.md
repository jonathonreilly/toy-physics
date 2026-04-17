# Review

**Date:** 2026-04-17  
**Branch:** `claude/charged-lepton-closure-review`  
**Verdict:** not accepted

This branch is not ready to land. The current blockers are:

1. **Theorem 3 overstates disjointness as orthogonality.**  
   In [docs/MASS_MIXING_SUBSPACE_DISJOINTNESS_THEOREM_NOTE.md](docs/MASS_MIXING_SUBSPACE_DISJOINTNESS_THEOREM_NOTE.md), the note proves `dim(V_H ∩ V_D) = 0` by a rank/intersection argument, but then upgrades that to “structurally orthogonal.” The runner only certifies trivial intersection. Those are different statements, and the stronger one is false as written.

2. **Observational-pin uniqueness is asserted, not checked.**  
   In [scripts/frontier_charged_lepton_observational_pin_closure.py](scripts/frontier_charged_lepton_observational_pin_closure.py), the uniqueness block sets `unique = True`, iterates over alternate orderings with no actual test, and then later hardcodes `unique_pin = True` again in the final verdict logic. That does not certify the note/matrix claim that the observational pin is unique up to scale.

3. **Theorem 7 hides a live mass-vs-mass-squared convention choice.**  
   In [docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md), Theorem 7 states the pin as `(w_{O_0}, w_a, w_b) = (m_e, m_\mu, m_\tau)`, but the runner explicitly says the natural second-order identification would be proportional to `(m_e^2, m_\mu^2, m_\tau^2)` and then switches to linear masses “by convention.” That convention materially affects the closure claim and must be surfaced or justified in the authority note.

4. **The new charged-lepton package row is not wired through the package truth surfaces.**  
   [docs/publication/ci3_z3/PUBLICATION_MATRIX.md](docs/publication/ci3_z3/PUBLICATION_MATRIX.md) and [docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md](docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md) were updated, but the same package is still absent from:
   - [docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md](docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md)
   - [docs/publication/ci3_z3/RESULTS_INDEX.md](docs/publication/ci3_z3/RESULTS_INDEX.md)
   - [docs/publication/ci3_z3/README.md](docs/publication/ci3_z3/README.md)
   - [docs/publication/ci3_z3/EXTERNAL_REVIEWER_GUIDE.md](docs/publication/ci3_z3/EXTERNAL_REVIEWER_GUIDE.md)

## Notes

- `py_compile` passed for the new scripts.
- I did not independently replay the full 19-runner stack in this review thread because the default desktop `python3` environment here does not have `sympy`.

## Fix expectation

This branch should not be resubmitted until all four blockers above are resolved and `review.md` is updated accordingly.
