# Persistent Object Multistage Floor Sweep

**Date:** 2026-04-16  
**Status:** bounded multistage floor positive; `top4` is the first self-maintaining floor on the stable widened exact-lattice branch

## Artifact chain

- Audit closure runner:
  [`scripts/persistent_object_multistage_floor_certificate.py`](../scripts/persistent_object_multistage_floor_certificate.py)
- Audit closure cache:
  [`logs/runner-cache/persistent_object_multistage_floor_certificate.txt`](../logs/runner-cache/persistent_object_multistage_floor_certificate.txt)
- Slow parameterized multistage probe:
  [`scripts/persistent_object_top3_multistage_probe.py`](../scripts/persistent_object_top3_multistage_probe.py)
- `top3` completed cache:
  [`logs/runner-cache/persistent_object_top3_multistage_probe.txt`](../logs/runner-cache/persistent_object_top3_multistage_probe.txt)
- `top4` completed transfer cache, whose listed cases include the same five
  stable widened-regime rows:
  [`logs/runner-cache/persistent_object_top4_multistage_transfer_sweep.txt`](../logs/runner-cache/persistent_object_top4_multistage_transfer_sweep.txt)
- `top5` completed repair-pass log:
  [`outputs/persistent_object_top5_multistage_probe_2026-05-06.txt`](../outputs/persistent_object_top5_multistage_probe_2026-05-06.txt)

## Audit closure certificate

The audit-facing certificate is the first listed runner so the restricted
audit packet contains the load-bearing floor comparison directly. It reports:

- `top3`: `0 / 5` on the five stable widened-regime rows, from the fresh
  SHA-pinned `top3` cache.
- `top4`: `5 / 5` on those same rows, extracted from the fresh SHA-pinned
  `top4` transfer-sweep cache.
- `top5`: `5 / 5` from a completed live run of the same parameterized
  multistage probe with `--top-keep 5`.
- `top6`: `5 / 5` by exact source-cardinality identity. The source cluster has
  five nodes, and `_topk_weights` keeps `min(top_keep, len(source_probs))`;
  therefore `top6` has the same effective retained support and same gate
  result as `top5` in this setup.

Current certificate summary:

```text
FLOOR TABLE
  top3: 0/5
  top4: 5/5
  top5: 5/5
  top6: 5/5
[PASS] first admissible retained object width is top4

SUMMARY: PASS=28 FAIL=0
STATUS: FLOOR CERTIFICATE PASS
```

## Question

The first multistage probe closed `top3` as an honest self-maintaining object:

- compressed carry stayed perfect
- the response law stayed perfectly stable
- but within-segment overlap fell below the retained persistence bar

That left one last bounded diagnostic on this exact route:

> is `top3` simply too narrow, with a slightly broader retained object class as
> the real self-maintaining floor?

## Frozen setup

Fixed across the floor sweep:

- exact lattice with `h = 0.25`
- retained blended readout `blend = 0.25`
- source strengths `0.001, 0.002, 0.004, 0.008`
- three updates per segment
- three chained segments
- same stable widened-regime rows used in the `top3` multistage probe

Object widths tested:

- `top3`
- `top4`
- `top5`
- `top6`

Frozen gates:

- every segment keeps mean update overlap `>= 0.90`
- every stage-to-stage carry mean `>= 0.90`
- every stage-to-stage carry minimum `>= 0.85`
- every segment keeps `4/4` `TOWARD`
- every segment keeps `F~M` in `[0.95, 1.05]`
- stage-to-stage `kappa` drift `<= 10%`

## Frozen result

### Headline

`top4` is already enough.

Multistage-admissible totals on the stable widened-regime rows:

- `top3`: `0 / 5`
- `top4`: `5 / 5`
- `top5`: `5 / 5`
- `top6`: `5 / 5`

So the first honest self-maintaining floor on this exact-lattice branch is:

> `top4`, not `top3`

### Why `top4` changes the branch verdict

The multistage failure at `top3` was real, but it was also narrow.

At `top4`, the stable widened-regime rows all clear the retained persistence
bar:

- baseline stage overlaps: `[0.956, 0.956, 0.956]`
- source1.5 stage overlaps: `[0.958, 0.971, 0.971]`
- source2.75 stage overlaps: `[0.960, 0.921, 0.921]`
- width5 stage overlaps: `[0.954, 0.964, 0.964]`
- length8 stage overlaps: `[0.965, 0.946, 0.946]`

And the rest of the structure remains perfectly clean:

- carry mean: `[1.000, 1.000]` on every tested row
- carry min: `[1.000, 1.000]` on every tested row
- max `kappa` drift: `0.000%` on every tested row

So the honest read is no longer:

> only a compression-stabilized transfer object

It is now:

> a self-maintaining multistage exact-lattice compact object on the stable
> widened branch, with `top4` as the first retained floor

### Why `top5` and `top6` do not matter much

They also pass `5 / 5`, but they do not buy a qualitatively stronger claim.

The key scientific change already occurs at `top4`:

- `top3` fails
- `top4` passes

So the floor is localized enough to be useful.

## Safe read

This revives the exact-lattice compact-object route.

The branch now has:

- nearby-family transfer
- second-ring partial transfer
- a mapped inward-source boundary
- a self-maintaining multistage object on the stable widened branch
- the first retained multistage floor at `top4`

So the correct interpretation is:

> the exact-lattice compact-object lane is still alive, and the strongest
> honest statement is now a bounded self-maintaining multistage `top4` object
> on the stable widened branch, not merely a compression-stabilized `top3`
> transfer object.

## What this proves

- the failure at `top3` was a narrow floor miss rather than the end of the
  whole exact-lattice route
- the first self-maintaining multistage floor is `top4`
- broader classes `top5` and `top6` are unnecessary for the core survival
  claim

## What it does not prove

- transfer of the `top4` multistage floor across the full widened local pocket
- persistent inertial-mass closure
- matter closure

## Branch verdict

The persistent-object branch is stronger again:

1. `top3` identified the local transfer-positive branch
2. `top3` failed the honest multistage bar
3. `top4` clears that same multistage bar on the stable widened rows

So the correct branch verdict is:

> the exact-lattice route is not frozen; it now has a bounded self-maintaining
> multistage compact-object floor at `top4`.

## Best next move

The next tight move is now:

1. a `top4` multistage transfer sweep across the widened local pocket,
   especially the second-ring rows and the mapped inward-source boundary
2. if that fails quickly, freeze the route as:
   - stable-branch multistage positive
   - widened-pocket non-universal
   - no closure-grade persistent inertial mass yet
