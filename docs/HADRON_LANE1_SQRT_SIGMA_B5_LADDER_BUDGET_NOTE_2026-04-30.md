# Lane 1 `sqrt(sigma)` B5 Finite-Volume Ladder Budget

**Date:** 2026-04-30
**Status:** support / compute-budget audit; no theorem or claim
promotion. This note decides whether a local `L = 4, 6, 8` pure-gauge
ladder can materially close the `(B5)` framework-to-standard-QCD bridge
for Lane 1 `sqrt(sigma)`.
**Script:** `scripts/frontier_hadron_lane1_sqrt_sigma_b5_ladder_budget.py`
**Lane:** 1 - Hadron mass program, route 3E `sqrt(sigma)` retained
promotion.

---

## 0. Result

An `L = 4, 6, 8` local ladder is a useful **scout, not closure**.

It can quantify finite-volume drift in the existing `4^4` check and
prepare the measurement pipeline. It cannot by itself retain `(B5)`
because it has too little large-loop leverage for an asymptotic Wilson /
Creutz / force-scale comparison.

The first B5-closing compute class is:

```text
production ladder: L = 8, 12, 16
```

or an equivalent theorem that bypasses framework-side large-volume
measurement.

## 1. Cost Scaling

For a four-dimensional pure-gauge Wilson lattice:

| `L` | sites `L^4` | links `4 L^4` | per-sweep cost vs `L=4` | conservative max square-loop `R` |
|---:|---:|---:|---:|---:|
| 4 | 256 | 1024 | 1x | 2 |
| 6 | 1296 | 5184 | 5.1x | 3 |
| 8 | 4096 | 16384 | 16x | 4 |
| 12 | 20736 | 82944 | 81x | 6 |
| 16 | 65536 | 262144 | 256x | 8 |

Memory is not the main blocker through `L=16`; raw complex128 `SU(3)`
links are under 40 MiB. The blocker is sampling cost and Wilson-loop
signal/noise at larger loops.

## 2. Why `L=4,6,8` Does Not Close

- `L=4` cannot test square loops beyond about `R=2`.
- `L=6` first reaches `R=3`, but only at the edge of the periodic box.
- `L=8` reaches `R=4`, but does not provide a multi-point asymptotic
  plateau.

B5 is not asking for another positive short-distance Creutz ratio. It
asks whether the framework substrate reproduces standard lattice-QCD
large-volume Wilson/Creutz/static-force observables with an uncertainty
budget. The local ladder is therefore only a drift diagnostic.

## 3. Required Observable Packet

Any B5 tightening attempt should report the same packet at each volume:

- plaquette mean and uncertainty;
- Wilson loops `W(R,T)`;
- Creutz ratios `chi(R,T)`;
- static-force or `r0`/`r1` proxy;
- same `beta=6` and action policy across volumes;
- explicit comparison to the standard-QCD bridge constants currently
  imported by `CONFINEMENT_STRING_TENSION_NOTE.md`.

## 4. Gate Model

| Plan | Framework measurement | Volume drift | Large-loop window | Uncertainty target | Closes B5? |
|---|---:|---:|---:|---:|---:|
| current `L=4` only | yes | no | no | no | no |
| local `L=4,6,8` scout | yes | yes | no | yes | no |
| production `L=8,12,16` ladder | yes | yes | yes | yes | yes |

This is a compute-budget no-go for local closure, not a physics no-go.

## 5. Claim-State Movement

Cycle 4 narrows the next B5 route:

```text
L=4-only evidence             -> too small
L=4,6,8 local ladder          -> scout / drift diagnostic
L=8,12,16 production ladder   -> first B5-closing compute class
```

Safe statement:

> The B5 framework link is compute-limited on the local surface. A local
> `L=4,6,8` ladder can improve residual accounting but should not be
> presented as retention. Retention requires a larger ladder or a theorem.

## 6. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_ladder_budget.py
```

Expected result:

```text
PASS=13 FAIL=0
```

## 7. Next Exact Action

Run either:

1. a fast `L=4,6,8` scout with low statistics to estimate finite-volume
   drift and validate the measurement pipeline; or
2. a production-oriented runner with resumable output and checkpointing
   for `L=8,12,16`.

The second route is the first one capable of materially tightening B5.
