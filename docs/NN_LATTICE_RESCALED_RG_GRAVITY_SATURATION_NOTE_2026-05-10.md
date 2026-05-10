# NN Lattice Rescaled-Lane RG Gravity Saturation Note

**Date:** 2026-05-10
**Type:** bounded_theorem (negative-result sharpening)
**Status:** bounded sharpened null-result — on the deterministic-rescale lane through `h = 0.0625`, simple power-law strength rescaling cannot give a continuum-limit gravity centroid. The blocker is identified as the `sqrt(lf)` leading order of the per-edge action, not the strength-scaling exponent choice.
**Status authority:** independent audit lane only.
**Primary runner:** [`scripts/lattice_nn_rescaled_response_exponents.py`](../scripts/lattice_nn_rescaled_response_exponents.py)
**Companion runner:** [`scripts/lattice_nn_rescaled_rg_gravity.py`](../scripts/lattice_nn_rescaled_rg_gravity.py)
**Cited authorities (one-hop):**

- `LATTICE_NN_HIGH_PRECISION_NOTE.md` — step-scale invariance theorem
  (closure addendum 2026-05-07): every framework observable is invariant
  under the deterministic per-edge rescale `step_scale = h / sqrt(FANOUT)`,
  because each observable is a ratio of two equal-degree amplitude
  polynomials. Verified on a small lattice to float64 precision. Used
  here to extend the propagation through `h = 0.0625` Born-clean.
- `LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md` — Born-clean refinement
  through `h = 0.0625` on the deterministic-rescale lane.
- `LATTICE_NN_RG_GRAVITY_NOTE.md` — earlier strength-scaling sweeps on
  the **raw** (no-rescale) kernel, all of which failed at `h = 0.125`
  because of float64 overflow rather than physics.
- `LATTICE_NN_CONTINUUM_NOTE.md` — canonical NN refinement note.

This note is a **sharpening** of the bounded null-result in
`LATTICE_NN_RG_GRAVITY_NOTE.md`. The earlier note left the strength-
scaling question open at finer spacing. This note closes it negatively
on a Born-clean refinement window two steps finer than the earlier work
could reach, by combining the step-scale invariance theorem with the
RG-style strength schemes.

## Question

On the deterministic-rescale lane (where the step-scale invariance
theorem extends Born-clean propagation through `h = 0.0625`), does any
simple power-law strength rescaling

```text
s(h) = BASE * h^(-r),   r ∈ R
```

give a continuum-limit gravity centroid (gravity h-stable as h → 0) on
the standard 3-edge NN harness?

## Result

**No.** The harness has a clean joint power-law response

```text
|gravity(h, s)| = A * h^q * s^p
```

with fitted exponents (fine-h subset `h ∈ {0.25, 0.125, 0.0625}`, 15 points,
strength grid `s ∈ {1.25e-4, 2.5e-4, 5e-4, 1e-3, 2e-3}`):

| quantity | value |
|---|---|
| `q`        | `+1.1923` |
| `p`        | `+0.4468` |
| `A`        | `1.198e+01` |
| `R^2`      | `0.9997` |
| Born `max` | `5.24e-16` |
| `k=0 max`  | `0.00e+00` |

The `p ≈ 0.45 ≈ 1/2` is the analytic prediction from the propagator's
per-edge action

```text
act = dl - ret = L * (1 + lf) - sqrt(L^2 * (1 + lf)^2 - L^2)
```

For small `lf`,

```text
sqrt(L^2 * (1+lf)^2 - L^2) = L * sqrt((1+lf)^2 - 1)
                            = L * sqrt(2*lf + lf^2)
                           ~  L * sqrt(2*lf)         (lf -> 0)
```

so the action's leading deviation from the field-free value is
`-L * sqrt(2*lf)`, **square root, not linear, in the field strength**.
This dictates the empirical `p ≈ 1/2`.

Continuum-stable gravity at fixed `s_BASE` would require strength
scaling

```text
s_critical(h) = const * h^(-q/p)
              = const * h^(-2.6684)
```

With the prefactor fixed so that `s_critical(h = 0.5) = 5e-4`, the
critical strength at `h = 0.0625` is `1.285e-1`, which is well above
the saturation threshold `~0.01` at which `lf` exits the leading-`sqrt`
regime in the harness's typical-`r ~ 5` source field. Therefore any
power-law schedule that compensates the `h^1.19` decay enters the
nonlinear-saturated propagator regime before reaching `h = 0.0625`,
and the linear-`p` extrapolation to a continuum-stable response
breaks down inside the refinement window.

## What is closed

- the deterministic-rescale lane is **Born-clean and `k=0`-clean**
  through `h = 0.0625` for every strength scheme tested
  (`fixed`, `1/sqrt(h)`, `1/h`, `1/h^1.19`, `1/h^1.5`)
- the harness's gravity response on the rescaled lane has a
  **clean joint power law in `(h, s)`** at `R^2 = 0.9997`
- the strength-response exponent `p ≈ 1/2` matches the analytic
  prediction from the `sqrt(lf)`-leading per-edge action
- no simple power-law strength schedule gives a continuum-limit
  gravity centroid on this harness — the route is structurally
  blocked at `s_critical(0.0625) ~ 0.13 >> 0.01`

## What is NOT closed

This note **does not** claim:

- that a continuum-limit gravity is unreachable on any NN-lattice
  variant (only that simple power-law strength scaling on the
  standard 3-edge harness is insufficient)
- that the per-edge action choice in the framework is the only
  possible action — different choices (e.g. an `act` that is
  linear in `lf` to leading order rather than `sqrt(lf)`) would
  evade this saturation obstruction and require a separate study
- promotion of the 19-row "lattice action / refinement /
  continuum-limit" sub-lane — this sharpened null-result tightens
  the bounded scope of those rows but does not open a promotion
  path

## What this implies for the cluster

The 19-row retained-bounded "lattice action / refinement /
continuum-limit" sub-lane (see
`docs/audit/FRONTIER_ROADMAP_2026-05-09.md`) cannot be promoted by the
straight-RG-strength-rescaling route. The remaining promotion routes
listed in the bridge gap analysis (Target A.1 polynomial-truncation
operator-norm convergence; Target A.2 Trotter / resolvent
identification; Target A.3 tightness + identification) are independent
of this saturation obstruction and remain open.

The saturation obstruction is **structural** to the propagator's
choice of action `act = dl - ret`. A successor lane that wants to
promote the cluster via a continuum-bridge route must either:

1. select a propagator whose per-edge action is linear-in-`lf` to
   leading order (different framework choice), or
2. work in the linear-`sqrt` regime by holding `s_critical` below the
   saturation threshold across a refinement window finer than
   `h = 0.0625` (requires either much smaller observable signals or a
   much larger lattice), or
3. directly identify the `h → 0` operator limit on the rescaled lane
   via Target A.1/A.2/A.3, bypassing the strength-scaling question.

## Reproduction

```bash
python3 scripts/lattice_nn_rescaled_rg_gravity.py
python3 scripts/lattice_nn_rescaled_response_exponents.py
```

Each runner prints its full grid and an analysis block. The exponent
fits and saturation check come from the second runner; the first
runner is the broader sweep across `{fixed, 1/sqrt(h), 1/h,
1/h^1.19, 1/h^1.5}`.

## Audit context

This is a class-A bounded-theorem sharpening of an existing bounded
null-result. The audit guards (Born `< 1e-10`, `k=0 < 1e-12`, joint
fit `R^2 > 0.99`) are checked by both runners and are part of the
audit packet. The result follows from running the framework's
canonical propagator on the canonical 3-edge NN lattice with the
deterministic-rescale schedule.
