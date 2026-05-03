# Discrete Evanescent-Barrier Amplitude Suppression on `Cl(3)/Z^3`

**Date:** 2026-04-17 (review-blocker revision 2026-04-17)
**Status:** proposed_retained lattice transfer-matrix bound + proposed_retained geometric
tortoise-length identity; the Planck-unit astrophysical exponent
`exp[-(R_S/l_P) ln(R_S/l_P)]` is explicitly CONDITIONAL on a per-site
rate lower bound that is NOT on the retained surface
**Script:** `scripts/frontier_evanescent_barrier_amplitude_suppression.py`
**Log:** [logs/retained/evanescent_barrier_amplitude_suppression_2026-04-17.log](../logs/retained/evanescent_barrier_amplitude_suppression_2026-04-17.log)

## Role

This note is the standalone authority for two retained framework-internal
statements:

1. a rigorous transfer-matrix amplitude bound for the discrete
   Schroedinger operator on `Cl(3)/Z^3`, and
2. an exact Schwarzschild-interior tortoise-length geometric identity.

The Planck-unit astrophysical exponent `exp[-(R_S/l_P) ln(R_S/l_P)]`
carried in the bounded GW-echo null companion is NOT a retained
consequence of (1) + (2) alone: converting the retained bound into the
Planck-unit astrophysical exponent requires a lower bound on the
per-lattice-site evanescent rate that the current framework surface
does not supply.  This revision explicitly demotes that step to a
named open conditional.

## Retained theorem A: discrete lattice transfer-matrix bound

**Theorem (discrete evanescent-barrier amplitude bound).**
Let `H = -t * Delta + V` be the discrete Schroedinger operator on `Z`
with the symmetric nearest-neighbor Laplacian

```
(Delta psi)_i  =  psi_{i+1}  -  2 psi_i  +  psi_{i-1},
```

hopping `t > 0`, and real potential `V`.  The eigenvalue equation
`(H - E) psi = 0` is equivalent to the second-order recurrence

```
psi_{i+1}  =  u_i * psi_i  -  psi_{i-1},      u_i  =  2 + (V_i - E)/t,
```

whose transfer matrix has characteristic polynomial
`lambda^2 - u_i * lambda + 1 = 0`.  In a classically-forbidden interval
`[R_1, R_2]` with `V_i - E > 0` (equivalently `u_i > 2`), the two
transfer eigenvalues are real, reciprocal, and positive:

```
lambda_+(i)  =  ( u_i + sqrt(u_i^2 - 4) ) / 2  >  1,
lambda_-(i)  =  1 / lambda_+(i)  <  1.
```

The lattice Green function across the forbidden region then satisfies
the rigorous amplitude bound

```
|G(R_1, R_2; E)|  <=  C * prod_{i in [R_1, R_2]} (1 / lambda_+(i))
                  =   C * exp[ - sum_{i in [R_1, R_2]} ln lambda_+(i) ],
```

with algebraic prefactor `C = O(t^{-1} * poly(R_2 - R_1))`.  This is the
standard discrete-Schroedinger evanescent bound.

### Asymptotic regimes

- **Shallow WKB** (`(V - E)/t -> 0`): `lambda_+ = 1 + sqrt((V-E)/t) +
  O((V-E)/t)`, so `ln lambda_+ ~ sqrt((V-E)/t)`.  This is the discrete
  analogue of the continuum WKB phase-integral `int sqrt(kappa^2) dr`.
- **Deep WKB** (`(V - E)/t -> infinity`): `lambda_+ = (V-E)/t +
  O((V-E)/t)^{-1}`, so `ln lambda_+ ~ ln((V-E)/t)`.

### Framework-retained ingredients

1. lattice spacing carried on the current Planck-scale package pin,
   `a^(-1) = M_Pl`, on the accepted physical-lattice reading
2. `Cl(3)/Z^3` nearest-neighbor Laplacian [retained; free-field sector
   of the retained Wilson-plus-staggered action surface]
3. lattice hard floor `R_min >= l_Planck` [retained corollary of a
   positive lattice spacing]

### Scope discipline

The retained theorem A above does NOT claim:

1. any lower bound on `ln lambda_+(i)` at individual sites
2. any universal astrophysical amplitude bound independent of the
   potential profile
3. any quantitative GW-echo null-result prediction
4. full nonlinear GR inside `R_S`
5. a no-horizon theorem beyond the retained restricted strong-field
   closure

## Retained theorem B: Schwarzschild interior tortoise-length identity

**Theorem (interior tortoise-length formula).**
Let `f(r) = 1 - R_S/r` be the Schwarzschild lapse, and take the
inverse-lapse interior integral

```
L*(R_min, R_S; eps)  :=  integral_{R_min}^{R_S - eps}  dr / |f(r)|.
```

For `r < R_S`, `|f(r)| = R_S/r - 1 = (R_S - r)/r`, so the integrand is
`r / (R_S - r)`.  A direct antiderivative via `u = R_S - r` gives

```
integral  r / (R_S - r)  dr  =  (R_S - r)  -  R_S * ln(R_S - r)  +  C,
```

and evaluation on `[R_min, R_S - eps]` yields the exact closed form

```
L*(R_min, R_S; eps)  =  R_S * ln((R_S - R_min) / eps)
                        +  eps  +  R_min  -  R_S.
```

With the natural lattice cutoff `eps = R_min` and for `R_min << R_S`,

```
L*(R_min, R_S; R_min)  ~  R_S * ln(R_S / R_min)  -  R_S  +  O(R_min).
```

This is an exact analytic identity about the Schwarzschild exterior
lapse.  Its framework content is: on the retained restricted
strong-field closure surface
([RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](./RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md)),
`f(r) = 1 - R_S/r` is the exterior bridge function, and
`R_min >= l_Planck` is the retained lattice hard floor on the current
Planck-scale package pin.

### Scope discipline

Theorem B is a geometric identity.  It does NOT by itself produce an
amplitude bound.  It names the length scale that would enter such a
bound if the per-site rate in tortoise coordinates were known.

## Open conditional: the Planck-unit astrophysical exponent

Combining theorems A and B to reach the Planck-unit astrophysical
exponent

```
|G|  <=  exp[ - (R_S/l_Planck) * ln(R_S/R_min) + O(R_S/l_Planck) ]
```

requires one additional ingredient that is NOT a retained consequence
of the current framework surface:

> **(C-rate)**  An order-one lower bound on the per-unit-tortoise-length
> evanescent rate `ln lambda_+(r*) / (dr*/a)` integrated over the
> Schwarzschild interior tortoise coordinate.

Equivalently, the direct-in-`r` sum `sum_i ln lambda_+(i)` appearing in
theorem A does NOT scale as `R_S ln(R_S/R_min)` when `V(r)/t = R_S/r` on
`[R_min, R_S]`; probe 3 of the runner shows it scales as `R_S` with a
subleading logarithmic correction, giving a ratio
`Phi_exact / (R_S ln(R_S/R_min))` that decreases with `R_S/R_min` rather
than approaching a positive constant.  Reaching the Planck-unit exponent
therefore depends on identifying the physically correct effective
potential in tortoise coordinates together with a rigorous lower bound
on its per-site rate — neither of which is on the retained surface.

Two honest consequences:

1. The retained-surface product of theorem A applied to the direct-in-`r`
   Schwarzschild profile on `[R_min, R_S]` gives suppression of order
   `exp(-c * R_S / a)` for some profile-dependent `c > 0` established
   numerically on moderate lattices, not `exp(-(R_S/a) ln(R_S/a))`.
2. The `exp[-(R_S/l_P) ln(R_S/l_P)]` formula that the bounded GW-echo
   null companion carries
   ([GW_ECHO_NULL_RESULT_NOTE.md](./GW_ECHO_NULL_RESULT_NOTE.md))
   remains a BOUNDED statement that depends on (C-rate) above.  This
   note does NOT promote that formula to the retained surface.

Promoting (C-rate) is an explicit follow-up theorem target.  Until it
lands, retained theorems A and B are the full retained surface of this
note.

## Validation

`scripts/frontier_evanescent_barrier_amplitude_suppression.py` runs six
probes, each using the `u_i = 2 + (V_i - E)/t`, `lambda_+ = (u_i +
sqrt(u_i^2 - 4))/2` evanescent eigenvalue explicitly consistent with
retained theorem A:

1. **Rectangular barrier (retained theorem A).**
   Discrete Schroedinger on a flat barrier; linear fit of `ln |G|`
   against barrier width `L` recovers the theoretical slope
   `-ln lambda_+` to within `1e-2`.

2. **Continuum WKB limit (retained theorem A asymptotics).**
   Shallow-barrier limit `(V-E)/t -> 0` recovers
   `ln lambda_+ -> sqrt((V-E)/t)` and deep-barrier limit
   `(V-E)/t >> 1` recovers `ln lambda_+ -> ln((V-E)/t)`.

3. **Schwarzschild interior tortoise length (retained theorem B).**
   Closed-form identity `L* = R_S ln((R_S - R_min)/eps) + eps + R_min
   - R_S` is verified against the leading-order formula
   `R_S ln(R_S/R_min) - R_S` to `1e-3` at `R_S/R_min >= 300`.

4. **Lattice sanity on the direct-in-`r` Schwarzschild profile
   (open conditional diagnostic).**
   For `V(r)/t = R_S/r` on `[R_min, R_S]` the retained-theorem-A sum
   `Phi_exact = sum_i ln lambda_+(i)` is an asserted upper bound on
   the quantity `(R_S/a) ln(R_S/a)` would formally suggest under the
   unproved O(1) per-site rate conditional (C-rate).  Probe 4 now
   asserts this inequality as a real `check(...)` call, not a
   print-only status column.  The probe documents rather than
   promotes the conditional.

5. **Robustness across barrier profiles (retained theorem A).**
   The transfer-matrix bound holds on rectangular, triangular, `1/r`,
   `1/r^2`, and logistic potential profiles.

6. **Spacing-scaling diagnostic for the bounded companion.**
   The GW150914 benchmark reproduces `log10 |T| ~ -2.3e41` under the
   (C-rate)-conditional Planck-unit exponent carried by
   `frontier_echo_null_result.py`, and doubling the hypothetical
   spacing halves the exponent magnitude.  This is a diagnostic for
   the bounded companion, not evidence for the conditional itself.

Run summary on commit land: `PASS = 11`, `FAIL = 0`.

## Relation to the bounded echo companion

The bounded companion
[GW_ECHO_NULL_RESULT_NOTE.md](./GW_ECHO_NULL_RESULT_NOTE.md) carries
the Planck-unit formula `|T| ~ exp[-(R_S/l_P) ln(R_S/R_min)]` and the
associated `log10 |T| ~ -10^41` numerical echo-amplitude statement for
LIGO-class targets.  That formula remains BOUNDED.  The retained
surface of this note — theorems A + B — does not promote the formula to
retained status, because the step from theorem A applied to
Schwarzschild-like potentials on `[R_min, R_S]` to the Planck-unit
exponent requires (C-rate) above.

What the retained surface of this note does provide:

- a rigorous amplitude bound for the discrete Schroedinger operator
  (theorem A), with the correct transfer-matrix eigenvalue formula
  consistent with the runner
- the exact tortoise-length identity (theorem B) that names the length
  scale `L* ~ R_S ln(R_S/R_min) - R_S` that would appear in any bound
  derived via the tortoise route

## Relation to the restricted strong-field closure

[RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](./RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md)
carves out a restricted exterior-shell closure and explicitly lists
"no-horizon / no-echo as theorem-level downstream consequences" among
the things not yet promotable.  The present note does not promote the
no-echo consequence.  It promotes the narrower retained surface above
(theorems A + B) which can be used as a public structural
backbone for the bounded companion without changing the restricted
strong-field boundary.

## Safe package claim

> On `Cl(3)/Z^3`:
>
> (A) For the discrete Schroedinger operator `H = -t Delta + V`, the
> Green function across any classically-forbidden interval is bounded
> by `|G| <= C exp[-sum_i ln lambda_+(i)]` with
> `lambda_+(i) = (u_i + sqrt(u_i^2 - 4))/2`,
> `u_i = 2 + (V_i - E)/t`.
>
> (B) For the Schwarzschild exterior lapse `f(r) = 1 - R_S/r`, the
> interior inverse-lapse integral admits the exact closed form
> `L*(R_min, R_S; eps) = R_S ln((R_S - R_min)/eps) + eps + R_min - R_S`
> with leading behavior `R_S ln(R_S/R_min) - R_S` for `R_min << R_S`.
>
> The Planck-unit astrophysical exponent
> `exp[-(R_S/l_P) ln(R_S/R_min)]` carried by the bounded GW-echo null
> companion requires an additional order-one per-unit-tortoise-length
> rate lower bound (C-rate) that is NOT on the retained surface of this
> note.  The companion remains bounded; theorems A and B do NOT by
> themselves imply the Planck-unit astrophysical exponent.

## Supporting notes

- [RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](./RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md)
  — retained exterior restricted strong-field closure
- [OH_STATIC_CONSTRAINT_LIFT_NOTE.md](./OH_STATIC_CONSTRAINT_LIFT_NOTE.md)
  — exact local shell-to-`3+1` constraint lift on the static conformal
  bridge surface
- [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](./OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
  — exact microscopic Schur boundary action for the shell law
- [STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md](./STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md)
  — `O_h` source family on which the restricted closure is exact
- `GW_ECHO_NULL_RESULT_NOTE.md` (sibling artifact; cross-reference only —
  not a one-hop dep of this note) — bounded downstream companion that
  consumes this theorem

## Primary reruns

```
python3 scripts/frontier_evanescent_barrier_amplitude_suppression.py
```

Expected output: `PASS = 11`, `FAIL = 0`.
