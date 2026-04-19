# Quark Up-Amplitude Native Affine No-Go

**Date:** 2026-04-19
**Status:** bounded no-go on widened native affine support laws for the
remaining reduced quark amplitude
**Primary runner:** `scripts/frontier_quark_up_amplitude_native_affine_no_go.py`

## Safe statement

The current quark branch still does **not** derive the remaining reduced
up-sector amplitude `a_u`.

This note sharpens the earlier native-expression result by testing the
strongest affine-support family that is still easy to defend from the current
projector/support notes:

```text
a_u = sqrt(5/6) * (c0 + c1 delta_A1(q_dem))
```

with

- exact projector magnitude `sqrt(5/6)`,
- exact support datum `delta_A1(q_dem) = 1/42`,
- coefficients `(c0, c1)` drawn from a bounded one-step grammar on the native
  seven-site support constants.

The result is a clean bounded no-go:

- some native affine laws beat the external `7/9` refit baseline,
- different native affine laws beat the external `sqrt(3/5)` anchored
  baseline,
- but **no** native affine law beats both at once.

So the affine support family is stronger than the earlier clean structural
instance `sqrt(5/6) * (6/7)`, but it still does not promote the remaining
quark scalar to a forced law.

## Why this is the right next restriction

The support/tensor notes already privilege two exact ingredients:

- the quark projector magnitude `sqrt(5/6) = sin(delta_std)`,
- the support-side scalar `delta_A1`.

They also privilege an affine support grammar for the carrier/readout side.
So this is the natural next family to test after the one-step native
expression scan:

- keep the exact projector prefactor fixed,
- let the remaining support dressing be affine in `delta_A1`,
- but still restrict the affine coefficients to exact native constants rather
  than arbitrary real fits.

Without that last restriction the family would be too flexible and the test
would be vacuous.

## Widened affine family

The runner uses the bounded support-coefficient atoms

```text
{0, 1, rho, supp, 1/6, 1/7, 6, 7}
```

where

- `rho = 1/sqrt(42)`
- `supp = 6/7`

and widens them by one-step exact operations

```text
-x
1 - x
x + y
x - y
x * y
x / y
```

This yields

- `247` distinct support coefficients,
- `6624` distinct affine amplitude laws after deduplicating by amplitude value.

That is broad enough to make the negative result nontrivial.

## Main result

### Clean structural affine instance

The structurally clean law already singled out by the earlier notes is

```text
a_u = sqrt(5/6) * (1 - 6 delta_A1)
    = sqrt(5/6) * (6/7)
```

It remains close to closure, but it is not the strongest affine law on either
scoring axis.

So the no-go does not come from choosing too weak a clean instance and then
stopping.

### Best widened affine refit law

On the two-ratio refit axis, the best widened affine law is

```text
a_u = sqrt(5/6) * (supp + (-1/6)/(1-rho) * delta_A1)
     = 0.778177341267
```

with

- refit objective `0.052727`
- anchored CKM+`J` aggregate deviation `0.853%`
- full-package max deviation below `1%`

So the widened affine family is already strong enough to beat the external
`7/9` refit baseline.

### Best widened affine anchored law

On the anchored CKM+`J` axis, the best widened affine law is

```text
a_u = sqrt(5/6) * (1-rho + rho*supp * delta_A1)
     = 0.774886561056
```

with

- anchored CKM+`J` aggregate deviation `0.717%`
- anchored max component deviation `0.684%`
- refit objective `0.054385`

So the widened affine family is also strong enough to beat the external
`sqrt(3/5)` anchored baseline.

### The actual no-go

The key comparison is the intersection test:

- affine laws with refit score better than `7/9`: `9`
- affine laws with anchored score better than `sqrt(3/5)`: `9`
- affine laws that do both at once: `0`

That is the sharpest bounded result in this lane so far.

The failure is no longer:

- “affine support laws are too weak to matter.”

Instead it is:

- “even after widening the native affine support family enough to beat each
  external baseline separately, the family still splits and does not force one
  dominant law.”

## Interpretation

This sharpens the reduced quark endpoint again.

The branch now supports the following chain:

1. the projector-ray reduction isolates one remaining scalar `a_u`;
2. the parameter audit fixes the exact ray, exact down amplitude, and exact
   support-angle probe;
3. the widened candidate scan compresses the scalar to a bounded shortlist;
4. the native-expression scan shows the current one-step native grammar does
   not force one law;
5. this affine no-go shows that even the widened projector-prefactored affine
   `delta_A1` family still does not force one dominant law.

So the remaining gap is no longer “completely free,” but it is still not
theorem-forced on the current note stack.

## Relation to the earlier notes

- [QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md](./QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
  isolates the remaining scalar after exact-support anchoring.
- [QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md)
  compresses that scalar to a bounded shortlist.
- [QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md)
  gives the earlier restricted one-step grammar no-go.
- This note is the follow-on widened affine-support no-go.

## Validation

Run:

```bash
python3 scripts/frontier_quark_up_amplitude_native_affine_no_go.py
```

Current expected result on this branch:

- `frontier_quark_up_amplitude_native_affine_no_go.py`: `PASS=7 FAIL=0`
