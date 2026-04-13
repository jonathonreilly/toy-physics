# Strong-Field Gravity Attack Plan

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Purpose:** Codex-owned research plan for the strongest remaining gravity upside:
full nonlinear / strong-field closure beyond the retained weak-field surface.

## Current honest state

The repo already supports a strong weak-field gravity surface:

- Poisson / Newton chain
- weak-field WEP
- weak-field time dilation

It does **not** yet support full nonlinear GR closure.

The strongest currently defensible strong-field statement is narrower:

- within the current conformal spatial-metric ansatz and leading
  self-consistency closure, the lattice point-source fixed point remains
  spatially nondegenerate
- this is **not** the same thing as a fully derived strong-field spacetime
  metric

## Do not retread these solved or near-solved substeps

The attack should **not** spend time redoing the following:

- weak-field Poisson / Newton derivation
- weak-field WEP or weak-field time dilation
- broad eikonal discussion as if that by itself gives strong-field closure
- old Schwarzschild-at-`r = R_S + l_P` arguments

Those are not the live blocker.

## Exact load-bearing blocker

The live blocker is:

> The repo does not yet derive a nonlinear **4D spacetime closure** tying the
> spatial conformal factor, the temporal sector, and matter backreaction into
> one self-consistent strong-field equation.

Concretely, the current strong-field branch still relies on two load-bearing
extensions that are not yet theorem-grade:

1. the weak-field conformal spatial form `g_ij = (1 - phi)^2 delta_ij` is
   extended into the strong-field regime
2. the backreaction law used in the fixed-point solve is inserted as a
   self-consistency ansatz rather than derived from the exact lattice
   propagator / Hamiltonian

Until those are replaced by a genuine nonlinear closure, the following stay
bounded or conditional:

- full strong-field metric
- no-horizon as a physics claim
- no-echo as a theorem-grade consequence
- any “full GR derived” wording

## Best derivation route already latent in the repo

The shortest credible route is **not** another phenomenology note. It is a
propagator-based metric reconstruction program:

1. start from the exact lattice propagator in background field form, not from
   Schwarzschild
2. derive the strong-field **spatial** metric from propagator decay / path cost
   without importing the continuum metric interpretation by hand
3. derive the strong-field **temporal** component from the phase / time-dilation
   sector on the same background
4. combine them into a single 4D metric candidate
5. compute Ricci / Einstein residuals or a Regge-lattice analog and test
   whether a closed nonlinear vacuum equation is actually satisfied

This route stays on the framework’s strongest native surface:

- path-sum action
- propagator-defined geometry
- self-consistency closure
- already-retained weak-field gravity

## Specific files to reuse

These are the strongest starting points already in the repo:

- `docs/GRAVITY_CLEAN_DERIVATION_NOTE.md`
- `docs/BROAD_GRAVITY_DERIVATION_NOTE.md`
- `docs/SPATIAL_METRIC_DERIVATION_NOTE.md`
- `docs/STRONG_FIELD_METRIC_NOTE.md`
- `docs/LATTICE_NO_HORIZON_NOTE.md`
- `scripts/frontier_broad_gravity.py`
- `scripts/frontier_strong_field_metric.py`
- `scripts/frontier_strong_field_extension.py`
- `scripts/frontier_lattice_no_horizon.py`

Use them as inputs. Do **not** assume their strongest status labels are already
paper-safe.

## Concrete attack sequence

### Attack 1: replace the strong-field self-consistency ansatz with a derived nonlinear equation

Current gap:

- the point-source fixed-point equation is elegant, but the backreaction law is
  not yet derived from the exact lattice propagator

Required outcome:

- derive the effective nonlinear source term directly from the Hamiltonian /
  resolvent / path-sum structure
- show that the strong-field fixed-point equation is not just a motivated ansatz

This is the highest-leverage step.

### Attack 2: derive `g_tt` and `g_ij` from the same object

Current gap:

- spatial and temporal sectors are still split
- no full spacetime horizon statement is possible without both

Required outcome:

- derive the temporal redshift factor from the exact same strong-field closure
  that gives the spatial metric
- remove the current mismatch where the spatial branch looks stronger than the
  temporal branch

### Attack 3: only after metric closure, revisit horizon / echo claims

Current gap:

- no-horizon is still conditional on the strong-field metric
- no-echo is separately weaker still

Required outcome:

- once the metric is fixed, re-evaluate horizon formation
- treat echo phenomenology as a downstream consequence, not the place where the
  gravity theorem is decided

## What not to overclaim

Even if the next step lands, keep these distinctions explicit:

- broad weak-field GR signatures are not the same as full nonlinear GR
- a bounded hard floor / no-singularity statement is not the same as no horizon
- no-horizon is not the same as no-echo

## Research success criteria

This lane is worth promoting only if all of the following hold:

1. the nonlinear closure is derived from the exact lattice framework, not
   inserted as a closure ansatz
2. `g_tt` and `g_ij` come from the same strong-field derivation
3. the resulting metric satisfies a real nonlinear field equation or Regge
   analog with controlled residuals
4. downstream no-horizon / strong-field claims are reclassified against that
   derived metric, not inherited from older notes

## Practical conclusion

The gravity upside is still real, but the branch should stop acting as if the
main task is “derive more GR signatures.” The actual task is:

> derive one nonlinear spacetime closure that replaces the current strong-field
> ansatzes with a genuine lattice theorem.
