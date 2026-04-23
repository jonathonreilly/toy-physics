# Neutrinoless Double-Beta Effective Majorana Mass m_ββ Prediction

**Date:** 2026-04-22
**Status:** derived m_ββ window prediction on the retained neutrino-chain surface plus PDG PMNS mixing angles. Testable by Legend-1000 / nEXO.
**Primary runner:** `scripts/frontier_neutrinoless_double_beta_mbb_prediction.py`

## 0. Framework prediction

**Retained prediction**: `m_ββ ∈ [0.00, 6.96] meV` on the retained light-neutrino masses + PDG 2024 PMNS mixing angles, with the specific value within this window depending on the (currently unknown) Majorana phases.

- **Below current KamLAND-Zen 2022 bound** `m_ββ < 28–122 meV` (nuclear matrix-element uncertainty) — current experiments are not constraining.
- **Below Legend-1000 projected reach** `~17 meV` — non-detection at Legend-1000 would be consistent with the retained chain.
- **Within nEXO projected reach** `~7–15 meV` — a detection at nEXO near 7 meV would be consistent with Majorana phases aligned constructively; non-detection below ~7 meV still compatible with cancellation-region phases.

## 1. Chain from the retained framework

From `docs/NEUTRINO_MASS_SUM_PREDICTION_NOTE_2026-04-22.md` (Part B, observable-corrected):

```text
m_1 ≈  4.37 meV   (retained, from M_3 = M_Pl · α_LM^7)
m_2 ≈  9.71 meV   (corrected via observed Δm²_21)
m_3 ≈ 50.4  meV   (retained, atmospheric)
```

With PDG 2024 PMNS mixing angles (NO best fit):

```text
sin²θ_12 = 0.307      →  |U_e1|² = cos²θ_12·cos²θ_13 = 0.6752
sin²θ_13 = 0.02241    →  |U_e2|² = sin²θ_12·cos²θ_13 = 0.3001
sin²θ_23 = 0.553      →  |U_e3|² = sin²θ_13           = 0.02241
```

The effective Majorana mass is

```text
m_ββ  =  | Σ_i |U_ei|² · m_i · e^{iα_i} |                       (1)
```

with Majorana phases α_i ∈ [0, 2π) not derived on the retained surface.

## 2. Window evaluation

**Maximum (constructive)**:
```text
m_ββ_max = |U_e1|²·m_1 + |U_e2|²·m_2 + |U_e3|²·m_3
         = 0.6752·(4.37) + 0.3001·(9.71) + 0.02241·(50.4) meV
         = 2.95 + 2.92 + 1.13 meV
         = 6.96 meV
```

**Minimum (destructive / triangle inequality)**:
```text
m_ββ_min = max(0, largest_term − sum_of_others_terms)
         = max(0, 2.95 − (2.92 + 1.13))
         = max(0, −1.10)
         = 0.00 meV
```

The three signed contributions (2.95, 2.92, 1.13 meV) satisfy the triangle inequality — any one term is less than the sum of the other two — so **full cancellation is possible**. This places the retained m_1 = 4.37 meV squarely in the "NO cancellation funnel" region where m_ββ can dip to zero for specific Majorana-phase choices.

## 3. Experimental status and falsifiability

| Experiment | Sensitivity (meV) | Framework m_ββ ≈ 0–7 meV |
|------------|-------------------|--------------------------|
| KamLAND-Zen 2022 (current) | 28–122 | **not constraining** (below bound 4–17×) |
| Legend-200 (running) | ~30 | below |
| Legend-1000 (~2030) | ~17 | below |
| nEXO (~2030) | ~7–15 | **within reach** — detection at 7 meV consistent, non-detection also consistent |

**Falsifiable predictions**:

- A *detection* of `m_ββ > 7 meV` would **rule out** the retained m_i chain plus NO + PDG PMNS (either the framework's m_i is wrong, ordering is IO, or PMNS needs revision).
- A *non-detection* at Legend-1000 / nEXO levels is consistent with the retained chain (via destructive Majorana phases).
- A *detection* at `m_ββ ≈ 5–7 meV` would be a strong positive indication of the retained m_i + near-constructive phases.

## 4. Structural interpretation

The retained framework's neutrino chain places `m_1 ≈ 4 meV` in a **specific position** within the allowed NO mass spectrum — not at the `m_lightest = 0` corner (where the `m_ββ` NO funnel dips as low as ~1.5 meV), nor at the near-degenerate regime (where `m_ββ` ~ 10–50 meV). The retained `m_1` value is characteristic: `m_1 = α_LM · m_3` up to minor corrections, where `α_LM ≈ 0.091`.

Because `m_1 / m_3 ≈ 0.09`, the two larger PMNS-squared contributions `|U_e1|² m_1 ≈ 2.95 meV` and `|U_e2|² m_2 ≈ 2.92 meV` happen to be nearly equal in magnitude. This is a structural consequence of the retained chain, not a tuning.

## 5. What this note closes and does not close

**Closes**:
- A concrete numerical window for the effective Majorana mass m_ββ on the retained light-neutrino surface.
- Explicit identification of the retained m_1 position within the NO cancellation funnel.
- Falsifiable experimental prediction.

**Does NOT close**:
- The specific m_ββ value within the window (depends on Majorana phases α_i; no retained-framework derivation).
- The retained "M_R currently zero" surface on which m_ββ vanishes trivially — this note operates on the bounded Majorana-seesaw surface with admitted Higgs/CW EW lane.
- The retained solar-gap lane (Δm²_21 still open; m_2 used here is observable-corrected).

## 6. Cross-references

- `docs/NEUTRINO_MASS_SUM_PREDICTION_NOTE_2026-04-22.md` — retained m_i values.
- `docs/NEUTRINO_MASS_DERIVED_NOTE.md` — retained neutrino-mass chain.
- `docs/NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` — M_R currently zero surface.
- `docs/NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE.md` — ε/B = α_LM/2.
- PDG 2024 for PMNS mixing angles; NuFit 5.3 consistent values.
- KamLAND-Zen Collaboration, *Search for Majorana Neutrinos near the Inverted Mass Hierarchy Region with KamLAND-Zen*, Phys. Rev. Lett. 130 (2023) 051801.
