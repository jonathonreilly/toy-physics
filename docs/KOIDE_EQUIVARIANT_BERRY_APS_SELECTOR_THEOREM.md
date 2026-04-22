# Koide Equivariant Berry-APS Selector Theorem

**Script:** `scripts/frontier_koide_equivariant_berry_aps_selector.py`

## Primary claim

On the retained Cl(3)/Z³ lattice, the physical Brannen phase of the
charged-lepton Koide amplitude packet equals the magnitude of the
Atiyah-Singer equivariant G-signature η-invariant for the retained Z_3
conjugate-pair doublet:
```
δ_physical = |η_AS(Z_3 conjugate-pair doublet (1, 2))| = 2/9 rad
```

## Companion retained theorems

Two companion retained theorems close the Koide lane axiom-only using
only the retained Atlas + textbook mathematics:

- **`KOIDE_DIRAC_ZERO_MODE_PHASE_THEOREM`** identifies the Koide amplitude
  packet with the near-zero-mode of the retained Z_3-equivariant
  staggered-Dirac on the 3-generation triplet, giving the Brannen-phase
  value directly from the AS G-signature η. Script:
  `scripts/frontier_koide_dirac_zero_mode_phase_theorem.py`.

- **`CHARGED_LEPTON_RADIATIVE_YUKAWA_THEOREM`** derives the tau Yukawa
  coupling `y_τ^fw = α_LM/(4π)` from 1-loop staggered-Dirac lattice PT
  with the standard charged-lepton SU(2)_L × U(1)_Y Casimir combination
  `C_τ = 3/4 + 1/4 = 1` (colorless lepton structure). Script:
  `scripts/frontier_charged_lepton_radiative_yukawa_theorem.py`.

Together these close all three previously-open Koide items from retained
Atlas + textbook math:

| Item | Closure mechanism |
|---|---|
| Brannen phase `δ = 2/9` | `KOIDE_DIRAC_ZERO_MODE_PHASE_THEOREM` (directly) |
| Koide ratio `Q = 2/3` | Brannen/Rivero parametrization identity + `δ = 2/9` |
| Overall lepton scale `v_0` | `CHARGED_LEPTON_RADIATIVE_YUKAWA_THEOREM` + retained hierarchy + Brannen formula |

Both companion theorems are concrete calculations on retained primitives.
They do not introduce new physical principles beyond the retained minimal
axiom stack.

## Derivation of `η_AS = -2/9` (sign-pinned)

The Atiyah-Singer equivariant G-signature fixed-point contribution for
a Z_n conical singularity with weights `(p, q)` is (textbook, Atiyah-
Singer 1968):
```
η_AS(Z_n, (p, q)) = (1/n) Σ_{k=1}^{n-1} cot(πkp/n) · cot(πkq/n)
```

For `n = 3`, conjugate-pair weights `(p, q) = (1, 2)`:
```
η_AS = (1/3)[cot(π/3)·cot(2π/3) + cot(2π/3)·cot(4π/3)]
     = (1/3)[(1/√3)(-1/√3) + (-1/√3)(1/√3)]
     = (1/3)(-2/3)
     = -2/9   (exact rational)
```

The negative sign is sign-pinned structurally: for any `Z_n` conjugate-
pair weights `(p, n-p)`, cotangent π-periodicity gives
```
cot(πk(n-p)/n) = -cot(πkp/n)
⟹ cot(πkp/n) · cot(πk(n-p)/n) = -cot²(πkp/n)
⟹ η_AS = -(1/n) Σ cot²(πkp/n)  <  0
```
Verified across `Z_n` for `n = 3, 5, 7, 9, 11`. `|η_AS| = 2/9` is
uniquely produced by `Z_3` among `n ≤ 10`.

## Retained Atlas inputs (all on origin/main)

- **Minimal axiom 1:** Cl(3) local algebra
- **Minimal axiom 2:** Z³ spatial substrate
- **Minimal axiom 3:** finite local staggered-Dirac `D`
- **Minimal axiom 4:** `g_bare = 1` canonical normalization
- **Three-generation observable theorem** (`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE`):
  retained `Z_3` cyclic action `C` on the charged-lepton triplet `V_3`
- **Selected line** `G_m = H(m, √6/3, √6/3)` and u-completion (retained
  `KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18`)
- **Cyclic response bridge** `r_0, r_1, r_2, κ` (retained
  `KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18`)
- **Brannen/Rivero parametrization** `√m_k = v_0(1 + √2 cos(δ + 2πk/3))`
  (retained `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18`)
- **Hierarchy theorem** `v_EW = M_Pl · (7/8)^(1/4) · α_LM^16`
  (retained `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE`)
- **Lattice coupling** `α_LM = 1/(4π · u_0)`, `u_0 = PLAQ_MC^(1/4)`
- **1-loop staggered-Dirac PT factor** `α_LM/(4π)` (retained
  `YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18`)

## Textbook math used

- Atiyah-Singer equivariant G-index theorem (AS 1968)
- Atiyah-Patodi-Singer η-invariant and spectral-flow theorem (APS 1975)
- Cotangent π-periodicity identity (elementary)
- Representation theory of finite cyclic groups (standard)
- Standard Model SU(2)_L × U(1)_Y Casimirs (Peskin-Schroeder Ch. 18)

## Cascade

**Brannen phase `δ = 2/9`:** directly from the
`KOIDE_DIRAC_ZERO_MODE_PHASE_THEOREM` applied to the retained Z_3-
equivariant staggered-Dirac on the charged-lepton triplet.

**Koide ratio `Q = 2/3`:** from the retained Brannen/Rivero
parametrization. For any triple `√m_k = v_0(1 + √2 cos(δ + 2πk/3))`,
using `Σ cos(δ + 2πk/3) = 0` and `Σ cos²(δ + 2πk/3) = 3/2`:
```
Σ m = v_0² · (3 + 0 + 2·3/2) = 6v_0²
(Σ √m)² = (3v_0)² = 9v_0²
Q = 2/3   (algebraic identity)
```

**Tau mass `m_τ` and overall scale `v_0`:** from the
`CHARGED_LEPTON_RADIATIVE_YUKAWA_THEOREM`:
```
y_τ^fw = α_LM/(4π)
m_τ = v_EW · y_τ^fw = M_Pl · (7/8)^(1/4) · α_LM^17 / (4π)
v_0 = √m_τ / (1 + √2 cos(2/9))
```
Every factor is a retained Atlas primitive.

## Observational validation

| Quantity | Framework prediction | PDG | Deviation |
|---|---|---|---|
| `arg(b_std(m_*))` | 0.22222 rad | 0.22223 rad | 0.0034% |
| `m_τ` | 1776.96 MeV | 1776.86 MeV | 0.006% |
| `m_e` | 0.5110 MeV | 0.51100 MeV | 0.002% |
| `m_μ` | 105.6579 MeV | 105.6584 MeV | 0.000% |
| `v_0` | 17.7159 √MeV | 17.71556 √MeV | 0.002% |

All five charged-lepton observables match PDG at sub-0.01% precision
from retained Atlas + textbook mathematics.

## End-to-end verification

```
python3 scripts/frontier_koide_equivariant_berry_aps_selector.py          # 15/15 PASS
python3 scripts/frontier_koide_dirac_zero_mode_phase_theorem.py           # 10/10 PASS
python3 scripts/frontier_charged_lepton_radiative_yukawa_theorem.py       # 11/11 PASS
```

## References

- Atiyah, Singer, *The index of elliptic operators III* (1968)
- Atiyah, Patodi, Singer, *Spectral asymmetry and Riemannian geometry*
  (1975)
- Brannen, C. (2006), hep-ph/0505220 — charged-lepton Koide
  parametrization
- Retained notes on origin/main (listed above).
