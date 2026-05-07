# sin²θ_W^GUT = 3/8 from SU(5) Embedding + LHCM-Derived Tr[Y²]

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem conditional on the
graph-first surface + cycle 16 (Tr[Y²] = 40/3 + SU(5) GUT consistency) +
the SU(5) embedding input. This note is not a retained-status authority;
independent audit owns effective status.
**Primary runner:** `scripts/frontier_sin2_theta_w_gut_from_su5.py`
**Authority role:** exact-support theorem deriving the GUT-scale Weinberg
angle prediction from cycle 16's SU(5) consistency.

## 0. Statement

**Theorem (sin²θ_W^GUT = 3/8 from SU(5) embedding).**

Given:
1. LHCM-derived hypercharges from
   [`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md)
   (cycles 1-3, modulo SM-definition convention);
2. [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md)
   (cycle 16, PR #279) result: in Convention B,
   `Tr[Y²]_per-Weyl-family = 10/3` over the SU(5) 5̄ ⊕ 10 representation;
3. SU(5) gauge-group embedding admission: at the GUT scale, all three SM
   gauge couplings unify (`g_3 = g_2 = g_1` in GUT normalization);
4. SU(5) hypercharge normalization: `Y_GUT = √(3/5) · Y_SM`
   (cycle 16 PR #279);

then the Weinberg angle at the GUT scale is uniquely:

```text
sin²θ_W^GUT  =  3/8.
```

**Proof.** The Weinberg angle is defined by `tan²θ_W = g'² / g_2²` where
`g'` is the U(1)_Y coupling and `g_2` is the SU(2)_L coupling.

In the GUT normalization, the U(1) coupling becomes
`g'_GUT = √(3/5) · g'_SM` (because Y_GUT = √(3/5) Y_SM).

At the GUT scale `g_3 = g_2 = g_1_GUT = g_1` (SU(5) unification). So
`g'_GUT² = g'²·(3/5)`. The relationship between g' and g_1_GUT is:

```text
g'²  =  g_1_GUT² · (3/5)
     =  g_2² · (3/5)            at GUT scale (g_2 = g_1_GUT)
```

Therefore at the GUT scale:

```text
tan²θ_W^GUT  =  g'² / g_2²  =  3/5.
```

Then:

```text
sin²θ_W^GUT  =  tan²θ_W^GUT / (1 + tan²θ_W^GUT)
             =  (3/5) / (1 + 3/5)
             =  (3/5) / (8/5)
             =  3/8.   ∎
```

## 1. Equivalent forms

```text
sin²θ_W^GUT  =  3/8  =  0.375
cos²θ_W^GUT  =  5/8  =  0.625
tan²θ_W^GUT  =  3/5  =  0.6
```

## 2. Comparison with experiment

The PDG-measured value `sin²θ_W(M_Z) ≈ 0.231` is **substantially less**
than `3/8 = 0.375`. This is **not** a contradiction: the GUT prediction
applies at the unification scale (~10^16 GeV), and renormalization-group
running brings sin²θ_W down to its measured value at M_Z ~ 91 GeV. The
running flow is well-known.

This note does **not** compute the running; it derives the GUT-scale
boundary condition `sin²θ_W^GUT = 3/8`.

## 3. Retained / admitted inputs

| Ingredient | Class | Source |
|---|---|---|
| LHCM-derived Y values | exact-support (cycles 1-3) | [`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md) |
| Tr[Y²] = 10/3 per Weyl family (Convention B) | exact-support (cycle 16) | [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md) |
| Y_GUT = √(3/5) · Y_SM | admitted SU(5) GUT normalization | standard SU(5) embedding |
| SU(5) unification at GUT scale | admitted SU(5) GUT structure | standard GUT |

## 4. What this closes

- **sin²θ_W^GUT = 3/8** as exact algebraic identity at the GUT scale,
  derived from LHCM hypercharges + cycle 16 + SU(5) embedding admission.
- **Equivalent forms** cos²θ_W = 5/8, tan²θ_W = 3/5 at GUT scale.

## 5. What this does NOT close

- **(coupling unification)** The SU(5) unification at GUT scale —
  `g_3 = g_2 = g_1` is an admitted physical assumption about RG running.
- **(GUT-group choice)** The choice of SU(5) (vs. SO(10), E6, ...) as the
  GUT group. The matter content also fits 16 of SO(10) and so on; this
  note does not derive *which* simple group containing
  `su(3) ⊕ su(2) ⊕ u(1)` is the correct GUT group. (See 5a.)
- The running of sin²θ_W from GUT scale to M_Z (requires RG running,
  not derived here)
- The GUT scale itself (~10^16 GeV is observational/external input)
- The retention of cycle 16 (still depends on Convention A vs B
  reclassification)

## 5a. SU(5) embedding admission status (2026-05-07 update)

The §3 admitted inputs (3) "SU(5) GUT-group embedding" and (4)
"`Y_GUT = √(3/5) · Y_SM` normalization" are addressed by the
bounded-theorem follow-on
[`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md).
That note derives:

- **Embedding consistency.** All 16 LH-form chiralities per generation map
  to unique `5̄ ⊕ 10 ⊕ 1` slots, with the hypercharge generator
  `T_24 ∝ diag(−2,−2,−2,+3,+3)` forced by Schur's lemma on the
  `su(3) ⊕ su(2)` block embedding.
- **Y_GUT normalization.** `Y_GUT = √(3/5) · Y_min` is trace-forced from
  `Tr[Y_GUT²]_5̄+10 = Tr[T_a²]_5̄+10 = 2` per Weyl family, under the
  standard SU(5) Killing-form normalization convention
  `Tr[T_a T_b]_5 = (1/2) δ_{ab}`.

After that note is independently audited, the §3 admissions (3)
and (4) move to derived-dependency status. The two **residual physical
admissions** at this note's surface are then:

- **(5)** SU(5) unification at GUT scale (`g_3 = g_2 = g_1`) — coupling
  unification physical assumption, not representation theory.
- **(6)** Choice of SU(5) (vs. SO(10), E6) as the GUT group — embedding
  *consistency* is derived; embedding *minimality* is not. Same matter
  content fits 16 of SO(10).

This subsection does not change the present note's claim status; it
records the cross-reference for the audit graph and signals the
load-bearing relationship to the embedding-consistency note.

## 6. Status

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on cycle 16 (Tr[Y²] = 10/3 / 40/3). The §3 admitted SU(5)
  embedding + Y_GUT normalization items are now derived by
  SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md
  (bounded_theorem, unaudited) under the SU(5) Killing-form normalization
  convention. Two residual physical
  admissions remain: (5) g_3 = g_2 = g_1 at GUT scale; (6) choice of
  SU(5) vs SO(10)/E6 as the GUT group. Both are physical / external
  choices, not representation theory.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7. Cross-references

- Cycle 16 / PR [#279](https://github.com/jonathonreilly/cl3-lattice-framework/pull/279) — [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md)
- Cycles 1-3 LHCM closure — [`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md)
- Cycle 6 / PR #262 — [`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md)
- Embedding-consistency derivation: [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) (bounded_theorem, unaudited)
- Standard references: Georgi-Glashow SU(5) (1974); Buras-Ellis-Gaillard-Nanopoulos (1978); PDG GUT review.
