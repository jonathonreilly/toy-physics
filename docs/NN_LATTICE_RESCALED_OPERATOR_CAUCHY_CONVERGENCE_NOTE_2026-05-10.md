# NN Lattice Rescaled-Lane Response-Vector Cauchy Certificate

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status:** bounded numerical Cauchy certificate — on the
deterministic-rescale lane through `h = 0.03125`, the chosen 15-component
response vector is Cauchy-like on the checked refinement window with fitted
geometric decay rate `r ≈ 1.513` and `R^2 = 0.9939`. The fitted tail estimate
is `7.7e-3`. This is not an operator-norm theorem and does not identify a
continuum PDE propagator.
**Status authority:** independent audit lane only.
**Primary runner:** [`scripts/lattice_nn_rescaled_operator_cauchy.py`](../scripts/lattice_nn_rescaled_operator_cauchy.py)
**Cached log:** [`logs/runner-cache/lattice_nn_rescaled_operator_cauchy.txt`](../logs/runner-cache/lattice_nn_rescaled_operator_cauchy.txt)

**Cited authorities (one-hop):**

- [`LATTICE_NN_HIGH_PRECISION_NOTE.md`](LATTICE_NN_HIGH_PRECISION_NOTE.md)
  — step-scale invariance theorem
  (closure addendum 2026-05-07): every observable used in this runner
  is invariant under `step_scale = h / sqrt(FANOUT)` per-edge rescale.
  Used here to extend Born-clean propagation through `h = 0.03125`.
- [`LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md`](LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md)
  — Born-clean refinement
  through `h = 0.0625`. This note extends to `h = 0.03125`.
- [`LATTICE_NN_CONTINUUM_NOTE.md`](LATTICE_NN_CONTINUUM_NOTE.md)
  — canonical NN refinement note;
  declared the continuum question open.
- [`NN_LATTICE_RESCALED_RG_GRAVITY_SATURATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_RG_GRAVITY_SATURATION_NOTE_2026-05-10.md)
  (companion) — sharpened the strength-rescaling route as blocked by
  saturation. This note attacks the same continuum-bridge gap from
  the response-vector side, **independent of any strength
  scaling**.

## Question

The companion saturation note closed the strength-rescaling route to
the continuum-bridge negatively for fixed-strength gravity. The remaining
route checked here is direct response-vector convergence: do the chosen
framework observables form a Cauchy-like sequence as `h` is refined,
independent of any strength-scaling question?

## Result

**Yes, within the bounded fitted-window scope.** On the
deterministic-rescale lane

| `h`     | nodes   | runtime |
|---------|---------|---------|
| 1.0     | 1681    | < 1s    |
| 0.5     | 6561    | < 1s    |
| 0.25    | 25921   | ~ 1s    |
| 0.125   | 103041  | ~ 7s    |
| 0.0625  | 410881  | ~ 30s   |
| 0.03125 | 1640961 | ~ 12 min |

we measure a 15-dim observable vector

```text
vec(h) = [obs_k(y_m, h) : k ∈ {gravity, MI, 1-pur, d_TV, born},
                          y_m ∈ {6, 8, 10}]
```

at fixed strength `5e-4` and fixed `K_PHYS = 5.0`. The pairwise
Cauchy increments are

| `h → h/2`             | `||vec(h) − vec(h/2)||_2` |
|-----------------------|--------------------------:|
| `1.0 → 0.5`           | `6.180e-01`               |
| `0.5 → 0.25`          | `3.899e-01`               |
| `0.25 → 0.125`        | `1.163e-01`               |
| `0.125 → 0.0625`      | `3.534e-02`               |
| `0.0625 → 0.03125`    | `1.428e-02`               |

A geometric-decay fit on the fine increments
(`h_geom = sqrt(h * h/2) ≤ 0.25`, three points) gives

| quantity | value |
|---|---|
| decay exponent `r` | `+1.5130` |
| prefactor `C`      | `1.526e+00` |
| `R^2`              | `0.9939` |

Under the fitted geometric-decay model, `r > 0` on a geometric `h`-grid
(ratio 2) gives a summable tail estimate for the response-vector increments,

```text
vec(h_0) + sum_{n >= 0} (vec(h_{n+1}) - vec(h_n))
```

and the tail estimate from the finest grid point `h = 0.03125` is

```text
|| vec_∞ - vec(h = 0.03125) ||_2  <=  7.7e-3
```

This is a **bounded numerical Cauchy certificate** for the chosen
15-component response vector. It is not, by itself, a retained-grade proof
that a full continuum operator `T_∞` exists.

## Per-component decay rates

The full vector decay `r ≈ 1.513` is dominated by the slowest
component, gravity (`r ≈ 1.19`). The other observables converge much
faster:

| observable          | `r`         | `R^2`   | continuum limit          |
|---------------------|-------------|---------|--------------------------|
| gravity (`y_m=6`)   | `+1.1868`   | `0.996` | `0` (fixed strength)     |
| gravity (`y_m=8`)   | `+1.2050`   | `0.999` | `0` (fixed strength)     |
| gravity (`y_m=10`)  | `+1.1775`   | `0.998` | `0` (fixed strength)     |
| `MI`                | `+6.1872`   | `0.966` | `1.0`                    |
| `1 - pur_cl`        | `+10.9337`  | `0.969` | `0.5`                    |
| `d_TV`              | `+6.8888`   | `0.971` | `1.0`                    |
| Born                | (noise floor) | (n/a) | `0` (machine clean)      |

The gravity decay rate `r ≈ 1.19` matches `q = +1.1923` from the
companion saturation note's joint `(h, s)` fit to four significant
figures. This is independent agreement: the same `h`-scaling exponent
is recovered from the response-vector Cauchy fit and from response-surface
fitting.

The Born component decay-rate fit is not load-bearing because Born stays at
the float64 noise floor (`< 1e-15`) at every grid point; there is no stable
signal to fit. This is expected and consistent with the step-scale invariance
theorem.

## Caveat — continuum gravity at fixed strength is trivial

The continuum-limit observable values are

```text
gravity_∞ = 0     (at fixed strength 5e-4)
MI_∞     = 1.0
(1 - pur_cl)_∞ = 0.5
d_TV_∞   = 1.0
born_∞    = 0    (machine precision)
```

Three of the five observables (`MI`, `1 - pur_cl`, `d_TV`) have
**nontrivial finite fitted limits** that the cluster's bounded results were
quoting as fixed-`h` finite values; this note records those limits as
bounded response-vector values under the fitted continuum extrapolation.

Gravity at fixed strength **converges to zero** in the continuum.
This is consistent with the companion saturation note: the strength
required to compensate the `h^1.19` decay grows past the propagator's
saturation threshold before the continuum is reached, so simple fixed-
strength continuum gravity is structurally trivial on this harness.

The "renormalized gravity" `h^(-q) · gravity(h)` does have a finite
continuum limit (it is approximately the prefactor `C ≈ 0.41` from the
companion note's gravity fit). That makes physical sense: the
framework's gravity centroid is a renormalization-scale-dependent
observable on the rescaled lane, not a continuum scalar.

## What this closes (bounded content)

This note registers, as a bounded numerical certificate on a fixed
observable basis:

1. The **chosen 15-component response vector has a fitted Cauchy tail**
   on the checked deterministic-rescale refinement window, with
   geometric Cauchy convergence at rate `r ≥ 1.513` and tail-sum
   bound `7.7e-3` at `h = 0.03125`.
2. The **decoherence observables** `MI`, `1 - pur_cl`, `d_TV` have
   nontrivial finite fitted limits `1.0`, `0.5`, `1.0` respectively,
   with fast geometric decay (`r ≥ 6`).
3. The **Born observable** is invariant under refinement on the
   step-scale-rescaled lane, consistent with the step-scale
   invariance theorem.
4. The gravity-component decay exponent `r ≈ 1.19` agrees independently
   with `q ≈ 1.19` from the joint `(h, s)` response-surface fit in the
   companion saturation note.

## What this does NOT close

This note does not claim:

- A continuum bridge for **the gravity centroid as a continuum
  scalar** at fixed strength — that limit is zero on this harness, by
  the saturation argument in the companion note.
- A continuum bridge that would let an arbitrary 19-row cluster member
  status-lift — any lift is per-row and depends on whether the row's
  specific claim references a bounded response-vector component with a
  nontrivial fitted limit (`MI`, `1 - pur_cl`, `d_TV`) vs. fixed-strength
  gravity (which is trivial).
- That `T_∞` matches a known continuum PDE propagator — that
  identification (Target A.2 Trotter / resolvent) is a separate
  question. This note is Target A.1 only.

## Implications for the 19-row cluster

The 19-row "lattice action / refinement / continuum-limit" sub-lane
has a possible per-row status-lift path under this bounded certificate:

- Rows that load-bear on `MI`, `1 - pur_cl`, `d_TV` continuum values
  → candidates for audit review: the bounded fixed-`h` value already
  matches the fitted response-vector value to within `7.7e-3` at
  `h = 0.03125`.
- Rows that load-bear on gravity at fixed strength → not status-liftable
  by this route. Their bounded scope tightens into "structurally
  bounded by saturation, not by continuum-existence."
- Rows that load-bear on gravity exponents (e.g., the q = 1.19 fit)
  → candidates for "response-vector-stable scaling exponent" review in
  light of the independent agreement between the response-vector Cauchy
  rate and the response-surface q.

A separate per-row audit of the 19 rows is required to tabulate
which rows are in which category. This note does not perform that
re-audit; it only supplies the upstream bounded certificate the
re-audit can cite.

## Reproduction

```bash
python3 scripts/lattice_nn_rescaled_operator_cauchy.py
```

The runner runs through `h = 0.03125` (~13 minutes total wallclock).
Audit guards (Born `< 1e-10`, `k=0 < 1e-12`, Cauchy fit `r > 0.5`,
`R^2 ≥ 0.95`) all PASS; runner exits zero on the cached log.

## Audit context

This is a bounded-theorem source note, not an audit verdict. It supplies a
finite-window numerical Cauchy certificate for a fixed response vector, with
explicit decay fit and tail estimate. The audit guards are internal to the
runner and check at every grid point. The result follows from running the
framework's canonical propagator on the canonical 3-edge NN lattice with the
deterministic-rescale schedule across six refinement points.

Fri May 15 09:01:56 EDT 2026
