# Quark E-Channel Endpoint Quotient Law

**Date:** 2026-04-19  
**Status:** theory-first bounded endpoint-law candidate for the remaining
`E`-channel readout primitive  
**Primary runner:** `scripts/frontier_quark_e_channel_endpoint_quotient_law.py`

## Safe statement

The current branch still does **not** derive the remaining quark `E`-channel
readout primitive exactly.

But the new endpoint-readout reduction already makes the right object precise:

```text
r_E = b_E / a_E = 6 * (gamma_E(center)/gamma_E(shell) - 1).
```

So the live problem is no longer “guess an up-amplitude law.” It is:

> what is the shell/center quotient `gamma_E(center)/gamma_E(shell)`?

This note gives the sharpest theory-first bounded candidate on the current
surface:

- the exact-support `T` channel already sits on the shell/center quotient
  `5/6`, giving `r_T = -1`;
- in a controlled low-rational endpoint class, the nearest `E`-channel
  shell/center quotient is `15/8`;
- that implies the bounded exact ratio law
  `r_E = 6 * (15/8 - 1) = 21/4`;
- and, together with the live shell-multiplicity candidate `a_T / a_E = -2`,
  it gives the anchored denominator candidate
  `D_E = r_E / 2 = 21/8`.

This is new bounded science, not an exact theorem.

## 1. Exact endpoint algebra

The endpoint-readout note already fixed the affine coefficients exactly from
the two support endpoints:

```text
gamma_E(delta_A1) = a_E + b_E delta_A1
gamma_T(delta_A1) = a_T + b_T delta_A1
delta_A1(center)  = 1/6
delta_A1(shell)   = 0.
```

That immediately yields the exact quotient identities

```text
r_E = b_E / a_E = 6 * (gamma_E(center)/gamma_E(shell) - 1)
r_T = b_T / a_T = 6 * (gamma_T(center)/gamma_T(shell) - 1).
```

So the open `E`-channel primitive is exactly equivalent to the shell/center
quotient `gamma_E(center)/gamma_E(shell)`.

## 2. T-channel template

On the same live endpoint data,

```text
gamma_T(center)/gamma_T(shell) = 0.833328...
```

which is already extremely close to the exact-support quotient

```text
5/6.
```

That quotient implies

```text
r_T = 6 * (5/6 - 1) = -1
```

exactly.

So the `T` channel already supplies the structural template:

- an endpoint quotient,
- one exact small fraction,
- one exact readout-ratio law.

## 3. E-channel bounded rationalization

The live `E`-channel shell/center quotient is

```text
gamma_E(center)/gamma_E(shell) = 1.876246130347...
```

The runner searches a **controlled** low-rational class:

- numerator `<= 96`
- denominator `<= 32`
- no wider expression grammar

and finds that the nearest candidate is

```text
15/8 = 1.875
```

with relative gap about `0.066%`.

That is already materially sharper than nearby small-rational competitors such
as `13/7`, `17/9`, or `47/25`.

So the clean bounded endpoint-law candidate is

```text
gamma_E(center)/gamma_E(shell) = 15/8.
```

## 4. Implied E-channel law

Using the exact endpoint identity,

```text
r_E = 6 * (15/8 - 1) = 21/4.
```

This law is within about `0.14%` of the live bounded `E`-channel ratio.

So the endpoint-quotient lane now reduces the remaining `E` primitive to one
small rational candidate:

```text
r_E = 21/4.
```

## 5. Anchored denominator candidate

If the live shell/intercept ratio is promoted to the clean shell-multiplicity
candidate

```text
a_T / a_E = -2
```

and the `T` channel is promoted to

```text
r_T = -1,
```

then the exact endpoint algebra gives

```text
|b_E / b_T| = r_E / 2.
```

So the `E`-quotient candidate implies the anchored denominator law

```text
D_E = 21/8 = 2.625.
```

That matters because:

- `21/8` is only about `0.13%` from the live bounded denominator
  `|b_E / b_T| = 2.621601...`;
- it is much closer to the live endpoint denominator than the older direct
  `sqrt(7)` proxy;
- and the corresponding anchored quark branch still stays below `1%` on the
  anchored CKM+`J` package.

So the rationalized `E`-channel law lands on the **same anchored branch** as
the live bounded endpoint solve.

## 6. What this unlocks

This note changes the remaining open problem.

The branch no longer needs to ask generically:

> what is the missing up-sector scalar law?

It can now ask more sharply:

1. can `gamma_E(center)/gamma_E(shell) = 15/8` be derived from the Route-2
   tensor support observable?
2. can `a_T / a_E = -2` be promoted from bounded shell multiplicity to theorem
   status?

If either of those lands, the `E`-channel law stops being a floating bounded
number.

## Honest endpoint

The current best theory-first bounded candidate is:

```text
gamma_E(center)/gamma_E(shell) = 15/8
=> r_E = 21/4
=> D_E = 21/8
```

This is useful new science because it rationalizes the remaining `E`-channel
primitive into one controlled endpoint law candidate. But it is still bounded,
not retained, because the current theorem stack does not yet derive `15/8`
from exact tensor machinery.

## Validation

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_e_channel_endpoint_quotient_law.py
```

Current expected result on this branch:

- `frontier_quark_e_channel_endpoint_quotient_law.py`: `PASS=16 FAIL=0`
