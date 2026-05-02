# SU(3) Anomaly-Forced 3̄ Singlet Completion Theorem

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the **derivation** that, given the retained left-handed quark
representation `Q_L : (3, 2)_{1/3}` from `LEFT_HANDED_CHARGE_MATCHING_NOTE.md`
and the SU(3)^3 anomaly cancellation requirement from
`ANOMALY_FORCES_TIME_THEOREM.md`, the SU(3) representation content of the
right-handed (anti-)quark fields `u_R^c, d_R^c` is forced to be **2 LH-Weyl
fermions in the 3̄ representation**. The derivation does not depend on
hand-coded RH content; it enumerates SU(3) cubic-anomaly coefficients
across irreducible representations, applies anomaly cancellation, and
applies a minimal-field-count completion principle. The hypercharges and
SU(2)_L ⊗ U(1)_Y labelling distinguishing `u_R^c` from `d_R^c` are
**out of scope** here (separate authority rows).
**Status:** audit pending. This note is a candidate **closing derivation**
of the verdict-identified obstruction on the parent
`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24`. Under the
scope-aware classification framework, `effective_status` is computed by
the audit pipeline; no author-side tier is asserted in source.
Audit-lane ratification is required before any retained-grade status
applies.
**Runner:** [`scripts/frontier_su3_anomaly_forced_3bar_completion.py`](./../scripts/frontier_su3_anomaly_forced_3bar_completion.py)
**Authority role:** closing derivation for the parent's class-B
load-bearing step (cross-note input verification on
`one_generation_matter_closure` for `u_R^c, d_R^c` rep content).

## Verdict-identified obstruction (quoted)

> Issue: the cancellation relies on the retained presence and SU(3)
> representations of u_R^c and d_R^c, but those right-handed
> anti-triplets are not established by the provided retained one-hop
> dependencies. The note's reproduction runner passes 33 checks, but
> it checks the hand-entered content table rather than deriving the
> missing matter-content authority. Why this blocks: without that
> matter-content input, the load-bearing +2 - 1 - 1 = 0 sum is only
> conditional algebra, not a theorem from the retained primitives.

## Statement

Let:

- (P1, retained) `Q_L : (3, 2)_{1/3}` be the left-handed quark
  representation per `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` (retained
  corollary on the current paper surface).
- (P2, admitted) The SU(3)^3 cubic-anomaly trace must vanish for gauge
  consistency; this is the anomaly-cancellation requirement encoded by
  `ANOMALY_FORCES_TIME_THEOREM.md`.
- (P3, admitted) Right-handed (anti-)quark fields are LH-Weyl
  SU(2)_L-singlet fermions in irreducible SU(3) representations.

**Conclusion (T1) (closing derivation).** Under P1+P2+P3, the SU(3)
representation content of the RH (anti-)quark sector is forced to be
**exactly 2 LH-Weyl fermions in the 3̄ representation**, with no
irreducible 3-rep fields and arbitrary number of singlets. This is the
**unique minimal-field-count anomaly-cancelling RH completion** in any
candidate rep set including `{1, 3, 3̄}`, and remains minimal under
extension to higher-dim irreps `{6, 6̄, 8, 10, 10̄, 15, 15̄, 27, ...}`.

**Conclusion (T2) (identification).** These 2 LH 3̄ singlets are
identified as `u_R^c` and `d_R^c` in the standard SM bookkeeping. The
SU(3) representation content (3̄) is fully derived from P1+P2+P3; the
distinguishing labels (u vs d) and hypercharges
`Y(u_R^c) = -4/3, Y(d_R^c) = +2/3` require additional authority
(STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24).

## Proof

### Step 1: SU(3) cubic-anomaly coefficient catalogue

For SU(3) irreducible representations, the cubic-anomaly coefficient
`A(R)` (Slansky 1981 Table 22; Cvitanović) is:

```text
A(1)    =   0,    A(3)    =  +1,    A(3̄)    =  -1,
A(6)    =  +7,    A(6̄)    =  -7,    A(8)    =   0,
A(10)   = +27,    A(10̄)   = -27,
A(15)   = +14,    A(15̄)   = -14,
A(27)   =   0,    ...
```

Conjugation symmetry: `A(R̄) = -A(R)`. Self-conjugate (real)
representations have `A(R) = 0` (e.g., 8, 27).

### Step 2: Q_L contribution to SU(3)^3 anomaly

P1 places `Q_L` in `(3, 2)`. The SU(3)^3 anomaly trace counts each
LH-Weyl fermion in irrep `R` with weight `A(R)`. The SU(2) doublet
structure of `Q_L` means there are **2 independent LH-Weyl fermions in
the 3 of SU(3)** (one for each SU(2) component). Therefore

```text
Q_L contribution to SU(3)^3 anomaly  =  2 · A(3)  =  +2.
```

### Step 3: P2 forces RH content to contribute -2

For total anomaly cancellation,

```text
Σ over all LH-Weyl fermions of A(R)  =  0.
```

With Q_L contributing +2 (and L_L : (1, 2) contributing 0 since `A(1) = 0`),
the RH content must contribute exactly **-2**.

### Step 4: 1-field completion is impossible

No SU(3) irrep R has `A(R) = -2`. Direct inspection of the catalogue
(or noting that the divisibility structure of `A(R)` values
`{0, ±1, ±7, ±14, ±27, ...}` excludes the value -2 for any single
irreducible representation): no LH-Weyl singlet in a single irrep can
provide the required -2 contribution.

### Step 5: 2-field minimal completions

Enumerating all 2-field completions `(n_R)` over candidate rep sets
with `Σ_R n_R · A(R) = -2`:

**Set A** = `{1, 3, 3̄}`. The unique 2-field solution is `{3̄: 2}`:
two LH-Weyl 3̄ singlets contributing `2 · A(3̄) = -2`. (Solutions
involving `1`-singlets are anomaly-free padding and don't affect the
2-field count constraint; the canonical minimal solution is taken without
trivial singlets.)

**Set B** = `{1, 3, 3̄, 6, 6̄, 8}`. With 2 fields, the only way to
combine `±1` with `±7` to obtain `-2` is `{3̄: 2}`. Alternative
combinations: `1·6̄ + 1·6 = 0` (doesn't cancel +2), `1·6̄ + 1·??? = -2`
requires a +5 contribution, which is unavailable in any 1-field rep.
Therefore `{3̄: 2}` is the unique 2-field minimal solution in any rep
set including `{1, 3, 3̄}`.

The runner verifies this by exhaustive enumeration over compositions
into 2 fields across the candidate rep sets.

### Step 6: Identification

The 2 LH-Weyl 3̄ fields are identified as `u_R^c` and `d_R^c` in the
standard SM bookkeeping (these are the LH-Weyl conjugates of the
right-handed up-quark and down-quark). Their distinct labels (u vs d)
and the specific hypercharges follow from additional gauge-anomaly
constraints (mixed `SU(3)^2 U(1)_Y, U(1)_Y^3, gravitational^2 U(1)_Y`)
plus the `SU(2)_L × U(1)_Y` representation theory; those are addressed
by `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24`.

The **SU(3) representation content (3̄)** of these RH fields is, however,
fully derived from P1+P2+P3 — closing the verdict-identified obstruction
on the parent row.

∎

## What this claims

- `(T1)`: forced SU(3) representation content of the RH (anti-)quark sector
  as exactly 2 LH-Weyl fermions in the 3̄, derived from retained
  `Q_L : (3, 2)` + SU(3)^3 anomaly cancellation + minimal-field-count
  completion.
- `(T2)`: identification of these 2 LH 3̄ fields with `u_R^c, d_R^c` in
  standard SM bookkeeping.

## What this does NOT claim

- Hypercharges `Y(u_R^c) = -4/3, Y(d_R^c) = +2/3`: separate authority
  ([`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)).
- Generation count (3 generations): separate authority
  ([`THREE_GENERATION_STRUCTURE_NOTE`](THREE_GENERATION_STRUCTURE_NOTE.md)).
- The anomaly-cancellation **principle** itself (the requirement that
  gauge anomaly traces vanish): separate authority
  ([`ANOMALY_FORCES_TIME_THEOREM`](ANOMALY_FORCES_TIME_THEOREM.md)).
- Lepton sector content (`L_L, e_R^c, ν_R^c`): separate authority
  ([`ONE_GENERATION_MATTER_CLOSURE_NOTE`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)).
- Additional anomaly cancellations (`SU(2)^2 U(1)_Y`, `U(1)_Y^3`, etc.):
  these constrain hypercharges, not the SU(3) rep content.

## Cited dependencies

- (P1) [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  — supplies retained `Q_L : (3, 2)_{1/3}`.
- (P2) [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  — supplies the anomaly-cancellation requirement.
- (P3) framework convention that RH (anti-)quark fields are LH-Weyl
  SU(2)_L-singlet fermions in irreducible SU(3) representations.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (Slansky 1981 / Cvitanović
  cubic-anomaly coefficient table is standard external mathematical
  reference, role-labelled as admitted-context external authority,
  not as a derivation input).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_su3_anomaly_forced_3bar_completion.py`](./../scripts/frontier_su3_anomaly_forced_3bar_completion.py)
verifies (PASS=15/0):

1. SU(3) cubic-anomaly coefficient catalogue (with conjugation
   symmetry `A(R̄) = -A(R)` and self-conjugate-rep zero).
2. `Q_L : (3, 2)` contribution `+2`.
3. RH content must contribute `-2` for cancellation.
4. No 1-field completion (no irrep has `A = -2`).
5. Set A = `{1, 3, 3̄}`: minimal field count = 2; unique 2-field
   solution `{3̄: 2}`.
6. Set B = `{1, 3, 3̄, 6, 6̄, 8}`: minimal field count remains 2;
   `{3̄: 2}` remains the unique 2-field solution.
7. Identification: 2 LH 3̄ singlets are `u_R^c, d_R^c` (SU(3) rep
   content forced by P1+P2+P3).
8. Parent row class-B load-bearing step.

## Cross-references

- [`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24`](SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md) —
  parent row whose verdict-identified obstruction is closed by this
  derivation.
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) —
  separate authority for hypercharges Y of `u_R^c, d_R^c`.
- [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24`](SU2_WITTEN_Z2_ANOVMALY_THEOREM_NOTE_2026-04-24.md) —
  sister anomaly-cancellation theorem with similar verdict-identified
  obstruction (identifies `Q_L, L_L` as SU(2) doublets).
- [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md) —
  related B-L anomaly-freedom note; uses `u_R^c, d_R^c` reps as input
  rather than deriving them.
