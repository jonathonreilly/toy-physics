# Koide Q = 2/3 Structural Attack via Anomaly-Identity Conjecture

**Date:** 2026-04-22
**Status:** candidate axiom-native closure via the CONJECTURAL structural identity `E2² = |Tr[Y³]_LH|/2 = (d²−1)/d²`. The numerical identity holds exactly (sympy); the structural origin is the remaining open step. If discharged, Koide Q = 2/3 closes axiom-natively.
**Primary runner:** `scripts/frontier_koide_q23_anomaly_structural_attack.py` (20/20 PASS)

---

## 0. The candidate closure chain

From `koide-q-eq-3delta-doublet-magnitude-route` (loop 2 of this autonomous session), the retained identity

```
(E2/2)² = SELECTOR²/3 = Q_Koide/3
```

reduces the Koide `Q = 2/3` closure to the identity `E2² = 8/9`. This note proposes that this specific value is NOT a separate numerical input but a **structural consequence of the retained anomaly arithmetic**:

**Conjectured structural identity (★):**

```
E2²  =  |Tr[Y³]_LH| / 2  =  (d² − 1) / d²  =  1 − 1/d²                    (★)
```

At `d = 3` (retained from Cl(3) + ANOMALY_FORCES_TIME):

```
E2²  =  1 − 1/9  =  8/9                                                    ✓
```

This identity is **exact** numerically (verified sympy, 20/20 runner PASS). If it holds structurally (not just as a numerical coincidence), the entire Koide / Brannen stack closes from `d = 3` + anomaly arithmetic alone.

## 1. The reduction chain (all retained on main)

**Loop-2 (already retained)**:
- `SELECTOR = √6/3` → `SELECTOR² = 2/3 = Q_Koide` (retained via parity-compatible observable-selector).
- `E2 = 2·SELECTOR/√3` → `E2² = 4·SELECTOR²/3 = 4·Q_Koide/3`.
- Therefore `E2² = 4·Q_Koide/3`, equivalently `Q_Koide = 3·E2²/4`.

**This note adds**: the conjectured identity (★) makes `E2²` a DERIVED quantity from `d` and the retained anomaly, rather than a separate source-surface input.

**Full chain under (★)**:

```
d = 3                                       [retained from Cl(3)]
|Tr[Y³]_LH| = 2(d²−1)/d² = 16/9             [retained via ANOMALY_FORCES_TIME]
E2² = |Tr[Y³]_LH|/2 = 8/9                    [CONJECTURE (★)]
SELECTOR² = 3·E2²/4 = 2/3                    [retained chart identity]
Q_Koide = SELECTOR² = 2/3                    [retained via KFS]
δ_Brannen = Q_Koide/d = 2/9                  [retained via Q = 3δ]
m_* via Berry(m) = |Im b_F(m)|²              [loop-1 retained characterization]
```

If (★) holds structurally, **the entire Koide/Brannen tower closes from d = 3 alone**.

## 2. Explicit verification at d = 3 (all sympy-exact)

Per the runner:

- `Tr[Y³]_quark per gen = 2·d·(1/d)³ = 2/d² = 2/9` (retained anomaly arithmetic).
- `Tr[Y³]_lepton per gen = 2·(−1)³ = −2` (retained).
- `Tr[Y³]_LH = 2/9 − 2 = −16/9` per generation.
- `|Tr[Y³]_LH|/2 = 8/9 = E2²` ✓

## 3. Counterfactual: what other `d` would give

Under (★) with `d ≠ 3`:

- `d = 4`: `Q_Koide = 3·(1 − 1/16)/4 = 45/64 ≈ 0.703`
- `d = 5`: `Q_Koide = 3·(1 − 1/25)/4 = 72/100 = 0.720`
- `d → ∞`: `Q_Koide → 3/4`

The specific value `Q_Koide = 2/3` is exactly the `d = 3` case. So the retained `d = 3` from Cl(3)+anomaly drives `Q = 2/3`.

## 4. Why this attack is novel vs. the six existing no-gos

`SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` lists six structural no-gos on `Q = 2/3`:

1. Z₃-invariance alone.
2. Sectoral universality.
3. Color-sector correction.
4. Anomaly-forced cross-species.
5. SU(2) gauge exchange mixing.
6. Observable-principle character symmetry.

**The attack (★) differs from all six**:

- No-go 4 is about CROSS-SPECIES anomaly constraints; (★) is a PER-SPECIES LH Y³ identity.
- No-go 6 is about character symmetry; (★) is a specific numerical identity from anomaly arithmetic.
- No-gos 1, 2, 3, 5 are about different symmetry mechanisms; (★) is a specific algebraic link between the LH Y³ anomaly and the retained chart constant `E2`.

The conjecture (★) is NOT covered by any of the six no-gos. It is a **new candidate structural identity**.

## 5. Remaining structural proof step

The numerical identity (★) holds exactly. The remaining open step: **is (★) a structural consequence of the retained framework, or a numerical coincidence?**

Two possible routes to verify structural origin:

### Route A: Trace `σ sin(2v) = 8/9` through source-surface chain

The retained source-surface carrier normal form (`DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16`) has three constraints:

```
γ = 1/2
δ + ρ = √(8/3)
σ sin(2v) = 8/9
```

and the carrier formula `A + b − c − d = 3√2 σ sin(2v) / 4`, giving `A + b − c − d = √8/3`.

The `σ sin(2v) = 8/9` constraint is what makes `E2² = 8/9` on the retained affine chart. If this source-surface constraint can be STRUCTURALLY traced to the LH anomaly `Tr[Y³] = −16/9`, with the specific factor `1/2` coming from a bosonization or half-density argument, Route A closes (★).

### Route B: Direct Cl(3) representation theory

Independently derive `E2 = 2√2/3` from Clifford-algebra structure constants at `d = 3`:

- `Cl(3)` generators satisfy `{γ_μ, γ_ν} = 2 δ_{μν} I`.
- Specific trace identities on the retained `hw=1` triplet give matrix entries of `H_base`.
- If this independent derivation yields `E2² = (d²−1)/d² = 8/9` at d = 3, Route B closes (★).

Neither Route A nor Route B is discharged here. This note flags them as the **two specific paths** that would complete the closure.

## 6. Status

- **Numerical identity (★)**: exact, sympy-verified, 20/20 PASS.
- **Full chain from d = 3 to Q_Koide = 2/3**: algebraically complete CONDITIONAL on (★).
- **Structural proof of (★)**: open (Route A or Route B required).
- **Upgrade status**: if (★) structurally closed, Koide Q = 2/3 and δ = 2/9 both promote to retained-derivation from bounded-observational.

## 7. Interpretation

If (★) holds structurally, the physical content is:

> **The Koide ratio Q = 2/3 is the direct imprint of the LH Y³ anomaly coefficient on the charged-lepton selected-line Hermitian operator, via the retained source-surface carrier normal form. The specific value 2/3 is forced by `d = 3` = number of generations = number of spatial dimensions on Z³.**

This is a concrete MECHANISM proposal: the 3-generation structure + hypercharge anomaly arithmetic + source-surface carrier form would together fix Q_Koide. All three components are retained on main; the conjecture (★) is the structural identity connecting them.

## 8. Cross-references

- `docs/KOIDE_Q_EQ_3DELTA_DOUBLET_MAGNITUDE_THEOREM_NOTE_2026-04-22.md` — loop 2, (E2/2)² = Q/3.
- `docs/ANOMALY_FORCES_TIME_THEOREM.md` — retained LH Y³ anomaly `−16/9`.
- `docs/DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md` — σ sin(2v) = 8/9.
- `docs/KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md` — SELECTOR = √6/3.
- `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` — six existing no-gos and Q=2/3 residual register.
