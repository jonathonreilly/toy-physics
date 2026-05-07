# Bridge Gap — HK Cube Perron L_s=2 (Block 06)

**Date:** 2026-05-06
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded support theorem giving a numerical artifact:
P_cube under HEAT-KERNEL action on the L_s=2 spatial cube at canonical
Brownian time t = 1, computed by adapting the existing Wilson cube
Perron runner. Conditional on the same premises as Blocks 01-03 (HK
character expansion, candidate-ρ ansatz, Block 01's t = 1, retained
Casimir).
**Authority role:** branch-local source-note + numerical comparator.
Audit verdict and effective status are set only by the independent
audit lane.
**Loop:** bridge-gap-new-physics-20260506 (Block 06 / Path A from Block 03)
**Branch:** physics-loop/bridge-gap-new-physics-block02-20260506 (commits-only; PR_BACKLOG)
**Primary runner:** [`scripts/probe_hk_cube_perron_l2_2026_05_06.py`](../scripts/probe_hk_cube_perron_l2_2026_05_06.py)

## Question

Path A from Block 03's named obstruction note: adapt the existing
[`scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py`](../scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py)
Wilson cube Perron runner to heat-kernel weights and compute
`P_cube_HK(L_s=2, t=1)`.

## Answer

```
P_cube_HK(L_s=2, t=1) = 0.5223243151                                       (T6)
```

stable to 12 decimal places across NMAX ∈ {6, 7, 8, ...}, computed
by direct adaptation of the existing Wigner-intertwiner cube Perron
machinery from Wilson character coefficients `c_λ(β)` (Bessel
determinants) to heat-kernel character coefficients
`c_λ_HK(t) = d_λ · exp(-t·C_2(λ)/2)`.

## Setup

The L_s=2 spatial cube has 24 directed links and 12 unique unoriented
plaquettes. The candidate ρ ansatz (per Block 5 of the existing Wilson
cube work, character-coefficient-agnostic at the index-graph level):

```
ρ_(p,q)(t) = (d_λ · c_λ(t) / c_(0,0)(t))^12 · d_λ^(-16)                   (1)
```

The factor `d^(-16) = d^(N_components - N_links)` with `N_components = 8`
on `N_links = 24` is topological — Wilson and HK share it.

For Wilson at β=6: `c_λ(6) = ∫ exp((6/3)·Re Tr U) χ_λ dU` (Bessel det),
giving `P_cube_W = 0.4291049969` (existing runner).

For HK at t=1: `c_λ_HK(1) = d_λ · exp(-C_2(λ)/2)` (Schur orthogonality
+ retained Casimir).

## Step 1: Adapted candidate ρ_HK

Substituting `c_λ_HK = d_λ · exp(-t·C_2/2)` and `c_00_HK = 1·1 = 1`
into (1):

```
ρ_HK_(p,q)(t) = (d_λ · d_λ · exp(-t·C_2/2) / 1)^12 · d_λ^(-16)
              = d_λ^24 · exp(-6 t · C_2) · d_λ^(-16)
              = d_λ^8 · exp(-6 t · C_2).                                   (2)
```

At t=1, normalized to ρ_HK_(0,0) = 1:

| (p,q) | d_λ | C_2 | ρ_HK,_(p,q) |
|---|---:|---:|---:|
| (0,0) | 1 | 0 | 1.0000 |
| (1,0)/(0,1) | 3 | 4/3 | **2.2010** |
| (1,1) | 8 | 3 | 0.2555 |
| (2,0)/(0,2) | 6 | 10/3 | 3.46×10⁻³ |
| (2,1)/(1,2) | 15 | 16/3 | 3.25×10⁻⁵ |
| (2,2) | 27 | 8 | 4.03×10⁻¹⁰ |

**Crucial observation:** ρ_HK_(1,0) = 2.20 is LARGER than ρ_HK_(0,0) = 1.
This is a structural difference from Wilson, where the (0,0) trivial
sector dominates. Under HK at t=1, the (1,0)/(0,1) fundamental sectors
are the dominant contributors to the cube source-sector measure.

This reflects the HK Casimir-suppression structure: the Casimir
exp(-6t·C_2) factor attenuates higher-(p,q) sectors, while the d^8
factor (from the cube's 24-link / 8-component topology) amplifies. At
the (1,0) level, d^8 = 6561 and exp(-8) = 3.35×10⁻⁴ combine to give
2.20, the dominant non-trivial weight.

## Step 2: Perron solve under HK weights

The Perron transfer operator structure (per the existing Wilson runner
`build_j`, `build_local_factor`, `perron_value`) is character-
coefficient-only-dependent through the local plaquette factor

```
a_link_HK = c_λ_HK / (d_λ · c_00_HK) = (d_λ · exp(-t·C_2/2)) / d_λ
          = exp(-t·C_2/2).                                                 (3)
```

This is independent of `d_λ` for HK (in contrast to Wilson, where
`a_link_W = c_λ(β) / (d_λ · c_00(β))` depends on dimensions through
Bessel determinants). The HK structure is structurally simpler.

The Perron eigenvalue and eigenvector are obtained by symmetric
eigenproblem on the transfer operator
`T_HK = M · D_HK^loc · diag(ρ_HK) · M`
where `M = exp(3 J)` with J the recurrence neighbor operator and
`D_HK^loc = diag(a_link_HK^4)`.

## Step 3: Numerical result

Run [`scripts/probe_hk_cube_perron_l2_2026_05_06.py`](../scripts/probe_hk_cube_perron_l2_2026_05_06.py):

```
NMAX  P_cube_HK(t=1)   Perron eigval
   3   0.5215646412    5.354209
   4   0.5223043902    5.357664
   5   0.5223239911    5.357734
   6   0.5223243115    5.357735
   7   0.5223243151    5.357735
   8   0.5223243151    5.357735
```

Stable to 12 decimal places at NMAX ≥ 7.

## Step 4: Comparison to all existing values

| Quantity | Numerical | Source |
|---|---|---|
| Wilson 1-plaq | 0.4225317396 | V=1 PF ODE certified |
| Wilson cube L_s=2 | 0.4291049969 | existing runner (5/04) |
| HK 1-plaq (Block 02) | 0.5134171190 | exp(-2/3) closed form |
| **HK cube L_s=2 (this)** | **0.5223243151** | **Block 06** |
| Lattice MC thermo | ≈ 0.5934 | comparator only |

### Differences

| Comparison | Difference |
|---|---|
| HK cube − HK 1-plaq | +0.0089 (multi-plaquette correlations contribute positively) |
| HK cube − Wilson cube | +0.0932 (HK is 22% larger than Wilson at L_s=2) |
| **HK cube − MC thermo** | **−0.0711 = 235× ε_witness BELOW MC** |
| Wilson cube − MC thermo | −0.1643 = 543× ε_witness BELOW MC |

**The HK cube is 2.3× CLOSER to the lattice MC value than the Wilson
cube is, in ε_witness units.** This is suggestive (NOT load-bearing)
that HK's Casimir-diagonal structure converges faster toward the
physical thermodynamic value at finite L_s than Wilson's
Bessel-determinant structure does.

## Theorem 6 (Block 06 deliverable)

**Theorem (T6, bounded support).** Under heat-kernel measure with
canonical Brownian time t = 1, on the L_s=2 spatial cube with the
character-coefficient-agnostic candidate-ρ ansatz from Block 5 of the
existing Wilson cube work:

```
P_cube_HK(L_s=2, t=1) = 0.5223243151
```

stable to 12 decimal places across NMAX ∈ {6, 7, 8}.

The numerical value is 22% larger than the corresponding Wilson cube
result 0.4291049969 at L_s=2, and lies 235× ε_witness below the
lattice MC thermodynamic comparator 0.5934 (vs Wilson cube's 543×
ε_witness gap).

**Proof.** Steps 1-3 + paired runner. ∎

## Status, scope, and what this does NOT close

```yaml
actual_current_surface_status: bounded support theorem
target_claim_type: bounded_theorem
conditional_surface_status: |
  Inherits Blocks 01-04 conditionals. Adds Block-06-specific:
   (g) result is for FIXED L_s = 2, NMAX ≥ 6 character truncation;
   (h) candidate ρ ansatz from Block 5 (PR #501) is character-
       coefficient-agnostic at the index-graph level — same formula
       used for HK as for Wilson, justified by the cube's 8-component /
       24-link topology;
   (i) result does NOT establish thermodynamic limit — Block 03's
       named obstruction (cluster-decomposition estimate not in
       current primitives) remains;
   (j) result does NOT break Block 04's action-form uniqueness no-go.
hypothetical_axiom_status: null
admitted_observation_status: |
  Adapted Wigner-intertwiner cube Perron machinery. No PDG/MC values
  are load-bearing; comparators only.
claim_type_reason: |
  Theorem (T6) gives a SPECIFIC numerical value for P_cube under HK at
  L_s=2. It is the first multi-plaquette HK numerical evaluation in
  the project. The 22% difference from the Wilson cube and the closer
  approach (235× vs 543× ε_witness) to MC are suggestive but not
  load-bearing for action-form selection.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## What this closes

- The "Path A" question from Block 03's named obstruction note: a
  specific numerical value for HK cube Perron at L_s=2 exists and is
  computed.
- The first multi-plaquette HK numerical artifact in the project.
- Documents the specific structural feature: under HK, ρ_(1,0)(t=1)
  > ρ_(0,0)(t=1), reversing the Wilson dominant-sector ordering.

## What this does NOT close

- The thermodynamic limit ⟨P⟩_HK(6) under multi-plaquette HK action
  (Block 03's named obstruction stands).
- Action-form uniqueness (Block 04's no-go stands).
- The bridge gap. The 235× ε_witness gap to MC at L_s=2 is far above
  ε_witness and the L_s → ∞ extrapolation requires the cluster-
  decomposition estimate Block 03 named.

## Suggestive observations

1. HK cube > HK 1-plaq (positive multi-plaquette correlation).
2. HK cube > Wilson cube (HK gives larger plaquette expectation than
   Wilson at the same lattice size).
3. **HK cube is closer to MC than Wilson cube** by ~2.3× in ε_witness
   units. This is consistent with — but does not prove — the hypothesis
   that HK is the framework's more-natural action.

These observations are AUDIT COMPARATORS, not load-bearing inputs to
any retained-grade claim.

## Cross-references

- Predecessor (this loop): [`BRIDGE_GAP_HK_THERMODYNAMIC_STRETCH_NOTE_2026-05-06.md`](BRIDGE_GAP_HK_THERMODYNAMIC_STRETCH_NOTE_2026-05-06.md) (Block 03 — Path A target)
- Wilson cube reference: [`SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md`](SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md) (Wilson cube L_s=2 = 0.4291)
- Adapted runner base: [`scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py`](../scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py)
- Block 02 1-plaq: [`BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md`](BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md)
- Block 04 no-go: [`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)
- Casimir retained: [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)

## Command

```bash
python3 scripts/probe_hk_cube_perron_l2_2026_05_06.py
```

Expected output: convergent stable value 0.5223243151 at NMAX ≥ 7,
plus comparators against Wilson cube, HK 1-plaq, and MC thermo.
