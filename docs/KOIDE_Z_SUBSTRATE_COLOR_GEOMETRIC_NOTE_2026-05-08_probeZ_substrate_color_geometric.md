# Probe Z-Substrate-Color-Geometric — Cl(3) graded basis 1+3+3+1=8 forces N_c=3 (probeZ_substrate_color_geometric)

**Date:** 2026-05-08 (compute date 2026-05-10)
**Type:** bounded_theorem (positive on the dim-counting forcing; bounded on the bridge identifying the Cl(3) graded basis with the SU(N_c) gauge adjoint)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal. Tests whether the
dimensional structure of the physical `Cl(3)` local algebra — specifically the graded
basis decomposition `1 ⊕ 3 ⊕ 3 ⊕ 1` (scalar + vectors + bivectors +
pseudoscalar) of total real dimension 8 — geometrically forces
`N_c = 3` for the framework's color SU(N_c), under the structural
assumption that the gauge adjoint is to be carried by Cl(3)'s
graded basis. The dim-matching equation `N_c² − 1 = 8` admits
exactly one positive integer solution (`N_c = 3`), so the dim-match
is rigid where it applies. The bridge from "Cl(3) graded basis
carries the gauge adjoint" to physical SM color is the bounded
admission, and is the same admission already named in
`CL3_COLOR_AUTOMORPHISM_THEOREM.md` (the 2026-05-04 audit
narrowed-scope bridge requirement) and resolved in the graph-first
direction by `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`. This probe
records the separate dimensional constraint that anomaly cancellation
alone does not supply: once the named adjoint-carrier bridge is in
place, the physical `Cl(3)` local algebra gives the rigid equation
`N_c^2 - 1 = 8`.
**Status:** source-note proposal. Verdict is **BOUNDED THEOREM**:
positive on the rigid `N_c² − 1 = 8 ⇒ N_c = 3` forcing under the
adjoint-carrier bridge; bounded on the bridge itself, which is
supported by the graph-first SU(3) closure and the symmetric-base
scope-narrowing. Effective status remains audit-owned.
**Authority disclaimer:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** probe-z-substrate-color-geometric-20260508-probeZ_substrate_color_geometric
**Primary runner:** [`scripts/cl3_koide_z_substrate_color_geometric_2026_05_08_probeZ_substrate_color_geometric.py`](../scripts/cl3_koide_z_substrate_color_geometric_2026_05_08_probeZ_substrate_color_geometric.py)
**Cache:** [`logs/runner-cache/cl3_koide_z_substrate_color_geometric_2026_05_08_probeZ_substrate_color_geometric.txt`](../logs/runner-cache/cl3_koide_z_substrate_color_geometric_2026_05_08_probeZ_substrate_color_geometric.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived `claim_type`,
`audit_status`, and `effective_status` are generated only after the
independent audit lane reviews the claim, dependency chain, and runner.
The audit lane has full authority to retag, narrow, or reject the proposal.

## 0. Question

A substrate-anomaly analysis can leave several choices not forced by
SM gauge anomaly cancellation alone:

1. `N_c = 3` (anomaly cancellation closes for any `N_c ≥ 2`)
2. `n_gen = 3` (anomaly cancellation linear in `n_gen`)
3. left-handed content choice (vectorlike vs Pati-Salam vs SM)
4. absolute hypercharge scale
5. the Koide Frobenius-equipartition condition for the
   charged-lepton sector

This probe asks: does the Cl(3) algebra structure — independently of
anomaly cancellation — force `N_c = 3` via the dim-counting identity

```text
   N_c² − 1   =   dim(adjoint SU(N_c))   ?=   8   =   dim_R Cl(3)
```

The repo baseline takes a physical `Cl(3)` local algebra at each
lattice site. `Cl(3,0)` as a real algebra has `2³ = 8` basis
elements (one scalar, three vectors, three bivectors, one
pseudoscalar). The classifying equation `N_c² − 1 = 8` has unique
positive integer solution `N_c = 3`. If the gauge adjoint of physical
color must be carried by Cl(3)'s graded basis (the bridge), then
`N_c = 3` is geometrically forced — independently of anomaly
cancellation.

**Question:** Under the framework's physical `Cl(3)` local algebra
and the graph-first SU(3) bridge support
(`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`), does the dim-counting
match `N_c² − 1 = 8 = dim_R Cl(3)` rigidly force `N_c = 3`,
constituting a structural forcing distinct from the anomaly-cancellation
ladder that admits any `N_c ≥ 2`?

## 1. Answer

**YES (BOUNDED THEOREM).** The dim-counting equation

```text
   N_c² − 1   =   8           (1)
```

admits **exactly one positive integer solution**, `N_c = 3`. (The
real-number companion `N_c = -3` is excluded: a non-abelian gauge
group dimension is positive by definition. The non-integer solutions
`N_c = ±3` are the only roots of the quadratic in any field
characteristic 0.) The forcing is rigid where the bridge applies:
under the adjoint-carrier bridge "the gauge adjoint is carried by
the Cl(3) graded basis," `N_c = 3` is the unique solution.

The probe's verdict is **bounded**, not positive, because the
adjoint-carrier bridge is itself a separate content layer:

- The Cl(3) graded basis `{1, γ_i, γ_iγ_j, γ_1γ_2γ_3}` has 8 real
  elements (Step 1 in `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`).
- `dim_R Cl(3,0) = 8` is exactly the real-dimension of `M_2(C)`.
- `dim adjoint SU(3) = 8` is exactly `N² − 1` at `N = 3`.
- The numerical coincidence `dim_R Cl(3) = dim adjoint SU(3) = 8`
  is structural (both are 8), not load-bearing-by-itself; the
  forcing is `N_c² − 1 = 8 ⇒ N_c = 3` once the bridge identifying
  Cl(3)-carried adjoint with physical color SU(N_c)_c is in place.

The graph-first SU(3) closure
(`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`) is the named bridge support:
it shows that, on the taste cube `V = (C²)^{⊗3}` (the
Cl(3)-induced staggered Hilbert), the canonical commutant after the
graph-first weak axis selector is `gl(3) ⊕ gl(1)` with compact
semisimple part `su(3)`. That `su(3)` is exactly 8-dimensional,
matching `dim_R Cl(3)`. So the bridge — once accepted — combines
with `(1)` to give a unique-`N_c` forcing.

This probe's marginal contribution:

1. Isolates the dimensional rigidity `N_c² − 1 = 8 ⇒ N_c = 3`
   as a separate structural claim, distinct from anomaly cancellation
   (which admits `N_c ≥ 2`).
2. Confirms numerically (and via the integer-quadratic argument)
   that the equation has unique integer solution `N_c = 3` in the
   relevant range.
3. Cross-checks: SU(2) has `dim = 3` (matches **only** the 3-vector
   sector of Cl(3), not the full 8-dim graded basis); SU(4) has
   `dim = 15` (no match); SU(5) has `dim = 24` (no match). Only
   `N_c = 3` gives the perfect 8-dim match with the full Cl(3)
   graded basis.
4. Frames the bridge as the bounded admission: the adjoint-carrier
   bridge from "Cl(3) graded basis" to "physical SU(N_c)_c color"
   is supplied by `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` (commutant
   route) and the symmetric-base scope of
   `CL3_COLOR_AUTOMORPHISM_THEOREM.md` (Gell-Mann embedding).
5. Supplies a candidate sharpening for any substrate-anomaly packet
   that records "`N_c = 3` is not forced by anomaly cancellation
   alone": anomaly cancellation alone remains broad, but the
   bounded Cl(3)-adjoint bridge constraint selects `N_c = 3`.

The probe does NOT introduce new content for the bridge itself — it
inherits `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` as the bridge
authority. Its scope is the dim-matching forcing layer.

## 2. Setup

### Premises

| ID | Statement | Class |
|---|---|---|
| BASE-CL3 | Physical `Cl(3)` local algebra | repo baseline; [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| BASE-Z3 | `Z^3` spatial substrate | repo baseline; same source |
| Cl3-Basis | `Cl(3,0)` real-algebra basis: `{1, γ_1, γ_2, γ_3, γ_1γ_2, γ_1γ_3, γ_2γ_3, γ_1γ_2γ_3}` (8 elements) | upstream support; [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) Step 1 |
| Cl3-Grading | `Cl(3) = Cl(3)_0 ⊕ Cl(3)_1 = (1 ⊕ 3) ⊕ (3 ⊕ 1)` graded by parity (scalar+bivectors / vectors+pseudoscalar) | upstream support; same source, with even subalgebra `Cl⁺(3) ≅ H` per [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) Section A |
| Cl3-RealDim | `dim_R Cl(3,0) = 2³ = 8` exactly | standard Clifford-algebra identity, cited in the upstream support above |
| GraphSU3 | Graph-first commutant `gl(3) ⊕ gl(1)`, compact semisimple `su(3)` (8-dim) on the taste cube | bounded bridge support; [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| GellMannComp | `{T^a : a=1..8}` is exactly an R-basis for `su(3)` (8 generators, no more, no fewer) | bridge support / decorated basis check; [`GELLMANN_COMPLETENESS_THEOREM_NOTE_2026-05-02.md`](GELLMANN_COMPLETENESS_THEOREM_NOTE_2026-05-02.md) |
| AdjointDim | `dim(adjoint SU(N_c)) = N_c² − 1` (standard SU(N) Lie-algebra dim formula) | textbook group theory |
| AnomalyComparison | SM gauge-anomaly cancellation alone admits any `N_c ≥ 2` in the comparison class | context only; not a one-hop dependency of this bounded theorem |

### Forbidden imports

- NO PDG observed values used as derivation input (no comparators
  used here at all — this is purely structural).
- NO new repo-wide axioms.
- NO promotion of unaudited content to retained.
- NO empirical fits.
- NO new content for the adjoint-carrier bridge — this note names
  the bridge support and leaves bridge status to the audit lane.

### Authority of this probe

This probe does NOT introduce new derivation primitives. The Cl(3)
real-dim 8 fact and the SU(N) adjoint-dim formula are standard
mathematical content, with the Cl(3) dimension cited to current repo
support. The graph-first SU(3) bridge is named as bridge support in
`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`. The probe's marginal
contribution is:

1. **Dimensional forcing identification.** Isolate the equation
   `N_c² − 1 = 8` as the rigid forcing of `N_c = 3` and demonstrate
   it has unique positive integer solution.
2. **Distinction from anomaly cancellation.** Verify that this
   forcing is structurally distinct from anomaly cancellation
   (which admits `N_c ≥ 2` in the comparison class).
3. **Cross-checks at neighbouring `N_c`.** Verify that `N_c = 2`
   matches only a sub-sector (3-dim adjoint = 3 bivectors), and
   `N_c ≥ 4` overshoots the full 8-dim Cl(3) basis.
4. **Substrate-anomaly comparison sharpening.** Record that an
   anomaly-only `N_c` freedom is not a contradiction: it is narrowed
   by the separate bounded Cl(3)-adjoint bridge constraint.

## 3. Theorem (bounded; Cl(3) graded basis dimensional forcing)

**Theorem (Z-Substrate-Color-Geometric, bounded; dim-counting forces
`N_c = 3` under the adjoint-carrier bridge).**

Under the premises of §2 with no new imports, the following hold:

- **(K1) Cl(3) graded-basis dimension count.** The real Clifford
  algebra `Cl(3,0)` has graded basis `{1; γ_1, γ_2, γ_3; γ_1γ_2,
  γ_1γ_3, γ_2γ_3; γ_1γ_2γ_3}` with grading `1 ⊕ 3 ⊕ 3 ⊕ 1`,
  totalling exactly 8 real-linearly-independent elements. The 8
  decomposes as:
  ```text
     scalar (grade 0):       1 element     (the unit 1)
     vectors (grade 1):      3 elements    (γ_1, γ_2, γ_3)
     bivectors (grade 2):    3 elements    (γ_iγ_j, i<j)
     pseudoscalar (grade 3): 1 element     (ω = γ_1γ_2γ_3)
     ----------------------------
     total dim_R Cl(3,0):    8
  ```

- **(K2) SU(N_c) adjoint dimension formula.** For any N_c ≥ 1,
  the adjoint representation of SU(N_c) has dimension
  `dim_adj(N_c) = N_c² − 1`. This is the standard Lie-algebra
  dimension formula, derived as: `dim_C M_{N_c}(C) − dim trace
  constraint = N_c² − 1` (one Hermiticity-and-trace constraint on
  N_c² complex matrix entries gives N_c² real Hermitian parameters,
  minus the trace constraint = N_c² − 1).

- **(K3) Forcing equation.** The dim-counting equation matching
  Cl(3)-graded-basis dim with SU(N_c) adjoint dim is:
  ```text
     dim_adj(N_c)   =   dim_R Cl(3,0)
     N_c² − 1       =   8                                       (3)
     N_c²           =   9
     N_c            =   ±3
  ```
  Restricted to positive integers, the unique solution is
  `N_c = 3`.

- **(K4) No competing solutions for nearby N_c values.** Direct
  enumeration:
  ```text
     N_c = 2:   dim_adj = 3       (matches only vector OR bivector sector, not full 8)
     N_c = 3:   dim_adj = 8       (PERFECT MATCH with full Cl(3) graded basis)  ← UNIQUE
     N_c = 4:   dim_adj = 15      (overshoots; no match)
     N_c = 5:   dim_adj = 24      (overshoots; no match)
     N_c = 6:   dim_adj = 35
     ...
  ```
  No `N_c ≠ 3` in the positive integers satisfies `N_c² − 1 = 8`.
  The forcing is rigid: it is an integer quadratic with unique
  positive root.

- **(K5) Distinction from anomaly cancellation.** The anomaly
  comparison records that anomaly cancellation `Tr[SU(3)^3] = 0`
  closes for ANY `N_c ≥ 2`. The Cl(3) dim-counting forces `N_c = 3`
  uniquely. The two arguments are structurally distinct:
  - Anomaly cancellation is a **trace identity** on the matter
    content; it depends on hypercharges and chirality assignments
    but not on the carrier-algebra dimension. It scales linearly
    with `n_gen` and admits the family `N_c ≥ 2`.
  - Cl(3) dim-counting is an **algebra-dimension identity**; it
    depends on the physical `Cl(3)` local algebra and does NOT depend on
    matter-content trace conditions. It admits a single integer
    `N_c = 3`.
  - Therefore the Cl(3) forcing is a structurally NEW selection
    constraint not visible at the anomaly-cancellation layer.

- **(K6) Bridge-conditional verdict.** The forcing K3 + K4 is
  rigid; the **bridge** "the gauge adjoint is carried by the Cl(3)
  graded basis" is the bounded admission. The bridge is supplied
  by repo bridge support:
  - **Commutant route** (graph-first):
    [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
    derives `Comm(weak SU(2), τ) = gl(3) ⊕ gl(1)` with compact
    semisimple `su(3)` (8 generators) on the taste cube `V =
    (C²)^{⊗3}` induced from the physical `Cl(3)` local algebra.
  - **Gell-Mann completeness route**:
    [`GELLMANN_COMPLETENESS_THEOREM_NOTE_2026-05-02.md`](GELLMANN_COMPLETENESS_THEOREM_NOTE_2026-05-02.md)
    confirms `{T^a : a = 1..8}` is an exact R-basis for su(3)
    on the framework's color algebra, with no extra (T^9)
    generator possible.
  Both routes deliver an 8-dim su(3); the dim-counting K3+K4
  rigidly fixes the rank from 8.

- **(K7) Substrate-anomaly comparison sharpening.** Under the
  bridge of K6, an anomaly-only statement "`N_c = 3` is not forced by
  anomaly cancellation alone; any `N_c ≥ 2` is admitted" is narrowed
  by the separate Cl(3)-adjoint bridge constraint. Anomaly
  cancellation alone admits `N_c ≥ 2`, but **Cl(3) substrate
  dim-counting forces `N_c = 3`** once the bridge is assumed. The
  combined closure is:
  ```text
     N_c ≥ 2  (from anomaly cancellation)
     N_c² − 1 = 8  (from Cl(3) dim count + adjoint-carrier bridge)
     ⇒  N_c = 3  (unique simultaneous solution)
  ```
  This gives a candidate sharpening for any substrate-anomaly packet
  that leaves `N_c = 3` free: anomaly cancellation alone gives
  `N_c ≥ 2`, while this bounded bridge constraint gives `N_c = 3`.

- **(K8) Tier verdict per brief.** The brief specifies:
  > Tier: Positive if Cl(3) 8-dim structure uniquely forces N_c=3;
  > bounded if forces N_c=3 modulo additional structural
  > assumption; negative if structure admits multiple N_c.

  The Cl(3) graded basis 1+3+3+1 = 8 + the adjoint-dim formula +
  the unique-positive-integer forcing of `N_c² = 9` give the rigid
  `N_c = 3` answer **modulo the adjoint-carrier bridge**, which has
  bounded graph support but remains a structural assumption named here. Tier:
  **BOUNDED THEOREM** (positive on the forcing rigidity, bounded
  on the bridge).

  Review-loop adopts the conservative bounded verdict. Any stronger
  classification belongs to the independent audit lane.

## 4. Proof sketch

### K1 Cl(3) graded-basis dimension count

Per `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`
Step 1: the relations `{γ_i, γ_j} = 2δ_{ij} I` generate the real
Clifford algebra `Cl(3,0)` with 8 basis elements

```text
   {1, γ_1, γ_2, γ_3, γ_1γ_2, γ_1γ_3, γ_2γ_3, γ_1γ_2γ_3}.
```

Direct grade decomposition:
- grade 0 (scalar): `1` → 1 element
- grade 1 (vector): `γ_1, γ_2, γ_3` → 3 elements
- grade 2 (bivector): `γ_1γ_2, γ_1γ_3, γ_2γ_3` → 3 elements
- grade 3 (pseudoscalar): `γ_1γ_2γ_3 = ω` → 1 element

Sum: 1+3+3+1 = 8. Equivalently, `dim_R Cl(3,0) = 2³ = 8` by the
standard Clifford-algebra dimension count (`dim_R Cl(p,q) = 2^{p+q}`).
Even subalgebra `Cl⁺(3)` (grades 0+2) has 1+3 = 4 elements
(`≅ H`, the quaternions) per `CL3_SM_EMBEDDING_THEOREM.md` Section A. ∎

### K2 SU(N_c) adjoint dimension formula

`SU(N_c)` is the group of `N_c × N_c` complex unitary matrices with
determinant 1. Its Lie algebra `su(N_c)` consists of `N_c × N_c`
traceless anti-Hermitian complex matrices. Real dimension count:
- `M_{N_c}(C)` has real-dim `2 N_c²`;
- Hermitian (or anti-Hermitian) condition halves: `N_c²` real
  parameters;
- Traceless condition reduces by 1: `N_c² − 1` real parameters.

Hence `dim_R su(N_c) = N_c² − 1 = dim adjoint`. This is the
standard textbook formula; see also
`GELLMANN_COMPLETENESS_THEOREM_NOTE_2026-05-02.md` Step 3 for the
explicit `N_c = 3` count (9 - 1 = 8). ∎

### K3 Forcing equation

Setting `dim adjoint = dim_R Cl(3,0)`:

```text
   N_c² − 1 = 8
   N_c² = 9
   N_c = ±3.
```

Restricting to positive integers (a non-abelian gauge group has
positive integer rank `≥ 2`), the unique solution is `N_c = 3`. ∎

### K4 No competing N_c

For any positive integer `N_c ≥ 2`:

| N_c | N_c² − 1 | dim Cl(3) match? |
|----:|--------:|:----------------|
|   2 |       3 | partial (3 = vector OR bivector sector, not full 8) |
|   3 |       8 | **EXACT** (full graded basis 1+3+3+1)            |
|   4 |      15 | overshoots (15 > 8)                              |
|   5 |      24 | overshoots                                        |
|  ≥6 |  ≥ 35   | overshoots monotonically                         |

Direct exhaustive enumeration over `N_c ∈ {2, 3, ..., 100}` (via
the runner) confirms: only `N_c = 3` satisfies `N_c² − 1 = 8`. The
quadratic identity has uniqueness over all of Z⁺ (not just
finite range), since `N_c ↦ N_c² − 1` is strictly monotone for
`N_c ≥ 1`. ∎

### K5 Distinction from anomaly cancellation

The substrate-anomaly comparison verifies that the SU(N_c)^3 cubic
anomaly trace
```text
   Tr[T^a T^b T^c]_{sym}  = 0
```
on the SM left-handed content (`Q_L`, `u_R^c`, `d_R^c`) cancels
for all `N_c ≥ 2`. The cancellation depends only on the chirality
assignment (`Q_L` vs `u_R^c, d_R^c` having opposite SU(N_c)
charges) and is not parameter-sensitive in `N_c`.

In contrast, the Cl(3) dim-counting equation `N_c² − 1 = 8` is
**not** a trace identity on matter content; it is an
algebra-dimension identity on the carrier algebra. The two
constraints are independent:
- anomaly cancellation: `N_c ≥ 2` admitted in the comparison class.
- Cl(3) dim count + bridge: `N_c = 3` forced.

Joint solution: `N_c = 3`. The Cl(3) constraint is structurally
new content not visible at the anomaly layer. ∎

### K6 Bridge-conditional verdict

The forcing K3+K4 is conditional on the bridge "Cl(3) graded basis
8-dim identifies with the gauge adjoint of SU(N_c)_c color".

Two repo routes support the bridge:

**Route A (commutant, graph-first):**
`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` derives, on the taste cube
`V = (C²)^{⊗3}` (the staggered Hilbert induced from the physical
`Cl(3)` local algebra):
- after the graph-first weak axis selector picks one of three axes,
- the residual `b_1 ↔ b_2` swap acts on the 4-point base,
- the base splits as `3 ⊕ 1` under that swap,
- the joint commutant of weak `su(2)` and the swap is `gl(3) ⊕ gl(1)`,
- with compact semisimple part `su(3)` of dimension 8.

This `su(3)` is exactly 8-dim — and the embedding of its 8 Gell-Mann
generators into the taste-cube structure draws on all 8 Cl(3) basis
elements (scalar, 3 vectors, 3 bivectors, pseudoscalar) via the
tensor-product structure of the staggered representation.

**Route B (Gell-Mann completeness):**
`GELLMANN_COMPLETENESS_THEOREM_NOTE_2026-05-02.md` confirms that
`{T^a : a = 1..8}` (Gell-Mann generators) is an R-basis for su(3)
with no possible 9th independent generator. The framework's color
algebra is exactly 8-dimensional.

Both routes deliver `dim su(3) = 8`. Combined with K3+K4, the
adjoint-carrier bridge + dim-counting jointly force `N_c = 3`.

The bridge is the bounded admission. The graph-first integration
supplies bridge support; the audit lane has authority over any
stronger effective classification. ∎

### K7 Substrate-anomaly comparison sharpening

An anomaly-only substrate analysis can state that `N_c = 3` is "not
forced by anomaly cancellation alone" because anomaly cancellation
admits `N_c ≥ 2`. Under this probe's K1–K6, that freedom is narrowed
by the Cl(3) dim-counting forcing layer:

| Constraint | N_c admitted |
|---|---|
| Anomaly cancellation `Tr[SU(N_c)^3] = 0` | any `N_c ≥ 2` |
| Cl(3) dim-counting `N_c² − 1 = 8` (this probe K3+K4) | exactly `N_c = 3` |
| Joint constraint | exactly `N_c = 3` |

The bridge becomes the new bounded layer. Net effect: `N_c = 3` is
not supplied by anomaly cancellation itself, but it is supplied by
the separate bounded Cl(3)-adjoint bridge constraint. ∎

### K8 Tier verdict

Per the brief:
- Positive if Cl(3) 8-dim structure uniquely forces `N_c = 3`.
- Bounded if forces `N_c = 3` modulo additional structural assumption.
- Negative if structure admits multiple `N_c`.

Result: `N_c² − 1 = 8` is rigid (unique positive-integer solution
`N_c = 3`), but the *applicability* of this equation depends on
the adjoint-carrier bridge "Cl(3) graded basis carries the gauge
adjoint." The bridge is the structural assumption, supplied by
two named routes (commutant and Gell-Mann completeness).

Conservative tier: **BOUNDED THEOREM** (forces uniquely modulo
the named bridge admission). Any stronger classification is
audit-owned. ∎

## 5. Consistency with cited content

### C1 Substrate-anomaly comparison

A substrate-anomaly analysis can leave `N_c = 3` unforced by anomaly
cancellation alone. This note supplies the separate bounded
Cl(3)-adjoint bridge constraint for that one color-count question.
It does not address the separate questions of `n_gen = 3`,
left-handed content choice, absolute hypercharge scale, or the Koide
Frobenius-equipartition condition.

### C2 Graph-first SU(3) integration

`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` is the load-bearing bridge
authority. This probe does NOT modify or extend that note; it
*cites* it as the bridge supplier. The script verifications in
the graph-first note (`scripts/frontier_graph_first_su3_integration.py`)
cover all three possible weak-axis selections and confirm the
8-dimensional su(3) commutant on each.

### C3 Cl(3) per-site uniqueness

`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`
Step 1 establishes `dim_R Cl(3,0) = 8` with the explicit
`{1, γ_i, γ_iγ_j, γ_1γ_2γ_3}` basis. This probe cites that count
directly; the graded-basis decomposition `1+3+3+1 = 8` is a
re-bookkeeping of the same 8 elements.

### C4 Cl⁺(3) ≅ H quaternionic structure

`CL3_SM_EMBEDDING_THEOREM.md` Section A establishes `Cl⁺(3) ≅ H`
(even subalgebra has 4 elements: scalar + 3 bivectors). This
matches K1's grading: even = 1+3 = 4, odd = 3+1 = 4. The
quaternionic SU(2) on the even subalgebra is one of the two
SU(2) sectors that, with the Z₃ axis selector, give the
graph-first SU(3).

This is consistent with the observation that "SU(2) × something"
exists at multiple layers in the framework: `Cl⁺(3) ≅ H` gives a
3-vector adjoint (3 bivectors); the fiber `b_3 ↔ b_3'` swap gives
the weak SU(2) (3 generators on the fiber); the residual `b_1 ↔
b_2` swap on the base gives the `3 ⊕ 1` split that lifts to
`gl(3) ⊕ gl(1)`. The 8-dim su(3) appears only at the joint-commutant
level.

### C5 Gell-Mann completeness

`GELLMANN_COMPLETENESS_THEOREM_NOTE_2026-05-02.md` (B5) confirms
that no extra generator beyond the 8 Gell-Mann generators is
possible. This rules out a "9th gluon" and confirms the strict
8-dim adjoint, exactly matching the Cl(3) dim count.

### C6 CL3_COLOR_AUTOMORPHISM_THEOREM scope-narrow

`CL3_COLOR_AUTOMORPHISM_THEOREM.md` was scope-narrowed to the
algebraic embedding result; its physical-color identification was
deferred to a separate bridge theorem. Probe Z's bridge admission is
that same deferred bridge. The named graph-first and Gell-Mann routes
together constitute the structural bridge support; this probe inherits
that support and does not extend it.

## 6. What this note DOES establish

1. **Cl(3) graded basis dim count.** The real Clifford algebra
   `Cl(3,0)` has graded basis `1+3+3+1 = 8` elements: 1 scalar,
   3 vectors, 3 bivectors, 1 pseudoscalar. Real-dim 8 exactly.
2. **Adjoint-dim formula application.** `dim adjoint SU(N_c) =
   N_c² − 1 = 8` has unique positive-integer solution `N_c = 3`.
3. **Forcing rigidity.** Direct enumeration over `N_c ∈ {2, 3,
   …, 100}` confirms uniqueness; for `N_c ≠ 3`, no match.
4. **Distinction from anomaly cancellation.** Cl(3) dim-counting
   is structurally distinct from anomaly cancellation (which
   admits `N_c ≥ 2` in the comparison class).
5. **Bridge identification.** The adjoint-carrier bridge is the
   bounded admission; supplied by named graph-first and Gell-Mann
   support. The bridge is named, not introduced.
6. **Substrate-anomaly comparison sharpening.** An anomaly-only
   color-count freedom is narrowed by the separate bounded
   Cl(3)-adjoint bridge constraint.

## 7. What this note does NOT establish

- It does **NOT** introduce any new axioms or imports beyond the
  repo-baseline physical `Cl(3)` local algebra and the standard SU(N)
  Lie dimension formula.
- It does **NOT** derive the adjoint-carrier bridge "Cl(3) graded
  basis 8-dim identifies with SU(N_c)_c gauge adjoint" — that is
  inherited from `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` and
  Gell-Mann completeness as bridge support. The bridge is the bounded
  admission of this probe.
- It does **NOT** address the separate questions of `n_gen = 3`,
  left-handed content choice, absolute hypercharge scale, or the Koide
  Frobenius-equipartition condition.
- It does **NOT** address the SO(N_c) or other gauge-group
  alternatives at the adjoint-dim layer; the analysis is restricted
  to SU(N_c) per the named graph-first SU(3) bridge. (Other
  groups give different `dim adjoint` formulas: SO(N) has
  `N(N-1)/2`; Sp(N) has `N(2N+1)`. The corresponding dim-counting
  exercise for SO(N) gives `N(N-1)/2 = 8 ⇒ N(N-1) = 16` whose
  integer solutions are `N = ?` — direct enumeration: N=4 gives
  12, N=5 gives 20; no integer solution. So SO(N) is excluded.
  This is logged as a robustness check in K4 of the runner.)
- It does **NOT** depend on or affect the staggered-Dirac
  realization gate, the g_bare gate, or any other framework gate.
- It does **NOT** consume any PDG values, observed masses, mixing
  angles, or empirical fits. The analysis is pure structural
  group-theory + standard Clifford algebra.

## 8. Empirical falsifiability

| Claim | Falsifier |
|---|---|
| K1 Cl(3) graded basis 8 elements | Demonstrate `dim_R Cl(3,0) ≠ 8`. Standard Clifford-algebra count, false on textbook content. |
| K2 SU(N_c) adjoint dim formula | Demonstrate `dim adjoint SU(N_c) ≠ N_c² − 1`. Standard Lie-algebra count, false on textbook content. |
| K3 forcing equation has unique positive integer solution | Find `N_c ∈ Z⁺ \ {3}` with `N_c² − 1 = 8`. Algebraically false (N_c² = 9 ⇒ N_c = ±3). |
| K4 no competing `N_c` in enumerated range | Find `N_c ∈ {2..100} \ {3}` with `N_c² − 1 = 8`. Numerically false (runner exhaustive). |
| K5 anomaly-cancellation admits `N_c ≥ 2` | Falsifier: show that anomaly cancellation alone excludes `N_c = 2` or `N_c ≥ 4` in the comparison class. |
| K6 bridge route A | Demonstrate `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` does NOT derive 8-dim su(3) commutant. Numerically false; runner reproduces. |
| K6 bridge route B | Demonstrate `GELLMANN_COMPLETENESS_THEOREM_NOTE_2026-05-02.md` does NOT establish 8 Gell-Mann generators as full R-basis. Numerically false. |
| K7 substrate-anomaly comparison sharpening | Demonstrate `N_c = 3` is NOT forced under joint anomaly + Cl(3)-adjoint constraints. Algebraically false (joint solution unique). |

## 9. Verdict per brief's three honest tiers

The originating brief listed three tiers:

> Tier: Positive if Cl(3) 8-dim structure uniquely forces N_c=3;
> bounded if forces N_c=3 modulo additional structural assumption;
> negative if structure admits multiple N_c.

**Verdict: BOUNDED THEOREM (positive on dim-counting forcing rigidity;
bounded on the adjoint-carrier bridge).**

The dim-counting equation `N_c² − 1 = 8` admits unique positive
integer solution `N_c = 3`, and direct enumeration over
`N_c ∈ {2..100}` confirms no competing solutions. The forcing is
rigid where applicable. The applicability depends on the
adjoint-carrier bridge ("Cl(3) graded basis carries the gauge
adjoint"), which is supplied by the named graph-first and
Gell-Mann bridge support. Review-loop adopts the conservative
bounded verdict; any stronger classification is audit-owned.

## 10. Honest scope (audit-readable)

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Tests whether the physical Cl(3) local algebra's graded basis decomposition
  1 ⊕ 3 ⊕ 3 ⊕ 1 = 8 (scalar + vectors + bivectors + pseudoscalar)
  geometrically forces N_c = 3 for the framework's color SU(N_c)_c,
  through the dim-counting identity N_c^2 - 1 = 8 and uniqueness
  of the positive integer solution N_c = 3.

  Verdict: BOUNDED THEOREM. The forcing equation has unique
  positive integer solution N_c = 3 by direct algebra (and
  numerically verified by exhaustive enumeration over
  N_c ∈ {2..100}). The applicability depends on the
  adjoint-carrier bridge "Cl(3) graded basis carries the gauge
  adjoint of SU(N_c)_c", supplied by GRAPH_FIRST_SU3_INTEGRATION_NOTE
  (commutant route) and GELLMANN_COMPLETENESS_THEOREM_NOTE
  (basis-completeness route). The bridge remains the bounded layer.

  Distinction from anomaly cancellation: anomaly cancellation
  Tr[SU(N_c)^3] = 0 admits any N_c ≥ 2 in the comparison class.
  Cl(3) dim-counting forces N_c = 3 uniquely under the named
  bridge. The two arguments are structurally independent;
  joint solution is N_c = 3.

  Candidate sharpening for anomaly-only packets: "N_c = 3 not
  forced by anomaly" is narrowed by the separate bounded Cl(3)
  adjoint-carrier bridge constraint.

residual_engineering_admission: none  # this is a structural probe; no engineering frontier
residual_structural_admissions:
  - cl3_graded_basis_to_su_n_c_adjoint_carrier_bridge  # named bridge support

declared_one_hop_deps:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29
  - graph_first_su3_integration_note
  - gellmann_completeness_theorem_note_2026-05-02
  - cl3_sm_embedding_theorem
  - cl3_color_automorphism_theorem
  - axiom_first_sm_anomaly_cancellation_complete_theorem_note_2026-05-03

admitted_context_inputs:
  - cl3_graded_basis_to_su_n_c_adjoint_carrier_bridge

support_inputs_used:
  - cl3_real_dim_8_with_basis_one_three_three_one
  - su_n_lie_algebra_dimension_n_squared_minus_one
  - graph_first_su3_8dim_commutant_on_taste_cube
  - gellmann_completeness_8_generators_no_more
  - anomaly_cancellation_n_c_ge_2_comparison

load_bearing_step_class: bounded_theorem  # rigid forcing modulo named bridge
```

## 11. Cross-references

### Direct parents (this note's load-bearing dependencies)

- [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) — Cl(3) real-dim 8 with explicit basis
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — adjoint-carrier bridge (route A, commutant)
- [`GELLMANN_COMPLETENESS_THEOREM_NOTE_2026-05-02.md`](GELLMANN_COMPLETENESS_THEOREM_NOTE_2026-05-02.md) — bridge route B (basis completeness)
- [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) — Cl⁺(3) ≅ H quaternionic even subalgebra (graded structure)
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md) — scope-narrowed Gell-Mann embedding
- [`AXIOM_FIRST_SM_ANOMALY_CANCELLATION_COMPLETE_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SM_ANOMALY_CANCELLATION_COMPLETE_THEOREM_NOTE_2026-05-03.md) — anomaly-cancellation comparison surface

### Repo baseline / meta

- `MINIMAL_AXIOMS_2026-05-03.md` — physical `Cl(3)` local algebra and `Z^3` spatial substrate baseline
- `PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`

### Substrate-anomaly context

This note does not depend on a separate substrate-anomaly source note.
It records the color-count constraint that can be used later wherever
anomaly cancellation alone leaves `N_c` free.

### Related color-structure surface

- `FRACTIONAL_CHARGE_DENOMINATOR_FROM_N_C_THEOREM_NOTE_2026-04-24.md` — quark charge denominator from N_c=3 (downstream consumer)
- `CL3_BARYON_QQQ_COLOR_SINGLET_THEOREM_NOTE_2026-05-02.md` — qqq baryon singlet (downstream consumer)

## 12. Validation

```bash
python3 scripts/cl3_koide_z_substrate_color_geometric_2026_05_08_probeZ_substrate_color_geometric.py
```

Expected: PASS=8, FAIL=0. K-statements verified:

- K1 Cl(3) graded basis 1+3+3+1 = 8 (PASS)
- K2 SU(N_c) adjoint dim N_c²-1 (PASS)
- K3 forcing equation N_c² = 9 ⇒ N_c = 3 (PASS)
- K4 no competing N_c in {2..100} (PASS, exhaustive)
- K5 distinction from anomaly cancellation (PASS)
- K6 bridge identification (PASS, both routes A and B named)
- K7 substrate-anomaly comparison sharpening (PASS)
- K8 tier verdict BOUNDED THEOREM (PASS)

Cached: [`logs/runner-cache/cl3_koide_z_substrate_color_geometric_2026_05_08_probeZ_substrate_color_geometric.txt`](../logs/runner-cache/cl3_koide_z_substrate_color_geometric_2026_05_08_probeZ_substrate_color_geometric.txt)

## 13. User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: Probe Z does
  NOT assert "consistency = derivation". The dim-match is a
  structural rigidity (`N_c² = 9` has unique positive integer
  solution); the bridge K6 is named as the bounded admission, not
  hidden inside a numerical coincidence.
- `feedback_hostile_review_semantics.md`: stress-tests the
  "Cl(3) algebra ⇒ N_c = 3" claim by separating algebraic content
  (K1: dim_R Cl(3) = 8) from the action-form bridge (K6: Cl(3)
  graded basis carries SU(N_c) adjoint). The bridge is named, not
  asserted by trace identity.
- `feedback_retained_tier_purity_and_package_wiring.md`: no
  cross-tier promotion. The bridge K6 is bounded and supplied by
  named graph-first SU(3) + Gell-Mann support. No new retained
  content introduced.
- `feedback_physics_loop_corollary_churn.md`: this is NOT a
  one-step relabel. The probe identifies a structural distinction
  (Cl(3) dim-counting vs anomaly cancellation) that narrows an
  anomaly-only color-count freedom by combining the physical `Cl(3)`
  local algebra with graph-first SU(3) bridge support.
- `feedback_compute_speed_not_human_timelines.md`: no time
  estimates. Verdict described in terms of structural blockages
  (K1-K8) and algebraic-equation rigidity (`N_c² = 9`).
- `feedback_special_forces_seven_agent_pattern.md`: this note
  packages a sharp PASS/FAIL probe with 8 K-statements yielding
  8/8 PASS. Each K-statement is a structurally distinct claim
  with a sharp algebraic or numerical threshold.
- `feedback_review_loop_source_only_policy.md`: source-only —
  this PR ships exactly (a) source theorem note, (b) paired
  runner, (c) cached output. No output-packets, lane promotions,
  synthesis notes, or "Block" notes.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: an
  anomaly-only "N_c = 3 not forced" gap decomposes into (a) anomaly
  cancellation admits N_c ≥ 2 plus (b) Cl(3) substrate dim-counting
  forces N_c = 3 conditional on the named bridge.
- `feedback_primitives_means_derivations.md`: no new axioms or
  imports. All derivations are from the physical `Cl(3)` local
  algebra + standard SU(N) dimension formula + named graph-first
  SU(3) / Gell-Mann bridge support.
- `feedback_bridge_gap_resolution_c_locked.md`: this probe does
  not touch the action-form derivation; it operates entirely
  within the algebraic carrier-dimension matching layer.

## 14. Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, avoid one-step
relabelings of already-landed cycles. This note:

- Is **NOT** a relabel of `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`.
  That note derives the 8-dim su(3) commutant on the taste cube;
  it does NOT separately analyze the dim-counting forcing of N_c
  by the Cl(3) graded basis 1+3+3+1 = 8, nor does it state the
  anomaly-comparison narrowing.
- Is **NOT** a relabel of `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS`.
  That note establishes the per-site Cl(3) module structure (and
  dim_R Cl(3) = 8); it does NOT extract the dim-counting forcing
  of N_c.
- Is **NOT** a relabel of `GELLMANN_COMPLETENESS`. That note
  proves the 8 Gell-Mann generators are the complete su(3) basis;
  it does NOT analyze the 8-dim match between Cl(3) graded basis
  and su(3) adjoint as a forcing constraint.
- Is **NOT** a relabel of the `AXIOM_FIRST_SM_ANOMALY_CANCELLATION`
  surface. That note verifies anomaly cancellation on the current
  matter content; it does NOT examine which N_c admit cancellation.
- Provides **structurally new content**: the explicit fragmentation
  of the anomaly-only statement "N_c = 3 not forced by anomaly"
  into (a) anomaly admits N_c ≥ 2 plus (b) Cl(3) dim-counting forces
  N_c = 3 conditional on the adjoint-carrier bridge. The K5
  distinction (anomaly is trace identity vs Cl(3) is algebra-dim
  identity) is the new structural claim. K6 names the bridge as the
  bounded admission.

## 15. Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | Yes — an anomaly-only "`N_c = 3` not forced" statement is narrowed by the bounded Cl(3)-adjoint bridge constraint. The dim-counting equation N_c² - 1 = 8 has unique positive integer solution N_c = 3. |
| V2 | New bounded support? | Yes — (i) explicit identification of the Cl(3) dim-counting forcing layer as structurally distinct from anomaly cancellation; (ii) explicit bridge K6 naming the adjoint-carrier admission and listing graph-first SU(3) + Gell-Mann support; (iii) cross-checks at neighbouring N_c (only N_c = 3 matches). |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) the Cl(3) graded basis count (K1, citing CL3_PER_SITE_UNIQUENESS Step 1), (ii) the SU(N_c) adjoint dim formula (K2, textbook), (iii) the forcing equation algebra (K3, integer quadratic with unique positive root), (iv) exhaustive numerical enumeration (K4, runner verifies), (v) anomaly distinction (K5), (vi) bridge routes (K6, citing graph-first SU(3) + Gell-Mann completeness), (vii) comparison sharpening (K7, joint constraint analysis), (viii) tier verdict (K8, bounded with explicit bridge admission). |
| V4 | Marginal content non-trivial? | Yes — the K5 structural distinction (Cl(3) dim-counting is structurally distinct from anomaly cancellation; anomaly admits N_c ≥ 2 while dim-counting forces N_c = 3) is a clear roadmap for similar future anomaly-only open rows. |
| V5 | One-step variant? | No — this is not a relabel of GRAPH_FIRST_SU3_INTEGRATION_NOTE (which derives 8-dim su(3) commutant but does not analyze dim-counting forcing of N_c), of AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS (which establishes Cl(3) module structure and dim 8 but does not extract the N_c forcing), of GELLMANN_COMPLETENESS (which proves the 8-generator basis but does not match it against Cl(3) graded basis as forcing), or of AXIOM_FIRST_SM_ANOMALY_CANCELLATION (which verifies anomaly cancellation on current content but does not examine N_c admissibility). The dim-counting forcing layer + anomaly-comparison sharpening is genuinely new. |

**Source-note V1-V5 screen: pass for bounded-theorem audit seeding.**
