# Higgs Mass: Canonical Authority Boundary

**Claim type:** bounded_theorem

## Question

After implementing the full 3-loop Higgs runner directly, what still keeps the
Higgs lane from being fully unbounded?

## Final reviewer answer

The canonical Higgs posture is now **derived quantitative lane with inherited
YT residuals**, and that inherited caveat is no longer a separate Higgs-native
systematic.

The framework now supports all of the following:

| Result | Status |
|---|---|
| taste condensate acts as the Higgs field | DERIVED |
| lattice Coleman-Weinberg electroweak symmetry breaking occurs naturally | DERIVED |
| the hierarchy problem is removed because the cutoff is physical (`pi/a`) | DERIVED |
| the boundary condition `lambda(M_Pl) = 0` is framework-native | OPEN (Gap #7, 2026-05-10) |
| a direct framework-side full 3-loop Higgs computation exists | DERIVED |
| Buttazzo-style calibrated-fit dependence is required | NO |

What is **not** yet unbounded is the exact numerical Higgs claim by itself,
because the Higgs lane still inherits the explicit `y_t(v)` systematic.

## Canonical bounded claim

The paper-safe Higgs claim is now:

- the framework derives the Higgs mechanism itself
- the high-scale boundary input `lambda(M_Pl) = 0` is consumed as
  *admitted-context, literature-standard* (Gap #7, 2026-05-10): the
  earlier "framework-native composite-Higgs / no-elementary-scalar"
  slogan is not theorem-grade; the landed composite-Higgs stretch
  attempt records the NJL/BHL composite-scalar obstruction, and no
  framework derivation of the boundary is currently in place. File pointer:
  `docs/VACUUM_CRITICAL_STABILITY_NOTE.md` records the open-gate audit and
  the three candidate routes
  (asymptotic safety, MPP, pNGB).
- the current package now contains a direct full 3-loop Higgs runner with no
  Buttazzo-style parametric fit
- for the current accepted central input `y_t(v) = 0.9176` and the
  admitted-context boundary `lambda(M_Pl) = 0`, that runner gives
  `m_H ~= 125.1 GeV`
- the exact Higgs lane is derived from observed inputs and inherits the
  current YT-lane precision caveat rather than a separate Higgs-only closure
  gap; the boundary-condition derivation is OPEN and is a separate
  upstream item, NOT load-bearing on the `m_H ~= 125.1 GeV` numerical
  prediction (which any SM-equivalent boundary input gives)

## What changed

The old Higgs limitation had two distinct pieces:

1. the package lacked a complete direct 3-loop Higgs implementation
2. the accepted `y_t(v)` route still carried the load-bearing precision caveat

The new runner
[scripts/frontier_higgs_mass_full_3loop.py](../scripts/frontier_higgs_mass_full_3loop.py)
removes blocker (1). It computes the Higgs mass from the admitted-context
boundary input `lambda(M_Pl) = 0` (literature-standard; no longer asserted
as a framework-native consequence — Gap #7, 2026-05-10) using the full
3-loop SM RGE system and current framework-side low-energy inputs.

So the remaining Higgs caveat is no longer “missing Higgs machinery.”
It is inherited from the accepted `y_t` lane.

## Taste-scalar support theorem

The current Higgs support stack also contains one exact taste-block theorem:
[TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md](./TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md).

That theorem shows that the one-loop fermion Coleman-Weinberg Hessian on the
retained taste block is isotropic at the axis-aligned electroweak minimum, so
the fermion-CW sector alone cannot split the Higgs direction from the two
orthogonal taste directions.

On the current bounded gauge-only split model this gives a near-degenerate
taste-scalar pair at

- `m_taste = 124.91 GeV`

with a scalar-only thermal-cubic estimate `v_c/T_c = 0.3079`.

This is useful support for Higgs/taste bookkeeping and downstream EWPT work,
but it does not change the canonical Higgs claim itself. The headline Higgs row
remains `m_H = 125.1 GeV`, with inherited YT-lane precision caveat.

## Current numerical posture

For the current central input `y_t(v) = 0.9176`, the full 3-loop Higgs runner
gives:

- `m_H ~= 125.1 GeV` with no parametric fit
- an inherited Higgs band of roughly `121.1-129.2 GeV` on the old
  bridge-path cross-check budget

That means the honest Higgs read is:

- **mechanism:** derived
- **3-loop computation:** implemented
- **central Higgs value:** framework-side and direct
- **remaining bound:** inherited from `y_t`, not from missing Higgs code

## Why exact Higgs closure is still systematic-limited

Only two scientific cautions remain.

1. The accepted `y_t(v)` route still carries the lane’s live precision caveat.
2. Vacuum stability inherits that same Yukawa-route precision caveat.

So the correct current claim is not “Higgs still lacks a real computation.”
It is “Higgs is conditionally closed at 3-loop on the accepted YT route.”

## Current route inventory

### Canonical authority

- [scripts/frontier_higgs_mass_full_3loop.py](../scripts/frontier_higgs_mass_full_3loop.py)
  is now the primary quantitative authority runner for the Higgs lane.
  Its job is to show that the Higgs-specific 3-loop blocker is gone.
- [scripts/frontier_higgs_mass_derived.py](../scripts/frontier_higgs_mass_derived.py)
  remains a useful mechanism / boundary companion, but it is no longer the
  only honest Higgs-boundary runner.

### Supporting Higgs surfaces

- [HIGGS_MECHANISM_NOTE.md](./HIGGS_MECHANISM_NOTE.md)
  mechanism-level support
- [HIGGS_FROM_LATTICE_NOTE.md](./HIGGS_FROM_LATTICE_NOTE.md)
  bounded / historical quantitative support
- [HIGGS_MASS_NOTE.md](./HIGGS_MASS_NOTE.md)
  historical numerical CW support

These notes remain useful context, but they should not outrank this note when
a reader asks what the Higgs lane currently claims.

## Input-authority chain

The primary runner
[`scripts/frontier_higgs_mass_full_3loop.py`](../scripts/frontier_higgs_mass_full_3loop.py)
consumes six hard-coded numeric inputs. This section names the on-repo
authority surfaces for those inputs so the audit graph can test the chain
directly. The audit ledger remains the only authority for audit verdicts and
effective status; this section does not promote this note or any sibling row.

| Runner input | Runner value | Authority notes | Boundary |
|---|---|---|---|
| `y_t(v)` | `0.9176` | [`YT_ZERO_IMPORT_AUTHORITY_NOTE.md`](./YT_ZERO_IMPORT_AUTHORITY_NOTE.md), [`YT_FLAGSHIP_BOUNDARY_NOTE.md`](./YT_FLAGSHIP_BOUNDARY_NOTE.md), [`YT_COLOR_PROJECTION_CORRECTION_NOTE.md`](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md), [`YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md`](./YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md) | Current YT-lane endpoint with the residual budget documented in the YT authority notes. This row does not promote the YT surface or remove the inherited Higgs precision caveat. |
| `g_1(v)` (GUT norm) | `0.464` | [`EW_COUPLING_DERIVATION_NOTE.md`](./EW_COUPLING_DERIVATION_NOTE.md), [`YT_EW_COLOR_PROJECTION_THEOREM.md`](./YT_EW_COLOR_PROJECTION_THEOREM.md); `docs/COMPLETE_PREDICTION_CHAIN_2026_04_15.md` is a file-pointer context reference, not a markdown dependency, to avoid a known back-edge through `higgs_mass_from_axiom_note -> higgs_mass_derived_note`. | The value is tied to the connected-trace EW specialization. The selector `kappa_EW = 0` remains a separate derivation gate. |
| `g_2(v)` | `0.648` | [`EW_COUPLING_DERIVATION_NOTE.md`](./EW_COUPLING_DERIVATION_NOTE.md), [`YT_EW_COLOR_PROJECTION_THEOREM.md`](./YT_EW_COLOR_PROJECTION_THEOREM.md); `docs/COMPLETE_PREDICTION_CHAIN_2026_04_15.md` remains a file-pointer context reference for cycle safety. | The runner value is consistent with the bounded EW specialization; non-perturbative SU(2) matching remains the open derivation gate. |
| `alpha_s(v)` | `0.1033` | [`ALPHA_S_DERIVED_NOTE.md`](./ALPHA_S_DERIVED_NOTE.md), [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](./PLAQUETTE_SELF_CONSISTENCY_NOTE.md), [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](./QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md) | The runner consumes `alpha_s(v)` directly. The plaquette `beta = 6` analytic insertion remains upstream work. |
| `v` | `246.28 GeV` | [`HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`](./HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md), [`HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md`](./HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md), [`GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md`](./GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md); `docs/COMPLETE_PREDICTION_CHAIN_2026_04_15.md` is context only. | This names the hierarchy surface that supplies the vev scale used by the runner; it does not add a new vev theorem. |
| `lambda(M_Pl) = 0` | `0.0` (admitted-context input) | [`HIGGS_MECHANISM_NOTE.md`](./HIGGS_MECHANISM_NOTE.md), [`ASSUMPTION_DERIVATION_LEDGER.md`](./ASSUMPTION_DERIVATION_LEDGER.md); `docs/HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md` and `docs/VACUUM_CRITICAL_STABILITY_NOTE.md` are file-pointer context references, not markdown dependencies, to avoid known back-edges. | **Gap #7 update 2026-05-10:** `lambda(M_Pl)` is OPEN. This row was previously framed as a framework-native boundary; the earlier "composite-Higgs / no-elementary-scalar" slogan is not theorem-grade, the landed composite-Higgs stretch attempt records the NJL/BHL composite-scalar obstruction, and no theorem-grade framework derivation is currently in place. The runner's `m_H` prediction uses this value as a literature-standard *admitted-context* input on equal footing with Buttazzo / Degrassi SM analyses. The `m_H ~= 125.1 GeV` numerical prediction therefore does NOT load-bear on a framework derivation of the boundary — it is the same prediction any SM analysis with the same inputs would give. The boundary-derivation itself is logged as an open gate; candidate routes (asymptotic safety, Multiple-Point Principle, pNGB-with-shift-symmetry per Contino-Pomarol 2003) are flagged but none is closed. |

This section changes only discoverability of the runner inputs. It does not
derive any of the six values, does not ask for status promotion, and does not
claim that the Higgs mass lane is closed.

## Note↔runner reconciliation

A reader scanning the Higgs portion of the repo encounters three distinct
numerical Higgs-mass values reported by three distinct runners on three
distinct surfaces. They are not in conflict; they compute different
observables along different chains. This section makes that mapping explicit so
the reader does not mistakenly treat them as competing predictions.

| Surface | Runner | Value | What it computes |
|---|---|---|---|
| **This note's named primary runner** | [`scripts/frontier_higgs_mass_full_3loop.py`](../scripts/frontier_higgs_mass_full_3loop.py) | `m_H ~= 125.1 GeV` | Full 3-loop SM RGE from `lambda(M_Pl) = 0` boundary down to `mu = v`, with the framework-derived input set `(g_1 = 0.464, g_2 = 0.648, alpha_s(v) = 0.1033, y_t(v) = 0.9176, v = 246.28 GeV)`. This is the canonical headline of `HIGGS_MASS_DERIVED_NOTE.md`. |
| Corrected-y_t support route | [`scripts/frontier_higgs_mass_corrected_yt.py`](../scripts/frontier_higgs_mass_corrected_yt.py) | `m_H = 119.93 GeV` (3L+NNLO partial) | A separate corrected-y_t RGE route at 3L+NNLO. The companion `vacuum_critical_stability_note` (file pointer: `docs/VACUUM_CRITICAL_STABILITY_NOTE.md`; not a markdown link to avoid citation back-edge) calls this the "2-loop support route." It is a different observable along a different chain and is NOT a verifier for the named primary runner. |
| Tree-level mean-field axiom note | [`scripts/higgs_tree_level_mean_field_runner_2026_05_03.py`](../scripts/higgs_tree_level_mean_field_runner_2026_05_03.py) | `m_curv_tree = v / (2 u_0) = 140.3 GeV` (per Gap #3 lite 2026-05-10 demotion; previously labeled `m_H_tree`) | Tree-level mean-field per-channel symmetric-point curvature scale with a `+12%` gap to observed; lives in `higgs_mass_from_axiom_note` (file pointer: `docs/HIGGS_MASS_FROM_AXIOM_NOTE.md`; not a markdown link to avoid citation back-edge). It is **not** a Higgs-mass prediction (the symmetric-point curvature is structurally distinct from a broken-phase pole; V_taste alone has no interior minimum, per Morse/convexity Gap #3 probe); it is NOT the headline of this note; and the gap-closure load is delegated explicitly to sister authorities (corrected-y_t RGE, lattice-spacing convergence, Wilson-term taste breaking). |

The headline of `HIGGS_MASS_DERIVED_NOTE.md` is and remains `m_H ~= 125.1 GeV`
on the full 3-loop framework-side route, with the inherited Higgs band
`121.1-129.2 GeV` on the older bridge-path cross-check budget. The `119.93 GeV`
support readout and the `140.3 GeV` tree-level mean-field
**symmetric-point per-channel curvature scale** (`m_curv_tree`, demoted from
`m_H_tree` in 2026-05-10 Gap #3 lite) are both auxiliary; neither competes
with this note's headline.

## Paper-safe framing

**Can claim**

- the Higgs mechanism emerges naturally from the lattice
- the hierarchy problem is solved structurally
- the repo now contains a direct full 3-loop Higgs computation with no
  Buttazzo-style calibrated-fit dependence
- for the admitted-context boundary input `lambda(M_Pl) = 0`
  (literature-standard, equal footing with Buttazzo / Degrassi SM
  analyses), the runner gives `m_H ~= 125.1 GeV`
- the remaining Higgs precision caveat is inherited from the accepted `y_t`
  lane and is independent of the boundary-condition derivation

**Cannot claim**

- `lambda(M_Pl) = 0` is a framework-native / framework-derived Higgs
  boundary condition (Gap #7 retirement, 2026-05-10): the earlier
  "composite-Higgs / no-elementary-scalar" slogan is not theorem-grade;
  the landed composite-Higgs stretch attempt records the NJL/BHL
  composite-scalar obstruction, and no theorem-grade derivation is
  currently in place. The boundary is consumed as admitted-context input.
- the Higgs lane is unbounded independently of `y_t`
- vacuum stability is unbounded while `y_t` still carries a live precision
  caveat
- older lattice-CW or partial-Higgs notes as if they were the live authority
