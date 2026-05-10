# ALT-Connectivity Grown DAG Family Operator-Cauchy Note

**Date:** 2026-05-10
**Claim type:** no_go (bounded numerical no-go for the ensemble-size
operator-Cauchy bridge on this alt-connectivity grown DAG harness)
**Status:** source-note proposal only; independent audit controls any retained
status.
**Status authority:** independent audit lane only.

## Artifact Chain

- [`scripts/alt_connectivity_family_operator_cauchy.py`](../scripts/alt_connectivity_family_operator_cauchy.py)
- [`logs/runner-cache/alt_connectivity_family_operator_cauchy.txt`](../logs/runner-cache/alt_connectivity_family_operator_cauchy.txt)
- rescaled NN harness results are comparison context only; this note does not
  promote or depend on the open continuum/operator claims in that lane.
- alt-connectivity-family context:
  - [`docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md`](ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md)
  - [`docs/ALT_CONNECTIVITY_FAMILY_FAILURE_NOTE.md`](ALT_CONNECTIVITY_FAMILY_FAILURE_NOTE.md)

## Question

Does the operator-Cauchy continuum-bridge test used in the rescaled NN lane
extend to this alt-connectivity grown DAG family when the only available
refinement axis is seed-ensemble size?

## Harness Structure (Findings)

The alt-connectivity harness is built on `grow(drift, seed)` from
`gate_b_no_restore_farfield` with the parity-rotated sector-transition rule
from `ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP._build_alt_connectivity`. It has the
following relevant parameters:

- `drift` in `[0.0, 0.5]`: per-layer Gaussian-jitter scale on node
  positions. The basin survives mid-drift; small/large drift are less stable
  (BASIN_NOTE: 32/45 pass).
- `seed`: RNG seed; controls per-seed DAG realization for drift > 0.
- `H = 0.5`, `NL = 25`, `PW = 8`: **hardcoded at module scope** in
  `gate_b_no_restore_farfield.py`. Not exposed as constructor arguments.

**There is no clean h-like spacing-refinement knob.** The candidate
refinement axes are:

| Axis | Verdict |
| --- | --- |
| `H -> 0` | not available — `H` is a module constant, not a parameter |
| `drift -> 0` | degenerate — drift=0 is a deterministic regular-grid point that is structurally separate from the drift>0 stochastic family the harness was built to study |
| Generation index `NL` | not refining a continuum; just makes the DAG longer |
| Ensemble size `N -> infinity` | the only available refinement axis |

We therefore adapt operator-Cauchy from spacing-refinement to
**ensemble-refinement**: at fixed drift, the seed ensemble is i.i.d. and the
ensemble mean has a CLT limit, so

```
vec(N; drift) := (1/N) sum_{seed=0}^{N-1} obs(seed, drift, source_z)
```

should be Cauchy in `N` with rate `N^{-1/2}` if the harness has any
continuum-limit object at all.

## Method

- **Refinement grid:** `N in {2, 4, 8, 16, 32, 64}` (geometric)
- **Drift fixed at 0.10** (mid-basin per BASIN_NOTE; drift=0.10 is one of
  the most stable rows in the existing sweep)
- **Source-position basis:** three `source_z` values `{2.0, 3.0, 4.0}`
- **Observable basis (5 framework observables):** `plus`, `minus`,
  `neutral`, `double`, `exponent` — the same observables the existing
  BASIN/FAILURE notes track
- **Vector dimension:** 5 x 3 = **15**, matching the comparison basis
  dimension used in the rescaled NN lane
- **Cauchy increment:** `||vec(N) - vec(2N)||_2`
- **Fit:** geometric decay `||vec(N) - vec(2N)||_2 ~ C * N^r`
- **Gate:** Cauchy convergence requires `r < -0.4` and `R^2 >= 0.85`; the CLT
  prediction is `r = -1/2`.

Two ensemble variants are reported:

1. **All-seeds:** the raw ensemble mean over `seed in {0..N-1}` — direct
   analog of the NN-harness 15-vector
2. **On-basin:** per-component, restrict to seeds whose row passes the
   basin gate (`zero=0`, `neutral<1e-12`, `plus>0`, `minus<0`, weak-charge
   exponent ~ 1)

## Result

```
ZERO-SOURCE BASELINE GUARD:  max |zero| across 64 seeds x 3 source_z = 0.00e+00   PASS
BASIN MEMBERSHIP:            42/64 at z=2.0, 41/64 at z=3.0, 42/64 at z=4.0
                             (consistent with BASIN_NOTE's 32/45 ~ 71% basin density)

ENSEMBLE-CAUCHY (ALL SEEDS):
   N1 -> N2     ||vec(N1) - vec(N2)||_2
    2 ->   4    4.957e-04
    4 ->   8    3.657e-05
    8 ->  16    4.012e-04
   16 ->  32    4.591e-04
   32 ->  64    2.588e-04
   Fit:  r = +0.1775,  C = 1.59e-04,  R^2 = 0.0318       GATE FAIL

ENSEMBLE-CAUCHY (ON-BASIN SEEDS ONLY):
   N1 -> N2     ||vec(N1) - vec(N2)||_2
    2 ->   4    3.135e-04
    4 ->   8    3.173e-05
    8 ->  16    6.365e-04
   16 ->  32    2.423e-04
   32 ->  64    1.389e-04
   Fit:  r = +0.0585,  C = 1.60e-04,  R^2 = 0.0032       GATE FAIL
```

**Both ensemble-Cauchy fits fail decisively.** The increments are
non-monotonic in `N`, R^2 is essentially zero, and the fitted exponent has
the **wrong sign** for Cauchy convergence (positive, where CLT predicts
`-1/2`).

Per-component decay rates show the same pattern: `plus`, `minus`, `double`
all have `r ~ +0.18` with `R^2 ~ 0.15-0.25`, far from the CLT prediction of
`r = -1/2` with `R^2 -> 1`.

## Diagnosis (Bounded Mechanism for the Null)

The harness has **two coupled obstructions** to clean Cauchy refinement:

### Obstruction 1: Heavy-tailed seed distribution

Single-seed measurements span ~3 orders of magnitude with no apparent
typical scale:

```
  plus@z=3 seed=14: +5.6e-07     (smallest)
  plus@z=3 seed=63: -9.2e-05     (largest, ~ 165x bigger and opposite sign)
  plus@z=3 typical: ~5e-6
```

The seed distribution is heavy-tailed with both signs. A small number of
outlier seeds (e.g. seeds 7, 13, 22, 36, 40, 57, 63) dominate the partial
sums, and adding 1-2 such outliers can dwarf the contributions of 30+
typical seeds. This destroys the `N^{-1/2}` CLT decay rate the
ensemble-Cauchy method requires: the increment from `N` to `2N` is
non-monotonic because it depends entirely on whether the new seeds
happened to include a heavy-tail draw.

### Obstruction 2: Seed-selective sign-orientation boundary

The basin is seed-selective (BASIN_NOTE: 32/45 pass; reproduced here at
42/64 ~ 66%). On-basin restriction does not fix the fit (`r = +0.0585`,
`R^2 = 0.003`) because:

- conditioning on "basin pass" introduces a selection bias that breaks the
  i.i.d. structure CLT requires
- the heavy-tail seeds that pass the basin gate (e.g. seed 24 with
  plus = +4.8e-5, seed 59 with plus = +4.6e-5) still dominate the partial
  sums

This is consistent with FAILURE_NOTE's finding: the misses are sign
reversals, not magnitude blow-ups, and the family flips orientation on a
subset of seeds. The orientation flip is the same effect that produces the
heavy-tailed seed distribution.

### Why no h-like axis is available

Unlike the rescaled NN harness, the alt-connectivity construction is
intrinsically a **stochastic discrete process**. There is no continuum PDE
underneath whose discretization at finer `h` would converge to it. The
`drift -> 0` limit is a structurally different deterministic system, not a
continuum limit of the drift>0 family. The closest analog of an `h`
refinement is therefore the ensemble axis, and the ensemble axis fails for
the reasons above.

## Comparison with the Rescaled NN Harness Context

|                          | rescaled NN lane context  | alt-connectivity (this note) |
| ---                      | ---                       | ---                          |
| refinement axis          | lattice spacing `h -> 0`  | ensemble size `N -> infinity` |
| observable dimension     | 15 (5 obs x 3 sources)    | 15 (5 obs x 3 sources)       |
| Cauchy decay rate `r`    | spacing-fit context       | +0.1775 (all) / +0.0585 (basin) |
| R^2                      | spacing-fit context       | 0.0318 / 0.0032              |
| verdict in this note     | not re-audited here       | bounded no-go for this adapted test |
| operator identification  | not promoted here         | none; ensemble-Cauchy gate fails |

## Safe Read

The operator-Cauchy continuum-bridge method is **harness-specific**. It
extends cleanly to harnesses with a genuine spacing-refinement axis (the
rescaled NN lattice) and an underlying PDE-like continuum, but it does not
extend to the alt-connectivity grown DAG family because:

1. the harness has no `h`-like refinement parameter (`H` is a module
   constant; `drift -> 0` is a degenerate point; the construction is
   intrinsically stochastic)
2. the only available refinement axis (ensemble size `N`) is contaminated
   by a heavy-tailed seed distribution coupled to a seed-selective
   sign-orientation boundary; the resulting `||vec(N) - vec(2N)||_2`
   curve is non-monotonic and the geometric-decay fit has `R^2 = 0.03`

This is bounded evidence that this alt-connectivity harness does not support
the specific ensemble-size operator-Cauchy bridge tested here. Any repo-wide
promotion-map or C-class consequence must be handled by the audit lane or a
separate reviewed mapping note.

## What This Supports

- A bounded no-go for this tested alt-connectivity grown DAG harness under the
  seed-ensemble operator-Cauchy adaptation.
- A bounded mechanism for the failed fit, with quantitative evidence:
  Cauchy fit `r = +0.18` (wrong sign), `R^2 = 0.03` (no geometric decay),
  ensemble distribution heavy-tailed with sign reversals.
- Zero-source baseline guard is **exact** (`0.00e+00` across all 64 x 3
  measurements), confirming the harness's existing controls survive at
  larger ensemble size than the basin sweep tested.

## What This Does Not Close

- This does not rule out **some** continuum-bridge method working on the
  alt-connectivity family; it only rules out the tested averaged and on-basin
  ensemble-Cauchy variants. A method that explicitly models the heavy-tailed
  seed distribution (e.g. median-of-seeds, or on-basin orientation-aligned
  averaging with explicit sign-correction) might recover ensemble-Cauchy but
  would require a separate registered derivation.
- The cousin alt-connectivity tables (sixth-family sheared, moving-source
  cross-family) were not re-tested under this method; they share the
  drift/seed structure but with different connectivity rules. This note only
  makes them follow-up targets; it does not assign them this verdict by
  inheritance.

## Conclusion

**The tested ensemble-size operator-Cauchy bridge does not close on this
alt-connectivity grown DAG harness.** This is a bounded no-go: the harness
lacks a clean spacing-refinement parameter, and the ensemble-refinement
substitute fails because the seed distribution is heavy-tailed with
sign-orientation flips. It is evidence against using this operator-Cauchy
adaptation as a continuum bridge for the tested harness, not a repo-wide
promotion or status change.
