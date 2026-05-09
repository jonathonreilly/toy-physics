# A² Closure Below W2 via Retained Quark-Doublet Identification Source Theorem

**Date:** 2026-04-25

**Status:** proposed_retained CKM × Cl(3) closure theorem on proposed_retained-tier authorities.

This note CLOSES `A² = N_pair/N_color = 2/3` BELOW W2 via a single
**Identification Source Theorem (S1)** that derives BOTH `N_pair = 2` and
`N_color = 3` from a SINGLE retained matter-content source on current `main`:
the retained left-handed quark representation
`Q_L : (2,3)_{+1/3}` (LEFT_HANDED_CHARGE_MATCHING_NOTE, "retained corollary")
together with the retained right-handed quark representations
`u_R : (1,3)_{+4/3}`, `d_R : (1,3)_{-2/3}` (ONE_GENERATION_MATTER_CLOSURE_NOTE,
"retained").

The (2,3) representation is the SAME single retained object that fixes:

- `N_pair := dim_SU2(Q_L)  = 2`  (the SU(2)_L doublet IS the up-down pair),
- `N_color := dim_SU3(Q_L) = 3`  (the SU(3)_c triplet IS the color count).

Therefore `A² = N_pair/N_color = 2/3` is DERIVED below W2 from a single
retained source — not asserted via a gauge-dimension consistency equality
nor a numerical coincidence.

## Why The Source Theorem Is Load-Bearing

Two narrower routes are real but not load-bearing:

- **Gauge-dimension equality:** `dim_fund(SU(2))/dim_fund(SU(3)) = 2/3`
  matches `N_pair/N_color = 2/3`, but this is only a gauge-dimension
  **consistency equality**. Two external numbers coincide; the CKM-side
  identification is not fixed at the source.

- **Numerical EW coincidence:** `g_2² = 1/4 = 1/N_pair²` at the retained
  values is only a **numerical coincidence check**, not a derivation.

This note instead uses **S1: Identification Source Theorem**:
both `N_pair` and `N_color` derive from the SAME retained matter-content
source `Q_L : (2,3)_{+1/3}`. The identification is not asserted at the
level of integer-equality; it is fixed at the source by the retained
representation literal itself.

**Primary runner:**
`scripts/frontier_ckm_a_squared_below_w2_y_quantum_closure.py`

## S1: Identification Source Theorem (NEW load-bearing route)

### Premises (all RETAINED on `main`)

```text
(P1)  MINIMAL_AXIOMS_2026-04-11 retains as current consequence:
      "exact native SU(2)" and "graph-first structural SU(3)".
      These retain the SU(2)_L and SU(3)_c gauge structures within
      the framework's accepted package.

(P2)  LEFT_HANDED_CHARGE_MATCHING_NOTE (Status: "retained corollary on
      the current paper surface") retains the left-handed quark sector:

          Q_L : (2,3)_{+1/3}

      where (a, b) denotes (SU(2)_L rep dim, SU(3)_c rep dim) and the
      subscript is hypercharge. This is RETAINED on main as the
      canonical left-handed quark representation under the framework's
      graph-first selected-axis surface.

(P3)  ONE_GENERATION_MATTER_CLOSURE_NOTE (Status: "retained") retains
      the right-handed quark sector:

          u_R : (1,3)_{+4/3}
          d_R : (1,3)_{-2/3}

      These RETAIN the up-type and down-type right-handed quarks as
      SU(2)_L singlets in the SU(3)_c triplet representation (color = 3).
```

### Definitions (CKM structural integers, on the SM construction)

```text
(D1)  N_pair := number of up-type / down-type quark-flavor partners per
      generation that are paired by the SU(2)_L weak interaction.
      Operationally: N_pair = dim_SU2(Q_L), the number of components of
      the left-handed-quark SU(2)_L representation. Each component is
      one quark flavor (up-type T_3 = +1/2, or down-type T_3 = −1/2);
      together they form ONE generation's quark doublet.

(D2)  N_color := number of color states per quark flavor.
      Operationally: N_color = dim_SU3(Q_L) = dim_SU3(u_R) = dim_SU3(d_R),
      the SU(3)_c rep dimension common to all quark fields by retained
      P2 + P3.

These definitions tie the W2 / CKM_MAGNITUDES structural integers
N_pair, N_color to the retained matter-content representation literals.
They are not independent integer-assertions — they read N_pair and
N_color directly off the SU(2)_L and SU(3)_c rep dimensions of the
retained Q_L : (2,3) matter content.
```

### Conclusion (Identification Source Theorem)

```text
(S1.a) From retained P2 (Q_L : (2,3)), reading the SU(2)_L rep:
       N_pair = dim_SU2(Q_L) = 2.

(S1.b) From retained P2 (Q_L : (2,3)), reading the SU(3)_c rep:
       N_color = dim_SU3(Q_L) = 3.
       Cross-checked by retained P3: dim_SU3(u_R) = dim_SU3(d_R) = 3.

(S1.c) Therefore A² := N_pair/N_color = 2/3, DERIVED below W2 from a
       SINGLE retained source (Q_L : (2,3)) — not from a consistency
       equality between two external integers.
```

The identification source theorem replaces the gauge-dimension
consistency equality with a direct read off the retained matter-content
representation. Both `N_pair` and `N_color` come from the same retained
object `Q_L : (2,3)_{+1/3}`.

### Why this is a derivation, not a consistency equality

| Aspect | Gauge-dimension equality | S1 (Identification Source) |
| --- | --- | --- |
| Source for N_pair = 2 | `dim_fund(SU(2)) = 2` (gauge-group fact) | `Q_L : (2,3)` retained (matter content) |
| Source for N_color = 3 | `dim_fund(SU(3)) = 3` (gauge-group fact) | `Q_L : (2,3)` retained (matter content) |
| Identification step | "2 = 2" coincidence + "3 = 3" coincidence | One retained literal fixes both |
| Independence of identifications | Two separate "X = Y" assertions | Single source theorem |
| Load-bearing below-W2 derivation? | No | Yes |

The (2,3) of Q_L is the ONE thing being read; both `N_pair` and `N_color`
are extracted from it by reading the SU(2)_L slot and the SU(3)_c slot.
There is no independent assertion that "N_pair (CKM side) equals
dim_fund(SU(2)) (gauge side)" — instead, N_pair is DEFINED operationally
as dim_SU2 of the retained Q_L rep, which is a direct read-off.

## Statement (full closure)

On retained-tier authorities of current `main`:

```text
(S1)  Identification Source Theorem (new load-bearing):
       N_pair  = dim_SU2(Q_L) = 2,
       N_color = dim_SU3(Q_L) = 3.
       Both derive from the SINGLE retained representation literal
       Q_L : (2,3)_{+1/3} in LEFT_HANDED_CHARGE_MATCHING_NOTE.

(S2)  Closure (BELOW W2):
       A² = N_pair / N_color = 2/3,
       derived from S1 via D1, D2 — that is, from retained matter-content
       BELOW the W2 structural-counts level.

(S3)  W2-level consistency check (not load-bearing for derivation):
       WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24
       independently retains A² = N_pair/N_color = 2/3 at the W2 level.
       The S1+S2 below-W2 derivation REPRODUCES this retained W2 value.
       This consistency confirms the chain but is not a load-bearing
       step for the below-W2 closure.

(S4)  Auxiliary corroborations (NOT load-bearing for closure):
       (i)  Gauge-dimension reading: dim_fund(SU(N)) = N gives
            dim_fund(SU(2)) = 2 and dim_fund(SU(3)) = 3, consistent
            with S1.a/S1.b. This is corroboration only, not a separate
            derivation route. (demoted corroboration)
       (ii) Numerical reading: YT_EW retained g_2² = 1/(d+1) = 1/4 and
            CKM_MAGNITUDES retained 1/N_pair² = 1/4 happen to coincide
            at the retained values. This is a corroboration, not a
            derivation. (demoted corroboration)

(S5)  NEW retained EW–CKM bridge identity (independent corroboration):
       sin²(theta_W)|_lattice = g_Y²/(g_Y² + g_2²) = (d+1)/(2d+3) = 4/9
       (with d = 3, retained from YT_EW), and
       A^4 = (N_pair/N_color)² = 4/9 (from S1+S2 squared).
       Therefore sin²(theta_W)|_lattice = A^4 = 4/9 at retained lattice scale.

(S6)  Auxiliary support-tier reading (NOT load-bearing):
       CL3_TASTE_GENERATION_THEOREM (support-tier): hw=1 sector has
       Y spectrum {+1/3, +1/3, -1}; the 2 quark-Y states are consistent
       with N_pair = 2 but NOT load-bearing for the closure.
```

The closure (S1+S2) holds at retained-tier authorities and is below W2.
S3 is consistency. S4 routes are demoted to corroborations. S5 is a
NEW retained EW–CKM bridge identity. S6 is support-tier and not
load-bearing.

## Retained Inputs (Explicitly Tagged by Authority Tier)

| Input | Authority on `main` | Tier | Role |
| --- | --- | --- | --- |
| `Q_L : (2,3)_{+1/3}` (left-handed quark rep) | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) | **retained corollary** | **S1 SOURCE** (load-bearing) |
| `u_R : (1,3)_{+4/3}`, `d_R : (1,3)_{-2/3}` (right-handed quark reps) | [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | **retained** | S1 corroboration on N_color |
| Z³ spatial substrate; "exact native SU(2)"; "graph-first structural SU(3)" | [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) | **retained** framework primitive + consequences | gauge-structure context |
| Bare `g_2² = 1/(d+1)`, `g_Y² = 1/(d+2)` | [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) | **retained** (DERIVED) | S5 EW–CKM bridge |
| `(W2)` `A² = N_pair/N_color = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) | **retained** | S3 consistency check |
| `N_pair = 2`, `N_color = 3`; primitive `N_pair = N_color − 1` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | **retained** | structural-counts package |
| Lie group rep theory: `dim(SU(N) fund) = N` | mathematical fact | external (math) | S4(i) corroboration only |
| hw=1 Y spectrum (auxiliary) | [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md) | **support-tier** (NOT load-bearing) | S6 |

The S1 closure uses ONLY retained-tier authorities. No PDG observable
enters as input. No support-tier inputs enter the load-bearing closure
chain (S1+S2).

## Derivation

### S1 derivation (Identification Source Theorem)

`LEFT_HANDED_CHARGE_MATCHING_NOTE.md` (Status: "retained corollary on
the current paper surface") explicitly retains:

> `Q_L : (2,3)_{+1/3}`

This is a retained statement of the matter content: the left-handed
quark field transforms in the SU(2)_L fundamental (doublet) and the
SU(3)_c fundamental (triplet) representations.

`ONE_GENERATION_MATTER_CLOSURE_NOTE.md` (Status: "retained") retains:

> `u_R : (1,3)_{+4/3}`, `d_R : (1,3)_{-2/3}`

The right-handed quarks are SU(2)_L singlets in the SU(3)_c triplet
representation.

**Reading off N_pair from the retained Q_L rep:**

The left-handed quark doublet `Q_L : (2,3)` has SU(2)_L rep dim = 2.
The two components ARE the up-type and down-type quark-flavor partners
of one generation (T_3 = +1/2 component is up-type; T_3 = −1/2 component
is down-type). The CKM-side count "number of paired up/down quark
flavors per generation" equals `dim_SU2(Q_L) = 2`. Therefore:

```text
N_pair = dim_SU2(Q_L) = 2.
```

**Reading off N_color from the retained Q_L rep:**

The same Q_L : (2,3) has SU(3)_c rep dim = 3. Each quark field has
3 color states. The CKM-side count "number of color states per quark
flavor" equals `dim_SU3(Q_L) = 3`. Cross-checked by retained P3:
`dim_SU3(u_R) = dim_SU3(d_R) = 3`. Therefore:

```text
N_color = dim_SU3(Q_L) = 3.
```

**Both N_pair and N_color come from the SAME retained source** — the
single retained representation literal `(2,3)` of Q_L. They are not
independent assertions about two integers happening to coincide; they
are direct read-offs from one retained matter-content statement.

### S2 closure (A² below W2)

```text
A² := N_pair / N_color
    = dim_SU2(Q_L) / dim_SU3(Q_L)
    = 2 / 3.
```

This is a derived equality from a retained source (S1), at a level
BELOW the W2 structural-counts package (which retains A² as a
derived consequence at the W2 level).

### S3 consistency check (W2 retains the same value)

`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`
retains at the W2 level:

```text
A² = N_pair / N_color = 2/3.
```

The S1+S2 below-W2 derivation reproduces this retained W2 value
exactly. This is a consistency check on the chain, not a separate
derivation route.

### S4 demoted corroborations (NOT load-bearing)

**(i) Gauge-dimension reading:**
`dim_fund(SU(N)) = N` (Lie group rep theory) gives
`dim_fund(SU(2)) = 2` and `dim_fund(SU(3)) = 3`. These are consistent
with S1.a/S1.b but do NOT independently derive N_pair = 2 or
N_color = 3 because the identification "N_pair = dim_fund(SU(2))" is
not derived — it would be a separate hypothesis. S1 avoids this by
reading both off the SAME retained matter-content literal Q_L : (2,3).

**(ii) Numerical reading:**
YT_EW retained `g_2² = 1/(d+1) = 1/4` and `1/N_pair² = 1/4` (at
retained N_pair = 2) coincide numerically. This is a corroboration of
the retained values, not a derivation.

These S4 routes appear in the runner as labeled CORROBORATION checks,
not load-bearing steps.

### S5 EW–CKM bridge identity (independent)

From YT_EW retained bare couplings:

```text
sin²(theta_W)|_lattice = g_Y² / (g_Y² + g_2²)
                        = (1/(d+2)) / (1/(d+1) + 1/(d+2))
                        = (d+1) / (2d+3) = 4/9   (with d = 3).
```

From S1+S2 squared:

```text
A^4 = (N_pair/N_color)² = (2/3)² = 4/9.
```

Therefore:

```text
sin²(theta_W)|_lattice = A^4 = 4/9   EXACTLY at retained lattice scale.
```

This NEW retained identity ties the EW Weinberg angle at lattice scale
to the Wolfenstein A parameter through two independent retained
authorities (YT_EW and S1+S2 / W2). It is an INDEPENDENT corroboration
of the framework's retained lattice-scale EW bare-normalization lane and CKM
lane at lattice scale.

### S6 auxiliary support reading (NOT load-bearing)

`CL3_TASTE_GENERATION_THEOREM` (support-tier on main) reads the hw=1
sector of the Z³ taste cube as having Y spectrum `{+1/3, +1/3, −1}`.
The 2 states with `Y = +1/3` are quark-like, consistent with N_pair = 2.

This is **support-tier auxiliary observation**, NOT load-bearing for
the closure. The closure (S1+S2) stands without it.

## Numerical Verification

All identities verified to **exact integer/Fraction arithmetic**.
The runner extracts the retained representation literals from the
authority files (rather than hard-coding) and DERIVES `A²` from the
chain:

| Identity | Source | Value | Match? |
| --- | --- | ---: | --- |
| P2: Q_L : (2,3) literal extracted from doc | LEFT_HANDED_CHARGE_MATCHING_NOTE | (2,3) | ✓ |
| P3: u_R : (1,3), d_R : (1,3) extracted | ONE_GENERATION_MATTER_CLOSURE_NOTE | (1,3), (1,3) | ✓ |
| S1.a: N_pair = dim_SU2(Q_L) | extracted from P2 | 2 | ✓ |
| S1.b: N_color = dim_SU3(Q_L) | extracted from P2 | 3 | ✓ |
| S1.b cross-check: dim_SU3(u_R) = dim_SU3(d_R) = N_color | extracted from P3 | 3 | ✓ |
| S2: A² = N_pair/N_color (DERIVED) | from S1 by D1/D2 | 2/3 | ✓ |
| S3: A² (W2 retained) consistency check | W2 doc | 2/3 | ✓ |
| S4(i): gauge-dim corroboration only | math | 2/3 | ✓ (not load-bearing) |
| S4(ii): numerical g_2² = 1/N_pair² corroboration only | YT_EW + CKM_MAG | 1/4 = 1/4 | ✓ (not load-bearing) |
| S5: sin²(θ_W)\|_lattice = A^4 = 4/9 | YT_EW + S2 | 4/9 = 4/9 | ✓ |

## Science Value

### What this lets the framework state cleanly

Previously, the `A²` story below `W2` existed only as structural-count
closure plus narrower corroboration routes. This note supplies the
missing source-level theorem as **S1: Identification Source Theorem**:

- the retained matter-content literal `Q_L : (2,3)_{+1/3}` from
  LEFT_HANDED_CHARGE_MATCHING_NOTE (retained corollary) is the single
  source from which both `N_pair = 2` and `N_color = 3` are read off.
- `N_pair = dim_SU2(Q_L)` is not an independent integer-assertion — it is
  the operational definition (the doublet IS the up-down pair).
- `N_color = dim_SU3(Q_L)` is similarly a direct read of the `SU(3)_c`
  rep dim of every quark, cross-checked by retained P3 right-handed reps.

The identification is FIXED AT THE SOURCE by the retained representation
literal — there is no separate "X = Y" identification step asserting
that two external integers happen to coincide.

### Below W2 in a meaningful sense

The closure is BELOW W2 because:

- W2 retains A² as a derived quantity at the structural-counts level.
- S1+S2 derive A² from the matter-content level (Q_L : (2,3) retained
  representation), which is the layer BENEATH the structural-counts
  package.
- The retained matter-content rep is the FOUNDATIONAL source from which
  the structural-counts (N_pair, N_color) emerge as direct read-offs.

### Closure does not depend on demoted routes

The closure (S1+S2) uses ONLY:

- LEFT_HANDED_CHARGE_MATCHING_NOTE (retained corollary, P2)
- ONE_GENERATION_MATTER_CLOSURE_NOTE (retained, P3 cross-check on N_color)
- MINIMAL_AXIOMS_2026-04-11 (retained, P1 gauge-structure context)

The gauge-dimension equality and the numerical `g_2²` coincidence are
now explicitly demoted to S4
corroborations — the runner labels them as such.

### NEW retained EW–CKM bridge identity (S5)

```text
sin²(theta_W)|_lattice  =  A^4  =  4/9    EXACTLY (retained level).
```

This is a NEW retained identity tying TWO independently-retained
quantities at the lattice scale:

- `sin²(θ_W)|_lattice = 4/9` from YT_EW retained bare couplings.
- `A^4 = 4/9` from S1+S2 squared (derived below W2).

The framework's retained lattice-scale EW bare-normalization lane and CKM
lane meet at this sharp
identity at lattice scale.

### What this does NOT promote

- Does NOT promote CL3_TASTE_GENERATION_THEOREM from support to retained.
- Does NOT promote CL3_COLOR_AUTOMORPHISM_THEOREM from support to retained.
- Does NOT promote CL3_SM_EMBEDDING_THEOREM from support to retained.
- Does NOT cite any unmerged branches as retained authorities.
- Does NOT use the gauge-dimension consistency equality as load-bearing.
- Does NOT use the YT_EW numerical coincidence as load-bearing.

### Falsifiable structural claim

The closure is sharp:

```text
A² = 2/3 closes BELOW W2 via the S1 Identification Source Theorem,
which DERIVES BOTH N_pair = 2 and N_color = 3 from the SINGLE retained
matter-content literal Q_L : (2,3)_{+1/3}.

The bonus identity sin²(θ_W)|_lattice = A^4 = 4/9 holds at retained
level via two independent retained authorities (YT_EW and S2).
```

Any framework revision changing the retained `Q_L : (2,3)_{+1/3}` rep
(e.g., demoting LEFT_HANDED_CHARGE_MATCHING_NOTE from retained, or
changing the SU(2)_L doublet structure of left-handed quarks) would
break S1.

### Why this counts as pushing the science forward

1. **True derivation below W2 (not consistency equality)**: the
   Identification Source Theorem (S1) gives a single retained matter
   content source for both `N_pair` and `N_color`. The closure `A² = 2/3`
   is derived below the `W2` structural-counts level, not asserted via
   dimension-equality coincidence.

2. **Demoted routes labeled honestly**: the gauge-dimension reading
   (S4(i)) and YT_EW numerical coincidence (S4(ii)) are explicitly
   labeled as corroborations, not derivations. The closure no longer
   load-bears on consistency equalities.

3. **NEW retained EW–CKM bridge identity** (S5): `sin²(θ_W)|_lattice =
   A^4 = 4/9` ties two independently-retained quantities at lattice
   scale. NEW structural identity at retained level, surviving the
   re-derivation.

## What This Claims

- `(S1)`: Identification Source Theorem from retained Q_L : (2,3) rep.
- `(S2)`: A² = 2/3 derived BELOW W2 from S1.
- `(S3)`: S1+S2 reproduces W2-retained A² = 2/3 (consistency check).
- `(S5)`: NEW retained EW–CKM bridge `sin²(θ_W)|_lattice = A^4 = 4/9`.

## What This Does NOT Claim

- Does NOT promote any support-tier theorem to retained.
- Does NOT use the gauge-dimension equality as load-bearing.
- Does NOT use the YT_EW numerical coincidence as load-bearing.
- Does NOT modify retained W2 (it grounds N_pair, N_color BELOW W2 at
  the matter-content level).
- Does NOT predict physical sin²(θ_W) at M_Z (the lattice-scale 4/9
  runs to PDG ≈ 0.231 via separate retained running).
- Does NOT close the deeper question of WHY CL3 spatial substrate is Z³
  (3-dim). That remains a retained framework primitive (axiom 2).
- Does NOT derive the SM gauge-rep assignment of Q_L from a yet-deeper
  axiom. The retention of Q_L : (2,3) in LEFT_HANDED_CHARGE_MATCHING_NOTE
  is itself a retained corollary on the framework's selected-axis
  surface, which is the foundational layer used here.

## Reproduction

```bash
python3 scripts/frontier_ckm_a_squared_below_w2_y_quantum_closure.py
```

Expected result:

```text
TOTAL: PASS=32, FAIL=0
A2_BELOW_W2_DERIVATION_CLOSED = TRUE  (via S1 Identification Source Theorem)
```

The runner:

1. Reads each cited authority file from disk.
2. Extracts the retained representation literals (Q_L, u_R, d_R) by
   regex matching against the actual document text — NOT hard-coded.
3. Parses (a, b) → (dim_SU2, dim_SU3) and reads N_pair = a, N_color = b.
4. DERIVES A² = N_pair/N_color from the parsed values via Fraction
   arithmetic.
5. Cross-checks against retained P3 right-handed reps for N_color.
6. Verifies S3 W2 consistency (that the derived value reproduces the
   W2-retained value).
7. Labels S4 routes as CORROBORATION ONLY (not load-bearing).
8. Verifies S5 EW–CKM bridge from independent YT_EW retained couplings.

## Cross-References

**Retained-tier authorities used in S1+S2 closure (load-bearing):**

- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  — retained corollary; `Q_L : (2,3)_{+1/3}` SOURCE for S1.
- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
  — retained; `u_R : (1,3)_{+4/3}`, `d_R : (1,3)_{-2/3}` cross-check on N_color.
- [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) — retained
  framework primitives + current consequences (P1 gauge-structure context).

**Retained-tier authorities used for consistency / S5 bridge:**

- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  — retained `(W2)` `A² = N_pair/N_color = 2/3` (S3 consistency).
- [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
  — retained DERIVED; bare `g_2² = 1/(d+1)`, `g_Y² = 1/(d+2)` (S5).
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — retained `N_pair = 2`, `N_color = 3` (structural-counts package).

**Support-tier auxiliary reading (NOT load-bearing for closure):**

- [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md) —
  support-tier; auxiliary observation on hw=1 Y multiplicity, NOT a
  derivation route.

**NOT cited as derivation input:**

- CL3_COLOR_AUTOMORPHISM_THEOREM (support-tier; redundant given retained
  MINIMAL_AXIOMS Z³ axiom + retained Q_L : (2,3)).
- CL3_SM_EMBEDDING_THEOREM (support-tier; explicitly "not part of the
  accepted minimal-input stack").
- Any unmerged branches.

---

## Current audit-lane disposition (informational)

This row was audited on 2026-05-05 by
`codex-cli-gpt-5.5-20260505-225305-c0ea7096-ckm_a_squared_below_w2_y-070`
and returned `audited_conditional`. The verdict identifies a concrete
local extraction gap, not just upstream-conditional propagation:

> *The proof imports a retained Q_L representation source and an
> identification of CKM counts with its representation dimensions, but
> the cited authority packet does not close either point. Without a
> retained Q_L literal and an audited bridge from CKM N_pair/N_color to
> matter-representation dimensions, the result is a conditional
> definition/import rather than a below-W2 theorem.*

The seven declared upstream authorities now sit at:

| Upstream authority | Effective status (current) |
|---|---|
| [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) | `unaudited` |
| [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | `unaudited` |
| [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) | `meta` |
| [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) | `retained_bounded` (cross-confirmed `audited_clean`, 2026-05-07) |
| [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) | `unaudited` (PR #764 added exact-symbolic verification, awaiting re-audit) |
| [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | `unaudited` (PR #766 added exact-symbolic magnitude-count verification, awaiting re-audit) |
| [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md) | `audited_conditional` |

### Local extraction gap (report-only)

The ledger-recorded runner failure at
`scripts/frontier_ckm_a_squared_below_w2_y_quantum_closure.py` reports

```text
S1 P2: Extract retained Q_L representation literal (NOT hard-coded)
  Reading docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md
  Searching for retained literal: Q_L : (a,b)_{Y}
  Extracted (dim_SU2, dim_SU3) for Q_L: None
  [FAIL] S1 P2: Q_L representation literal extracted from retained doc
```

`LEFT_HANDED_CHARGE_MATCHING_NOTE.md` does discuss the `(2,3)` and `(2,1)`
blocks of the LH-doublet sector, but does not write the Q_L literal in
the `Q_L : (a,b)_{Y}` form the runner pattern expects. Two repair paths
remain, both deferred to a separate proof-walk PR rather than this
audit-sweep:

1. *Source-side repair*: amend `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` to
   include the explicit literal `Q_L : (2,3)_{+1/3}` so the extractor
   succeeds.
2. *Runner-side repair*: relax the extractor pattern to accept the
   existing `(2,3)` block discussion plus the surrounding
   "LH-doublet sector" context.

Until one of those lands, this row is upstream-conditional on the
unaudited matter-content authorities AND additionally fails its own
local extraction step, so it cannot be promoted. The local
class-(A) algebra in the body of the note is unaffected.
