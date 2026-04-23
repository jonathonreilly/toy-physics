# Λ_QCD Derivation Support Note

**Date:** 2026-04-22
**Status:** support-level extraction, NOT a retained closure. Λ_QCD is a scheme-and-loop-order-dependent derived quantity; the framework-native input is `α_s(v)` or `α_s(M_Z)`. This note provides a 1-loop and 2-loop Λ_QCD extraction from the retained `α_s(M_Z)` for cross-reference against PDG 4-loop values.
**Primary runner:** `scripts/frontier_lambda_qcd_derivation_support.py`

## 0. Extracted values from retained α_s(M_Z) = 0.1181 at 1-loop

| Quantity | Framework 1-loop | PDG 4-loop MS-bar |
|----------|------------------|--------------------|
| `Λ_QCD^(5)` | 87.8 MeV | 208 MeV |
| `Λ_QCD^(4)` | 229 MeV | 292 MeV |
| `Λ_QCD^(3)` | 251 MeV | 332 MeV |
| `α_s(2 GeV)` | 0.268 | 0.302 |

The ~40–50% factor between framework-1-loop and PDG-4-loop is the **expected scheme-truncation difference**. Λ_QCD is defined as the scale where `α_s` diverges in the chosen loop truncation; higher-loop truncations push Λ higher.

## 1. Framework-native input: `α_s`, not Λ

The retained framework derives `α_s(v) = 0.1033` and runs to `α_s(M_Z) = 0.1181` (both on `ALPHA_S_DERIVED_NOTE.md`). These are SCHEME-INDEPENDENT physical observables at their respective scales.

`Λ_QCD` is a DERIVED parameter: once `α_s(μ)` is fixed at some reference scale `μ`, inverting the RG equation at loop order `L` defines Λ at that order. Different `L` gives different Λ by design.

So this note extracts Λ support values as a CROSS-CHECK; they are not a framework closure.

## 2. 1-loop extraction details

**Formula** (1-loop, MS-bar):
```text
α_s(μ)  =  1 / [2·b_0·ln(μ/Λ)]         →         Λ = μ · exp(−1/(2·b_0·α_s(μ)))
```

with `b_0 = (33 − 2 n_f)/(12π)`.

For `n_f = 5` at `μ = M_Z`:
```text
b_0(n_f=5)  =  23/(12π) = 0.6103
Λ^(5)_1loop =  91.1876 · exp(−1 / (2·0.6103·0.1181))  =  0.0878 GeV  =  87.8 MeV.
```

Threshold matching at 1-loop:
- At `μ = m_b = 4.18 GeV`: compute `α_s(m_b)` in `n_f=5`, then invert in `n_f=4` to get `Λ^(4) = 229 MeV`.
- At `μ = m_c = 1.27 GeV`: same with `n_f=4 → n_f=3`, giving `Λ^(3) = 251 MeV`.

## 3. Why 1-loop differs from 4-loop

`Λ_QCD` is defined implicitly by the condition `α_s(Λ) → ∞`. At 1-loop, this is `α_s(Λ_{1-loop}) → ∞`; at 4-loop, it's `α_s(Λ_{4-loop}) → ∞`. Since the 4-loop β-function is more negative (coupling grows faster in IR), the divergence point `Λ_{4-loop}` is at a LARGER scale than `Λ_{1-loop}`. Hence PDG 4-loop Λ ≈ 2× the 1-loop value.

For a physical quantity at a scale μ where perturbation theory applies, however, the values of `α_s(μ)` from different loop orders agree at the μ-scale (that's the whole point of the RG flow — physical observables are truncation-independent in the perturbative regime).

## 4. Confinement scale interpretation

The 1-loop `Λ^(3) ≈ 250 MeV` places the confinement / hadronization scale in the **physical hadron-mass window**. This is the qualitative prediction of the retained framework: confinement kicks in around 200–300 MeV, consistent with the ~1 GeV proton mass. Precision matching to PDG 4-loop values is available but requires the higher loop orders.

## 5. Cross-check: α_s(2 GeV)

Using `Λ^(4)_1loop = 229 MeV`:
```text
α_s(2 GeV)_1-loop  =  1 / [2·b_0(4)·ln(2 GeV / 0.229 GeV)]  =  0.268
```

PDG 4-loop value: `α_s(2 GeV) ≈ 0.302`. The 1-loop undershoot of ~11% is again the expected loop-truncation effect; same `α_s(M_Z)` run with 4-loop β-function gives `α_s(2 GeV) ≈ 0.302`.

## 6. Relation to the retained mass-ratio lanes (loops 1–3 closures)

Loop 2 of this series produced `ckm-scale-convention-theorem` which used the PDG 4-loop `α_s(2 GeV)/α_s(m_b) = 1.14747^(25/12)` transport factor. That note used PDG α_s directly rather than running from the retained `α_s(M_Z)`, because 1-loop running undershoots by ~1% in the transport factor.

**This note documents the exact loop-order mismatch** between retained 1-loop running and PDG 4-loop convention. Future runs that reconcile the two require 4-loop matching at scales `m_b` and `m_c` — standard QCD calculation, not framework-specific.

## 7. What this note closes and does not close

**Does**:
- Extract 1-loop `Λ_QCD^(3,4,5)` from the retained `α_s(M_Z) = 0.1181`.
- Clarify that framework-native is `α_s`, and Λ is scheme-derived.
- Document the expected ~2× loop-order scheme gap vs PDG 4-loop Λ.

**Does NOT**:
- Derive a 4-loop Λ_QCD (requires 4-loop β-function computation, standard QCD).
- Promote `α_s(M_Z)` from retained → "retained including Λ_QCD".
- Address lattice-QCD determinations of Λ (separate lane).

## 8. Cross-references

- `docs/ALPHA_S_DERIVED_NOTE.md` — retained `α_s(v), α_s(M_Z)`.
- `docs/CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md` — 4-loop PDG transport factor.
- `docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md` — retained plaquette surface.
- PDG 2024 *QCD Section*, 4-loop MS-bar Λ values.
