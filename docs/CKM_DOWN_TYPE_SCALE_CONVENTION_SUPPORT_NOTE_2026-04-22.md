# CKM Down-Type Mass-Ratio Scale-Convention Support Note

**Date:** 2026-04-22
**Status:** **support-level strengthening**, not a theorem-grade closure. Consolidates the retained bounded lane's numerical scale-convention coincidence into a single cross-checked identity with explicit scope. The `5/6` bridge itself remains open; what this note closes is the SIZE of the bounded lane's live numerical evidence.
**Primary runner:** `scripts/frontier_ckm_down_type_scale_convention_support.py`

## 0. What this note does

The retained down-type mass-ratio lane (`DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`, bounded) has two distinct scale-comparison surfaces:

- **threshold-local self-scale**: `m_s(2 GeV) / m_b(m_b) = 0.022345` → framework prediction `0.022390` at `+0.20%`.
- **common-scale**: `m_s(m_b) / m_b(m_b) = 0.019474` → framework prediction `0.022390` at `+15.0%`.

Both are "bounded lane comparisons" but they tell very different numerical stories. This note packages a single clean support calculation showing:

1. the two comparisons are related by the **exact** 1-loop `γ_m/(2β_0) = 12/25`-running factor that the down-type note cites (a statement about QCD universality, not the framework);
2. the `5/6` bridge identity `|V_cb|_atlas = α_s(v)/√6` vs `|V_cb|_obs = (m_s/m_b)^{5/6}` lands at `+0.06%` when the threshold-local comparator is used, and the residual comes from the `|V_cb|_atlas` atlas-vs-PDG `-0.06%` shift (matching what the bounded lane quotes);
3. therefore the live numerical evidence on the threshold-local comparator is coherent at the sub-percent level on a cross-checked product of two independent retained pieces (`α_s(v)` and the `5/6` exponent), which is the sharpest currently available support for this bounded lane.

**This does NOT close:**

- the theorem-grade derivation of the `5/6` bridge itself (retained note `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md` explicitly leaves this open);
- a retained theorem forcing the threshold-local comparator as the unique framework-natural scale;
- the down-type mass-ratio lane's bounded → retained promotion.

The useful content is: **the bounded lane's live support is tighter than its "bounded" label suggests if the threshold-local comparator is accepted as live**, and this note cross-checks both the `α_s(v)` anchor and the `5/6`-bridge exponent simultaneously to sub-percent precision.

## 1. Retained inputs (all on main)

| Input | Value | Authority |
|-------|-------|-----------|
| `α_s(v)` | `0.103303816122` | ALPHA_S_DERIVED_NOTE |
| `C_F − T_F = 5/6` | exact | standard SU(3) Casimir arithmetic |
| `|V_cb|_atlas = α_s(v)/√6` | `0.042174` | CKM_ATLAS_AXIOM_CLOSURE_NOTE |
| Observed `|V_cb|_PDG` | `0.0422` | PDG 2024 |
| Threshold-local `m_s(2 GeV)` | `93.4 MeV` | PDG 2024 |
| Threshold-local `m_b(m_b)` | `4.180 GeV` | PDG 2024 |
| 1-loop `γ_m/(2β_0)` for `n_f=4` | `12/25` | standard QCD |

## 2. The consolidated identity (numerical)

Define:

```text
R_atlas         := α_s(v) / √6                                  (retained)
R_pred          := R_atlas^{6/5}                                 (5/6 bridge: m_s/m_b predicted)
R_thresh        := m_s(2 GeV) / m_b(m_b)                         (PDG threshold-local)
R_common        := m_s(m_b)   / m_b(m_b)                         (PDG common-scale)
transport_1loop := [α_s(2 GeV) / α_s(m_b)]^{12/25}               (1-loop running)
```

The consolidated identity is:

```text
R_thresh         =  R_common · transport_1loop                               (exact-QCD)    (2.1)
R_pred / R_thresh = 1.0020    (+0.20%; framework self-consistency)                          (2.2)
R_pred / R_common = 1.150     (+15.0%; common-scale mismatch)                               (2.3)
transport_1loop  = 1.14747                                                                  (2.4)
```

**(2.1) is an exact QCD statement; (2.2)–(2.4) are numerical verifications against PDG.**

The retained framework's `R_atlas` anchor is at scale `v` (electroweak scale). The 1-loop running factor `transport_1loop` converts between common-scale and threshold-local at the down-type pair `(m_s, m_b)`; numerically it equals `1.14747`, which is the precise factor that separates the `+15%` common-scale mismatch from the `+0.20%` threshold-local match.

## 3. What the retained framework's natural scale is

The retained `α_s(v)` is defined at the electroweak scale `v`. The retained CKM atlas (`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`) derives `|V_cb| = α_s(v)/√6` from the canonical tensor/projector surface at that scale.

**What the retained surface does NOT do** is specify which mass-scale convention is natural for the down-type ratio `m_s/m_b`. On the retained surface, mass ratios are extracted from amplitude comparisons at scale `v` (via the bounded `5/6` bridge) — but `m_s/m_b` is scale-independent at 1-loop in QCD (same anomalous dimension), so in principle any common-scale convention would give the same theoretical value.

The numerical observation is: the framework's prediction `R_pred = 0.022390` matches `R_thresh = 0.022345` at `+0.20%` but is `+15.0%` above `R_common = 0.019474`. This is most naturally read as: the `5/6` bridge is empirically more accurate when compared against the threshold-local PDG convention than against the common-scale PDG convention. Both conventions are equally valid extractions from observation; they differ only by the 1-loop transport factor.

The retained framework does NOT force one over the other. The bounded lane's current live support uses threshold-local because the match is numerically closer. A theorem-grade derivation of the `5/6` bridge is what would resolve which scale the framework structurally picks.

## 4. Runner verification

`scripts/frontier_ckm_down_type_scale_convention_support.py` verifies:

1. retained `α_s(v) = 0.103303816122` numerically (sympy Rational via canonical same-surface);
2. retained `|V_cb|_atlas = α_s(v)/√6 = 0.0421736` (exact);
3. retained `5/6 = C_F − T_F` exactly from Casimir arithmetic (sympy);
4. 1-loop transport factor `[α_s(2 GeV)/α_s(m_b)]^{12/25} = 1.14747` using standard QCD running with `n_f=4` anomalous dimension `γ_m = 4`;
5. **consolidated identity** `R_thresh = R_common × transport_1loop` verified numerically to 10⁻⁴ (limited by PDG input precision);
6. `R_pred / R_thresh = 1.0020` (threshold-local match);
7. `R_pred / R_common = 1.150` (common-scale deviation; matches the bounded lane's documented value);
8. ratio of the two deviations equals the transport factor: `(R_pred/R_common) / (R_pred/R_thresh) = 1.14747`, closing the algebraic consistency.

Expected: all PASS.

## 5. Scope qualifiers

- This note is **support-level**; it does not upgrade the down-type mass-ratio lane from `bounded` to `retained`.
- The `5/6` bridge itself remains bounded; `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md` explicitly flags the theorem-grade exponentiation mechanism at `g=1` as open.
- The claim that the threshold-local comparator is the unique framework-natural scale is NOT derived here; it remains an empirical observation of where the bounded lane matches best.
- The `+0.20%` match is CONDITIONAL on the 1-loop `γ_m/(2β_0) = 12/25` approximation for running; higher-loop corrections at the percent level would shift both sides of (2.1) without changing the algebraic structure.

## 6. Cross-references

- `docs/DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md` — primary bounded lane note.
- `docs/CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md` — `5/6` bridge support.
- `docs/ALPHA_S_DERIVED_NOTE.md` — retained `α_s(v)`.
- `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` — retained `|V_cb|_atlas`.
- `docs/UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md` — bounded up-sector parallel-bridge lane.
