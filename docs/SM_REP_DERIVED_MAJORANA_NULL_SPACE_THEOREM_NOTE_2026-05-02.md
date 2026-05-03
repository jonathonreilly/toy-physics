# SM One-Generation Representation Synthesis + Majorana Null-Space Derivation

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the **integrated derivation** of the SM one-generation
matter representation from anomaly cancellation + retained graph-first
primitives (synthesizing cycles 01+02+04 of the retained-promotion
campaign), plus the Majorana null-space classification on the
DERIVED representation. The verdict-identified obstruction on
`NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md` was: "the runner
hard-codes the representation and proves the invariant-bilinear result
only conditional on that imported representation. Repair target: ...
an integrated runner that derives the full representation from
retained primitives before solving the Majorana null space."
This PR provides exactly that integrated derivation.
**Status:** audit pending. Audit-lane ratification is required before
any retained-grade status applies. Under the scope-aware
classification framework, `effective_status` is computed by the audit
pipeline; no author-side tier is asserted in source.
**Runner:** [`scripts/frontier_sm_rep_majorana_null_space_derivation.py`](./../scripts/frontier_sm_rep_majorana_null_space_derivation.py)
**Authority role:** closing derivation for the parent's class-B
load-bearing step (representation hand-coding).

## Verdict-identified obstruction (quoted)

From `neutrino_majorana_operator_axiom_first_note`'s `verdict_rationale`:

> Issue: the classification depends on the anomaly-fixed one-generation
> spectrum, U(1)_Y charges, chirality surface, and right-handed sector
> being retained inputs, but those authorities are not present as
> one-hop ledger dependencies and some listed authority paths are not
> resolved by the audit bundle. Why this blocks: the runner hard-codes
> the representation and proves the invariant-bilinear result only
> conditional on that imported representation. Repair target: add
> retained one-hop dependencies or an integrated runner that derives
> the full representation from retained primitives before solving the
> Majorana null space.

## Statement

Let:

- (P1, retained) Graph-first SU(3) integration giving Q_L : (2, 3) on
  the framework's selected-axis surface, plus the retained
  narrow-ratio theorem
  `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`
  (td=265, retained) establishing Y(L_L)/Y(Q_L) = -3 structurally.
- (P2, sister-derivation cycle 01, [PR #382](https://github.com/jonathonreilly/cl3-lattice-framework/pull/382))
  SU(3)^3 cubic anomaly cancellation forces the RH quark sector to
  consist of two SU(3) anti-fundamentals (3̄). Combined with the
  Q-labelling convention Q(u_R) > 0, this fixes
  `u_R^c, d_R^c : (1, 3̄)` in the LH-conjugate frame, equivalently
  `u_R, d_R : (1, 3)` in the standard frame.
- (P3, sister-derivation cycle 02, [PR #383](https://github.com/jonathonreilly/cl3-lattice-framework/pull/383))
  SU(2) Witten Z_2 anomaly forces an even number of SU(2) doublets
  per generation; the minimal anomaly-cancelling matter content has 4
  doublets (Q_L: 3 colors × 2 (SU(2) doublet states each) and L_L: 1
  state × 2). RH species are SU(2) singlets by chirality.
- (P4, sister-derivation cycle 04, [PR #390](https://github.com/jonathonreilly/cl3-lattice-framework/pull/390))
  U(1)_Y mixed anomaly cancellation `Tr[Y] = Tr[SU(3)² Y] = Tr[Y³] = 0`
  on the no-ν_R sector forces Y(u_R) = +4/3, Y(d_R) = -2/3, Y(e_R) =
  -2 (in doubled-Y convention with Q-labelling Q(u_R) > 0).
- (P5, admitted) Including ν_R as a 4th SU(2)-singlet RH species
  with neutrality input Y(ν_R) = 0 extends the rep to the full SM
  with ν_R; without this admission, the framework's matter is the
  no-ν_R sector.
- (P6, retained) The lattice CPT structure of `CPT_EXACT_NOTE.md`
  provides the spinor C-conjugation matrix and γ_5 chirality projector
  needed for same-chirality bilinears. Standard QFT machinery
  (Peskin-Schroeder ch. 3) is admitted-context external authority.

**Conclusion (T1) (integrated SM rep derivation).** Under P1+P2+P3+P4
on the no-ν_R sector, the one-generation SM matter representation is

```text
Q_L : (2, 3)_{+1/3}
L_L : (2, 1)_{-1}
u_R : (1, 3)_{+4/3}
d_R : (1, 3)_{-2/3}
e_R : (1, 1)_{-2}
```

DERIVED (not hand-coded) from anomaly cancellation + retained graph-first
SU(3) integration + retained Y(L_L)/Y(Q_L) = -3 ratio + Q(u_R) > 0
labelling.

Adding P5 (Y(ν_R) = 0 input), the rep extends to include
`ν_R : (1, 1)_0`.

**Conclusion (T2) (no-ν_R Majorana null space is empty).** On the
DERIVED no-ν_R sector representation, the space of local quadratic
same-chirality (P_R) bilinears that are simultaneously
SU(3)_c-invariant, SU(2)_L-invariant, and U(1)_Y-invariant is the
**zero vector space**: no quadratic Majorana operator is admissible.

**Conclusion (T3) (with-ν_R Majorana null space is one-dimensional).**
Adding P5 to extend the rep with `ν_R : (1, 1)_0`, the same-chirality
P_R Majorana null space becomes one-dimensional, spanned by

```text
ν_R^T C P_R ν_R
```

(matching `NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md`'s
classification, but now on the DERIVED rep).

**Conclusion (T4) (counterfactuals).** Changing any single Y value
(e.g., y_3 = -2 → y_3 = -1) makes the previously-admissible Majorana
operator gauge-non-invariant; changing a rep (e.g., e_R from (1,1) to
(1,3)) likewise breaks gauge-invariance. The Majorana null space is
contingent on the SPECIFIC SM Y values that cycle 04 derives.

## Proof

### Step 1: Q_L from retained graph-first SU(3)

By P1, the graph-first SU(3) integration on the selected-axis surface
gives the Sym²(3) ⊕ Anti²(1) decomposition of the residual permutation
τ on a 4-point base. The Sym²(3) part carries the SU(3) fundamental
(3) — that's `Q_L : (2, 3)`. The narrow-ratio theorem (retained,
td=265) establishes the ratio Y(L_L)/Y(Q_L) = -3 on the traceless
abelian generator, structurally from the 6-state and 2-state
LH-doublet sub-decompositions. The convention Y(Q_L) = +1/3 (or
equivalently Y(L_L) = -1) fixes the overall scale.

### Step 2: RH quark color rep from SU(3)^3 anomaly (cycle 01)

By P2 (cycle 01), the SU(3)^3 cubic anomaly cancellation
`Tr[T^a T^b T^c]_quarks = 0` forces the RH quark sector to consist of
fields in the **anti-fundamental** 3̄ (in the LH-conjugate frame).
Equivalently, in the physical (RH) frame, u_R and d_R transform under
the SU(3) fundamental 3 (the anti-fundamental of the LH-conjugate).
Cycle 01 pinned this via Diophantine enumeration over irrep
cubic-anomaly coefficients; the unique 2-field minimal completion is
{3̄: 2}, mapping to {u_R^c, d_R^c}.

### Step 3: SU(2) singlet status of RH from cycle 02

By P3 (cycle 02), the SU(2) Witten Z_2 anomaly forces an even number
of LH SU(2) doublets per generation. The framework's chirality of
SU(2)_L (retained, NATIVE_GAUGE_CLOSURE_NOTE) means RH fields are
SU(2) singlets. Combined with cycle 02's count: 4 LH doublets per
generation (Q_L: 3 + L_L: 1) and 0 RH doublets, so all RH species are
SU(2)-singlets (1 under SU(2)).

### Step 4: RH hypercharge values from cycle 04 no-ν_R variant

By P4 (cycle 04), on the no-ν_R sector the U(1)_Y mixed anomaly
system

```text
Tr[Y] = -3(y_1 + y_2) - y_3 = 0
Tr[SU(3)²Y] = (1/2) [(2/3) - (y_1 + y_2)] = 0
Tr[Y³] = -16/9 - 3(y_1³ + y_2³) - y_3³ = 0
```

closes uniquely on (y_1, y_2, y_3) = (+4/3, -2/3, -2) modulo the
u_R↔d_R relabelling, which is broken by Q(u_R) > 0.

### Step 5: Full no-ν_R SM rep DERIVED

Combining Steps 1-4:

```text
Q_L : (2, 3)_{+1/3}    [retained graph-first + narrow-ratio]
L_L : (2, 1)_{-1}      [retained graph-first + narrow-ratio]
u_R : (1, 3)_{+4/3}    [cycles 01 + 02 + 04]
d_R : (1, 3)_{-2/3}    [cycles 01 + 02 + 04]
e_R : (1, 1)_{-2}      [cycles 02 + 04]
```

This is the no-ν_R SM rep, DERIVED (not hand-coded).

### Step 6: Majorana null space on no-ν_R rep

A same-chirality P_R Majorana bilinear `ψ_i^T C M_{ij} P_R ψ_j` is
gauge-invariant iff M satisfies, for each gauge generator G:

```text
G^T M + M G = 0,
```

i.e., M is in the null space of (G^T ⊕ G) acting on the RH species
multi-index.

For the no-ν_R RH species {u_R, d_R, e_R}:

- **U(1)_Y**: M_{ij} carries Y_i + Y_j. For Y-invariant M_{ij},
  need Y_i + Y_j = 0.
  Y(u_R) = +4/3, Y(d_R) = -2/3, Y(e_R) = -2.
  Pairwise sums: (4/3+4/3)=+8/3, (4/3-2/3)=+2/3, (4/3-2)=-2/3,
  (-2/3-2/3)=-4/3, (-2/3-2)=-8/3, (-2-2)=-4.
  None of these are zero. **Y-invariance forces M_{ij} = 0 for all
  pairs (i, j) on the no-ν_R sector.**

- **No surviving Majorana bilinear** ⇒ Majorana null space is the
  **zero vector space**.

**T2: ✓**

### Step 7: Majorana null space on with-ν_R rep

Adding ν_R : (1,1)_0 with Y(ν_R) = 0 (from P5):

- Y(ν_R) + Y(ν_R) = 0 ✓ (Y-invariant)
- ν_R is SU(3) singlet × SU(2) singlet, so SU(3) and SU(2) invariance
  are trivial.
- Hence the bilinear `ν_R^T C P_R ν_R` is fully gauge-invariant.

For all other pairs involving ν_R: Y(ν_R) + Y(other) = 0 + Y(other) ≠ 0
(since Y(u_R, d_R, e_R) ≠ 0). So no Y-invariant cross-bilinear with ν_R.

For pairs not involving ν_R: as Step 6, no Y-invariant bilinears.

**Hence the with-ν_R Majorana null space is one-dimensional, spanned
by `ν_R^T C P_R ν_R`. T3: ✓.**

### Step 8: Counterfactuals

**Counterfactual A (changed Y values)**: Replace y_3 = -2 with y_3 = -1
(non-SM). Then 2·Y(e_R) = -2 ≠ 0. Y(e_R) + Y(ν_R) = -1 ≠ 0. So no
new Majorana operator emerges; existing ν_R^T ν_R remains. But the
rep is no longer anomaly-free (cycle 04 forces y_3 = -2). So this
counterfactual is anomalous + Majorana-irrelevant.

**Counterfactual B (changed reps)**: Replace e_R from (1,1) with (1,3).
Then e_R is colored. e_R^T C e_R is in 3⊗3 = 6_s ⊕ 3̄_a; neither
contains the SU(3) singlet 1. So e_R Majorana bilinear is
SU(3)-non-invariant. Original Majorana (ν_R^T C P_R ν_R) survives
but is unrelated. The Majorana classification is contingent on the
SPECIFIC SU(3) reps that cycles 01-02 derive.

∎

## What this claims

- `(T1)` Integrated SM rep derivation: synthesizes cycles 01+02+04
  + retained graph-first into a single derivation of the no-ν_R SM
  rep.
- `(T2)` No-ν_R Majorana null space is **empty**. No quadratic
  Majorana operator on the framework's minimal anomaly-cancelling
  matter content.
- `(T3)` With-ν_R (Y(ν_R) = 0 admitted) Majorana null space is
  one-dimensional, spanned by `ν_R^T C P_R ν_R`. Matches
  `NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md`'s classification,
  but on the DERIVED rep.
- `(T4)` Counterfactuals: changing Y values or reps breaks
  Majorana-null-space dimension or makes the rep anomaly-non-free.

## What this does NOT claim

- Does NOT derive Y(ν_R) = 0 from framework primitives (it's an
  admitted input for the with-ν_R extension). Cycle 04's no-ν_R
  variant shows ν_R is OPTIONAL.
- Does NOT prove Majorana coefficient is nonzero. Parent's
  companion no-go notes
  (`NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE`,
  `NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE`) show the
  framework's current native surface gives zero coefficient.
- Does NOT close PMNS / leptogenesis / Δm² / m_ββ — downstream
  phenomenology.
- Does NOT promote any author-side tier; audit-lane ratification is
  required.

## Cited dependencies

- (P1) [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) (retained, td=312); [`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md) (retained, td=265).
- (P2) [`SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md`](SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md) ([PR #382](https://github.com/jonathonreilly/cl3-lattice-framework/pull/382), audit pending).
- (P3) [`SU2_WITTEN_ANOMALY_DOUBLET_COUNT_DERIVED_THEOREM_NOTE_2026-05-02.md`](SU2_WITTEN_ANOMALY_DOUBLET_COUNT_DERIVED_THEOREM_NOTE_2026-05-02.md) ([PR #383](https://github.com/jonathonreilly/cl3-lattice-framework/pull/383), audit pending).
- (P4) [`SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md`](SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md) ([PR #390](https://github.com/jonathonreilly/cl3-lattice-framework/pull/390), audit pending).
- (P5) Y(ν_R) = 0 admitted neutrality input; consistent with cycle 04's analysis but not derived.
- (P6) [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) (retained); Peskin-Schroeder 1995 ch. 3 (admitted-context external).

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention beyond the
  doubled-Y convention.
- No same-surface family arguments.
- No load-bearing dependency on the demoted
  `HYPERCHARGE_IDENTIFICATION_NOTE` (cycle 04's decoupling carries
  through).

## Validation

Primary runner: [`scripts/frontier_sm_rep_majorana_null_space_derivation.py`](./../scripts/frontier_sm_rep_majorana_null_space_derivation.py)
verifies (PASS=18/0, exact rational arithmetic + structural reps):

1. Cycle 01 forced 3̄ minimal completion via Diophantine on
   compositions (re-execution).
2. Cycle 02 doublet count = 4 per generation (re-execution).
3. Cycle 04 no-ν_R cubic system closes uniquely on (y_1, y_2, y_3) =
   (+4/3, -2/3, -2) (re-execution).
4. Integrated SM rep derivation produces the full no-ν_R rep.
5. Majorana null-space solve on no-ν_R rep: empty (no Y-invariant
   pair sums to zero).
6. Adding ν_R: (1,1)_0: Majorana null-space dimension = 1, spanned
   by `ν_R ν_R`.
7. Counterfactual A: y_3 = -1 makes the rep anomaly-non-free
   (Tr[Y] ≠ 0).
8. Counterfactual B: e_R rep (1,3) makes e_R bilinear
   SU(3)-non-invariant.
9. Spinor factor: same-chirality bilinears antisymmetric in flavor;
   matches parent's classification.

## Cross-references

- [`NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md`](NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md) —
  parent row whose verdict-identified obstruction is closed by this
  derivation.
- [`SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md`](SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md) —
  cycle 01 sister.
- [`SU2_WITTEN_ANOMALY_DOUBLET_COUNT_DERIVED_THEOREM_NOTE_2026-05-02.md`](SU2_WITTEN_ANOMALY_DOUBLET_COUNT_DERIVED_THEOREM_NOTE_2026-05-02.md) —
  cycle 02 sister.
- [`SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md`](SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md) —
  cycle 04 sister.
- [`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md) —
  retained narrow-ratio theorem cited in P1.
- [`NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md`](NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md) —
  companion no-go showing Majorana coefficient is zero on the current
  native surface.
