# Koide Q PMNS-Transfer Odd-Slot No-Go Note

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_q_pmns_transfer_odd_slot_no_go.py`
**Status:** executable no-go

RESIDUAL_SCALAR=`sigma_PMNS_transfer = 18*(2*y^2 - x^2)` and
`rho_odd_missing = r2`

## Theorem Attempt

The strongest retained-interface route after the Wilson coefficient no-go was:
specialize the positive PMNS `hw=1` transfer theorem to the charged-lepton
Koide cyclic carrier. The hope was that the PMNS aligned transfer kernel would
either supply the missing odd cyclic response or force the even response ratio
needed by the Koide circle.

## Brainstormed Variants

1. **Aligned transfer import:** use the positive PMNS kernel
   `T_seed = x I + y(C+C^2)` directly as a charged-lepton cyclic source law.
2. **Dominant-mode value law:** test whether the eigenvalue pair
   `(lambda_+, lambda_-)` fixes `y/x`.
3. **Odd-slot extension:** ask whether the PMNS commutant/orientation selector
   can provide the missing `r2` channel.
4. **Assumption inversion:** maybe transfer-only data are too coarse; test
   whether off-seed source profiles share the same transfer summary.
5. **Full source-transfer pack:** only a supplied source-response pack can see
   the breaking carrier; importing it would need a new charged-lepton source
   theorem.

Ranking for this cycle:

1. PMNS transfer odd-slot route: strongest retained interface not already
   covered by the Wilson no-go.
2. PMNS commutant orientation route: likely supplies a bit, not a radius.
3. Full source-transfer pack transplant: too close to adding a source
   primitive unless derived on the charged surface.
4. Delta Wilson-line phase route: only after Q routes keep failing.
5. Color-sector correction: cross-sector support, not a charged-lepton
   source law.

## Executable Result

The retained PMNS aligned transfer kernel is

```text
T_seed = x I + y(C + C^2).
```

On the Koide cyclic basis

```text
B0 = I
B1 = C + C^2
B2 = i(C - C^2),
```

the responses are exactly

```text
r0 = 3x
r1 = 6y
r2 = 0.
```

So the aligned PMNS transfer image is reflection-even. It does not supply the
odd cyclic slot.

The response-circle residual becomes

```text
sigma_PMNS_transfer = r1^2 + r2^2 - 2 r0^2
                    = 18(2 y^2 - x^2).
```

The PMNS transfer eigenvalues are

```text
lambda_+ = x + 2y
lambda_- = x - y.
```

They reconstruct the seed pair exactly:

```text
x = (lambda_+ + 2 lambda_-)/3
y = (lambda_+ - lambda_-)/3.
```

That reconstruction has rank `2`; it does not select `y/x`. Exact off-circle
transfer-compatible witnesses:

```text
y = 0    -> sigma_PMNS_transfer = -18
y = 1/2  -> sigma_PMNS_transfer = -9
```

The circle-compatible value

```text
y/x = 1/sqrt(2)
```

is one special coefficient law, not a theorem supplied by the transfer
spectrum.

## Off-Seed Blindness

The runner also checks an exact symbolic version of the PMNS boundary theorem:
distinct off-seed active profiles can share the same transfer means. Transfer
sees `xbar,ybar`; zero-sum breaking directions are invisible until
source-response columns are supplied.

That matters for Koide because importing the full PMNS source-response pack
would be a new charged-lepton source theorem unless derived on the charged
surface itself.

## Odd-Slot Extension

If an additional retained orientation route supplied a real odd coefficient
`z`, the full response map would be

```text
r0 = 3x
r1 = 6y
r2 = 6z.
```

This restores the three-response carrier but still leaves

```text
sigma_full = -18 x^2 + 36 y^2 + 36 z^2.
```

So odd-slot existence alone is not enough. The missing law would be

```text
y^2 + z^2 = x^2/2.
```

## Hostile Review

- **Circularity:** the runner does not set the response circle; it tests the
  transfer image and finds the residual.
- **Target import:** no mass-table data, external observational pin, `H_*`
  witness, or Koide value enters the derivation.
- **Hidden selector:** the needed relation `y^2 + z^2 = x^2/2` would be a new
  source/radius law.
- **Axiom link:** PMNS transfer gives a positive aligned seed-pair theorem, but
  not a charged-lepton coefficient-radius theorem.
- **Scope:** this rejects importing the aligned PMNS transfer law as Koide
  closure. A future charged-surface source-response theorem would be a new
  route, not covered by this no-go.

## Verdict

The PMNS `hw=1` transfer interface is useful retained support, but it does not
derive the charged-lepton Koide source law.

```text
PMNS_TRANSFER_FORCES_K_TL=FALSE
KOIDE_Q_PMNS_TRANSFER_ODD_SLOT_CLOSES_Q=FALSE
RESIDUAL_SCALAR=sigma_PMNS_transfer=18*(2*y^2-x^2);rho_odd_missing=r2
```
