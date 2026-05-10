# N_F Trace-Space Bounded Obstruction Note (V_3 vs V Selection)

**Date:** 2026-05-07
**Claim type:** open_gate
**Status authority:** source-note proposal — audit verdict and downstream
status set only by the independent audit lane.
**Primary runner:** [`scripts/cl3_n_f_v3_trace_check_2026-05-07_w2binary.py`](../scripts/cl3_n_f_v3_trace_check_2026-05-07_w2binary.py)

## Claim

The prior W2 result
[`N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md`](N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md)
narrows the `N_F` admission in the `g_bare` chain from a continuous
positive scalar family to a binary set `{1/2, 1}`, corresponding to the
two natural trace surfaces:

- `Tr_{V_3}(T_a T_b) = (1/2) δ_{ab}` on the 3-dim irreducible color
  carrier `V_3`,
- `Tr_V(T_a^V T_b^V) = δ_{ab}` on the full 8-dim taste cube
  `V = C^8`.

The ratio is structurally fixed: `Tr_V / Tr_{V_3} = 2 = dim(V_fiber)`.

This note attempts to reduce that binary admission to `Tr_{V_3}` alone,
and **documents the structural bridge obstruction left open by the tested
Cl(3) + Z^3 routes**.

```text
Final N_F admission status:
   continuum scalar family   ->   binary {1/2, 1}   ->   ?  N_F = 1/2 ?
                              prior W2 reduction          present obstruction
```

The present note's review boundary: the tested routes do **not** close
the binary reduction to `N_F = 1/2` from Cl(3) + Z^3 primitives alone.
They become positive only *conditionally*, under a framework-level
identification (matter rep = V_3, irrep-trace convention, or per-site
Cl(3) identification). Each such identification is itself a non-trivial
framework structural claim, not a Cl(3) + Z^3 axiom-level identity.

## Eight attack vectors checked

The companion runner enumerates eight independent attack angles. Each
is verified numerically and given a structural status:

| Vector | Description | Status |
|---|---|---|
| V1 | Coupling structure (matter rep = V_3) | positive (under matter-rep identification) |
| V2 | Anomaly cancellation specific to V_3 | partial — rep-content not trace-surface |
| V3 | Cl(3) automorphism on V_3 (irreducible carrier) | positive (under irrep-trace convention) |
| V4 | HS projection: T_a^V vanishes off V_color | partial — reduces V to V_color, not V_3 |
| V5 | Anti-fundamental: V doesn't carry 3-bar | positive (under matter-coupling structure) |
| V6 | Holonomy: Wilson loop on V_3 = matter character | positive (under standard QCD convention) |
| V7 | Substrate Z^3 dim = N_c = 3 | positive (color/weak structural split) |
| V8 | Cl(3) bivector at SU(2) level (1/2 forced) | partial — bridge to SU(3) sub-level non-trivial |

**Six positives, two partials.** The strongest joint argument is
**V3 + V5 + V8**: SU(3) on irreducible V_3, V doesn't carry 3-bar, and
Cl(3) bivectors force SU(2) normalization 1/2.

This joint argument is *suggestive but not unconditional* — see the
obstruction below.

## Structural obstruction at the bridge

The strongest attack path (V8) factors as:

```
Cl(3) bivectors at per-site            (axiom A1)
   |
   |  Spin(3) -> SO(3) double cover
   v
T_k = sigma_k/2 on per-site C^2     (Tr = 1/2 forced)
   |
   |  ?  bridge identification
   v
SU(2) sub of color-SU(3) on V_3 has Tr = 1/2          (V8 conclusion)
   |
   |  Killing rigidity (one Ad-invariant form on simple su(3) up to scalar)
   v
SU(3) on V_3 has Tr_{V_3}(T_a T_b) = (1/2) delta_ab     (N_F = 1/2 on V_3)
```

The bridge step is: **"the SU(2) sub of color-SU(3) on V_3 IS the
per-site Cl(3) bivector SU(2)."**

This identification is **not** derivable from Cl(3) + Z^3 primitives:

1. **Per-site Cl(3) bivectors** live on per-site Hilbert space `C^2`
   (per
   [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)).
2. **The color SU(3)** lives on the 8-dim taste cube `V = C^8`, a
   tensor / multi-mode structure built from many sites and / or
   internal degrees of freedom (per
   [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)).
3. **The SU(2) sub of color-SU(3)** acts on the (1,2)-block of V_3 — a
   2-dim subspace of V, not the per-site C^2.

The two `C^2`'s — per-site and the (1,2)-block of V_3 — are both 2-dim
faithful SU(2) reps and hence **algebraically isomorphic**, but they
live on different parts of the framework's Hilbert space hierarchy.
Identifying them as the same SU(2) requires an additional structural
claim that is not derived from Cl(3) + Z^3 primitives alone.

## Verification (29/0 PASS)

```bash
python3 scripts/cl3_n_f_v3_trace_check_2026-05-07_w2binary.py
```

Verifies the load-bearing structural facts:

- `Tr_{V_3}(T_a T_b) = (1/2) δ_{ab}` (canonical Gell-Mann on V_3).
- `Tr_V(T_a^V T_b^V) = δ_{ab}` (full taste cube V).
- Ratio `Tr_V / Tr_{V_3} = 2` (fiber multiplicity exactly).
- `T_a^V . P_lepton = 0` (gauge generators kill V_lepton).
- `T_a^V` acts as `T_a ⊗ I_2` on `V_color` (verified).
- 3-bar generators `-T_a^*` differ from 3 generators `T_a`
  (V_3 is not self-dual; SU(3) is complex).
- `Tr_{V_color}` decomposes under SU(3)_c as `2 . Tr_{V_3}`
  (factor 2 = fiber multiplicity).
- d-symbols on V are `2 . d`-symbols on V_3 (factor 2 inflation).
- Cl(3) bivector half-Pauli `T_k = σ_k/2` has
  `Tr_{C^2}(T_a T_b) = (1/2) δ_{ab}` (forced by Spin(3) double cover).
- SU(2) sub of SU(3) on V_3 has `Tr = (1/2) δ_{ab}` (matches bivector).
- SU(2) sub of SU(3) on V_color has `Tr = δ_{ab}` (factor 2 off —
  incompatible with bivector 1/2).

Expected runner output:

```text
EXACT   : PASS = 29, FAIL = 0
BOUNDED : PASS = 0, FAIL = 0
TOTAL   : PASS = 29, FAIL = 0
```

## What this note DOES establish

1. **Exhaustive attack enumeration.** Eight independent structural
   angles, each verified numerically. None unconditionally forces V_3
   from Cl(3) + Z^3 primitives.

2. **Localization of the obstruction.** The bridge "per-site Cl(3)
   bivector SU(2) = SU(2) sub of color-SU(3) on V_3" is the
   load-bearing weak point. Closing it would lift V8 from partial to
   positive and (combined with V3 + V5) yield V_3 selection.

3. **Conditional V_3 selection chain.** Under any one of:
   - the framework matter-rep identification (matter = V_3 via
     `CL3_COLOR_AUTOMORPHISM` + per-site dim 2 + the open staggered-
     Dirac realization gate),
   - the irrep-trace convention (trace on irreducible carrier, not on
     multiplicity inflation),
   - the per-site / lattice SU(2) identification (per-site Cl(3)
     bivector SU(2) = SU(2) sub of color-SU(3)),

  `N_F = 1/2` follows. This note leaves each of these identifications
   as an open structural bridge rather than treating it as derived from
   Cl(3) + Z^3 primitives alone.

4. **Cleanest reading.** The V_3 vs V trace-surface admission is a
   *convention* at the same conceptual level as the prior overall-
   scalar `N_F` admission. Both are framework normalization choices
   that the literature conventionally makes; neither is forced by
   Cl(3) + Z^3 primitives.

## What this note does NOT establish

- It does not close `N_F = 1/2` from Cl(3) + Z^3 primitives.
- It does not lift the binary admission to a unique value.
- It does not change the prior W2 row's effective status.
- It does not change the parent
  [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  four-layer stratification: L3 remains the single admitted
  convention, just now with a more detailed structural analysis of
  *what* the L3 admission actually consists of (a trace-surface choice
  V_3 vs V, plus an overall scalar within the chosen surface).

## Implications for the parent stratification

Under the four-layer stratification of the parent constraint-vs-
convention note, the L3 admission is the overall scalar `N_F`. The
present note adds detail to L3:

- **L3a.** Trace-surface admission: V_3 vs V (this note's binary).
- **L3b.** Overall scalar within chosen surface: 1/2 (canonical
  Gell-Mann), 1 (full V trace), or any other positive scalar. This is
  the original L3 admission.

The structural facts:

- **L3a** is a *binary* admission per the prior W2 note, NOT a
  continuous family.
- **L3b** is a *continuous* family, narrowed by Killing rigidity to
  "up to scalar."

Both layers are framework-conventional. The present note documents
that **neither layer can be derived from Cl(3) + Z^3 primitives**.

## Sister-strengthening direction

A future closure of `N_F = 1/2` from Cl(3) + Z^3 primitives must
strengthen **the bridge step in V8** — specifically, derive the
per-site Cl(3) bivector / SU(2)-sub-of-color-SU(3) identification as
a positive theorem.

The closest existing structural inputs are:

- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md):
  SU(3)_c on V_3 + commutativity with SU(2)_weak.
- [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md):
  per-site `C^2` is the Cl(3) irrep with bivector half-Pauli SU(2).

Bridging these two upstream results to a single positive theorem
identifying their SU(2)'s would be the natural closure path. That is
itself a Nature-grade target.

Adding more instances of attack types V1-V7 (which all import
similar identifications at different layers) would NOT close the
problem — it would only add redundant conditional conclusions. The
load-bearing bridge step is the per-site / lattice identification,
and that is what must be derived.

## Honest scope (audit-readable)

```yaml
target_claim_type: open_gate
proposed_claim_scope: |
  The binary trace-surface admission N_F in {1/2, 1} from the prior W2
  reduction (V_3 vs V trace) is not reduced to N_F = 1/2 by the tested
  Cl(3) + Z^3 routes. Eight independent attack vectors are enumerated;
  six give positive V_3 selection conditional on
  framework-level identifications, and two give partial reductions.
  The load-bearing bridge step (per-site Cl(3) bivector SU(2) =
  SU(2) sub of color-SU(3) on V_3) is structurally non-trivial and
  not derivable from Cl(3) + Z^3 primitives.
proposed_load_bearing_step_class: A (algebraic identification + numerical verification)
declared_one_hop_deps:
  - n_f_bounded_z2_reduction_theorem_note_2026-05-07_w2
  - cl3_color_automorphism_theorem
  - cl3_per_site_hilbert_dim_two_theorem_note_2026-05-02
  - g_bare_hilbert_schmidt_rigidity_theorem_note_2026-05-07
  - g_bare_constraint_vs_convention_restatement_note_2026-05-07
independent_audit_required_before_effective_status_change: true
parent_update_allowed_only_after_independent_audit_accepts_child_rows: true
distinguishing_content_from_prior_W2_note: |
  The prior W2 note narrows N_F admission from continuous to binary
  {1/2, 1}.  The present note attempts (and documents the failure of)
  the further narrowing to N_F = 1/2.  It enumerates eight attack
  vectors, identifies the structural obstruction at the per-site /
  lattice bridge step (V8), and classifies the residual binary as a
  trace-surface convention rather than a derivable identity.
```

## Cross-references

- [`N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md`](N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md)
  — the prior W2 result this note attempts to close.
- [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  — parent four-layer stratification; the present note adds
  L3a/L3b detail.
- [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
  — joint Tr-and-Casimir rigidity (overall scalar admission).
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  — SU(3) on the symmetric base V_3 + commutativity with SU(2)_weak.
- [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)
  — per-site Hilbert space C^2 (Cl(3) irrep).
- [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
  — C_F = 4/3 on V_3 in canonical Gell-Mann normalization (uses N_F = 1/2).
- [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
  — Cl(3) → End(V) → su(3) embedding canonicity.
- `MINIMAL_AXIOMS_2026-05-03.md`
  — current framework axioms A1 (Cl(3)) + A2 (Z^3).

## Bounded-result honest summary

The attempt to close `N_F = 1/2` from Cl(3) + Z^3 primitives via the
V_3 trace-surface selection produces a **structural obstruction**: the
binary admission `{1/2, 1}` cannot be reduced under the primitives
alone. The reduction is conditional on framework-level identifications
(matter rep, irrep-trace convention, or per-site / lattice SU(2)
identification) — each of which is non-trivial structural content, not
an axiom-level identity.

The cleanest reading is that the V_3 vs V choice is a **trace-surface
convention** at the same conceptual level as the overall-scalar
convention. Both are framework normalization choices, and the deeper
convention-vs-derivation status of each remains open.

This note is the honest scope on the V_3 selection problem: a clean
obstruction, with the load-bearing bridge step explicitly identified
and the closure path through that bridge mapped for future work.
