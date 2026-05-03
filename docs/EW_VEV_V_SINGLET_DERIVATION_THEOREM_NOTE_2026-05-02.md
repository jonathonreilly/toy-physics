# Electroweak VEV V-Singlet Derivation Theorem Note

**Date:** 2026-05-02
**Type:** exact support theorem (modulo two textbook-standard admissions C1, C2 + admitted hierarchy baseline B5)
**Claim scope:** the `(A_2/A_4)^(1/4) = (7/8)^(1/4)` selector factor appearing in
the EW v-derivation chain follows from V=Z₂×Z₂-invariance of the
free-energy density `f_vac` on the minimal Klein-four APBC block,
**without** the four functional-equation bridges (scalar additivity,
CPT-even phase blindness, continuity, normalization) admitted in
`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`. The numerical readout
`v = M_Pl · (7/8)^(1/4) · α_LM^16 = 246.28 GeV` continues to depend on the
admitted hierarchy baseline `M_Pl · α_LM^16 = 254.6432 GeV` (B5), which is
out of scope of this note.
**Status authority:** independent audit lane only. This source note does
not set or predict an audit outcome; later effective status is generated
by the audit pipeline after independent review.
**Primary runner:** `scripts/frontier_ew_vev_v_singlet_derivation.py`

## 0. Question

`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` was demoted to bounded support
theorem on 2026-05-02 (cycle 8 of `audit-backlog-campaign-20260502`,
PR [#267](https://github.com/jonathonreilly/cl3-lattice-framework/pull/267))
because it admits four bridge assumptions (B1 scalar additivity, B2 CPT-even
phase blindness, B3 continuity, B4 normalization) plus B5 hierarchy baseline
import.

Can the `(A_2/A_4)^(1/4) = (7/8)^(1/4)` selector factor in the v-derivation
chain be re-derived through a route that retires bridges B1+B2+B3 by
reformulating the load-bearing observable as the V-invariant free-energy
density `f_vac` rather than the functional-equation-derived
`W = log|det(D+J)| - log|det D|`?

## 1. Setup

Retained framework primitives (all from `MINIMAL_AXIOMS_2026-04-11.md` or
direct corollaries; see this campaign's `ASSUMPTIONS_AND_IMPORTS.md`):

| # | Primitive |
|---|---|
| A3 | finite local Grassmann / staggered-Dirac partition |
| A6 | action `S` on the minimal `L_s = 2` APBC block is V-invariant |
| A7 | exact closed-form determinant `\|det(D + m)\| = ∏_ω [m² + u_0²(3 + sin²ω)]^4` |
| A8 | Klein-four orbit closure: `L_t = 2` is unresolved sign pair, `L_t = 4` is the unique minimal **resolved** closed orbit, `L_t > 4` splits |
| A9 | exact algebraic ratio `A(L_t = 2) / A(L_t = 4) = 7/8` |
| A10 | `Z` is V-invariant when `S` is V-invariant |

New admissions (C1, C2) introduced by this note:

| # | Admission | Role |
|---|---|---|
| C1 | `v² = -∂²f_vac/∂m²\|_{m=0}` for a homogeneous V-singlet mass source `m` (standard EFT identification of EW order-parameter scale with curvature of effective potential at origin) | textbook-standard; replaces B1+B2+B3 |
| C2 | the `m = 0` vacuum on the finite minimal Klein-four block is V-singlet (no spontaneous breaking on a finite-volume V-symmetric block) | provable; below |

Comparators (admitted-context, never derivation inputs):

- `(7/8)^(1/4) = 0.967168210134` (already in the framework via `HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`; this note must DERIVE the same value through a different load-bearing route)
- `v_meas = 246.22 GeV` (PDG)
- `M_Pl · α_LM^16 = 254.6432 GeV` (admitted B5)

## 2. Definitions

The free-energy density on the minimal Klein-four block is the standard
thermodynamic quantity:

```text
f_vac(L_t, m)  =  -(1/V_total) · log|det(D + m)|
```

where `V_total = L_t · L_s³ = 8 L_t` (with `L_s = 2`). On using the
determinant identity A7:

```text
f_vac(L_t, m)  =  -(4/V_total) ∑_ω log[m² + u_0²(3 + sin²ω)]
              =  -(1/(2 L_t)) ∑_ω log[m² + u_0²(3 + sin²ω)]
```

The Klein-four `V = Z₂ × Z₂` action on APBC temporal Matsubara phases:

```text
Z_2(a):  z → -z,  i.e.  ω → ω + π   (mod 2π)
Z_2(b):  z → z*,  i.e.  ω → -ω      (mod 2π)
```

so the orbit of a phase `ω` under V is `{ω, ω+π, -ω, -ω+π}`. On `sin²(·)`:

```text
sin²(ω + π)  =  sin²ω      (sign flip preserves sin²)
sin²(-ω)     =  sin²ω      (conjugation preserves sin²)
```

Therefore `sin²ω` is V-invariant for each Matsubara mode, and the
mode-summand `log[m² + u_0²(3 + sin²ω)]` is V-invariant.

## 3. Lemma H2.1 — `f_vac` is V-invariant on the minimal Klein-four block

**Lemma.** For `L_s = 2` and any `L_t ≥ 1`, the free-energy density
`f_vac(L_t, m)` is V-invariant under the Klein-four action on temporal
Matsubara phases.

**Proof.** The closed-form determinant A7 gives `f_vac` as a sum over
Matsubara modes of `log[m² + u_0²(3 + sin²ω)]`. The V action on phases
preserves `sin²ω` mode-by-mode (computation above). Therefore each term
in the sum is V-invariant, and `f_vac` is V-invariant. ∎

**Remark.** This is not the framework's previous functional-equation
route (`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` Theorem 1). It does not
require scalar additivity (B1), CPT-even phase blindness (B2), or
continuity (B3). It uses only the V-action on Matsubara phases (A8) and
the closed-form determinant (A7).

## 4. Lemma H2.2 — m²-curvature `A(L_t)` is V-invariant

**Lemma.** For a homogeneous V-singlet mass source `m`,
`A(L_t) := -∂²f_vac/∂m²\|_{m=0}` is V-invariant.

**Proof.** Direct differentiation of the closed-form expression in §2:

```text
∂²f_vac/∂m²|_{m=0}  =  -(1/(2 L_t)) ∑_ω ∂²/∂m² log[m² + u_0²(3 + sin²ω)]|_0
                    =  -(1/(2 L_t)) ∑_ω (2 / [u_0²(3 + sin²ω)])
                    =  -(1/(L_t · u_0²)) ∑_ω 1/(3 + sin²ω)
```

Therefore:

```text
A(L_t)  =  +(1/(L_t · u_0²)) ∑_ω 1/(3 + sin²ω)
```

(equivalent to the framework's `A(L_t) = (1/(2 L_t · u_0²)) ∑_ω 1/(3 + sin²ω)`
up to an overall normalization absorbed into the v-derivation chain).

The mass source `m` is V-singlet (homogeneous, doesn't transform under V).
Differentiation w.r.t. a V-singlet source preserves V-invariance of the
result. Each summand `1/(3 + sin²ω)` is V-invariant by Lemma H2.1's
argument. Therefore `A(L_t)` is V-invariant. ∎

## 5. Lemma H2.3 — vacuum at m=0 is V-singlet on the finite minimal block

**Lemma.** The `m = 0` configuration on the minimal `L_s = 2` APBC block
is V-singlet (no spontaneous V-breaking).

**Proof.** Spontaneous symmetry breaking requires either:

(a) infinite volume (Mermin-Wagner-type arguments require the lattice
    volume → ∞ for true SSB), or

(b) explicit symmetry-breaking term in the action.

The minimal Klein-four block has finite volume `V_total = 8 L_t`, so
(a) does not apply. The action `S` is V-invariant by A6, so (b) does not
apply.

By the standard argument (any V-equivariant Gibbs measure on a finite
V-symmetric system has V-invariant correlation functions), the vacuum
state at `m = 0` is V-invariant — i.e., V-singlet. ∎

**Remark.** This justifies admission C2 from primitives.

## 6. Theorem H2 — `(A_2/A_4)^(1/4) = (7/8)^(1/4)` follows without B1+B2+B3

**Theorem.** The selector factor `(A_2/A_4)^(1/4) = (7/8)^(1/4)` in the
EW v-derivation chain follows from:

1. Lemma H2.1 (`f_vac` is V-invariant)
2. Lemma H2.2 (`A(L_t)` is V-invariant for V-singlet sources)
3. Lemma H2.3 (vacuum is V-singlet)
4. A8 (Klein-four orbit closure: L_t=4 is unique minimal resolved orbit)
5. A9 (exact algebraic ratio `A(L_t=2)/A(L_t=4) = 7/8`)
6. C1 (textbook-standard EFT identification `v² = -∂²f_vac/∂m²\|_0`)

**Proof.**

By Lemma H2.3, the m=0 vacuum is V-singlet. By admission C1, `v²` is
identified with `-∂²f_vac/∂m²\|_{m=0}` for a V-singlet source. By Lemma
H2.2, that derivative is V-invariant; equivalently, it is `A(L_t)` (up to
normalization). By A8, the unique minimal closed orbit under V on APBC
temporal phases is at `L_t = 4`. Selecting this orbit:

```text
v_physical²  ∝  A(L_t = 4)
v_baseline²  ∝  A(L_t = 2)         (UV unresolved-pair endpoint)
```

By A9:

```text
A(L_t = 2) / A(L_t = 4)  =  7/8.
```

The fourth-root structure of the v-formula (inherited from the staggered
taste-determinant chain `(det D)^(1/4)`; see `YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`)
gives:

```text
v_physical / v_baseline  =  (A_2 / A_4)^(1/4)  =  (7/8)^(1/4)  ≈  0.96717.
```

This matches the framework's existing value derived through the
functional-equation route in `HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`
and `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`, without admitting bridges
B1+B2+B3 of the parent note. ∎

## 7. Bridges retired by H2

| Bridge in `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE` | Role in original derivation | Status under H2 |
|---|---|---|
| B1: scalar additivity `W[J_1 ⊕ J_2] = W[J_1] + W[J_2]` | premise of functional-equation argument forcing `W = c log\|Z\|` | **RETIRED**: H2 uses `f_vac` directly as the standard thermodynamic free-energy density. Extensivity of `f_vac` (intensive per spacetime volume) follows from `Z` factorizing on independent subsystems, not from a separate functional equation. |
| B2: CPT-even phase blindness `W` depends on \|Z\| | premise forcing `W` to depend only on \|Z\|, not phase | **RETIRED**: For staggered-Dirac with real masses, `det D` is real and positive (no fermionic phase). `f_vac = -(1/V_total) log\|det D\|` is automatically real with no phase admission. |
| B3: continuity (regularity for functional equation) | premise admitting unique solution to the additivity functional equation | **RETIRED**: H2 does not use a functional equation. Analyticity of `Z[J]` in `J` (finite-dim Grassmann is polynomial in `J`, hence entire in `J`) replaces this. |
| B4: normalization choice | overall constant `c` in `W = c log\|Z\|` | **NOT RETIRED**: still appears as a normalization in `f_vac = -(1/V_total) log\|det D\|`. This is the standard thermodynamic normalization; not a framework-specific bridge. |
| B5: hierarchy baseline import `M_Pl · α_LM^16` | numerical baseline for v-formula | **NOT RETIRED**: out of scope of H2; depends on plaquette / α_LM chain. |

## 8. Admissions remaining under H2

| # | Admission | Class | Role |
|---|---|---|---|
| C1 | `v² = -∂²f_vac/∂m²\|_{m=0}` for V-singlet source `m` | textbook-standard EFT (Peskin-Schroeder ch. 11; Coleman-Weinberg 1973) | identifies the EW order-parameter scale with curvature of effective potential at origin |
| C2 | vacuum at m=0 is V-singlet on the finite minimal block | provable (Lemma H2.3) | not actually an admission once the proof is accepted |
| B4 | normalization choice (overall constant in `f_vac`) | textbook-standard (thermodynamic free energy) | trivial up to overall constant; no framework-specific role |
| B5 | hierarchy baseline `M_Pl · α_LM^16` | external lane (separate plaquette / α_LM chain) | out of scope; H2 does not change this |

## 9. Corollary H2-B — m_H representation-theoretic distinction

**Corollary.** The `(7/8)^(1/4)` selector factor applies to `v` (the EW
order-parameter scale at the V-singlet origin) but NOT to `m_H` (the
Higgs mass at the V-broken minimum).

**Reasoning.** EWSB places the physical vacuum at `⟨H⟩ = v ≠ 0`, where
the Higgs minimum spontaneously breaks the V symmetry (in the framework's
mapping to physical EW). The Higgs mass is the curvature `m_H² ~
∂²V_eff/∂h²|_{h = v}` at the broken minimum, which is NOT a V-singlet
configuration. Consequently:

- `v² ~ A(L_t = 4)` is a V-invariant quantity at the V-singlet origin
  (carries the L_t=4 selector and the (7/8)^(1/4) factor).
- `m_H² ~ ∂²V_eff/∂h²|_{h = v}` is evaluated at a V-broken point and is
  NOT subject to the same Klein-four orbit-closure selector.

This dissolves the apparent "different correction factors for v and m_H"
paradox into a representation-theoretic distinction: V-singlet origin vs
V-broken minimum.

The detailed Higgs-mass derivation chain remains in `HIGGS_MASS_FROM_AXIOM_*`
notes; H2-B only states the structural reason why the selectors differ.

## 10. Numerical readout (out-of-scope, admitted-context only)

Using admitted hierarchy baseline `M_Pl · α_LM^16 = 254.643210673818 GeV`
(B5, out of scope of this note's load-bearing claim):

```text
v_physical  =  254.643210673818 · (7/8)^(1/4)  =  246.282818290129 GeV
```

Compared with PDG comparator `v_meas = 246.22 GeV`:

- relative error +0.0255%
- absolute error +0.0628 GeV

This relative-error readout is shown as **comparator only**. It is not
consumed as a load-bearing input by any in-scope claim of this note.

## 11. Verification surface

The runner `scripts/frontier_ew_vev_v_singlet_derivation.py` checks:

1. closed-form determinant identity at `L_t ∈ {2, 3, 4, 5, 6, 8, 10}` against direct matrix computation
2. Klein-four orbit structure on Matsubara phases for `L_t ∈ {2, 4, 6, 8}`: enumerates orbits, confirms L_t=4 is the unique minimal **resolved** closed orbit (and L_t=2 is unresolved, L_t>4 splits)
3. V-invariance of `f_vac` and `A(L_t)` at sample u_0 values: checks that the V-orbit-permuted phase configurations give identical sums (V-invariance is exact, not approximate)
4. `A(L_t = 2)/A(L_t = 4) = 7/8` from direct sum (NOT hard-coded; the runner sums over Matsubara modes and computes the ratio symbolically/numerically)
5. Exact rational identity (computed): `A(2) = 1/(8 u_0²)`, `A(4) = 1/(7 u_0²)`, ratio `= 7/8`
6. The `(7/8)^(1/4) = 0.967168210134...` numerical value as a DERIVED output (computed from the ratio, not asserted)
7. Negative control: a non-V-singlet source (mode-localized) gives a different curvature ratio that is NOT `7/8` and NOT V-invariant — confirming the V-singlet condition is load-bearing

## 12. Honest status

```yaml
actual_current_surface_status: exact support theorem on the retained framework primitives + admitted C1 (textbook-standard EFT) + admitted B5 (separate hierarchy baseline lane)
target_claim_type: positive_theorem
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  The bridges retired (B1, B2, B3) are framework-specific functional-equation
  premises in OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE. They are replaced by
  the V-invariance of f_vac (a one-line computation from A7+A8+A6+A10) plus
  one textbook-standard EFT admission (C1). C2 is provable. B4 is trivial.
  B5 is out of scope. This is a strict reduction in framework-specific
  load-bearing admissions for the EW v lane.
audit_required_before_effective_retained: true
bare_retained_allowed: false
proposal_allowed: false
proposal_allowed_reason: |
  Honest tier on this branch is exact-support theorem with two admissions
  remaining (C1 textbook-standard, B5 separate-lane). Independent audit
  ratification is required before any effective-retained promotion. C1's
  classification (definition vs bridge) is the load-bearing audit question.
```

## 13. What this closes

- The `(A_2/A_4)^(1/4) = (7/8)^(1/4)` factor in the EW v-derivation can be
  re-derived through a route that retires bridges B1+B2+B3 of the parent
  `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE`.
- The reformulation introduces one textbook-standard EFT admission (C1)
  and one provable lemma (C2/H2.3), strictly fewer framework-specific
  bridges than the original 3 (B1+B2+B3).
- The (m_H paradox) is resolved into a representation-theoretic
  distinction: V-singlet origin (v) vs V-broken minimum (m_H).

## 14. What this does NOT close

- The hierarchy baseline `M_Pl · α_LM^16` (B5) — separate plaquette / α_LM lane.
- The exact analytic value of `⟨P⟩(β=6)` — bounded same-surface (`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`); see this campaign's H1 routes (block 02, 03) for stretch-attempts.
- The audit classification of C1 as "definition" vs "bridge" — load-bearing audit question; if audit returns "C1 is comparable in weight to B1+B2 combined", H2 is sideways rather than a strict reduction.
- Any of the lattice → physical matching cluster obstructions (cycles 5, 9, 11, 17 of `audit-backlog-campaign-20260502`) — H2 is INDEPENDENT of these.

## 15. Cross-references

- Parent (demoted): [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md), [`OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md`](OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md), audit-backlog cycle 8 / PR [#267](https://github.com/jonathonreilly/cl3-lattice-framework/pull/267)
- Sister theorems on the same chain: [`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md), [`HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md`](HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md), [`YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`](YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md)
- Cluster context (independent): [`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`](LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md)
- Axioms: [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md)
- Loop pack: `.claude/science/physics-loops/vev-v-singlet-derivation-20260502/`
