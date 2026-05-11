# Symmetric-Point Curvature Ratio κ_curv from V_taste — Narrow Algebraic Theorem

**Date:** 2026-05-10
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.
**Primary runner:** [`scripts/frontier_higgs_kappa_curv_narrow.py`](../scripts/frontier_higgs_kappa_curv_narrow.py)

## 0. Audit context and scope

This note isolates a **dimensionless ratio derived from V_taste's
symmetric-point curvature** and gives it an explicit name,
`κ_curv`, distinct from any SM EFT object. The Clifford-fixed identity:

```text
κ_curv  :=  |∂²V_taste/∂m²|_{m=0}|  /  (2 N_taste)  =  1 / (8 u_0²).
```

Two prior iterations of this PR established that:

1. The substitution chain `m_H_tree = v/(2u_0) ⟹ m_H² = 2λv² ⟹ λ = 1/(8u_0²)`
   is a class-(F) renaming (silently identifies the framework's
   tachyonic-symmetric-point curvature scale with the SM post-EWSB Higgs
   pole). An independent audit pre-check flagged this in the v1
   draft; v2 attempted to defuse it by introducing `λ_curv` while
   keeping λ in the symbol.
2. Even with `λ_curv` as the symbol, **calling a curvature-derived ratio
   "λ" is misleading by first-principles QFT standards** — λ is the
   coefficient of `|φ|⁴` in V_eff, not a normalized curvature ratio.
   This v3 iteration replaces the misleading λ-name with the
   first-principles-honest **κ** (kappa, generic dimensionless ratio).

**Why the symbol matters.** In standard QFT, the SM Higgs quartic λ
is the |φ|⁴ coefficient of V_eff. The framework's V_taste at m=0 has
its **dimensionless lattice curvature** ≈ -4/u_0² and its **m⁴ coefficient** ≈
+1/(4u_0⁴). These are different objects. Any v²-normalized magnitude
of a physical mass² coefficient (what the framework elsewhere compares
to `m_H_tree²/v²`) requires an additional scale map not proved here. This
theorem keeps only the lattice-normalized curvature ratio. Naming it
κ_curv (not λ_curv) makes that boundary honest.

The κ_curv ↔ SM λ bridge — i.e., whether κ_curv is *related* to the
SM EFT quartic at any matching scale — is named here as an **open
theorem**, not closed.

## 1. Claim scope

> **Theorem (symmetric-point curvature ratio).** Define the
> dimensionless ratio
>
> ```text
> κ_curv  :=  |∂²V_taste/∂m²|_{m=0}|  /  (2 N_taste)                  (1)
> ```
>
> on the physical Cl(3) local algebra plus Z^3 spatial substrate
> Wilson-plaquette + staggered-Dirac mean-field surface, where:
> - `V_taste(m) = -8 log(m² + 4u_0²)` is the per-channel taste-trace
>   potential at the symmetric point on the L_s = 2 mean-field APBC
>   surface (admitted from HIGGS_MASS_FROM_AXIOM Step 4);
> - `N_taste = 16` is the staggered taste count from the open
>   staggered-Dirac realization gate;
> - `u_0` is the mean-field plaquette parameter.
>
> Then
>
> ```text
> κ_curv  =  1 / (8 u_0²)                                              (2)
> ```
>
> with no dependence on `v`. At
> `u_0 = ⟨P⟩^(1/4) ≈ 0.8776` (Gate #7 engineering frontier),
>
> ```text
> κ_curv  ≈  0.1623.                                                   (3)
> ```

The narrow theorem **explicitly does NOT** claim:

- that `κ_curv` is the SM Higgs quartic coupling λ at any scale;
- that `κ_curv` is *any* coefficient in the SM EFT effective potential
  (κ_curv is constructed from the m² coefficient of V_taste; the SM
  EFT quartic λ is the |φ|⁴ coefficient of V_eff — see §3, these are
  structurally different objects);
- that this theorem closes Gate #6 (lambda-UV anchor) of the
  seven-gate near-zero-imports map;
- that `m_H_tree := v/(2u_0)` is the SM post-EWSB Higgs pole;
- that the dimensionless lattice curvature has already been converted
  into a physical `m_H_tree²/(2v²)` ratio;
- a Higgs mass closure at observed `m_H_pole = 125.10 GeV`;
- a precise scale identification (the natural matching scale of κ_curv
  is the lattice mean-field scale where V_taste's curvature is read
  off, which is Planck-scale up to O(1) Wilson coefficient under the
  still-separate Planck pin bridge).

## 2. Counterfactual Pass — implicit assumptions

| # | Assumption | Forced or imported? | If wrong, what changes? |
|---|---|---|---|
| 1 | V_taste form `-8 log(m² + 4u_0²)` per channel | Imported from HIGGS_MASS_FROM_AXIOM Step 4 | Numerical κ_curv shifts; structural form stays. |
| 2 | N_taste = 16 = 2^D in D=4 | Open staggered-Dirac gate | Numerical κ_curv shifts; structural form `1/(8u_0²)` unchanged. |
| 3 | u_0 = ⟨P⟩^(1/4) ≈ 0.8776 | Gate #7 engineering frontier | Numerical κ_curv shifts; structural form unchanged. |
| 4 | κ_curv uses the dimensionless lattice curvature normalization `|V''(0)|/(2N_taste)` | Forced (this note's choice) | If this is instead interpreted as a physical `m_H_tree²/(2v²)` statement, an extra lattice-to-EW scale bridge is being smuggled in. This theorem does not close that bridge. |
| 5 | κ_curv is structurally NOT the SM Higgs quartic λ | Forced from first principles (see §3) | If κ_curv WERE identified with SM λ, the theorem would close Gate #6 — but the identification doesn't hold from first principles, so the bridge remains open. |

The load-bearing assumption is (1): V_taste's logarithmic form. Once
that is admitted, (i) ∂²V_taste/∂m²|_{m=0} = -4/u_0² is class-(A)
algebraic, and the κ_curv definition (1) reduces to `1/(8u_0²)` by
substitution.

## 3. Elon first-principles — what is κ_curv, really?

**Stripping all framework conventions, what does fundamental QFT say
about the objects this theorem touches?**

The Standard Model Higgs Lagrangian has

```text
V_SM(φ)  =  -μ²|φ|²  +  λ|φ|⁴  +  (loop corrections).                  (*)
```

In Wilsonian RG, **λ at scale μ is the coefficient of `|φ|⁴`** in the
Wilsonian effective potential after integrating out modes with momentum
greater than μ. m_H is the curvature at the broken-phase MINIMUM:
`m_H_pole² = ∂²V_eff/∂φ²|_{φ=v_min} = 2λv²` at tree level.

These are well-defined first-principles objects. λ is a **|φ|⁴
coefficient**. m_H_pole is a **broken-phase pole**.

Now, what is V_taste from a first-principles standpoint?

V_taste(m) = -8 log(m² + 4u_0²) is the log of the staggered Dirac
determinant on the L_s=2 minimal block under mean-field gauge. By
construction, this is the **fermion-loop contribution to the Wilsonian
effective action at the lattice scale** for a composite scalar
parameterized by m. If m is identified with a Yukawa-coupled Higgs
scalar (m = y_t · φ), then V_taste in φ has

```text
V_taste(φ)  =  -8 log(y_t² φ² + 4u_0²)
            =  const  -  (2 y_t²/u_0²) φ²  +  (y_t⁴/(4u_0⁴)) φ⁴  -  O(φ⁶).
```

By first-principles QFT, the **|φ|⁴ coefficient is `y_t⁴/(4u_0⁴)` per
channel**. This IS a fermion-loop-induced quartic at the lattice
scale. It is the candidate "λ" in the SM EFT sense (with N_taste, N_c
multiplicities applied). It depends on `y_t`, not just `u_0`.

**Now: what is κ_curv as defined in (1)?**

```text
κ_curv  =  |∂²V_taste/∂m²|_{m=0}|  /  (2 N_taste)
        =  (4/u_0²)  /  32
        =  1 / (8 u_0²).
```

So κ_curv is a dim-0 ratio of [dimensionless lattice curvature of
V_taste] / [taste-count normalization]. **It is structurally a
lattice-normalized curvature ratio, NOT a |φ|⁴ coefficient.**
κ_curv is structurally a lattice-normalized curvature ratio, not a quartic coupling.
Concretely:

- κ_curv = (dimensionless ratio of) the symmetric-point curvature
  magnitude divided by `2N_taste`.
- SM λ (first-principles definition) = |φ|⁴ coefficient in V_eff.

These are different kinds of objects. κ_curv is a lattice curvature
ratio; SM λ is a quartic coupling. The numerical relation
`m_H² = 2λv²` in the SM holds only **post-EWSB at the broken-phase
pole**, where `m_H` is the pole mass and λ is the broken-phase
quartic. Reusing that relation here would require a separate bridge
from lattice curvature to physical mass scale. That bridge is not
proved here.

**Net first-principles statement:**

κ_curv is a **well-defined dimensionless lattice quantity**: it is the
normalized magnitude of V_taste's symmetric-point curvature, divided
by `2N_taste`. It is NOT structurally the SM Higgs quartic. The
relation to SM λ requires both a lattice-curvature-to-physical-mass
bridge and, after that, a broken-phase pole/quartic bridge. Neither is
a first-principles identity in this theorem.

**What this means for naming.** Calling this object "λ_curv" is
misleading by first-principles standards because λ already denotes a
quartic coupling. The honest first-principles symbol is **κ** (a
generic dimensionless ratio with no implied quartic-coupling
structure), with the subscript `_curv` indicating it derives from a
curvature.

This is the heart of the rescoping. The previous PR drafts (v1, v2)
both used "λ" naming because they were anchored on the framework's
HIGGS_MASS_FROM_AXIOM convention; this v3 strips the framework
convention and uses the first-principles-honest symbol.

## 4. Admitted dependencies

| Authority | Role | Status |
|---|---|---|
| [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) Step 4 | V_taste form `-8 log(m² + 4u_0²)` per channel | unaudited |
| [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md) | N_taste = 16 = 2^D | open gate |
| [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | physical Cl(3) local algebra plus Z^3 spatial substrate baseline | meta |
| `u_0 = ⟨P⟩^(1/4) ≈ 0.8776` (Gate #7) | numerical input | engineering frontier |

The bare algebraic identity `κ_curv = 1/(8u_0²)` requires only the
V_taste form. No SM EFT structure, no Higgs scalar, no λ identification
is admitted. This note does not load-bear on any unmerged sibling PRs.

## 5. Load-bearing step (class A)

```text
From V_taste(m) = -8 log(m² + 4 u_0²):

  ∂V_taste/∂m  =  -8 · 2m / (m² + 4 u_0²)

  ∂²V_taste/∂m²  =  -8 · [2/(m² + 4u_0²)  -  4m²/(m² + 4u_0²)²]

At m = 0:

  ∂²V_taste/∂m²|_{m=0}  =  -8 · 2 / (4 u_0²)  =  -4 / u_0².            (i)

Definition of κ_curv (this theorem; class E):

  κ_curv  :=  |∂²V_taste/∂m²|_{m=0}|  /  (2 N_taste)
            =  (4 / u_0²)  /  (2 · 16)
            =  1 / (8 u_0²).                                             (ii)

No `v` scale is used in this theorem. Any later conversion of this
lattice-normalized curvature ratio into a physical
`m_H_tree²/(2v²)`-style comparison is a separate bridge. Class (A)
algebraic substitution in (ii). ∎
```

## 6. Structural implications (named, not derived)

### 6.1 Numerical value

At `u_0 = ⟨P⟩^(1/4) ≈ 0.8776` (Gate #7):

```text
κ_curv  =  1 / (8 · 0.7702)  =  0.1623.
```

Clifford-fixed: depends only on u_0.

### 6.2 Named open bridge: κ_curv ↔ SM λ

The relation between κ_curv (lattice curvature ratio) and the SM
EFT Higgs quartic λ (a |φ|⁴ coefficient at some matching scale) is
**not** a first-principles identity. Two paths to a future bridge
theorem:

1. **Identify symmetric-point curvature with broken-phase pole.** The
   framework's HIGGS_MASS_FROM_AXIOM Step 5(b) admits this becomes
   exact in a limit "(i) all N_taste taste channels degenerate, (ii)
   gauge corrections vanish, (iii) EWSB saddle aligns with
   symmetric-point curvature. None of (i)-(iii) is exactly true."
   The +12% gap from m_H_tree=140.3 to m_H_pole_obs=125.10 GeV is the
   numerical magnitude of (i)-(iii) failing. Closing this would map
   κ_curv to (1+ε) · λ(μ_*) at some matching scale μ_*.
2. **Compute the first-principles fermion-loop quartic at the lattice
   scale.** The |φ|⁴ coefficient of V_taste(φ=y_t·φ) at the lattice
   scale is `y_t⁴/(4u_0⁴)` per channel (see §3). This IS a candidate
   for SM λ at the lattice scale via fermion-loop matching. The
   relation between κ_curv (lattice curvature ratio) and this fermion-loop quartic
   is `κ_curv ≠ y_t⁴/(4u_0⁴)`; they are different objects.

This narrow theorem closes neither bridge. It records the gap.

### 6.3 No comparison to Shaposhnikov-Wetterich

S-W's `λ(M_Pl) = 0` is for the SM EFT λ. κ_curv is not the SM EFT λ
(per §3). The theorem makes no comparison to S-W; comparison would
require closing the bridge in §6.2 first.

## 7. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_higgs_kappa_curv_narrow.py
```

Verifies:

1. V_taste curvature `∂²V_taste/∂m²|_{m=0} = -4/u_0²` symbolically via
   SymPy.
2. κ_curv definition `|∂²V_taste/∂m²|_{m=0}|/(2N_taste)` with
   sign-magnitude convention.
3. Clifford-fixed identity `κ_curv = 1/(8u_0²)`.
4. Numerical κ_curv ≈ 0.1623 at u_0 = 0.8776.
5. **First-principles fermion-loop quartic** `y_t⁴/(4u_0⁴)` per channel
   (the SM-EFT-style |φ|⁴ coefficient) — computed separately to make
   the structural distinction explicit.
6. Audit comparator against SM λ_obs(v) ≈ 0.129 (PDG-derived; NOT a
   derivation input).
7. Note structure / scope discipline / first-principles-honest naming
   (no "λ" applied to curvature ratios).

The runner does **not** verify any identification of κ_curv with SM λ
— that's outside this theorem's scope.

## 8. Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Algebraic identity kappa_curv = 1/(8 u_0^2) where kappa_curv is the
  framework's dimensionless symmetric-point curvature ratio defined as
  |d^2 V_taste/dm^2|_{m=0}| / (2 N_taste) on L_s=2 mean-field
  surface. kappa_curv is structurally a lattice-normalized curvature
  ratio, NOT a quartic coupling and NOT a physical mass/v^2 bridge.
  EXPLICITLY DISTINCT from the SM EFT Higgs quartic lambda; the
  kappa_curv <-> SM lambda bridge is named as open work, not closed.
  At u_0 = 0.8776 (Gate #7), kappa_curv ≈ 0.1623.
proposed_load_bearing_step_class: A
proposed_definitional_step_class: E   # the (2v^2) divisor is a definitional choice
status_authority: independent audit lane only

declared_one_hop_deps:
  - higgs_mass_from_axiom_note   # V_taste form Step 4
  - staggered_dirac_realization_gate_note_2026-05-03   # N_taste=16
  - minimal_axioms_2026-05-03   # physical Cl(3) local algebra + Z^3 spatial substrate baseline
  - c_iso_su3_nnlo_closure_bounded_note_2026-05-10_su3nnlo   # u_0 frontier

admitted_context_inputs:
  - V_taste form V(m) = -8 log(m² + 4 u_0²) (HIGGS_MASS_FROM_AXIOM Step 4)
  - N_taste = 16 = 2^D (staggered-Dirac realization open gate)
  - numerical u_0 ≈ 0.8776 (Gate #7 engineering frontier; structural
    form 1/(8 u_0^2) holds independent of numerical value)

forbidden_imports_used: false   # no PDG values are derivation inputs;
                                 # observed lambda_obs(v) appears only as
                                 # audit comparator
proposal_allowed: true
audit_required_before_effective_status_change: true

named_open_bridge:
  bridge_id: kappa_curv_to_sm_lambda
  description: |
    The relation between the framework's kappa_curv (mass^2-derived
    dimensionless ratio at the lattice symmetric point) and the SM
    EFT Higgs quartic lambda (a |phi|^4 coefficient at some matching
    scale) is open. From first principles these are different
    structural objects (mass^2 vs quartic coupling); identifying them
    requires either (a) a theorem mapping symmetric-point curvature
    to broken-phase pole (the framework's named +12% gap), or (b)
    matching kappa_curv to the first-principles fermion-loop quartic
    y_t^4/(4 u_0^4) per channel. Neither is closed.
```

## 9. What this theorem closes

- **`κ_curv = 1/(8u_0²)` is an exact Clifford-fixed dimensionless
  lattice ratio.** Class (A) algebraic on V_taste's symmetric-point
  curvature plus the (E) definitional choice of the `2N_taste`
  normalization.
- **The first-principles-honest naming is now in place.** The object
  is not called λ (a quartic coupling); it's called κ (a generic
  dimensionless ratio). The structural distinction from SM λ is
  visible at the symbol level.

## 10. What this theorem does NOT close

- **`κ_curv ↔ SM λ` bridge** (named open theorem).
- **Gate #6 (lambda-UV anchor) in full.** Gate #6 closure requires
  the bridge above; this narrow theorem provides one Clifford-fixed
  lattice-side ingredient, not the bridge.
- **The framework's `λ(M_Pl) = 0` claim from VACUUM_CRITICAL_STABILITY.**
  That claim is about SM λ; this theorem is silent on it (κ_curv is a
  different object).
- **The first-principles fermion-loop quartic `y_t⁴/(4u_0⁴)`** at the
  lattice scale (a different object from κ_curv; if it could be
  computed from the framework's y_t Ward chain plus u_0, it would be a
  candidate UV anchor for SM λ via fermion-loop matching).
- The Higgs-mass prediction at v.
- The Planck pin (Gate #4).
- The staggered-Dirac realization gate.
- The numerical u_0 (Gate #7).

## 11. Cross-references

### Parent / structural
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  — provides V_taste form (Step 4); Step 5(b) names the +12% gap
  that becomes the named open bridge in §6.2.
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  — N_taste = 16 = 2^D origin (open gate).

### Context (parallel-track, not load-bearing)
- `VACUUM_CRITICAL_STABILITY_NOTE.md`
  — claims `λ(M_Pl) = 0` for SM λ; this narrow theorem is silent on
  whether that holds; κ_curv is a different object entirely.
- `HIGGS_MASS_DERIVED_NOTE.md`
  — assumption-derivation ledger names the open quartic-boundary
  theorem.

### Framework baseline / structural
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md`](C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md)
  — Gate #7 engineering frontier; provides u_0 numerical context.

### Standard physics references (admitted-context literature, not load-bearing)
- Coleman & Weinberg (1973) — radiative corrections framing for the
  named open bridge in §6.2.
- Bardeen, Hill, Lindner (1990) — top-condensation NJL: composite
  scalar with finite induced quartic at matching scale (a comparator
  for the first-principles fermion-loop quartic in §6.2 path 2).
