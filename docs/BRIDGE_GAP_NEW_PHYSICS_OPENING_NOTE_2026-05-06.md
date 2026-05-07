# Bridge Gap — New-Physics Opening: Wilson Action Is Imported, Not Derived

**Date:** 2026-05-06
**Claim type:** new-physics research target identification
**Status:** This note identifies an unexamined assumption shared by all
seven previously-exhausted attack routes, supersedes the "commit to
industrial SDP" framing of [`BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md`](BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md),
and frames the actual new-physics research target.
**Origin:** round-3 special-forces attack (action-form derivation, Cl(3)
Grassmann determinant, Hamiltonian limit), 2026-05-06.
**Authority role:** new top of the bridge gap science stack.

## 0. The unexamined assumption

All seven previously-exhausted attack routes (per
[`BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md))
shared a load-bearing assumption: **the framework's gauge action is
standard SU(3) Wilson** with character coefficients given by Bessel
determinants. Under that assumption, ⟨P⟩(β=6) ≈ 0.5934 is the famous
50-year-old open SU(3) lattice gauge plaquette evaluation problem, and no
framework-internal lever exists to close it at ε_witness ≈ 3×10⁻⁴ within
tractable cost.

The round-3 action-form-derivation agent established that this assumption
is **not justified by the audit chain**. Quoting verbatim from the
relevant retained notes (file paths and line numbers verified by direct
read):

From [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md):

> "the Wilson plaquette action `S = -beta Re Tr(U_plaq)` is not itself
> uniquely derived from Cl(3) structure — it is the standard Euclidean
> lattice gauge action, and its functional form (quadratic in F_µν,
> summed over plaquettes) is imported as the standard kinetic ansatz."

> Premises table: "Standard Wilson plaquette action ... retained
> convention, **not derived from Cl(3)**."

From [`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`](G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md):

> "The choice of the Wilson plaquette action form (Symanzik / improved
> actions remain outside this scope)."

From [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](G_BARE_RIGIDITY_THEOREM_NOTE.md):

> "the physical theory is the **Hamiltonian/operator theory**, not a
> path-integral regulator with an independent bare-action coefficient."

From [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md) Theorem
inputs:

> "3. **Wilson matching surface:** `beta = 2 N_c / g_bare^2`."

The Wilson form is INPUT (premise), not derived. The g_bare = 1 result is
conditional on Wilson being correct.

Additionally, from [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md):
the framework's only retained axioms are A1 (Cl(3) local algebra) and A2
(Z³ substrate). The staggered-Dirac realization (formerly axiom A3) and
the g_bare normalization (formerly axiom A4) are **open derivation gates**.
SU(3) gauge group emergence depends on the staggered-Dirac open gate plus
a deferred physical-color identification bridge per
[`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
(2026-05-04 audit verdict: `audited_renaming`).

**Therefore the four cluster lanes' bridge gap is not the famous open
SU(3) Wilson problem.** It is a different problem: compute ⟨P⟩(β=6)
under the framework's actually-derived gauge action, which has not yet
been identified.

## 1. The Cl(3)-native action candidate: heat-kernel

The Casimir-natural alternative to Wilson is the **heat-kernel action**:

```
P_β(U) = Σ_λ d_λ · exp(-β · C_2(λ) / 2) · χ_λ(U)
S_HK(U) = -log P_β(U)
```

This action has structural advantages over Wilson:

1. **Casimir is framework-derived.** The quadratic Casimir
   `C_2(p,q) = (1/3)(p² + pq + q² + 3p + 3q)` is forced by SU(3) Lie
   algebra, and `C_2(1,0) = 4/3` is exact-rational from the framework's
   retained [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
   via the Cl(3) trace form `Tr(T_a T_b) = δ_{ab}/2`.

2. **Wilson character coefficients have no Cl(3)-native motivation.**
   The Wilson `c_λ(β) = ∫ exp(β · (1/N) Re Tr U) χ_λ(U) dU` are Bessel
   determinants — natural objects in Wilson's specific 1974 formulation,
   but not derived from the framework's algebra.

3. **Heat-kernel is the canonical lattice-gauge analog of Brownian motion
   on the gauge manifold.** It's the "minimal" action choice that
   preserves the continuum limit while being Casimir-diagonal.

## 2. The HK time convention is not yet derived

A probe computation
([`scripts/probe_heat_kernel_su3_plaquette.py`](../scripts/probe_heat_kernel_su3_plaquette.py))
shows that heat-kernel single-plaquette ⟨(1/3) Re Tr U⟩ depends sharply
on the HK time convention `t_HK(β=6)`:

| Convention | t_HK at β=6 | ⟨P⟩_HK(6) | Notes |
|---|---:|---:|---|
| I: t = β | 6 | 0.018 | Literal Casimir-suppression weight |
| II: t = 1/β | 1/6 | 0.895 | Continuum-natural matching |
| III: t = N_c/β | 1/2 | 0.717 | Menotti-Onofri 1981 |
| **IV: t = 1** | **1** | **0.513** | **Canonical g_bare² = 1** |
| V: t = 2N_c²/β | 3 | 0.135 | Drouffe-Zuber matching |

For comparison:
- Wilson single-plaquette ⟨P⟩_W,1plaq(6) = 0.4225317396 (V=1 PF ODE certified)
- Lattice MC thermodynamic ⟨P⟩(6) ≈ 0.5934 (canonical comparator, NOT
  rigorous derivation input)

**Convention IV gives ⟨P⟩_HK = 0.513 — closer to the MC comparator
0.5934 than Wilson's 0.4225 is.** This is suggestive (not load-bearing)
that the framework's actually-derived single-plaquette value may sit in
the upper region of the [0.42, 0.59] band, narrowing the bridge gap
*before* any thermodynamic-limit calculation.

The convention dependence is not arbitrary — it reflects the framework's
canonical Cl(3) connection normalization. The right HK time is **forced
by the algebraic structure of g_bare = 1**, just as β = 6 was forced.
Determining it is a finite-dimensional algebraic problem, not the famous
open lattice problem.

## 3. The new-physics research target

**Question 1 (action-form derivation).** What gauge action does the
framework's axiomatic chain
- A1 (Cl(3) local algebra) +
- A2 (Z³ substrate) +
- canonical Cl(3) connection normalization (Tr(T_a T_b) = δ_{ab}/2) +
- staggered-Dirac realization (open gate, A3) +
- physical-color identification (deferred bridge)

force, when promoted to a path-integral measure on the link variables?

This is a derivation problem with finite-dimensional algebraic content.
Plausible answers:

- **Wilson** (current import): `S = -β · Re Tr U_p`. Bessel-determinant
  characters. ⟨P⟩(6) is the famous open problem.
- **Heat-kernel**: `S = -log P_t(U_p)` for some t = t(β) forced by
  canonical normalization. Casimir-natural. ⟨P⟩_HK(6) = exp(-2t/3) at
  single-plaquette level, closed form. Thermodynamic limit may also
  close in closed form due to Casimir-diagonal structure.
- **Manton**: `S = β · d²(U, I)` (geodesic distance squared). Different
  finite-β values from both above; same continuum limit.
- **Cl(3)-native volume-form**: minimal gauge-invariant curvature-square
  in the Cl(3)-induced volume measure. Possibly different from all of
  the above. Flagged as future direction in
  [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
  line 542.
- **Cl(3) ⊗ Cl(3) → Spin(6) ≅ SU(4) ⊃ SU(3) × U(1) embedding action**:
  the link variable lives in a larger group via tensor structure on
  adjacent sites. Different action functional. Not yet investigated.

**Question 2 (Cl(3)-native time t).** Conditional on heat-kernel being
the right form, what specific t = t(β) is forced by the canonical
Cl(3) normalization?

The standard candidates (I–V above) come from different physical
matchings. The framework's canonical normalization should pick one. The
right derivation chain is:
1. Cl(3) connection has canonical operator normalization Tr(T_a T_b) = δ_{ab}/2.
2. This induces a canonical metric on the gauge manifold.
3. Brownian motion on the gauge manifold with this metric runs at
   canonical time-rate t.
4. Match to Wilson at the continuum limit (small a) to extract t = t(β).
5. Evaluate at framework's β = 6.

If this chain closes, t is a specific framework-internal rational
expression (e.g., t = 1, or t = N_c/β = 1/2, etc), and ⟨P⟩(6) follows
in closed form.

**Question 3 (thermodynamic limit under HK action).**
Even if single-plaquette HK is closed-form, the four cluster lanes need
the THERMODYNAMIC ⟨P⟩(6) on a full lattice with multi-plaquette
correlations. Heat-kernel partition function on a lattice is also
character-diagonal:

```
Z_HK,Λ(β) = Σ_{λ on each plaquette} (Π_p d_{λ_p}) · exp(-β·Σ_p C_2(λ_p)/2) · (intertwiner contractions)
```

The Casimir-diagonal structure may make the thermodynamic limit MORE
tractable than Wilson's Bessel-determinant version, because the
β-dependence factorizes per plaquette.

## 4. Cross-validation from round-3 sister agents

- The **Grassmann determinant agent** independently recommended that
  "the framework's prediction must come through gauge-action *modification*
  not fermion-determinant modification" — which is exactly the angle in
  Question 1.

- The **Hamiltonian-limit agent** confirmed that retained primitives
  (RP, single-clock, Lieb-Robinson, per-site Cl(3) dim 2, Klein-four V)
  do NOT force a finite-dim H truncation, and that the obstruction is
  isomorphic to Perron-Jacobi underdetermination — i.e., the gauge
  sector's character truncation IS the missing primitive. **A
  Casimir-diagonal action like heat-kernel forces a specific natural
  truncation** (truncate at fixed C_2 cutoff, exponentially suppressed),
  resolving the Hamiltonian-limit obstruction simultaneously.

This is genuine cross-validation: three round-3 agents converge on
"the framework's gauge action is the missing primitive," not "the
framework's lever inside Wilson is the missing primitive."

## 5. Implications for previously-landed claims

- The seven exhausted routes consolidation note remains correct as a
  no-go on ⟨P⟩_Wilson(6). It does NOT exhaust ⟨P⟩_framework(6) under a
  different action.
- The industrial SDP battle plan
  ([`BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md`](BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md))
  is **demoted from primary path to fallback**. SDP closes Wilson at
  ε_witness, but Wilson may not be the framework's actual action — in
  which case SDP closes the wrong number.
- The four cluster lanes' downstream chain (u_0 = ⟨P⟩^(1/4), α_s(v) =
  α_bare/u_0², etc.) currently anchors on ⟨P⟩ = 0.5934. If the
  framework's actual derived action gives ⟨P⟩ ≠ 0.5934, the entire
  downstream chain shifts. Quantitative claims (α_s(M_Z) = 0.1180) would
  need re-evaluation under the derived action.
- The V=1 Picard-Fuchs ODE [`PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md)
  is for the **Wilson** single-plaquette integral. The HK single-plaquette
  has a DIFFERENT generating function (Casimir-suppressed sum, not
  Bessel-determinant) and would have a different ODE.

## 6. Concrete next research steps

In priority order:

### Step 1: Derive the canonical Cl(3) gauge metric (HIGHEST PRIORITY)
Trace from `Tr(T_a T_b) = δ_{ab}/2` (canonical normalization) →
gauge-manifold metric → canonical Brownian time rate. Compare to
literature (Menotti-Onofri, Drouffe-Zuber, Bonati-D'Elia).

**Deliverable:** a specific rational (or transcendental closed-form)
expression for `t_HK(β=6)`, with derivation chain rooted in Cl(3) +
canonical normalization.

### Step 2: Compute single-plaquette ⟨P⟩_HK(6) from derived t
Given Step 1's `t_HK(6)`, evaluate `⟨P⟩_HK,1plaq = exp(-2t_HK/3)`.
Compare to Wilson 0.4225 and MC 0.5934.

**Deliverable:** a specific closed-form `⟨P⟩_HK,1plaq(6)`, derived from
A1 + A2 + canonical normalization. This is the framework's actually-
derived single-plaquette plaquette value.

### Step 3: Derive thermodynamic ⟨P⟩(6) under HK action
For multi-plaquette HK partition function, Casimir-diagonal structure
factorizes the β-dependence. Investigate whether:
- a closed-form character-sum evaluation exists on infinite-volume
  3+1D, OR
- the cube-shell enumeration that gave β⁵/472392 for Wilson generalizes
  to HK with possibly closed-form all-order summation, OR
- an exact Schwinger-Dyson loop equation closes on the HK Casimir basis.

**Deliverable:** either a closed-form thermodynamic ⟨P⟩_HK(6), or a
sharp obstruction analogous to the Wilson no-go.

### Step 4: Cross-check against canonical-normalization audit
The framework's [`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md)
constrains the canonical normalization. Verify that the HK-derived
⟨P⟩_HK(6) is consistent with the canonical chain: `u_0 = ⟨P⟩^(1/4)`,
`α_s(v) = α_bare/u_0²`, etc.

If consistent: the bridge gap is closed in closed-form via the new
action.

If inconsistent: there's an additional structural constraint that
selects between Wilson and HK (or selects a third action). Identify it.

### Step 5: Apply to four cluster lanes
Once the framework's actual ⟨P⟩(6) is in closed form:
- α_s direct Wilson: re-derive with ⟨P⟩_framework(6); compare to PDG
  world average.
- Higgs mass: re-derive lattice-curvature ↔ (m_H/v)² with framework
  action; compare to PDG.
- Gauge-scalar bridge: the no-go's β⁶-completion freedom may collapse
  under HK because Casimir-diagonal structure pins higher orders.
- Koide-Brannen: same structural reduction.

If all four lanes close under the framework's derived action: the four
cluster lanes lift to retained tier, and the project's quantitative
claims become genuine derivations rather than conditional on admitted
imports.

## 7. Status

```yaml
actual_current_surface_status: new-physics research target identification
proposal_allowed: false
proposal_allowed_reason: |
  This note identifies an unexamined assumption (Wilson is imported, not
  derived) and frames the actual new-physics research target. It is not
  itself a derivation of the framework's gauge action. The numerical
  values from the heat-kernel probe are convention-dependent and are
  illustrative only — the actual derived value depends on Step 1's
  canonical Cl(3) gauge-metric derivation, which is the Step-1 research
  target.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
supersedes_path_decision_in: BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06
```

## 8. Cross-references

### Round-3 agent verdicts (2026-05-06)
- **Action-form derivation (Agent α):** POSITIVE — Wilson is admitted import per `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18`; SU(3) emergence requires open staggered-Dirac gate + deferred color bridge; heat-kernel is Casimir-native alternative
- **Cl(3) Grassmann determinant (Agent β):** NEGATIVE on closed-form effective measure (heavy-m: reduces to quenched at shifted β; chiral m→0: closed form fails) — but explicitly recommends gauge-action modification as the right angle
- **Hamiltonian limit (Agent γ):** NEGATIVE on retained primitives forcing finite-dim H — but identifies that gauge-sector character truncation IS the missing primitive (which heat-kernel provides naturally)

### Probe computation
- [`scripts/probe_heat_kernel_su3_plaquette.py`](../scripts/probe_heat_kernel_su3_plaquette.py)

### Existing framework structural inputs
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) — A1 + A2 only retained
- [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md) — C_2(1,0) = 4/3 retained
- [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md) — adjoint Casimir
- [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md) — Wilson-as-import documented
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md) — physical-color bridge deferred
- [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md) — per-site dim 2

### Related no-go / underdetermination notes
- [`BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md)
- [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md)
- [`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`](LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md)

### Demoted by this note
- [`BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md`](BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md) — primary → fallback

### Standard methodology references
- Menotti, P. & Onofri, E. (1981). "The action of SU(N) lattice gauge theory in terms of the heat kernel on the group manifold." Nucl. Phys. B 190, 288.
- Drouffe, J.-M. & Zuber, J.-B. (1983). "Strong coupling and mean field methods in lattice gauge theories." Phys. Rep. 102, 1.
- Bonati, C. et al. (2014, 2018) — modern heat-kernel SU(N) lattice studies
- Doran-Lasenby, "Geometric Algebra for Physicists" — Cl(3) structure references
