# sin²θ_W^GUT = 3/8 from SU(5) Embedding + LHCM-Derived Tr[Y²]

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on retained
graph-first surface + cycle 16 (Tr[Y²] = 40/3 + SU(5) GUT consistency) +
admitted SU(5) gauge-group embedding. NOT proposed_retained — see
CLAIM_STATUS_CERTIFICATE.md.
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

- The SU(5) unification itself (admitted GUT structure)
- The running of sin²θ_W from GUT scale to M_Z (requires RG running,
  not derived here)
- The GUT scale itself (~10^16 GeV is observational/external input)
- The retention of cycle 16 (still depends on Convention A vs B
  reclassification + admitted SU(5) embedding)

## 6. Status

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on cycle 16 (Tr[Y²] = 10/3 / 40/3) and admitted SU(5)
  gauge-group embedding. SU(5) embedding is a standard GUT structure
  not derivable from the graph-first framework alone.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7. Cross-references

- Cycle 16 / PR [#279](https://github.com/jonathonreilly/cl3-lattice-framework/pull/279) — [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md)
- Cycles 1-3 LHCM closure — [`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md)
- Cycle 6 / PR #262 — [`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md)
- Standard references: Georgi-Glashow SU(5) (1974); Buras-Ellis-Gaillard-Nanopoulos (1978); PDG GUT review.
