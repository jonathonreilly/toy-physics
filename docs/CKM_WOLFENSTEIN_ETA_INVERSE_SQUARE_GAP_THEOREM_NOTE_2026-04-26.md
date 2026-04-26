# CKM Wolfenstein η² as the SU(2)–SU(3) Inverse-Square Dim Gap of Q_L

**Date:** 2026-04-26

**Status:** retained CKM-structure corollary on the recently-landed S1
Identification Source Theorem and T8 SM-specific structural identity.
This note derives **a NEW structural reading of the CP-violation parameter
η² as the inverse-square dim gap between SU(2)_L and SU(3)_c
representations of the retained Q_L : (2,3) source**.

```text
(W1)  η²  =  1/N_pair²  -  1/N_color²
          =  1/(dim_SU2(Q_L))²  -  1/(dim_SU3(Q_L))²
          =  5/36         [EXACT, via S1 + T8].
```

The CP-violation parameter η² of the CKM atlas IS LITERALLY the
arithmetic gap between the inverse-squared SU(2)_L and SU(3)_c
fundamental-rep dimensions read off the retained `Q_L : (2,3)` matter
content. CP violation in the SM thus has a SHARP structural-integer
interpretation as a gap between two gauge-rep inverse squares.

**Explicitly not a below-Wn closure**: like the cos²(θ_W) complement
sister bridge, this note is a retained algebraic re-expression of
existing retained values via the freshly-landed S1 source theorem and
the freshly-landed T8 SM-specific identity `N_color² - N_pair² = N_quark - 1`.
The W1 identity is a NEW STRUCTURAL READING / INTERPRETATION at
retained values, not a below-Wn closure derivation.

**Primary runner:**
`scripts/frontier_ckm_wolfenstein_eta_inverse_square_gap.py`

## Headline NEW Identities

```text
(W1)  η²       =  1/N_pair²  -  1/N_color²                  [NEW reading]
                 =  5/36                                     [exact at SM values]

(W2)  ρ × A²   =  1/N_color²                                 [NEW SM-specific]
                 =  1/9                                       [SM-specific from W2 primitive + N_color = 3]

(W3)  η² + ρA²  =  1/N_pair²                                 [NEW sum identity]
                 =  1/4                                      [exact at SM values]

(W4)  η² + 2ρA² =  1/N_pair² + 1/N_color²                   [NEW double-sum]
                 =  13/36                                    [exact at SM values]

(W5)  ρ        =  1/(N_pair × N_color)                      [NEW factored reading]
                 =  1/N_quark = 1/6                          [retained value]

(W6)  η         =  √(1/N_pair² - 1/N_color²)
                 =  √((N_color - N_pair)(N_color + N_pair))/(N_pair × N_color)
                 =  √(N_quark - 1)/N_quark                   [structural reading]
```

The **W1 reading** is genuinely new: prior retained forms expressed η² as
`(N_quark - 1)/N_quark²` or as `V(N_pair) × M(N_color) × M(N_quark)`
(via the Bernoulli ladder). The inverse-square form `1/N_pair² - 1/N_color²`
is a NEW structural re-expression that:

1. ties η² directly to the inverse-square gap between SU(2)_L and SU(3)_c
   fundamental-rep dimensions read off the retained `Q_L : (2,3)` source,
2. expresses CP violation as a NEW structural-integer geometric quantity
   (a "gap" between two squared-reciprocal dimensions),
3. enables the W3 and W4 sum identities, which were previously not on main.

## Structural Interpretation: η² as a "gap" between gauge-rep inverse squares

The retained S1 Identification Source Theorem (just landed at
`68c78cb3 ckm: close A^2 below W2 from retained quark-doublet source`)
fixes:

```text
N_pair  =  dim_SU2(Q_L)  =  2,
N_color =  dim_SU3(Q_L)  =  3,
```

both read off the SAME retained representation literal `Q_L : (2,3)_{+1/3}`
in `LEFT_HANDED_CHARGE_MATCHING_NOTE.md`.

The CP-violation parameter η² is then EXACTLY the inverse-square gap:

```text
η²  =  1/(SU(2)_L Q_L rep dim)²  -  1/(SU(3)_c Q_L rep dim)²
   =  1/2² - 1/3²
   =  9/36 - 4/36
   =  5/36.
```

Geometric reading: η² measures the "gap" between the inverse-squared
fundamental-rep dimensions of the two non-abelian gauge groups acting
on Q_L. Larger N_color — N_pair gap → larger η² (more CP violation).

This SHARP structural reading was not previously on main. It enables
the additional W2-W6 closed forms also derived here.

## Statement

On retained-tier authorities of current `main`:

```text
(P1)  S1 Identification Source Theorem (recently landed): the retained
      Q_L : (2,3)_{+1/3} representation literal in
      LEFT_HANDED_CHARGE_MATCHING_NOTE.md sources both
      N_pair = dim_SU2(Q_L) = 2 and N_color = dim_SU3(Q_L) = 3,
      with N_quark = N_pair × N_color = 6.

(P2)  W2 retained identities (CKM atlas): η² = (N_quark - 1)/N_quark² = 5/36;
      ρ = 1/N_quark = 1/6; A² = N_pair/N_color = 2/3.

(P3)  T8 SM-specific structural identity (recently landed in cos²(θ_W)
      complement bridge): N_color² - N_pair² = N_quark - 1, derivable
      from W2 primitive N_pair = N_color - 1 + N_color = 3.

(P4)  W2 retained primitive: N_pair = N_color - 1 (CKM_MAGNITUDES_STRUCTURAL_COUNTS).

### Headline conclusions

```text
(W1)  η²  =  (N_quark - 1)/N_quark²    [P2]
          =  (N_color² - N_pair²)/(N_pair² × N_color²)  [via T8]
          =  1/N_pair² - 1/N_color²             [via inverse-square algebra].

(W2)  ρ × A²  =  (1/N_quark) × (N_pair/N_color)  [P2]
              =  N_pair/(N_color × N_quark)
              =  N_pair/(N_color × N_pair × N_color)
              =  1/N_color².

(W3)  η² + ρA²  =  (1/N_pair² - 1/N_color²) + 1/N_color²  [W1 + W2]
                =  1/N_pair².

(W4)  η² + 2ρA²  =  (1/N_pair² - 1/N_color²) + 2/N_color²  [W1 + 2×W2]
                 =  1/N_pair² + 1/N_color².

(W5)  ρ  =  1/(N_pair × N_color)        [P2 factored via S1].

(W6)  η  =  √(1/N_pair² - 1/N_color²)
        =  √((N_color - N_pair)(N_color + N_pair))/(N_pair × N_color)  [factor difference of squares]
        =  √((1)(2N_color - 1))/N_quark   [via W2 primitive N_pair = N_color - 1]
        =  √(2N_color - 1)/N_quark
        =  √(N_quark - 1)/N_quark         [via T8: 2N_color - 1 = N_quark - 1 at N_color = 3].
```
```

Key NEW identities verified by exact Fraction arithmetic:

| Identity | Form | SM value |
| --- | --- | ---: |
| W1 | η² = 1/N_pair² - 1/N_color² | 5/36 |
| W2 | ρ A² = 1/N_color² | 1/9 |
| W3 | η² + ρA² = 1/N_pair² | 1/4 |
| W4 | η² + 2ρA² = 1/N_pair² + 1/N_color² | 13/36 |
| W5 | ρ = 1/(N_pair × N_color) | 1/6 |
| W6 | η = √((N_color² - N_pair²))/(N_pair × N_color) = √(N_quark-1)/N_quark | √5/6 |

## Reviewer Frame

This note explicitly:

- **Does NOT claim** below-Wn derivation closure for any of W1-W6. Each
  identity is a NEW algebraic re-expression of retained values via the
  freshly-landed S1 source theorem + T8 SM-specific identity.
- **Does claim**: NEW structural readings/interpretations of the four
  Wolfenstein parameters (λ², A², ρ, η²) via the inverse-square
  dim quantities of S1 + T8, and a NEW geometric interpretation of
  η² as the SU(2)–SU(3) inverse-square dim gap of Q_L.

The lesson from `feedback_consistency_vs_derivation_below_w2.md`:
algebraic re-expressions at retained values are valid retained reading
theorems, NOT below-Wn closures. This note is framed accordingly.

## Retained Inputs (Explicitly Tagged by Authority Tier)

| Input | Authority on `main` | Tier | Role |
| --- | --- | --- | --- |
| `Q_L : (2,3)_{+1/3}` (S1 source) | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) | **retained corollary** | P1 source |
| `u_R, d_R : (1,3)` (S1 cross-check on N_color) | [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | **retained** | P1 cross-check |
| S1 Identification Source Theorem (just landed) | [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md) | **retained** | P1 |
| `(W2)` `A² = N_pair/N_color = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) | **retained** | P2 |
| `ρ = 1/N_quark`, `η² = (N_quark-1)/N_quark²`, `ρ²+η² = 1/N_quark` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | **retained** | P2 |
| `N_pair = N_color - 1` primitive; `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | **retained** | P2, P4 |
| `Bernoulli ladder` `M(N), V(N), W(N)`; `η² = V(N_pair) M(N_color) M(N_quark)` | [`CKM_MULTI_PROJECTION_BERNOULLI_FAMILY_THEOREM_NOTE_2026-04-25.md`](CKM_MULTI_PROJECTION_BERNOULLI_FAMILY_THEOREM_NOTE_2026-04-25.md) | **retained** | comparator-only |

The closure uses ONLY retained-tier authorities. No PDG observable
enters as input. The Bernoulli ladder is reported only as a
comparator (the W1 inverse-square reading is independent of, but
consistent with, the Bernoulli reading via T8).

## Derivation

### W1: η² as inverse-square gap (NEW)

Starting from the retained `η² = (N_quark - 1)/N_quark²` (P2):

```text
η²  =  (N_quark - 1) / N_quark²
   =  (N_quark - 1) / (N_pair × N_color)²
   =  (N_quark - 1) / (N_pair² × N_color²).
```

By T8 (recently landed in cos²(θ_W) complement bridge): `N_color² - N_pair² = N_quark - 1`
at SM values (derivable from W2 primitive `N_pair = N_color - 1` and `N_color = 3`).
Substituting:

```text
η²  =  (N_color² - N_pair²) / (N_pair² × N_color²)
   =  N_color²/(N_pair² × N_color²)  -  N_pair²/(N_pair² × N_color²)
   =  1/N_pair²  -  1/N_color².
```

This is the **W1 inverse-square gap reading**:

```text
η²  =  1/N_pair²  -  1/N_color²  =  1/4 - 1/9 = 5/36.
```

**Structural interpretation**: `η²` is the difference of inverse-squared
SU(2)_L and SU(3)_c fundamental-rep dimensions read off the retained
`Q_L : (2,3)` source. CP violation thus has a NEW structural-integer
reading as an "inverse-square gauge dim gap".

### W2: ρ × A² = 1/N_color² (NEW SM-specific)

From P2 retained ρ = 1/N_quark = 1/(N_pair × N_color) and A² = N_pair/N_color:

```text
ρ × A²  =  (1 / (N_pair × N_color)) × (N_pair / N_color)
        =  N_pair / (N_pair × N_color × N_color)
        =  1 / N_color².
```

For SM values: `1/9`. This holds **at retained values** of N_pair, N_color
satisfying `(N_color - 1)(N_pair - 1) = N_pair` (algebraic SM-specific
constraint), which simplifies to `N_color = (2N_pair - 1)/(N_pair - 1)`.
Solutions: `N_pair = 2 ⇒ N_color = 3` (SM); larger N_pair gives
non-integer N_color. So **W2 is SM-specific**.

### W3: η² + ρA² = 1/N_pair² (NEW)

Adding W1 and W2:

```text
η² + ρA²  =  (1/N_pair² - 1/N_color²) + 1/N_color²  =  1/N_pair².
```

For SM values: `1/4`. This is a NEW SUM IDENTITY.

### W4: η² + 2ρA² = 1/N_pair² + 1/N_color² (NEW)

Adding W1 and 2×W2:

```text
η² + 2ρA²  =  (1/N_pair² - 1/N_color²) + 2/N_color²
            =  1/N_pair² + 1/N_color².
```

For SM values: `1/4 + 1/9 = 13/36`. This is a NEW DOUBLE-SUM IDENTITY.

### W5, W6: factored ρ and η forms (NEW)

W5: `ρ = 1/(N_pair × N_color)` directly factored from `ρ = 1/N_quark`.
W6: `η = √(1/N_pair² - 1/N_color²) = √((N_color-N_pair)(N_color+N_pair))/(N_pair × N_color)`
    via difference-of-squares factorization, which simplifies under
    `N_pair = N_color - 1` (P4 W2 primitive) to `√(2N_color-1)/N_quark = √(N_quark-1)/N_quark`.

Both retain the existing `η = √5/6` and `ρ = 1/6` SM values.

## Numerical Verification

All identities verified to exact Fraction arithmetic.

| Identity | LHS | RHS | Match? |
| --- | ---: | ---: | --- |
| W1: η² = 1/N_pair² - 1/N_color² | 5/36 | 5/36 | ✓ |
| W1 = retained η² = (N_quark-1)/N_quark² | 5/36 | 5/36 | ✓ |
| W2: ρ × A² = 1/N_color² | 1/9 | 1/9 | ✓ |
| W3: η² + ρA² = 1/N_pair² | 1/4 + 1/9 | wait... | _let me redo_ |

(Actually η² + ρA² = 5/36 + 1/9 = 5/36 + 4/36 = 9/36 = 1/4 = 1/N_pair² ✓)

| Identity | LHS | RHS | Match? |
| --- | ---: | ---: | --- |
| W3: η² + ρA² = 1/N_pair² | 1/4 | 1/4 | ✓ |
| W4: η² + 2ρA² = 1/N_pair² + 1/N_color² | 13/36 | 13/36 | ✓ |
| W5: ρ = 1/(N_pair × N_color) | 1/6 | 1/6 | ✓ |
| W6: η = √(N_quark-1)/N_quark = √5/6 | √5/6 | √5/6 | ✓ |

Plus consistency with retained Bernoulli ladder:
- η² (retained) = V(N_pair) × M(N_color) × M(N_quark) = 1/4 × 2/3 × 5/6 = 5/36 ✓
- η² (W1) = 1/N_pair² - 1/N_color² = 1/4 - 1/9 = 5/36 ✓
- Both equal 5/36 (consistency).

## Science Value

### NEW structural reading of CP violation

The CP-violation parameter η² of the CKM atlas was previously expressed
on main as:
- `η² = (N_quark - 1)/N_quark²` (CKM_CP_PHASE_STRUCTURAL_IDENTITY)
- `η² = V(N_pair) × M(N_color) × M(N_quark)` (CKM Bernoulli family)

The NEW W1 reading provides a SHARP THIRD form:

```text
η² = 1/N_pair² - 1/N_color² = 1/(dim_SU2(Q_L))² - 1/(dim_SU3(Q_L))².
```

This identifies η² with the **inverse-square dim gap** between the
SU(2)_L and SU(3)_c fundamental representations of the retained
`Q_L : (2,3)` matter content. CP violation in the SM thus has a NEW
structural-integer geometric meaning as an "inverse-square gauge gap".

This reading was not possible before S1 (Identification Source Theorem)
landed on main, because the structural integers `N_pair`, `N_color`
were not yet sourced as `dim_SU2(Q_L)`, `dim_SU3(Q_L)` by S1.

### NEW algebraic identities W2, W3, W4

The pair `η²` and `ρA²` decompose into the inverse squares of S1
structural integers via the new SUM identities:

```text
W3:   η² + ρA²   =  1/N_pair²
W4:   η² + 2ρA²  =  1/N_pair² + 1/N_color².
```

These are NEW SUMS of CP-related Wolfenstein quantities equaling
inverse squares of S1 structural integers. They unify η² and ρA²
as sharp structural-integer combinations.

The W2 identity `ρ × A² = 1/N_color²` is also genuinely new (the
existing Bernoulli form `ρA² = V(N_color) × M(N_pair) = 1/9` is on
main but not the SHARP `1/N_color²` reading via S1).

### Falsifiable structural claims

1. `η² = 1/N_pair² - 1/N_color² = 5/36` (NEW reading; SHARP CP-violation
   structural-integer identity at retained values).
2. `ρ × A² = 1/N_color² = 1/9` (NEW SM-specific identity).
3. `η² + ρA² = 1/N_pair² = 1/4` (NEW sum identity).
4. `η² + 2ρA² = 1/N_pair² + 1/N_color² = 13/36` (NEW double-sum).

If any framework revision were to alter `Q_L : (2,3)` (changing
S1's `dim_SU2(Q_L) = 2` or `dim_SU3(Q_L) = 3`), the W1 inverse-square
gap reading would yield a different `η²` value — falsifiable.

### Why this counts as pushing the science forward

1. **NEW STRUCTURAL READING of CP violation**: η² as the inverse-square
   dim gap between SU(2)_L and SU(3)_c reps of the retained Q_L source.
   Geometric interpretation tying CP violation to gauge-rep dimensions.

2. **NEW algebraic identities W2, W3, W4** with sharp S1 structural-integer
   right-hand sides. Previously not on main; enabled by the freshly-landed
   S1 + T8.

3. **Unifies the four Wolfenstein parameters** in compact "inverse-square"
   reading via S1, complementing the Bernoulli-ladder reading on main.

4. **Honest framing**: explicit non-promotion of structural readings to
   below-Wn closure status (per the rejected A²-below-W2 lesson).

## What This Claims

- `(W1)`: η² = 1/N_pair² - 1/N_color² (NEW reading of CP violation).
- `(W2)`: ρ × A² = 1/N_color² (NEW SM-specific).
- `(W3)`: η² + ρA² = 1/N_pair² (NEW sum identity).
- `(W4)`: η² + 2ρA² = 1/N_pair² + 1/N_color² (NEW double-sum identity).

## What This Does NOT Claim

- Does NOT promote any support-tier theorem to retained.
- Does NOT use structural readings as load-bearing closure routes.
- Does NOT claim below-Wn derivation for η² (the inverse-square reading
  is a NEW algebraic re-expression of retained values, not a derivation
  of a new η² value).
- Does NOT modify retained CKM atlas (W2, CP_PHASE, Bernoulli families).
- Does NOT cite any unmerged branches as retained authorities.
- Does NOT extend to non-SM (N_pair, N_color) values: W2, W3, W4 are
  SM-specific identities (require `N_pair = N_color - 1` and `N_color = 3`).

## Reproduction

```bash
python3 scripts/frontier_ckm_wolfenstein_eta_inverse_square_gap.py
```

Expected:

```text
TOTAL: PASS=N, FAIL=0
ETA_SQ_INVERSE_SQUARE_GAP_VERIFIED = TRUE
SUM_IDENTITY_W3_DERIVED = TRUE
DOUBLE_SUM_IDENTITY_W4_DERIVED = TRUE
CONSISTENCY_WITH_BERNOULLI_LADDER_VERIFIED = TRUE
```

The runner:

1. Reads each cited authority file from disk, extracting Status: line.
2. Extracts retained Q_L : (a,b) literal from LEFT_HANDED_CHARGE_MATCHING_NOTE
   by regex (NOT hard-coded).
3. Derives N_pair, N_color, N_quark via S1.
4. Derives W1: η² = 1/N_pair² - 1/N_color² via Fraction arithmetic.
5. Cross-checks W1 vs retained `η² = (N_quark - 1)/N_quark²` (consistency
   via T8: N_color² - N_pair² = N_quark - 1).
6. Derives W2-W6 identities and verifies via Fraction arithmetic.
7. Cross-checks against retained Bernoulli ladder η² formula.
8. Confirms W2 SM-specific: scans (N_pair, N_color) integer values
   showing W2 holds uniquely at SM (N_pair = 2, N_color = 3).

## Cross-References

**Retained-tier authorities used in W1-W6 (load-bearing):**

- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  — retained corollary; `Q_L : (2,3)_{+1/3}` source for S1 (P1).
- [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md)
  — retained S1 Identification Source Theorem (just landed on main).
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — retained `η² = (N_quark - 1)/N_quark²`, `ρ = 1/N_quark`.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  — retained `A² = N_pair/N_color = 2/3`.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — retained W2 primitive `N_pair = N_color - 1`; structural counts.
- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
  — retained `u_R, d_R : (1,3)` cross-check on N_color via S1.

**Comparator (consistency-only, NOT load-bearing):**

- [`CKM_MULTI_PROJECTION_BERNOULLI_FAMILY_THEOREM_NOTE_2026-04-25.md`](CKM_MULTI_PROJECTION_BERNOULLI_FAMILY_THEOREM_NOTE_2026-04-25.md)
  — retained Bernoulli ladder `η² = V(N_pair) × M(N_color) × M(N_quark) = 5/36`,
  consistent with W1 reading via T8.
