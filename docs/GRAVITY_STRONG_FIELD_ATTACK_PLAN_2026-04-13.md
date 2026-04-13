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

New exact foothold now extracted on this branch:

- for a rank-one additive attractive local potential,
  the strong-field enhancement factor used in the point-source note is an
  exact resolvent identity
- see `docs/STRONG_FIELD_RESOLVENT_CLOSURE_NOTE.md`
- this removes one heuristic from the current point-source closure, but it does
  **not** yet produce the full strong-field spacetime metric

New exact foothold extracted after that:

- the same resolvent program now extends beyond the rank-one source to a
  finite-support diagonal attractive source class
- the exact field can be written as `phi = G_0 P (I - V G_S)^-1 m`
- see `docs/DISTRIBUTED_SOURCE_SPACETIME_CLOSURE_NOTE.md`
- this removes the "point source only" limitation from the exact source-model
  foothold, but still does **not** derive the physical matter source class

New bounded bridge now extracted on this branch:

- for the standard static isotropic vacuum system, the spatial conformal factor
  `psi` and the combination `alpha psi` are both harmonic outside the source
- this fixes the isotropic Schwarzschild lapse once the spatial harmonic data
  are given
- see `docs/STATIC_ISOTROPIC_VACUUM_BRIDGE_NOTE.md`
- this is **not** a framework derivation of full GR; it sharpens the temporal
  sector target by showing what a common static vacuum closure would force

New bounded bridge sharpened after that:

- the finite-support source theorem now provides one common exterior harmonic
  field that can drive both `psi` and `alpha` through
  `psi = 1 + phi`, `alpha psi = 1 - phi`
- see `docs/DISTRIBUTED_SOURCE_SPACETIME_CLOSURE_NOTE.md`
- this is still **bounded**, because the static isotropic vacuum bridge itself
  has not yet been derived from the lattice closure rather than imported as
  the correct exterior target

New exact/bounded split extracted after that:

- the exact source-model foothold now extends further to a finite-rank
  positive-semidefinite support operator, not just a diagonal support source
- see `docs/FINITE_RANK_GRAVITY_RESIDUAL_NOTE.md`
- the direct common-source 4D metric candidate built from that exact field has
  a nonzero vacuum Einstein residual outside the source
- the monopole-projected isotropic candidate built from the same exact field
  reduces that residual by roughly `6.5e2`
- this pinpoints the remaining gap:
  the theorem-grade reduction from the exact finite-rank harmonic exterior
  field to the isotropic-vacuum surface

New exact/bounded asymptotic reduction extracted after that:

- for the exact cubic-symmetric finite-rank source class, the renormalized
  support source and the exact exterior field are both `O_h`-invariant
- the first non-monopole exterior correction is the unique cubic `l=4` mode
- the relative exterior anisotropy decays with a bounded slope consistent with
  quartic suppression, and is already `~1.6e-3` by radius `r = 6`
- see `docs/CUBIC_MONOPOLE_REDUCTION_NOTE.md`
- this means the asymptotic isotropic reduction is no longer ad hoc for that
  exact source class; the remaining gap is why the physical source lands in,
  or flows to, that cubic-symmetric sector strongly enough near the source

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
- `docs/STRONG_FIELD_RESOLVENT_CLOSURE_NOTE.md`
- `docs/LATTICE_NO_HORIZON_NOTE.md`
- `scripts/frontier_broad_gravity.py`
- `scripts/frontier_strong_field_metric.py`
- `scripts/frontier_strong_field_resolvent_closure.py`
- `scripts/frontier_strong_field_extension.py`
- `scripts/frontier_lattice_no_horizon.py`

Use them as inputs. Do **not** assume their strongest status labels are already
paper-safe.

## Concrete attack sequence

### Attack 1: replace the strong-field self-consistency ansatz with a derived nonlinear equation

Current gap:

- the point-source fixed-point equation is elegant, but the backreaction law is
  not yet derived from the exact lattice propagator

Current status update:

- the rank-one local-source version of that enhancement law is now exact
- the same exact closure now extends to a finite-support diagonal attractive
  source class
- the same exact closure now extends again to a finite-rank correlated support
  operator
- the remaining issue is upgrading that exact source class to the actual
  physical matter source / strong-field Hamiltonian

Required outcome:

- derive the effective nonlinear source term directly from the Hamiltonian /
  resolvent / path-sum structure
- show that the strong-field fixed-point equation is not just a motivated ansatz

This is the highest-leverage step.

### Attack 2: derive `g_tt` and `g_ij` from the same object

Current gap:

- spatial and temporal sectors are still split
- no full spacetime horizon statement is possible without both

Current bridge result:

- on the static isotropic vacuum surface, `g_tt` is not an arbitrary extra
  function once the harmonic spatial data are fixed
- so the real unresolved issue is no longer “guess a lapse,” but “derive why
  the lattice strong-field closure reduces to this common harmonic system”
- the finite-support source theorem now provides one exact exterior harmonic
  object that both sectors can share, but the reduction to the static isotropic
  vacuum bridge is still a bounded step
- the new finite-rank residual test sharpens that further:
  the direct common-source candidate is not yet vacuum-closed, while the
  monopole/isotropic projection of the same exact field is nearly vacuum
- the new cubic-monopole reduction result sharpens it again:
  for the exact `O_h`-symmetric source class, the isotropic reduction is
  asymptotically justified and the first anisotropic correction is controlled

Required outcome:

- derive the temporal redshift factor from the exact same strong-field closure
  that gives the spatial metric
- remove the current mismatch where the spatial branch looks stronger than the
  temporal branch
- derive why the physical source law reduces to the cubic-symmetric source
  class strongly enough in the exterior / near-source matching region

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
