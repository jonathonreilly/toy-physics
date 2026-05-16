# `y_t` Bridge Moment Closure Note

**Date:** 2026-04-15 (demoted 2026-05-16)
**Claim type:** bounded_theorem
**Status:** bounded numerical-match scan (target-conditioned moment-band collapse across selected profile families on an accepted-branch affine-kernel fit)
**Audit class:** G — load-bearing step is a target-conditioned numerical scan against an accepted-branch kernel fit, not a derivation
**Primary runner:** `scripts/frontier_yt_bridge_moment_closure.py`

## Scope (honest framing)

This note is **not** a derivation that the remaining UV-localized bridge
problem closes to a two-moment system `(I_2, c_2)` on the exact interacting
lattice bridge. It is a bounded *target-conditioned numerical scan* layered
on top of an accepted-branch affine-kernel fit. Given the imported physical
endpoint `y_t(v) = 0.9176`, a chosen SM-like reference transport, a chosen
lattice-side UV bridge profile, a single accepted-branch logistic bridge
(`center_frac = 0.975`, `width_frac = 0.020`) used to construct the response
kernel, a pre-selected UV-localized window (`tau_frac >= 0.94`) on which the
kernel is fit affinely, three pre-selected endpoint-preserving profile
families (logistic, error-function, smoothstep), and a fixed
`(center_frac, width_frac)` scan grid, the runner reports that the
near-target rows (those retained inside `|dev| < 0.1%`) and the best row of
each scanned family share a narrow response-weighted moment band
`J_aff = I_2 * (a c_2 + b)`, where `(a, b)` are the slope and intercept of
the accepted-branch affine kernel fit.

Seven load-bearing inputs are imported, not derived inside this note:

1. the physical target `y_t(v) = 0.9176`,
2. the SM-like reference transport anchored at the low-energy strong
   coupling (one-loop QCD beta), used as the `g_{3,SM}` reference in `I_2`
   and the kernel construction,
3. the constructive lattice-side UV bridge profile the family deforms
   toward,
4. the *single* accepted-branch logistic bridge
   (`center_frac = 0.975`, `width_frac = 0.020`) used to build the
   linearized response kernel `K(tau)` from which the affine kernel
   `(a, b)` is read,
5. the pre-selected UV-localized window `tau_frac >= 0.94` on which the
   affine kernel fit is performed,
6. the three pre-selected smooth profile families parameterized by
   `(center_frac, width_frac)` on the fixed scan grid, and
7. the `|dev| < 0.5%` viable-class retention cut and the `|dev| < 0.1%`
   near-target retention cut against the imported target.

The runner's PASS rows
(`1a` affine kernel max relative error `2.29e-3`,
`1b` `corr(I_2, dev) = +0.999888`,
`1c` near-target `J_aff` band width `8.68e-5`,
`1d` best-family `J_aff` band width `2.27e-5`,
`1e` near-target `c_2` band width `1.06e-2`)
are therefore statements about *these scanned profile families inside this
pre-selected UV-localized window, weighted by the affine fit of the
linearized response kernel on the accepted-branch logistic bridge against
this imported target*, not statements that the exact interacting lattice
bridge is forced to be controlled by two moments, that the affine fit
extrapolates outside the scanned window, or that the kernel `K(tau)` itself
is the kernel of the exact (non-linearized) interacting bridge.

This is therefore an `audited_numerical_match` / class-G proxy in the
project's audit taxonomy, not a closed first-principles derivation. The
remaining structural gaps are recorded below in "What remains open".

## Upstream-cluster context (informational)

The bounded claim conditions on the same target-conditioned numerical
proxies that the rest of the YT moment-closure cluster conditions on, all
of which have been honestly framed as proxies:

- broad / diffuse bridges fail to reproduce the imported endpoint
  (`YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md`),
- only a narrow UV-localized window admits any fit
  (`YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md`),
- three endpoint-preserving profile families tuned inside the pre-selected
  UV-localized window agree on the imported endpoint with cross-family
  spread `<= 0.0252%` (`YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md`),
- inside that retained class, the normalized gauge-surplus action `I_2`
  correlates with endpoint deviation at `+0.999889` and the retained class
  shares a tight UV centroid `0.978 +/- 0.004`
  (`YT_BRIDGE_ACTION_INVARIANT_NOTE.md`),
- a structurally consistent reason to expect monotonic endpoint response to
  positive bridge surplus on the accepted background is recorded as a
  separate proxy in
  `YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md`, conditioned on the same
  accepted background and on positivity of the bridge surplus.

This note is downstream of all five and does not re-derive them. The
present "two-moment closure" framing is a numerical refinement of the
single-moment correlation reported in
`YT_BRIDGE_ACTION_INVARIANT_NOTE.md`: by reading off the slope and
intercept `(a, b)` of the linearized response kernel on the accepted-branch
logistic bridge inside the pre-selected UV-localized window, the runner
combines `I_2` with the surplus UV centroid `c_2` into a single weighted
moment `J_aff`, and reports that the retained rows share a narrow `J_aff`
band. Both the kernel and the window are chosen on the accepted branch and
are not derived from the framework axioms.

## Numerical result

Against the imported target `y_t(v) = 0.9176`, scanning
`center_frac in linspace(0.955, 0.985, 7)` and
`width_frac in linspace(0.012, 0.026, 8)` for each of the three profile
families and retaining `|dev| < 0.5%` for the viable class and `|dev| < 0.1%`
for the near-target class, the runner reports (cache
`logs/runner-cache/frontier_yt_bridge_moment_closure.txt`):

- accepted-branch affine kernel fit on `tau_frac >= 0.94`:
  `K(x) ~= 5.5995e-02 x - 9.6151e-03` with max relative error `2.286e-3`
  and rms relative error `1.016e-3`,
- `83` profiles retained inside the `|dev| < 0.5%` viable class,
- `22` profiles retained inside the `|dev| < 0.1%` near-target class,
- `corr(I_2, dev) = +0.999888` on the viable class
  (re-derived here from the same scan that
  `YT_BRIDGE_ACTION_INVARIANT_NOTE.md` reports),
- near-target `J_aff` band width `8.680e-5`,
- best-row-per-family `J_aff` band width `2.275e-5`,
- near-target `c_2` band width `1.058e-2`.

The honest interpretation is that, **conditional on** the imported endpoint
target, **conditional on** the chosen SM-like reference transport,
**conditional on** the chosen lattice-side UV bridge profile,
**conditional on** the single accepted-branch logistic bridge used to build
the kernel, **conditional on** the pre-selected UV-localized window on
which the kernel is fit affinely, **conditional on** the three pre-selected
profile families and their fixed scan grid, and **conditional on** the
`|dev|` retention cuts, the near-target rows and the best row of each
scanned family share a narrow common `J_aff` band.

It does **not** establish that the exact interacting lattice bridge selects
the two-moment system `(I_2, c_2)`, that the affine fit extrapolates
outside the pre-selected UV-localized window, that the linearized response
kernel is the kernel of the exact (non-linearized) interacting bridge, or
that the three scanned profile families fairly sample the admissible
bridge class outside the pre-selected window.

## Meaning (bounded)

The bounded claim this note licenses is narrow:

> *Conditional on* the imported endpoint `y_t(v) = 0.9176`,
> *conditional on* the chosen SM-like reference transport and lattice-side
> UV bridge profile, *conditional on* the single accepted-branch logistic
> bridge (`center_frac = 0.975`, `width_frac = 0.020`) used to build the
> linearized response kernel, *conditional on* the pre-selected
> UV-localized window `tau_frac >= 0.94` on which the kernel is fit
> affinely, *conditional on* the three pre-selected endpoint-preserving
> profile families (logistic, error-function, smoothstep) parameterized by
> `(center_frac, width_frac)` on the scanned grid, and *conditional on*
> the `|dev|` retention cuts, the near-target rows
> (`|dev| < 0.1%`) and the best row of each scanned family share a narrow
> common response-weighted moment band `J_aff = I_2 * (a c_2 + b)` with
> band widths `8.68e-5` and `2.27e-5` respectively, where `(a, b)` are read
> from the accepted-branch affine kernel fit on the pre-selected window.

It does **not** establish:

- that the exact interacting lattice bridge selects the two-moment system
  `(I_2, c_2)`,
- that the affine fit of the linearized response kernel extrapolates
  outside the pre-selected UV-localized window,
- that the linearized response kernel is the kernel of the exact
  (non-linearized) interacting bridge,
- that the moment band `J_aff` is uniquely selected by any axiom in the
  framework, or
- that the three pre-selected profile families fairly sample the
  admissible bridge class outside the pre-selected window.

## What remains open (load-bearing gaps)

To upgrade this row from `audited_numerical_match` to a clean derivation,
the following structural gaps must be closed, none of which the present
runner addresses:

1. derive the endpoint `y_t(v) = 0.9176` from the framework axioms rather
   than importing it as the comparator target;
2. derive the response kernel of the exact (non-linearized) interacting
   lattice bridge from operator content alone, rather than building a
   linearized kernel on a single accepted-branch logistic bridge;
3. derive why that exact response kernel is affine on the relevant window
   from operator content, rather than fitting an affine kernel on a
   pre-selected UV-localized window `tau_frac >= 0.94` to a max relative
   error `2.286e-3`;
4. derive why the kernel slope and intercept `(a, b)` (and hence the
   moment band `J_aff`) are structurally selected by the axioms, rather
   than read off the accepted-branch affine fit;
5. derive why the three pre-selected profile families exhaust (or fairly
   sample) the admissible smooth bridge class outside the pre-selected
   UV-localized window, rather than treating them as convenient analytic
   placeholders;
6. derive the SM-like reference transport that defines `g_{3,SM}` in
   `I_2` from a closed two-loop (or higher) QCD beta on the framework's
   physical lattice surface, rather than the one-loop QCD beta as a
   proxy.

## Audit dependency repair links

This graph-bookkeeping section records the upstream notes the
moment-closure proxy reuses. It does not promote this note or change the
audited claim scope.

- [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md)
  for the forced UV-localized class premise (target-conditioned numerical
  proxy).
- [YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
  for the constructive UV-localized bridge family the kernel reuses
  (target-conditioned numerical proxy).
- [YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md](YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md)
  for the rearrangement statement about the linearized endpoint-response
  kernel (target-conditioned numerical proxy on the same accepted
  background).
- [YT_BRIDGE_ACTION_INVARIANT_NOTE.md](YT_BRIDGE_ACTION_INVARIANT_NOTE.md)
  for the dominant `I_2` correlation the moment closure refines into the
  weighted band `J_aff = I_2 * (a c_2 + b)` (target-conditioned numerical
  proxy on the same scan).
- [YT_BOUNDARY_THEOREM.md](YT_BOUNDARY_THEOREM.md)
  for the v boundary used as the IR endpoint reference.
