# Quark Up-Amplitude Tensor-Endpoint Bridge

**Date:** 2026-04-19
**Status:** bounded tensor-endpoint bridge from support-tensor data to the
reduced up-sector quark affine family
**Primary runner:** `scripts/frontier_quark_up_amplitude_tensor_endpoint_bridge.py`

## Safe statement

The current branch still does **not** derive a unique reduced up-sector
amplitude law `a_u`.

But the remaining quark affine family is now less arbitrary than the earlier
candidate scans made it look.

The support-tensor notes already carry two endpoint invariants that seed the
two strongest support-native quark affine laws:

- the **exact support endpoint gap**
  `Delta_endpoint = delta_A1(e0) - delta_A1(s/sqrt(6)) = 1/6`
- the **bounded tensor slope ratio**
  `k_tensor = |b_E / b_T|` from the endpoint-fixed readout
  `gamma_E = a_E + b_E delta_A1`,
  `gamma_T = a_T + b_T delta_A1`

So the current tensor/support surface already organizes the split affine
quark winners into an endpoint-derived pair. That is still a bounded
statement, not a retained theorem, because the tensor readout coefficients are
themselves only bounded and the two endpoint laws still split between the
best refit and best anchored packages.

## Tensor endpoint data used here

This bridge stays on the same exact-support anchor as the recent quark notes:

- `delta_A1(q_dem) = 1/42`
- `sin(delta_std) = sqrt(5/6)`
- `6/7 = 1 - 6 delta_A1`

The new ingredient is the endpoint-fixed support-tensor readout already
present in:

- [TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md](./TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md)
- [S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md](./S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md)

On the current branch that readout gives

```text
gamma_E(delta_A1) = -2.010572657265e-04 + (-1.057053906426e-03) delta_A1
gamma_T(delta_A1) = +4.031967723697e-04 + (-4.032091965809e-04) delta_A1
```

with the derived endpoint ratios

```text
Delta_endpoint = 1/6
k_tensor       = |b_E / b_T| = 2.621602...
k_shell        = |a_T / a_E| = 2.005383...
```

The important point is not the exact numerical values by themselves. It is
that they are **endpoint data already present on the support-tensor surface**,
so they can now seed a genuinely tensor-connected quark law family.

## Endpoint-derived bridge family

The bridge runner tests a small family of reduced up-amplitude laws built only
from:

- the exact support fraction `6/7`
- the exact endpoint gap `Delta_endpoint`
- the bounded tensor ratios `k_tensor`, `k_shell`, and `|b_T / a_T|`

The two strongest laws are:

### Exact endpoint-gap law

```text
a_u = sin(delta_std) * (6/7 - delta_A1 * Delta_endpoint)
    = sin(delta_std) * (6/7 - delta_A1 / 6)
    = 0.778838292749
```

This reproduces the strongest current affine refit branch:

- two-ratio refit objective: `0.052796`
- full-package refit max deviation: `0.862%`
- anchored CKM+`J` aggregate deviation: `0.892%`

So the earlier best affine refit law is no longer just a naked scan winner.
Its `1/6` correction is exactly the support-endpoint gap already derived on
the tensor side.

### Bounded tensor-ratio law

```text
a_u = sin(delta_std) * (6/7 - delta_A1 / k_tensor)
    = sin(delta_std) * (6/7 - delta_A1 / |b_E / b_T|)
    = 0.774170054824
```

This is the strongest anchored law in the endpoint-derived family:

- anchored CKM+`J` aggregate deviation: `0.723%`
- anchored max component deviation: `0.667%`
- full-package refit max deviation: `1.052%`

Numerically this law sits within `0.1%` of the earlier `delta_A1 / sqrt(7)`
proxy branch. So the previously empirical-looking `sqrt(7)` denominator now
has a concrete bounded tensor-endpoint precursor: the current slope ratio
`|b_E / b_T|`.

## What this changes

This note sharpens the quark endpoint again.

Before this bridge, the honest statement was:

- the current affine `delta_A1` family was privileged,
- but the best refit and anchored laws still looked like separate scan
  outcomes.

After this bridge, the sharper statement is:

- the strongest **refit** law is seeded by the exact tensor support endpoint
  gap `1/6`
- the strongest **anchored** law is seeded by the bounded tensor slope ratio
  `|b_E / b_T|`
- so the current split is already organized by tensor endpoint data rather
  than by a free expression search

That is real progress, even though it still does not produce one unique
theorem-grade `a_u` law.

The follow-on resolution note now closes the next cycle on this same surface:
[QUARK_UP_AMPLITUDE_TENSOR_ENDPOINT_RESOLUTION_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_TENSOR_ENDPOINT_RESOLUTION_NOTE_2026-04-19.md)
shows that no exact identity `|b_E / b_T| = sqrt(7)` lands, and that the
restricted exact endpoint grammar still does not force one unique anchored
denominator. So this bridge note remains the right pre-resolution structural
statement, not the final endpoint.

## What this still does not close

This note still does **not** prove:

1. an exact tensor dynamics identification for the endpoint readout
2. an exact theorem that `|b_E / b_T| = sqrt(7)`
3. a single endpoint-derived quark law that beats both external baselines
   `7/9` and `sqrt(3/5)` at once

So the quark lane remains bounded. The current gain is structural compression,
not retained closure.

## Relation to the earlier quark notes

- [QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md](./QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
  isolates the remaining up-sector scalar gap.
- [QUARK_UP_AMPLITUDE_AFFINE_SUPPORT_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_AFFINE_SUPPORT_SCAN_NOTE_2026-04-19.md)
  identifies the `6/7`-centered affine family and its split winners.
- [QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE_2026-04-19.md)
  proves that no widened native affine law beats both external baselines at
  once.
- This note is the endpoint-derivation follow-on: it shows that the two
  surviving affine winners are already organized by current tensor endpoint
  data.
- [QUARK_UP_AMPLITUDE_TENSOR_ENDPOINT_RESOLUTION_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_TENSOR_ENDPOINT_RESOLUTION_NOTE_2026-04-19.md)
  closes the next theorem attempt with the bounded no-go endpoint on the
  current exact endpoint grammar.

## Validation

Run:

```bash
python3 scripts/frontier_quark_up_amplitude_tensor_endpoint_bridge.py
```

Current expected result on this branch:

- `frontier_quark_up_amplitude_tensor_endpoint_bridge.py`: `PASS=6 FAIL=0`
