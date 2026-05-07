# Bridge Gap — Action-Form Uniqueness No-Go (Block 04)

**Date:** 2026-05-06
**Type:** named-obstruction no-go
**Claim type:** no_go
**Status:** branch-local no-go proposal: under the framework's current
retained primitive stack (A1+A2 + canonical Tr-form + per-site dim 2 +
A11 RP + single-clock + Lieb-Robinson + retained Casimir), the
action-form uniqueness question — does Cl(3)/Z³ select Wilson,
heat-kernel, Manton, or some other gauge action functional? — CANNOT
be resolved. The framework's derived action is action-form ambiguous;
distinct admissible actions (compatible with all current primitives)
give distinct ⟨P⟩(6) values at finite β.
**Authority role:** branch-local no-go proposal. Audit verdict and
effective status are set only by the independent audit lane.
**Loop:** bridge-gap-new-physics-20260506 (Block 04 / R4)
**Branch (intended):** physics-loop/bridge-gap-new-physics-block04-20260506 (PR_BACKLOG — cluster cap hit at Block 02)

## Question

Does the framework's current retained primitive stack uniquely select
the gauge action functional `S(U)`? In particular, does it force
**heat-kernel** `S_HK = -log P_t(U)` (Block 01-02 candidate) over
**Wilson** `S_W = -β · Re Tr U / N_c` (currently imported per
[`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md))?

## Answer

**NO.** The framework's current retained primitives do not uniquely
select an action-form. At least three distinct gauge actions
(Wilson, heat-kernel, Manton) are jointly compatible with:

- A1 (Cl(3) local algebra)
- A2 (Z³ substrate)
- Canonical Tr-form `Tr(T_a T_b) = δ_{ab}/2`
- Per-site Hilbert dim 2 (Cl(3) Pauli)
- A11 reflection positivity
- Single-clock evolution + Lieb-Robinson
- Retained Casimir `C_2(1,0) = 4/3`
- Continuum-limit consistency at small `a`

Each produces the same continuum limit `(1/2g²)∫Tr F² d⁴x` and the
same retained algebraic structure. They differ only in **finite-β
behavior**, including ⟨P⟩(β=6) values.

## A_min for this no-go

Same as Blocks 01-03. No new primitives.

## Setup: candidate action functionals

Three concrete actions consistent with the framework's primitives:

### Candidate I: Wilson

```
S_W(U_p) = β · (1 - (1/N_c) Re Tr U_p), β = 2 N_c / g_bare² = 6.            (W)
```

Currently imported per `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18`
explicit "retained convention, not derived from Cl(3)."

### Candidate II: Heat-kernel

```
S_HK(U_p) = -log P_t(U_p), t = g_bare² = 1 (Block 01 derived).               (HK)
```

Casimir-diagonal: `P_t(U) = Σ_λ d_λ exp(-t·C_2/2) χ_λ(U)`. Uses
retained `C_2`. ⟨P⟩_HK,1plaq(6) = exp(-2/3) ≈ 0.5134 (Block 02).

### Candidate III: Manton

```
S_M(U_p) = β · d²(U_p, I), d(·,·) = bi-invariant geodesic distance.        (M)
```

Uses the canonical bi-invariant metric (Block 01 Step 1). For U near
identity: `d²(U, I) = |X|² + O(X⁴)` matching Wilson and HK at leading
order. Differs at higher orders.

## Step 1: All three pass continuum-limit matching

For `U = exp(iX)` with `X` small:

| Action | Small-X expansion | Continuum limit |
|---|---|---|
| Wilson | `(β/(4 N_c)) |X|² + O(X⁴)` (Block 01 eq. (8)) | `(1/2g²) Tr F² + O(a²)` |
| Heat-kernel | `|X|²/(2 t) + O(X⁴)` (Block 01 eq. (13)) | `(1/2g²) Tr F² + O(a²)` |
| Manton | `(β/2) |X|² + O(X⁴)` (Helgason-style geodesic expansion) | `(1/2g²) Tr F² + O(a²)` |

Setting `(β/(4 N_c)) = 1/(2t) = (β_M / 2)` matches all three at leading
order. At canonical `g_bare = 1, β = 6`:

```
β_W = 6, t_HK = 1, β_M = 1/3.                                              (Step 1.1)
```

All three actions are consistent with A1+A2+canonical Tr-form +
continuum-limit matching at the framework's canonical evaluation point.
**No primitive in the retained stack distinguishes them.**

## Step 2: Higher-order expansions differ

For `U = exp(iX)` with `X` not infinitesimal, the actions differ at
O(X⁴) and beyond. Standard SU(N) results (Drouffe-Zuber 1983,
Menotti-Onofri 1981):

| Action | O(X⁴) coefficient |
|---|---|
| Wilson | proportional to `Tr(X⁴)` and `(Tr X²)²` with specific Wilson coefficients |
| Heat-kernel | proportional to same monomials with different (Brownian-motion-derived) coefficients |
| Manton | proportional to same monomials with geodesic-curvature coefficients |

These differences propagate to **distinct finite-β plaquette
expectations**:

```
⟨P⟩_W(β=6) ≠ ⟨P⟩_HK(t=1) ≠ ⟨P⟩_M(β=1/3) at finite β.                       (Step 2.1)
```

In particular, single-plaquette evaluations:

| Action | ⟨P⟩_1plaq(canonical) | Source |
|---|---|---|
| Wilson | 0.4225317396 | V=1 PF ODE certified |
| **Heat-kernel** | **0.5134171190 = exp(-2/3)** | **Block 02** |
| Manton | (uncomputed; bracketed by HK and Wilson at fixed β-matching) | not computed in this loop |

## Step 3: Naturality arguments — suggestive, not tight

Several arguments suggest HK is the most "Cl(3)-native" action, but
none rises to a uniqueness theorem under the no-new-axiom rule:

### Naturality argument (a): Casimir-diagonal under retained Tr-form

HK uses the Casimir `C_2(λ) = Σ_a (T_a)² eigenvalue on irrep λ` directly.
This Casimir IS retained (`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02`)
and follows from the canonical Tr-form (`Tr(T_a T_b) = δ_{ab}/2`) as a
direct algebraic consequence. Wilson's Bessel-determinant character
coefficients `c_λ(β)` are NOT direct algebraic consequences of Tr-form
— they require defining `exp(β · Re Tr U / N_c)` and computing
characters, which is an external functional choice.

**But:** Wilson's coefficients can ALSO be expressed in terms of
Casimirs (via the integral representation of Bessel determinants). So
"Casimir-diagonal" is a cleaner formal property of HK, not a uniqueness
selector.

### Naturality argument (b): Brownian-motion uniqueness on Riemannian manifold

On a Riemannian manifold with metric `g`, the heat semigroup `exp(t·Δ_g)`
is **uniquely determined** by `g` (no convention freedom). Brownian motion
is the canonical diffusion generator. For the canonical Tr-form metric,
HK is the canonical heat semigroup.

**But:** "the canonical heat semigroup" doesn't translate directly to
"the canonical lattice gauge action." A lattice gauge action is a
functional `S: SU(N) → ℝ` of the link variables; Wilson, HK, and Manton
are all valid functionals. Their "canonicity" depends on what criterion
is being optimized.

### Naturality argument (c): Symanzik improvement

Standard Symanzik analysis: improved actions reduce O(a²) lattice
artifacts. HK has specific O(a²) coefficients; Wilson has different
ones; Manton has yet different ones. The framework's primitives don't
specify a Symanzik-improvement criterion that selects one over the
others.

## Step 4: Why this is a STRUCTURAL no-go, not a research-effort gap

The action-form ambiguity is structural because:

1. **All three actions use only retained primitives.** Wilson's
   functional `Re Tr U` is a Lie-algebra-level construction; HK uses
   retained Casimir; Manton uses canonical metric. None requires a
   new axiom.

2. **All three give the same continuum limit.** The `a → 0` matching
   at leading order is identical. There's no continuum-limit lever
   distinguishing them.

3. **The differences are at finite β** = lattice scale = the framework's
   evaluation point. Finite-β evaluation is exactly where the famous
   open lattice problem lives. There's no retained primitive that pins
   the finite-β coefficient structure tightly enough to force one
   action over others.

4. **The no-new-axiom rule** (per skill protocol) forbids enlarging the
   axiom stack to break the ambiguity.

## Theorem 4 (Block 04 deliverable: NO-GO)

**Theorem (T4, no-go).** Under the framework's current retained
primitive stack (A1+A2 + canonical Tr-form + per-site dim 2 + A11 RP +
single-clock + Lieb-Robinson + retained Casimir + g_bare = 1 open
gate), the gauge action functional cannot be uniquely selected from
{Wilson, heat-kernel, Manton}. All three are jointly compatible with
all retained primitives + continuum-limit matching. They give DISTINCT
finite-β ⟨P⟩(6) values, and the difference structure cannot be
resolved without enlarging the axiom stack or admitting an additional
non-derivation convention.

**Proof.** Steps 1-4. ∎

## Consequence for the four cluster-obstruction lanes

The four cluster lanes (yt_ew M, gauge-scalar bridge, Higgs mass scalar
normalization, Koide-Brannen phase) per
[`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`](LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md)
all anchor on the framework's gauge plaquette evaluation. Under T4's
no-go, the lanes' downstream quantitative claims are **range-bounded**
by the action-form ambiguity:

| Lane | Wilson value | HK value (Block 02 1-plaq, thermo open) | Range |
|---|---|---|---|
| `u_0 = ⟨P⟩^(1/4)` | 0.4225^(1/4) = 0.806 (1-plaq) | 0.5134^(1/4) = 0.847 (1-plaq) | ~5% range |
| `α_s(v) = α_bare/u_0²` | scaled by u_0² ~ 0.65 | scaled by u_0² ~ 0.72 | ~10% range |

The ~5-10% action-form range exceeds ε_witness ~ 3×10⁻⁴ by ~150-300×.
Until action-form uniqueness is closed, the four cluster lanes'
quantitative claims are **structurally ambiguous at the action-form
level**, not just at the famous-open-problem level.

## Status, scope, and what this does NOT close

```yaml
actual_current_surface_status: named-obstruction no-go
target_claim_type: no_go
conditional_surface_status: |
  Conditional on:
   (a) the no-new-axiom rule (no extension to A1+A2);
   (b) the framework's current retained primitive stack as enumerated
       in Step 4 above;
   (c) the candidate action set {Wilson, heat-kernel, Manton} as a
       representative finite enumeration (other candidates such as
       Cl(3)-volume-form or Cl(3)⊗Cl(3)→SU(4) tensor actions might
       extend the no-go but do not weaken it).
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  Theorem (T4) is a structural no-go on action-form uniqueness given
  the current retained primitive stack. It is reusable negative
  evidence: future cycles encountering "is action X the framework's
  derived action?" should cite this no-go and pivot to either
  (i) governance reclassification (admit a specific action as scheme
  convention with narrow non-derivation role) or (ii) a new structural
  primitive that pins action-form (which would be a new axiom — currently
  forbidden under no-new-axiom rule).
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## What this closes

- The action-form uniqueness question is formally retired as a Resolution-A
  closure path under current primitives.
- The four cluster-obstruction lanes' downstream quantitative range-
  bounding is named explicitly: ~5-10% range across action choices,
  far exceeding ε_witness.
- Reusable negative evidence: future cycles can cite this no-go rather
  than re-deriving the action-form ambiguity from each candidate
  comparison.

## What this does NOT close

- The bridge gap itself. The action-form ambiguity adds a structural
  layer beyond the famous open lattice problem, but does not retire it.
- The thermodynamic ⟨P⟩_HK(6) under the heat-kernel candidate (Block 03
  named obstruction).
- Possible escape routes:
  - **Governance reclassification (Resolution B)**: admit a specific
    action (e.g., Wilson) as scheme convention with narrow non-derivation
    role. Per
    [`BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md`](BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md)
    + new-physics opening, Resolution B remains a defensive labeling
    option even though the user explicitly de-prioritized it.
  - **Cl(3) ⊗ Cl(3) → Spin(6) ≅ SU(4) embedding**: if the framework's
    actually-derived gauge group is SU(4) ⊃ SU(3) × U(1) (not pure
    SU(3)), the action analysis changes entirely. This is exploratory
    and not yet investigated. (Future block / future loop.)
  - **Externally-supplied non-perturbative input** (industrial SDP at
    L_max ≥ 22 with Mosek): closes the famous open problem at
    ε_witness for ONE specific action choice. Per
    [`BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md`](BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md)
    this is a $510k / 15mo engineering bet, demoted to fallback by
    the new-physics opening but viable.

## Cross-references

- Predecessor (this loop): [`BRIDGE_GAP_HK_THERMODYNAMIC_STRETCH_NOTE_2026-05-06.md`](BRIDGE_GAP_HK_THERMODYNAMIC_STRETCH_NOTE_2026-05-06.md) (Block 03 stretch + named obstruction)
- Block 02 deliverable: [`BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md`](BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md) (HK 1-plaq closed form)
- Block 01 deliverable: [`BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md`](BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md) (HK time)
- New-physics opening: [`BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md`](BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md)
- Wilson-as-import: [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
- Sister no-gos: [`BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md)
- Standard methodology: Drouffe-Zuber 1983 Phys. Rep. 102 ("Strong coupling and mean field methods in lattice gauge theories"); Menotti-Onofri 1981 Nucl. Phys. B190; Helgason 1978 (bi-invariant metrics)
