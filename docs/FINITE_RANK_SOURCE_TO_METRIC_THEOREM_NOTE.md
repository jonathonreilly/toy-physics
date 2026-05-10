# Finite-Rank Source-to-Metric Theorem Path via Exact Boundary Action and Coarse-Grained Exterior Law

**Date:** 2026-04-14 (audit-prep cite-chain rigorize 2026-05-10)
**Script:** `scripts/frontier_finite_rank_source_to_metric_theorem.py`
**Status:** exact finite-rank source-to-exterior theorem plus bounded scalar metric reduction; not full nonlinear GR
**Claim type:** bounded_theorem
**Claim scope:** the note supports exact finite-rank source-to-exterior algebraic
closure (Woodbury/Dyson identity plus stationary Schur boundary action) and an
explicitly bounded scalar/isotropic coarse-grained metric residual improvement;
it explicitly disclaims full tensorial `3+1` GR closure.

## Audit-driven dependency-edge rigorization (2026-05-10)

The 2026-05-05 audit verdict on this row was `audited_conditional` (critical,
load-bearing 10.596) with rationale: "The exact Woodbury-style source-to-exterior
identity closes as an algebraic check, but the bounded source-to-metric claim
imports the coarse-grained exterior law, Schur boundary action, isotropic
metric residual construction, and thresholds through unprovided runner modules.
The missing step is a retained-grade derivation or fully provided verification
of that scalar-to-metric reduction from the restricted packet alone." The named
repair target was: "missing_dependency_edge: provide the imported runner modules
and retained authority notes for the finite-rank operator, Schur boundary action,
coarse-grained exterior law, and isotropic metric residual map, or inline an
independent derivation of the bounded scalar-to-metric reduction."

This rigorize pass makes the one-hop dependency status explicit so the audit
graph can route directly to the upstream authority surfaces and the imported
runner modules. It does not derive any of the imported objects within this
packet, does not promote any sibling claim, and does not change this row's
`audited_conditional` status. Audit verdict and effective status are set by
the independent audit lane only; nothing in this rigorization edit promotes
status.

**Cited authority (one-hop dep with retained-grade upstream surface):**

- [`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](./OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
  — `claim_type: bounded_theorem`, current ledger
  `effective_status: retained_bounded`. Canonical surface for the exact
  scalar Schur Dirichlet-to-Neumann boundary action `I_R(f; j) = (1/2) f^T
  Lambda_R f - j^T f` whose stationarity at the finite-rank shell trace is
  the load-bearing closure step in this note. Strongest leg of the input
  chain; supplies the `Lambda_R` operator, `trace_idx` boundary indexing,
  and stationarity verification used by the runner.

**Runner-imported frontier modules (script-level deps with no dedicated
retained source note):**

The companion runner `scripts/frontier_finite_rank_source_to_metric_theorem.py`
loads its finite-rank source operator, the coarse-grained exterior radial
harmonic projection, and the Schur boundary action via Python
`SourceFileLoader` directly from three frontier modules. These modules are
imported authorities for this bounded result; the restricted packet does
not currently provide retained-grade audited authority notes for the
finite-rank operator construction or the coarse-grained exterior law.

| Imported module | Role in this note |
|---|---|
| [`scripts/frontier_finite_rank_gravity_residual.py`](../scripts/frontier_finite_rank_gravity_residual.py) | constructs the exact finite-rank support operator `H_W = H_0 - P W P^T`, the Woodbury/Dyson identity that gives `q_eff = (I - W G_S)^-1 m`, and the exact exterior field `phi = G_0 P q_eff` (via `exact_finite_rank_field()`) |
| [`scripts/frontier_coarse_grained_exterior_law.py`](../scripts/frontier_coarse_grained_exterior_law.py) | builds the finite-rank `phi` grid (`build_finite_rank_phi_grid()`) and runs the shell-averaging plus radial harmonic `phi_eff(r) = a/r` projection that produces the bounded coarse-grained metric residual reported in the verdict (via `analyze_family(...)`) |
| [`scripts/frontier_oh_schur_boundary_action.py`](../scripts/frontier_oh_schur_boundary_action.py) | supplies the Schur Dirichlet-to-Neumann matrix `Lambda_R` and the stationary boundary-action evaluation used to verify that the exact finite-rank shell trace is a stationary point of `I_R` (via `schur_dtn_matrix(...)` and `analyze_family(...)`) |

**What the cite-chain does NOT close.** Only `OH_SCHUR_BOUNDARY_ACTION_NOTE.md`
has a retained-grade upstream surface; the other two imported frontier
modules do not have dedicated retained authority notes. The
"missing_dependency_edge" repair target is therefore not directly satisfied
by this rigorize pass; the chain remains conditional on those module-level
imports being correct (the same conditional perimeter the audit already
recorded). The runner's PASS=4/0 verifies the load-bearing exact-Woodbury
reconstruction (`6.939e-17`), exact Schur stationarity (`flux_err =
4.163e-16`, `stationary_grad = 4.163e-16`), and bounded coarse-grained
metric residual (`coarse = 7.028e-06` vs. `direct = 1.039e-02`,
improvement `~1.48e3`) on the currently imported finite-rank grid; this
is the bounded scope on which the row stands.

**What this rigorize pass NEVER claims.** It does not derive the
finite-rank operator, the coarse-grained radial harmonic projection, or
the Schur boundary action from the accepted axiom within this packet.
It does not close the tensorial `3+1` matching map. It does not promote
`finite_rank_source_to_metric_theorem_note` to retained or remove the
sharp blocker recorded in the verdict.

## Audit-aware repair path

Per `audit_ledger.json`, `notes_for_re_audit_if_any` for
`finite_rank_source_to_metric_theorem_note`: the cheapest path to a
stronger audit verdict is to attach retained-grade cited notes for the
two unsourced frontier modules listed above (the finite-rank operator
construction in `frontier_finite_rank_gravity_residual.py` and the
coarse-grained exterior law in `frontier_coarse_grained_exterior_law.py`),
or to inline those derivations directly in this runner so they are
derived from the accepted axiom rather than loaded. Either path makes
the bounded scalar-to-metric reduction self-contained from the axiom
alone; the current note is conditional on those imports.

## Purpose

This is the finite-rank source-to-metric route in the current gravity program:
attack the finite-rank source-to-metric architecture directly, using the exact
finite-rank source family plus the retained bridge/action laws, and avoid the
current `eta_floor_tf` endpoint route entirely.

The goal is to see how far the exact finite-rank source stack can go as a clean
end-to-end GR architecture:

1. exact finite-rank source renormalization
2. exact microscopic boundary action / Dirichlet principle
3. unique coarse-grained exterior harmonic law
4. induced static isotropic metric reduction

## Exact theorem: finite-rank source determines the exterior harmonic field

For the exact finite-rank support operator already on the branch,

- `H_W = H_0 - P W P^T`
- `G_0 = H_0^-1`
- `G_S = P^T G_0 P`

the exact Woodbury/Dyson identity gives

- `G_W P = G_0 P (I - W G_S)^-1`

so every bare support source vector `m` induces the exact renormalized source

- `q_eff = (I - W G_S)^-1 m`

and the exact exterior field

- `phi = G_0 P q_eff`.

That is the exact finite-rank source-to-exterior theorem already supported by
the current gravity stack.

## Exact theorem: the same microscopic boundary action is stationary

Using the exact Schur-complement boundary action on the current bridge
surface,

- `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`

the exact finite-rank shell trace is recovered as the unique stationary point
with microscopic flux `j = (H_0 phi_ext)|_(Gamma_R)`.

So the finite-rank source family does not merely give an exterior harmonic
field. It also lands on the same exact microscopic boundary-action surface as
the retained bridge law.

## Bounded theorem: the exterior field coarse-grains to a near-vacuum isotropic metric

Shell averaging the exact finite-rank exterior field and projecting it onto
the unique radial harmonic law `phi_eff(r) = a/r` gives a static isotropic
`3+1` metric candidate with strongly reduced vacuum residual.

On the exact finite-rank family, the best matching radius in the current scan
is `R_match = 5.0`:

- direct same-source metric residual: `1.039e-02`
- coarse-grained radial-harmonic residual: `7.028e-06`
- improvement factor: `~1.48e3`

So the finite-rank family does support a clean source-to-exterior-metric
architecture at the scalar/isotropic level.

## Sharp blocker: the tensorial `3+1` matching map is still missing

The direct common-source metric candidate built from the exact finite-rank
field still has a nonzero Einstein residual.

That means the exact finite-rank source family does **not** by itself supply a
theorem-grade tensorial map from microscopic source data to the full `3+1`
metric.

What is missing is the same thing the current gravity frontier has already
localized elsewhere:

> a tensorial matching/completion principle that promotes the exact scalar
> exterior law to the full lapse-shift-spatial metric.

So route 3 is cleaner than the current `eta_floor_tf` endpoint route because
it starts from exact finite-rank source renormalization and exact retained
boundary/action laws, but it still stops at the scalar/static exterior sector.

## Verdict

The finite-rank source family gives a stronger exact/bounded architecture than
the current tensor residual route:

- exact finite-rank source-to-exterior closure: yes
- exact microscopic boundary-action closure: yes
- bounded coarse-grained source-to-metric reduction: yes
- full tensorial `3+1` closure / full nonlinear GR: no

So this route is a real end-to-end source architecture, but it still needs a
new tensorial matching principle before it can become full GR.

## Boundaries

This note does not close:

- a tensorial `3+1` matching law: the direct same-source metric still
  carries a nonzero Einstein residual on the finite-rank family;
- full nonlinear GR;
- any retained-grade promotion of the imported frontier modules
  `frontier_finite_rank_gravity_residual.py` or
  `frontier_coarse_grained_exterior_law.py`;
- any chain closure beyond the explicit exact finite-rank source-to-exterior
  identity, the exact Schur stationarity, and the bounded coarse-grained
  metric residual reported by the runner.
