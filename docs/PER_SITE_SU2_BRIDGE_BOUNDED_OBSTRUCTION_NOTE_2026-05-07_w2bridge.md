# Per-Site SU(2) ↔ Color-SU(3) (1,2)-Block SU(2) Bridge — Bounded Characterization

**Date:** 2026-05-07
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Primary runner:** [`scripts/cl3_per_site_su2_bridge_check_2026_05_07_w2bridge.py`](../scripts/cl3_per_site_su2_bridge_check_2026_05_07_w2bridge.py)

## Authority disclaimer

This note is graph-visible and queued for the independent audit lane.
It does not set or predict an audit outcome; the effective status is
pipeline-derived after the audit lane reviews the claim and dependency
chain. The bounded classification reflects the structural barrier
documented below; closure to a positive theorem would require lifting
the L3a admission (the `V_3` trace surface) to a derived consequence
of `A1 + A2`.

## Claim

Let `V = (C²)^{⊗3} = C^8` be the framework's 3-site taste cube, with
per-site `C²` the Cl(3) Pauli irrep
([`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md))
and `V_3 ⊂ V` the 3-dim symmetric-base subspace
([`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)).
Let:

- `T_a^{site_j}` = per-site Cl(3) bivector SU(2) generator at site `j`
  (acting as `σ_a/2` on tensor factor `j`, identity elsewhere);
- `T_a^{color}` = SU(2) sub of color-SU(3) on the `(1,2)`-block of
  `V_3`, embedded in `V` as `M_3_sym ⊗ I_2 + 0_antisym`.

**Theorem (W2.bridge, bounded sharpening of W2.binary V8).**

**(B1) Operator inequivalence.** `T_a^{site_j}` and `T_a^{color}` are
NOT unitarily equivalent operators on `V`. The eigenvalue spectra of
`T_3^{site_j}` and `T_3^{color}` differ in multiplicity counts:

```text
spec(T_3^{site_j}|_V)  =  {±1/2 with mult 4}                    (per-site)
spec(T_3^{color}|_V)   =  {±1/2 with mult 2, 0 with mult 4}     (color sub)
```

**(B2) Algebraic equivalence.** As ABSTRACT su(2) Lie algebras with
their canonical 2-dim faithful irreducible reps, `T_a^{site_j}` and
`T_a^{color}` ARE equivalent. Both have:
- generators of the form `σ_a / 2`;
- Killing form `(1/2) δ_{ab}` on the 2-dim fundamental;
- Casimir `3/4` on the 2-dim fundamental.

**(B3) Bridge admission L3b reduces to L3a.** The non-trivial
identification of `T_a^{site_j}` with `T_a^{color}` requires admitting
that the framework's gauge-action trace surface is the irreducible
color carrier `V_3` (the L3a admission per
[`N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md`](N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md)).
Under L3a:
- `Tr_{V_3}(T_a^{color} T_b^{color}) = (1/2) δ_{ab}`,
- `Tr_{C²}(T_a^{site_j} T_b^{site_j}) = (1/2) δ_{ab}`,
- The two SU(2)'s have the SAME normalization on their 2-dim
  fundamentals.

Without L3a (e.g., on `V` trace surface), the normalizations differ:
- `Tr_V(T_a^{color} T_b^{color}) = δ_{ab}` (factor 2 fiber inflation);
- `Tr_{C²}(T_a^{site_j} T_b^{site_j}) = (1/2) δ_{ab}` (per-site).

Thus the checked bridge introduces no independent normalization scalar
separate from L3a. The remaining foundational issue is still the L3a
trace-surface admission itself.

**(B4) Net effect on g_bare chain admissions.** The framework's `g_bare`
chain (per the four-layer stratification of
[`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md))
has no second L3 bridge scalar exhibited by this check beyond the L3a
trace-surface choice. The W2.binary V8 result raised the question of a
potential separate admission L3b; this work narrows that question to
the already named L3a surface.

## Boundaries

This note does not claim:

- a derivation of `N_F = 1/2` from `A1 + A2` alone (the L3a admission
  remains the single open foundational question);
- a closure of the V_3 selection problem (V_3 vs V trace surface);
- a parent status update for `G_BARE_DERIVATION_NOTE.md`;
- a lift of any bounded-theorem row to audit-retained grade.

What it DOES establish:

- The checked bridge admission L3b reduces to the L3a trace-surface
  admission.
- The runner does not exhibit a second L3 bridge scalar beyond L3a.
- The two SU(2)'s are operator-inequivalent on V but algebraically
  equivalent as Lie-algebra reps.

## Why the seven attack vectors do not provide unconditional closure

The 7 attack angles enumerated in the W2.bridge task were evaluated:

| Vector | Status | Residual barrier |
|---|---|---|
| V1: Substrate-locality | PARTIAL | V_3 built from per-site C²'s, but bridge requires L3a |
| V2: Anomaly cancellation | OBSTRUCTION | Anomaly cancellation is matter-content dependent |
| V3: Cl(3)⊗Cl(3) → Spin(6) | PARTIAL | Spin(6) embedding lives within L3a, doesn't derive it |
| V4: Operational Wilson loops | OBSTRUCTION | Wilson observables differ by factor 2 (fiber mult) |
| V5_NEW: Z³ rotation invariance | PARTIAL | Color SU(2) sub corresponds to S_3-symmetric E-component combination of per-site SU(2)'s; distinguishes but doesn't identify |
| V6: Spin(3) double cover | OBSTRUCTION | Per-site C² (spinor) vs V_3 (vector) are different reps |
| V7: HS projection π: V → V_3 | OBSTRUCTION | π IS the L3a admission |

**Three partials reduce to L3a; four obstructions are structural barriers.**

The new structural finding is V5_NEW: Z³ point-group symmetry
`O_h(3) = S_3 ⋉ (Z_2)^3` distinguishes the color SU(2) sub
(`S_3`-invariant `E`-component within `V_3`) from individual per-site
SU(2)'s (`S_3`-orbit of length 3). The color SU(2) sub corresponds to
the `S_3`-symmetric `E`-projection combination of per-site SU(2)'s.
This sharpens the structural picture but does not provide independent
closure.

## Dependencies (one-hop)

| Authority | Current audit-lane status | Role |
|---|---|---|
| [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md) | unaudited | provides the four-layer L1-L4 stratification |
| [`N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md`](N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md) | unaudited | provides the L3a binary trace-surface admission |
| [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md) | unaudited | provides Killing-rigidity (R1)–(R5) |
| [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md) | retained_bounded | provides the `V_3 ⊂ V` symmetric-base / SU(3) embedding |
| [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md) | unaudited | provides per-site `C²` (Pauli irrep) |
| [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) | audited_conditional | provides Cl(3) per-site uniqueness up to chirality |
| [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md) | audited_conditional | provides `V = (C²)^{⊗3} = C^8` taste cube structure |
| `MINIMAL_AXIOMS_2026-05-03.md` | meta | identifies the current A1/A2 axiom context |

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews the claim and
dependency chain.

## Verification

Run:

```bash
python3 scripts/cl3_per_site_su2_bridge_check_2026_05_07_w2bridge.py
```

Expected:

```text
EXACT      : PASS = 52, FAIL = 0
STRUCTURAL : PASS = 4, FAIL = 0
TOTAL      : PASS = 56, FAIL = 0
```

The runner verifies (in 7 sections):

- **Section 0:** Per-site SU(2) and color SU(2) sub Hermiticity, su(2)
  algebra `[T_1, T_2] = i T_3`, Killing form `(1/2) δ_{ab}` on
  fundamental.
- **Section 1:** Per-site SU(2)'s at sites 0, 1, 2 are tensor-local
  (factor through one site each), pairwise commuting on V.
- **Section 2:** Color SU(2) sub on V_3's (1,2)-block has T_3 spectrum
  `{±1/2 mult 2, 0 mult 4}`; per-site SU(2) has `{±1/2 mult 4}`.
  Spectra DIFFER, so the two are not unitarily equivalent on V.
- **Section 3:** (1,2)-block of color T_a on V_3 IS canonical `σ_a/2`,
  matching per-site `σ_a/2` (algebraic equivalence under L3a).
- **Section 4:** 7 attack vectors evaluated; bridge L3b reduces to L3a.
- **Section 5:** Both SU(2)'s have SAME Killing form `(1/2) δ_{ab}` on
  their respective 2-dim fundamentals (algebraic equivalence).
- **Section 6:** g_bare chain admission count: 1 (L3a only).
- **Section 7:** Sharpening of W2.binary V8 documented.

## Honest scoping

This note SHARPENS the W2.binary V8 PARTIAL result. What it
establishes:

1. **Operator inequivalence (B1).** Per-site SU(2) and color SU(2) sub
   are not unitarily equivalent operators on V (different T_3 spectra).
2. **Algebraic equivalence (B2).** They are algebraically equivalent
   as abstract Lie-algebra reps (Killing rigidity + matching
   normalization).
3. **L3b reduces to L3a (B3).** The checked bridge identification
   reduces to the L3a trace-surface admission.
4. **No second L3 bridge scalar is exhibited (B4).** Net structural
   tightening of the W2.binary open-gate boundary.

This note **does not** close:

- the V_3 selection problem (L3a remains a framework-level admission);
- the `N_F = 1/2` derivation from `A1 + A2`;
- the parent `G_BARE_DERIVATION_NOTE.md` repair targets beyond this
  bridge characterization.

The framework's path forward for closing the residual L3a admission is
the same as identified in W2.binary: requires either matter-rep
identification (matter = V_3), irrep-trace convention (trace on
irreducible carrier), or per-site / lattice Wilson-loop convention.
None is a Cl(3) + Z³ primitive.

## Reading rule

This note is the claim boundary for the W2.bridge attack on the V8
sub-problem of the W2.binary open-gate result. It SHARPENS
the W2.binary obstruction by reducing the apparent two-admission
structure (L3a trace surface + L3b bridge identification) to a
single-admission structure (L3a only).

It does NOT promote the bounded classification of the upstream
N_F / g_bare chain to retained. The L3a trace-surface admission
remains the load-bearing weak point in the framework's normalization
chain.

```yaml
claim_type_author_hint: bounded_theorem
claim_scope: |
  The bridge admission L3b (per-site Cl(3) bivector SU(2) ↔ color-SU(3)
  (1,2)-block SU(2) on V_3) reduces to the L3a trace-surface admission
  (V_3 vs V choice). The two SU(2)'s are operator-inequivalent on V but
  algebraically equivalent as Lie-algebra reps; the identification is
  reduced by L3a + Killing rigidity + matching normalization. This
  check does not exhibit a second L3 bridge scalar beyond L3a.
proposed_load_bearing_step_class: A
upstream_dependencies:
  - g_bare_constraint_vs_convention_restatement_note_2026-05-07
  - n_f_bounded_z2_reduction_theorem_note_2026-05-07_w2
  - g_bare_hilbert_schmidt_rigidity_theorem_note_2026-05-07
  - cl3_color_automorphism_theorem
  - cl3_per_site_hilbert_dim_two_theorem_note_2026-05-02
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29
  - cl3_taste_generation_theorem
  - minimal_axioms_2026-05-03
admitted_context_inputs:
  - L3a_v3_trace_surface_admission
independent_audit_required_before_effective_status_change: true
```

## Cross-references

- [`N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md`](N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md)
  — prior W2 reduction this work sharpens.
- [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  — four-layer stratification with L3a as the admitted-convention layer.
- [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
  — Hilbert-Schmidt + Casimir rigidity (joint).
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  — SU(3) on `V_3` (3D symmetric base subspace of V).
- [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md)
  — `V = (C²)^⊗3 = C^8` taste cube; 3-site tensor product structure.
- [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)
  — per-site `H_x = C²` (Pauli irrep).
- [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md)
  — Cl(3) per-site uniqueness theorem.
- `MINIMAL_AXIOMS_2026-05-03.md`
  — current framework axioms (A1: Cl(3), A2: Z³).

Related non-load-bearing context: the older g_bare structural
normalization note, the Hamiltonian-level g_bare rigidity note, and the
SU(3) fundamental-Casimir note.

## Citation references (representation theory)

- Slansky, R. *Group Theory for Unified Model Building*, Phys. Rep. 79
  (1981) 1-128 — SU(3) Gell-Mann embedding and matrix-rep canonical
  normalization.
- Greiner, W. & Müller, B. *Quantum Mechanics: Symmetries* (Springer,
  1994) — SU(2) double cover (Spin(3) → SO(3)) and per-site `σ_a/2`
  conventions.
- Howe, R. & Tan, E.-C. *Non-Abelian Harmonic Analysis: Applications of
  SL(2,R)* (Springer, 1992) — Schur lemma and Wedderburn theorem
  applied to faithful 2-dim irreducible reps of su(2).
- Cvitanović, P. *Group Theory: Birdtracks, Lie's, and Exceptional
  Groups* (Princeton, 2008) — birdtrack treatment of canonical
  normalization conventions for SU(N) and Spin(N).
- Lawson, H. B. & Michelsohn, M.-L. *Spin Geometry* (Princeton, 1989)
  — Cl(3) ⊗ Cl(3) ≅ Cl(6) ≅ Spin(6) decomposition (V3 attack).
