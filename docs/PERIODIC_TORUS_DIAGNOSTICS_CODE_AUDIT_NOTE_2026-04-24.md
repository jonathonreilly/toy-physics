# Periodic 2D Torus Diagnostics Code Audit Note

**Date:** 2026-04-24
**Status:** review-hardening artifact for the active-queue item
"periodic 2D torus diagnostics: nearby torus probes still need code
audit before reuse outside the corrected retained notes". The lane
remains OPEN; this note pins down the candidate set for follow-up
manual review.
**Runner:** `scripts/frontier_periodic_torus_diagnostics_audit.py`
**Result:** `5/5 PASS`. Wallclock < 1 second.

## 1. Question

The 2026-04-11 minimum-image bug
([`PERIODIC_2D_WRAPAROUND_FIX_NOTE_2026-04-11.md`](PERIODIC_2D_WRAPAROUND_FIX_NOTE_2026-04-11.md))
was: periodic adjacency built with modulo indexing, but hopping
weights computed from raw coordinate differences. A wraparound
nearest-neighbor on a `side x side` torus was treated as having
distance `side - 1` instead of `1`.

The fix note lists 9 canonical-corrected periodic scripts. The
active queue notes that other periodic-torus scripts have not been
audited against the helper at `scripts/periodic_geometry.py`.

## 2. Setup

Static-analysis classification of every `scripts/*.py` file (2048
total) using regex pattern matching:

- **Periodic modulo** detection: `% side`, `% L`, `% N`, `% n`,
  `% n_side`, `% nside`, `% edge`.
- **Helper import** detection: `from periodic_geometry import …` or
  `import periodic_geometry`.
- **Inline minimum-image guard** detection:
  - `min(dx, side - dx)` form,
  - explicit `minimum_image` symbol,
  - centered-modulo `(... + L // 2) % L - L // 2` form.
- **Distance-weighted coupling** detection:
  - `1.0 / max(d, ...)` (Hamiltonian hop weights),
  - `exp(-mu * d)` (Yukawa kernels),
  - `1.0 / d ** 2` (Coulomb-like),
  - `math.hypot(dx, dy)` (distance computation),
  - `sqrt(dx ** 2 + ...)` (Euclidean norm).
- **np.roll** detection (auto-periodic shifts without manual distances).

## 3. Frozen audit table

Across 2048 scripts/*.py files:

| status | count | meaning |
|---|---:|---|
| `NOT_APPLICABLE` | 1987 | no periodic modulo at all |
| `CLEAN_NO_DISTANCE` | 35 | modulo present but no distance-weighted couplings |
| `CLEAN_HELPER` | 6 | imports `periodic_geometry` helper |
| `CLEAN_INLINE` | 11 | inline minimum-image guard present |
| `NEEDS_REVIEW` | 9 | periodic modulo + distance couplings + no guard |
| `ERROR` | 0 | could not read file |

### NEEDS_REVIEW (9 scripts)

1. `frontier_continuous_dirac_potential.py`
2. `frontier_correct_coupling.py`
3. `frontier_dirac_bottleneck_tests.py`
4. `frontier_geometric_gravity_v2.py`
5. `frontier_graph_kg_16card.py`
6. `frontier_graph_kg_full_suite.py`
7. `frontier_graph_laplacian_kg.py`
8. `frontier_shapiro_delay.py`
9. `frontier_staggered_3d_17card.py`

These are the candidates for follow-up manual review against the
helper at `scripts/periodic_geometry.py`. The audit **does not**
prove these scripts exhibit the bug; it identifies them as having
the structural ingredients (periodic modulo + distance couplings +
no minimum-image guard).

### Cross-check vs canonical fix note

All 9 canonical-corrected scripts from the 2026-04-11 fix note are
correctly classified into `CLEAN_*` buckets:

- `frontier_bmv_entanglement.py` -> CLEAN_HELPER
- `frontier_bmv_threebody.py` -> CLEAN_HELPER
- `frontier_born_rule_alpha.py` -> CLEAN_INLINE
- `frontier_boundary_law_robustness.py` -> CLEAN_HELPER
- `frontier_branch_entanglement_robustness.py` -> CLEAN_HELPER
- `frontier_eigenvalue_stats_and_anderson_phase.py` -> CLEAN_INLINE
- `frontier_holographic_probe.py` -> CLEAN_HELPER
- `frontier_self_consistency_test.py` -> CLEAN_INLINE
- `frontier_staggered_geometry_superposition_retained.py` -> CLEAN_HELPER

This validates the audit rules: every script the fix note declares
clean is correctly classified clean by the audit.

## 4. Verdicts

- **A.1 PASS**: every canonical-corrected script avoids `NEEDS_REVIEW`.
- **A.2 PASS**: every canonical-corrected script lands in some
  `CLEAN_*` bucket.
- **B.1 PASS**: audit produces a frozen `NEEDS_REVIEW` list of 9
  scripts.
- **B.2 PASS**: audit is reproducible (deterministic regex scan).
- **C.1 PASS**: audit is honestly framed as static analysis only;
  `NEEDS_REVIEW` ≠ `BUG`. Manual confirmation is required for each
  flagged script.

## 5. Known false-positive class

Spot-checking `frontier_shapiro_delay.py` shows the modulo is a
1D ring (`(x+1) % n` at line 264) while the 2D Hamiltonian
(`_build_H` at line 91) uses *open* adjacency without
wraparound. The two pieces don't interact, so the script may be
genuinely clean despite the audit flag.

This illustrates the soft-positive character of the audit: the
regex finds structural ingredients without proving they connect
in the buggy way. The audit's job is to narrow the manual-review
surface from 2048 scripts to 9, a 227× reduction. Final
classification of each flagged script requires file-level review.

## 6. Falsifier

- A `NEEDS_REVIEW` script that, on manual inspection, is clean
  (would tighten the audit rules — e.g. add the centered-modulo
  guard, which we already added in this run after spot-checking
  `frontier_monopole_derived.py`).
- A `CLEAN_*` script that uses raw periodic-edge distances at
  any Hamiltonian site (would loosen the audit rules and require
  a stronger check).

The runner exposes both via the cross-check section A.

## 7. Active-queue update

The `periodic 2D torus diagnostics` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains OPEN. The new content is the frozen 9-script
`NEEDS_REVIEW` list. The lane is not promoted, demoted, or closed.

## 8. Next concrete step

Manually review each of the 9 `NEEDS_REVIEW` scripts against
`scripts/periodic_geometry.py`. For each:

- If the script is in current use, fix or quarantine it.
- If it is historical and not used, mark it as such in a follow-up
  note and demote it from any reuse path.
- If it turns out to be genuinely clean (false positive), tighten
  the audit regex.

A reasonable next loop could take 2-3 of these scripts and produce
explicit per-script verdicts.

## 9. Provenance

- Runner: `scripts/frontier_periodic_torus_diagnostics_audit.py`
- Underlying patterns: regex scan against
  `scripts/periodic_geometry.py` (helper) and the centered-modulo
  /`min(dx, side - dx)` idioms.
- Result: `5/5 PASS`, wallclock < 1 second.
- Reproducibility: deterministic; same input directory → same
  classification.
- Runtime caveat: validation host Python 3.12.8; the audit is pure
  filesystem + regex, no numerical libraries used.
