# Wave Direct-dM Family Scout

**Date:** 2026-04-08
**Status:** exploratory single-seed family scout
**Claim type:** bounded_theorem

**Review repair perimeter (2026-04-28 generated-audit context):**
Generated-audit context before this narrowing identified this chain-closure
blocker: "The source note supports only
an exploratory one-seed, one-strength scout across Fam1/Fam2/Fam3.
The ledger has no runner_path for live verification, and the note
explicitly says it is not a portability, multi-seed, control-stack,
or continuum-stability claim." The repair target being addressed is
`runner_artifact_issue`: "run and audit a full
Fam1/Fam2/Fam3 portability batch with multiple seeds, S=0 nulls,
weak-strength sweeps, and both retained H values." This rigorization
edit only sharpens the boundary of the repair perimeter and
registers the live runner under "Cited authority chain (2026-05-10)"
below; nothing here promotes audit status. The "exploratory single-
seed family scout" status is exactly the bounded repair perimeter
the verdict identifies; the note already made the
non-portability-claim caveat explicit and that scope is unaffected.

This note records the smallest cross-family extension of the direct-`dM`
matched-schedule lane:

> Hold the direct-`dM` setup fixed, switch only the retained grown-family
> parameters `Fam1/Fam2/Fam3`, and ask whether the reference-strength
> matched-schedule effect keeps the same sign and stays material across
> the three canonical families.

This is **not** a portability claim. It is a one-seed, one-strength
scout designed to decide whether a larger portability batch is worth
running.

## Setup

- families: `Fam1 = (0.20, 0.70)`, `Fam2 = (0.05, 0.30)`, `Fam3 = (0.50, 0.90)`
- seed: `0`
- strength: `0.004`
- resolutions: `H = 0.5`, `0.35`
- same direct-`dM` schedule pair as the retained Fam1 note:
  - identical realized move trace
  - different timing of that trace within the active interval

## Result

| family | `H = 0.5` `R_hist` | `H = 0.35` `R_hist` | sign agreement |
| --- | ---: | ---: | ---: |
| `Fam1` | `-43.59%` | `-42.36%` | yes |
| `Fam2` | `-42.33%` | `-37.73%` | yes |
| `Fam3` | `-44.29%` | `-41.82%` | yes |

Reference-strength details:

| family | `H` | `dM(early)` | `dM(late)` | `delta_hist` | `delta_hist / s` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `Fam1` | `0.5` | `+0.005385` | `+0.009547` | `-0.004161` | `-1.040348` |
| `Fam1` | `0.35` | `+0.004811` | `+0.008346` | `-0.003535` | `-0.883765` |
| `Fam2` | `0.5` | `+0.005565` | `+0.009650` | `-0.004085` | `-1.021142` |
| `Fam2` | `0.35` | `+0.004743` | `+0.007617` | `-0.002874` | `-0.718417` |
| `Fam3` | `0.5` | `+0.005037` | `+0.009042` | `-0.004005` | `-1.001339` |
| `Fam3` | `0.35` | `+0.005022` | `+0.008632` | `-0.003610` | `-0.902451` |

## Honest read

This scout is directionally good:

- all three canonical families keep the same negative sign
- all six family/`H` points remain material in size
- the normalized effect stays in the same broad band: about `-38%` to
  `-44%`

What it still does **not** justify:

- not a portability promotion
- not a multi-seed statement
- not a full control-stack carryover on every family
- not a continuum-stability claim

So the safe bounded use of this note is:

> A one-seed, one-strength scout suggests the direct-`dM`
> matched-schedule effect is not obviously local to `Fam1`. All three
> canonical families keep the same negative sign and a material
> normalized effect at `H = 0.5` and `0.35`. A portability claim still
> requires the full null/linearity stack and multiple seeds per family.

## Next step

If this lane is worth widening, the next honest batch is:

- `Fam1/Fam2/Fam3`
- at least two seeds per family
- exact `S = 0` null on each family/seed
- weak-strength sweep `0.002, 0.004, 0.008`
- both retained `H` values

## Artifact chain

- [`scripts/wave_direct_dm_matched_history_probe.py`](../scripts/wave_direct_dm_matched_history_probe.py)
- [`logs/2026-04-08-wave-direct-dm-family-scout.txt`](../logs/2026-04-08-wave-direct-dm-family-scout.txt)

## Cited authority chain (2026-05-10)

The active runner registered for this scout is
[`scripts/wave_direct_dm_matched_history_probe.py`](../scripts/wave_direct_dm_matched_history_probe.py)
(declares `AUDIT_TIMEOUT_SEC = 1800`; audit-lane runner cache:
`status: ok`, elapsed ~100 s, exit 0, unmodified runner SHA pinned
by the cache). The runner is the same harness already cited in the
matched-history probe lane and is the named runner for the broader
direct-`dM` matched-schedule lane. The frozen scout output is
[`logs/2026-04-08-wave-direct-dm-family-scout.txt`](../logs/2026-04-08-wave-direct-dm-family-scout.txt).
This scout's explicit scope is one-seed (`seed=0`), one-strength
(`s=0.004`), and the two retained `H` values (`H=0.5, 0.35`) on the
three canonical retained families
`Fam1=(0.20, 0.70)`, `Fam2=(0.05, 0.30)`, `Fam3=(0.50, 0.90)`;
the headline same-sign / material-band readings in the result
table propagate the bounded perimeter of the upstream
runner exactly. The full portability batch the generated repair target's
repair target requires (multi-seed, S=0 nulls, weak-strength sweep,
both retained H values) is the named "Next step" lane below; that
batch is a separate runner workload, not a re-scoping of this scout
note. The scout's "Honest read" caveat list inside the note already
mirrors the bounded repair perimeter exactly.
