# Gauge-Vacuum Plaquette Spectral-Measure Theorem

**Date:** 2026-04-16
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** (1) staggered-Dirac realization derivation target (canonical parent: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)); (2) g_bare = 1 derivation target (canonical parent: `G_BARE_DERIVATION_NOTE.md` — bookkeeping pointer, see-also cross-reference; not a load-bearing dependency of this spectral-measure theorem's local algebra).
**Status:** support - exact generating-object theorem on the finite Wilson source surface; explicit spectral-measure identification at `beta = 6` still open
**Script:** `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py`

## Question

After proving that the connected plaquette hierarchy is exact and cannot
truncate at finite order, do we at least have an exact equivalent generating
object for that hierarchy?

## Answer

Yes.

On every finite periodic Wilson `L^4` source surface, the entire connected
plaquette hierarchy is exactly equivalent to one compact positive spectral
measure on `[-1,1]`.

If

`A_L(U) = (1 / N_plaq) sum_p X_p(U)`,

with

`X_p(U) = (1/3) Re Tr U_p`,

then the Haar pushforward

`mu_L = (A_L)_* dnu_Haar`

is a probability measure on `[-1,1]`, and the finite Wilson partition function
is exactly its Laplace transform:

`Z_L(beta) = Z_L(0) integral_[-1,1] exp(beta N_plaq a) dmu_L(a)`.

Therefore:

- `P_L(beta)` is exactly the tilted first moment of `mu_L`,
- `chi_L(beta)` is exactly `N_plaq` times the tilted variance of `mu_L`,
- the full connected plaquette hierarchy is exactly the tilted cumulant
  hierarchy of `mu_L`,
- and by compact Hausdorff moment uniqueness, this measure is the unique exact
  generating object equivalent to the finite Wilson connected hierarchy.

So the abstract “equivalent generating object” gap is closed.

What remains open is narrower:

> explicitly identify that spectral measure, or equivalently its Laplace
> transform, on the accepted `3 spatial + 1 derived-time` Wilson surface at
> the framework point `beta = 6`.

## Setup

On a finite periodic Wilson `L^4` surface, the configuration space is

`Omega_L = SU(3)^(N_link)`,

which is compact. The normalized plaquette average

`A_L(U) = (1 / N_plaq) sum_p X_p(U)`

is continuous and satisfies `A_L(U) in [-1,1]` because each

`X_p(U) = (1/3) Re Tr U_p`

lies in `[-1,1]`.

Hence the pushforward of normalized Haar measure by `A_L` defines a unique
probability measure

`mu_L`

on `[-1,1]`.

## Theorem 1: exact Laplace-transform representation

By definition of the Wilson partition function,

`Z_L(beta) = integral_(Omega_L) exp[beta sum_p X_p(U)] dnu_Haar(U)`.

Since `sum_p X_p(U) = N_plaq A_L(U)`, pushing forward by `A_L` gives

`Z_L(beta) = Z_L(0) integral_[-1,1] exp(beta N_plaq a) dmu_L(a)`.

So the full finite-surface Wilson partition function is exactly the Laplace
transform of one compact positive measure.

## Corollary 1: exact moment / cumulant formulas

Define the tilted measure

`dmu_(L,beta)(a) = exp(beta N_plaq a) dmu_L(a) / integral exp(beta N_plaq a) dmu_L(a)`.

Then

`P_L(beta) = (1 / N_plaq) d/d beta log Z_L(beta)
           = integral a dmu_(L,beta)(a)`.

Differentiating once more gives

`chi_L(beta) = dP_L/d beta
             = N_plaq Var_(mu_(L,beta))(a)`.

More generally,

`(1 / N_plaq) d^n / d beta^n log Z_L(beta)
 = N_plaq^(n-1) kappa_n(mu_(L,beta))`,

where `kappa_n` is the `n`-th tilted cumulant of `a`.

So the shell-summed connected plaquette hierarchy is exactly the cumulant
hierarchy of one compact positive measure.

## Theorem 2: uniqueness of the equivalent generating object

Because `mu_L` is supported on the compact interval `[-1,1]`, the Hausdorff
moment problem is determinate: a compactly supported positive measure on
`[-1,1]` is uniquely determined by its moments.

But the Taylor coefficients of

`Z_L(beta) / Z_L(0) = integral exp(beta N_plaq a) dmu_L(a)`

at `beta = 0` are exactly the moments of `mu_L`.

Therefore:

> the finite Wilson connected plaquette hierarchy has a unique exact
> equivalent generating object, namely the compact plaquette spectral measure
> `mu_L`.

## Corollary 2: exact reduction-law reformulation

The previously closed reduction law

`P_L(beta) = P_1plaq(beta_eff,L(beta))`

can now be written as an equality of two spectral-moment functions:

`integral a dmu_(L,beta)(a)
 = integral x dmu_(1,beta_eff,L(beta))(x)`.

So the remaining nonperturbative plaquette problem is no longer “find some
bridge factor.” It is:

- explicitly identify `mu_L`, or
- explicitly identify its Laplace transform / tilted first moment
  on the accepted Wilson surface.

## What this closes

- exact compact positive spectral measure generating the full finite Wilson
  plaquette hierarchy
- exact Laplace-transform representation of the finite Wilson partition
  function
- exact moment/cumulant representation of `P_L`, `chi_L`, and the higher
  connected hierarchy
- exact uniqueness of the equivalent generating object

## What this does not close

- an explicit formula for the spectral measure `mu_L`
- an explicit formula for the full Laplace transform at `beta = 6`
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Support consequence for the live package

The live package can now say:

- the exact connected plaquette hierarchy is closed,
- no finite truncation can close it,
- and an exact equivalent generating object is also closed:
  the compact plaquette spectral measure.

That means the remaining analytic issue is no longer existence or structural
equivalence. It is explicit nonperturbative identification of that generating
object at the framework point.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=2 FAIL=0`


## Hypothesis set used (axiom-reset 2026-05-03)

Per [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md), this note depends on **both** open gates:

1. **Staggered-Dirac realization derivation target** — canonical parent note: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md) (`claim_type: open_gate`); in-flight supporting work: `PHYSICAL_LATTICE_NECESSITY_NOTE.md`, `THREE_GENERATION_STRUCTURE_NOTE.md`, `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, `scripts/frontier_generation_rooting_undefined.py`, `GENERATION_AXIOM_BOUNDARY_NOTE.md`.
2. **`g_bare = 1` derivation target** — canonical parent: `G_BARE_DERIVATION_NOTE.md` (`claim_type: positive_theorem`, `audit_status: audited_conditional`); bookkeeping pointer / see-also cross-reference, not a load-bearing dependency of this spectral-measure theorem's local algebra. In-flight supporting work: `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`, `G_BARE_RIGIDITY_THEOREM_NOTE.md`, `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`, `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`, `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`, `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`, `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`.

The note produces (or directly supports) a quantitative gauge prediction (Wilson plaquette content, `α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`, `g_2`, `β = 6`, CKM/quark/hadron mass hierarchy, action-unit metrology, etc.) by fixing `g_bare = 1` without independently deriving it — therefore both gates must close for the lane to upgrade.

Therefore `claim_type: bounded_theorem` until both gates close. When both gates close, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
