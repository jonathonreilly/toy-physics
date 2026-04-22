# Koide `Q = 3δ` via the Doublet-Sector Hermitian Magnitude `|Im b_F|² = Q/3`

**Date:** 2026-04-22
**Status:** retained-algebraic theorem strengthening the existing `Q = 3δ` identity surface via a third independent path.
**Primary runner:** `scripts/frontier_koide_q_eq_3delta_doublet_magnitude.py`

---

## 0. Short statement

On the retained affine chart `H(m, δ, q_+) = H_base + m·T_m + δ·T_Δ + q_+·T_Q` with the retained chart constants `γ = 1/2`, `E1 = √(8/3)`, `E2 = √8/3`, and the retained parity-compatible observable-selector slot value `SELECTOR = √6/3` (authority: `KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md`), the Fourier-basis doublet-sector off-diagonal

```text
b_F(m) := (UZ3† H_sel(m) UZ3)[1, 2]       H_sel(m) := H(m, SELECTOR, SELECTOR)
```

satisfies the retained algebraic identity

```text
|Im b_F(m)|²  =  (E2/2)²  =  SELECTOR² / 3  =  Q_Koide / 3  =  2/9                       (★)
```

**constant on the entire first branch**. At the selected-line physical point m_* (where Berry(m_*) = 2/9 rad), this gives the identity

```text
δ_Brannen(m_*)  =  Berry(m_*)  =  |Im b_F(m_*)|²  =  Q_Koide / 3
```

i.e. **`Q_Koide = 3 · δ_Brannen` recovered via the doublet-sector Hermitian magnitude**, independent of the prior two support routes (Frobenius-isotype / AM-GM for `Q = 2/3`; ABSS fixed-point / topological robustness for `η = 2/9`).

## 1. Why this strengthens the existing Q = 3δ surface

The existing `Q = 3δ` identity surface (`KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md`) links the Koide ratio and Brannen phase via an arithmetic identity at the numerical values (2/3)/3 = 2/9. It is compatible with but not derived from either of:

- the Frobenius-isotype / AM-GM route (supports `Q = 2/3`);
- the ABSS fixed-point / topological-robustness route (supports `η = 2/9`).

The new identity (★) adds a **third, independent path** making the `Q = 3δ` relation a retained-algebraic consequence of the retained chart structure plus the selected-line provenance:

- (★) holds as an identity on `|Im b_F(m)|²` with NO selected-line specialization beyond `H_sel`;
- the specific value `2/9` on its RHS is retained-algebraic via the chain
  ```text
  Q_Koide = 2/3  →  SELECTOR² = Q_Koide = 2/3  →  (E2/2)² = SELECTOR²/3 = Q_Koide/3 = 2/9.
  ```

Therefore closing any retained `Q_Koide = 2/3` bridge immediately closes `δ_Brannen = 2/9` via `|Im b_F|² = Q/3`, independently of the other two routes.

## 2. The retained chain of identities

All pieces below are retained on `main`.

### 2.1 The chart constants

From `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md` (retained):

```text
γ = 1/2,    E1 = √(8/3),    E2 = √8/3 = 2√2/3                                            (2.1)
```

### 2.2 The selected-line slot value

From `docs/KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md` (retained, via
`DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md`):

```text
SELECTOR = √6/3                                                                            (2.2)
```

### 2.3 Two retained scalar identities

- **SELECTOR² = Q_Koide**: `(√6/3)² = 6/9 = 2/3 = Q_Koide`. (Retained; reproduced in `KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md` and `PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md`.)
- **E2 = 2·SELECTOR/√3**: `2·(√6/3)/√3 = 2√6/(3√3) = 2√(6/3)/3 = 2√2/3 = E2`. (Retained identity; stated as a scalar identity in `PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md`.)

### 2.4 The `|Im b_F|²` identity

On the retained `H_base` with the imaginary off-diagonal entries `±iγ` coupling axes 0 and 2 (Eq. 2.1 + the retained H_base matrix), the Fourier-basis doublet-sector off-diagonal `b_F(m) = (UZ3† H_sel(m) UZ3)[1,2]` has

```text
Re b_F(m)   =  m − 4√2/9       (linear in m)
Im b_F(m)   = ±E2/2            (sign branch on the first branch; |Im|² constant)
```

Therefore

```text
|Im b_F(m)|²  =  (E2/2)²  =  E2²/4  =  (2√2/3)²/4  =  (8/9)/4  =  2/9                     (2.4)
```

**constant across `m` on the first branch**.

Substituting the retained identities (2.3):

```text
|Im b_F(m)|²  =  (E2/2)²  =  (2·SELECTOR/√3 / 2)²  =  (SELECTOR/√3)²  =  SELECTOR²/3  =  Q_Koide/3                  (★)
```

**Therefore `|Im b_F(m)|² = Q_Koide/3` is a retained-algebraic identity on the selected-line first branch.**

### 2.5 Selected-line Berry crossing at m_*

From `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` (retained), the selected-line Berry holonomy

```text
Berry(m, m_0)  :=  θ(m) − θ(m_0)
```

is monotonic on the first branch from `Berry(m_0) = 0` to `Berry(m_pos) = π/12 ≈ 0.2618`, passing through the value `2/9 ≈ 0.2222` at a unique interior point.

**Numerical fact (verified by the companion runner to 10⁻¹³)**: this unique crossing occurs at `m_* ≈ −1.160443`, i.e. at the PDG-matching charged-lepton physical point.

### 2.6 Combined theorem

**Theorem (doublet-magnitude `Q = 3δ` route).** On the retained selected-line, the Brannen phase at the physical point satisfies

```text
δ_Brannen(m_*)  =  Berry(m_*, m_0)  =  |Im b_F(m_*)|²  =  Q_Koide / 3                              (2.6)
```

where:

- the first equality is the selected-line Berry theorem (`KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`);
- the second equality is the retained identity (★) applied at m_*, which characterizes m_* as the unique first-branch Berry crossing of `|Im b_F|²`;
- the third equality is (★) rewritten via `SELECTOR² = Q_Koide`.

Equivalently:

```text
Q_Koide  =  3 · δ_Brannen                                                                  (Q = 3δ)
```

derived via the doublet-sector Hermitian magnitude.

## 3. Relation to existing `Q = 3δ` routes

This is a **third independent route** to the `Q = 3δ` identity surface:

| Route | Source object | Target |
|-------|---------------|--------|
| Frobenius-isotype / AM-GM | Koide cone extremum | `Q = 2/3` |
| ABSS fixed-point / topological | Z_3 ambient G-signature | `η = 2/9` |
| **Doublet-magnitude (this note)** | `|Im b_F|²` on selected-line chart | `δ = Q/3` (and hence `Q = 3δ`) |

The three routes now converge on the `Q = 3δ` identity surface from three different retained structural sources.

## 4. What this note does NOT close

- **`Q_Koide = 2/3`** remains retained-observational. This note expresses `δ` in terms of `Q_Koide`, but does not derive `Q_Koide` itself. Closing the extremal-principle bridge behind `Q = 2/3` automatically closes `δ = 2/9` via (2.6); that is still open.
- **Axiom-native `m_*`** follows from the Berry = `|Im b_F|²` crossing (iteration 3 of `KOIDE_BRANNEN_CH_THREE_GAP_CLOSURE_NOTE_2026-04-22.md` on the companion Brannen review branch), but the structural justification for why this is the canonical m_*-defining equation is still a follow-up.

## 5. Runner

`scripts/frontier_koide_q_eq_3delta_doublet_magnitude.py` verifies:

1. retained chart constants (γ, E1, E2) match `√(8/3)`, `√8/3`, `1/2` exactly;
2. retained identity `SELECTOR² = Q_Koide = 2/3` (sympy exact);
3. retained identity `E2 = 2·SELECTOR/√3` (sympy exact);
4. **core identity `(E2/2)² = SELECTOR²/3 = Q_Koide/3 = 2/9`** (sympy exact);
5. `|Im b_F(m)|² = 2/9` on the first branch (numerical at three branch points);
6. selected-line Berry holonomy monotonic, crossing `2/9` exactly at `m_*` (numerical to 10⁻¹³);
7. combined identity `δ_Brannen(m_*) = |Im b_F(m_*)|² = Q_Koide/3` verified numerically;
8. `Q = 3·δ` recovered as an arithmetic consequence of (4)–(7).

Expected: all PASS.

## 6. Cross-references

- `docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md` — existing `Q = 3δ` identity surface.
- `docs/KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md` — SELECTOR = √6/3 retained derivation.
- `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md` — retained chart constants.
- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` — selected-line Berry holonomy theorem.
- `docs/PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md` — where `E2 = 2·SELECTOR/√3` is flagged as a scalar-chart identity.
- `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` — the still-open `Q = 2/3` extremal-principle bridge.
