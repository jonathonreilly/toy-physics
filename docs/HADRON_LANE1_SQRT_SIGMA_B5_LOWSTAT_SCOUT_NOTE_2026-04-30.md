# Lane 1 `sqrt(sigma)` B5 Low-Stat Finite-Volume Scout

**Date:** 2026-04-30
**Status:** support / pipeline scout; not B5 closure and no claim
promotion.
**Script:** `scripts/frontier_hadron_lane1_sqrt_sigma_b5_lowstat_scout.py`
**Lane:** 1 - Hadron mass program, route 3E `sqrt(sigma)` retained
promotion.

---

## 0. Result

The local `L=4,6,8` pure-gauge measurement pipeline works as a scout.
It should not be used as B5 closure.

The runner performs a fixed low-statistics `beta=6` `SU(3)` Metropolis
chain (`therm=6`, `meas=4`, `skip=1` per volume) and measures:

- plaquette mean and uncertainty;
- Wilson loops `W(1,1)`, `W(1,2)`, `W(2,2)`;
- `chi(2,2)` where the signal is positive;
- acceptance rate.

The pass criteria intentionally check only robust pipeline properties:
finite plaquette, usable acceptance, positive Wilson-loop signals, and
area ordering. They do not compare to the imported standard-QCD
`sigma a^2 = 0.0465` bridge constant.

## 1. Boundary

This is **not** B5 closure because:

- statistics are deliberately low;
- loops only reach `R,T <= 2`;
- `L=8` is still scout scale, not a multi-point asymptotic plateau;
- no production uncertainty target is claimed.

The value of the scout is operational: it validates a reusable pipeline
for plaquette/Wilson-loop/Creutz measurements before spending compute on
`L=8,12,16`.

## 2. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_lowstat_scout.py
```

Expected result:

```text
PASS=9 FAIL=0
```

## 3. Next Exact Action

Convert the scout into a resumable production runner:

- configurable `L`, therm, measurement count, skip, stride, and seed;
- append-only JSONL checkpoints;
- per-volume uncertainties;
- production target `L=8,12,16`;
- explicit wall-clock stop/resume behavior.

That production runner is the next realistic B5 tightening step.
