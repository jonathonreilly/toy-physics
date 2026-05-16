# Nonlinear Propagator: Born-Rule and Gravity-Sign Correlation (Exhibited Examples)

**Status:** support — honest-demoted to a bounded exhibited-counterexample
note. The earlier universal phrasing ("any amplitude nonlinearity breaks the
Born rule and flips Newtonian gravity") is **not** established here.

**Date of demotion:** 2026-05-16  (audit fix; iter29 of the science-fix loop)

## What this note now claims (narrow, defensible)

This note carries **two** distinct statements that need to be read separately.

### (A) Linear half — algebraic theorem (already retained)

> Given linear amplitude composition together with the quadratic Born surface
> `P = |A|^2`, the Sorkin third-order interference parameter `I_3` vanishes
> identically on every multi-slit configuration.

This direction is purely algebraic and is the retained theorem documented in
[`I3_ZERO_EXACT_THEOREM_NOTE.md`](I3_ZERO_EXACT_THEOREM_NOTE.md). The runner
`scripts/frontier_nonlinear_born_gravity.py` re-exhibits it numerically in 2D
(linear mode gives `|I_3|/P ~ 1.6e-16`, i.e. machine precision); it is not
needed as proof.

### (B) Nonlinear half — exhibited examples on a chosen 2D setup

For two specific pointwise amplitude nonlinearities,

- **quadratic**: `psi_out = sum_j K_ij * |psi_in(j)| * psi_in(j)`
- **cubic**: `psi_out = sum_j K_ij * psi_in(j)^3`

evaluated on a fixed 2D forward lattice (`20 x 21` for the Sorkin test,
`40 x 60` for the deflection test, `k = 6.0`, free-space kernel
`exp(i k L) / L` over nearest-neighbour `dy in {-1, 0, +1}`, per-layer
amplitude renormalization to keep the iterate bounded, analytic
`phi(x, y) = -M / r` coupling via action `S = L (1 - <phi>)`), we observe:

| Mode      | `|I_3|/P`  | Centroid-shift sign vs linear   |
|-----------|-----------|---------------------------------|
| linear    | `1.6e-16` | toward the mass (attractive)    |
| quadratic | `1.94e-1` | away from the mass (sign flip)  |
| cubic     | `2.35e-1` | away from the mass (sign flip)  |

So for **these two** nonlinearities on **this** lattice / kernel / coupling
choice, the Born rule is violated (`|I_3|/P ~ O(0.1)`, far above linear
machine noise) **and** the sign of the centroid shift relative to the linear
baseline flips from toward to away.

This is an **exhibited correlation on a finite menu**, not a universal
theorem.

## What this note no longer claims

The earlier file made three statements that the audit (codex-gpt-5.5,
2026-05-05) correctly flagged as not supported by the runner:

1. **"The Born rule and attractive Newtonian gravity are both consequences of
   linear amplitude superposition"** as a closed implication. The (A)-direction
   above is real; the reverse universal claim ("any nonlinearity breaks both")
   is not derived. The runner only tests two pointwise nonlinearities; there
   are families of nonlinear evolutions that preserve `I_3 = 0` (any unitary
   nonlinear gauge that still sums interferers pairwise on the Born surface),
   so the universal form is false as stated.

2. **"Mass exponent beta breaks for nonlinear propagators"**. The runner
   actually reports `beta = 0.997` (quadratic) and `beta = 0.992` (cubic),
   indistinguishable from the linear value `beta = 1.014` to the precision of
   the four-point fit. Beta does **not** break in these runs; only the sign
   does. The earlier note's table column "beta" with values "0.997 / 0.992"
   was correctly reported but mis-interpreted as evidence of mass-law failure.

3. **"The diamond NV Sorkin test simultaneously confirms both quantum and
   gravitational sectors"** as a model-independent claim. This is downgraded
   to: under the present framework's specific propagator class plus the
   gravity coupling fixed elsewhere in this repository, a Sorkin `I_3 = 0`
   measurement is consistent with both sectors; it is not a universal
   simultaneous certification.

## What is and is not load-bearing

- **Load-bearing (retained):** statement (A) above. This is the algebraic
  `I_3 = 0` theorem; it lives in `I3_ZERO_EXACT_THEOREM_NOTE.md` and does not
  need this note.
- **Support only (non-load-bearing):** statement (B). It establishes that the
  set of amplitude evolutions that simultaneously break Born and flip the
  observed gravity sign on the framework's chosen 2D propagation packet is
  **non-empty**. That is useful as a sanity check that linearity is not
  decorative, but it is not a generic no-go.
- **Removed:** the universal "nonlinear ⇒ both broken" implication, the
  mass-law-breaks claim, and the experimental simultaneity claim in their
  original universal form.

## Method (unchanged)

The runner `scripts/frontier_nonlinear_born_gravity.py` performs:

- **Sorkin test (2D, `20 x 21`, `k = 4`).** A three-slit barrier at column
  `Lx // 2`, slits at offsets `{-3, 0, +3}` from the mid-row, layer-by-layer
  free-kernel propagation with `dy in {-1, 0, +1}`. For each of the seven
  open-slit subsets the runner computes `|psi|^2` at the detector column and
  forms `I_3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C`. The reported
  scalar is `max(|I_3|) / sum(P_ABC)`.
- **Deflection test (2D, `40 x 60`, `k = 6`).** A Gaussian source of width
  `sigma = 2` is propagated through an analytic `phi(x, y) = -M / r` field
  via action `S = L (1 - 0.5 (phi_old + phi_new))`. The y-centroid at the
  penultimate column is compared to the no-field baseline. A small mass sweep
  `M in {0.002, 0.004, 0.008, 0.016}` and a distance sweep
  `b in {5, 7, 9, 11, 14, 18}` are fit on log-log to extract a mass exponent
  `beta` and an apparent distance exponent `alpha`.

For all three modes the post-layer renormalization
`psi_new / ||psi_new||` is applied in the deflection test; the linear Sorkin
test deliberately omits the normalization so that the I_3 cancellation is
exact rather than approximate. This asymmetry is documented in the script
comments and does not affect the (A)-direction theorem.

## Why this rewrite

The auditor's verdict was correct on the substance:

> The numerical runner is not a first-principles derivation from the stated
> framework axiom; it is a toy simulation at chosen lattice sizes, propagation
> kernels, nonlinearities, normalizations, and field coupling. Its stdout
> also overstates the mass-law claim: beta remains near 1 for the nonlinear
> cases, while the asserted gravity failure is mainly the selected sign
> response. The source note's universal conclusion does not follow from the
> restricted packet even if the reported runner values are accepted.

This note is now written so that what it claims is exactly what the runner
shows: two specific nonlinearities on one specific 2D setup that flip the
centroid-shift sign and produce a Sorkin parameter far from zero. The
universal-implication framing has been removed.

## Script

`scripts/frontier_nonlinear_born_gravity.py`

The script's CONCLUSION print block still narrates the original universal
framing because the runner is shared with other lanes; that text should be
read as a description of what was observed on the menu of two
nonlinearities, not as a theorem statement. The authoritative interpretation
is the present note.
