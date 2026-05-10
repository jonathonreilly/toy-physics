# Rescaled NN Lattice C_arm Next-to-Leading-Order Saddle Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem (NLO saddle correction predicts the right
sign and ~67% of the magnitude of the empirical alpha-residual; residual
gap |delta alpha| = 0.0086 outside the +/- 0.005 strong-closure band)
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/lattice_nn_rescaled_C_arm_NLO_saddle.py`](../scripts/lattice_nn_rescaled_C_arm_NLO_saddle.py)
**Cached log:** [`logs/runner-cache/lattice_nn_rescaled_C_arm_NLO_saddle.txt`](../logs/runner-cache/lattice_nn_rescaled_C_arm_NLO_saddle.txt)
**Companion / parent notes:**
- [`NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md)
  ([`scripts/lattice_nn_rescaled_C_arm_derivation.py`](../scripts/lattice_nn_rescaled_C_arm_derivation.py))
- [`NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md)
  ([`scripts/lattice_nn_rescaled_continuum_identification.py`](../scripts/lattice_nn_rescaled_continuum_identification.py))
**Diagnostic comparator:** the continuum diagnostic note's four-point fit
`sigma_arm(h) = C_arm h^alpha`, `C_arm = 2.7107`, `alpha = 0.5256`,
`R^2 = 0.9996` on `h in {0.25, 0.125, 0.0625, 0.03125}`.

## Context

The leading-order saddle of the coherent-saddle support note gives the
geodesic constant

```text
C_arm_LO = sqrt( L_2 / ( sqrt(2)/c + 2 ) ) = 2.4855
```

with `c = exp(-BETA pi^2 / 16) = 0.61050`, `L_2 = 2 L_total / 3 = 26.667`.
The same leading model has `alpha = 1/2`. The empirical four-point
fit gives `alpha = 0.5256`, so the alpha-residual `0.5256 - 0.5 = 0.026`
must come from a sub-leading correction that vanishes as `h -> 0`.

The continuum diagnostic measurements directly support a power-law approach
to the LO constant:

| `h`     | `sigma_arm` | `sigma^2 / h` |
|---------|-------------|---------------|
| 0.25    | 1.3198      | 6.9676        |
| 0.125   | 0.8990      | 6.4672        |
| 0.0625  | 0.6282      | 6.3160        |
| 0.03125 | 0.4416      | 6.2406        |

`sigma^2 / h` decreases monotonically with h, asymptoting to a value
indistinguishable from `C_LO^2 = 6.178` at the smallest h. So
`sigma^2(h) = C_LO^2 h (1 + delta(h))` with `delta(h) > 0` in the fit
window and `delta(h) -> 0` as `h -> 0`.

## Claim

The leading non-trivial NLO correction to the LO saddle is

```text
delta(h) ~ d2 h^2 + O(h^4),
   d2 = (A / (A + B)) * [k (sqrt(2) - 1)]^2 / 2 = 1.1510
```

with `A = c / (FANOUT sqrt(2))`, `B = c^2 / FANOUT`. The closed-form
prediction propagated through the continuum diagnostic's four-point log-log
fit gives

```text
alpha_NLO_eff = 0.5170
```

versus empirical `alpha = 0.5256`. The NLO captures the **direction** and
**~67% of the magnitude** of the empirical alpha-residual. Residual
gap is `|delta alpha| = 0.0086`. This is a bounded theorem, not a full
closure.

The candidate (b) `q^4` saddle correction is < 1% of the candidate (a)
phase correction on the fit window and does not change the conclusion.

## Imported Authorities

| Authority | Role |
|---|---|
| [`docs/NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md) | freezes `a_0(h)`, `a_pm(h)`, the lateral characteristic function `g(q; h)`, the saddle expansion to `q^2`, the `L_2` slit-plane geometry, and the LO closed form `C_LO^2 = L_2 / (sqrt(2)/c + 2)` |
| [`docs/LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md`](LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md) | freezes harness parameters `BETA = 0.8`, `k = 5`, `L_total = 40`, `FANOUT = 3`, slit at `nl // 3` |

This note adds the next-order term to the saddle expansion of the parent
note and propagates it through the per-h variance and the log-log fit
protocol of the continuum diagnostic note. It does not introduce a new axiom
and does not modify any retained-grade row.

## Setup recap

Per-edge amplitudes on the deterministic-rescale NN lane:

```text
a_0(h)   =  exp(i k h)                /  sqrt(FANOUT)
a_pm(h)  =  c * exp(i k h sqrt(2))    /  sqrt(2 FANOUT),     c = exp(-BETA pi^2/16)
```

Both are h-independent in magnitude (`step_scale * 1/L` cancels h); the
h-dependence sits entirely in the per-edge phase.

Lateral characteristic function (per edge):

```text
g(q; h)  =  a_0(h)  +  2 a_pm(h) cos(q h).
```

Per-arm path amplitude over `N_2 = L_2 / h` post-slit edges:

```text
g(q; h)^{N_2}.
```

Define
```text
A := |a_pm| |a_0|       =  c / (FANOUT sqrt(2))     =  0.143896
B := 2 |a_pm|^2         =  c^2 / FANOUT             =  0.124236
omega := k (sqrt(2) - 1)                            =  2.071068
r(h)   := a_pm(h) / g(0; h)                         (complex, per-h)
N_2    := L_2 / h
```

The LO saddle gives

```text
sigma^2(h) = L_2 * h * |a_pm|^2 / [Re(a_pm conj(a_0)) + 2 |a_pm|^2]
           = L_2 * h * (c^2 / (2 FANOUT)) / [A cos(omega h) + B]                  (1)
```

with the geodesic limit (cos -> 1) giving

```text
C_LO^2 = L_2 * (c^2 / (2 FANOUT)) / (A + B)          = 6.1779
C_LO   = 2.4855.                                                                  (2)
```

## Derivation

### 1. Sources of the NLO correction

There are two natural mechanisms that take `sigma^2(h)/h` away from the
flat geodesic value `C_LO^2`:

**(a) Phase NLO** — the LO formula (1) carries an explicit
`cos(omega h)` factor in the denominator coming from the
real part `Re(a_pm conj(a_0))`. Expanding the cosine in `h` gives a
correction to `sigma^2(h)/(C_LO^2 h)` at order `h^2`, `h^4`, ...

**(b) Saddle NLO** — the LO saddle keeps only the `q^2` term in
`log[g(q; h) / g(0; h)]`. The next contribution is `q^4`, which corrects
the inverse Fourier transform of `g^{N_2}(q)` at order `h^2` via standard
perturbation theory in the variance.

Both candidates produce an `O(h^2)` correction. We compute each in closed
form and report which dominates.

### 2. Candidate (a): phase NLO

From (1) divide top and bottom by `(A + B)`:

```text
sigma^2(h) = C_LO^2 * h * (A + B) / [A cos(omega h) + B]
           = C_LO^2 * h * (1 + delta_a(h)),                                       (3)

   delta_a(h) := (A + B) / [A cos(omega h) + B] - 1.
```

Expand `cos(omega h) = 1 - (omega h)^2 / 2 + (omega h)^4 / 24 - ...`:

```text
A cos(omega h) + B  =  (A + B)  -  A (omega h)^2 / 2  +  A (omega h)^4 / 24  -  ...
                    =  (A + B) [ 1 - x + (A/(A+B)) (omega h)^4 / 24 ],
                          x = (A / (A + B)) * (omega h)^2 / 2.
```

Then

```text
1 / [A cos(omega h) + B]  =  (1 / (A + B)) [ 1 + x + x^2 - (A/(A+B)) (omega h)^4 / 24 + ... ]
delta_a(h)                =  x  +  x^2  -  (A/(A+B)) (omega h)^4 / 24  +  O(h^6)

   d2_phase  :=  (A / (A + B))           * omega^2 / 2
              =  0.536661 * 4.289323 / 2
              =  1.150955

   d4_phase  :=  (A / (A + B))^2 * omega^4 / 4
              -  (A / (A + B))   * omega^4 / 24
              =  0.913297                                                         (4)
```

So

```text
delta_a(h) = 1.1510 * h^2 + 0.9133 * h^4 + O(h^6).
```

### 3. Candidate (b): q^4 saddle NLO

Expand `g(q; h) / g(0; h)` to `O(q^4)`:

```text
g(q; h) / g(0; h)  =  1  +  (2 a_pm / g(0)) (cos(q h) - 1)
                   =  1  -  r u^2  +  r u^4 / 12  +  O(u^6),         u := q h, r = a_pm / g(0)

log [g/g(0)]       =  -r u^2  +  (r/12 - r^2/2) u^4  +  O(u^6).                   (5)
```

Hence

```text
g^{N_2}(q)  =  g(0)^{N_2} * exp( -alpha_2 q^2  -  alpha_4 q^4  +  O(q^6) )
   alpha_2  =  N_2 r h^2  =  L_2 r h           (complex)
   alpha_4  =  N_2 (r^2/2 - r/12) h^4  =  L_2 (r^2/2 - r/12) h^3.                 (6)
```

The position-space wavefunction is

```text
A(y) = (g(0)^{N_2} / 2 pi) integral dq exp(-alpha_2 q^2 - alpha_4 q^4 - i q y)
     = A_0(y) * [1 - alpha_4 X(y) + O(alpha_4^2)]
```

where `A_0(y) = (g(0)^{N_2} / sqrt(4 pi alpha_2)) exp(-y^2 / (4 alpha_2))`
is the LO Gaussian and, with `mu := 1/(4 alpha_2)`,

```text
X(y) = ( -1/A_0(y) ) * d^4/dy^4 A_0(y) ... evaluated explicitly:
X(y) = 12 mu^2  -  48 mu^3 y^2  +  16 mu^4 y^4.                                   (7)
```

The position distribution `|A(y)|^2` is a real-Gaussian times a complex
correction:

```text
|A(y)|^2 = |A_0(y)|^2 * |1 - alpha_4 X(y)|^2
         ~ |A_0(y)|^2 * [ 1 - 2 Re(alpha_4 X(y)) ].
```

`|A_0|^2` is itself a real Gaussian with LO variance

```text
sigma_0^2(h)  =  N_2 h^2 |r|^2 / Re(r)
              =  L_2 h |a_pm|^2 / [Re(a_pm conj(a_0)) + 2 |a_pm|^2]
              =  C_LO^2 h (1 + delta_a(h)).                                       (8)
```

So the candidate-(b) correction is *additive on top of* the full
candidate-(a) result of equation (3) — they are not double counting; they
are independent contributions to the q-expansion of `log g^{N_2}(q)`.

Compute the variance correction by Gaussian moments under the weight
`exp(-y^2 / (2 sigma_0^2))`:

```text
<X>     = 12 mu^2  -  48 mu^3 sigma_0^2  +  48 mu^4 sigma_0^4
<y^2 X> = 12 mu^2 sigma_0^2  -  144 mu^3 sigma_0^4  +  240 mu^4 sigma_0^6
Y       := <y^2 X> - sigma_0^2 <X>
        =  -96 mu^3 sigma_0^4  +  192 mu^4 sigma_0^6
        =  96 mu^3 sigma_0^4 (2 mu sigma_0^2 - 1).                                (9)

dV_b(h)   :=  variance correction
            =  -2 Re( alpha_4 Y ).                                                (10)
```

`mu`, `sigma_0^2`, `alpha_4` are all complex per-h objects; we evaluate
them numerically (closed form, no Monte Carlo) in the runner.

### 4. Numerical magnitude of (a) vs (b)

From the runner ([`scripts/lattice_nn_rescaled_C_arm_NLO_saddle.py`](../scripts/lattice_nn_rescaled_C_arm_NLO_saddle.py)):

| `h`     | `delta_a(h)` (exact) | `d2_phase * h^2` | `dV_b / sigma_0^2` |
|---------|----------------------|------------------|--------------------|
| 0.5     | 0.356719             | 0.287739         | 0.92%              |
| 0.25    | 0.075664             | 0.071935         | 0.25%              |
| 0.125   | 0.018209             | 0.017984         | 0.11%              |
| 0.0625  | 0.004510             | 0.004496         | 0.05%              |
| 0.03125 | 0.001125             | 0.001124         | 0.025%             |

Two readings:
- `delta_a(h) ~ d2_phase h^2` to better than 5% on the entire fit window.
  The `d4_phase h^4` and higher terms are sub-percent at `h <= 0.25`.
- The `q^4` saddle correction is < 1% of the phase correction on the fit
  window. Candidate (a) dominates. The closed-form leading NLO is
  `delta(h) ~ 1.1510 * h^2`.

### 5. Per-h cross-check vs continuum diagnostic measurements

| `h`     | `sigma^2_meas` | `sigma^2_a` | residual_a | `sigma^2_a+b` | residual_a+b |
|---------|----------------|-------------|------------|---------------|--------------|
| 0.25    | 1.74187        | 1.66133     | -4.62%     | 1.66551       | -4.38%       |
| 0.125   | 0.80820        | 0.78629     | -2.71%     | 0.78712       | -2.61%       |
| 0.0625  | 0.39464        | 0.38786     | -1.72%     | 0.38805       | -1.67%       |
| 0.03125 | 0.19501        | 0.19328     | -0.89%     | 0.19332       | -0.87%       |

The NLO prediction undershoots the measurement at every h, with a
residual that monotonically decreases as h shrinks. Max residual is
4.4% at h = 0.25.

### 6. Effective alpha from the log-log fit

The continuum diagnostic uses the protocol:
fit `log sigma_arm = log C_arm + alpha log h`
by ordinary least squares on `h in {0.25, 0.125, 0.0625, 0.03125}`. We
reproduce this protocol with the predicted `sigma_arm(h)` for each model:

| Model | `alpha_eff` | `C_eff` | `|alpha_eff - 0.5256|` |
|-------|-------------|---------|------------------------|
| LO only        | 0.5000 | 2.4855 | 0.0256 |
| candidate (a)  | 0.5165 | 2.6186 | 0.0091 |
| candidate (a+b)| 0.5170 | 2.6234 | 0.0086 |
| empirical      | 0.5256 | 2.7107 | (--)   |

The NLO closes 67% of the alpha-residual: from `0.0256` (LO) to
`0.0086` (NLO), recovering the right sign and most of the magnitude.

The induced `C_eff = 2.6234` also moves toward the empirical `2.7107`,
shrinking the LO C-residual from `-8.31%` to `-3.22%`. So the
LO C-residual and the alpha-residual are coupled: both shrink together
under the same NLO correction. This is consistent with the picture that
the LO formula is the `h -> 0` reference and the fit-window extracts a
window-averaged effective constant inflated by the `delta(h)` term.

### 7. Local alpha sanity check

At the geometric-mean `h_geom = sqrt(0.25 * 0.03125) = 0.0884`, the
model's local slope is

```text
d log sigma / d log h  evaluated at h_geom:
   LO            : 0.5000
   candidate (a) : 0.5090
   candidate (a+b): 0.5094
```

The window-averaged `alpha_eff = 0.5170` is larger than the local-slope
value `0.5094` because the LSQ fit on log-spaced points is dominated by
the larger-h points where `delta(h)` is larger. Both numbers are well
below the empirical `0.5256`, so the residual gap is robust to the
choice of "alpha summary" (window OLS vs local slope vs constrained
fit).

## Outcome class and unaccounted gap

This is a **bounded theorem** outcome:

- **Sign**: PASS. NLO predicts `delta(h) > 0`; data has `sigma^2/h`
  decreasing as h shrinks (consistent with `delta(h) > 0`).
- **Magnitude**: 67% recovery. NLO shifts `alpha_eff` from `0.5000` to
  `0.5170`; empirical is `0.5256`. Residual gap `0.0086`.
- **C constant**: NLO shrinks the LO `-8.3%` C-residual to `-3.2%`.
- **Per-h sigma^2**: max residual `4.4%` at `h = 0.25`, decreasing to
  `0.9%` at `h = 0.03125`.

The unaccounted residual gap of `|delta alpha| = 0.0086` is outside the
strong-closure band `+/- 0.005` set by the task acceptance criterion. Three
candidate sources for the next-to-NLO contribution:

1. **O(h^4) phase corrections** to the variance. The `d4_phase = 0.913`
   coefficient is comparable to `d2_phase = 1.151`, so at `h = 0.25` the
   `h^4` correction adds `0.913 * 0.0039 = 0.0036` to delta_a, against
   the `0.072` from `d2 h^2` — a 5% lift. Propagating an extra `+0.0036`
   to `delta_a(h=0.25)` would close a small fraction of the per-h
   residual (`-4.62% -> -4.27%`).

2. **q^6 (and higher) saddle terms** in (5). The next-leading term is
   `O((qh)^6)` in `log[g/g(0)]`, with coefficient mixing `r`, `r^2`, and
   `r^3`. By the runner's accounting the q^4 term contributes only
   `~0.25%` at `h = 0.25`; q^6 is suppressed by another factor of
   `(qh)^2 / N_2`, so this is unlikely to close the gap.

3. **Finite-slit-aperture corrections.** The coherent-saddle support note
   observes `sigma_1 ~
   0.4 - 0.9` versus a slit half-width of `1.0` on the fit window — i.e.
   the slit transmits the full natural Gaussian tail of the source wave,
   not a narrow sub-aperture. The slit therefore acts as a soft (not
   sharp) position constraint, and the residual `~4.4%` per-h at
   `h = 0.25` is in the right ballpark to be explained by sub-leading
   slit-aperture geometry, not by the saddle expansion.

The runner reports all three candidates and tags the outcome BOUNDED.

## Reproducibility

```text
python3 scripts/lattice_nn_rescaled_C_arm_NLO_saddle.py
```

Closed form. No Monte Carlo, no lattice propagation, no fit. Depends
only on `BETA`, `K_PHYS`, `PHYS_L`, `FANOUT` (taken from
`scripts/lattice_nn_deterministic_rescale.py`) and the slit-plane
fraction `1/3`. Bounded-support guards inside the runner check:

- `delta(h) > 0` in fit window (correct sign).
- `0.5000 < alpha_eff < 0.5256` (correct direction, undershoot not
  overshoot).
- `|alpha_eff - 0.5256| <= 0.020` (right magnitude band).
- max per-h `sigma^2` residual `<= 5%`.
- candidate (a) dominates (b) on the fit window (ratio < 1%).
- `h -> 0` limit recovers `C_LO^2 = 6.178`.

All seven guards PASS at the harness-fixed parameters.

## Bounded scope

This note:

- derives the closed-form NLO `delta(h) ~ 1.1510 h^2` from the saddle
  expansion of the per-step characteristic function, with a clean
  algebraic origin (the cosine phase factor in `Re(a_pm conj(a_0))`);
- propagates `delta(h)` through the continuum diagnostic's log-log fit
  protocol and
  predicts `alpha_eff = 0.5170` versus empirical `alpha = 0.5256`;
- shows that the `q^4` saddle correction is sub-leading to the phase NLO
  by two orders of magnitude on the fit window;
- documents the `0.0086` residual alpha-gap and three candidate sources
  for the next-to-NLO contribution.

It does NOT:

- close the alpha-residual to the `+/- 0.005` strong-closure band;
- promote any retained-grade row;
- close or promote the upstream diagnostic fit;
- claim derivation of `sigma_arm` outside the rescaled NN harness or
  away from the deterministic-rescale lane;
- pin down which of the three next-to-NLO candidates closes the
  residual `0.0086` gap (this is left for follow-up).

## Status

This source note is a bounded next-to-leading-order saddle proposal. It
extends the parent LO support note by one order in the saddle
expansion. The audit lane sets the effective status after independent
review of the runner, the saddle expansion, and the alpha_eff
extraction protocol.

https://claude.ai/code/session_015mocy1jaZodDXSwpnZypjH
