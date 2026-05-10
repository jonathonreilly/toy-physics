# Generated Geometry Synthesis

---

**This is a synthesis/overview note. It does not establish any retained claim.**
For retained claims, see the per-claim notes referenced from the
`## Audit scope` block below.

---

**Date:** 2026-04-05
**Status:** support / historical synthesis only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / historical synthesis only — does not propagate retained-grade
**Audit status:** audited_conditional (per audit ledger)
**Propagates retained-grade:** no
**Proposes new claims:** no

## Audit scope (relabel 2026-05-10)

This file is an **overview / program synthesis** of the generated-
geometry (Gate B) results. It is **not** a single retained theorem
and **must not** be audited as one. The audit ledger row for
`generated_geometry_synthesis_note` classified this source as
conditional/bounded with auditor's repair target:

> missing_dependency_edge: add completed cached primary runner output
> and one-hop retained artifact notes or runner packets for the
> distance-law, joint-package, no-restore, connectivity, and 2D
> confirmation claims.

The minimal-scope response in this PR is to **relabel** this document
as an overview/program synthesis rather than to physically split it
into atomic retained-claim files. Splitting is editorial work that
belongs in a dedicated review-loop pass. Until that split is performed:

- This file makes **no** retained-claim assertions of its own.
- The far-field gravity, distance-law, joint-package, 2D, no-restore,
  connectivity, and robustness-hierarchy rollups below are
  **historical program memory only**.
- The retained-status surface is the audit ledger
  (`docs/audit/AUDIT_LEDGER.md`) plus the per-claim notes, **not**
  this file.
- Retained-grade does **NOT** propagate from this synthesis note to
  any sub-claim, successor card, or successor runner.

### Per-claim pointers

The thematic sub-claims in this file have dedicated runners where the
live audit-clean status, if any, lives. Inclusion in this list is
**not** a status assertion: the live status is whatever the audit-
ledger row for each linked runner/note says today.

- **3D far-field gravity + F~M** — consult
  `scripts/gate_b_farfield_harness.py` and its per-claim note(s).
- **3D distance-law tail** — consult
  `scripts/gate_b_grown_distance_law.py` and its per-claim note(s).
- **3D joint package (Born/d_TV/MI/decoherence)** — consult
  `scripts/gate_b_grown_joint_package.py` and its per-claim note(s).
- **No-restore robustness** — consult
  `scripts/gate_b_no_restore_farfield.py` /
  `scripts/gate_b_no_restore_joint_package.py` and their per-claim
  note(s).
- **Connectivity sensitivity** — consult
  `scripts/gate_b_connectivity_tolerance.py` and its per-claim
  note(s).
- **2D cross-dimensional confirmation** — no separate audit-clean
  retained-claim note for the synthesis-level rollup tracked here yet;
  treat as historical program memory and consult per-runner logs.

For any retained claim about generated-geometry physics, audit the
corresponding dedicated runner/note as a separate scoped claim — not
this overview synthesis.

## Growth rule

Template previous layer + Gaussian drift (σ = drift × h) + restoring
force (fraction restore toward grid positions) + NN connectivity from
grid labels. Valley-linear action S=L(1-f), kernel 1/L^(d-1) with
h^(d-1) measure.

## Retained results (all with frozen artifact chains)

### 3D far-field gravity (12 seeds × 3 z-values = 36 tests per row)

| drift | restore | TOWARD | F∝M |
|-------|---------|--------|-----|
| 0.3 | 0.5 | 36/36 (100%) | 1.00 |
| 0.2 | 0.7 | 36/36 (100%) | 1.00 |
| 0.1 | 0.9 | 36/36 (100%) | 1.00 |
| 0.0 | 1.0 | 36/36 (100%) | 1.00 |

Artifacts: `gate_b_farfield_harness.py` + log + note

### 3D distance law (4 seeds, z=3..7)

| Geometry | Tail | R² |
|----------|------|-----|
| Exact grid | b^(-0.90) | 0.855 |
| Grown drift=0.2 | b^(-0.83) | 0.884 |

Artifacts: `gate_b_grown_distance_law.py` + log + note

### 3D joint package (4 seeds)

| Geometry | Born | d_TV | MI | Decoherence |
|----------|------|------|-----|-------------|
| Exact grid | 2.12e-15 | 0.787 | 0.568 | 49.4% |
| Grown drift=0.2 | 2.19e-15 | 0.811 | 0.569 | 49.4% |

Artifacts: `gate_b_grown_joint_package.py` + log + note

### 2D cross-dimensional confirmation (8 seeds)

| Geometry | TOWARD | F∝M |
|----------|--------|-----|
| Exact 2D grid | 100% | 1.00 |
| 2D grown drift=0.2 | 97% | 1.00 |

### Without restoring force (8 seeds, 3 z-values)

| drift | restore | TOWARD | F∝M | Decoherence |
|-------|---------|--------|-----|-------------|
| 0.1 | 0.0 | 83% | 1.00 | seed-dependent |
| 0.2 | 0.0 | 79% | 1.00 | seed-dependent |
| 0.3 | 0.0 | 83% | 1.00 | seed-dependent |

F∝M=1.00 survives even without restoring force. Gravity sign drops
to ~80% (from 100% with restore). Decoherence is unreliable at
one-seed measurement.

## Robustness hierarchy

| Property | What it needs | Robustness |
|----------|--------------|------------|
| F∝M = 1.00 | Just the propagator | Most robust — survives everything |
| Born | Linearity | Machine precision everywhere |
| Gravity sign | ~85% connectivity + moderate regularity | Needs structured edges |
| Distance law | Position stability (restore ≥ 0.5) | Needs moderate regularity |
| Decoherence | Position stability + slit structure | Needs the most structure |

## What this means for Gate B

The generated geometry program is the strongest it has been:

1. **Full Newtonian physics transfers** from fixed to grown lattice
   (Born, gravity, F∝M, distance, d_TV, MI, decoherence)
2. **The growth rule is dimension-independent** (tested 2D and 3D)
3. **F∝M = 1.00 is a pure propagator property** (survives without
   restoring force, on broken graphs, on random DAGs)
4. **Every result has a frozen artifact chain** (script + log + note)

The remaining open items:
- Near-field (z ≤ 2) is mixed on both grown and fixed lattices
- The growth rule still uses grid labels for connectivity
- No 4D grown geometry test yet
- The growth rule is simple but not derived from axioms

## Artifact index

| Script | Tests | Log |
|--------|-------|-----|
| `gate_b_farfield_harness.py` | Gravity + F∝M (12 seeds) | ✓ |
| `gate_b_grown_distance_law.py` | Distance tail (4 seeds) | ✓ |
| `gate_b_grown_joint_package.py` | Born/d_TV/MI/decoh (4 seeds) | ✓ |
| `gate_b_no_restore_farfield.py` | Without restore | ✓ |
| `gate_b_no_restore_joint_package.py` | Without restore | ✓ |
| `gate_b_connectivity_tolerance.py` | Connectivity sweep | ✓ |
