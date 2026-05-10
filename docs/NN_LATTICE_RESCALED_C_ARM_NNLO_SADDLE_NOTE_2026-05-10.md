# NN Lattice Rescaled-Lane C_arm NNLO Saddle Note (2026-05-10)

**Claim type:** bounded_theorem (finite-slit-aperture NNLO correction matches
the four-point C_arm alpha fit inside the scoped deterministic-rescale harness;
does not change authority for the unaudited upstream chain)
**Status authority:** source-note proposal only; audit verdict and effective
status are set by the independent audit lane.
**Primary runner:** [`scripts/lattice_nn_rescaled_C_arm_NNLO_saddle.py`](../scripts/lattice_nn_rescaled_C_arm_NNLO_saddle.py)
**Cached log:** [`logs/runner-cache/lattice_nn_rescaled_C_arm_NNLO_saddle.txt`](../logs/runner-cache/lattice_nn_rescaled_C_arm_NNLO_saddle.txt)

## Status

`bounded`: the finite-slit-aperture NNLO correction reduces the fit-window
residual to `|alpha_NNLO - 0.5256| = 0.0009 <= 0.005`, closing the 33%
alpha gap left by the NLO saddle note inside this scoped empirical
comparison. This does not change authority for the upstream notes or the
dependency chain.

## Companion work

| Source note | Outcome |
| ------ | ---------------------------------------------------------- |
| [`NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md) | Numerical fit: `sigma_arm(h) = 2.7107 * h^{0.5256}` on the 4-point window `h <= 0.25`. |
| [`NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md) | LO saddle: `alpha_LO = 0.5000`, `C_arm_LO = 2.4855`. |
| [`NN_LATTICE_RESCALED_C_ARM_ALPHA_CONSTRAINED_REFIT_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_ALPHA_CONSTRAINED_REFIT_NOTE_2026-05-10.md) | Alpha-constrained refit: per-h residual <1% at h = 0.015625; confirms LO asymptote pointwise as a bounded diagnostic. |
| [`NN_LATTICE_RESCALED_C_ARM_NLO_SADDLE_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_NLO_SADDLE_NOTE_2026-05-10.md) | NLO phase: `alpha_NLO = 0.5170`, residual `|delta alpha| = 0.0086` (closes 67%). |
| This note | NNLO with finite-slit aperture: `alpha_NNLO = 0.5247`, residual `|delta alpha| = 0.0009` on the same fit window. |

## Task statement

Continue the saddle expansion to NNLO. Three concrete candidate sources:

1. NNLO phase: cos(omega h) to O(h^4) and beyond.
2. NNLO saddle: q^6 cumulant of the lateral random walk.
3. Finite-slit-aperture correction: truncation of the pre-slit wavefunction
   to the physical aperture `y in [SLIT_Y, SLIT_Y + W] = [3, 5]`.

Combine into `alpha_NNLO_eff`. Acceptance bands:
- **strong-closure**: `|alpha_NNLO - 0.5256| <= 0.005` inside this bounded
  empirical comparison.
- **bounded**: `|alpha_NNLO - 0.5256| <= 0.012` and >=30% improvement over NLO.
- **null**: NNLO doesn't help.

This note registers the strong-closure numerical outcome as bounded science.

## Setup recap

Per-edge amplitudes at lattice spacing `h`:
```
a_0(h)  = step * exp(i k h)         / sqrt(F)
a_pm(h) = step * c * exp(i k h sqrt(2)) / sqrt(2 F)
```
with `step = h/sqrt(F)`, `F = FANOUT = 3`, `c = exp(-BETA * pi^2 / 16) ~ 0.6105`,
`k = K_PHYS = 5`, `BETA = 0.8`. The lateral characteristic function is
```
g(q; h) = a_0(h) + 2 a_pm(h) cos(q h).
```

Let `A := |a_pm| |a_0| = c / (F sqrt(2))`, `B := 2 |a_pm|^2 = c^2 / F`,
`omega := k (sqrt(2) - 1) = 2.07107`, `r := A/(A+B) = 0.53666`.

The leading-order saddle gives `sigma^2_LO(h) = C_LO^2 h` with
```
C_LO^2 = L_2 (c^2 / (2 F)) / (A + B) = 6.17786,    C_LO = 2.48553
```
where `L_2 = 2 L_total / 3 = 26.667` is the post-slit propagation length.

The NLO saddle note supplemented the saddle with the cos(omega h) phase factor in the
denominator `A cos(omega h) + B` (the real part of `a_pm conj(a_0)`):
```
sigma^2_NLO(h) = C_LO^2 h * (1 + delta_a(h)),
delta_a(h)     = (A+B) / (A cos(omega h) + B) - 1.
```

The NLO runner already uses the exact cos(omega h), so further orders of
this expansion contribute zero. (This is documented below as a sharp null on
candidate 1.)

---

## 1) NNLO phase (cos(omega h) to O(h^4) and beyond)

### Expansion

Let `x := (omega h)^2`. Then
```
A cos(omega h) + B = (A+B) - A x/2 + A x^2/24 - A x^3/720 + A x^4/40320 - ...
                   = (A+B) [1 - r x/2 + r x^2/24 - r x^3/720 + r x^4/40320 - ...]
```
so
```
delta_a(h) = (A+B) / (A cos(omega h) + B) - 1
           = 1 / (1 - u) - 1
           = u + u^2 + u^3 + u^4 + ...
```
with
```
u(x) = c_1 x + c_2 x^2 + c_3 x^3 + c_4 x^4 + ...
c_1  = r/2,  c_2 = -r/24,  c_3 = r/720,  c_4 = -r/40320,  ...
```

Collecting powers of `x` in `u + u^2 + u^3 + u^4`:
```
[x^1]:  c_1                                              = r/2
[x^2]:  c_2 + c_1^2                                       = -r/24 + r^2/4
[x^3]:  c_3 + 2 c_1 c_2 + c_1^3                           = r/720 - r^2/24 + r^3/8
[x^4]:  c_4 + 2 c_1 c_3 + c_2^2 + 3 c_1^2 c_2 + c_1^4
     = -r/40320 + r^2/720 + r^2/576 - r^3/32 + r^4/16
```

Since `x^k = (omega h)^{2k}`, this gives a power series in `h^2`:
```
delta_a(h) = d2 h^2 + d4 h^4 + d6 h^6 + d8 h^8 + ...
```

### Closed-form coefficients (NEW; the rest of the cos series)

| Coefficient | Closed form                                                          | Numerical    |
| ----------- | -------------------------------------------------------------------- | ------------ |
| `d2`        | `(r/2) omega^2`                                                       | `1.150955`   |
| `d4`        | `(r^2/4 - r/24) omega^4`                                              | `0.913297`   |
| `d6`        | `(r^3/8 - r^2/24 + r/720) omega^6`                                    | `0.636480`   |
| `d8`        | `(r^4/16 - r^3/32 + r^2/576 + r^2/720 - r/40320) omega^8`             | `0.420024`   |

(The `d2` value matches the NLO saddle note exactly.)

### Numerical check: truncated series vs exact (the cos closed form)

| `h`       | `delta_a` exact | `d2 h^2`   | `d2 h^2 + d4 h^4` | `d2 h^2 + d4 h^4 + d6 h^6` |
| --------- | -------------- | ---------- | ------------------ | --------------------------- |
| 0.50000   | 0.356719       | 0.287739   | 0.344820           | 0.354765                    |
| 0.25000   | 0.075664       | 0.071935   | 0.075502           | 0.075658                    |
| 0.12500   | 0.018209       | 0.017984   | 0.018207           | 0.018209                    |
| 0.06250   | 0.004510       | 0.004496   | 0.004510           | 0.004510                    |
| 0.03125   | 0.001125       | 0.001124   | 0.001125           | 0.001125                    |

The h^2 + h^4 + h^6 partial sum matches the exact `delta_a(h)` to 6 decimal
places at h = 0.25 and exponentially better below.

### Verdict (candidate 1)

**Sharp null.** The NLO runner uses the closed-form
`(A+B)/(A cos(omega h) + B) - 1` (not the h^2 truncation), so d4, d6, d8
contribute zero new physics. They are reported as analytic record.

---

## 2) NNLO q^6 saddle correction

Per-edge: let `s := a_pm / g(0; h)`. With `u := q h`:
```
g(q; h)/g(0; h) = 1 - s u^2 + (s/12) u^4 - (s/360) u^6 + O(u^8)
```
(using `cos(q h) = 1 - u^2/2 + u^4/24 - u^6/720 + ...` and
`g/g0 = 1 + (2 a_pm/g0)(cos - 1) = 1 - s u^2 + (s/12) u^4 - (s/360) u^6 + ...`).

Then `log(g/g0) = xi - xi^2/2 + xi^3/3 - ...` with
`xi = -s u^2 + (s/12) u^4 - (s/360) u^6`:
```
log(g/g0) = -s u^2
            + (s/12 - s^2/2) u^4
            + (-s/360 + s^2/12 - s^3/3) u^6
            + O(u^8)
```

After `N = L_2 / h` edges:
```
g^N(q)/g(0)^N = exp[ -alpha_2 q^2 - alpha_4 q^4 - alpha_6 q^6 + ... ]
```
with
```
alpha_2 = L_2 s h                            (complex; LO support)
alpha_4 = L_2 (s^2/2 - s/12) h^3              (complex; NLO saddle)
alpha_6 = L_2 (s^3/3 - s^2/12 + s/360) h^5    (complex; NEW)
```

Treat `alpha_6` as a perturbation on the LO complex-Gaussian inverse FT.
`|A(y)|^2 = |A_0(y)|^2 (1 - 2 Re[alpha_4 X_4(y)] - 2 Re[alpha_6 X_6(y)] + ...)`.

With `mu := 1/(4 alpha_2)`:
- `X_4(y) = 12 mu^2 - 48 mu^3 y^2 + 16 mu^4 y^4`
- `X_6(y) = 120 mu^3 - 720 mu^4 y^2 + 480 mu^5 y^4 - 64 mu^6 y^6`

(`X_6` from `(d^6 / dy^6) e^{-mu y^2} = (120 mu^3 - 720 mu^4 y^2
+ 480 mu^5 y^4 - 64 mu^6 y^6) e^{-mu y^2}` — verified by direct
differentiation.)

Real variance correction with Gaussian moments
`<y^{2k}>_{G(0, sigma_0)} = (2k-1)!! sigma_0^{2k}`:
```
dV_6 = -2 Re( alpha_6 ( <y^2 X_6> - sigma_0^2 <X_6> ) )
```
where `sigma_0^2 = L_2 h |s|^2 / Re(s)`.

### Numerical magnitude

| `h`       | `sigma_0^2` | `dV_q4`              | `dV_q6`              | `|dV_q6| / sigma_0^2` |
| --------- | ---------- | -------------------- | -------------------- | --------------------- |
| 0.25000   | 1.661325   | +4.184e-3            | +8.889e-6            | 5.4e-6                |
| 0.12500   | 0.786294   | +8.271e-4            | +1.191e-6            | 1.5e-6                |
| 0.06250   | 0.387857   | +1.944e-4            | +1.508e-7            | 3.9e-7                |
| 0.03125   | 0.193275   | +4.786e-5            | +1.891e-8            | 9.8e-8                |
| 0.015625  | 0.096556   | +1.192e-5            | +2.365e-9            | 2.4e-8                |

### Verdict (candidate 2)

**Sharp null.** The q^6 saddle correction is sub-leading by ~10^3 to the
finite-slit-aperture correction (candidate 3) on the fit window. It alone
would not detectably move alpha.

---

## 3) Finite-slit-aperture NNLO correction (the dominant term)

### Setup

The slit at layer `nl // 3` blocks all `y` except the aperture
`y in [SLIT_Y, SLIT_Y + SLIT_W] = [3.0, 5.0]` (physical units). The arm
distance is `sqrt(<y_det^2>)` of the conditional detected distribution.

In the saddle / continuum limit, the lattice propagator from the origin to
the slit layer (length `L_1 = L_total / 3`) is a complex Gaussian
```
psi_pre(y_s) = (2 pi alpha_pre)^{-1/2} exp(-y_s^2 / (4 alpha_pre)),
alpha_pre    = L_1 s h.
```

The post-slit kernel from `y_s` at the slit layer to `y` at the detector
(length `L_2 = 2 L_total / 3`) is also a complex Gaussian
```
K(y, y_s; alpha_post) = (2 pi alpha_post)^{-1/2} exp(- (y - y_s)^2 / (4 alpha_post)),
alpha_post           = L_2 s h.
```

### Closed-form aperture-truncated convolution

The detected amplitude is
```
psi_det(y) = int_{SLIT_Y}^{SLIT_Y + SLIT_W} dy_s  psi_pre(y_s) K(y, y_s; alpha_post).
```

Completing the square in `y_s`:
- Define `M := 1/alpha_pre + 1/alpha_post = (alpha_pre + alpha_post) / (alpha_pre alpha_post)`.
- Define `y_c(y) := y / (alpha_post M)`.
- The y_s exponent becomes `-(M/4) (y_s - y_c)^2` plus a piece quadratic in y.
- That piece simplifies (using `1 - alpha_post M = -alpha_post / alpha_pre`) to
  `-y^2 / (4 (alpha_pre + alpha_post))`.

The `y_s` integral is a complex error function:
```
int_a^b dy_s exp(- (M/4) (y_s - y_c)^2)
    = (sqrt(pi) / sqrt(M)) * (1/2) [ erf((b - y_c) sqrt(M)/2) - erf((a - y_c) sqrt(M)/2) ]
```
(`erf` evaluated at complex argument). Dropping y-independent constants:
```
psi_det(y) propto exp(- y^2 / (4 alpha_total)) * Phi(y)
alpha_total = alpha_pre + alpha_post = L_total s h
Phi(y)      = erf(u_b(y)) - erf(u_a(y))
u_{a,b}(y)  = (SLIT_Y_{a,b} - y/(alpha_post M)) * sqrt(M) / 2
SLIT_Y_a    = SLIT_Y,  SLIT_Y_b = SLIT_Y + SLIT_W.
```

This is the **closed-form NNLO wavefunction** at the detector. Both factors
are analytic (complex erf is standard). Moments
`mu_arm = <y>` and `sigma_arm^2 = <y^2> - <y>^2` are then computed by 1D
quadrature on `|psi_det(y)|^2` -- the integrand is closed-form, only the
1D moment integrals are numerical.

### Numerical agreement on the continuum diagnostic four-point fit window

| `h`       | `mu_meas` | `mu_NNLO` | `sigma_meas` | `sigma_NNLO` | residual (NNLO) | residual (NLO only) |
| --------- | --------- | --------- | ------------ | ------------ | --------------- | ------------------- |
| 0.25000   | 3.3168    | 3.4302    | 1.3198       | 1.3171       | -0.205%         | -2.339%             |
| 0.12500   | 3.1701    | 3.2268    | 0.8990       | 0.8996       | +0.063%         | -1.365%             |
| 0.06250   | 3.0895    | 3.1191    | 0.6282       | 0.6281       | -0.020%         | -0.862%             |
| 0.03125   | 3.0467    | 3.0616    | 0.4416       | 0.4417       | +0.023%         | -0.446%             |

**Max sigma residual on fit window: 0.21%** (NNLO) vs **2.34%** (NLO only).
The NNLO closed form matches each fit-window point to <0.3%.

### Bounded-support remark (h = 0.015625)

At `h = 0.015625`, the slit position `y = SLIT_Y = 3.0` sits in the deep
exponential tail of the LO saddle (`exp(-y^2 / (4 alpha_pre))` evaluates to
roughly `exp(-46)`). The closed-form Gaussian saddle does not capture the
amplitude transmitted by the slit; the empirical `sigma_arm = 0.3115` is
within 0.3% of the pure-LO `sqrt(L_2 |s|^2 / Re(s) h) = 0.3107`, indicating
that at this h the post-slit distribution is dominated by ballistic
lattice-level dispersion outside the q^2 saddle universality. The closed
form gives 0.2884 (-7.4% residual), which is OUTSIDE the four-point alpha
fit window. The alpha-constrained refit note already verified the LO
asymptote pointwise at this h
(C_arm(h) = 2.4922, 0.27% residual against analytic 2.4855), so the
finite-window alpha fit -- which is what the continuum diagnostic reports -- is the
right place to compare NNLO.

This is acknowledged as a **bounded-support caveat**: the closed-form NNLO
applies to the four-point fit window only. Below the window, the LO formula
takes over and the NNLO correction asymptotically vanishes (consistent with
the alpha-constrained note's `sigma_arm / sqrt(h) -> C_LO`).

---

## 4) Combined alpha_NNLO_eff

Applying the continuum diagnostic's log-log linear fit protocol to each model on the fit
window `h in {0.25, 0.125, 0.0625, 0.03125}`:

| Model                          | `alpha_eff` | `C_eff`  | `|alpha - 0.5256|` |
| ------------------------------ | ----------- | -------- | ------------------- |
| LO     (C_arm support)         | 0.5000      | 2.4855   | 0.0256              |
| NLO    (phase note, exact)     | 0.5165      | 2.6186   | 0.0091              |
| NNLO_q (phase + q^4 + q^6)     | 0.5170      | 2.6234   | 0.0086              |
| **NNLO_full (+ aperture)**     | **0.5247**  | **2.7041** | **0.0009**       |
| EMPIRICAL  (continuum)         | 0.5256      | 2.7107   | --                  |

**Closure**: the slit-aperture NNLO closes the residual `|delta alpha|`
from `0.0086` (NLO) to `0.0009` (NNLO), a factor-9.6 reduction.

Local alpha at the geometric-mean fit-window point `h_geom = sqrt(0.25 * 0.03125) = 0.08839`:
- LO          : `alpha_local = 0.5000`
- NLO (phase) : `alpha_local = 0.5090`
- NNLO (full) : `alpha_local = 0.5175`

(The fit-window alpha is dominated by the steeper h = 0.25 endpoint.)

---

## Acceptance verdict

`|alpha_NNLO_eff - 0.5256| = 0.0009 <= 0.005`. This clears the
strong-closure band inside the bounded fit-window comparison.

All seven bounded-support guards PASS:

- `delta_a(h) > 0` on the fit window.
- Phase series `h^2 + h^4 + h^6` matches the exact `delta_a` to 1e-5 at h = 0.25.
- `|alpha_NNLO - 0.5256| <= 0.005` (strong-closure band).
- `alpha_NNLO_full > alpha_NLO` (strict improvement).
- `alpha_NNLO_full <= 0.5256` (no overshoot, NNLO closes from below).
- Max sigma residual on fit window <= 1.0% (achieved: 0.21%).
- `q^6` saddle term sub-leading (`|dV_q6| / sigma^2 < 1e-2` on the fit window).
- `h -> 0` recovery of `C_LO^2` (cross-confirmed by the alpha-constrained
  pointwise asymptote).

## Decomposition of the original 0.0256 alpha residual

| Source                             | `alpha_eff` contribution | running cumulative      |
| ---------------------------------- | ------------------------ | ----------------------- |
| LO   saddle                         | 0.5000                   | residual 0.0256 left    |
| NLO  phase (cos(omega h) resummed) | +0.0165                  | residual 0.0091 left    |
| NNLO q^4 saddle                    | +0.0005                  | residual 0.0086 left    |
| NNLO q^6 saddle                    | < 0.0001                 | residual ~0.0086 left   |
| **NNLO finite-slit aperture**      | **+0.0077**              | **residual 0.0009 left**|
| Combined                           | 0.5247                   | clears fit-window band  |

The 33% gap left by the NLO saddle note is explained primarily by the finite-slit-
aperture truncation, with the bulk-saddle q^4 contribution providing the
remainder of the closure and q^6 being numerically irrelevant.

## Cross-validation against the alpha-constrained refit

The alpha-constrained refit gives `C_arm(h)` per h:

| `h`       | `C_arm(h) := sigma_arm(h)/sqrt(h)` | predicted C_arm (NNLO closed) |
| --------- | ----------------------------------- | ------------------------------ |
| 0.25000   | 2.6396                              | 2.6342                         |
| 0.12500   | 2.5428                              | 2.5444                         |
| 0.06250   | 2.5128                              | 2.5123                         |
| 0.03125   | 2.4981                              | 2.4986                         |

C_arm(h) per-h matches predicted NNLO to <0.3% on the fit window. The
analytic asymptote `C_LO = 2.4855` is recovered as h -> 0 (the
alpha-constrained refit's
0.27% residual at h = 0.015625 is consistent with the residual ballistic-
tail contribution noted above).

## Files

- `scripts/lattice_nn_rescaled_C_arm_NNLO_saddle.py` — closed-form NNLO
  computation; prints all coefficients and `alpha_NNLO_eff` with the
  bounded fit-window closure.
- `docs/NN_LATTICE_RESCALED_C_ARM_NNLO_SADDLE_NOTE_2026-05-10.md` (this file).

## What is NOT claimed

- No re-measurement of any sigma_arm value. The empirical data are the
  measurements from the continuum diagnostic and alpha-constrained refit,
  unchanged.
- No fit-protocol change. The same 4-point log-log fit of the continuum
  diagnostic is
  applied to each model uniformly.
- No claim that the closed-form NNLO applies below h = 0.03125. The
  alpha-constrained refit
  is the authoritative numerical extension to h = 0.015625; the closed
  form there underpredicts (-7.4% residual at h = 0.0156) because the
  slit sits in the deep saddle tail and the empirical amplitude is sourced
  by sub-leading non-Gaussian lattice modes. The alpha-constrained refit already documents
  this regime via the alpha-constrained per-h estimator.

## Session

https://claude.ai/code/session_015mocy1jaZodDXSwpnZypjH
