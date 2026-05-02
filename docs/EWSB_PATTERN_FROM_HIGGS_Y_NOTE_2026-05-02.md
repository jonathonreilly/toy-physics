# Electroweak Symmetry Breaking Pattern from Higgs Y_H = +1

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on retained
graph-first surface + cycle 15 (Y_H = +1) + standard SU(2) Lie algebra.
NOT proposed_retained — see CLAIM_STATUS_CERTIFICATE.md.
**Primary runner:** `scripts/frontier_ewsb_pattern_from_higgs_y.py`
**Authority role:** exact-support theorem deriving the unbroken
electromagnetic charge `Q = T_3 + Y/2` from the Higgs VEV and `Y_H = +1`.

## 0. Statement

**Theorem (EWSB pattern Q = T_3 + Y/2 from Y_H = +1).**

Given:
1. Higgs in `(1, 2)_{Y=+1}` representation under SU(3) × SU(2)_L × U(1)_Y
   (cycle 15, PR #278);
2. Higgs VEV in the **neutral** component (T_3 = −1/2 for the lower
   doublet entry):
   ```
   ⟨H⟩ = (0, v/√2)^T
   ```
3. SU(2)_L generators T_a (a=1,2,3) with `T_a = σ_a/2` (Pauli matrices/2);
4. U(1)_Y generator with charge Y_H = +1 acting as `Y · H = +1 · H`;

then the **unbroken** generator is the linear combination

```text
Q  =  T_3  +  Y/2
```

(the SM electromagnetic charge formula on SU(2) doublets), i.e. the unique
combination satisfying `Q · ⟨H⟩ = 0`.

**Proof.** Acting on `⟨H⟩ = (0, v/√2)^T`:

```text
T_3 · ⟨H⟩  =  (σ_3/2) · (0, v/√2)^T
             =  (1/2)·diag(+1, −1) · (0, v/√2)^T
             =  (0, −v/(2√2))^T
             =  −(1/2) · ⟨H⟩

Y · ⟨H⟩    =  Y_H · ⟨H⟩  =  +1 · ⟨H⟩
```

Therefore:

```text
(T_3 + α·Y) · ⟨H⟩  =  (−1/2 + α) · ⟨H⟩
```

Setting this to zero (annihilating the VEV, hence "unbroken"):

```text
α  =  +1/2.
```

So the unbroken U(1) generator is `T_3 + (1/2) · Y`, equivalently
`Q = T_3 + Y/2`. ∎

## 1. Three broken generators

The other three generators of SU(2)_L × U(1)_Y are broken by ⟨H⟩:

```text
T_1 · ⟨H⟩  =  (σ_1/2) · (0, v/√2)^T
             =  (v/(2√2), 0)^T  ≠ 0     [broken]

T_2 · ⟨H⟩  =  (σ_2/2) · (0, v/√2)^T
             =  (−i v/(2√2), 0)^T  ≠ 0  [broken]

(T_3 − Y/2) · ⟨H⟩  =  (−1/2 − 1/2) · ⟨H⟩  =  −⟨H⟩  ≠ 0   [broken]
```

The combination `Z = T_3 − Y/2` (orthogonal to Q) is broken — this is
(modulo electroweak mixing) the Z-boson generator.

## 2. Electric charges of fermions reproduce SM

With `Q = T_3 + Y/2` acting on LHCM-derived hypercharges:

| Particle | T_3 | Y | Q |
|---|---|---|---|
| u_L | +1/2 | +1/3 | +1/2 + 1/6 = +2/3 ✓ |
| d_L | −1/2 | +1/3 | −1/2 + 1/6 = −1/3 ✓ |
| ν_L | +1/2 | −1   | +1/2 − 1/2 = 0 ✓ |
| e_L | −1/2 | −1   | −1/2 − 1/2 = −1 ✓ |
| u_R | 0    | +4/3 | +2/3 ✓ |
| d_R | 0    | −2/3 | −1/3 ✓ |
| e_R | 0    | −2   | −1 ✓ |
| ν_R | 0    | 0    | 0 ✓ |
| H+ | +1/2  | +1   | +1/2 + 1/2 = +1 ✓ |
| H0 | −1/2  | +1   | −1/2 + 1/2 = 0 ✓ (the VEV component) |

All 10 cases reproduce SM electric charges.

## 3. Retained / admitted inputs

| Ingredient | Class | Source |
|---|---|---|
| Higgs in (1, 2)_{Y=+1} | exact-support (cycle 15) | PR #278 |
| Higgs VEV in neutral T_3=−1/2 component | admitted SM convention | standard SSB |
| SU(2)_L Lie algebra T_a = σ_a/2 | standard | Pauli matrices |
| U(1)_Y action `Y · H = Y_H · H` | standard gauge action | SM |

## 4. What this closes

- **Q = T_3 + Y/2 derivation** as exact consequence of Y_H = +1
  (cycle 15) + standard SSB structure.
- **Three broken generators** explicitly identified.
- **All 10 SM particle electric charges** verified at exact Fraction
  precision.

## 5. What this does NOT close

- The Higgs potential `V(H†H) = −μ² H†H + λ(H†H)²` form (admitted SM convention).
- The VEV `v` magnitude (admitted external observable).
- The W/Z mass formulas (require Higgs kinetic term + EW mixing angle).
- The retention of cycle 15 / Y_H = +1 derivation (still depends on
  admitted SM Yukawa structure).

## 6. Status

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on cycle 15 (Y_H = +1) which is itself conditional on
  admitted SM Yukawa structure. Higgs VEV neutral-component admission
  is standard SSB convention, not derivation.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7. Cross-references

- Cycle 15 / PR [#278](https://github.com/jonathonreilly/cl3-lattice-framework/pull/278) — Higgs Y_H = +1 derivation
- Cycle 16 / PR [#279](https://github.com/jonathonreilly/cl3-lattice-framework/pull/279) — Tr[Y²] = 40/3 + SU(5) GUT
- Cycle 6 / PR [#262](https://github.com/jonathonreilly/cl3-lattice-framework/pull/262) — LHCM atlas
- LHCM closure trio: PRs [#254](https://github.com/jonathonreilly/cl3-lattice-framework/pull/254), [#255](https://github.com/jonathonreilly/cl3-lattice-framework/pull/255), [#256](https://github.com/jonathonreilly/cl3-lattice-framework/pull/256)
