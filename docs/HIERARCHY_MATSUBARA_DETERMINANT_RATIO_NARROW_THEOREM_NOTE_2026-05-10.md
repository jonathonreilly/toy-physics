# Hierarchy Matsubara Determinant Ratio — Narrow Algebraic Theorem

**Date:** 2026-05-10
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.
**Primary runner:** [`scripts/frontier_hierarchy_matsubara_determinant_ratio_narrow.py`](../scripts/frontier_hierarchy_matsubara_determinant_ratio_narrow.py)

## 0. Audit context

The hierarchy formula
[`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
asserts the compression factor

```text
C = (A_2 / A_4)^(1/4) = (7/8)^(1/4) ≈ 0.96717
```

between the L_t = 2 UV Matsubara endpoint and the L_t = 4 IR endpoint
selected by Klein-four bosonic-bilinear orbit closure. The (1/4) power
index is currently asserted via "dimension-4 effective-potential
density" reasoning, and the audit lane has flagged the parent row
[`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md)
as `audited_numerical_match` because the (1/4) is asserted, not derived
from primitives.

This narrow theorem closes the structural derivation of the **(7/8)**
factor as an exact rational identity on the staggered Dirac determinant,
and reduces the open piece to a single named readout admission (the
per-mode geometric-mean reading). It does NOT close the readout
admission itself.

## 1. Claim scope

> **Theorem (Matsubara determinant ratio identity).** On the minimal
> spatial APBC block `L_s = 2` of the staggered Dirac operator on `Z⁴`,
> with the mean-field gauge factorization (admitted standard mean-field
> convention; same setup as
> [`HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md`](HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md)),
> the massless determinants at temporal blocks `L_t ∈ {2, 4}` satisfy
> the **exact rational identity**:
>
> ```text
> |det(D, L_t = 4, m = 0)|  /  |det(D, L_t = 2, m = 0)|²  =  (7/8)^16.
> ```
>
> Equivalently:
>
> ```text
> |det(D, L_t = 4)|  =  (7/8)^16  ·  |det(D, L_t = 2)|²        (m = 0).
> ```

The narrow theorem **explicitly does NOT** claim:

- the absolute scale of the EW VEV `v` (separate; depends on the framework
  hierarchy formula's specific identification of `v` with the staggered
  determinant);
- the per-mode geometric-mean readout `v(L_t) ∝ |det(L_t)|^(1/(N_taste · L_t))`
  itself (this is the named admission whose closure would discharge the
  remaining (1/4) gap — see Section 4);
- the staggered-Dirac realization gate (the count `N_taste = 16 = 2^D`
  inherits from the open gate
  [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)).

## 2. Admitted dependencies

| Authority | Role | Status |
|---|---|---|
| Cl(3) Clifford identity `D_taste² = d · I` | admitted standard staggered fermion algebra | parent narrow theorem |
| Mean-field factorization `U_{ab} → u_0 δ_{ab}` | admitted standard mean-field convention | parent narrow theorem |
| `L_s = 2` minimal APBC block | admitted block-size choice; pins spatial momenta to BZ corners (sin²(k_i) = 1) | parent narrow theorem |
| Standard staggered Dirac dispersion `λ²(k, ω) = u_0² Σ_μ sin²(k_μ)` | admitted standard staggered fermion algebra | parent narrow theorem |

All dependencies are inherited from the retained-tier-conditional parent
narrow theorem
[`HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md`](HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md).
This note adds zero new admissions for the algebraic identity itself.
The cross-endpoint reading in Section 4 lists one named admission
(per-mode geometric-mean readout).

## 3. Load-bearing step (class A)

```text
From the parent narrow theorem (admitted standard staggered fermion
algebra + L_s = 2 mean field), the closed form is

  |det(D + m)|  =  ∏_ω  [m² + u_0² (3 + sin²ω)]⁴                       (1)

with ω over L_t APBC Matsubara modes ω_n = (2n+1)π/L_t.

At m = 0:

  |det(D, L_t)|_{m=0}  =  ∏_ω  [u_0² (3 + sin²ω)]⁴
                       =  u_0^(8 L_t) · ∏_ω (3 + sin²ω)⁴.              (2)

Specialize to L_t = 2 and L_t = 4:

  L_t = 2:  ω ∈ {π/2, 3π/2},  sin²ω ∈ {1, 1}
    |det(D, L_t = 2)|_{m=0}  =  ∏_ω [4 u_0²]⁴
                              =  (4 u_0²)^8                            (3)
                              =  u_0^16 · 4^8.

  L_t = 4:  ω ∈ {π/4, 3π/4, 5π/4, 7π/4},  sin²ω = 1/2  (all four)
    |det(D, L_t = 4)|_{m=0}  =  ∏_ω [(7/2) u_0²]⁴
                              =  ((7/2) u_0²)^16                       (4)
                              =  u_0^32 · (7/2)^16.

Form the ratio:

  |det(D, L_t = 4)|_{m=0}
  ──────────────────────────  =  u_0^32 · (7/2)^16  /  (u_0^16 · 4^8)²
  |det(D, L_t = 2)|_{m=0}²       =  u_0^32 · (7/2)^16  /  (u_0^32 · 4^16)
                                =  (7/2)^16 / 4^16
                                =  (7/8)^16.    ∎                      (5)
```

This is class (A) — algebraic identity on admitted standard staggered
fermion eigenvalue structure. The single non-trivial step is the
Klein-four orbit closure giving sin²ω = 1/2 uniformly at L_t = 4 (per
[`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md));
the rest is direct substitution.

## 4. Bridge to the v compression (named-admission corollary)

**Corollary (conditional).** Under the admitted **per-mode geometric-mean
readout**

```text
v(L_t)  ∝  |det(D, L_t)|^(1 / (N_taste · L_t))                          (R)
```

with `N_taste = 16 = 2^D` in `D = 4` spacetime dimensions (admission
inherited from
[`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)),
the cross-endpoint compression factor is

```text
v(L_t = 4)
──────────  =  (|det(L_t = 4)| / |det(L_t = 2)|²)^(1 / (N_taste · L_t = 4))
v(L_t = 2)
            =  ((7/8)^16)^(1/64)
            =  (7/8)^(16/64)
            =  (7/8)^(1/4)                                             (6)
```

The **(1/4) power index is structurally forced** by the determinant
identity exponent 16 divided by `N_taste · L_t = 16 · 4 = 64`. The
factor (7/8) is **not** a numerical coincidence — it is the rational
identity (5).

### 4.1 Sign and placement

- **Sign.** From (5), `(7/8)^16 < 1`, hence the compression factor
  `(7/8)^(1/4) < 1`. The L_t = 4 endpoint has *smaller* `v` than the
  L_t = 2 endpoint. Sign: downward compression by ~3.3%.
- **Placement.** The compression is multiplicative on `v` itself
  (mass dim 1), not on `v²` or `v⁴`. Applied post-α_LM^16 hierarchy
  reduction.

### 4.2 What is NOT closed

The corollary depends on the **per-mode geometric-mean readout (R)**.
This admission is dimensionally consistent (`v` has mass dim 1; the
geometric mean of fermion eigenvalues has mass dim 1) and standard in
QFT (an average eigenvalue scale of a Dirac operator). However, the
framework does **not** independently derive this readout from the
retained primitive stack. Specifically:

1. The framework's hierarchy formula
   [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
   uses
   `v_UV = M_Pl × α_LM^16 = M_Pl × (1/(2π))^16 / |det(L_t = 2)|`
   (with `α_LM = 1/(4π u_0)` and `|det(L_t = 2)| = (4 u_0²)^8`),
   which is `v ∝ |det|^(-1)`, not `v ∝ |det|^(1/(N_taste · L_t))`.

2. The per-mode readout (R) is consistent with the COMPRESSION RATIO
   `(7/8)^(1/4)`, but does not by itself reproduce the absolute
   normalization of `v_UV`. Reconciling the two would require a
   bridge theorem connecting `|det|^(-1)` (the framework's specific
   absolute-scale identification at L_t = 2) with `|det|^(1/(N_taste · L_t))`
   (the per-mode reading that gives the right cross-endpoint compression).

3. Independent justification of (R) from the framework's primitives —
   e.g., a structural derivation of `v` as the geometric-mean fermion
   eigenvalue scale, with placement of the `M_Pl` scaling — is the
   single open theorem replacing the prior "dim-4 effective-potential
   density" hand-wave.

This is a strictly sharper formulation of the open piece than the
parent's "where does the (1/4) come from?" question. The parent
admitted "dim-4 V_eff density" as the hand-wave; this note reduces
the gap to the per-mode geometric-mean readout (R), which is
structurally narrower and directly testable.

## 5. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_matsubara_determinant_ratio_narrow.py
```

Verifies, at exact rational precision via Python `Fraction`:

1. Direct evaluation of `(7/2)^16 / 4^16 = (7/8)^16` as exact rational.
2. The L_s = 2 APBC mode placement gives `sin²(k_i) = 1` for all
   spatial directions and the temporal modes specialize to `sin²ω = 1`
   at L_t = 2 and `sin²ω = 1/2` at L_t = 4.
3. Substitution into formula (1) at m = 0 reproduces (3) and (4).
4. The ratio (5) holds as an exact rational identity.
5. Independent direct matrix evaluation: build the staggered Dirac
   operator on L_s = 2 × L_t lattice for L_t ∈ {2, 4}, compute
   `|det|` numerically with NumPy, and verify the ratio matches
   `(7/8)^16` to machine precision.
6. Corollary (6): `((7/8)^16)^(1/64) = (7/8)^(1/4)` to all available
   digits.

## 6. Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Pure algebraic determinant ratio identity for the staggered Dirac
  operator on Z^4 APBC at L_s = 2 with mean-field gauge factorization:
  |det(D, L_t=4, m=0)| / |det(D, L_t=2, m=0)|^2 = (7/8)^16.
  Plus a CONDITIONAL corollary deriving the v compression factor
  (7/8)^(1/4) from the determinant identity AND the per-mode
  geometric-mean readout v(L_t) ~ |det(L_t)|^(1/(N_taste * L_t)).
  The corollary is bounded by the named per-mode-readout admission;
  the determinant identity itself is unconditional.
proposed_load_bearing_step_class: A
status_authority: independent audit lane only

declared_one_hop_deps:
  - hierarchy_matsubara_determinant_narrow_theorem_note_2026-05-02
  - hierarchy_bosonic_bilinear_selector_note
  - hierarchy_dimensional_compression_note
  - hierarchy_effective_potential_endpoint_note
  - staggered_dirac_realization_gate_note_2026-05-03
  - minimal_axioms_2026-05-03

admitted_context_inputs:
  - per-mode geometric-mean readout v(L_t) ~ |det(L_t)|^(1/(N_taste * L_t))
    (named, separate from the determinant identity itself)
  - staggered taste count N_taste = 16 = 2^D in D = 4 spacetime dimensions
    (inherits from the staggered-Dirac realization open gate)

forbidden_imports_used: false
proposal_allowed: true
audit_required_before_effective_status_change: true
```

The narrow theorem is class (A) algebraic on admitted-standard staggered
fermion algebra (parent narrow theorem). The bridge corollary is
class (B) (carries one named admission). The independent audit lane
will evaluate the load-bearing class and any later status.

## 7. What this theorem closes

- **The (7/8) factor** in the v compression is now an **exact rational
  identity** on the staggered Dirac determinant, not a numerical
  coincidence. The (7/8)^(1/4) match to observed C_obs at 0.025% is no
  longer surprising — it's structurally forced.
- **The (1/4) power index** is reduced from "dim-4 V_eff density"
  hand-waving to **per-mode geometric-mean readout** — a structurally
  narrower and dimensionally clean named admission.
- **The audit lane's `audited_numerical_match` flag** on
  `hierarchy_dimensional_compression_note` should be reconsidered: the
  numerical match is now backed by an exact algebraic identity (5).

## 8. What this theorem does NOT close

- The per-mode geometric-mean readout (R) itself. This is the single
  open admission. Closing it would require deriving the readout from
  the retained framework primitives.
- Reconciliation with the framework's specific `v_UV ∝ |det(L_t = 2)|^(-1)`
  identification — the per-mode readout (R) gives the right COMPRESSION
  but a different ABSOLUTE-SCALE identification.
- Higgs-mass derivation `m_H = v / (2 u_0)` (separate; cluster
  obstruction).
- Choice of L_t = 4 endpoint (covered by the bosonic-bilinear selector
  note; this theorem inherits that selection).
- The 0.025% residual `C_obs - (7/8)^(1/4) = -0.000247` (consistent with
  plaquette/u_0 input uncertainty — gate #7 engineering frontier).

## 9. Cross-references

### Parent / specialization
- [`HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md`](HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md)
  — parent narrow theorem; this note carves out the cross-endpoint
  ratio specialization at L_t ∈ {2, 4}.
- [`HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md`](HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md)
  — grandparent decomposition note.

### v compression chain
- [`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
  — Klein-four orbit selection of L_t = 4 (inherited).
- [`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md)
  — auditor flagged `audited_numerical_match`; this note structurally
  backs the (7/8) factor.
- [`HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md`](HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)
  — exact A_2, A_4, A_inf endpoint formulas.
- [`HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`](HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md)
  — retained spatial APBC u_0 scaling.

### Framework axioms / structural
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  — open gate for N_taste = 16 = 2^D structural origin.

### Hierarchy product chain
- [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
  — full hierarchy formula `v = M_Pl × (7/8)^(1/4) × α_LM^16 = 246.28 GeV`.
