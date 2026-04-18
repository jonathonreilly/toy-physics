# CKM-Dual Bridge Identity Theorem
## Retained Structural Identities + Proposed Atlas-Projector-Weighted Texture Primitive

**Date:** 2026-04-17 (first draft); revised 2026-04-17 after review.md (new-science path: propose texture primitive).
**Status (two-layer):**
- **retained structural identities** — the `sqrt(6)`, `1/n_{pair}`, and `5/6` constants in the down-type CKM-dual lane are the same retained framework constants as those appearing in the Ward theorem and the CKM atlas (SI1, SI2, SI3 below).
- **proposed new retained primitive (P-AT)** — the Atlas-Projector-Weighted Mass-Matrix Texture on the retained `hw=1` down-type block. Under P-AT, the GST relation and the `5/6` bridge become **leading-order-exact** hierarchical identities, and combining with the retained CKM atlas gives the mass-ratio identification surface (I1)–(I2) as a framework output.
- **conditional on P-AT acceptance** — GST `|V_{us}| = \sqrt{m_d/m_s}` and the `5/6` bridge `|V_{cb}| = (m_s/m_b)^{5/6}` are retained leading-order theorems; (I1)–(I2) are retained identification-surface outputs.

P-AT is explicitly a **new retained primitive proposal**, not a derivation from pre-existing retained inputs. It uses only retained atlas projector weights as exponents in the `(2,3)` off-diagonal of the down-type mass matrix. Its acceptance or rejection is a framework-level decision.

**Primary runner:** `scripts/frontier_ckm_dual_bridge_identity.py`
**Authority role:** proposes and validates P-AT; separates retained structural identities from conditional-on-P-AT bridge theorems.

## Reviewer context

The earlier draft of this note claimed the bridges as unconditional retained framework theorems. The review on this branch (see `review.md`, P1/P1/P2) correctly flagged that the previous framing promoted a chosen identification surface as if the framework had already derived it. This revision takes the **new-science path**: propose a concrete, sharp new primitive that actually derives the bridges (at leading order), and label it transparently as new.

## Retained inputs (unchanged)

1. **Ward-identity theorem** —
   [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](YT_WARD_IDENTITY_DERIVATION_THEOREM.md),
   `y_t(M_Pl) / g_s(M_Pl) = 1/\sqrt{6} = 1/\sqrt{N_c \cdot N_{iso}}`. The
   `\sqrt{6}` is the Clebsch-Gordan normalization of the unit-norm scalar
   singlet composite `H_unit = (1/\sqrt{6}) \sum \psī\psi` on the
   left-handed quark block `Q_L`, derived from `D9` (composite Higgs) and
   `D17` (scalar-uniqueness on `Q_L`) with `Z^2 = N_c \cdot N_{iso} = 6`.

2. **CKM atlas/axiom closure** —
   [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md),
   `|V_{us}| = \sqrt{\alpha_s(v)/2}`, `|V_{cb}| = \alpha_s(v)/\sqrt{6}`.
   The `2` is the residual color pair (EWSB `1 + 2` split), and the `6` is
   `n_{quark} = n_{pair} \cdot n_{color} = \dim(Q_L)`.

3. **Atlas `1 + 5` projector split on `Q_L`** — same atlas note. On the
   six-state quark block, the center-excess scalar CP-even weight is
   `CENTER\_EXCESS\_WEIGHT = 1/n_{quark} = 1/6`, and the CP-odd orthogonal
   complement has weight `ORTHOGONAL\_PHASE\_WEIGHT = 1 - 1/6 = 5/6`.

4. **Z_2 `hw=1` mass-matrix parametrization** —
   [Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md).
   The retained `Z_2`-invariant Hermitian normal form is a 5-parameter
   family on the `hw=1` down-type triplet.

5. **Canonical same-surface coupling** —
   [ALPHA_S_DERIVED_NOTE.md](ALPHA_S_DERIVED_NOTE.md),
   `\alpha_s(v) = \alpha_{bare} / u_0^2 = 0.103303816122`.

No observed quark masses enter as derivation inputs. No new retained
primitives apart from P-AT (stated below) are introduced.

## Layer 1: retained structural identities (unchanged by review)

**SI1 (same-`\sqrt{6}` identity).** The `\sqrt{6}` in the Ward identity
`y_t(M_Pl)/g_s(M_Pl) = 1/\sqrt{6}` and in `|V_{cb}|_{atlas} =
\alpha_s(v)/\sqrt{6}` is the **same** retained framework constant
`\sqrt{N_c · N_{iso}} = \sqrt{n_{pair} · n_{color}} = \sqrt{n_{quark}}
= \sqrt{\dim(Q_L)} = \sqrt{6}`.

**SI2 (GST exponent origin).** The `1/2` exponent in the GST form
`|V_{us}| = (m_d/m_s)^{1/2}` equals `1/n_{pair}` where `n_{pair} = 2` is
the retained EWSB residual color-pair count.

**SI3 (`5/6` atlas projector origin).** The `5/6` exponent in the bridge
`|V_{cb}| = (m_s/m_b)^{5/6}` equals the retained atlas orthogonal-complement
projector weight `1 - 1/n_{quark} = 5/6` on the six-state `Q_L` block, the
same `5/6` that appears as `\sin^2(\delta_{std})` in the atlas `1 + 5`
projector split. The numerical coincidence with the SU(3) Casimir
combination `C_F - T_F = 5/6` is recorded as a cross-check, not the
retained origin.

SI1, SI2, SI3 are exact retained identities that specify *which* framework
constants carry the `\sqrt{6}`, `1/2`, and `5/6` numbers. They do **not**
by themselves derive the mass-ratio identification surface — that is what
the proposed primitive in Layer 2 supplies.

## Layer 2: proposed new retained primitive — P-AT

**Primitive P-AT (Atlas-Projector-Weighted Mass-Matrix Texture).** On the
retained `hw=1` down-type mass matrix in the axis basis `(X_1, X_2, X_3)`
(where `X_3` is aligned with the heaviest generation), the real symmetric
mass matrix has the NNI-zero + atlas-projector-weighted `(2,3)` texture

```
              [  m_d            \sqrt{m_d · m_s}        0                        ]
    M_d  =    [  \sqrt{m_d·m_s}   m_s                     m_s^{w_o} · m_b^{w_c}    ]      (P-AT)
              [  0              m_s^{w_o} · m_b^{w_c}   m_b                      ]
```

with

- `w_o = ORTHOGONAL\_PHASE\_WEIGHT = 5/6` (retained CP-odd projector weight
  on `Q_L`, SI3);
- `w_c = CENTER\_EXCESS\_WEIGHT = 1/6` (retained CP-even projector weight
  on `Q_L`, SI3);
- `w_o + w_c = 1` (complete atlas projector split on `Q_L`);
- the `(1,2)` off-diagonal is the classical NNI geometric mean
  `\sqrt{m_d · m_s}` (standard texture-zero mechanism);
- the `(1,3)` off-diagonal is zero (texture zero, in the standard NNI
  sense).

The new retained content in P-AT is specifically the `(2,3)` off-diagonal
form: the heavier generation is weighted by the CP-even `CENTER\_EXCESS`
atlas projector fraction `1/6`, and the lighter generation by the CP-odd
`ORTHOGONAL` complement `5/6`. The geometric-mean `(1,2)` entry and the
texture zero `(1,3)` are standard NNI content and are not novel here.

**Motivation (framework-internal, but not a pre-existing retained
derivation).** The atlas bilinear tensor carrier
[S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md](S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md)
on the `Q_L` block decomposes into a CP-even singlet (weight `1/6`) and a
CP-odd orthogonal complement (weight `5/6`). The bridge-inducing operator
that mixes generations 2 and 3 couples through this same `Q_L` carrier.
P-AT asserts that the off-diagonal `(2,3)` mass-matrix element inherits
the same atlas projector weighting, with the heavier generation carried
on the CP-even fraction and the lighter generation on the CP-odd
complement. This is structurally motivated — but it is a **new claim**
and not a theorem on the current retained surface.

## Consequences under P-AT

**T1 (GST leading-order exactness under P-AT).** In the hierarchical
limit `m_d/m_s \to 0`, `m_s/m_b \to 0`, the down-type diagonalization of
P-AT gives
```
    |V_{us}|  =  \sqrt{m_d/m_s}   (leading-order-exact).
```

**T2 (`5/6` bridge leading-order exactness under P-AT).** In the same
hierarchical limit, the down-type diagonalization of P-AT gives
```
    |V_{cb}|  =  (m_s/m_b)^{5/6}  (leading-order-exact).
```

**T3 (mass-ratio identification surface).** Equating T1 and T2 with the
retained atlas values
`|V_{us}|_{atlas} = \sqrt{\alpha_s(v)/n_{pair}}` and
`|V_{cb}|_{atlas} = \alpha_s(v)/\sqrt{n_{quark}}` gives the mass-ratio
identification surface
```
    m_d/m_s  =  \alpha_s(v) / n_{pair}                                   (I1)
    m_s/m_b  =  [ \alpha_s(v) / \sqrt{n_{quark}} ]^{n_{quark}/(n_{quark}-1)}
             =  [ \alpha_s(v) / \sqrt{6} ]^{6/5}                         (I2)
```

as a retained framework output under P-AT (at leading order).

The exponents `1/n_{pair}` and `n_{quark}/(n_{quark}-1)` in (I1)–(I2) are
fixed by the retained structural counts (SI2, SI3), not chosen. No
mass-matrix parameter is free.

## Numerical verification

The runner `scripts/frontier_ckm_dual_bridge_identity.py` verifies:

1. **Retained structural identities SI1, SI2, SI3** — `\sqrt{6}` Ward /
   atlas / quark-block dimension equalities; `1/2 = 1/n_{pair}`;
   `5/6 = 1 - 1/n_{quark}` atlas projector weight equalities.
2. **P-AT hierarchical limit** — numerical diagonalization of the P-AT
   mass matrix at a sequence of epsilon-scaled mass hierarchies
   `(m_d/m_s, m_s/m_b) = (\epsilon, \epsilon)` for
   `\epsilon \in \{10^{-1}, 10^{-2}, 10^{-3}, 10^{-4}, 10^{-5}, 10^{-6}\}`,
   confirming
   - `|V_{us}| / \sqrt{m_d/m_s}  \to  1` as `\epsilon \to 0`,
   - `|V_{cb}| / (m_s/m_b)^{5/6}  \to  1` as `\epsilon \to 0`.
3. **Identification-surface match at the observed hierarchy** — using the
   canonical `\alpha_s(v) = 0.103303816122`, the P-AT diagonalization gives
   `|V_{us}|_{P-AT} \approx |V_{us}|_{atlas}` and
   `|V_{cb}|_{P-AT} \approx |V_{cb}|_{atlas}` within small-hierarchy
   leading-order error.
4. **Mass-ratio readout against PDG threshold-local self-scale** —
   `m_d/m_s = 0.05165` (`+3.30%`),
   `m_s/m_b = 0.02239` (`+0.20%`),
   `m_d/m_b = 0.001156` (`+3.50%`).

Expected result: `RETAINED PASS=N`, `P-AT PASS=M`, `BOUNDED PASS=K`,
`FAIL=0`. The runner tags results by layer.

## Status summary

**Retained on `main` (structural-identity layer):**

- SI1: `\sqrt{6}` = retained Ward Clebsch-Gordan `\sqrt{N_c · N_{iso}}`,
  same as atlas `\sqrt{n_{quark}}`.
- SI2: GST exponent `1/2 = 1/n_{pair}` (atlas EWSB pair count).
- SI3: `5/6` exponent = atlas `1 + 5` orthogonal-complement projector
  weight (not the SU(3) Casimir coincidence).

**Proposed new retained primitive (framework-level review pending):**

- P-AT: down-type `hw=1` mass matrix has NNI-zero structure + atlas-projector-weighted `(2,3)` off-diagonal with exponents `(w_o, w_c) = (5/6, 1/6)`.

**Consequences under P-AT (retained conditional on P-AT acceptance):**

- T1: GST `|V_{us}| = \sqrt{m_d/m_s}` is leading-order exact.
- T2: `5/6` bridge `|V_{cb}| = (m_s/m_b)^{5/6}` is leading-order exact.
- T3: mass-ratio identification surface (I1)–(I2) is the framework output
  combining T1–T2 with the retained atlas CKM values.

**Still bounded (downstream quantitative):**

- Absolute values `m_d`, `m_s`, `m_b` (only their ratios are pinned).
- Threshold-local versus same-scale comparator choice.

**Still open (explicitly named):**

- Framework-level review: does P-AT (atlas-projector-weighted `(2,3)`)
  qualify as a retained primitive, or is it a proposal that needs further
  derivation from a retained operator-theoretic argument on the `Q_L`
  bilinear tensor carrier `K_R`?
- A sub-leading-order correction program beyond the hierarchical
  leading-order exact bridges.
- A framework-level scale-selection rule for the threshold-local
  comparator surface.

## Relation to prior notes

- [CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md](CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md)
  — `5/6` exponent origin upgraded from Casimir coincidence to retained
  atlas projector weight (SI3); the bridge itself is now retained
  **leading-order** under P-AT (not exact at finite hierarchy).
- [CKM_FROM_MASS_HIERARCHY_NOTE.md](CKM_FROM_MASS_HIERARCHY_NOTE.md)
  — GST exponent origin upgraded from NNI-texture assumption to retained
  atlas `1/n_{pair}` count (SI2); the GST relation itself is now retained
  **leading-order** under P-AT.
- [Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md)
  — P-AT is a specific 2-parameter subspace of the 5-parameter `Z_2`
  normal form (after identifying `m_d`, `m_s`, `m_b` up to scale). P-AT
  does not follow from `Z_2` symmetry alone; the `(2,3)` off-diagonal
  structure is the new framework content.

## Honest boundary

This revised note does **not** claim:

- that P-AT is derived from pre-existing retained primitives;
- exact closure of GST or `5/6` bridge at finite hierarchy (only
  leading-order);
- full retention of absolute down-type mass values (only ratios up to
  overall scale);
- a scale-selection theorem;
- closure of the up-type or charged-lepton sectors.

What it does claim, in two sharp layers:

1. **Layer 1 (retained on `main`):** SI1–SI3 identify the `\sqrt{6}`,
   `1/2`, and `5/6` numbers with retained framework structural constants
   (Ward Clebsch-Gordan, `n_{pair}`, atlas orthogonal-complement
   projector weight). These are retained unconditionally.
2. **Layer 2 (proposed new primitive, framework-level review pending):**
   P-AT asserts the atlas-projector-weighted `(2,3)` off-diagonal in the
   down-type mass-matrix texture. Under P-AT, T1 (GST), T2 (`5/6`
   bridge), and T3 (identification surface I1-I2) follow at leading order
   in the hierarchical limit.

The earlier draft of this note conflated Layer 1 and Layer 2. This
revision separates them: Layer 1 is retained and unambiguous; Layer 2 is
a new framework proposal with explicit "proposed primitive" status and
explicit leading-order qualifier on the derived bridges.
