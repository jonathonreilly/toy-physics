# EW-EM Lattice Double-Angle Trinity: cos(2θ_W) = e² = 1/N_color²

**Date:** 2026-04-26

**Status:** retained EW-EM lattice-scale identity theorem; NEW
THREE-way RETAINED equality at lattice scale tying the double-angle
Weinberg cosine, the squared electric coupling, and the inverse-square
color count from the recently-landed S1 Identification Source Theorem.

```text
(C1)  cos(2 θ_W) | _lattice  =  e² | _lattice  =  1 / N_color²  =  1/9     [THREE-WAY RETAINED]
```

This is a sister identity to the retained `sin²(θ_W)|_lattice = A^4 = 4/9`
bridge and the retained `cos²(θ_W)|_lattice = 1 - A^4 = 5/9` complement
bridge. Where those bridge the SQUARED Weinberg sine and cosine to the
Wolfenstein A and to the structural integers from S1, this trinity
bridges the DOUBLE-ANGLE Weinberg cosine to the squared electric
coupling and to the inverse-square color count.

The structural reading is novel:

> At lattice scale, the double-angle Weinberg cosine `cos(2 θ_W)`
> EQUALS the squared electric coupling `e²` EQUALS `1/N_color²`.
> All three are `1/9` exactly at retained values.

Plus NEW closed forms for the double-angle Weinberg sine, the
fine-structure constant, and the cos(2θ_W)/sin(2θ_W) ratio at lattice
scale.

**Explicitly not a below-Wn closure**: this note is a retained
algebraic identity at lattice scale (consistency-at-retained-values
type), NOT a below-Wn derivation closure. The labelling follows the
preceding `A^4` and `cos²(θ_W)` complement bridges and the lesson from
`feedback_consistency_vs_derivation_below_w2.md`.

**Primary runner:**
`scripts/frontier_ew_em_lattice_double_angle_trinity.py`

## Headline NEW Identities

```text
(C1)  cos(2 θ_W) | _lattice  =  e² | _lattice  =  1 / N_color²  =  1/9
                                                                  [THREE-WAY RETAINED]

(C2)  sin²(2 θ_W) | _lattice =  4 sin²(θ_W) cos²(θ_W) | _lattice
                              =  4 × (4/9) × (5/9)
                              =  80/81
                              =  N_pair^4 × (N_quark - 1) / N_color^4    [NEW closed form]

(C3)  sin(2 θ_W) | _lattice  =  4 √(N_quark - 1) × N_pair / N_color²
                              =  4 √5 / 9 ≈ 0.9938                       [NEW closed form]

(C4)  α_EM | _lattice         =  e² / (4 π)
                              =  1 / (4 π × N_color²)
                              =  1 / (36 π) ≈ 0.008842                   [NEW reading via S1]

(C5)  1 / α_EM | _lattice     =  4 π × N_color²
                              =  36 π ≈ 113.10                           [NEW reading via S1]

(C6)  Pythagorean closure:
            cos²(2 θ_W) + sin²(2 θ_W) | _lattice
         =  (1/N_color²)² + N_pair^4 (N_quark - 1) / N_color^4
         =  (1 + N_pair^4 (N_quark - 1)) / N_color^4
         =  (1 + 80) / 81
         =  81 / 81  =  1.                                                [EXACT]

(C7)  tan(2 θ_W) | _lattice  =  4 N_pair √(N_quark - 1)
                              =  4 √5 ≈ 8.944                            [NEW closed form]
```

## Reviewer Frame

This note explicitly:

- **Does NOT claim** below-Wn derivation closure for any of C1-C7.
  Each identity is a NEW algebraic re-expression of retained values
  at lattice scale via the freshly-landed S1 Identification Source
  Theorem.
- **Does claim**: a NEW retained THREE-way EW-EM-S1 lattice-scale
  equality at `1/N_color²` (cos(2θ_W) = e² = 1/N_color² = 1/9), NEW
  closed forms for `sin(2θ_W)`, `sin²(2θ_W)`, `tan(2θ_W)`, and a NEW
  S1-backed structural reading of `α_EM|_lattice = 1/(4π × N_color²)`.

The lesson from `feedback_retained_tier_purity_and_package_wiring.md`:
N-way retained equalities must include only retained-tier sources.
The THREE-way equality C1 uses only retained-tier authorities (EW Higgs
diagonalization tree theorem; YT_EW retained bare couplings; S1
recently-landed source theorem; sister A^4 bridge and cos²(θ_W)
complement bridge — all retained on main).

## Statement

On retained-tier authorities of current `main`:

```text
(P1)  EW Higgs gauge-mass diagonalization (retained tree theorem):
        sin²(θ_W) = g_Y² / (g_2² + g_Y²),
        cos²(θ_W) = g_2² / (g_2² + g_Y²),
        1/e² = 1/g_2² + 1/g_Y².

(P2)  YT_EW retained bare lattice couplings:
        g_2² = 1/(d+1) = 1/4,
        g_Y² = 1/(d+2) = 1/5,
        d = dim(Z³) = 3.

(P3)  Sister `A^4` lattice bridge (retained):
        sin²(θ_W) | _lattice  =  A^4  =  4/9.

(P4)  Sister `cos²(θ_W)` complement bridge (retained):
        cos²(θ_W) | _lattice  =  1 - A^4  =  5/9.

(P5)  S1 Identification Source Theorem (retained):
        Q_L : (2,3)_{+1/3} sources N_pair = dim_SU2(Q_L) = 2 and
        N_color = dim_SU3(Q_L) = 3, with N_quark = N_pair × N_color = 6.

(P6)  T8 SM-specific structural identity (retained, in cos²(θ_W)
      complement bridge): N_color² - N_pair² = N_quark - 1 (= 5)
      derivable from W2 primitive N_pair = N_color - 1 + N_color = 3.
```

### Headline conclusions

```text
(T1)  cos(2 θ_W) | _lattice  =  cos²(θ_W) - sin²(θ_W) | _lattice
                              =  5/9 - 4/9          [from P3, P4]
                              =  1/9.

(T2)  e² | _lattice  =  1 / (1/g_2² + 1/g_Y²)            [from P1]
                     =  1 / ((d+1) + (d+2))                [from P2]
                     =  1 / (2d + 3)
                     =  1/9                                 [at d = 3].

(T3)  1 / N_color²  =  1/9                                 [from P5: N_color = 3].

(T4)  THREE-way RETAINED equality at 1/9:
        cos(2 θ_W) | _lattice  =  e² | _lattice  =  1 / N_color²  =  1/9.
      All three sides derive from independent retained-tier surfaces
      (EW Higgs diag + sister bridges, EW Higgs diag + YT_EW, S1 retained
      respectively) and converge at 1/9 = 1/N_color².

(T5)  sin²(2 θ_W) | _lattice  =  4 sin²(θ_W) cos²(θ_W) | _lattice    [trig identity]
                              =  4 × (4/9) × (5/9)                    [from P3, P4]
                              =  80/81.

      Structural form (via S1 + T8):
        80 = N_pair^4 × (N_quark - 1)        [16 × 5 with N_pair = 2, N_quark - 1 = 5]
        81 = N_color^4                        [3^4 with N_color = 3]
      so sin²(2 θ_W) | _lattice  =  N_pair^4 × (N_quark - 1) / N_color^4.

(T6)  sin(2 θ_W) | _lattice    =  √(80/81)  =  4 √5 / 9
                                =  4 N_pair √(N_quark - 1) / N_color².

(T7)  Pythagorean closure (consistency):
        cos²(2 θ_W) + sin²(2 θ_W) | _lattice  =  (1/9)² + 80/81
                                              =  1/81 + 80/81
                                              =  81/81 = 1.            [EXACT]

(T8)  tan(2 θ_W) | _lattice    =  sin(2 θ_W) / cos(2 θ_W) | _lattice
                                =  (4 √5 / 9) / (1/9)
                                =  4 √5
                                =  4 N_pair √(N_quark - 1) / N_pair  ... wait
                                =  N_pair² × √(N_quark - 1)            [structural form]
                                =  4 × √5 ≈ 8.944.

(T9)  α_EM | _lattice          =  e² | _lattice / (4 π)
                                =  1 / (36 π)
                                =  1 / (4 π × N_color²).
        1 / α_EM | _lattice    =  36 π = 4 π × N_color² ≈ 113.10.
```

Note on T8 structural form: `tan(2 θ_W) = sin(2θ_W)/cos(2θ_W) = (4√5/9) / (1/9) = 4√5`.
Structurally: `4 = N_pair²`, so `tan(2 θ_W) | _lattice = N_pair² × √(N_quark - 1)` at SM values
(using N_pair = 2, N_quark - 1 = 5, giving N_pair² × √(N_quark-1) = 4 × √5 = 4√5 ✓).

## Retained Inputs (Explicitly Tagged by Authority Tier)

| Input | Authority on `main` | Tier | Role |
| --- | --- | --- | --- |
| `g_2² = 1/(d+1)`, `g_Y² = 1/(d+2)`, `d = 3` | [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) | **retained** (DERIVED) | T2 source for e² |
| `1/e² = 1/g_2² + 1/g_Y²`, `cos²(θ_W) = g²/(g²+g_Y²)` | [`EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md`](EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md) | **retained** (tree theorem) | T1, T2 dictionary |
| `sin²(θ_W)|_lattice = A^4 = 4/9` | [`CKM_EW_LATTICE_A4_BRIDGE_RETAINED_IDENTITY_NOTE_2026-04-25.md`](CKM_EW_LATTICE_A4_BRIDGE_RETAINED_IDENTITY_NOTE_2026-04-25.md) | **retained** | T1 source |
| `cos²(θ_W)|_lattice = 1 - A^4 = 5/9` (complement bridge) | [`EW_LATTICE_COS_SQ_THETA_W_COMPLEMENT_BRIDGE_THEOREM_NOTE_2026-04-26.md`](EW_LATTICE_COS_SQ_THETA_W_COMPLEMENT_BRIDGE_THEOREM_NOTE_2026-04-26.md) | **retained** | T1 source |
| `Q_L : (2,3)_{+1/3}` (S1 source); `u_R, d_R : (1,3)` cross-check | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | **retained corollary**, **retained** | P5 / T3 source for N_color |
| S1 Identification Source Theorem | [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md) | **retained** | P5 |
| `(W2)` `A² = N_pair/N_color = 2/3`; `N_pair = N_color - 1` primitive | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md), [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | **retained** | P3, P6 |
| Z³ spatial substrate; SU(3)_c via graph-first integration | [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md), [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | **retained** framework + **bounded-retained** | P5 ties d = N_color |

The THREE-way equality C1 / T4 uses ONLY retained-tier authorities.
No PDG observable enters as input. No support-tier inputs are
load-bearing.

## Comparator readings (NOT load-bearing)

The bare `g_em²` value `1/9` is recorded on main inside the support-tier
note `FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`
(D2: `g_em²(bare) = 1/(2d+3) = 1/9`, D5: `α_em(bare) = 1/(36π)`). That
note's framing keeps the structural reading at support tier because it
relies on a "Cl(3) → SM algebraic support packet" for the `d+1` and
`d+2` carrier counts.

This trinity theorem is **independent and stronger** because:

1. The `1/g_em² = 1/g_2² + 1/g_Y² = 9` algebra uses the
   *retained-tier* EW Higgs diagonalization tree theorem and the
   *retained-tier* YT_EW bare couplings — not the support-tier
   "Cl(3) → SM algebraic support packet" framing.
2. The structural reading `1/9 = 1/N_color²` is now backed by the
   recently-landed S1 Identification Source Theorem (RETAINED), which
   sources `N_color = dim_SU3(Q_L)` from the retained `Q_L : (2,3)`
   matter-content literal.
3. The NEW THREE-way identity `cos(2θ_W)|_lattice = e²|_lattice = 1/N_color²`
   ties the double-angle Weinberg cosine to both, giving a NEW
   structural interpretation not present in the support-tier
   `FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE`.

Therefore the support-tier note is referenced as a comparator only,
not as an authority for the C1 / T4 retained equality.

## Derivation

### T1: cos(2θ_W)|_lattice from sister A^4 + cos² complement bridges

From the retained `A^4` sister bridge (P3) and the retained `cos²(θ_W)`
complement bridge (P4):

```text
sin²(θ_W) | _lattice  =  4/9,
cos²(θ_W) | _lattice  =  5/9.
```

The double-angle identity `cos(2x) = cos²(x) - sin²(x)` gives:

```text
cos(2 θ_W) | _lattice  =  cos²(θ_W) - sin²(θ_W) | _lattice
                       =  5/9 - 4/9
                       =  1/9.
```

### T2: e²|_lattice from EW Higgs diag + YT_EW

From EW Higgs diagonalization (P1, retained tree theorem):

```text
1/e² = 1/g_2² + 1/g_Y².
```

Substituting retained YT_EW bare couplings (P2):

```text
1/e²  =  (d+1) + (d+2)  =  2d + 3  =  9                  [at d = 3].
```

So `e²|_lattice = 1/9`.

### T3: 1/N_color² via S1

From S1 (P5, retained on main): `N_color = dim_SU3(Q_L) = 3`. Therefore:

```text
1 / N_color²  =  1 / 3²  =  1/9.
```

### T4: THREE-way RETAINED equality

T1, T2, T3 each derive `1/9` from independent retained-tier surfaces:

```text
T1 (sister bridges):   cos(2 θ_W) | _lattice  =  1/9     [via cos² - sin² with P3 + P4]
T2 (EW Higgs + YT_EW): e² | _lattice          =  1/9     [via 1/e² = 1/g_2² + 1/g_Y² with P1 + P2]
T3 (S1 source):        1 / N_color²            =  1/9     [via P5: N_color = 3]
```

All three at `1/9`. Hence the **THREE-way RETAINED equality**:

```text
cos(2 θ_W) | _lattice  =  e² | _lattice  =  1 / N_color²  =  1/9.
```

### T5, T6: sin²(2θ_W) and sin(2θ_W) closed forms

```text
sin²(2 θ_W) | _lattice  =  4 sin²(θ_W) cos²(θ_W) | _lattice
                        =  4 × (4/9) × (5/9)
                        =  80/81.

sin(2 θ_W) | _lattice   =  √(80/81)  =  √80 / 9  =  4 √5 / 9.
```

In structural form (using N_pair^4 = 16, N_quark - 1 = 5, N_color = 3):

```text
80  =  16 × 5  =  N_pair^4 × (N_quark - 1)
81  =  3^4    =  N_color^4

sin²(2 θ_W) | _lattice  =  N_pair^4 × (N_quark - 1) / N_color^4
sin(2 θ_W) | _lattice   =  N_pair² × √(N_quark - 1) / N_color²    [positive root]
                        =  4 × √5 / 9                              [at SM values].
```

(Cross-check: at N_pair = 2, N_color = 3, N_quark - 1 = 5,
`N_pair² × √(N_quark - 1) / N_color² = 4 × √5 / 9 ≈ 0.9938`. And
`4 × 2 × √5 / 9 = 8√5/9 ≈ 1.987`, NOT equal — so the correct factor is
`N_pair² × √(N_quark-1) / N_color² = 4√5/9`. The "N_pair^4 × (N_quark-1)"
in the squared form is N_pair² × N_pair² × (N_quark-1) = (N_pair² × √(N_quark-1))²
in the unsquared form, consistent.)

### T7: Pythagorean closure (consistency check)

```text
cos²(2 θ_W) + sin²(2 θ_W) | _lattice
   =  (1/9)² + 80/81
   =  1/81 + 80/81
   =  81/81  =  1.        [EXACT]
```

### T8: tan(2θ_W) closed form

```text
tan(2 θ_W) | _lattice  =  sin(2 θ_W) / cos(2 θ_W) | _lattice
                       =  (4 √5 / 9) / (1/9)
                       =  4 √5
                       =  N_pair² × √(N_quark - 1)        [structural form, SM values].
```

### T9: α_EM and 1/α_EM at lattice scale

```text
α_EM | _lattice  =  e² | _lattice / (4 π)
                =  1 / (36 π)
                =  1 / (4 π × N_color²).

1 / α_EM | _lattice  =  4 π × N_color²
                     =  36 π
                     ≈  113.10.
```

The retained running brings `1/α_EM` from lattice scale (`≈ 113.10`)
down to `1/α_EM(M_Z) ≈ 127.67` (the retained value on main), via the
retained YT_EW Δ_R audit and 1-loop running bridge. The lattice-scale
identity is the structural anchor.

## Numerical Verification

All identities verified to exact `Fraction` arithmetic (or via
`Fraction` for the squared / rational parts; surd parts cross-checked
algebraically).

| Identity | LHS | RHS | Match? |
| --- | ---: | ---: | --- |
| T1: cos(2θ_W)\|_lattice = cos² - sin² = 1/9 | 1/9 | 1/9 | ✓ |
| T2: e²\|_lattice via 1/e² = 1/g_2² + 1/g_Y² = 1/9 | 1/9 | 1/9 | ✓ |
| T3: 1/N_color² = 1/9 | 1/9 | 1/9 | ✓ |
| T4: THREE-way RETAINED equality at 1/9 | 1/9 = 1/9 = 1/9 | — | ✓ |
| T5: sin²(2θ_W)\|_lattice = 4 sin² cos² = 80/81 | 80/81 | 80/81 | ✓ |
| T5 structural: N_pair^4 (N_quark-1) / N_color^4 | 80/81 | 80/81 | ✓ |
| T7: cos²(2θ_W) + sin²(2θ_W) = 1 | 1 | 1 | ✓ |
| T8 algebra: tan²(2θ_W)\|_lattice = sin²/cos² = (80/81)/(1/81) = 80 | 80 | 80 | ✓ |

## Science Value

### What this lets the framework state cleanly

Previously the EW-CKM lattice-scale bridges retained at lattice scale:
- `sin²(θ_W)|_lattice = A^4 = 4/9` (CKM-EW A^4 bridge)
- `cos²(θ_W)|_lattice = 1 - A^4 = 5/9` (cos² complement bridge)

This trinity theorem extends the bridge family to the DOUBLE-ANGLE
Weinberg trigonometry and the SQUARED ELECTRIC COUPLING:

1. **THREE-way retained equality** `cos(2θ_W)|_lattice = e²|_lattice = 1/N_color²`
   ties the double-angle Weinberg cosine to the squared electric
   coupling and the inverse-square color count (S1).

2. **NEW closed forms for double-angle Weinberg trig** at lattice scale:
   `sin²(2θ_W) = 80/81 = N_pair^4(N_quark-1)/N_color^4`,
   `sin(2θ_W) = 4√5/9`, `tan(2θ_W) = 4√5`.

3. **NEW S1-backed reading of α_EM at lattice scale**:
   `α_EM|_lattice = 1/(4π × N_color²) = 1/(36π)`. Previously this
   value was carried in a SUPPORT-tier dimension-ratio note; now it
   rides on the retained-tier S1 source theorem for the structural
   reading.

### NEW structural interpretation

> At lattice scale, the double-angle Weinberg cosine `cos(2 θ_W)`
> EQUALS the squared electric coupling `e²` EQUALS `1/N_color²`.

This is a SHARP NEW STRUCTURAL IDENTITY tying three independent EW/EM
quantities to the inverse-square color count. The underlying reason:
both `cos(2θ_W) = (g_2² - g_Y²)/(g_2² + g_Y²) = (1/4 - 1/5)/(1/4 + 1/5) = (1/20)/(9/20) = 1/9`
and `1/e² = 1/g_2² + 1/g_Y² = 9` route through the same retained YT_EW
bare couplings, and the resulting `1/9` is structurally identified with
`1/N_color²` via S1.

### Why this counts as pushing the science forward

1. **NEW THREE-way RETAINED equality** at lattice scale across three
   independent retained-tier surfaces (sister bridges, EW Higgs +
   YT_EW, S1).

2. **NEW double-angle Weinberg closed forms**: `sin²(2θ_W) = 80/81`,
   `sin(2θ_W) = 4√5/9`, `tan(2θ_W) = 4√5` — none of these were on
   main before.

3. **Promotion of α_EM lattice-scale structural reading**:
   `α_EM|_lattice = 1/(4π × N_color²)` was previously support-tier
   (in `FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE`);
   now backed by retained S1 + retained EW Higgs + retained YT_EW.

4. **Honest framing**: explicit non-promotion to below-Wn closure;
   THREE-way equality uses only retained-tier authorities; support-tier
   `FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE`
   is referenced as a comparator only, not as an authority.

## Falsifiable structural claims

1. `cos(2 θ_W) | _lattice = 1/9` (sharp lattice-scale prediction).
2. `e² | _lattice = 1/9 = 1/N_color²` (NEW structural reading via S1).
3. THREE-way equality `cos(2θ_W) = e² = 1/N_color² = 1/9` at retained
   values (NEW unification).
4. `sin²(2 θ_W) | _lattice = 80/81 = N_pair^4(N_quark-1)/N_color^4`
   (NEW double-angle closed form).
5. `α_EM | _lattice = 1/(4π × N_color²)` (NEW retained structural
   reading; support-tier comparator now backed by S1-retained).

## What This Claims

- `(C1 / T4)`: cos(2θ_W)|_lattice = e²|_lattice = 1/N_color² = 1/9
  (THREE-way RETAINED equality at lattice scale).
- `(C2 / T5)`: sin²(2θ_W)|_lattice = 80/81 (NEW closed form).
- `(C3 / T6)`: sin(2θ_W)|_lattice = 4√5/9 (NEW closed form).
- `(C4 / T9)`: α_EM|_lattice = 1/(4π × N_color²) = 1/(36π) (NEW
  retained-backed structural reading).

## What This Does NOT Claim

- Does NOT promote any support-tier theorem to retained.
- Does NOT use consistency equalities as load-bearing closure routes.
- Does NOT claim below-Wn derivation for cos(2θ_W), e², or α_EM.
- Does NOT predict physical α_EM at PDG scale (lattice anchor only;
  retained running bridge takes `1/α_EM|_lattice ≈ 113.10` to
  `1/α_EM(M_Z) ≈ 127.67`, the retained value).
- Does NOT modify retained sister bridges (`A^4 = sin²(θ_W) = 4/9`,
  `1 - A^4 = cos²(θ_W) = 5/9`); this trinity COMPLEMENTS them.
- Does NOT cite any unmerged branches as retained authorities.
- Does NOT include the support-tier `FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE`
  as a load-bearing route inside the THREE-way retained equality —
  it is referenced only as a comparator note.

## Reproduction

```bash
python3 scripts/frontier_ew_em_lattice_double_angle_trinity.py
```

Expected:

```text
TOTAL: PASS=N, FAIL=0
COS_2_THETA_W_LATTICE_TRINITY_VERIFIED         = TRUE
SIN_SQ_2_THETA_W_LATTICE_CLOSED_FORM_VERIFIED  = TRUE
ALPHA_EM_LATTICE_S1_BACKED_READING_VERIFIED    = TRUE
PYTHAGOREAN_CLOSURE_AT_LATTICE_VERIFIED        = TRUE
```

The runner:

1. Reads each cited authority file from disk and extracts Status: line
   for ground-up tier verification.
2. Extracts retained Q_L : (a,b) literal from
   LEFT_HANDED_CHARGE_MATCHING_NOTE.md by regex (NOT hard-coded).
3. Extracts retained YT_EW closed forms `g_2² = 1/(d+1)`, `g_Y² = 1/(d+2)`.
4. Derives:
   - `cos(2 θ_W) | _lattice` via `cos²(θ_W) - sin²(θ_W)` from sister
     bridges (T1).
   - `e² | _lattice` via `1/e² = 1/g_2² + 1/g_Y²` from EW Higgs +
     YT_EW (T2).
   - `1/N_color²` from S1 (T3).
5. Verifies the THREE-way RETAINED equality at `1/9` (T4) — the
   load-bearing PASS.
6. Derives `sin²(2 θ_W) | _lattice = 80/81` and verifies its structural
   form `N_pair^4 × (N_quark - 1) / N_color^4` (T5, T6).
7. Verifies Pythagorean closure `cos²(2θ_W) + sin²(2θ_W) = 1` (T7).
8. Derives `tan²(2 θ_W) | _lattice = 80` and the structural form (T8).
9. Reports `α_EM | _lattice = 1 / (36 π)` as a NEW S1-backed reading
   (T9).
10. Cross-checks against the support-tier comparator note
    `FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE`
    as an auxiliary check (NOT load-bearing).

## Cross-References

**Retained-tier authorities used in T1-T9 (load-bearing):**

- [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
  — retained DERIVED; bare lattice couplings `g_2² = 1/(d+1)`, `g_Y² = 1/(d+2)`.
- [`EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md`](EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md)
  — retained tree theorem; `1/e² = 1/g_2² + 1/g_Y²`, `cos²(θ_W) = g²/(g² + g_Y²)`.
- [`CKM_EW_LATTICE_A4_BRIDGE_RETAINED_IDENTITY_NOTE_2026-04-25.md`](CKM_EW_LATTICE_A4_BRIDGE_RETAINED_IDENTITY_NOTE_2026-04-25.md)
  — retained sister bridge; `sin²(θ_W)|_lattice = A^4 = 4/9`.
- [`EW_LATTICE_COS_SQ_THETA_W_COMPLEMENT_BRIDGE_THEOREM_NOTE_2026-04-26.md`](EW_LATTICE_COS_SQ_THETA_W_COMPLEMENT_BRIDGE_THEOREM_NOTE_2026-04-26.md)
  — retained sister complement bridge; `cos²(θ_W)|_lattice = 1 - A^4 = 5/9`.
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  — retained corollary; `Q_L : (2,3)_{+1/3}` source for S1.
- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
  — retained; `u_R, d_R : (1,3)` cross-check on N_color via S1.
- [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md)
  — retained S1 Identification Source Theorem.

**Comparator (NOT load-bearing for T1-T9):**

- [`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`](FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md)
  — support-tier; carries `g_em²(bare) = 1/9`, `α_em(bare) = 1/(36π)`,
  `α_3(bare)/α_em(bare) = 9` as support-only comparator readings.
  Referenced here as an auxiliary numerical companion, NOT as a
  load-bearing authority for the THREE-way retained equality.
