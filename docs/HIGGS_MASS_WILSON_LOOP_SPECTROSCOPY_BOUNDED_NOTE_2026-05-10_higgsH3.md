# Higgs-Channel Wilson-Loop Spectroscopy on Retained MC — Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Sub-gate:** Lane 2 (m_H) — alternative path via lattice spectroscopy
**Status authority:** independent audit lane only; effective status is
pipeline-derived after audit ratification and dependency closure.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.

**Primary runner:** [`scripts/cl3_higgs_mass_wilson_loop_spectroscopy_2026_05_10_higgsH3.py`](../scripts/cl3_higgs_mass_wilson_loop_spectroscopy_2026_05_10_higgsH3.py)
**Cached output:** [`logs/runner-cache/cl3_higgs_mass_wilson_loop_spectroscopy_2026_05_10_higgsH3.txt`](../logs/runner-cache/cl3_higgs_mass_wilson_loop_spectroscopy_2026_05_10_higgsH3.txt)

## 0. Audit context

The Lane 2 (physical Higgs mass `m_H`) closure has been pursued along two
prior paths:

1. **Tree-level mean-field source-stack path** (`HIGGS_MASS_FROM_AXIOM_NOTE.md`):
   gives `m_H = v / (2 u_0) = 140.3 GeV` with a +12 % gap to PDG;
2. **3-loop SM RGE path** (`HIGGS_MASS_DERIVED_NOTE.md`,
   `frontier_higgs_mass_full_3loop.py`): gives `m_H ≈ 125.1 GeV` but
   inherits the `y_t(v)` lane's precision caveat and the lattice ->
   physical matching theorem at PR #843.

This note opens a **third path**: bypass the perturbative lattice ->
physical matching by building gauge-invariant scalar correlators and
extracting a bounded scalar-channel mass-scale estimator on the
framework's retained Monte Carlo infrastructure.
This is the standard lattice-gauge-theory spectroscopy route used in
e.g. Morningstar–Peardon (1999) for 0++ glueball mass extraction.

The probe asks a single question:

> Is the framework's retained content sufficient to extract a physical
> scalar mass scale by direct lattice spectroscopy, without the
> perturbative matching theorem?

**Answer (this note):** Yes — but the result is **bounded** by four
explicit named admissions (Section 4). The runner demonstrates that
scalar-channel correlators ARE buildable on the retained
numba-accelerated MC infrastructure (`scripts/cl3_exact_tier_ewitness_2026_05_07_ewitness.py`)
without new repo-wide axioms or imports, and extracts a bounded
mass-scale estimator `m_eff` at the canonical operating point
`β_W = 6` (`g_bare = 1`).

This note does not close the Lane 2 perturbative matching theorem; it
provides a **second, independent quantitative readout** of the Higgs-
sector scalar mass scale that is convention-dependent in different ways
than the perturbative path.

## Claim

## 1. Theorem (bounded; spectroscopy on retained surface)

**Theorem (Higgs-channel Wilson-loop spectroscopy, bounded).**

Let `H_KS(g²)` denote the framework Kogut-Susskind Hamiltonian on `Z³`
at the canonical operating point `g² = g_bare² = 1`, equivalently the
Wilson lattice action at `β_W = 2 N_c = 6`. Define the spatial
plaquette timeslice operator

```text
P(t) := (1 / N_p^{(σ)}(L)) · Σ_{x in slice t}  Σ_{i < j ≤ 3}
                                  (1/N_c) · Re Tr U_{x; ij}(t)        (1)
```

with `N_p^{(σ)}(L) = L³ · 3` (number of distinct spatial plaquettes per
timeslice on a cubic spatial slice) and `U_{x; ij}(t)` the spatial
plaquette in the `(i, j)` plane at site `(x, t)`. Define the connected
plaquette-plaquette timeslice correlator

```text
C(t) := < P(0) P(t) >  -  < P >^2.                                   (2)
```

**Claim 1 (operator buildability).** The timeslice operator `P(t)` and
its connected correlator `C(t)` are buildable on the framework's
retained MC infrastructure (specifically, on the numba-jitted SU(3)
heatbath kernel of `scripts/cl3_exact_tier_ewitness_2026_05_07_ewitness.py`)
WITHOUT new repo-wide axioms, new imports, or new lattice content beyond what is
already retained at PR #685 / PR #845.

**Claim 2 (bounded mass-scale extraction).** On the canonical operating point
`β_W = 6` on a periodic `L³ × T` lattice with `L = 4, T = 8`, three
seeds, and `n_measure = 160` sweeps per seed, the connected correlator
`C(t)` yields a finite absolute-log-ratio effective-mass-scale estimator

```text
m_eff^(lattice) > 0,    finite,    estimated from log(|C(d)| / |C(d+1)|)
                                      on d in [1, T/2 - 1].                 (3)
```

When the connected correlator changes sign or lacks a clean
single-exponential plateau on this small lattice, the runner reports the
absolute-log-ratio estimator as a bounded upper-scale diagnostic and
flags that mode. This note does **not** establish a clean spectroscopy
plateau.

**Claim 3 (GeV reading, convention-dependent).** Under the convention
`a · v_EW = 1` at the canonical operating point (i.e. identifying the
inverse lattice spacing with the framework's hierarchy-theorem `v_EW`
scale), the physical-units reading is

```text
m_eff^(GeV)  =  m_eff^(lattice) · (v_EW^{retained} = 246.28 GeV).    (4)
```

This GeV reading is **conditional** on the convention (3) and on the
four admissions in Section 4. It is a **comparison-only** readout
against the PDG anchor `m_H_PDG = 125.25 GeV`; the PDG value is **not
load-bearing** for the derivation.

## 2. What this closes vs. does not close

### Closed (bounded, this note)

- **Operator buildability**: scalar-channel timeslice correlators are
  buildable on the retained numba MC infrastructure with no new repo-wide axioms
  or imports.
- **Numerical demonstration at canonical operating point**: at
  `β_W = 6` on `4³ × 8`, the connected correlator `C(t)` is
  numerically positive at `t = 0`, satisfies the Schwarz inequality
  `C(0) ≥ |C(t)|`, and yields a finite positive mass-scale estimator
  from absolute log-ratios `log(|C(d)| / |C(d + 1)|)`.
- **Estimator extraction**: a weighted estimator over
  `d ∈ [1, T/2 - 1]` is reported with a stat error from block-jackknife
  pooled across seeds, and the runner flags whether it used a clean
  positive-decay window or an upper-scale fallback.
- **GeV conversion under convention `a · v_EW = 1`**: a single-line
  conversion formula is recorded and the resulting `m_eff^(GeV)` is
  printed alongside `m_H_PDG = 125.25 GeV` for comparison.

### Not closed (frontier remaining)

- **Lane 2 closure** (lattice -> physical matching theorem at PR #843):
  this note does NOT close that theorem. It provides a parallel
  quantitative readout that depends on different admissions.
- **Channel identification**: identifying the mass-scale estimator extracted
  from `C(t)` with the physical Higgs `m_H` requires the Higgs-channel
  identification of `CL3_SM_EMBEDDING_THEOREM`, which itself enumerates
  multiple channel candidates (parallel to the per-channel ambiguity
  in `WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md`).
  This is a non-derived admission.
- **Finite-size systematic**: the spatial volume `L = 4` and temporal
  extent `T = 8` used by the runner are at the campaign's compute-tier
  limit. The leading `m_eff` inherits a finite-size systematic that is
  not eliminated until `L · a · m_eff > 4` (rule of thumb) and
  `T · a · m_eff > 6`. This is part of the named compute frontier.
- **Lattice-spacing convention**: the conversion `a^{-1} = v_EW`
  uses `a · v_EW = 1` at the canonical operating point. This is a
  convention, not a derivation.
- **Multi-state plateau systematic**: the runner uses a single-state
  log-ratio estimator. A variational-smearing multi-state fit
  (Lüscher–Weisz 1985 / Morningstar–Peardon 1999) would give a tighter
  plateau systematic but requires content beyond this campaign's
  compute frontier.
- **Exact-tier ε_witness on m_eff from spectroscopy alone**: not
  reached. The dominant remaining uncertainty is the finite-size and
  channel-identification admissions, which exceed the ~3 × 10⁻⁴
  exact-tier target.

### Final readout

```text
m_eff^(lattice)         = (runner-reported estimator) ± (runner-reported, stat)
m_eff^(GeV)             = m_eff^(lattice) · 246.28 GeV     (convention)
                         (comparison only against m_H_PDG = 125.25 GeV;
                          PDG NOT load-bearing for this derivation)
stat error budget       = block-jackknife pooled across seeds
NAMED ADMISSIONS        = (1) channel ID, (2) finite-size,
                          (3) lattice-spacing convention,
                          (4) plateau-fit window
```

## Proof-Walk

## 3. Proof-Walk

| Step | Load-bearing input | New axiom or import? |
|---|---|---|
| Define spatial-plaquette timeslice operator `P(t)` per eq. (1) | gauge-invariant Wilson loop, retained at PR #674 | no |
| Define connected correlator `C(t) = <P(0)P(t)> - <P>²` per eq. (2) | standard lattice-spectroscopy operator | no |
| Implement timeslice accumulator on the framework's retained numba MC kernel | mirror of the `_plaquette_measure_jit` kernel pattern; no new MC algorithm | no |
| Run isotropic Wilson MC at `β_W = 6` on `L³ × T` with three seeds | retained MC operating point per PR #685 | no |
| Compute `C(t)` per measurement; pool across seeds via block-jackknife | retained error-estimation pattern from PR #685 | no |
| Extract local effective-mass-scale estimator `m_eff(d) = log(|C(d)| / |C(d + 1)|)` for `d ∈ [1, T/2 - 1]` | bounded lattice-spectroscopy diagnostic | no |
| Weighted estimator / upper-scale fallback via inverse-variance weights | standard finite-statistics diagnostic; not a retained spectroscopy plateau | no |
| GeV conversion via `m_gev = m_lat · v_EW` under convention `a · v_EW = 1` | hierarchy theorem `v_EW = 246.28 GeV` retained | no |
| Compare to `m_H_PDG = 125.25 GeV` (comparison only, NOT load-bearing) | PDG comparison anchor (NOT load-bearing) | no |

Every step uses retained MC infrastructure, retained Wilson loop
operator, retained `β_W = 6`, retained `v_EW`, and standard lattice-
spectroscopy estimators. No new repo-wide axioms, no new lattice content, no new
imports beyond stdlib + numpy + (optional) numba.

## 4. Conditional admissions

This bounded theorem is conditional on four explicit named admissions:

**(1) Channel-identification admission.** The mass-scale estimator extracted
from `<P_spatial(0) P_spatial(t)>` is the lightest 0++ scalar in the
spatial-plaquette channel for SU(3) pure-gauge at `β_W = 6`.
Identifying that with the physical Higgs `m_H` requires the Higgs-channel
identification of `CL3_SM_EMBEDDING_THEOREM`, which lists multiple
candidate identifications. The per-channel ambiguity is catalogued in
[`WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md`](WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md):
single-class `S = {2}` is r-independent (no closure mechanism), while
paired classes `S = {0, 4}` and `S = {1, 3}` and the uniform-16 class
all close at distinct `r` values. **The channel identification is a
non-derived admission.**

**(2) Finite-size admission.** The spatial volume `L³` and temporal
extent `T` used by the runner are at the campaign's compute-tier limit.
The leading `m_eff` inherits a finite-size systematic that is not
eliminated until `L · a · m_eff > 4` and `T · a · m_eff > 6`. This is
part of the named compute frontier and is NOT closed by this note. A
finite-size scaling extrapolation parallel to Path B in
[`EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness.md`](EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness.md)
would close this admission but requires significantly more compute.

**(3) Lattice-spacing-conversion admission.** The conversion
`a^{-1} = v_EW / (a · v_EW)_lattice` uses the convention
`a · v_EW = 1` at the canonical operating point. This is a convention,
not a derivation. The framework's hierarchy theorem assigns `v_EW` to
the `L_t = 2` APBC block (per `HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`),
but this runner runs at `L_t > 2` for spectroscopy purposes.
Convention-dependence is flagged in this section.

**(4) Plateau-fit admission.** The estimator is read off from a small
`d`-window via the absolute-log-ratio diagnostic. If the small-volume
connected correlator changes sign or lacks a clean positive-decay
window, the runner uses an upper-scale fallback. The bounded result
therefore inherits the systematic of the estimator window. A
variational-smearing multi-state fit (Lüscher–Weisz 1985 /
Morningstar–Peardon 1999) would tighten this admission but requires
content beyond this campaign's compute frontier.

Any of (1)–(4) failing voids the GeV reading.

## 5. Implementation

The runner [`scripts/cl3_higgs_mass_wilson_loop_spectroscopy_2026_05_10_higgsH3.py`](../scripts/cl3_higgs_mass_wilson_loop_spectroscopy_2026_05_10_higgsH3.py)
implements:

1. **numba-jitted SU(3) Cabibbo-Marinari heatbath** with three SU(2)
   subgroup sweeps per link; matches the kernel pattern of the retained
   `cl3_exact_tier_ewitness` runner at PR #685.
2. **SU(3) overrelaxation** via three SU(2) reflections (same kernel
   pattern).
3. **Even-odd parity sweep** with `n_overrelax` overrelaxation passes
   per heatbath sweep.
4. **NEW: timeslice spatial-plaquette accumulator** `_spatial_plaquette_per_slice`:
   sums the gauge-invariant `Re Tr U_p` over all spatial plaquettes
   `(μ < ν, μ, ν ∈ {0, 1, 2})` on each timeslice `t`, returning a
   length-`T` array `P_slice[t]`.
5. **NEW: connected correlator** `_build_correlator`: returns
   `C[d] = (1/T) Σ_t (P_slice[t] - mean) · (P_slice[(t + d) mod T] - mean)`.
6. **Block-jackknife error estimation** on the connected correlator.
7. **Multi-seed pooling** with seed-to-seed std as cross-check.
8. **Local m_eff estimator extraction** via the absolute-log-ratio diagnostic
   `m_local(d) = log(|C(d)| / |C(d + 1)|)` and inverse-variance-weighted
   estimator mean.
9. **GeV conversion** under convention `a · v_EW = 1`.
10. **PDG comparison** with explicit "NOT load-bearing" flagging.
11. **13-part PASS/FAIL verification** of note structure, forbidden
    vocabulary absence, cited upstream existence, kernel self-test,
    timeslice consistency, correlator extraction, production MC,
    m_eff extraction, GeV conversion, four explicit admission
    statements, compute-tier summary, stat error budget, and boundary
    section.

## Dependencies

## 6. Dependencies

- [`EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness.md`](EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness.md)
  for the retained numba-jitted SU(3) heatbath kernel pattern (PR #685),
  multi-seed pooling, block-jackknife error estimation, and canonical
  `<P>_iso(β_W = 6) = 0.5934` operating point.
- [`EXACT_TIER_PATH_INTEGRAL_BOUNDED_NOTE_2026-05-07_exact.md`](EXACT_TIER_PATH_INTEGRAL_BOUNDED_NOTE_2026-05-07_exact.md)
  (PR #674) for the prior bounded W1 path-integral closure on the
  same operating point.
- [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) for
  the Higgs-sector identification within `Cl⁺(3)` and the Y, SU(2)_weak
  block decomposition that constrains the channel admission (1).
- [`WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md`](WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md)
  for the per-channel ambiguity catalogue: this note inherits the same
  channel-identification non-derivation status.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) for
  the parent tree-level mean-field setup and the +12 % Higgs gap that
  this spectroscopy probe approaches from a different angle.
- [`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md) for the
  3-loop SM RGE path (`m_H ~ 125.1 GeV`) that this note is
  complementary to.
- [`HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`](HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md)
  for the L_t = 2 APBC block that fixes `v_EW`; this note's convention
  `a · v_EW = 1` is consistent with that assignment at the L_t = 2
  level.
- [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
  (file pointer; not a markdown link, to avoid known back-edges) for
  the framework's complete prediction chain context.
- `MINIMAL_AXIOMS_2026-05-03.md` for
  the repo baseline physical `Cl(3)` local algebra and `Z^3` spatial
  substrate.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

## 7. Boundaries

This note does NOT close:

- the Lane 2 lattice -> physical matching theorem at PR #843;
- the exact `m_H` numerical value at retained-tier precision via
  spectroscopy alone;
- the channel-identification ambiguity catalogued in
  `WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md`;
- the lattice-spacing convention `a · v_EW = 1` (a convention, not a
  derivation);
- finite-size systematics on `L = 4, T = 8`;
- multi-state plateau systematics on the log-ratio estimator;
- exact-tier ε_witness ~ 3 × 10⁻⁴ on `m_eff` from spectroscopy alone;
- any parent theorem / status promotion;
- any claim that the `0++` scalar mass extracted from `<P_spatial(0) P_spatial(t)>`
  in pure SU(3) gauge IS the physical `m_H`. The relation is
  conditional on the channel-identification admission (1) and the
  conventional GeV reading admission (3).

## Verification

## 8. Verification

Run:

```bash
python3 scripts/cl3_higgs_mass_wilson_loop_spectroscopy_2026_05_10_higgsH3.py
```

Expected:

```text
=== TOTAL: PASS=N, FAIL=0 ===
VERDICT: bounded_theorem source-note proposal verified.
  - scalar-channel correlators ARE buildable on the retained
    numba-jitted MC infrastructure (no new repo-wide axioms / imports);
  - the leading scalar mass m_eff at the canonical operating
    point is extracted to within stat error reported above;
  - the m_eff -> GeV reading is conditional on the four named
    admissions (channel ID, finite size, lattice-spacing
    convention, plateau-fit window) catalogued in part 10.
  - this note does NOT close the Lane 2 m_H matching theorem.
```

The PASS count `N` is whatever the runner reports; FAIL must be 0.

## 9. Standard lattice-gauge-theory references

- **Cabibbo N., Marinari E.** (1982) *A new method for updating SU(N)
  matrices in computer simulations of gauge theories*, Phys. Lett. B
  119, 387. SU(N) pseudo-heat-bath via SU(2) subgroup sweeps.
- **Kennedy A.D., Pendleton B.J.** (1985) *Improved heat bath method
  for Monte Carlo calculations in lattice gauge theories*, Phys. Lett.
  B 156, 393. SU(2) exact heat-bath sampler.
- **Lüscher M., Weisz P.** (1985) *Definition and general properties of
  the transfer matrix in continuum limit improved lattice gauge
  theories*, Nucl. Phys. B 240, 349. Variational smearing for
  spectroscopy on the lattice.
- **Engels J., Karsch F., Satz H.** (1990) *A finite-size analysis of
  the SU(3) deconfinement phase transition*, Nucl. Phys. B 342, 7.
  SU(3) plaquette benchmarks at large `β_W`.
- **Morningstar C.J., Peardon M.** (1999) *Glueball spectrum from an
  anisotropic lattice study*, Phys. Rev. D 60, 034509. High-precision
  0++ glueball mass extraction from anisotropic lattice spectroscopy
  (the standard-lattice-gauge-theory benchmark for scalar-channel mass
  extraction).
