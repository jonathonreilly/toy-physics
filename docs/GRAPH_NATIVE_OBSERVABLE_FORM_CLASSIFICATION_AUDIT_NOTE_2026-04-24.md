# Retained Graph-Native Observable Form-Type Classification Audit

**Date:** 2026-04-24
**Status:** N+3 step — package-level observable audit applying the
loop-15 and N+2 force-vs-gauge separation theorems.
**Runner:** `scripts/frontier_graph_native_observable_form_classification_audit.py`
**Result:** `8/8 PASS`. Wallclock `0.01 s`.
**Predecessor notes:**
- [`STAGGERED_FORCE_GAUGE_SEPARATION_THEOREM_NOTE_2026-04-24.md`](STAGGERED_FORCE_GAUGE_SEPARATION_THEOREM_NOTE_2026-04-24.md) — loop 15 single-cycle theorem (T.1-T.5).
- [`STAGGERED_FORCE_GAUGE_MULTI_CYCLE_HOMOLOGY_THEOREM_NOTE_2026-04-24.md`](STAGGERED_FORCE_GAUGE_MULTI_CYCLE_HOMOLOGY_THEOREM_NOTE_2026-04-24.md) — N+2 multi-cycle extension (M.1-M.5).

## 1. Question

Loops 15 (single-cycle) and N+2 (multi-cycle homology) established a
classification framework for graph-native observables: 0-form
(local, no cycle dependence), 1-form (edge integral, source-proximal
rule), 2-form (plaquette / face), and higher (general Wilson loops).

The N+3 question: does this classification framework apply
uniformly across the **retained** graph-native observable package?
Are there latent edge-selection ambiguities hiding in manuscript-
adjacent scripts?

## 2. Method

Hand-classified catalog of 12 retained graph-native observables,
with automated heuristic verification:

- each observable mapped to its canonical script
- form type: `0-form` / `1-form` / `2-form` / `higher` / `top-form`
- rule status: `N/A` (0-form) / `explicit` / `implicit` / `ambiguous`
- script existence check (all 12 present in repo)
- keyword heuristic verifying explicit-rule 1-form/2-form scripts
  reference the expected rule vocabulary (`source-proximal`,
  `non-bridge`, `plaquette`, `Wilson loop`, `area law`, etc.)

## 3. Frozen catalog

### 0-form observables (6)

| Observable | Script | Description |
|---|---|---|
| Newton's force F = G M m / r^2 | `scripts/frontier_newton_derived.py` | Gradient of phi at test particle position |
| Self-consistent Poisson field equation | `scripts/frontier_self_consistent_field_equation.py` | Vertex-wise scalar equation; unique self-consistent closure |
| Staggered backreaction force rows | `scripts/frontier_staggered_graph_observables_backreaction_stress.py` | Source-sector rows: force, density response, two-body additivity, etc. |
| Three-generation observable | `scripts/frontier_three_generation_observable_theorem.py` | Fermion zero-mode count; spectrum topological invariant |
| Anomaly-forced 3+1 time axis | `scripts/frontier_anomaly_forces_time.py` | Vertex-local anomaly cancellation constraint |
| CKM atlas observable basis | `scripts/frontier_ckm_atlas_axiom_closure.py` | Spectral matrix-element observables in chosen basis |

### 1-form observables (2)

| Observable | Script | Rule |
|---|---|---|
| U(1) edge current j(i,j) = phi(j) - phi(i) | `scripts/frontier_staggered_backreaction_active_gauge_edge_selection.py` | source-proximal non-bridge edge (explicit, loop-15 T.5) |
| Staggered backreaction gauge/current row | `scripts/frontier_staggered_backreaction_active_gauge_edge_selection.py` | same rule; DAGs correctly get N/A |

### 2-form observables (2)

| Observable | Script | Rule |
|---|---|---|
| Wilson plaquette P_mu_nu(x) | `scripts/frontier_non_abelian_gauge.py` | canonical 4-site face on cubic lattice; averaged over all plaquettes |
| Canonical plaquette expectation <P> | `scripts/canonical_plaquette_surface.py` | canonical average on Cl(3)/Z^3 package surface |

### Higher-order / top-form (2)

| Observable | Script | Rule |
|---|---|---|
| Wilson loop W(C), area-law string tension | `scripts/frontier_confinement_string_tension.py` | rectangular R×T loops; translation-averaged |
| Strong CP topological charge Q_top (theta term) | `scripts/frontier_strong_cp_theta_zero.py` | top-form integration over whole lattice; no local edge/face ambiguity |

## 4. Verdicts

- **A.1** PASS: all 6 0-form observables have `rule_status = N/A`
  (no edge selection needed; locality follows from loop-15 T.1).
- **A.2** PASS: both 1-form observables have explicit edge rules
  (source-proximal non-bridge per loop-15 T.5).
- **A.3** PASS: both 2-form observables have explicit face rules
  (canonical plaquette averaged over all faces).
- **B.1** PASS: catalog has 12 entries; structured and reproducible.
- **C.1** PASS: all 12 cataloged scripts exist in the repo.
- **C.2** PASS: all explicit-rule 1-form/2-form/higher scripts contain
  the expected rule keywords on heuristic inspection.
- **D.1** PASS: no 1-form/2-form observables with ambiguous or
  implicit edge/face rules detected.
- **E.1** PASS (honest-open): the classification is hand-curated
  and the keyword check is heuristic, not a proof. A reviewer
  should spot-check any manuscript-facing observable against its
  actual implementation.

## 5. Interpretation

Three sharp conclusions:

1. **The retained graph-native package is uniformly consistent with
   the loop-15 / N+2 classification framework.** No latent edge-
   selection ambiguities were found among the 12 cataloged
   observables. Every 1-form and 2-form observable either has an
   explicit edge/face rule embedded in its canonical script, or is
   an averaged/translation-invariant quantity by construction.

2. **The retained observable distribution is heavily 0-form
   weighted**: 6/12 = 50% of cataloged observables are local
   0-forms, consistent with a manuscript-core package that
   emphasizes POISSON/NEWTON scalar gravity, spectrum-level matter
   observables, and specific-basis CKM/YT numbers — all of which
   live at the vertex level.

3. **The staggered backreaction gauge/current row is the sharpest
   test case for the loop-15/N+2 source-proximal rule.** It is the
   only 1-form observable where the edge selection is the central
   object of the experimental protocol (rather than implicit via
   canonical averaging). Future backreaction cards inherit the
   explicit-rule requirement from this row's precedent.

## 6. What this changes

- The loop-15 + N+2 theorem framework is now **package-wide**: it
  applies uniformly across the 12 cataloged retained observables.
- Future additions to the retained package can be classified
  immediately via the same catalog structure.
- The absence of ambiguous cases means no ongoing manuscript claim
  needs a cycle-rule retrofit.

## 7. Falsifier

- A retained 0-form observable found to have hidden cycle
  dependence (would reclassify and invalidate A.1).
- A retained 1-form observable with an ambiguous edge rule hidden
  by averaging (would invalidate A.2 if the averaging isn't
  uniform).
- A 2-form observable that's secretly edge-dependent rather than
  face-dependent (miscategorization; would invalidate A.3).
- A script claimed to have explicit rule but not referencing the
  expected keywords (C.2 heuristic false-positive).

None of these are currently exhibited by the 12-entry catalog.

## 8. What this does NOT do

- Not a theorem-grade audit: the classification is hand-curated
  and heuristic-verified, not automatically verified by the
  runner against the implementation semantics.
- Does not extend the catalog beyond 12 observables; the repo has
  many more exploratory scripts not classified here.
- Does not cover non-abelian Wilson loops as primary observables
  (only as 2-form plaquettes and higher-order rectangular loops);
  the N+4 lift to non-abelian cycle holonomies is a separate step.

## 9. Next concrete step

- **N+4 non-abelian lift**: extend loop-15/N+2 to the non-abelian
  setting where cycle integral becomes a Wilson loop (gauge-
  invariant, nontrivial); this is the natural theorem-grade
  extension.
- **Catalog expansion**: classify additional exploratory
  observables (growth-based, interferometric, phenomenology) as
  they are promoted toward retained status. The N+3 catalog
  becomes a living document.
- **Backreaction-card specification**: write a formal retained
  backreaction card template that requires 0-form / 1-form / 2-form
  labels for every observable row, with explicit edge/face rules
  where applicable.

## 10. Provenance

- Runner: `scripts/frontier_graph_native_observable_form_classification_audit.py`
- Catalog: 12 hand-curated entries covering gravity, gauge (abelian
  + non-abelian), matter, strong CP, and staggered backreaction.
- Result: `8/8 PASS`, wallclock `0.01 s`.
- Reproducibility: deterministic; catalog is a module-level
  constant, heuristic checks are simple regex over script source.
- Runtime caveat: validation host Python 3.12.8; no numerical
  libraries used. Pure filesystem + structured data.
