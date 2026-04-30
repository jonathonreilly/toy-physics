# Opportunity Queue

Campaign mode remains active under the 12-hour request. Ranking favors
retained-positive probability, missing-import reduction, available runners,
review landability, and low repo-wide blast radius.

## 1. B5 Production Wilson/Creutz Statistics

**Route:** resume `frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder.py`
with `--profile production` under wall-clock checkpoints.

**Current checkpoint:** `L=8` has `1000/1000` production measurements after
`10239` sweeps. `L=12` has `76/1000` production measurements after `981`
sweeps. `L=16` has not started.

**Why first:** it directly attacks the named active residual: the
framework-to-standard-QCD bridge for imported `sqrt(sigma)` / static-energy
values.

**Expected status movement:** bounded support can become materially stronger
or the route can fail with a quantified obstruction.

**Blockers:** Python runtime may be slow; production evidence still needs
uncertainty aggregation after enough JSONL records accumulate.

## 2. B5 Production Aggregator / Uncertainty Gate

**Route:** add a JSONL aggregation runner that consumes production records,
computes per-volume means/errors, tests volume drift, and states whether the
current data are below closure threshold.

**Why second:** production data without an uncertainty gate cannot move B5.

**Expected status movement:** converts raw measurements into a reviewable
bridge-state statement.

**Blockers:** needs enough production records to be meaningful.

## 3. Force-Scale Observable Pivot

**Route:** draft a branch-local bounded-support packet choosing `r0`/`r1` as
the Lane 1 force-scale observable and keeping `sqrt(sigma)` as a comparator.

**Why third:** if finite-window `sigma` remains convention-split, `r0`/`r1`
may be the cleaner B2 observable.

**Expected status movement:** isolates a less ambiguous B2 target, but B5
still remains open.

**Blockers:** still imports external standard-lattice values and does not
derive framework-side B5.

## 4. Lane 3 Light-Quark Sum Pivot

**Route:** pivot to the Lane 3 `m_u + m_d` blocker if B5 production compute
stalls or produces no reviewable movement after the deep block.

**Why fourth:** it is independent of the `sqrt(sigma)` bridge and unblocks
GMOR-style pion work.

**Expected status movement:** possible import retirement or sharper no-go on
the light-quark input.

**Blockers:** requires a separate grounded route portfolio before execution.
