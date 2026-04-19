# Quark Up-Amplitude Tensor-Endpoint Resolution

**Date:** 2026-04-19
**Status:** bounded derive-or-no-go resolution on the exact endpoint grammar
**Primary runner:** `scripts/frontier_quark_up_amplitude_tensor_endpoint_resolution.py`

## Safe statement

The current branch still does **not** derive a unique reduced up-sector
amplitude law `a_u`.

This note resolves the next question left open by the earlier
tensor-endpoint bridge:

> can the bounded endpoint slope ratio `|b_E / b_T|` be promoted to the exact
> scalar-comparison denominator `sqrt(7)`, or do the current endpoint data
> stop one theorem short?

On current `main`, the answer is now clean:

- no exact identity `|b_E / b_T| = sqrt(7)` lands,
- the exact scalar-comparison denominator `sqrt(7)` is present and remains a
  strong anchored law,
- but the restricted exact endpoint grammar already contains other exact
  denominators that beat `sqrt(7)` on anchored aggregate,
- so the cycle resolves to a **bounded no-go**, not a positive `sqrt(7)`
  theorem.

The honest endpoint is:

- exact endpoint gap `1/6` fixes the best refit branch,
- bounded slope ratio `|b_E / b_T|` fixes the endpoint-data anchored branch,
- current endpoint data do not force their unification.

## Stage A: exact algebra pass

The runner first recomputes the endpoint readout directly from the live
support-tensor modules, not copied constants.

The exact endpoint atoms are:

```text
delta_A1(q_dem) = 1/42
6/7
1/6
1/sqrt(42)
1/sqrt(7)
sqrt(6/7)
sqrt(5/6)
```

The live endpoint readout ratios are:

```text
|b_E / b_T| = 2.621601678209
|a_T / a_E| = 2.005382749600
|b_T / a_T| = 1.000030814262
```

The direct exact anchored-law denominators from the same atom set are:

```text
6          -> anchor = 0.892%, refit max = 0.862%
sqrt(42)   -> anchor = 0.908%, refit max = 0.850%
sqrt(7)    -> anchor = 0.723%, refit max = 1.062%
sqrt(7/6)  -> anchor = 0.830%, refit max = 1.575%
```

The key negative Stage A result is:

- none of `|b_E / b_T|`, `|a_T / a_E|`, or `|b_T / a_T|` hits any of those
  direct exact denominators at machine precision,
- in particular `|b_E / b_T|` misses `sqrt(7)` by `0.912770%`.

So the positive route already fails at the exact-identity level.

## Stage B: restricted exact endpoint grammar

The runner then asks a narrower question:

> inside a bounded one-/two-step grammar built only from the exact endpoint
> atoms above, does the current surface force `sqrt(7)` or a unique anchored
> denominator?

The grammar sizes on the live branch are:

```text
one-step denominator grammar = 465
two-step denominator grammar = 20,934
```

The nearest exact grammar denominator to the bounded endpoint ratio
`|b_E / b_T|` is

```text
sqrt(7) - delta_A1 = 2.621941787255
```

with a relative gap of only `0.012973%`, but still **not** an exact identity.

The decisive no-go then comes from the anchored side.

The restricted exact grammar already contains the explicit exact counterexample

```text
sqrt(42/5) = 2.898275349238
```

which gives

- anchored aggregate deviation: `0.716%`
- anchored max deviation: `0.686%`
- refit max deviation: `1.031%`

That is already better on anchored aggregate than the exact scalar-comparison
denominator

```text
sqrt(7) = 2.645751311065
```

which gives anchored aggregate `0.723%`.

And this is not an isolated accident:

- the restricted exact two-step endpoint grammar contains **212** exact
  denominators that beat the direct `sqrt(7)` law on anchored aggregate.

So the exact endpoint grammar does **not** force `sqrt(7)`, and it does
**not** force a unique anchored denominator either.

## Stage C: endpoint verdict

The three important laws on the live branch are now:

### Exact refit branch

```text
d = 6
a_u = sin(delta_std) * (6/7 - delta_A1/6)
    = 0.778838292749
```

with

- anchored aggregate deviation: `0.892%`
- refit max deviation: `0.862%`

This remains the strongest current exact refit branch, sourced directly by the
support endpoint gap `1/6`.

### Exact scalar-comparison anchored branch

```text
d = sqrt(7)
a_u = sin(delta_std) * (6/7 - delta_A1/sqrt(7))
    = 0.774245730253
```

with

- anchored aggregate deviation: `0.723%`
- refit max deviation: `1.062%`

This remains a strong exact anchored law, but it is no longer a plausible
theorem endpoint because it is not uniquely selected even on the restricted
exact endpoint grammar.

### Bounded endpoint-data anchored branch

```text
d = |b_E / b_T|
a_u = sin(delta_std) * (6/7 - delta_A1/|b_E / b_T|)
    = 0.774170054824
```

with

- anchored aggregate deviation: `0.723%`
- anchored max deviation: `0.666%`
- refit max deviation: `1.065%`

This remains the strongest branch tied to the **actual endpoint data**
themselves. But because `|b_E / b_T|` is not exactly `sqrt(7)`, and because
the restricted exact grammar still does not force one unique anchored
denominator, it remains bounded rather than retained.

## Honest endpoint

The quark cycle now resolves cleanly to:

- exact `1/6` refit branch,
- bounded slope-ratio anchored branch,
- theorem-grade bounded no-go against a positive `sqrt(7)` derivation on the
  current endpoint surface.

That is the correct endpoint for this cycle. It is stricter than the earlier
tensor-endpoint bridge, but it still does **not** promote full retained quark
closure.

## Relation to the earlier quark notes

- [QUARK_UP_AMPLITUDE_TENSOR_ENDPOINT_BRIDGE_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_TENSOR_ENDPOINT_BRIDGE_NOTE_2026-04-19.md)
  organizes the split affine winners by endpoint data.
- [QUARK_UP_AMPLITUDE_AFFINE_SUPPORT_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_AFFINE_SUPPORT_SCAN_NOTE_2026-04-19.md)
  identifies the `6/7`-centered native family.
- [QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE_2026-04-19.md)
  proves that the widened affine family still does not yield one dominant law.
- This note closes the next theorem attempt on the current surface:
  no exact `sqrt(7)` endpoint identity lands, and the restricted exact
  endpoint grammar still does not force one anchored denominator.

## Validation

Run:

```bash
python3 scripts/frontier_quark_up_amplitude_tensor_endpoint_resolution.py
```

Current expected result on this branch:

- `frontier_quark_up_amplitude_tensor_endpoint_resolution.py`: `PASS=16 FAIL=0`
