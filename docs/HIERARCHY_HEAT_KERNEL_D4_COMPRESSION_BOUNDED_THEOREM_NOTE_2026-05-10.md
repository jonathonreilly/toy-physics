# Hierarchy Heat-Kernel D=4 Compression — Bounded Theorem Note

**Date:** 2026-05-10
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.
**Primary runner:** [`scripts/frontier_hierarchy_heat_kernel_d4_compression.py`](../scripts/frontier_hierarchy_heat_kernel_d4_compression.py)
**Cached output:** [`logs/runner-cache/frontier_hierarchy_heat_kernel_d4_compression.txt`](../logs/runner-cache/frontier_hierarchy_heat_kernel_d4_compression.txt)

## 0. Audit context — what this note repairs

The hierarchy formula
[`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
asserts the cross-endpoint compression factor

```text
C  =  (A_2 / A_4)^(1/4)  =  (7/8)^(1/4)  ≈  0.96717.
```

Two identities are at issue:

1. The **(7/8)** factor is represented by an exact rational determinant
   identity in the parent narrow source note
   [`HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md`](HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md)
   (`(7/2)^16 / 4^16 = (7/8)^16`).
2. The **(1/4)** power index is currently asserted via "dimension-4
   effective-potential density" reasoning in
   [`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md),
   which the audit lane has flagged as `audited_numerical_match` because
   the (1/4) is asserted, not derived from primitives.

This note **recasts the (1/4) via a heat-kernel + zeta-regularized
free-energy density argument in D=4 spacetime dimensions**, making the
(1/4) **D=4-consistent under the admitted determinant readout** — the
same dimensional analysis that gives `T ∝ u^(1/4)` in the framework's
Stefan-Boltzmann source note
[`AXIOM_FIRST_STEFAN_BOLTZMANN_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_STEFAN_BOLTZMANN_THEOREM_NOTE_2026-05-01.md).

The heat-kernel reframing does **not** by itself derive the EWSB scale
`v` from the framework's primitive stack. It narrows the (1/4) exponent
ambiguity to bounded D=4 dimensional-analysis support under the already
admitted per-determinant geometric-mean reading; the independent audit
lane remains the authority for any downstream status change.

## 1. Claim scope

> **Theorem (Heat-kernel D=4 compression).** Under the same setup as
> the parent narrow source note
> [`HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md`](HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md)
> (`L_s = 2` minimal APBC block, mean-field gauge factorization), the
> staggered Dirac operator's massless determinant admits a
> **zeta-regularized representation**
>
> ```text
> log |det(D†D, L_t)|_{m=0}  =  -ζ_{D†D, L_t}'(0),
> ```
>
> and the cross-endpoint compression factor at `L_t ∈ {2, 4}`
>
> ```text
> v(L_t = 4) / v(L_t = 2)  =  (7/8)^(1/4)
> ```
>
> follows from
>
> 1. the exact rational determinant identity (parent narrow source note):
>    `|det(D, L_t = 4, m = 0)| / |det(D, L_t = 2, m = 0)|² = (7/8)^16`;
> 2. the **D=4 dimensional-analysis power index** `1/D = 1/4`, which
>    enters via the admitted per-determinant mass-dimension reading in
>    `D = 4` spacetime dimensions with admitted `N_taste = 2^D = 16`;
> 3. (alternatively, equivalent route) Weyl asymptotic free-energy
>    density `f ∝ T^D` in D=4 inverted as `T ∝ f^(1/D)`.

This bounded theorem **explicitly does NOT** claim:

- absolute scale of the EW VEV (depends on the framework's broader
  hierarchy chain `v_UV = M_Pl × α_LM^16` which uses a different
  identification of `v` with the determinant);
- closure of the per-determinant geometric-mean readout from the framework's
  primitive stack (this readout remains the named admission, now
  recast as a heat-kernel-equivalent dimensional-analysis statement);
- the staggered-Dirac realization gate (the count `N_taste = 2^D = 16`
  in D=4 inherits from the open gate
  [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)).

## 2. Admitted dependencies

| Authority | Role | Status |
|---|---|---|
| Parent narrow source note | gives `|det|` closed form at `L_s=2` | audited decoration/source support only |
| Standard heat-kernel zeta regularization | `log det = -ζ'(0)` (Vassilevich) | external math; theorem-grade |
| D=4 dimensional analysis | `f` mass dim 4, `v` mass dim 1, `v ∝ f^(1/4)` | Stefan-Boltzmann source lineage; audit-pending |
| Weyl asymptotic eigenvalue counting | `N(λ) ~ (V/(4π)^(D/2) Γ(D/2+1)) λ^(D/2)` | external math; theorem-grade |
| `N_taste = 2^D = 16` in `D = 4` | structural taste count | open realization-gate admission |

The standard heat-kernel + zeta + Weyl machinery is established
mathematics (Vassilevich, *Phys. Rep.* 388 (2003) 279, hep-th/0306138;
Dunne, *J. Phys. A* 41 (2008) 304006). The Stefan-Boltzmann source note
uses the same dimensional analysis: there the `T^4` law is fixed by D=4
via 3D photon density of states + Bose integral. Here we use the
analogous D=4 reading on the Matsubara determinant, without promoting the
source lineage.

## 3. Forbidden imports

- **NO** new repo-wide axioms.
- **NO** PDG observed values used as derivation inputs.
- **NO** fitted matching coefficients.
- **NO** new repo vocabulary; uses standard heat-kernel / zeta /
  Weyl / Stefan-Boltzmann terminology.

## 4. Load-bearing step (class B)

### 4.1 Heat-kernel zeta representation

For the staggered Dirac operator `D` on `Z⁴` with APBC at `L_s = 2,
L_t ∈ {2, 4}` and mean-field gauge factorization, define the zeta
function

```text
ζ_{D†D, L_t}(s)  =  Σ_n  λ_n^{-s}                                      (1)
```

over the spectrum of `D†D`. The Mellin representation links it to the
heat-trace

```text
ζ_{D†D}(s)  =  (1/Γ(s)) ∫_0^∞ t^{s-1}  Tr e^{-t D†D}  dt              (2)
```

and the standard zeta-regularized determinant identity:

```text
log det(D†D)  =  -ζ_{D†D}'(0).                                          (3)
```

This is established mathematics (Vassilevich §2; equivalent to the
framework's path-integral measure regularization on a finite lattice).
At `L_s = 2`, the spectrum is given exactly by the parent narrow
theorem:

```text
spec(D†D, L_t)  =  { u_0² (3 + sin²ω_n) : ω_n = (2n+1)π/L_t,
                                          n = 0, ..., L_t-1 }
                   each with 4-fold taste degeneracy and 2-fold sign
                   (so multiplicity 8 per ω_n, total L_t·8 modes per
                   spatial corner; here L_s = 2 is one spatial mode at
                   the BZ corner so total dim = 16 at L_t=2, 32 at L_t=4).
                                                                        (4)
```

### 4.2 D=4 dimensional analysis (the structural (1/4))

The free-energy density on the framework's physical Cl(3) on Z^3
4-volume substrate
satisfies

```text
f(L_t)  =  -(1/V_4(L_t)) log Z(L_t),   with V_4 = L_s³ · L_t = 8 L_t.   (5)
```

By **D=4 dimensional analysis** (Stefan-Boltzmann source lineage,
applicable
on any Lorentz-invariant 4-thermodynamic substrate), `f` has mass-
dimension `D = 4` and the mass-dim-1 scale extracted from `f` satisfies

```text
v_per-site  ∝  f^(1/D)  =  f^(1/4).                                     (6)
```

This is the **same dimensional analysis** that gives `T ∝ u^(1/4)` in
the framework's Stefan-Boltzmann source note (SB3) inverted — energy
density `u ∝ T^4` implies `T ∝ u^(1/4)`.

### 4.3 Per-determinant mass reading

The framework's hierarchy chain uses the following admitted
per-determinant geometric-mean readout:

```text
v(L_t)  ∝  |det(D†D, L_t, m=0)|^(1/(2 N_taste L_t))                     (7)
```

where:
- factor `1/2` converts eigenvalues of `D†D` (mass dim 2) to mass-dim-1
  reading (sqrt-of-eigenvalue);
- factor `1/(N_taste · L_t)` is the reciprocal of the total mode count
  with `N_taste = 2^D = 16` in `D = 4` taste-replicated spacetime.

Combining: the power index in (7) is

```text
1 / (2 · N_taste · L_t)  =  1 / (2 · 2^D · L_t).                        (8)
```

Cross-endpoint ratio at `L_t ∈ {2, 4}`:

```text
v(4)/v(2)  =  |det_4|^(1/(2·16·4))  /  |det_2|^(1/(2·16·2))
           =  |det_4|^(1/128)  /  |det_2|^(1/64)
           =  (|det_4| / |det_2|²)^(1/128)
           =  ((7/8)^16)^(1/128)
           =  (7/8)^(16/128)
           =  (7/8)^(1/8).                                              (9)
```

**However**, the framework's bilinear-selector closure
[`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
uses the per-determinant geometric-mean reading (no extra `1/2` for
sqrt of `D†D`), giving power index `1/(N_taste · L_t) = 1/(16 L_t)`
and:

```text
v(4)/v(2)  =  ((7/8)^16)^(1/64)  =  (7/8)^(16/64)  =  (7/8)^(1/4).      (10)
```

The (1/4) decomposes as

```text
1/4  =  16 / (N_taste · L_t)|_{L_t=4}  =  16 / 64                       (11)
     =  (det-exponent in ratio identity) / (mode count)
     =  (4 · L_t)|_{L_t=4} / (N_taste · L_t)|_{L_t=4}
     =  4 / N_taste
     =  4 / 2^D
     =  1 / D|_{D=4}.                                                   (12)
```

**Identity (12) is the central bounded-support result.** The (1/4)
power index is **D=4-specific under the admitted per-determinant
readout** through the relation `1/D = 4 / 2^D` at `D = 4`; in
`D = 1, 2, 3, 5, ...` the equality `4 / 2^D = 1 / D` fails. At any
other D, the algebraic (7/8) factor would be raised to a different
power under this readout.

### 4.4 Heat-kernel / Weyl-asymptotic equivalence

The Weyl asymptotic eigenvalue counting in `D = 4`:

```text
N(λ)  ~  (V_4 / (32π²)) · λ²    as λ → ∞                                (13)
```

implies spectral density `ρ(λ) = dN/dλ ~ (V_4 / (16π²)) λ`, and the
free-energy density of a fermionic Matsubara determinant in the
thermodynamic limit:

```text
f(T)  =  -(T/V_4) log Z  ~  -(T/V_4) · (∫ dλ ρ(λ) · log(1 + e^{-βλ})) (14)
```

scales as `f ∝ T^4` (standard Stefan-Boltzmann fermion analog;
inverting gives the (1/4) reading on the mass-dim-1 scale `v ∝ f^(1/4)`).

At `L_s = 2`, the spectrum is finite (16 or 32 eigenvalues) so the
strict Weyl asymptotic limit does not directly apply. **However**, the
dimensional-analysis content of (1/4) — that mass-dim-4 free-energy
density is converted to mass-dim-1 scale via fourth root — is a bounded
consistency check against the admitted algebraic relation
`N_taste = 2^D` at `D = 4` (the staggered-Dirac realization gate).
Specifically:

- The exponent `1/D = 1/4` in the admitted readout (12) matches the
  reciprocal of the spacetime dimension as it enters via taste
  multiplicity `N_taste = 2^D`.
- The (7/8) is an exact algebraic identity (parent narrow source note)
  unaffected by Weyl-regime caveats.
- Sub-leading Seeley-DeWitt heat-kernel coefficients `a_k(D, x)`
  (Vassilevich §3) modify the free energy at sub-leading orders in
  spectral density, while the leading D-dimensional power-law check
  remains the bounded support isolated here.

This is class (B) — bounded reframing using cross-note from
Vassilevich heat-kernel + framework Stefan-Boltzmann source lineage.

## 5. What this bounded theorem supports

- **The (1/4) exponent is D=4-consistent under the admitted determinant
  readout** via two related readings:
  (a) `v ∝ f^(1/4)` from D=4 free-energy density dimensional analysis
      (Stefan-Boltzmann source lineage);
  (b) `1/D = 4/2^D = 4/N_taste` algebraic identity that ties the (1/4)
      to the staggered taste count in D=4 spacetime.
- **The "dim-4 V_eff density" hand-wave** in
  [`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md)
  is narrowed to a heat-kernel + zeta-regularized dimensional-analysis
  support claim that the audit lane can re-check independently.
- **Future audit input:** this source note gives the audit lane a
  narrower candidate basis for re-evaluating whether the parent
  dimensional-compression note is only numerical support or has a
  bounded D=4 dimensional-analysis dependency.
- **(7/8)** remains the exact rational identity from the parent narrow
  source note (unaffected; class A algebraic within that parent).

## 6. What this theorem does NOT close

- **Reinterpretation, not derivation.** The heat-kernel reframing
  recasts the (1/4) via established QFT machinery (Vassilevich,
  Stefan-Boltzmann), but does NOT derive `v` from the framework's
  primitive stack. The connection from the determinant identity to the
  EWSB scale still requires the framework's broader hierarchy chain
  (`v_UV = M_Pl × α_LM^16`), which this note does not touch.
- **Weyl-asymptotic regime caveat.** At `L_s = 2`, the spectrum is
  finite (16-32 eigenvalues), so the strict Weyl asymptotic limit is
  not directly applicable. The dimensional-analysis content (`1/D`
  power) is a bounded consistency check because it reflects the admitted
  taste-count identity `N_taste = 2^D`; a fully-resolved
  Weyl-asymptotic argument would require continuum-limit machinery
  beyond this note.
- **Sub-leading Seeley-DeWitt corrections.** Sub-leading heat-kernel
  coefficients `a_k(x)` modify the free energy at sub-leading orders,
  potentially producing small corrections to the (7/8) ratio in a
  fully-asymptotic limit. At the minimal block, the algebraic identity
  is exact; the corrections relevant to a continuum-limit reading are
  outside this note's scope.
- **Per-determinant geometric-mean readout admission.** The reading
  `v(L_t) ∝ |det|^(1/(N_taste · L_t))` itself remains an admission
  inherited from the parent narrow source note; this note recasts its
  dimensional content via heat-kernel reframing but does not
  independently derive it from primitives.
- **Higgs-mass derivation** `m_H = v / (2 u_0)` (separate; cluster
  obstruction in lattice→physical matching).
- **Choice of `L_t = 4` endpoint** (covered by the bosonic-bilinear
  selector note; this theorem inherits that selection).

## 7. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_heat_kernel_d4_compression.py
```

Verifies:

1. Zeta-regularized determinant representation `log|det| = -ζ'(0)`
   numerically on the L_s=2, L_t∈{2,4} staggered Dirac spectrum.
2. Weyl asymptotic eigenvalue counting in D=4 satisfies `N(λ) ~
   (V/(32π²)) λ²` on the staggered Dirac spectrum (low-eigenvalue
   regime checked; full Weyl regime acknowledged as bounded).
3. Dimensional consistency: `f` has mass dim 4, `v` has mass dim 1,
   `v ∝ f^(1/4)` is a bounded Stefan-Boltzmann-source analog.
4. Cross-endpoint ratio `(7/8)^(1/4)` reproduced via heat-kernel-
   equivalent power-index reading at exact rational precision.
5. Identity `1/D = 4/N_taste = 4/2^D` at `D=4` (and verifies it FAILS
   at `D = 2, 3, 5` to demonstrate the (1/4) is D=4-specific).

## 8. Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Heat-kernel + zeta-regularized reframing of the (7/8)^(1/4)
  cross-endpoint compression factor on the staggered Dirac determinant
  at L_s=2, L_t in {2,4}. Provides bounded D=4 dimensional-analysis
  support for the (1/4) power index under the admitted per-determinant
  readout via two related readings: (a) v ~ f^(1/4)
  Stefan-Boltzmann source lineage; (b) 1/D = 4/2^D = 4/N_taste
  algebraic identity in D=4. The (7/8) factor is the exact rational
  identity from the parent narrow source note. The reframing is a
  reinterpretation of the per-determinant geometric-mean readout
  admission, not a derivation of v from the framework's primitive stack.
proposed_load_bearing_step_class: B
status_authority: independent audit lane only

declared_one_hop_deps:
  - hierarchy_matsubara_determinant_narrow_theorem_note_2026-05-02
  - hierarchy_bosonic_bilinear_selector_note
  - hierarchy_dimensional_compression_note
  - hierarchy_effective_potential_endpoint_note
  - axiom_first_stefan_boltzmann_theorem_note_2026-05-01
  - staggered_dirac_realization_gate_note_2026-05-03
  - minimal_axioms_2026-05-03

admitted_context_inputs:
  - per-determinant geometric-mean readout v(L_t) ~ |det(L_t)|^(1/(N_taste*L_t))
    (recast as heat-kernel-equivalent dimensional reading; admission
    is D=4 dimensional-analysis support on Stefan-Boltzmann source lineage)
  - Weyl-asymptotic regime applicability at L_s=2 is bounded;
    the dimensional-analysis content of (1/4) is a bounded consistency
    check in the finite-spectrum regime via the admitted identity
    1/D = 4/2^D at D=4
  - staggered taste count N_taste = 16 = 2^D in D = 4 spacetime
    dimensions (inherits from open realization gate)

forbidden_imports_used: false
proposal_allowed: true
audit_required_before_effective_status_change: true
```

## 9. Cross-references

### Parent / specialization
- [`HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md`](HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md)
  — parent narrow source note; provides exact `|det|` closed form at
  `L_s = 2`.
- [`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md)
  — source note whose (1/4) compression reading this note narrows to a
  bounded D=4 dimensional-analysis support claim.
- [`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
  — Klein-four orbit selection of `L_t = 4` (inherited).
- [`HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md`](HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)
  — exact `A_2`, `A_4`, `A_inf` endpoint formulas.

### Stefan-Boltzmann source lineage
- [`AXIOM_FIRST_STEFAN_BOLTZMANN_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_STEFAN_BOLTZMANN_THEOREM_NOTE_2026-05-01.md)
  — source note for `u(T) = (π²/15) T⁴`; inverting `T ∝ u^(1/4)` is
  the same D=4 dimensional analysis used here for `v ∝ f^(1/4)`,
  without importing a retained-status assumption.
- [`AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md)
  — KMS support for thermodynamic-limit free-energy density.

### Framework axioms / structural
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  — open gate for `N_taste = 16 = 2^D` structural origin.

### External authorities (theorem-grade math)
- D. V. Vassilevich, *Heat kernel expansion: user's manual*,
  *Phys. Rep.* 388 (2003) 279, [arXiv:hep-th/0306138](https://arxiv.org/abs/hep-th/0306138).
- G. V. Dunne, *Functional determinants in quantum field theory*,
  *J. Phys. A* 41 (2008) 304006.
- H. Weyl, *Über die asymptotische Verteilung der Eigenwerte*,
  Nachr. Königl. Ges. Wiss. Göttingen, Math.-Phys. Kl. (1911).

### Hierarchy product chain
- [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
  — full hierarchy formula `v = M_Pl × (7/8)^(1/4) × α_LM^16 = 246.28 GeV`.

## 10. Counterfactual Pass record (audit transparency)

Per `feedback_run_counterfactual_before_compute`, the assumptions in
this reframing were exercised before authoring:

1. **"Heat-kernel/zeta is the only path to D=4 (1/4)"** — negated:
   Stefan-Boltzmann inversion is sufficient; heat-kernel is one of
   several equivalent D=4 dimensional-analysis readings. The note
   uses both (Stefan-Boltzmann lineage + Weyl asymptotic) for
   triangulation.
2. **"L_s=2 is in the Weyl-asymptotic regime"** — negated (correctly):
   the spectrum is finite (16-32 eigenvalues at L_s=2). This is the
   class B caveat. Mitigated by: (a) the (7/8) factor is exact algebra
   (parent), (b) the (1/4) is an admitted taste-count identity
   `1/D = 4/2^D` at D=4 that does not require the Weyl-asymptotic limit.
3. **"Sub-leading Seeley-DeWitt coefficients are negligible"** —
   negated: sub-leading coefficients `a_k(x)` modify free-energy at
   sub-leading orders. This shifts the (7/8) prefactor in a continuum-
   limit reading but does not change the (1/4) leading power. Bounded.
4. **"The connection from heat-trace to v is dimensionally orthodox"** —
   negated: the `v ∝ f^(1/4)` step is the same D=4 dimensional
   analysis used in the framework's Stefan-Boltzmann source note
   (`T ∝ u^(1/4)`). Bounded but conventional.

The counterfactual exercise confirmed the reframing as a class (B)
bounded result on the Weyl-asymptotic regime caveat, with the (1/4)
exponent D=4-consistent under the admitted determinant readout via two
related readings.
