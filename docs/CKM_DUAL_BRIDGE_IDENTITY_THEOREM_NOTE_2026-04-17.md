# CKM-Dual Bridge Identity Theorem

**Date:** 2026-04-17
**Status:** retained structural theorem for the GST and `5/6` bridge exponents; bounded quantitative mass-ratio readout remains controlled by the current mass-hierarchy surface
**Primary runner:** `scripts/frontier_ckm_dual_bridge_identity.py`
**Authority role:** structural bridge-identity authority for the down-type
CKM-dual mass-ratio lane. Replaces the naked `5/6 = C_F - T_F` Casimir
coincidence as the retained origin of the bridge exponents.

## Role

This note upgrades the down-type CKM-dual lane from "bounded with two
independently motivated bridge relations" to "retained structural bridge
identity plus bounded quantitative mass-ratio readout". It parallels the
confinement / `sqrt(sigma)` pattern: a retained structural theorem that fixes
the exponent structure exactly, alongside a bounded quantitative prediction
that still inherits the mass-hierarchy systematic.

The structural content now retained is:

- the `sqrt(6)` appearing in `|V_cb| = alpha_s(v)/sqrt(6)` and in the `5/6`
  bridge `|V_cb| = (m_s/m_b)^(5/6)` is the **same** retained framework
  constant as the Ward-identity Clebsch-Gordan `1/sqrt(N_c · N_iso)` on the
  left-handed quark block `Q_L = (2, 3)`;
- the `5/6` exponent in the bridge is the **retained** CP-odd
  orthogonal-complement weight on the same six-state quark block, equal to
  `1 - 1/6` where `1/6` is the exact center-excess scalar weight from the
  retained atlas projector split `6 = 1 + 5`;
- the bridge relations are **exact algebraic identities** on the retained
  identification surface
  `m_d/m_s := alpha_s(v)/2`, `m_s/m_b := [alpha_s(v)/sqrt(6)]^(6/5)`.

The bridge exponents are therefore no longer independent bridge parameters;
they are fixed by retained structural numbers of the framework. The
**quantitative** match to PDG threshold-local self-scale comparators
(`+3.3%` for `m_d/m_s`, `+0.2%` for `m_s/m_b`) is the downstream bounded
readout of this retained structural identity.

## Retained inputs

All structural constants used below are already retained or promoted:

1. **Ward-identity theorem** —
   [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](YT_WARD_IDENTITY_DERIVATION_THEOREM.md),
   `y_t(M_Pl) / g_s(M_Pl) = 1/sqrt(6) = 1/sqrt(N_c · N_iso)`. The `sqrt(6)`
   is the Clebsch-Gordan normalization of the unit-norm scalar singlet
   composite `H_unit = (1/sqrt(6)) Sigma ψ̄ψ` on the left-handed quark block
   `Q_L`. The Clebsch-Gordan is derived from `D9` (composite Higgs) and
   `D17` (scalar-uniqueness on `Q_L`) as canonical Hilbert-space
   normalization, with `Z^2 = N_c · N_iso = 6`.

2. **CKM atlas/axiom closure** —
   [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md),
   `|V_us| = sqrt(alpha_s(v)/2)`, `|V_cb| = alpha_s(v)/sqrt(6)`. The `2` is
   the residual color pair from the exact EWSB `1 + 2` split. The `6` is
   the exact left-handed quark-block dimension `n_quark = n_pair · n_color
   = 2 · 3`, the same `6` as in the Ward theorem.

3. **Atlas `1 + 5` projector split on the quark block** — same atlas note.
   On the six-state quark block, the center-excess scalar CP-even weight is
   exactly
   `CENTER_EXCESS_WEIGHT = 1/n_quark = 1/6`,
   and the CP-odd orthogonal complement has weight
   `ORTHOGONAL_PHASE_WEIGHT = 1 - 1/6 = 5/6`.
   These are the projector weights that give `cos^2(delta_std) = 1/6` and
   `sin^2(delta_std) = 5/6` in the atlas closure.

4. **Canonical same-surface coupling** —
   [ALPHA_S_DERIVED_NOTE.md](ALPHA_S_DERIVED_NOTE.md),
   `alpha_s(v) = alpha_bare / u_0^2 = 0.103303816122` on the plaquette /
   CMT surface. This is the coupling used in both the CKM atlas and the
   down-type lane.

No additional axioms are used. No observed quark masses enter. The theorem
statement below is an exact algebraic identity on the retained surface
built from (1)-(4).

## Theorem statement

**Theorem (CKM-Dual Bridge Identity).** On the retained framework surface,
define the canonical down-type mass-ratio identification

```
    m_d/m_s := alpha_s(v) / 2                                       (I1)
    m_s/m_b := [ alpha_s(v) / sqrt(6) ]^(6/5)                       (I2)
```

where `2 = n_pair` is the residual color-pair count of the EWSB `1 + 2`
split and `6 = n_quark = n_pair · n_color` is the left-handed quark-block
dimension. Then on this identification surface the two bridge relations

```
    (GST)       |V_us|_atlas = sqrt( m_d/m_s )                      (T1)
    (5/6)       |V_cb|_atlas = ( m_s/m_b )^(5/6)                    (T2)
```

hold **exactly**. The exponent `1/2` in (T1) is `1/n_pair`, the exponent
`5/6` in (T2) is the orthogonal-complement projector weight on the
six-state quark block. Both are retained framework constants, not free
bridge parameters.

Furthermore:

- the `sqrt(6)` in `|V_cb|_atlas = alpha_s(v)/sqrt(6)` is the **same**
  retained framework constant as the Ward-theorem Clebsch-Gordan
  `1/sqrt(N_c · N_iso)` on `Q_L`;
- the `5/6` in (T2) is the retained orthogonal-complement projector weight
  on the **same** six-state quark block `Q_L`;
- the `2` in (I1) is the retained EWSB residual color pair count and the
  `1/2` exponent in (T1) is the atlas `n_pair` structural count.

No Nearest-Neighbor Interaction (NNI) texture assumption is used. No ad-hoc
exponentiation mechanism is used. The theorem fixes the bridge exponents
**from retained framework structure**.

## Proof

### 1. The two `sqrt(6)` factors are the same framework constant

The Ward-identity theorem derives the composite-Higgs Clebsch-Gordan

```
    Z^2 = N_c · N_iso = 3 · 2 = 6
```

from `D17` (unique scalar singlet on `Q_L`). This makes
`1/sqrt(6) = 1/sqrt(N_c · N_iso) = 1/sqrt(dim(Q_L))` the canonical
unit-norm normalization of `H_unit` on `Q_L`.

The CKM atlas derives

```
    |V_cb|_atlas = A * lambda_w^2 = sqrt(n_pair/n_color) * (alpha_s(v)/n_pair)
                 = alpha_s(v)/sqrt(n_pair · n_color)
                 = alpha_s(v)/sqrt(n_quark)
                 = alpha_s(v)/sqrt(6)
```

from the same structural count `n_quark = n_pair · n_color = dim(Q_L)`.

Both `sqrt(6)` factors therefore come from the retained structural count
`dim(Q_L) = N_c · N_iso = 6`. They are the same framework constant.

### 2. The `5/6` in (T2) is the retained orthogonal-complement weight

On the six-state quark block, the atlas projector decomposition gives

```
    6 = 1 + 5
```

with the `1`-dimensional factor being the CP-even singlet center-excess
direction and the `5`-dimensional factor being its orthogonal complement.
The corresponding normalized weights are

```
    CENTER_EXCESS_WEIGHT        = 1/6         (CP-even)
    ORTHOGONAL_PHASE_WEIGHT     = 5/6         (CP-odd)
```

These are the exact atlas projector weights, retained in the closure note
as `cos^2(delta_std) = 1/6`, `sin^2(delta_std) = 5/6`. The `5/6`
appearing in the bridge relation (T2) is this retained orthogonal-complement
weight.

### 3. The bridge relations are exact algebraic identities

Given the identifications (I1) and (I2),

```
    sqrt(m_d/m_s) = sqrt(alpha_s(v)/2) = |V_us|_atlas
```

which is (T1). And

```
    (m_s/m_b)^(5/6) = ( [alpha_s(v)/sqrt(6)]^(6/5) )^(5/6)
                    = alpha_s(v)/sqrt(6)
                    = |V_cb|_atlas
```

which is (T2). Both are exact on the identification surface (I1)-(I2); no
approximations or bridge hypotheses are used.

### 4. Downstream chain ratio

The chain `m_d/m_b = (m_d/m_s)(m_s/m_b)` follows algebraically:

```
    m_d/m_b = alpha_s(v) / 2  *  [alpha_s(v)/sqrt(6)]^(6/5)
            = alpha_s(v)^(11/5) / ( 2 * 6^(3/5) ).
```

This is the framework-native chain ratio on the retained identification
surface.

## Numerical readout (bounded quantitative layer)

Using the canonical same-surface value `alpha_s(v) = 0.103303816122`:

| Ratio | Framework identification | Threshold-local comparator | Deviation |
|---|---|---|---|
| `m_d/m_s` | `alpha_s(v) / 2 = 0.0516519` | `4.67/93.4 = 0.0500000` | `+3.30%` |
| `m_s/m_b` | `[alpha_s(v)/sqrt(6)]^(6/5) = 0.0223897` | `93.4/4180 = 0.0223445` | `+0.20%` |
| `m_d/m_b` | `alpha_s(v)^(11/5) / (2 * 6^(3/5)) = 0.001156` | `4.67/4180 = 0.0011172` | `+3.50%` |

The quantitative match is bounded by the current mass-hierarchy surface and
remains subject to the same explicit systematic that controls the Yukawa /
top lane. What the retained theorem above provides is the **exact
structural identity** of the bridge exponents with retained framework
structural numbers.

## What the theorem does and does not retain

**Retained (new structural theorem):**

- `sqrt(6)` in both `|V_cb|_atlas` and the `5/6` bridge is the same
  framework constant `sqrt(dim(Q_L))`, identified with the Ward-theorem
  Clebsch-Gordan `sqrt(N_c · N_iso)`.
- The `5/6` exponent in the bridge is the orthogonal-complement projector
  weight `1 - 1/dim(Q_L) = 5/6` on the six-state quark block.
- The bridge relations (T1) and (T2) are exact algebraic identities on the
  retained identification surface (I1)-(I2).

**Still bounded (downstream quantitative):**

- The absolute down-type mass ratios `m_d/m_s`, `m_s/m_b`, `m_d/m_b`
  inherit the mass-hierarchy lane systematic. The theorem fixes the
  **bridge exponents** exactly, not the absolute mass ratios.
- The threshold-local versus same-scale comparator choice is not closed by
  this theorem. The `+15%` same-scale deviation remains separately
  characterized by the one-loop transport factor `(alpha_s(2 GeV)/
  alpha_s(m_b))^(12/25) = 1.14747` and is not claimed to be retained.

**Named open work (explicitly not claimed here):**

- a framework-internal derivation of the mass-ratio surface (I1)-(I2) from
  a retained RG/transport theorem that connects `y_s(M_Pl)/y_b(M_Pl)` to
  the retained Ward-identity `y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6)` UV boundary.
  This would move the mass-ratio identification itself from retained
  identification surface to retained theorem output. It is the remaining
  theorem-grade work for a full retention of the absolute mass ratios;
- a framework-internal scale-selection theorem that forces the
  threshold-local self-scale comparator as the unique retained comparison
  surface.

## Relation to prior notes

This note supersedes the support-only framing in:

- [CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md](CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md)
  — the `5/6` exponent origin is now retained structural, not just the
  `C_F - T_F` Casimir identity;
- [CKM_FROM_MASS_HIERARCHY_NOTE.md](CKM_FROM_MASS_HIERARCHY_NOTE.md)
  — the GST relation `|V_us| = sqrt(m_d/m_s)` is now retained on the
  identification surface (I1) as an exact algebraic consequence of the
  retained atlas `n_pair = 2` count, not an NNI-texture assumption.

Those support notes remain live as route-history and numerical-support
material; this note carries the retained structural authority.

## Validation

Run:

```bash
python3 scripts/frontier_ckm_dual_bridge_identity.py
```

The runner verifies:

1. `sqrt(6)` origin is the retained Ward-theorem Clebsch-Gordan `sqrt(N_c ·
   N_iso)` on `Q_L`;
2. CKM atlas `|V_cb| = alpha_s(v)/sqrt(6)` uses the same `sqrt(6)` = `sqrt
   (dim(Q_L))`;
3. `1 + 5` projector split on the quark block gives `CENTER_EXCESS_WEIGHT =
   1/6` and `ORTHOGONAL_PHASE_WEIGHT = 5/6` exactly;
4. the GST exponent `1/2` equals `1/n_pair` exactly;
5. the bridge exponent `5/6` equals the atlas orthogonal-complement weight
   exactly;
6. `|V_us|_atlas = sqrt(m_d/m_s)` on the identification surface (T1) is
   exact algebraic;
7. `|V_cb|_atlas = (m_s/m_b)^(5/6)` on the identification surface (T2) is
   exact algebraic;
8. the chain ratio `m_d/m_b = alpha_s(v)^(11/5) / (2 · 6^(3/5))` is exact
   algebraic on the same surface;
9. the `5/6` retained orthogonal-complement weight is numerically
   coincident with the standard SU(3) Casimir combination `C_F - T_F =
   4/3 - 1/2 = 5/6` (reported as a coincidence check, not as a retained
   derivation);
10. the quantitative readout against the threshold-local self-scale
    comparators matches at `+3.3%` / `+0.2%` / `+3.5%` as a bounded
    downstream consequence.

Expected result: `EXACT PASS=N` exact algebraic checks, `BOUNDED PASS=M`
numerical-comparator checks, `FAIL=0`.

## Honest boundary

This note is deliberately narrow. It does not claim:

- full retention of the absolute down-type mass ratios;
- a framework-internal derivation of the mass-hierarchy itself;
- closure of the scale-selection rule;
- any claim about the up-type or charged-lepton sectors;
- any claim about the `+15%` same-scale deviation residual.

What it does claim is the structural identity of the bridge exponents with
retained framework constants, on top of which the down-type lane carries a
bounded quantitative readout that stays inside the existing mass-hierarchy
systematic.
