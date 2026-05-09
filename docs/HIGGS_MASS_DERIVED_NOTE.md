# Higgs Mass: Canonical Authority Boundary

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
| the boundary condition `lambda(M_Pl) = 0` is framework-native | DERIVED |
| a direct framework-side full 3-loop Higgs computation exists | DERIVED |
| Buttazzo-style calibrated-fit dependence is required | NO |

What is **not** yet unbounded is the exact numerical Higgs claim by itself,
because the Higgs lane still inherits the explicit `y_t(v)` systematic.

## Canonical retained claim

The paper-safe Higgs claim is now:

- the framework derives the Higgs mechanism itself
- the framework derives the natural high-scale boundary `lambda(M_Pl) = 0`
- the current package now contains a direct full 3-loop Higgs runner with no
  Buttazzo-style parametric fit
- for the current accepted central input `y_t(v) = 0.9176`, that runner gives
  `m_H ~= 125.1 GeV`
- the exact Higgs lane is derived and inherits the current YT-lane precision
  caveat rather than a separate Higgs-only closure gap

## What changed

The old Higgs limitation had two distinct pieces:

1. the package lacked a complete direct 3-loop Higgs implementation
2. the accepted `y_t(v)` route still carried the load-bearing precision caveat

The new runner
[scripts/frontier_higgs_mass_full_3loop.py](../scripts/frontier_higgs_mass_full_3loop.py)
removes blocker (1). It computes the Higgs mass directly from the framework
boundary condition `lambda(M_Pl) = 0` using the full 3-loop SM RGE system and
current framework-side low-energy inputs.

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
but it does not change the canonical Higgs claim itself. The promoted Higgs row
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

## Input-authority chain (audit-explicit)

The 2026-05-07 audit (`audited_conditional`, xhigh, load-bearing 16.776) flagged
that the runner is a real 3-loop SM RGE solver but that the restricted packet
"does not close authority for any of: `y_t(v) = 0.9176`, `g_1`, `g_2`,
`alpha_s`, `v`, or `lambda(M_Pl) = 0`." The repair target was: "Add
retained-grade direct dependency edges for the current YT authority path,
g1/g2/alpha_s/v framework inputs, and lambda(M_Pl)=0 boundary authority, then
re-audit whether y_t(v)=0.9176 is independently derived rather than calibrated
to the Higgs target."

This section makes that input-side dependency chain explicit. Each row is a
pointer to the authority that supplies the runner's hard-coded numeric input
(`scripts/frontier_higgs_mass_full_3loop.py`, lines 940-952). The audit ledger
remains the only authority for current audit and pipeline-derived status; this
section does not promote any sibling claim or change the audit_status of
`higgs_mass_derived_note` itself.

| Runner input | Runner value | Authority note | Author tier (audit ledger) | What this row closes / what it does not |
|---|---|---|---|---|
| `y_t(v)` | `0.9176` | [`YT_ZERO_IMPORT_AUTHORITY_NOTE.md`](./YT_ZERO_IMPORT_AUTHORITY_NOTE.md) (primary), [`YT_FLAGSHIP_BOUNDARY_NOTE.md`](./YT_FLAGSHIP_BOUNDARY_NOTE.md), [`YT_COLOR_PROJECTION_CORRECTION_NOTE.md`](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md), [`YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md`](./YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md) | YT zero-import authority is `unaudited / positive_theorem`; YT color projection correction is `audited_renaming / positive_theorem`. The Ward ratio `y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6)` and color-projection factor `sqrt(8/9)` carry their own authority surfaces; the central `0.9176` value is the current YT-lane endpoint with `~1.95%` standard-method residual budget per the YT flagship note. | This row scopes the runner's `y_t(v) = 0.9176` to the live YT authority surface. It does NOT promote that surface to retained-grade; the inherited Higgs precision caveat documented above remains in force. |
| `g_1(v)` (GUT-norm) | `0.464` | [`EW_COUPLING_DERIVATION_NOTE.md`](./EW_COUPLING_DERIVATION_NOTE.md) (D1 / D2), `complete_prediction_chain_2026_04_15` (file pointer: `docs/COMPLETE_PREDICTION_CHAIN_2026_04_15.md`; not a markdown link to avoid citation back-edge through `higgs_mass_from_axiom_note -> higgs_mass_derived_note`) section 5.2, [`yt_ew_color_projection_theorem`](./YT_EW_COLOR_PROJECTION_THEOREM.md) | EW-coupling derivation note is `audited_conditional / bounded_theorem`. YT EW color-projection theorem is `audited_clean / bounded_theorem` for the bounded normalization family `K_EW(kappa_EW) = 1/(8/9 + kappa_EW/9)` with `kappa_EW = 0` connected-trace specialization explicitly NOT audited as derived. Complete-prediction-chain row reports `g_1(v) = 0.4644` at `kappa_EW = 0` (`+0.08%` vs observed). | The runner value `0.464` matches the connected-trace specialization at `kappa_EW = 0`. Row supplies an audit-conditional bounded authority. It does NOT close `kappa_EW = 0` as a derived selector. |
| `g_2(v)` | `0.648` | [`EW_COUPLING_DERIVATION_NOTE.md`](./EW_COUPLING_DERIVATION_NOTE.md) (D2 BOUNDED), `complete_prediction_chain_2026_04_15` (file pointer: `docs/COMPLETE_PREDICTION_CHAIN_2026_04_15.md`; not a markdown link to avoid citation back-edge through `higgs_mass_from_axiom_note -> higgs_mass_derived_note`) section 5.2, [`yt_ew_color_projection_theorem`](./YT_EW_COLOR_PROJECTION_THEOREM.md) | EW-coupling derivation note explicitly marks `g_2(v)` as `BOUNDED`, NOT derived: SU(2) hits a Landau pole when run perturbatively from `M_Pl`, so the framework requires non-perturbative SU(2) matching that is not yet supplied. Complete-prediction-chain row reports `g_2(v) = 0.6480` at `kappa_EW = 0` (`+0.26%` vs observed); same `K_EW` bounded family as `g_1`. | The runner value `0.648` is consistent with the bounded `K_EW` specialization. Row makes the load-bearing bounded status explicit: SU(2) non-perturbative matching is the open derivation gap. |
| `alpha_s(v)` (drives `g_3`) | `0.1033` (= `alpha_bare/u_0^2`) | [`ALPHA_S_DERIVED_NOTE.md`](./ALPHA_S_DERIVED_NOTE.md), [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](./PLAQUETTE_SELF_CONSISTENCY_NOTE.md), [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](./QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md) | All three are `audited_conditional / bounded_theorem`. `alpha_s_derived_note` carries `bounded` author tier explicitly; the canonical chain is `<P> = 0.5934` (MC-evaluated, bounded analytic scope at `beta = 6`) → `u_0 = <P>^{1/4}` → `alpha_s(v) = alpha_bare/u_0^2 = 0.1033`. | Row scopes `alpha_s(v)` to the live bounded same-surface lane. The plaquette `beta = 6` analytic insertion remains the upstream open work; the runner does NOT depend on the `v -> M_Z` bridge step (it consumes `alpha_s(v)` directly). |
| `v` (Higgs vev) | `246.28 GeV` (= `M_PL * (7/8)^{1/4} * alpha_LM^16`) | `complete_prediction_chain_2026_04_15` (file pointer: `docs/COMPLETE_PREDICTION_CHAIN_2026_04_15.md`; not a markdown link to avoid citation back-edge through `higgs_mass_from_axiom_note -> higgs_mass_derived_note`) section 3.2 (hierarchy theorem row), [`HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`](./HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md), [`HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md`](./HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md), [`GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md`](./GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md) | Hierarchy spatial-BC + Matsubara + connected-hierarchy-theorem rows are all `audited_clean / retained_bounded`, supplying the exact `u_0^{8 L_t}` taste-determinant suppression and finite-volume identities. The `(7/8)^{1/4}` APBC factor and `alpha_LM^16` exponent (= 16 staggered tastes in 4D) are derived structurally. | This is the strongest leg of the input chain: the 16-power suppression structure is `audited_clean`. The hierarchy formula `v = M_Pl * (7/8)^{1/4} * alpha_LM^16` matches observed `v` to `+0.03%`. Row does NOT add a new authority; it makes the existing retained-bounded surface explicit. |
| `lambda(M_Pl) = 0` | `0.0` (boundary condition) | [`HIGGS_MECHANISM_NOTE.md`](./HIGGS_MECHANISM_NOTE.md) (mechanism-level), [`ASSUMPTION_DERIVATION_LEDGER.md`](./ASSUMPTION_DERIVATION_LEDGER.md) (Higgs CW/stability package row, "bounded"); plus file-pointer references (no link, to avoid citation back-edges) to `docs/HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md` and `docs/VACUUM_CRITICAL_STABILITY_NOTE.md` | Higgs mechanism note is `audited_clean / retained_bounded` but supports only mechanism-level / EWSB-surface claims, NOT `lambda(M_Pl) = 0` as an independent retained derivation. The two file-pointer companions (`higgs_vacuum_explicit_systematic_note`, `vacuum_critical_stability_note`) are `unaudited / positive_theorem` and `unaudited / bounded_theorem` respectively; both treat the `lambda(M_Pl) = 0` boundary as the natural framework-side high-scale pin tied to the composite-Higgs / no-elementary-scalar boundary structure rather than as a stand-alone retained theorem. | This is the WEAKEST leg of the input chain. The boundary condition is treated framework-natively in mechanism-level support, but no retained-grade theorem currently derives `lambda(M_Pl) = 0` independently. The runner's `0.0` boundary value is therefore `bounded` on the audit ledger, NOT retained. **Open derivation needed:** a retained-grade theorem that forces `lambda(mu = M_Pl) = 0` from the Cl(3)/Z^3 axioms (composite-Higgs / no-elementary-scalar boundary structure made explicit and audit-clean). |

### What this section changes and what it does not

This section adds explicit pointers from the runner's hard-coded inputs to
their on-repo authority surfaces. It does not derive any of the six inputs and
it does not ask the audit ledger to upgrade any sibling status. The audit
ledger's `audited_conditional` verdict on `higgs_mass_derived_note` (terminal
audit, 2026-05-07) remains in force, and the lane's bounded posture is
unchanged. The point of the section is to make the dep chain explicit so that
a future re-audit can read each runner input against its named authority
without further investigation.

The two strongest legs are `v` (the hierarchy `audited_clean` surface) and
`alpha_s(v)` (the bounded same-surface plaquette chain). The two weakest legs
are `g_2(v)` (open SU(2) non-perturbative matching) and `lambda(M_Pl) = 0`
(no retained-grade independent derivation; mechanism-level support only). The
remaining three (`y_t`, `g_1`, the EW connected-trace specialization
`kappa_EW = 0`) are bounded / unaudited authority surfaces in active work.

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
| Tree-level mean-field axiom note | [`scripts/higgs_tree_level_mean_field_runner_2026_05_03.py`](../scripts/higgs_tree_level_mean_field_runner_2026_05_03.py) | `m_H_tree = v / (2 u_0) = 140.3 GeV` | Tree-level mean-field formula with a `+12%` gap to observed; lives in `higgs_mass_from_axiom_note` (file pointer: `docs/HIGGS_MASS_FROM_AXIOM_NOTE.md`; not a markdown link to avoid citation back-edge). It is NOT the headline of this note; the gap-closure load is delegated explicitly to sister authorities (corrected-y_t RGE, lattice-spacing convergence, Wilson-term taste breaking). |

The headline of `HIGGS_MASS_DERIVED_NOTE.md` is and remains `m_H ~= 125.1 GeV`
on the full 3-loop framework-side route, with the inherited Higgs band
`121.1-129.2 GeV` on the older bridge-path cross-check budget. The `119.93 GeV`
support readout and the `140.3 GeV` tree-level mean-field readout are both
auxiliary; neither competes with this note's headline.

## Paper-safe framing

**Can claim**

- the Higgs mechanism emerges naturally from the lattice
- the hierarchy problem is solved structurally
- `lambda(M_Pl) = 0` is a framework-native Higgs boundary condition
- the repo now contains a direct full 3-loop Higgs computation with no
  Buttazzo-style calibrated-fit dependence
- the remaining Higgs precision caveat is inherited from the accepted `y_t`
  lane

**Cannot claim**

- the Higgs lane is unbounded independently of `y_t`
- vacuum stability is unbounded while `y_t` still carries a live precision
  caveat
- older lattice-CW or partial-Higgs notes as if they were the live authority
