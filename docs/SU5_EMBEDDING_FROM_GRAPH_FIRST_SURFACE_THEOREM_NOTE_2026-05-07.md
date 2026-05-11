# SU(5) Embedding Consistency from Graph-First Surface

**Date:** 2026-05-07
**Type:** bounded_theorem
**Admitted context inputs:** staggered-Dirac realization derivation target
(canonical parent:
`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`;
see `MINIMAL_AXIOMS_2026-05-03.md`).
**Status:** structural representation-theory / algebraic embedding-consistency
theorem on the current graph-first SU(3) × SU(2) × U(1)_Y surface plus the
LHCM atlas (cycles 1-3) and STANDARD_MODEL_HYPERCHARGE_UNIQUENESS. Conditional
on those upstream surfaces as explicit imports; not a new axiom or admission.
**Review role:** provides the bounded algebraic replacement candidate for
cycles 16 and 19's "admitted SU(5) gauge-group embedding" and "admitted
Y_GUT = √(3/5)·Y_SM normalization" by deriving them as direct algebraic
consequences of the LHCM hypercharge structure plus representation-theory of
`5̄ ⊕ 10 ⊕ 1` of SU(5). Independent audit decides whether this candidate can
replace those admissions in the effective dependency chain.
**Primary runner:** `scripts/frontier_su5_embedding_from_graph_first_surface.py`

## 0. Statement

**Theorem (SU(5) embedding consistency).** Let

```text
G_GFS = SU(3)_color × SU(2)_weak × U(1)_Y
```

be the current graph-first gauge group on the LH-doublet surface (cited in
[`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) §1
via the `gl(3) ⊕ gl(1)` commutant theorem of
[`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md))
and let the one-generation matter content be the 16-chirality LH-doublet +
SU(2)-singlet RH completion of
[`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
+ [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
with hypercharges (doubled convention `Q = T_3 + Y/2`)

```text
Y(Q_L) = +1/3,  Y(L_L) = −1,
Y(u_R) = +4/3,  Y(d_R) = −2/3,  Y(e_R) = −2,  Y(ν_R) = 0.
```

Then there exists an injective Lie-algebra embedding

```text
ι : g_GFS = su(3) ⊕ su(2) ⊕ u(1)_Y  ↪  su(5)
```

(canonical up to inner automorphisms fixing the standard `3 + 2` block
decomposition of the defining 5; the choice of SU(5) itself vs. larger
groups containing it is *not* claimed unique — see §2) such that the
all-LH (conjugate-RH) form of the framework's one-generation matter
content decomposes as

```text
[matter]_one_gen,LH  =  5̄  ⊕  10  ⊕  1                                     (★)
```

where the SU(5) representations have the standard branching

```text
5̄  =  (3̄, 1)_{Y_min=+1/3}   ⊕   (1, 2)_{Y_min=−1/2},
10 =  (3, 2)_{Y_min=+1/6}    ⊕   (3̄, 1)_{Y_min=−2/3}   ⊕   (1, 1)_{Y_min=+1},
 1 =  (1, 1)_{Y_min=0}.
```

The matching is exact: every chirality has a unique (color × isospin × Y_min)
slot in (★) and every slot in (★) is filled. The embedded U(1)_Y generator,
in the SU(5) Cartan basis of the defining 5, is the canonical traceless
generator

```text
T_24  =  (1/√(60)) · diag(−2, −2, −2, +3, +3),                              (✦)
```

which is the unique (up to sign and overall scale) traceless diagonal
SU(5) generator commuting with `su(3) ⊕ su(2) ⊂ su(5)` and with vanishing
trace on each `(3, 1)` and `(1, 2)` block of the standard `3 ⊕ 2`
splitting of the defining 5. The GUT normalization

```text
Y_GUT  =  √(3/5) · Y_min     (equivalently  Y_GUT²  =  (3/20) · Y²)         (✧)
```

then follows by the trace identity

```text
Tr[Y_GUT²]_5̄+10  =  Tr[T_a²]_5̄+10  =  2     per Weyl family,
```

which, under (★), forces the rescaling factor `√(3/5)` between `Y_GUT` and
`Y_min` (equivalently `√(3/20)` between `Y_GUT` and `Y` in doubled convention).

(★) and (✦) together state that the framework's gauge group sits inside SU(5)
as the manifest `(3+2)`-block subgroup, and that its matter content fills
exactly the standard SU(5) 5̄ ⊕ 10 ⊕ 1 representation slots. (✧) is
trace-forced.

## 1. What this addresses

This theorem addresses two prior admissions in the cycle 16 / cycle 19 chain
(`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`,
`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`):

| Prior admitted item | Now derived |
|---|---|
| SU(5) gauge-group embedding (admitted "standard GUT structure") | (★) algebraic decomposition of LHCM matter into 5̄ ⊕ 10 ⊕ 1, with explicit Cartan embedding (✦) |
| Y_GUT = √(3/5) · Y_SM normalization (admitted) | (✧) trace-forced from Tr[Y_GUT²] = Tr[T_a²]_simple consistency on the embedded matter content, conditional on [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) (Y5) |

If independent audit accepts this bounded theorem and its upstream imports,
the residual external content in the cycle 19 sin²θ_W^GUT = 3/8 derivation is
the GUT-scale unification assumption `g_3 = g_2 = g_1` and the GUT scale
itself (~10^16 GeV). Both are physical assumptions about coupling running,
not representation-theory statements, and remain admitted at the cycle 19
surface.

## 2. What this does NOT claim

- **Does not claim SU(5) is uniquely forced.** The same matter content fits
  16 of SO(10) (which contains 5̄ ⊕ 10 ⊕ 1 of SU(5)), or larger-group
  embeddings (E6 ⊃ SO(10) ⊃ SU(5)). The theorem asserts SU(5)-embedding
  *consistency*, not minimality among admissible GUT groups.
- **Does not claim coupling unification.** `g_3 = g_2 = g_1` at any specific
  scale is not a statement of representation theory; it is a physical
  assumption about RG running. This theorem makes no claim about whether or
  at what scale couplings unify.
- **Does not derive the GUT scale.** The scale at which SU(5) is supposed
  to be unbroken (~10^16 GeV) is not addressed.
- **Does not derive proton decay.** SU(5)-induced proton decay rates depend
  on the scale and on coupling-unification dynamics, neither of which is
  derived here.
- **Does not retain LHCM convention.** The Convention A vs B (doubled vs
  minimal `Y`) reclassification noted in cycle 16 is unchanged: `Y_GUT² /
  Y² = 3/20` in doubled convention or `Y_GUT² / Y_min² = 3/5` in minimal
  convention; either form is the same physics, and the convention choice
  is governance-side.
- **Does not close the staggered-Dirac open gate.** The matter content is
  imported from LHCM atlas + STANDARD_MODEL_HYPERCHARGE_UNIQUENESS, both of
  which depend on the staggered-Dirac realization derivation target listed
  in `MINIMAL_AXIOMS_2026-05-03.md`. This theorem inherits that admission
  via `admitted_context_inputs`.

## 3. Declared Inputs

| Input | Source |
|---|---|
| graph-first SU(3) ⊂ commutant of selected weak axis | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| graph-first SU(2)_weak from bipartite + selected-axis structure | [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) §1 |
| graph-first U(1)_Y as traceless generator in `gl(3) ⊕ gl(1)` commutant | [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) (1)–(2) |
| LH content `Q_L : (2, 3)_{+1/3}, L_L : (2, 1)_{−1}` | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) |
| RH SU(2)-singlet completion + uniqueness `(y_1, y_2, y_3, y_4) = (+4/3, −2/3, −2, 0)` | [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) |
| three-generation orbit algebra `8 = 1 + 1 + 3 + 3` | [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) |
| `Tr[Y_GUT²]_three_gen = Tr[T_a²]_SU(2),three_gen = Tr[T_a²]_SU(3),three_gen = 6` | [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) (Y5) |

No observed coupling, mass, scale, or running input is used. The SU(5)
embedding is derived as algebraic representation theory on the imported
matter content; the SU(5) group itself is treated as the standard `5×5`
unitary unimodular Lie group, not as a GUT-scale physical postulate.

## 4. Derivation

### 4.1 LH-form transcription of the framework's one-generation content

Pass to all-LH form by writing each RH chirality as the LH conjugate of its
antiparticle: `u_R → u^c_L` etc. Conjugation flips sign of every additive
quantum number; in particular `Y(u_R) = +4/3` becomes `Y(u^c_L) = −4/3` in
doubled convention, equivalently `Y_min = −2/3`. Apply this to all four RH
species:

| RH state | Y (doubled) | LH conjugate | Y_min(conjugate) |
|---|---:|---|---:|
| `u_R : (1, 3)_{+4/3}` | `+4/3` | `u^c_L : (1, 3̄)_{−4/3}` | `−2/3` |
| `d_R : (1, 3)_{−2/3}` | `−2/3` | `d^c_L : (1, 3̄)_{+2/3}` | `+1/3` |
| `e_R : (1, 1)_{−2}`   | `−2`   | `e^c_L : (1, 1)_{+2}` | `+1`   |
| `ν_R : (1, 1)_{0}`    | `0`    | `ν^c_L : (1, 1)_{0}` | `0`    |

Together with the LH-doublet content unchanged:

| LH state | (su3, su2) | Y (doubled) | Y_min |
|---|---|---:|---:|
| `Q_L : (2, 3)_{+1/3}` | `(3, 2)`   | `+1/3` | `+1/6` |
| `L_L : (2, 1)_{−1}`   | `(1, 2)`   | `−1`   | `−1/2` |

The full all-LH content per generation has 16 chiralities labelled by
`(SU(3)-rep, SU(2)-rep, Y_min)`:

```text
Q_L      : (3,  2, +1/6)   6 states
u^c_L    : (3̄, 1, −2/3)  3 states
d^c_L    : (3̄, 1, +1/3)  3 states
L_L      : (1,  2, −1/2)  2 states
e^c_L    : (1,  1, +1)    1 state
ν^c_L    : (1,  1, 0)     1 state
                          ----------
                          16 states / generation.
```

### 4.2 Standard SU(5) representation branchings

The defining `5` of SU(5), under the manifest `SU(3) × SU(2) ⊂ SU(5)`
embedding (`5 = 3 ⊕ 2`), branches to `(3, 1) ⊕ (1, 2)`. The hypercharge
generator must commute with `su(3) ⊕ su(2)` and lie in the SU(5) Cartan. Up
to sign and overall scale the unique such generator is

```text
Y̌  :=  diag(−1/3, −1/3, −1/3, +1/2, +1/2)                               (✦′)
```

acting on the defining 5 with `Y_min` eigenvalues `(−1/3, +1/2)` on the
`(3, 1)` and `(1, 2)` blocks respectively. (Tracelessness fixes the ratio
`(−1/3) : (+1/2) = −2/3 : +1`, equivalently `(−2, −2, −2, +3, +3) / 6`,
identifying `Y̌` with the canonical Standard Model hypercharge in `Y_min`
units.) The standard SU(5) branchings then give

```text
5  =  (3, 1)_{−1/3}  ⊕  (1, 2)_{+1/2},
5̄  =  (3̄, 1)_{+1/3}  ⊕  (1, 2)_{−1/2},
10  =  ∧²(5)
     =  (3̄ × 1, anti²)_{−2/3}  ⊕  (3, 2; mixed)_{+1/6}  ⊕  (1, anti²)_{+1}
     =  (3̄, 1)_{−2/3}  ⊕  (3, 2)_{+1/6}  ⊕  (1, 1)_{+1},
1   =  (1, 1)_0.
```

### 4.3 Slot-by-slot match

Compare §4.1 LH content with §4.2 SU(5) decompositions:

| LH chirality (LHCM) | (SU(3), SU(2), Y_min) | SU(5) slot |
|---|---|---|
| `Q_L`     | `(3,  2, +1/6)`  | `10 ⊃ (3, 2)_{+1/6}` ✓ |
| `u^c_L`   | `(3̄, 1, −2/3)` | `10 ⊃ (3̄, 1)_{−2/3}` ✓ |
| `e^c_L`   | `(1,  1, +1)`    | `10 ⊃ (1, 1)_{+1}` ✓ |
| `d^c_L`   | `(3̄, 1, +1/3)` | `5̄ ⊃ (3̄, 1)_{+1/3}` ✓ |
| `L_L`     | `(1,  2, −1/2)`  | `5̄ ⊃ (1, 2)_{−1/2}` ✓ |
| `ν^c_L`   | `(1,  1, 0)`     | `1` ✓ |

Every LHCM chirality has a unique slot, and every slot in `5̄ ⊕ 10 ⊕ 1`
is filled exactly once. The state-count bookkeeping is

```text
|5̄|  =  3 + 2  =  5,                |10|  =  3 + 6 + 1  =  10,                |1| = 1,
|5̄ ⊕ 10 ⊕ 1|  =  16  =  |LH content|.
```

This is identity (★).

### 4.4 Hypercharge-generator embedding (✦)

The U(1)_Y generator must:
- commute with `su(3) ⊕ su(2) ⊂ su(5)`,
- lie in the SU(5) Cartan subalgebra,
- vanish in trace on the defining 5.

By Schur's lemma applied to the irreducible representations `3` of
`su(3)` and `2` of `su(2)` on the defining 5, any element of `gl(5, ℂ)`
commuting with the standard `su(3) ⊕ su(2)` block embedding is
block-scalar on each invariant block — i.e. equal to `a · I_3 ⊕ b · I_2`
for some `a, b ∈ ℂ`. Restriction to the SU(5) Cartan + tracelessness gives
`a, b ∈ ℝ` with `3a + 2b = 0`. Up to overall scale this fixes the unique
generator

```text
Y_GUT  ∝  diag(−2, −2, −2, +3, +3) / 6.
```

The proportionality constant is set by §4.5 trace consistency. With the
canonical SU(5) Killing-form normalization (`Tr[T_a T_b] = (1/2) δ_{ab}` on
the defining 5), the embedded hypercharge generator is

```text
T_24  =  (1/√(60)) · diag(−2, −2, −2, +3, +3),                            (✦)
```

with `Tr[T_24²]_5 = 1/2`, matching the SU(5) Dynkin index of the
fundamental.

### 4.5 GUT normalization (✧) by trace consistency

The rescaling factor between `Y_min` and `Y_GUT` is forced *given the
SU(5) Killing-form normalization convention* `Tr[T_a T_b]_5 = (1/2) δ_{ab}`
for SU(5) generators acting on the defining 5 (i.e. canonical Dynkin index
`T(fund) = 1/2`). This is the standard GUT convention; without it the
"trace consistency" comparison in this section is vacuous, so we surface
it explicitly here as a convention input rather than a hidden assumption.

Acting on `5̄` (with sign flip), `Y_GUT` has eigenvalues `+1/3` on the
`(3̄, 1)` block (3 states) and `−1/2` on the `(1, 2)` block (2 states), in
units of the same √(3/5) prefactor that converts `Y_min` to `Y_GUT`:

```text
Y_GUT(5̄)  =  √(3/5) · Y_min(5̄).
```

Concretely:

```text
Tr[Y_GUT²]_5̄  =  3 · (√(3/5) · 1/3)² + 2 · (√(3/5) · 1/2)²
              =  (3/5) · (3 · 1/9 + 2 · 1/4)
              =  (3/5) · (1/3 + 1/2)
              =  (3/5) · (5/6)
              =  1/2.

Tr[Y_GUT²]_10 =  3 · (√(3/5) · 2/3)² + 6 · (√(3/5) · 1/6)² + 1 · (√(3/5) · 1)²
              =  (3/5) · (3 · 4/9 + 6 · 1/36 + 1 · 1)
              =  (3/5) · (4/3 + 1/6 + 1)
              =  (3/5) · (5/2)
              =  3/2.

Tr[Y_GUT²]_5̄+10  =  1/2 + 3/2  =  2.
```

The same trace, computed instead from `Tr[T_a²]_5̄+10`, equals
`T(5̄) + T(10) = 1/2 + 3/2 = 2` (Dynkin indices of the SU(5) fundamental and
antisymmetric reps). Hence

```text
Tr[Y_GUT²]_5̄+10  =  Tr[T_a²]_5̄+10  =  2     per Weyl family,
```

which is identity (Y5) of [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
(catalogued there at three-generation level: `Tr[Y_GUT²]_three_gen = 6`).

The rescaling factor `√(3/5)` between `Y_GUT` and `Y_min` is forced by this
identity: a different rescaling `Y_GUT = c · Y_min` would give
`Tr[Y_GUT²]_5̄+10 = c² · 10/3` (using `Tr[Y_min²]_5̄+10 = 10/3` from the
LHCM-derived hypercharges per Weyl family in Convention B), which equals 2
iff `c² = 3/5`, i.e. `c = √(3/5)`. ∎

### 4.6 Three-generation extension

The three-generation orbit algebra
([`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md))
gives identical hypercharges per generation, so (★) holds in each generation
copy independently. Three-generation traces are simply 3× the per-generation
values, recovering identity (Y5) `Tr[Y_GUT²]_three_gen = Tr[T_a²]_SU(2),three_gen
= Tr[T_a²]_SU(3),three_gen = 6`.

## 5. Independence from cycle 19's GUT-scale assumption

Cycle 19's `SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`
derives `sin²θ_W^GUT = 3/8` from:
1. LHCM hypercharges (cycles 1-3),
2. cycle 16's `Tr[Y²] = 40/3` per generation,
3. SU(5) GUT-group embedding (admitted),
4. Y_GUT = √(3/5)·Y_SM normalization (admitted),
5. SU(5) unification at GUT scale (admitted).

After this theorem, items (3) and (4) are derived (this theorem's (★) and
(✧) respectively). Items (1) and (2) are upstream imported results; the audit
lane determines retained-grade status.
Two external admissions remain at the cycle 19 surface:

- **(5)** `g_3 = g_2 = g_1` at GUT scale (coupling-unification physical
  assumption about RG running).
- **(6)** Choice of SU(5) (vs. SO(10), E6, …) as the GUT group. This
  theorem proves embedding *consistency*, not minimality, so the choice
  of which simple group containing `su(3) ⊕ su(2) ⊕ u(1)` to embed in is
  not derived. The same matter content fits 16 of SO(10) which contains
  `5̄ ⊕ 10 ⊕ 1` of SU(5).

Both are physical / external choices, not representation-theory
statements, and remain admitted at the cycle 19 surface.

The explicit form of `sin²θ_W^GUT = 3/8` (proved in cycle 19) is unchanged
by this note. What changes is the load-bearing structure of cycle 19's
proof: three of its five admitted ingredients now have explicit
representation-theoretic derivation.

## 6. Status

```yaml
actual_current_surface_status: structural representation-theory / algebraic embedding-consistency theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on LHCM atlas (cycles 1-3, currently bounded via the
  staggered-Dirac realization derivation target per
  MINIMAL_AXIOMS_2026-05-03.md), STANDARD_MODEL_HYPERCHARGE_UNIQUENESS
  (unaudited), and HYPERCHARGE_SQUARED_TRACE_CATALOG (unaudited).
  The theorem itself is exact algebra on Fraction-precision; runner verifies
  all 16 chirality slot assignments and the Tr[Y_GUT²] = Tr[T_a²] = 2
  identity. Audit status and effective status are independent-lane decisions.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_su5_embedding_from_graph_first_surface.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: SU(5) embedding consistency derived from LHCM hypercharges +
representation-theory of 5̄ ⊕ 10 ⊕ 1; Y_GUT = √(3/5)·Y_min trace-forced.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings present.
2. **LHCM chirality table.** All 16 LH-form chiralities have correct
   `(SU(3), SU(2), Y_min)` labels via direct computation from LHCM
   doubled-convention hypercharges.
3. **SU(5) representation branchings — derived, not asserted.** `5 = (3,1)_{−1/3}
   ⊕ (1,2)_{+1/2}` is derived from `T_24 = (1/√60)·diag(−2,−2,−2,+3,+3)`
   eigenvalues plus the `Y_min = Y_GUT/√(3/5)` rescaling. `10 = ∧²(5)`
   branching is derived from antisymmetric tensor decomposition: `∧²(3,1) =
   (3̄,1)` with doubled Y, `(3,1) ⊗ (1,2) = (3,2)` with summed Y, `∧²(1,2)
   = (1,1)` with doubled Y. The `1 = (1,1)_0` SU(5)-singlet is the unique
   trivial-irrep slot.
4. **Slot match (★).** Each LHCM chirality maps to a unique SU(5) slot
   and every slot is filled.
5. **State-count bookkeeping.** `|5̄ ⊕ 10 ⊕ 1| = 16 = |LH content|` per
   generation.
6. **Hypercharge-generator embedding (✦).** `T_24 ∝ diag(−2,−2,−2,+3,+3)`
   commutes with `su(3) ⊕ su(2)` and is traceless; SU(5) normalization
   gives `Tr[T_24²]_5 = 1/2`.
7. **Trace consistency (✧).** `Tr[Y_GUT²]_5̄+10 = Tr[T_a²]_5̄+10 = 2`
   per Weyl family in Convention B; `Y_GUT² = (3/5) · Y_min²`.
8. **Three-generation lift.** `Tr[Y_GUT²]_three_gen = Tr[T_a²]_three_gen
   = 6` matches HYPERCHARGE_SQUARED_TRACE_CATALOG (Y5).
9. **What is NOT claimed.** Negative checks: no minimality claim, no
   unification claim, no proton-decay claim, no GUT-scale derivation.
10. **Cycle 16/19 admission-replacement scope.** The note explicitly records
    the bounded candidate that addresses the SU(5) gauge-group embedding
    admission and Y_GUT normalization admission, while leaving the GUT-scale
    unification assumption residual at cycle 19's surface.

## 8. Cross-references

- `FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`
  — cycle 16, admission addressed by this bounded embedding candidate
- `SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`
  — cycle 19, admissions addressed for SU(5) embedding + Y_GUT normalization;
  GUT-unification assumption remains external
- [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
  — (Y5) trace identity used to force √(3/5) normalization
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  — RH hypercharge uniqueness (`y_1 = +4/3`, `y_2 = −2/3`, `y_3 = −2`,
  `y_4 = 0`)
- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  — graph-first U(1)_Y as traceless commutant generator
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  — LH content `Q_L`, `L_L` and matter assignment
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  — graph-first SU(3) commutant
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
  — three-generation orbit algebra
- `MINIMAL_AXIOMS_2026-05-03.md` — current
  axiom set + open gates (staggered-Dirac realization derivation target)
- Standard references: Georgi–Glashow (1974), Slansky (1981) tables.
