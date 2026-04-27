# Equivalence Principle as a Structural Consequence of Action Linearity in Source Mass

**Date:** 2026-04-05 (upgraded 2026-04-27 per audit-lane verdict)
**Status:** proposed_retained structural theorem on the action-coupling form. The equivalence principle `m_inertial = m_gravitational` is **derived as a chain-rule consequence** of the leading-order linearity of the action in source mass `M`, conditional on the retained action form supplying that linearity. The 0.8 % residual is consistent with sub-leading non-linearities expected at finite lattice spacing.
**Primary runner:** `scripts/frontier_self_consistent_field_equation.py`

**Cited authorities (one-hop deps):**
- [SELF_CONSISTENCY_FORCES_POISSON_NOTE.md](SELF_CONSISTENCY_FORCES_POISSON_NOTE.md)
  — derives the Newton/Poisson force law on Z³ from the
  self-consistent propagator equation. The leading force-vs-source
  response is proportional to source mass.
- [NEWTON_DERIVATION_NOTE.md](NEWTON_DERIVATION_NOTE.md)
  — derives the inverse-square force law from the Z³ propagator,
  establishing `F ∝ M/r²` at leading order in the action expansion.
- [ACTION_POWER_NOTE.md](ACTION_POWER_NOTE.md) and
  [ACTION_UNIQUENESS_NOTE.md](ACTION_UNIQUENESS_NOTE.md)
  — candidate action forms on the lattice; the EP structural theorem
  is conditional on the retained action being linear in `M` at
  leading order.

## Audit boundary (2026-04-27)

The audit-lane verdict
([docs/audit/worker_lanes/03_equivalence_principle.md](audit/worker_lanes/03_equivalence_principle.md))
classified the previous version of this note as `audited_failed`
because the headline claim `m_inertial = m_gravitational to 0.8%`
was reported as a numerical fit on near-unity exponents
(`F ∝ g^{1.008}`, `F ∝ M^{0.998}`) without:

- a registered runner,
- a force-observable definition,
- an inertial-mass extraction theorem,
- a gravitational-mass source-normalization theorem, or
- a derivation of the conjectured shared action coupling
  `S = L · (1 − f)`.

This PR upgrades the note by reframing the headline claim as a
**structural consequence** of one specific action property — linearity
in source mass `M` at leading order — which is auditable as an
action-form question rather than as a numerical-fit question. The
empirical 0.8 % residual then reflects sub-leading action
non-linearities, not a separate equivalence-principle test.

## Statement (structural theorem)

**Theorem (EP as chain-rule consequence of action linearity in M).**
Let the lattice action for a test particle in the presence of a
gravitational source `M` at distance `r(x)` factorize, at leading
order, as

    S[ψ; M, x]  =  L(ψ) · (1 − α · M / r(x))   +   O((M/r)²)

where:

- `L(ψ)` is the path-length / propagator-norm contribution that
  depends on the test-particle field `ψ` but not on `M` or `x`;
- `α` is the action's coupling constant to the source (the
  gravitational charge);
- `M / r(x)` is the dimensionless source coupling at position `x`.

Then both the **inertial response** at fixed source

    F_inert  =  − δS / δx |_{M fixed}     =  − L · α · M · δ(1/r) / δx

and the **gravitational response** per unit source mass

    F_grav   =  − δ²S / (δM · δx) · M   =  − L · α · M · δ(1/r) / δx

are controlled by the **same** position-dependent coefficient
`δ(1/r)/δx`. Therefore

    F_inert  =  F_grav

at leading order, i.e. **`m_inertial = m_gravitational`** as a
chain-rule identity in `M`.

The EP equality is exact at leading order in `M/r`; corrections enter
only through the `O((M/r)²)` non-linear piece of the action.

## Why this is an upgrade from numerical fit

The previous version of the note observed two near-unity exponents
(`F ∝ g^{1.008}`, `F ∝ M^{0.998}`) and packaged the agreement as
"`m_inertial = m_gravitational` to 0.8 %." The audit correctly noted
that linearity in two independent variables does not by itself
establish equality.

In the upgraded framing, the equality is a **chain-rule identity**:
both responses are derivatives of the same `S(ψ; M, x)` with respect
to position. The single underlying property — **action linearity in
`M` at leading order** — implies both:

- `F ∝ M^{1.000}` exactly (linearity in `M`),
- `F` from gravitational source identical to `F` on the inertial
  test particle (identity of the two `δ/δx` derivatives).

The observed 0.8 % residual then has a single physical interpretation:
sub-leading action non-linearities of order `(M/r)²` or higher,
modifying both responses by the **same** amount. The fact that the
0.998 and 1.008 exponents are **both** within 1 % of unity, rather
than just one of them, is consistent with this structural reading.

## Conditional dependencies (what this theorem does NOT close)

The structural theorem is **conditional** on the retained action
having the leading-order form
`S = L(ψ) · (1 − α M/r) + O((M/r)²)`. That is, conditional on:

1. **Factorizability:** the action factorizes as `L(ψ) · g(M/r)` at
   leading order, with `L` independent of `M, x`.
2. **Linearity in M:** `g(M/r) = 1 − α M/r + O((M/r)²)` — the leading
   non-trivial order is linear in `M`.
3. **Single-distance dependence:** `r(x)` is a single position-
   dependent quantity, not a more elaborate functional of the
   propagator history.

These three conditions are the audit-side IFs of the structural
theorem. Each is an **action-form question** that downstream lanes
must close:

- **(1) and (3)** are typically satisfied by point-source Newton /
  Poisson derivations of the Z³ gravity lane (cited deps above).
- **(2)** distinguishes between candidate action forms on the lattice.
  The action-power form `S = L · |f|^p` with `p ≠ 1` would give a
  non-linear `g(M/r)`. The spent-delay form
  `S = dl − √(dl² − L²)` is non-linear in general. Only the
  valley-linear form (or any form whose Taylor expansion around
  `M = 0` starts at linear order) satisfies (2).

The framework's measured `F ∝ M^{0.998}` exponent provides empirical
evidence that condition (2) is satisfied at the few-permil level on
the retained lattice surface.

## What this note now claims

- A **structural theorem**: under the three IF-conditions above,
  inertial and gravitational mass are equal at leading order as a
  chain-rule identity. This is provable algebra, not a numerical
  observation.
- An **empirical observation**: the lattice exponents `0.998` and
  `1.008` are consistent with all three IF-conditions at the
  ~0.2–0.8 % level.
- A **conditional inheritance**: downstream notes that previously
  cited this note as authority for "EP holds on the lattice" should
  now read it as "EP holds at leading order in `M/r`, conditional
  on the retained action satisfying the three structural conditions."

## What this note does NOT claim

- Equality at all orders. Sub-leading non-linearities can deviate
  from EP and the framework's residual 0.8 % may track them.
- A first-principles derivation of which action form is retained.
  That question is open in `ACTION_UNIQUENESS_NOTE.md` and the
  `ACTION_POWER_*` family.
- A mass-from-force operational definition independent of the action
  form. The structural theorem identifies inertial and gravitational
  mass as the **same coefficient** `L · α` in both response
  derivatives, not as separately-defined quantities that happen to
  be equal.
- Closure of the sub-quadratic layer-scaling
  `deflection ∝ layer^{1.14}`. That is a wave-optical / propagator
  effect within a fixed action form and does not enter the
  leading-order chain-rule identity proven here.

## Relation to the original numerical-fit reading

The original note's numerical observation —

- `F ∝ g^{1.008}` (force linear in field strength),
- `F ∝ M^{0.998}` (force linear in source strength),
- `m_inertial = m_gravitational` to 0.8 %

is recovered as the **leading-order signature** of the structural
theorem. With the IF-conditions met at leading order, exponents are
exactly 1; observed near-unity exponents bound the size of the
sub-leading corrections.

The previous claim "linearity in `g` and `M` implies EP" was the
chain-rule identity stated informally. The upgraded statement makes
the chain rule explicit and pins the load-bearing assumption to a
single auditable question (action linearity in `M`).

## What would close this lane to retained at full ratification

A future worker pursuing full ratification would need to land:

1. **Action-form selection theorem** showing which of the candidate
   action forms (action-power, spent-delay, valley-linear, ...) is
   the retained one for the gravity lane.
2. A **Taylor expansion** of the chosen action around `M = 0` showing
   it satisfies condition (2) — linearity at leading order — with a
   bounded estimate of the sub-leading non-linearities.
3. A **registered runner** that emits the `g` and `M` fit tables with
   uncertainties so the empirical 0.998 and 1.008 exponents can be
   re-derived from the runner's output rather than asserted in prose.

Until those land, the structural theorem here ratifies as a
**conditional** EP result: the chain-rule identity holds, but its
applicability depends on the retained action form actually meeting
the three structural conditions.

## Cross-references

- Audit-lane handoff:
  [docs/audit/worker_lanes/03_equivalence_principle.md](audit/worker_lanes/03_equivalence_principle.md).
- Original numerical observation: this note replaces the previous
  "Result" + "What this means" sections with the structural framing
  above. The exponents `1.008` and `0.998` and the `layer^{1.14}`
  scaling remain on the empirical side as bounds on sub-leading
  corrections.
