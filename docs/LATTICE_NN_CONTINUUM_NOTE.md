# Nearest-Neighbor Lattice Refinement Note

**Date:** 2026-04-03 (continuum-bridge identification addendum 2026-05-10)  
**Status:** bounded refinement window through `h = 0.25` (the original bounded
scope) PLUS continuum-operator-stable decoherence observables (`MI`, `1-pur`,
`d_TV`, `Born`) identified by the geodesic-continuum bridge (see
`NN_LATTICE_RESCALED_OPERATOR_CAUCHY_CONVERGENCE_NOTE_2026-05-10.md` /
`NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md` /
`NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`); `h = 0.125` on the
raw (non-rescaled) kernel remains an open gate.

**Claim type:** bounded_theorem

**Claim scope:** raw nearest-neighbor lattice refinement is Born-clean through
`h = 0.25` (the original bounded scope); the decoherence observables on that
window are now continuum-operator-stable values matching the geodesic
identification within 7.7e-3 at `h = 0.03125` (PR #957) and within 5e-4 on the
Gaussian-arm prediction (PR #968); the fixed-strength gravity centroid remains
bounded, and that bound is now structurally identified (geodesic limit gives 0;
strength-saturation in PR #945 explains why simple strength-rescaling cannot
lift it); `h = 0.125` and finer on the raw (non-rescaled) kernel remain open.

This note freezes the canonical raw nearest-neighbor lattice refinement run.
It is intentionally narrow:

- it does **not** claim a full continuum limit
- it does **not** use fan-out normalization or layer normalization
- it keeps the standard linear propagator only
- it treats `h = 0.125` as an unresolved gate, not as part of the
  finite-spacing window

Artifacts:

- [`scripts/lattice_nn_continuum.py`](../scripts/lattice_nn_continuum.py)
- [`logs/runner-cache/lattice_nn_continuum.txt`](../logs/runner-cache/lattice_nn_continuum.txt)

## Claim Boundary

The load-bearing claim is exactly the finite-window statement

```text
H_finite = {2.0, 1.0, 0.5, 0.25}
```

for the raw nearest-neighbor runner. A row belongs to this window only if the
same harness returns finite values for the gravity, `k=0`, `MI`, classical
purity, total-variation, and Born checks. The next requested spacing,
`h = 0.125`, is a gate row: because the raw runner reports `FAIL`, it is not
part of `H_finite` and cannot be used for a continuum or finer-spacing claim.

## Canonical Finite Window

The raw NN lattice is Born-clean through the last successful spacing:

| `h` | nodes | gravity | `k=0` | `MI` | `1-pur` | `d_TV` | Born |
|---|---:|---:|---:|---:|---:|---:|---:|
| `2.0` | `441` | `-0.775486` | `0.00e+00` | `0.5558` | `0.4215` | `0.7498` | `2.88e-16` |
| `1.0` | `1681` | `-0.116678` | `0.00e+00` | `0.5022` | `0.4229` | `0.7455` | `6.02e-16` |
| `0.5` | `6561` | `+0.138226` | `0.00e+00` | `0.7420` | `0.4844` | `0.9072` | `2.26e-16` |
| `0.25` | `25921` | `+0.077415` | `0.00e+00` | `0.9470` | `0.4989` | `0.9878` | `3.83e-16` |

Safe read:

- gravity flips sign and becomes positive by `h = 0.5`
- `MI` rises strongly toward `1` by `h = 0.25`
- `1-pur` rises toward `0.5`
- `d_TV` rises toward `1`
- Born stays at machine precision on the finite window
- `k=0` stays exactly zero

## Finite-Window Derivation Chain

The closure is computational and bounded, not asymptotic:

1. `generate_nn_lattice(h)` fixes the raw family: each interior node has the
   same three forward nearest-neighbor edges, with physical `W`, `L`, slit
   location, mass location, `K_PHYS`, `BETA`, and `LAM` held fixed by the
   runner.
2. `measure_full(h)` applies the same propagator and observable definitions to
   every requested spacing. No row in `H_finite` uses fan-out normalization, layer
   normalization, a fitted selector, or an observed target value.
3. For every `h` in `H_finite`, the runner returns a finite row with `k=0 =
   0.00e+00` and Born residual below the stated audit tolerance
   `1e-10`. The worst cached finite-window Born residual is `6.02e-16`.
4. The "positive refinement trend" is therefore only the finite-row trend shown
   in the table: the refined rows `h = 0.5` and `h = 0.25` have positive
   gravity response, while `MI`, `1-pur`, and `d_TV` move toward the listed
   endpoint diagnostics on the last successful refinements.
5. The same runner then reports `FAIL` at `h = 0.125`. That failure blocks
   extending the window, so the derivation stops at `H_finite` and leaves the
   continuum question open.

Thus the auditable implication is:

```text
raw NN harness + finite runner rows through h = 0.25
  => Born-clean finite-spacing refinement window H_finite
raw NN harness + FAIL at h = 0.125
  => open finer-spacing/continuum gate
```

## Unresolved Point

The raw kernel overflows at `h = 0.125` in the canonical run.

That means:

- the refinement trend is real on the finite window
- the next finer point is not yet frozen
- a full continuum claim is not review-safe yet

## Safe Conclusion

The correct wording is:

- the nearest-neighbor lattice shows a **Born-clean positive refinement trend through `h = 0.25`**
- the raw kernel has a **computational resolution limit** at finer spacing
- the continuum question remains open on the raw kernel; the decoherence
  observables on the bounded raw window are now identified with the
  continuum-stable geodesic operator (see the 2026-05-10 addendum below)

Do **not** promote this note to a full continuum theorem on the raw kernel;
the scope extension covers the decoherence observables only.

## 2026-05-10 Continuum-Bridge Identification (Scope Extension)

This addendum lifts the load-bearing decoherence-observable claims (`MI`,
`1-pur`, `d_TV`, `Born`) on the bounded raw window from "fixed-`h` finite
values" to "continuum-operator-stable values" by citing an upstream
identification produced on the deterministic-rescale companion harness. The
bounded harness scope (`BETA = 0.8`, `K_PHYS = 5.0`, slits at `±3`, `L = 40`)
is unchanged; this is a **scope extension, not a tier upgrade**.

Upstream load-bearing dependencies (each a single open PR against `main`):

- [`NN_LATTICE_RESCALED_OPERATOR_CAUCHY_CONVERGENCE_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_OPERATOR_CAUCHY_CONVERGENCE_NOTE_2026-05-10.md)
  (PR #957) — `T_∞` exists on the 15-dim observable subspace of the rescaled
  NN harness; Cauchy convergence at `r ≥ 1.51`; tail-bound `7.7e-3` at
  `h = 0.03125`.
- [`NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md)
  (PR #968) — `T_∞` identified as the geodesic operator on the slit-detector
  decoherence subblock; `σ_arm(h) = C_arm · h^0.526`, `R² = 0.9996`; the
  Gaussian-arm prediction matches `MI` / `d_TV` to `5e-4`.
- [`NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md)
  (PR #1003) — closed-form analytic derivation of `C_arm = 2.4855` with `8.3%`
  residual against the numerical `C_arm = 2.7107`.

Consequences for this note:

- the `MI`, `1-pur`, `d_TV`, `Born` columns of the canonical finite window are
  no longer load-bearing only as "bounded fixed-`h` finite values" — they are
  now load-bearing as continuum-operator-stable values matching the geodesic
  identification to the tolerances above.
- the gravity centroid at fixed strength remains bounded on this note; the
  bound is now identified as **structural** (the geodesic limit gives 0, and
  the strength-saturation observation in PR #945 explains why simple
  strength-rescaling cannot lift it). This identification does **not** widen
  the gravity claim — it only labels its known bound.
- the raw `h = 0.125` gate is untouched: the raw kernel still fails there, and
  the sub-`0.25` regime on the raw harness remains open. The continuum-stable
  observables live on the deterministic-rescale companion harness, not on the
  raw kernel.
- `claim_type` stays `bounded_theorem`; the rows are still bounded by the
  fixed harness parameters above.
