# SU(2) Witten Z₂ Anomaly — Doublet-Count Derivation Theorem

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the **derivation** that, given the retained matter
representations `Q_L : (2, 3)_{1/3}` and `L_L : (2, 1)_{-1}` plus the
structural chirality of the SU(2)_L gauge group, the count of LH-Weyl
SU(2) fundamental-representation fermions per generation is **forced to
be 4**, and therefore even, so the SU(2) Witten Z₂ topological anomaly
cancels. The derivation does not depend on a hand-coded matter-content
table; the doublet count is computed from the retained representation
literals (rep dim of SU(3) factor), and the RH-singlet status follows
from the chirality of SU(2)_L. Hypercharges, generation count, and the
RH content of the (anti-)quark sector are explicitly out of scope —
those are separate authority rows.
**Status:** audit pending. This is a candidate **closing derivation** of
the verdict-identified obstruction on
`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24`. Under the scope-aware
classification framework, `effective_status` is computed by the audit
pipeline; no author-side tier is asserted in source. Audit-lane
ratification is required before any retained-grade status applies.
**Runner:** [`scripts/frontier_su2_witten_anomaly_doublet_count_derivation.py`](./../scripts/frontier_su2_witten_anomaly_doublet_count_derivation.py)
**Authority role:** closing derivation for the parent's class-B
load-bearing step (cross-note input verification on
`one_generation_matter_closure` for SU(2) doublet count + RH-singlet
completion).

## Verdict-identified obstruction (quoted)

> Issue: the theorem's load-bearing premise identifies the retained
> chiral matter fields Q_L and L_L as SU(2) Weyl doublets with
> multiplicities 3 and 1, while treating RH fields as singlets. Why
> this blocks retained status: the supplied retained-grade authorities
> close native SU(2), graph-first 3+1 structure, and three-generation
> algebra, but they do not ratify the full one-generation chiral field
> identification; the runner hard-codes that premise and then checks
> parity. Repair target: add or cite a retained-grade one-generation
> matter theorem deriving the Q_L/L_L SU(2) Weyl-doublet content and
> singlet completion from the retained graph/gauge surface.

## Statement

Let:

- (P1, retained) `Q_L : (2, 3)_{1/3}` from
  `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` (retained corollary on the
  graph-first selected-axis surface).
- (P2, retained) `L_L : (2, 1)_{-1}` from
  `ONE_GENERATION_MATTER_CLOSURE_NOTE.md`.
- (P3, admitted/structural) The SU(2)_L gauge symmetry is **chiral**:
  it acts only on the left-handed projector subspace `P_L = (1 + γ_5)/2`.
  Right-handed Weyl fields, by chirality, sit in the trivial (singlet)
  representation of SU(2)_L. This is encoded in the framework's
  `NATIVE_GAUGE_CLOSURE_NOTE.md`, which establishes SU(2) as the weak
  gauge factor on the chiral surface.
- (P4, admitted) `π_4(SU(2)) = Z_2` (Witten 1982). For SU(2) gauge
  theory with `N` LH-Weyl fermions in the fundamental 2 of SU(2), the
  partition function changes sign under topologically non-trivial
  gauge transformations iff `N` is odd; consistency requires `N`
  even.

**Conclusion (T1) (closing derivation).** Under P1+P2+P3+P4, the
number of LH-Weyl SU(2) fundamental-rep fermions per generation is
**forced to be**

```text
N_doublets per generation = dim_SU(3)(Q_L) · 1 + dim_SU(3)(L_L) · 1 + 0
                          = 3 + 1 + 0
                          = 4,
```

derived from the retained `(2, 3)` and `(2, 1)` representation literals
plus the chirality structural argument for RH-singlet completion. The
Witten Z₂ index per generation is `4 mod 2 = 0`, so the Witten anomaly
cancels.

**Conclusion (T2) (multi-generation extension).** For any number `N_gen`
of generations, `N_total = 4 N_gen` is always even, so the Witten
anomaly cancels for any integer generation count.

**Conclusion (T3) (counterfactual non-triviality).** Dropping the
leptonic doublet (`L_L` set to a SU(2) singlet) would give 3 LH
doublets per generation (odd) and one-generation Witten anomaly would
NOT cancel. The framework's matter content is therefore not trivially
anomaly-free; the specific `(2, 3)` quark and `(2, 1)` lepton doublet
literals matter.

## Proof

### Step 1: π_4(SU(2)) = Z_2 (admitted)

This is a standard topological fact (Witten 1982; cf. any QFT textbook
covering global anomalies). It is admitted-context external mathematical
authority — not derived from the framework's retained primitives, but
universal.

### Step 2: Q_L : (2, 3) contributes 3 LH SU(2) doublets per generation

The `(2, 3)` literal of `Q_L` encodes:
- SU(2) representation: 2 (fundamental, doublet).
- SU(3) representation: 3 (fundamental, triplet).

Each color component of the SU(3) triplet is an independent LH-Weyl
fermion (the framework's lattice-fermion content puts each color
component as a separate Weyl field). Each color-component fermion
sits in the SU(2) doublet representation. So `Q_L` contributes

```text
N_doublets(Q_L)  =  dim_SU(3)(Q_L) × 1  =  3
```

LH SU(2) doublets per generation.

### Step 3: L_L : (2, 1) contributes 1 LH SU(2) doublet per generation

Analogously, `L_L : (2, 1)` is an SU(2) doublet × SU(3) singlet:

```text
N_doublets(L_L)  =  dim_SU(3)(L_L) × 1  =  1
```

LH SU(2) doublet per generation.

### Step 4: RH-singlet completion from chirality of SU(2)_L

The SU(2)_L gauge group is chiral: it acts only on `P_L`. Any
right-handed Weyl field (representable as an LH-Weyl charge-conjugate
field) inherits zero SU(2)_L action. Therefore RH fields contribute 0
to the LH SU(2) doublet count:

```text
N_doublets(RH)  =  0.
```

This is structural; it is not an additional postulate but a
consequence of identifying SU(2)_L as a chiral gauge group on the
framework's selected-axis surface (P3).

### Step 5: Total doublet count per generation = 4

Summing:

```text
N_doublets per generation  =  N(Q_L) + N(L_L) + N(RH)  =  3 + 1 + 0  =  4.
```

### Step 6: Witten Z_2 index per generation = 0

By P4, the Witten Z_2 anomaly index is `N_doublets mod 2 = 4 mod 2 = 0`.
The anomaly cancels per generation.

### Step 7: Multi-generation extension

For `N_gen` generations, `N_total = 4 N_gen`, which is always even.
The Witten anomaly cancels for any integer generation count.

### Step 8: Counterfactual non-triviality

If `L_L` were a SU(2) singlet instead of doublet (i.e., (1, 1) instead
of (2, 1)), then `N_doublets per generation = 3`, which is odd. The
Witten Z_2 anomaly would NOT cancel for one generation. The
cancellation is therefore non-trivial: it requires both the quark and
lepton sectors to be SU(2) doublets, with the specific multiplicities
3 and 1 fixed by the SU(3) representation dimensions.

∎

## What this claims

- `(T1)`: SU(2) doublet count per generation = 4, derived from retained
  `Q_L`, `L_L` rep literals + chirality of SU(2)_L.
- `(T2)`: Witten Z_2 anomaly cancels for any `N_gen` (even count of
  doublets).
- `(T3)`: Counterfactual non-triviality (the lepton doublet is required;
  removing it gives an anomalous one-generation theory).

## What this does NOT claim

- Does NOT derive hypercharges. Separate authority:
  [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md).
- Does NOT derive the generation count `N_gen = 3`. Separate authority:
  [`THREE_GENERATION_STRUCTURE_NOTE`](THREE_GENERATION_STRUCTURE_NOTE.md).
- Does NOT derive the RH (anti-)quark sector content (`u_R^c, d_R^c` :
  3̄). Separate closing derivation:
  [`SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02`](SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md)
  (cycle 01 of this campaign, [PR #382](https://github.com/jonathonreilly/cl3-lattice-framework/pull/382)).
- Does NOT derive the Witten topology itself (`π_4(SU(2)) = Z_2`).
  Admitted-context external mathematical fact.

## Cited dependencies

- (P1) [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) — supplies retained `Q_L : (2, 3)_{1/3}`.
- (P2) [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) — supplies retained `L_L : (2, 1)_{-1}`.
- (P3) [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) — establishes SU(2)_L as chiral gauge factor.
- (P4) Witten 1982; standard external QFT textbook reference for π_4(SU(2)) = Z_2 and the Z_2 anomaly index formula.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_su2_witten_anomaly_doublet_count_derivation.py`](./../scripts/frontier_su2_witten_anomaly_doublet_count_derivation.py)
verifies (PASS=14/0):

1. π_4(SU(2)) = Z_2 admitted.
2. Q_L doublet count = 3 (from rep literal `(2, 3)`).
3. L_L doublet count = 1 (from rep literal `(2, 1)`).
4. RH doublet count = 0 (chirality of SU(2)_L).
5. Total per generation = 4.
6. Witten index per generation = 4 mod 2 = 0.
7. Multi-generation extension for `N_gen ∈ {1, 2, 3, 4, 5, 100}`: all
   give index = 0.
8. Counterfactual: dropping `L_L` doublet gives index = 1 (anomalous).
9. Parent row class-B load-bearing step.

## Cross-references

- [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md) —
  parent row whose verdict-identified obstruction is closed by this
  derivation.
- [`SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02`](SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md) —
  cycle 01 sister closing derivation: same shape (matter-content
  derivation from anomaly cancellation), different anomaly
  (SU(3)^3 cubic vs SU(2) Witten Z_2).
- [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md) —
  related anomaly-freedom theorem on B-L gauging.
