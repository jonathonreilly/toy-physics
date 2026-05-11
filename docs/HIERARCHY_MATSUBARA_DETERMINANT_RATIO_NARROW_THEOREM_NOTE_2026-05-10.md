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
**dim-4 effective-potential-density reading** — `v ∝ A(L_t)^(-1/4)`
where `A` is the m² coefficient of `Δf` at the symmetric point, per
[`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md)
and [`HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md`](HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)).
It does NOT close the readout admission itself.

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
- the **dim-4 effective-potential-density reading**
  `v ∝ A(L_t)^(-1/4)` itself (this is the named admission whose closure
  would discharge the remaining (1/4) gap — see Section 4);
- the staggered-Dirac realization gate (any further dependence on
  `N_taste = 16 = 2^D` inherits from the open gate
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
(**dim-4 effective-potential-density readout** — see
[`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md)
for the dimensional-analysis primitive and
[`HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md`](HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)
for the exact `A(L_t)` endpoint formulas).

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

**Corollary (conditional).** Under the admitted **dim-4
effective-potential-density readout**

```text
v(L_t)  ∝  A(L_t)^(-1/4)                                                (R)
```

where `A(L_t)` is the m² coefficient of `Δf` at the symmetric point
(per
[`HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md`](HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)):

```text
Δf(L_t, m)   =  A(L_t) m² + O(m⁴)
A(L_t)        =  (1 / (2 L_t u_0²)) Σ_ω 1 / (3 + sin²ω).
```

This is the dim-4 effective-potential-density reading: `v` has mass
dim 1, and `A · m²` (the curvature of the dim-4 free-energy density
at the symmetric point) has mass dim 2 — i.e., a mass². The full
dim-4 density at the symmetric point goes as `A · m⁴` once one
factors out the dim-4 normalization, so by `D = 4` dimensional
analysis at fixed external `m`, the dim-1 scale `v` extracted from
this density satisfies `v ∝ (A · m⁴)^(1/4) ∝ A^(1/4) · m`, with the
inverse compression `v ∝ A^(-1/4)` arising when `A` enters the
denominator of the scale-extracting map (Stefan-Boltzmann analog
`T ∝ (u/σ)^(1/4)` with `A` playing the role of the inverse-density
coefficient `σ`; see Section 4.3 for the QFT primitives derivation).

The exact endpoint values from
[`HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md`](HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)
are

```text
A_2  =  A(L_t = 2)  =  1 / (8 u_0²)
A_4  =  A(L_t = 4)  =  1 / (7 u_0²).
```

The cross-endpoint compression factor is then

```text
v(L_t = 4)
──────────  =  (A_2 / A_4)^(1/4)
v(L_t = 2)
            =  ((1/(8 u_0²)) / (1/(7 u_0²)))^(1/4)
            =  (7/8)^(1/4).                                             (6)
```

Within the admitted readout (R), the **(1/4) power index** is the
`D = 4` dimensional bookkeeping for an effective-potential density
(Stefan-Boltzmann-style scaling of a dim-1 scale extracted from a
dim-4 energy-density coefficient). This is not an independent
derivation of (R). The factor (7/8) is **not** a numerical coincidence
inside that conditional bridge: it equals `A_2 / A_4` exactly, and via
the Class A identity (5), the same `(7/8)^16` rational identity also
factors through the determinant ratio (since both `A_2 / A_4` and the
determinant ratio are governed by the same `(3 + sin²ω)` Matsubara sum
at L_s = 2).

### 4.1 Sign and placement

- **Sign.** Since `A_2 < A_4` (`1/8 < 1/7`), `(A_2 / A_4)^(1/4) < 1`,
  hence the compression factor `(7/8)^(1/4) < 1`. The L_t = 4
  endpoint has *smaller* `v` than the L_t = 2 endpoint. Sign:
  downward compression by ~3.3%.
- **Placement.** The compression is multiplicative on `v` itself
  (mass dim 1), not on `v²` or `v⁴`. Applied post-α_LM^16 hierarchy
  reduction.

### 4.2 Consistency with the Class A identity (5)

The endpoint values `A_2 = 1/(8 u_0²)` and `A_4 = 1/(7 u_0²)` are
direct consequences of the same `(3 + sin²ω)` Matsubara sum that
appears inside the determinant identity (5). Specifically, at L_s = 2
the contribution to `A(L_t)` from a single `ω` mode is
`1 / (3 + sin²ω)`; at L_t = 2 every mode has `sin²ω = 1` giving the
sum `2 / (3 + 1) = 1/2`, hence `A_2 = 1 / (2 · 2 · u_0²) · (1/2) = 1/(8 u_0²)`;
at L_t = 4 every mode has `sin²ω = 1/2` giving the sum
`4 / (3 + 1/2) = 8/7`, hence `A_4 = 1 / (2 · 4 · u_0²) · (8/7) = 1/(7 u_0²)`.
The (7/8) factor is therefore unified: it appears in **both** the
determinant ratio (5) — as `(7/8)^16` — and the dim-4 readout (R) —
as `A_2 / A_4 = 7/8` — through the same Klein-four-orbit selection
of `sin²ω = 1/2` at L_t = 4. This is the structural reason the
factor and the (1/4) power compose to give the observed
`(7/8)^(1/4)` compression.

### 4.3 Dimensional motivation for the readout admission (R)

Stripping framework vocabulary, standard QFT primitives motivate the
readout admission:

1. A scalar order parameter `φ` has mass dim 1 (4D action
   `S = ∫d⁴x [(∂φ)² - m²φ² - λφ⁴/4 + ...]` dimensionless).
2. The effective potential `V_eff(φ)` has mass dim 4 (energy
   density on Z⁴).
3. The curvature at the symmetric point `V_eff''(0) = A · m²` has
   mass dim 2, where `A` is the dimensionless (in `u_0` units)
   coefficient of `m²` in the small-φ expansion of `Δf`.
4. The readout admission treats the EWSB scale `v` as the dim-1 scale
   extracted from the effective-potential density. The Stefan-Boltzmann analog:
   thermal energy density `u = σ T⁴` gives `T ∝ (u/σ)^(1/4)` —
   when `σ` (the bulk normalization coefficient) varies with `L_t`
   and `u` is held fixed by an external scale, `T ∝ σ^(-1/4)`.
5. If this scale-extraction map is admitted, then by the same `D = 4`
   dimensional structure, with `A(L_t)` the
   `L_t`-dependent normalization coefficient of the dim-4 density
   and `m` the fixed external scale, the dim-1 EWSB scale extracted
   from the density satisfies `v(L_t) ∝ A(L_t)^(-1/4)`.

This dimensional motivation uses no framework-specific vocabulary:
only `D = 4` spacetime, the standard QFT mass-dimension assignments,
and Stefan-Boltzmann-style 1/4-power dimensional analysis. It does
**not** require introducing `N_taste` or per-mode geometric means, but
it still leaves (R) as the named readout admission identified in this
note.

### 4.4 What is NOT closed

The corollary depends on the **dim-4 effective-potential-density
readout (R)** as the framework's identification of `v`. This
admission is structurally clean (D = 4 spacetime dimensions; v has
mass dim 1; V_eff has mass dim 4; standard Stefan-Boltzmann scaling)
and directly inherits from
[`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md).
However, the framework does **not** independently derive (R) from
the retained primitive stack. Specifically:

1. The framework's hierarchy formula
   [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
   uses
   `v_UV = M_Pl × α_LM^16 = M_Pl × (1/(2π))^16 / |det(L_t = 2)|`
   (with `α_LM = 1/(4π u_0)` and `|det(L_t = 2)| = (4 u_0²)^8`),
   which is `v ∝ |det|^(-1)` at L_t = 2.

2. The dim-4 readout (R) `v ∝ A(L_t)^(-1/4)` is consistent with the
   COMPRESSION RATIO `(7/8)^(1/4)` and stays at fixed `m`, but does
   not by itself reproduce the absolute normalization of `v_UV`.
   Reconciling the two requires a bridge theorem connecting the
   absolute-scale identification at L_t = 2 with the dim-4-density
   `A`-scaling that governs the cross-endpoint compression.

3. Independent justification of (R) from the framework's primitives —
   e.g., a structural derivation showing the EWSB order parameter's
   dim-4 effective-potential-density character is forced by retained
   axioms rather than admitted as a standard QFT identification —
   is the single open theorem.

The previous formulation of this note (per-mode geometric-mean
readout `v ∝ |det|^(1/(N_taste · L_t))`) was **post-hoc**: the
combination `N_taste · L_t` had no QFT motivation, and `|det|^(1/N)`
is a fermion-eigenvalue scale, not the EWSB VEV. The current
dim-4-density reading is structurally cleaner: it gives the same
`(7/8)^(1/4)` compression but via D = 4 Stefan-Boltzmann-style
dimensional scaling — the same primitive that
[`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md)
established as the appropriate mapping between the L_t residual and
the EWSB scale.

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
6. **Dim-4 readout corollary (6):** the exact endpoint values
   `A_2 = 1/(8 u_0²)` and `A_4 = 1/(7 u_0²)` (per the
   effective-potential endpoint note) yield the compression
   `(A_2 / A_4)^(1/4) = (7/8)^(1/4)`. The runner verifies this with
   `Fraction` arithmetic on the `(3 + sin²ω)` Matsubara sum at
   L_s = 2.

## 6. Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Pure algebraic determinant ratio identity for the staggered Dirac
  operator on Z^4 APBC at L_s = 2 with mean-field gauge factorization:
  |det(D, L_t=4, m=0)| / |det(D, L_t=2, m=0)|^2 = (7/8)^16.
  Plus a CONDITIONAL corollary computing the v compression factor
  (7/8)^(1/4) from the determinant identity AND the dim-4 effective-
  potential-density readout v ∝ A(L_t)^(-1/4), where A(L_t) is the
  m^2 coefficient of Δf at the symmetric point per
  hierarchy_effective_potential_endpoint_note. The corollary is
  bounded by the named dim-4 V_eff'' readout admission; the
  determinant identity itself is unconditional.
proposed_load_bearing_step_class: A
status_authority: independent audit lane only

declared_one_hop_deps:
  - hierarchy_matsubara_determinant_narrow_theorem_note_2026-05-02
  - hierarchy_bosonic_bilinear_selector_note
  - hierarchy_dimensional_compression_note
  - hierarchy_effective_potential_endpoint_note
  - minimal_axioms_2026-05-03

admitted_context_inputs:
  - dim-4 effective-potential-density readout v ∝ A(L_t)^(-1/4),
    where A(L_t) is the m^2 coefficient of Δf at the symmetric
    point (named, separate from the determinant identity itself).
    Stefan-Boltzmann-style 1/4-power dimensional analysis motivates
    the admitted readout: v has mass dim 1 and V_eff has mass dim 4,
    so within this readout v scales as the 1/4 power of the appropriate
    L_t-dependent dim-4 density coefficient.

forbidden_imports_used: false
proposal_allowed: true
audit_required_before_effective_status_change: true
```

The narrow theorem is class (A) algebraic on admitted-standard staggered
fermion algebra (parent narrow theorem). The bridge corollary is
class (B) (carries one named admission). The independent audit lane
will evaluate the load-bearing class and any later status.

## 7. What this theorem closes

- **The (7/8) factor** in the conditional v-compression bridge is now an **exact rational
  identity** on the staggered Dirac determinant via (5), and is
  unified with the **`A_2 / A_4 = 7/8` ratio** of the dim-4
  effective-potential-density coefficients via the same `(3 + sin²ω)`
  Matsubara sum at L_s = 2 (Section 4.2). The `(7/8)^(1/4)` comparator
  is therefore structurally explained conditional on the admitted
  readout.
- **The (1/4) power index** is organized by the dim-4
  effective-potential-density readout admission
  ([`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md))
  and the exact endpoint values
  ([`HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md`](HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)).
  The 1/4 is the `D = 4` dimensional bookkeeping inside that admission:
  v has mass dim 1, V_eff has mass dim 4, and Stefan-Boltzmann-style
  scaling gives a 1/4-power map. This is structurally cleaner than the
  prior post-hoc per-mode geometric-mean readout
  `v ∝ |det|^(1/(N_taste · L_t))`, which had no QFT motivation for
  the combination `N_taste · L_t`.
- **The audit lane's `audited_numerical_match` flag** on
  `hierarchy_dimensional_compression_note` now has a sharper source-note
  basis for re-review: the numerical match is backed by an exact
  algebraic identity (5) and an exact endpoint computation
  `A_2 = 1/(8 u_0²)`, `A_4 = 1/(7 u_0²)` per the effective-potential
  endpoint note.

## 8. What this theorem does NOT close

- The dim-4 effective-potential-density readout (R) itself. This is
  the single open admission. Closing it would require a structural
  derivation (from retained framework primitives) showing the EWSB
  order parameter is genuinely identified with a dim-4
  effective-potential-density coefficient rather than a generic
  scalar field VEV.
- Reconciliation with the framework's specific `v_UV ∝ |det(L_t = 2)|^(-1)`
  absolute-scale identification at L_t = 2 — the dim-4 readout (R)
  gives the right COMPRESSION but does not by itself reproduce the
  absolute normalization.
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
  — auditor flagged `audited_numerical_match`; this note supplies exact
  source-note support for the (7/8) factor.
- [`HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md`](HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)
  — exact A_2, A_4, A_inf endpoint formulas.
- [`HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`](HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md)
  — retained spatial APBC u_0 scaling.

### Framework axioms / structural
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  — referenced by parent narrow theorem; the dim-4 readout in this
  note's §4 corollary does not depend on `N_taste`.

### Hierarchy product chain
- [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
  — full hierarchy formula `v = M_Pl × (7/8)^(1/4) × α_LM^16 = 246.28 GeV`.
