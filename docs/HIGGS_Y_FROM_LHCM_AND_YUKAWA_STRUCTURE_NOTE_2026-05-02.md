# Higgs Y_H from LHCM-Derived Hypercharges and Yukawa Structure

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on retained
graph-first surface + LHCM closure trio (cycles 1-3) + Yukawa-structure
admitted SM convention. NOT proposed_retained — see
CLAIM_STATUS_CERTIFICATE.md.
**Primary runner:** `scripts/frontier_higgs_y_from_lhcm_yukawa.py`
**Authority role:** exact-support theorem extending the LHCM atlas
(cycle 6 / PR #262) to derive the Higgs Y assignment on the SM Yukawa
surface.

## 0. Statement

**Theorem (Higgs Y_H from LHCM and Yukawa structure).**

Given:
1. LHCM-derived LH content `Y(Q_L) = +1/3, Y(L_L) = −1` (cycles 2-3, modulo
   SM-definition convention `Q_e = −1`);
2. STANDARD_MODEL_HYPERCHARGE_UNIQUENESS-derived RH content
   `Y(u_R) = +4/3, Y(d_R) = −2/3, Y(e_R) = −2, Y(ν_R) = 0` (cycles 1-3 +
   SM hypercharge uniqueness theorem);
3. SM-structure Yukawa coupling pattern (admitted convention):
   - quark up Yukawa: `−y_u Q̄_L · H̃ · u_R + h.c.` with `H̃ = iσ²H*`
   - quark down Yukawa: `−y_d Q̄_L · H · d_R + h.c.`
   - lepton charged Yukawa: `−y_e L̄_L · H · e_R + h.c.`
   - (optional) lepton neutral Yukawa: `−y_ν L̄_L · H̃ · ν_R + h.c.`

then U(1)_Y invariance of the Yukawa terms forces the Higgs hypercharge:

```text
Y_H  =  +1   in conventional Y units (where Q = T_3 + Y/2).
```

**Proof.** From the up-quark Yukawa `Q̄_L · H̃ · u_R`:

```text
−Y(Q_L) − Y(H̃) − Y(u_R)  =  0           (Y of dagger field is negated)
```

Using `Y(H̃) = −Y(H)` (charge conjugation):

```text
Y(H)  =  Y(u_R) − Y(Q_L)
       =  +4/3 − 1/3
       =  +1.
```

From the down-quark Yukawa `Q̄_L · H · d_R`:

```text
Y(H)  =  Y(d_R) − Y(Q_L)
       =  −2/3 − 1/3
       =  −1.
```

These appear inconsistent — but recall `Q̄_L` is the conjugate. The down
Yukawa is `Q̄_L · H · d_R = (Q_L)† · H · d_R`. The hypercharge sum is
`−Y(Q_L) + Y(H) + Y(d_R) = 0`, giving `Y(H) = Y(Q_L) − Y(d_R) = 1/3 −
(−2/3) = +1`. ✓

So both quark Yukawas give `Y_H = +1` consistently.

From the charged-lepton Yukawa `L̄_L · H · e_R`:

```text
Y(H)  =  Y(L_L) − Y(e_R)
       =  −1 − (−2)
       =  +1.   ✓
```

All three SM Yukawa couplings consistently force `Y_H = +1`. The neutral
lepton Yukawa (`L̄_L · H̃ · ν_R`) gives:

```text
−Y(H̃) = Y(L_L) − Y(ν_R) − Y(H̃)  =  ⋯
+Y(H) =  Y(ν_R) − Y(L_L)
      =  0 − (−1) = +1.   ✓
```

Therefore `Y_H = +1` is **forced** by the LHCM-derived fermion content +
Yukawa-structure SM convention.

## 1. Retained / admitted inputs

| Ingredient | Class | Source |
|------------|-------|--------|
| LHCM-derived (Q_L, L_L) hypercharges (+1/3, −1) | exact-support (cycles 1-3 modulo SM convention) | Cycle 6 atlas (PR #262) |
| STANDARD_MODEL_HYPERCHARGE_UNIQUENESS RH content | proposed_retained, unaudited | parent theorem |
| SM Yukawa structural coupling form (Q̄_L H u_R, etc.) | admitted SM convention | Halzen-Martin SM textbook |

## 2. What this closes

- **Y_H = +1 derivation from LHCM atlas** as exact algebraic consequence
  modulo SM Yukawa coupling structural admission.
- **Cross-check consistency** across all three (or four) Yukawa couplings:
  up-quark, down-quark, charged-lepton, and neutral-lepton (when ν_R
  Yukawa exists). All three independent equations yield Y_H = +1.

## 3. What this does NOT close

- The SM Yukawa coupling form itself (admitted as standard SM convention)
- The retention of LHCM (still depends on SM-definition convention
  reclassification, see cycle 6 atlas)
- The retention of `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS` (still
  proposed_retained, unaudited)
- The Higgs VEV `v` value (admitted external)

## 4. Status

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
conditional_surface_status: |
  conditional on:
    - LHCM atlas (cycle 6, PR #262) modulo SM-definition conventions
    - SM hypercharge uniqueness theorem (proposed_retained, unaudited)
    - SM Yukawa coupling structural form (admitted SM convention)
proposal_allowed: false
proposal_allowed_reason: |
  Multiple admitted conditions remain (SM Yukawa form, LHCM SM-definition
  conventions). Honest tier is exact-support modulo these admissions.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 5. Validation

- primary runner:
  [`scripts/frontier_higgs_y_from_lhcm_yukawa.py`](../scripts/frontier_higgs_y_from_lhcm_yukawa.py)
  — verifies (a) all four Yukawa couplings give Y_H = +1 at exact rational
  precision, (b) cross-check consistency across the four couplings, (c)
  with conjugate field Y rules, (d) non-closure documentation.

## 6. Cross-references

- LHCM atlas: PR [#262](https://github.com/jonathonreilly/cl3-lattice-framework/pull/262) (cycle 6)
- LHCM closure trio: PRs [#254](https://github.com/jonathonreilly/cl3-lattice-framework/pull/254), [#255](https://github.com/jonathonreilly/cl3-lattice-framework/pull/255), [#256](https://github.com/jonathonreilly/cl3-lattice-framework/pull/256) (cycles 1-3)
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- Halzen-Martin SM Yukawa structure
