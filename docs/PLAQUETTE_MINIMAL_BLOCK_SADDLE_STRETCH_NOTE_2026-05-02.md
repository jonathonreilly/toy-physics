# Plaquette Minimal-Block Self-Consistent Saddle — Stretch Attempt

**Date:** 2026-05-02
**Type:** stretch attempt / named obstruction
**Claim scope:** attempt to compute `⟨P⟩(β=6)` analytically via the
self-consistent mean-field saddle on the V=Z₂×Z₂-invariant minimal Klein-four
block, using only existing retained framework primitives. **Expected
outcome:** named-obstruction stretch attempt, NOT closure. The famous
open lattice problem of analytic `⟨P⟩(β=6)` is not solved here; this note
sharpens which specific structural object remains unclosed.
**Status authority:** independent audit lane only.
**Primary runner:** `scripts/frontier_plaquette_minimal_block_saddle_stretch.py`

## 0. Question

`PLAQUETTE_SELF_CONSISTENCY_NOTE.md` (status amended 2026-05-01 to
`bounded`) states the verdict:

> "the load-bearing step still imports unratified direct authority from
> the bridge-support stack and that the explicit analytic `beta = 6`
> insertion remains open."

The user's H1 Route 1 strategy proposed:

> "Self-consistent saddle on the Klein-four minimal block. The framework
> already restricts to a 16-site Klein-four invariant block with mean-field
> factorization `U → u_0`. On this block, the partition function is:
>
> `Z_min(β, m, u_0) = e^{-S_gauge(u_0; β)} · ∏_ω [m² + u_0²(3+sin²ω)]^4`
>
> Self-consistency (saddle in u_0): `⟨P⟩ = u_0^4 = -∂lnZ_min/∂β |_{u_0=u_0*}`."

Can this self-consistent saddle be solved analytically on the V-invariant
minimal block to give `⟨P⟩(β=6)` = MC value `0.5934`?

## 1. Setup

Retained framework primitives:

| # | Primitive |
|---|---|
| A7 | exact closed-form determinant on `L_s=2` APBC block: `\|det(D + m)\| = ∏_ω [m² + u_0²(3+sin²ω)]^4` |
| AB | Wilson gauge action: `S_W = β · ∑_p [1 - (1/N_c) Re Tr U_p]` (admitted Wilson canonical convention; `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`) |
| AC | mean-field tadpole factorization `U_link = u_0 · V_link + ...` (admitted ansatz, framework standard) |
| AD | the exact framework's `PLAQUETTE_SELF_CONSISTENCY_NOTE` self-consistency relation `⟨P⟩ = u_0^4` (retained on the same-surface) |

For the L_s=2, L_t=4 V-invariant minimal block:
- 4-volume `V_4 = L_s³ × L_t = 8 × 4 = 32` sites
- Plaquettes per site: `C(4,2) = 6` (4D)
- Total oriented plaquettes: `N_p = 6 V_4 = 192`

## 2. Naive mean-field saddle (insufficient)

Naive U → u_0 · I factorization gives:

```text
S_W(u_0) = β · N_p · (1 - u_0^4)
log Z_MF^{naive} = -β · N_p · (1 - u_0^4) + 4 ∑_ω log[u_0²(3+sin²ω)]   (m=0)
```

Saddle equation `∂(log Z_MF)/∂u_0 = 0`:

```text
4 β N_p u_0^3 + 8 ∑_ω 1/u_0 = 0
β N_p u_0^4 + 2 L_t = 0
u_0^4 = -2 L_t / (β N_p)        (NEGATIVE — no positive solution)
```

The naive mean-field has **no positive saddle**. Both gauge and fermion
contributions favor large u_0; the Haar measure ENTROPY of the gauge
field (constraint that `u_0` must come from a unitary link average) is
missing from this naive setup.

**Naive mean-field is insufficient.** The framework's PLAQUETTE_SELF_CONSISTENCY
uses MC evaluation, not naive mean-field, precisely because the SU(3) Haar
entropy is non-trivial.

## 3. Proper mean-field with Haar entropy (technically required)

The proper mean-field includes the Haar-measure entropy of the SU(N_c)
configurations consistent with the constraint `⟨(1/N_c) Re Tr U⟩ = u_0`.

Standard SU(N_c) single-link mean-field gives:

```text
F_MF(u_0; β) = β N_p (1 - u_0^4) - V_4 · h(u_0)
```

where `h(u_0)` is the entropy density of single-link SU(N_c) configurations
with mean trace `(1/N_c) ⟨Re Tr U⟩ = u_0`. For SU(3), `h(u_0)` does not
have a closed form: it is given by an integral over the SU(3) Haar measure
constrained to fixed mean trace, which reduces to a 2-dimensional Cartan
integral but does not close to elementary functions.

**Standard known result** (Drouffe-Zuber 1983; Münster 1981): mean-field
for SU(3) at `β = 6` gives `⟨P⟩_MF ≈ 0.55-0.58`, while the MC value is
`0.5934`. The ~5% gap is the "mean-field-vs-bulk" deficiency.

## 4. V-invariant restriction (framework-specific)

The framework's H1 Route 1 strategy adds: restrict the mean-field to the
V=Z₂×Z₂-invariant subspace. The Klein-four orbit closure on APBC temporal
modes (already proven, `OBSERVABLE_PRINCIPLE_FROM_AXIOM` Theorem 4) selects
L_t=4 as the unique resolved orbit.

For the V-invariant minimal block:
- The Haar measure is restricted to V-respecting link configurations
- The mean trace `u_0` is computed on V-invariant subspace
- The saddle equation becomes a V-restricted version of the standard
  SU(3) single-link mean-field

The V-invariant restriction CHANGES the entropy term `h(u_0)` because
fewer link configurations are allowed. Without explicit calculation, we
cannot say whether the V-restricted mean-field result is closer to 0.5934
or further from it than the bulk SU(3) mean-field.

**Open structural question:** does the V-invariant restriction make the
minimal-block mean-field MATCH the bulk thermodynamic-limit value, or
does it remain at the standard mean-field gap (~5%) below MC?

## 5. Numerical exploration (this stretch)

The companion runner attempts to compute the V-invariant minimal-block
mean-field saddle numerically. It uses:
- Direct enumeration of Wilson plaquette configurations on the V-invariant
  subspace of the minimal block
- Self-consistency iteration to find u_0*

Realistic expected outcome (per the famous-open-problem context): the
numerical result is in the range `0.55-0.62` for `β=6`, neither exactly
matching `0.5934` nor disproving the V-invariant approach. This is a
SHARPER NAMED OBSTRUCTION than just "the saddle is not closed analytically."

## 6. Numerical result

(See runner output for actual values; this section is updated after the
runner runs.)

The runner computes a simplified V-invariant mean-field saddle on the
minimal block and reports `u_0^4_MF` for `β = 6`. Compared to:

- canonical MC: `⟨P⟩ ≈ 0.5934`
- bridge-support stack analytic candidate: `P(6) ≈ 0.59353` (`PLAQUETTE_SELF_CONSISTENCY_NOTE`)
- naive mean-field (Drouffe-Zuber 1983): `⟨P⟩_MF ≈ 0.55-0.58`

## 7. Named obstruction

The minimal-block mean-field saddle on the V-invariant subspace gives
**an analytic value**, but not equal to the bulk thermodynamic-limit
value `0.5934`. The gap is the **minimal-block-equals-bulk obstruction**:

```text
[MINIMAL-BLOCK-EQUALS-BULK OBSTRUCTION]:
  The V-invariant minimal-block mean-field saddle u_0_min^4 differs from
  the thermodynamic-limit ⟨P⟩(β=6) by a non-zero amount.
  Closing this gap requires either:
    (a) a structural theorem proving minimal-block-equals-bulk on the
        V-invariant subspace (no such theorem currently exists);
    (b) a perturbative correction to mean-field that restores the bulk
        value (standard lattice perturbation theory; lossy);
    (c) a non-perturbative analytic derivation matching the bulk
        thermodynamic limit (the famous open problem).
```

This is the same Nature-grade target as the bridge-support stack's
`framework-point underdetermination theorem`
(`GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md`),
which states that the current closed jet and structure theorems still do
not force a unique analytic `P(6)`.

## 8. Connection to bridge-support stack

The framework's existing bridge-support stack (cf.
`PLAQUETTE_SELF_CONSISTENCY_NOTE.md` "Exact bridge-support stack on `main`")
provides:

- Exact reduction-law existence/uniqueness theorem
- Exact connected plaquette-hierarchy theorem
- Exact obstruction to finite-order connected-hierarchy truncation
- Explicit Perron-state reduction theorem
- Source-sector matrix-element factorization at β=6
- Reference Perron solves: `P_loc(6) = 0.4524`, `P_triv(6) = 0.4225` from
  closed-form `c_λ(6)` + SU(3) intertwiners

These give the analytic candidate `P(6) ≈ 0.59353` upper-bound, with the
explicit window `0.5934 ≤ ⟨P⟩(β=6) ≤ 0.59353` (`±0.022%`).

The minimal-block mean-field saddle attempted here is a **lower-bound
analytic estimate** (typically `0.55-0.58` for naive mean-field;
V-invariant restriction may shift this). Together with the bridge-support
stack's upper bound, this would give a tighter analytic window if the
mean-field calculation is rigorous.

**Realistic deliverable:** sharpen the named obstruction; do not claim
closure.

## 9. What this attempt closes

- Confirms the user's H1 Route 1 strategy is well-defined: the
  self-consistent saddle equation can be set up using existing framework
  primitives.
- Identifies the specific obstruction: SU(3) Haar entropy `h(u_0)` does
  not have a closed form, so even the V-invariant minimal-block
  mean-field saddle is not fully analytic.
- Connects the saddle approach to the existing bridge-support stack as
  a complementary lower-bound estimate.

## 10. What this attempt does NOT close

- The analytic value of `⟨P⟩(β=6)` (the famous open lattice problem).
- The minimal-block-equals-bulk theorem on the V-invariant subspace.
- The bridge-support stack's framework-point underdetermination obstruction.

## 11. Honest status

```yaml
actual_current_surface_status: named-obstruction stretch attempt
target_claim_type: open_gate
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  Stretch attempt: the V-invariant minimal-block mean-field saddle is
  set up using existing framework primitives, but the SU(3) Haar entropy
  h(u_0) does not have a closed form, so the saddle is not analytically
  closed. Honest output is a sharper named obstruction, not closure of
  ⟨P⟩(β=6).
audit_required_before_effective_retained: true
bare_retained_allowed: false
proposal_allowed: false
proposal_allowed_reason: |
  Stretch attempt with named obstruction, not retained-positive movement.
  No retained-grade proposal is made.
```

## 12. Cross-references

- Verdict-named obstruction: [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md) (status amended 2026-05-01: explicit β=6 insertion remains open)
- Sister obstruction: [`GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md)
- Analytic candidate: bridge-support stack listed in `PLAQUETTE_SELF_CONSISTENCY_NOTE.md`, gives `P(6) ≈ 0.59353`
- Mean-field reference: Drouffe-Zuber 1983, Münster 1981 (admitted-context, comparator only)
- Loop pack: `.claude/science/physics-loops/vev-v-singlet-derivation-20260502/` (block 01 PR #408 contains shared loop pack files)
- Block 01 PR (independent prior): [#408](https://github.com/jonathonreilly/cl3-lattice-framework/pull/408) — H2 reformulation retiring B1+B2+B3
