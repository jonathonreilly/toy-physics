# Rescaled NN Lattice c2_inf Analytic Derivation Note

**Date:** 2026-05-10
**Claim type:** positive_theorem (analytic-vs-empirical residual 0.12% in the
h -> 0 saddle, < 1% per-h on all four PR #997 fit points; well inside the 10%
positive-theorem band)
**Proposal allowed:** false
**Status authority:** source-note proposal only; audit verdict and effective
status are set by the independent audit lane.
**Primary runner:** [`scripts/lattice_nn_rescaled_c2_derivation.py`](../scripts/lattice_nn_rescaled_c2_derivation.py)
**Companion magnitude derivation:** [`docs/NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md)
**Trigger:** PR #997 (kernel-identification runner): the single-source,
field-free, no-slit detector amplitude `A(y_d)` on the rescaled NN lane has
Gaussian magnitude and quadratic phase at every h tested. The quadratic-phase
coefficient `c2(h)` converges to a finite `c2_inf ~= 0.02995`, with the
empirical approximation `c2_inf ~= K_PHYS / (4 L_total) = 0.03125` accurate
to ~4%. The closed-form derivation of `c2_inf` was left open in PR #997.

## Claim

The quadratic-in-`y_d` coefficient of `arg A(y_d)`, in the continuum limit of
the deterministic-rescale lane, is

```text
c2_inf  =  k * (2 - sqrt(2)) / (4 * c * L_total)
```

with `c = exp(-BETA * pi^2 / 16)` the diy = +/- 1 angular weight at
`theta = pi/4`. With harness parameters `BETA = 0.8`, `k = K_PHYS = 5.0`,
`L_total = 40`:

```text
c2_inf_analytic  =  0.029985
```

versus

```text
c2_inf_empirical =  0.02995    (PR #997, h = 0.0625; cached log).
```

Residual `+0.12%`. The empirical heuristic `K_PHYS / (4 L_total) = 0.03125`
is recovered up to the factor `(2 - sqrt(2)) / c ~= 0.9596`, which is what
carries the residual ~4% gap PR #997 noted between `K/(4L)` and the measured
0.02995. The proximity of `(2 - sqrt(2)) / c` to 1 is the reason the empirical
fit looked like `K/(4L)` at the few-percent level.

## Imported Authorities

| Authority | Role |
|---|---|
| [`docs/NN_LATTICE_RESCALED_KERNEL_IDENTIFICATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_KERNEL_IDENTIFICATION_NOTE_2026-05-10.md) (PR #997) | empirical anchor — measured c2_inf and the K/(4L) heuristic; this note's quantitative target. |
| [`docs/NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md) (PR #1003) | companion magnitude derivation — same saddle-point machinery, applied to `Re(r)`. This note applies the saddle to `Im(r)`. |
| [`docs/LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md`](LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md) | freezes the deterministic-rescale schedule, the per-step factor `step_scale = h / sqrt(FANOUT)`, and the harness parameters used here. |

This note is a closed-form derivation note. It does not introduce a new axiom,
does not modify any retained theorem family, and does not promote any status
row.

## Derivation

### 1. Per-edge phase and the `Sigma diy_i^2` constraint

On the rescaled NN lane, an edge from `(layer, iy)` to `(layer+1, iy + diy)`
with `diy in {-1, 0, +1}` carries the framework factor

```text
f(diy; h)  =  step_scale  *  exp(i k L_edge)  *  exp(-BETA theta^2)  /  L_edge
```

with `step_scale = h / sqrt(FANOUT)`, `L_edge = h sqrt(1 + diy^2)`, and
`theta = atan2(|diy|, 1)`. Linearizing `L_edge` in small h (small diy):

```text
L_edge / h  =  sqrt(1 + diy^2)  =  1  +  diy^2 / 2  +  O(diy^4).
```

The per-edge phase is `k h sqrt(1 + diy^2) = k h + (k h / 2) diy^2 + O((kh)·diy^4)`.
Summing over `N = L_total / h` edges, the total path phase is

```text
phi_path  =  k h * N  +  (k h / 2) Sigma_i diy_i^2  +  O(...)
          =  k L_total  +  (k h / 2) Sigma_i diy_i^2.
```

The first term is path-independent (a global drift). The second depends on the
path only through `Sigma_i diy_i^2`, NOT through the lateral displacement
`Sigma_i diy_i = (y_d - y_s)/h`. The quadratic dependence on `y_d` therefore
comes from how `Sigma_i diy_i^2` correlates with the displacement under the
constraint `Sigma_i diy_i = (y_d - y_s)/h`.

This is exactly the saddle-point structure PR #1003 used for the magnitude:
the per-step lateral characteristic function packages this constraint into a
Gaussian in `q`, and the lateral Fourier transform converts that into a
Gaussian in `y`. The real and imaginary parts of the Gaussian's covariance
become the magnitude width and the phase Hessian, respectively.

### 2. Lateral characteristic function (per PR #1003)

```text
g(q; h)  =  a_0(h)  +  a_pm(h) exp(+i q h)  +  a_pm(h) exp(-i q h)
        =  a_0(h)  +  2 a_pm(h) cos(q h),
```

with

```text
a_0(h)   =  exp(i k h)              /  sqrt(FANOUT)
a_pm(h)  =  c * exp(i k h sqrt(2))  /  sqrt(2 * FANOUT),    c = exp(-BETA pi^2 / 16).
```

The lateral path amplitude over `N = L_total / h` edges is `G_N(q) = g(q;h)^N`,
and the position amplitude at the detector is

```text
A(y)  =  (1 / 2 pi)  integral  dq  g(q;h)^N  exp(-i q y).
```

### 3. Saddle-point expansion at q = 0

`g(q;h)` is even in `q` because `a_+ = a_- = a_pm`, so its first q-derivative
at `q = 0` vanishes. The Taylor expansion to second order is

```text
g(q; h)  =  g(0; h)  -  a_pm(h) (q h)^2  +  O((q h)^4),
```

so

```text
log(g(q;h) / g(0;h))  =  -r(h) (q h)^2  +  O((q h)^4),
                with  r(h)  :=  a_pm(h) / g(0; h)   (complex in general),
```

and

```text
g(q;h)^N  =  g(0;h)^N  *  exp( -N r(h) (q h)^2  +  O((q h)^4) ).
```

This is the **saddle-point equation**: `g(q)^N` is a complex Gaussian in `q`
centered at the saddle `q = 0` with complex covariance `1 / (2 N r(h) h^2)`.

### 4. The 1-D Hessian at the saddle

The exponent's q-Hessian at the saddle is

```text
H(h)  :=  d^2/dq^2 [ -N log g(q; h) ] |_{q=0}  =  2 N r(h) h^2  =  2 L_total r(h) h.
```

This is the lateral saddle's complex Hessian. Its real and imaginary parts
play distinct roles:

- `Re(H) = 2 L_total Re(r) h`: sets the lateral Gaussian width of the
  saddle-integrated amplitude. (PR #1003.)
- `Im(H) = 2 L_total Im(r) h`: sets the lateral Gaussian's phase curvature.

In the continuum `h -> 0` the per-step phase ramp `exp(i k h (sqrt(2) - 1))`
linearizes, `Im(r) ~ h` linearly with `h`, so `Im(H) / h` stabilizes to a
finite continuum value — this is what allows c2 to have a finite continuum
limit even though `Im(H) -> 0`.

The determinant of the 1-D Hessian is `H` itself; the lateral saddle is 1-D
so there are no off-diagonal couplings.

### 5. Position amplitude as a complex Gaussian in y

Fourier-transforming the q-Gaussian:

```text
A(y)  =  g(0;h)^N  *  ( 1 / sqrt(4 pi N r h^2) )  *  exp( - y^2 / (4 N r h^2) ).
```

Splitting `r = Re(r) + i Im(r)` and using `1 / r = conj(r) / |r|^2`:

```text
- y^2 / (4 N r h^2)
   =  - y^2 * (Re(r) - i Im(r)) / (4 N h^2 |r|^2)
   =  - y^2 * Re(r) / (4 N h^2 |r|^2)
     + i * y^2 * Im(r) / (4 N h^2 |r|^2).
```

The real part is the Gaussian magnitude decay (PR #1003):

```text
|A(y)|^2  proportional to  exp( - y^2 * Re(r) / (2 N h^2 |r|^2) ),
sigma_arm^2  =  N h^2 |r|^2 / Re(r)  =  L_total h |r|^2 / Re(r).
```

The imaginary part is the **quadratic phase** contributed by the lateral
saddle:

```text
arg A(y)  ⊇  y^2 * Im(r) / (4 N h^2 |r|^2)  =  c2(h) * y^2,
c2(h)  =  Im(r) / (4 N h^2 |r|^2)  =  Im(r) / (4 L_total h |r|^2).
```

Additional y-independent phase comes from `g(0)^N`'s global path-length
drift `k L_total + O(k h)` and from `arg(1/sqrt(4 pi N r h^2))`, which contributes
a y-independent constant. Neither affects the quadratic-in-y coefficient.

### 6. Simplification with the harness amplitudes

Use `r = a_pm / g(0)` with `g(0) = a_0 + 2 a_pm`:

```text
Im(r)  =  Im( a_pm * conj(g(0)) ) / |g(0)|^2,
|r|^2  =  |a_pm|^2 / |g(0)|^2.
```

So

```text
Im(r) / |r|^2  =  Im(a_pm * conj(g(0))) / |a_pm|^2.
```

Now `a_pm * conj(g(0)) = a_pm * conj(a_0) + 2 |a_pm|^2`. The `2 |a_pm|^2`
piece is real, so its imaginary part vanishes:

```text
Im(a_pm * conj(g(0)))  =  Im( a_pm * conj(a_0) ).
```

Hence the closed form

```text
c2(h)  =  Im( a_pm(h) * conj(a_0(h)) )  /  ( 4 L_total h |a_pm(h)|^2 ).
```

### 7. Numerical reduction

`a_pm * conj(a_0) = (c / sqrt(2 FANOUT)) * (1 / sqrt(FANOUT)) *
exp(i k h (sqrt(2) - 1)) = c / (sqrt(2) FANOUT) * exp(i k h (sqrt(2) - 1))`,
so

```text
Im( a_pm * conj(a_0) )  =  ( c / (sqrt(2) FANOUT) )  *  sin( k h (sqrt(2) - 1) ).
```

With `|a_pm|^2 = c^2 / (2 FANOUT)`:

```text
c2(h)  =  [ c / (sqrt(2) FANOUT) * sin( k h (sqrt(2) - 1) ) ]
            / [ 4 L_total h * c^2 / (2 FANOUT) ]
        =  sin( k h (sqrt(2) - 1) )  /  ( 2 sqrt(2) * c * L_total * h ).
```

### 8. Continuum limit (`h -> 0`)

Use `sin(x) ~ x`:

```text
c2_inf  =  k * (sqrt(2) - 1)  /  ( 2 sqrt(2) * c * L_total )
       =  k * (2 - sqrt(2))   /  ( 4 c L_total ).
```

This is the parameter-free closed form for `c2_inf` in the geodesic
(continuum) limit.

### 9. Numerical evaluation

With `BETA = 0.8`, `k = 5`, `L_total = 40`, `FANOUT = 3`:

```text
c                  =  exp(-0.8 * pi^2 / 16)            =  0.61050
2 - sqrt(2)        =                                       0.58579
(2 - sqrt(2)) / c  =                                       0.95952
c2_inf_analytic    =  5 * 0.58579 / (4 * 0.61050 * 40)  =  0.029985
```

versus

```text
c2_inf_empirical   =  0.02995    (PR #997 finest h = 0.0625)
K_PHYS / (4 L)     =  0.03125    (empirical heuristic, ~4% above c2_inf)
K_PHYS / (2 L)     =  0.06250    (naive ray-optics, 2x off; ruled out by data)
```

Residuals:

| Estimate | Value | Residual vs 0.02995 |
|---|---:|---:|
| **Saddle-point closed form (this note)** | **0.029985** | **+0.12%** |
| Empirical heuristic `K/(4L)` | 0.031250 | +4.34% |
| Ray-optics `K/(2L)` (PR #997 null) | 0.062500 | +108.7% |
| Saddle with wrong `L = L_2 = 2L/3` | 0.044978 | +50.18% |

### 10. Per-h cross-check with the finite-h sin(...) formula

Retaining the full `sin(k h (sqrt(2) - 1))` factor before linearizing:

```text
c2(h)  =  sin( k h (sqrt(2) - 1) )  /  ( 2 sqrt(2) c L_total h ).
```

Evaluated at the four PR #997 fit points:

| `h` | `c2_analytic(h)` | `c2_empirical(h)` (PR #997) | residual |
|---|---:|---:|---:|
| 0.5    | 0.024906 | 0.025062 | -0.62% |
| 0.25   | 0.028663 | 0.028768 | -0.36% |
| 0.125  | 0.029651 | 0.029676 | -0.08% |
| 0.0625 | 0.029901 | 0.029886 | +0.05% |

All four points agree with the PR #997 measurement to within ~1%, with the
fit-residual systematically approaching zero as `h -> 0` — consistent with
the saddle being valid up to `O((q h)^4)` corrections that decouple in the
continuum limit.

## Length identification: why `L_total`, not `L_2` (the load-bearing physics step)

The companion magnitude derivation (PR #1003) used `L_eff = L_2 = 2 L_total / 3`
because that harness places a slit at layer `nl // 3`, and the per-arm
magnitude on the detector is set by post-slit spreading. For the **phase**
side, in the harness used by PR #997 (single source at origin, no slits, no
blocked nodes, no field), there is **no slit anchoring** — the saddle's
characteristic function integrates over all paths from source to detector
through the full `L_total = 40` lattice depth. The propagation length entering
the saddle is `L_total`.

Quantitative test of this identification: the closed form

```text
c2_inf(L)  =  k (2 - sqrt(2)) / (4 c L)
```

evaluated at the two candidate lengths gives

- `L = L_total = 40`: c2_inf = 0.029985 (residual `+0.12%`),
- `L = L_2 = 26.67`: c2_inf = 0.044978 (residual `+50.18%`).

The `L_total` choice wins by a factor of ~400 in residual. So:

- In PR #1003's slit harness, the magnitude saddle integrates over post-slit
  paths only, anchored at the slit -> `L_eff = L_2`.
- In PR #997's slit-free harness, the phase saddle integrates over all
  source-to-detector paths -> `L_eff = L_total`.

This is the structural asymmetry between the two derivations. They are not
in tension: they apply the same saddle machinery to different harnesses.

## Cross-validation table

Closed-form residuals at the harness-fixed parameters (no Monte Carlo):

| Estimate | Formula | Value | Residual vs 0.02995 |
|---|---|---:|---:|
| **Saddle, `L = L_total`** | **`k (2 - sqrt(2)) / (4 c L_total)`** | **0.029985** | **+0.12%** |
| Empirical heuristic | `K_PHYS / (4 L_total)` | 0.031250 | +4.34% |
| Saddle, `L = L_2` (wrong) | `k (2 - sqrt(2)) / (4 c L_2)` | 0.044978 | +50.18% |
| Ray-optics (PR #997 null) | `K_PHYS / (2 L_total)` | 0.062500 | +108.7% |

The saddle-point form sharpens the empirical `K/(4L)` heuristic by a factor
of ~36 in residual. The two "wrong" alternatives (L_2 length, ray-optics
prefactor) both land far outside the 10% positive-theorem band, providing
sharp falsifiability.

## Hessian and saddle geometry

The lateral saddle is one-dimensional. Its complex Hessian at `q = 0` is

```text
H(h)  =  2 L_total * r(h) * h,    r(h) = a_pm(h) / g(0; h).
```

Per-h values from the runner:

| `h` | Re(H) | Im(H) | Re(H)/h | Im(H)/h |
|---|---:|---:|---:|---:|
| 0.5    | 9.0306 | 5.6555 | 18.06 | 11.31 |
| 0.25   | 4.6078 | 1.3165 | 18.43 | 5.27  |
| 0.125  | 2.3136 | 0.3236 | 18.51 | 2.59  |
| 0.0625 | 1.1580 | 0.0806 | 18.53 | 1.29  |

Re(H)/h converges to `2 L_total * Re(r)|_{h->0}` ≈ 18.53. Im(H)/h converges
to `2 L_total * (k (sqrt(2)-1) c) / (FANOUT (1 + sqrt(2) c)^2 / FANOUT) * (1/h) * h`
≈ 1.29 → 0 only because `Im(r)` itself ~ h. The combination

```text
c2(h)  =  Im(r) / (4 L_total h |r|^2),
```

with `Im(r) ~ h * Im(r)_lin` and `|r|^2 -> Re(r)|_0^2`, has a finite continuum
limit `c2_inf = Im(r)_lin / (4 L_total Re(r)|_0^2)` ≈ 0.029985. This is the
phase-Hessian survival mechanism: even though `H -> 0` like `h`, the ratio
`Im(H) / (4 L_total |H/h|^2 h^2) = Im(r) / (4 L_total h |r|^2)` is `O(h^0)`.

## Reproducibility

```bash
python3 scripts/lattice_nn_rescaled_c2_derivation.py
```

Prints all five stages: the saddle-point closed form, harness-amplitude
reduction, length identification (with cross-check against `L = L_2`),
per-h table against PR #997's measured `c2(h)`, and the saddle-Hessian
diagnostic. Runner is closed-form (no Monte Carlo, no lattice propagation);
depends only on `BETA`, `K_PHYS`, `PHYS_L`, `FANOUT` from the upstream harness
script, and is independent of the slit-plane fraction (which is included only
as a cross-check that the wrong-length alternative gives a 50% residual).

The runner also asserts internal consistency: the harness-amplitude saddle
formula and the explicit `sin(...)` closed form give bit-identical numbers
at each h (assertion-checked in `report()`).

## Bounded scope

This note derives `c2_inf` for the **no-slit, single-source, field-free**
harness used by PR #997. It does not:

- prove the magnitude side; that is PR #1003's job and that derivation uses
  `L_eff = L_2` for the slit harness.
- close the formal `O((q h)^4)` correction in the saddle expansion. The
  ~1% per-h residual at h = 0.5 is consistent with a `(k h)^2` correction
  to the saddle's Gaussian approximation; it shrinks as `(k h)^2` does.
- claim the analytic formula holds outside the rescaled-NN deterministic-
  rescale lane (`step_scale = h / sqrt(FANOUT)` is baked into the per-step
  amplitudes).
- claim a positive Schrödinger free-particle identification. PR #997's null
  stands: the same `c2_inf` value is incompatible with the Gaussian width's
  separate scaling. This note derives the **phase** side closed-form; the
  width side is the geodesic mechanism (PR #968), and PR #997 already
  documented that no single Schrödinger `m_eff` reconciles both.

## What this closes

- A positive analytic derivation of `c2_inf` to 0.12% versus PR #997's
  empirical extrapolation. The closed form is `c2_inf = k (2 - sqrt(2))
  / (4 c L_total)`.
- The factor `(2 - sqrt(2)) / c ~= 0.96` is identified as the source of
  the ~4% gap PR #997 noted between `K/(4L)` and the measured `c2_inf`.
  `K/(4L)` is the heuristic; the actual closed form has the explicit
  `(2 - sqrt(2)) / c` correction.
- A clean structural pairing with PR #1003: both derivations use the same
  per-step lateral characteristic function `g(q;h) = a_0 + 2 a_pm cos(qh)`
  and the same Gaussian saddle at `q = 0`. The magnitude side reads off
  `Re(r)`; the phase side reads off `Im(r)`. Together they reconstruct
  the full complex Gaussian.

## What this does NOT close

- A positive continuum identification of `T_inf`'s scattering kernel as a
  recognized PDE propagator. PR #997's null-result stands: the magnitude
  collapses to a delta in `y` (sigma -> 0) while the phase Hessian survives
  (c2_inf finite), giving `K_inf(y_d) ~ delta(y_d) * exp(i c2_inf y_d^2)`
  in a distributional sense. The Schrödinger free-particle propagator is
  ruled out because it cannot have both behaviors with a single `m_eff`.
- A general theorem outside the harness-specific parameters. The closed form
  has explicit `k`, `c`, `L_total` dependence; other parameter choices give
  different `c2_inf`. The dimensional structure `c2 ~ k / L` is universal in
  the saddle expansion, but the prefactor `(2 - sqrt(2)) / (4 c)` is
  harness-specific.

## Status

This source note is a closed-form derivation proposal. The audit lane sets
the effective status after independent review of the runner, the derivation
steps, and the length identification (slit-free harness ⇒ `L_total`, not
`L_2`).
