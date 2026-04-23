# Tritium Beta-Decay Effective Mass m_β Prediction

**Date:** 2026-04-22
**Status:** derived numerical prediction `m_β = 9.86 meV` on the retained neutrino-mass surface plus PDG 2024 PMNS mixing angles. Falsifiable by Project-8-class atomic tritium spectroscopy.
**Primary runner:** `scripts/frontier_tritium_beta_mass_prediction.py`

## 0. Framework prediction

**`m_β ≈ 9.86 meV`** (single-valued; Majorana-phase-independent).

| Experiment | Sensitivity | Framework prediction as % |
|------------|-------------|---------------------------|
| KATRIN 2022 bound | `m_β < 800 meV` (90% CL) | 1.23% of bound |
| KATRIN final target | `m_β < 200 meV` | 4.9% of target |
| Project 8 (atomic tritium) | `~40 meV` | 24.7% of target |

**Falsifiable**: a detection of `m_β > ~15 meV` by any β-decay experiment would rule out the retained light-neutrino chain (`m_1 ≈ 4.4 meV` + PDG PMNS NO + observable-corrected `m_2`).

## 1. Chain

From `docs/NEUTRINO_MASS_SUM_PREDICTION_NOTE_2026-04-22.md` (Part B):

```text
m_1 ≈  4.37 meV    (retained, M_3 = M_Pl · α_LM^7)
m_2 ≈  9.71 meV    (corrected via observed Δm²_21)
m_3 ≈ 50.4  meV    (retained, atmospheric)
```

From PDG 2024 NO PMNS:

```text
|U_e1|² = cos²θ_12·cos²θ_13 ≈ 0.6752
|U_e2|² = sin²θ_12·cos²θ_13 ≈ 0.3001
|U_e3|² = sin²θ_13           ≈ 0.0224
```

## 2. m_β from incoherent sum

Unlike m_ββ (which depends on unknown Majorana phases), the tritium β-decay endpoint observable is

```text
m_β²  =  Σ_i |U_ei|² · m_i²                                             (1)
```

(an incoherent sum of probabilities × squared masses). Substituting:

```text
m_β²  =  0.6752·(4.37)²  +  0.3001·(9.71)²  +  0.0224·(50.4)²    meV²
      =  12.89          +  28.30            +  56.96             meV²
      =  98.14 meV²
m_β   =  √98.14 meV  =  9.86 meV                                        (2)
```

## 3. Structural observation

The contributions to `m_β²` from each mass eigenstate:

```text
|U_e1|² m_1² : |U_e2|² m_2² : |U_e3|² m_3²  =  13.1% : 28.8% : 58.0%
```

**The atmospheric mass `m_3` dominates `m_β²` at 58%**, despite its small PMNS weight `|U_e3|² = 0.022`. This is because `m_3² / m_1² ≈ 130×`, so even the small `|U_e3|²` suppression cannot undo the atmospheric-scale enhancement.

Structurally, the retained framework's `m_β` is primarily a measurement of `√(|U_e3|²·m_3²)`, modulated by the `m_1, m_2` tails.

## 4. Comparison with NO minimum (lightest = 0)

For comparison, the NO absolute minimum with `m_1 → 0` is:

```text
m_β(NO, min)  =  √(|U_e2|² · Δm²_21 + |U_e3|² · Δm²_31)
             =  √(0.300·(7.41e-5) + 0.022·(2.505e-3))
             ≈  8.90 meV
```

The retained framework prediction (`9.86 meV`) is only `1.0 meV` above this NO minimum. This places the framework at the **lowest end** of the NO-accessible `m_β` range, consistent with the retained `m_1 ≈ 4.4 meV` being small.

## 5. Experimental outlook

- **KATRIN 2022** (`m_β < 800 meV`): framework is `1.23%` of the bound — not currently constraining.
- **KATRIN final** (projected `m_β < 200 meV`): framework is `5%` of target — non-detection consistent.
- **Project 8 atomic tritium** (projected `~40 meV`): framework is `25%` of target — non-detection still consistent, but approaching the edge.
- **Far future atomic tritium / spin-selective spectroscopy** (`~10 meV` reach projected): framework directly accessible — a detection at `~10 meV` would strongly support the retained neutrino chain.

The `m_β ≈ 10 meV` value sits in a scientifically interesting zone: above the NO minimum (8.9 meV) but below current experimental reach. Future decades of atomic β-decay work could probe this regime.

## 6. Three-observable fingerprint (cross-reference to loops 5 and 6)

Combining with the companion predictions:

| Observable | Retained framework value | Experimental target |
|------------|--------------------------|--------------------|
| `Σm_ν` (cosmology) | 64.5 meV (Part B) | Planck 2018: < 120 meV; DESI 2024: < 72 meV |
| `m_β` (tritium, **this note**) | 9.86 meV | KATRIN: < 200 meV; Project 8: ~40 meV |
| `m_ββ` (0ν double-beta) | [0, 7] meV (Majorana phases) | Legend-1000: ~17 meV; nEXO: ~7-15 meV |

The three observables **form a coherent fingerprint** of the retained light-neutrino chain:

- `Σm_ν` directly below current bounds, in tension with DESI at Part-A-level.
- `m_β` directly below current bounds, accessible only to far-future atomic β-decay.
- `m_ββ` partial cancellation, accessible to nEXO.

A *combined* non-detection across all three channels is **consistent**. A detection in *any one* channel at odds with the above numerical values would falsify the retained m_i.

## 7. What this note does and does not close

**Does**:
- Derive a single-valued numerical `m_β` prediction on the retained neutrino surface + PDG PMNS NO.
- Expose the structural origin of `m_β` as atmospheric-scale dominated.
- Provide the third leg of the three-observable retained neutrino fingerprint.

**Does NOT**:
- Close the retained solar-gap lane (`m_2` still observable-corrected).
- Derive PDG PMNS angles from the retained core (PMNS chamber-pin lane still bounded).
- Address the retained "M_R currently zero" surface (where light neutrinos are Dirac and `m_β` via the same formula).

## 8. Cross-references

- `docs/NEUTRINO_MASS_SUM_PREDICTION_NOTE_2026-04-22.md` — retained m_i values.
- `docs/NEUTRINOLESS_DOUBLE_BETA_MBB_PREDICTION_NOTE_2026-04-22.md` — m_ββ companion.
- `docs/NEUTRINO_MASS_DERIVED_NOTE.md` — retained chain.
- `docs/PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md` — PMNS chamber-pin lane.
- KATRIN Collaboration, *Direct neutrino-mass measurement with sub-electronvolt sensitivity*, Nature Phys. 18 (2022) 160.
- Project 8 Collaboration, *Atomic-tritium beta-decay spectroscopy*, PRC 103 (2021) 065501.
