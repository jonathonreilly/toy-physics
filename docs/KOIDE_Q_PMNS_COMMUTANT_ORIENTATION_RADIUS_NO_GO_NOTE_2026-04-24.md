# Koide Q PMNS-Commutant Orientation/Radius No-Go Note

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_q_pmns_commutant_orientation_radius_no_go.py`
**Status:** executable no-go

RESIDUAL_SCALAR=`sigma_comm = r1^2 + r2^2 - 2*r0^2`

## Theorem Attempt

After the aligned PMNS transfer route failed to supply the odd cyclic slot, the
next strongest retained-interface variant was the projected commutant
eigenoperator route. That route is positive in the PMNS lane because it
produces `C3` even/odd orbit data: an even passive class and an odd
branch/orientation selector. The Koide question is whether that odd data can
be promoted to the missing charged-lepton response-radius law.

## Brainstormed Variants

1. **Odd orientation as `r2`:** identify the commutant odd mode with the Koide
   odd cyclic response.
2. **Even mode as scale:** identify the commutant even mode with `r0`.
3. **Identity-shift inversion:** test whether adding an even identity component
   preserves orientation while moving the radius.
4. **Transfer plus commutant composition:** combine PMNS transfer's even slot
   with commutant odd data.
5. **Selector/radius distinction:** test whether a branch bit or `Z3` class is
   categorically too small to determine a real radius equation.

## Executable Result

A canonical two-equal-corner projected commutant profile can be written

```text
v = (e + 2o, e - o, e - o).
```

Its `C3` Fourier decomposition gives

```text
v_even = e
v_odd  = o
```

on the chosen real branch. This is exactly the type of data the PMNS commutant
route supplies: an even offset and an odd orientation class.

In the best-case Koide mapping

```text
r0 = 3e
r1 = 0
r2 = 6o,
```

the response residual is

```text
sigma_comm = r1^2 + r2^2 - 2 r0^2
           = 36 o^2 - 18 e^2.
```

Positive odd orientation can be below, on, or above the Koide radius:

```text
e = 1, o = 1/10       -> sigma_comm = -441/25
e = 1, o = sqrt(2)/2  -> sigma_comm = 0
e = 1, o = 1          -> sigma_comm = 18
```

So the branch/orientation selector is weaker than a radius theorem.

## Identity-Shift Obstruction

The even identity shift

```text
e -> e + s
```

preserves the odd orientation `o`, but changes the residual by

```text
delta_sigma = -18*((e+s)^2 - e^2).
```

Therefore the projected commutant selector cannot by itself be a Koide radius
law while the retained even/identity offset remains free.

## Transfer Plus Commutant

Combining PMNS transfer's even channel with commutant odd data gives the
full-rank chart

```text
r0 = 3e
r1 = 6y
r2 = 6o.
```

But the full residual is still

```text
sigma_full = -18 e^2 + 36 y^2 + 36 o^2.
```

The missing equation is

```text
y^2 + o^2 = e^2/2.
```

That equation is not supplied by the PMNS transfer theorem or the projected
commutant selector.

## Hostile Review

- **Circularity:** the runner tests orientation data without setting the radius.
- **Target import:** no observational data or external witness enters the
  derivation.
- **Hidden selector:** using `y^2 + o^2 = e^2/2` would add the missing scalar
  law.
- **Axiom link:** the PMNS commutant route supplies selector/class data; it
  does not supply a charged-lepton source-radius theorem.
- **Scope:** this rejects only the promotion of PMNS commutant orientation data
  to Koide closure. It remains valid PMNS support.

## Verdict

Projected commutant orientation is not charged-lepton Koide closure.

```text
PMNS_COMMUTANT_ORIENTATION_FORCES_K_TL=FALSE
KOIDE_Q_PMNS_COMMUTANT_ORIENTATION_CLOSES_Q=FALSE
RESIDUAL_SCALAR=sigma_comm=r1^2+r2^2-2*r0^2
```

