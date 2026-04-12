# Irregular Endogenous Sign Observable Note

**Date:** 2026-04-11  
**Script:** `scripts/frontier_irregular_endogenous_sign_observable.py`  
**Status:** final hold, not retained

## Question

Can a transport observable on the same low-screening irregular surface close
the endogenous sign lane after the shell-packet family and size portability
checks failed?

This probe stays on the same irregular bipartite families and keeps the packet
family fixed. It only changes the observable:

- signed inward boundary current across BFS cuts `k = 1, 2`
- time-integrated impulse of that same boundary current

No packet-family sweep is used here.

## Design

Surface:

- `mu2 = 0.001`
- same irregular families as the retained shell-packet lane
- same graph-center source rule
- same outward shell packet

Audited families:

- random geometric (`side=8`)
- growing (`n_target=64`)
- layered cycle (`8x8`)

Seeds:

- `42..46`

Couplings:

- `G = 5, 10`

Rows:

- `30`

## Observable

For each run, the probe measures:

1. `cut1_margin`
   - inward current across the `k = 1` BFS cut, comparing `+Phi` and `-Phi`
2. `cut2_margin`
   - inward current across the `k = 2` BFS cut, comparing `+Phi` and `-Phi`
3. `impulse_margin`
   - time-integrated inward current across the `k = 1` cut

Positive margins mean attraction produces more inward transport than
repulsion on the same surface.

## Result

### Global

| Metric | Positive rows | Mean | Minimum |
|---|---:|---:|---:|
| `cut1_margin` | `26/30` | `+9.42e-03` | `-7.18e-02` |
| `cut2_margin` | `9/30` | `-1.85e-04` | `-4.62e-03` |
| `impulse_margin` | `26/30` | `+1.02e-02` | `-7.76e-02` |

Norm drift stayed machine-clean:

- `max_norm_drift = 1.33e-15`

### Family readout

- `random_geometric`: `cut1` and `impulse` are positive on all `10/10` rows,
  but `cut2` is negative on all `10/10` rows.
- `growing`: the transport signal is mixed; `cut1` and `impulse` only reach
  `3/5` positives per coupling and `cut2` stays near zero or negative.
- `layered_cycle`: `cut1` and `impulse` are positive on all `10/10` rows, but
  `cut2` is negative at `G=10`.

## Honest Verdict

This transport probe is cleaner than the earlier density-margin readout, but
it still does **not** close the irregular endogenous sign lane.

What it shows:

- `cut1` and `impulse` do favor attraction on most audited rows
- the low-screening shell-packet surface still carries a real same-surface
  transport asymmetry

What it does not show:

- portable closure across all audited rows
- a uniform transport separator on the same irregular surface
- a final retained sign law for arbitrary irregular observables

The key blocker is the `k = 2` cut, which flips negative on most of the
audited surface. So this is a stronger same-surface transport diagnostic, but
still a hold.

## Retain / Hold

- `retain`: no
- `hold`: yes

If this lane is reopened, the next credible step is a different transport
definition on the same irregular surface, not another packet-family sweep.
