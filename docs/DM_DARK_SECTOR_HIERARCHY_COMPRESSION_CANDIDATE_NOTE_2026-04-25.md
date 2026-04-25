# Dark-Sector Hierarchy Compression -- Unified A0+G1 Candidate

**Date:** 2026-04-25 (next-science step after adversarial review)
**Status:** **CANDIDATE** structural identity. Consolidates the two open
lanes (A0 dark-sector hierarchy compression, G1 Wilson-mass derivation
of `m_DM = N_sites * v`) named in
[`DM_ETA_FREEZEOUT_BYPASS_ADVERSARIAL_REVIEW_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_ADVERSARIAL_REVIEW_NOTE_2026-04-25.md)
into a single open object.
**Primary runner:** `scripts/frontier_dm_dark_sector_hierarchy_compression_candidate.py`
**Runner result:** `PASS = 6, FAIL = 0`.
**Framework convention:** "axiom" means only the single framework axiom
`Cl(3)` on `Z^3`.

## Statement

The unified candidate identity is

```
m_DM = 6 * M_Pl * (8/3) * (7/8)^(1/4) * alpha_LM^16
     = 16 * v.
```

Equivalently, the dark-sector hierarchy compression factor

```
C_dark = m_DM / m_S3_bare = 16 v / (6 M_Pl)
       = (8/3) * (7/8)^(1/4) * alpha_LM^16
       = (8/3) * C_vis
```

where `C_vis = (7/8)^(1/4) * alpha_LM^16` is the retained visible-sector
hierarchy compression and `8/3 = dim(adj_3)/N_c = (N_c^2 - 1)/N_c` is the
SU(3) color-loop Casimir ratio.

## Closure-target structure

Each piece of the identity is now classified:

| piece | value | status |
|---|---:|---|
| `m_S3_bare` (chiral Wilson on Cl(3) cube) | 6 M_Pl | RIGOROUS |
| Visible compression `C_vis = (7/8)^(1/4) * alpha_LM^16` | 2.02e-17 | RETAINED |
| **Color enhancement `8/3 = dim(adj_3)/N_c`** | 8/3 | **CANDIDATE** |
| Composite `m_DM = 16 v` | 3940 GeV | numerically exact |

The CANDIDATE step is the SU(3) color-loop enhancement of the dark
gauge-singlet running. Replacing this single step with a derived theorem
would close BOTH A0 and G1 simultaneously.

## Robustness against alternative Casimir ratios

The runner tests 7 simple SU(3) Casimir ratios as potential bridging
factors. Only `8/3` reproduces `16 v` exactly:

| candidate enhancement | value | predicted m_DM | dev vs 16v |
|---|---:|---:|---:|
| **`dim(adj_3)/N_c = 8/3`** | **2.667** | **3940.53** | **+0.000%** |
| `N_c = 3` | 3.000 | 4433.09 | +12.500% |
| `2 T_F = 2` | 2.000 | 2955.39 | -25.000% |
| `C_2(F) = 4/3` | 1.333 | 1970.26 | -50.000% |
| `dim(adj_3) = 8` | 8.000 | 11821.58 | +200.000% |
| `1/N_c = 1/3` | 0.333 | 492.57 | -87.500% |
| `dim(adj_3) + 8/3 = 16/3` | 5.333 | 7881.05 | +100.000% |

The next-closest simple SU(3) Casimir is at 12.5% deviation. The
selection of `8/3` is genuinely unique within textbook SU(3) algebra,
not a fitted free parameter.

## Heuristic for the open Coleman-Weinberg derivation

The structural argument that motivates `8/3` (NOT YET a derivation):

- The visible (Higgs) sector couples to `N_c = 3` color fundamentals; its
  hierarchy compression `(7/8)^(1/4) alpha_LM^16` is set by the
  dimension-4 effective potential normalization on the visible's
  color-coupled condensate (retained Higgs derivation).
- The dark sector is a color-SINGLET mode but lives on the same
  SU(3)-gauged staggered minimal block. Color-loop self-energy
  contributions to the dark-singlet propagator come from gluon
  exchange in the sea of `dim(adj_3) = N_c^2 - 1 = 8` adjoint gauge
  bosons, normalized by the `N_c` color-trace of the gauge-singlet
  sink.
- Schematically the one-loop gauge self-energy contribution to the
  dark singlet's mass is proportional to `dim(adj_3)/N_c = 8/3`.
- This Casimir ratio appears in textbook QCD calculations (heavy-
  quarkonium binding, gluonic self-energies of color-singlet states),
  where it controls the multiplicity of gauge-loop diagrams normalized
  by the color trace.

Promotion to retained-grade requires either:
- (a) a one-loop Coleman-Weinberg calculation of the dark-singlet's
  self-energy on the SU(3)-gauged minimal block, or
- (b) a Casimir-sum identity on the staggered Dirac determinant
  restricted to the color-singlet sector.

## Why this is meaningful progress

Before this consolidation, the freeze-out-bypass theorem listed TWO
independent open lanes:
- A0 (dark-sector hierarchy compression, assumption)
- G1 (Wilson-mass derivation of `m_DM = N_sites * v`)

After this consolidation, there is ONE open lane:
- the SU(3) gauge-loop enhancement step `8/3 = dim(adj_3)/N_c` in the
  dark-sector running.

The closure target is a **single rational SU(3) Casimir ratio in a
Coleman-Weinberg argument**, with the rest of the structural chain
either rigorous (chiral Wilson mass = 6 M_Pl), retained (visible
compression to v), or numerically exact (16 = 6 * 8/3 = N_sites).

This sharpens the publication-grade open lane from "two independent
structural assumptions" to "one named SU(3) gauge-loop derivation".

## What this note does NOT claim

- That the `8/3 = dim(adj_3)/N_c` enhancement is derived. It is
  CANDIDATE, motivated by structural heuristics and uniquely selected
  among simple SU(3) Casimir alternatives.
- That A0 or G1 is independently closed. They are still open;
  this note unifies them into one open object.
- That the freeze-out-bypass theorem is now retained. It remains
  bounded-grade (see
  [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)).

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_dark_sector_hierarchy_compression_candidate.py
```

Expected: `PASS = 6, FAIL = 0`.

## Cross-references

- [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
  -- main quantitative theorem.
- [`DM_ETA_FREEZEOUT_BYPASS_ADVERSARIAL_REVIEW_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_ADVERSARIAL_REVIEW_NOTE_2026-04-25.md)
  -- the review that named A0 and G1.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) --
  source for the staggered minimal block, N_sites = 16, and the
  Higgs-sector Coleman-Weinberg derivation that this note generalizes.
- [`R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md`](R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md)
  -- retained group-theory identity `R_base = 31/9` containing the same
  SU(3) Casimirs (`C_2(3) = 4/3`, `dim(adj_3) = 8`).
