# Gauge-Vacuum Plaquette Susceptibility-Flow Theorem

**Date:** 2026-04-16
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** (1) staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`); (2) g_bare = 1 derivation target (canonical parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md)).
**Status:** support - exact nonperturbative flow theorem for the implicit plaquette reduction law on finite Wilson evaluation surfaces; explicit closure at `beta = 6` still open
**Script:** `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py`

## Question

After closing the exact existence and uniqueness of the implicit reduction law

`P_L(beta) = P_1plaq(beta_eff,L(beta))`,

can we derive anything more explicit about the full nonperturbative reduction
without already solving the Wilson plaquette at the framework point?

## Answer

Yes.

The exact reduction law is governed by a nonperturbative susceptibility flow:

`beta_eff,L'(beta) = chi_L(beta) / chi_1plaq(beta_eff,L(beta))`

where

- `chi_L(beta) = dP_L/d beta = Var_beta(S_L) / N_plaq`,
- `chi_1plaq(beta) = dP_1plaq/d beta = Var_beta(X)`.

Equivalently,

`P_L(beta) = integral_0^beta chi_L(s) ds`

and therefore

`beta_eff,L(beta) = P_1plaq^(-1)(integral_0^beta chi_L(s) ds)`.

So the remaining open object is now even sharper:

> derive the full connected Wilson plaquette susceptibility profile
> `chi_L(beta)` on the accepted `3 spatial + 1 derived-time` surface.

That would close the explicit nonperturbative reduction law.

## Theorem 1: exact susceptibility identities

On a finite periodic Wilson `L^4` surface,

`P_L(beta) = (1/N_plaq) d/d beta log Z_L(beta)`

with

`Z_L(beta) = integral DU exp[beta S_L(U)]`

and

`S_L(U) = sum_p (1/3) Re Tr U_p`.

Differentiating once more gives

`chi_L(beta) = dP_L/d beta = Var_beta(S_L) / N_plaq`.

For the local one-plaquette block,

`P_1plaq(beta) = d/d beta log Z_1plaq(beta)`

with

`Z_1plaq(beta) = integral dU exp[beta X(U)]`

and

`X(U) = (1/3) Re Tr U`,

so

`chi_1plaq(beta) = dP_1plaq/d beta = Var_beta(X)`.

Because both observables are nonconstant and the densities are strictly
positive for finite `beta`, both susceptibilities are strictly positive on the
finite Wilson evaluation surface.

## Theorem 2: exact nonperturbative flow law for `beta_eff,L`

The previously closed exact implicit reduction law

`P_L(beta) = P_1plaq(beta_eff,L(beta))`

may now be differentiated exactly:

`chi_L(beta) = chi_1plaq(beta_eff,L(beta)) * beta_eff,L'(beta)`.

Therefore

`beta_eff,L'(beta) = chi_L(beta) / chi_1plaq(beta_eff,L(beta))`.

This is an exact nonperturbative transport equation for the reduction map on
every finite periodic Wilson evaluation surface.

## Corollary 1: exact integral representation

Since `P_L(0) = 0`,

`P_L(beta) = integral_0^beta chi_L(s) ds`.

Substituting into the exact inverse relation yields

`beta_eff,L(beta) = P_1plaq^(-1)(integral_0^beta chi_L(s) ds)`.

So the explicit nonperturbative reduction law is equivalent to the exact
connected plaquette susceptibility profile.

## Corollary 2: first nonlocal susceptibility coefficient

The mixed-cumulant onset theorem already proved

`P_L(beta) - P_1plaq(beta) = beta^5 / 472392 + O(beta^6)`.

Differentiating gives the exact first nonlocal susceptibility correction:

`chi_L(beta) - chi_1plaq(beta) = 5 beta^4 / 472392 + O(beta^5)`.

Equivalently, from

`beta_eff,L(beta) = beta + beta^5 / 26244 + O(beta^6)`,

one gets

`beta_eff,L'(beta) = 1 + 5 beta^4 / 26244 + O(beta^5)`.

Using the exact common slope

`chi_1plaq(0) = chi_L(0) = 1/18`,

the first transport correction is

`chi_1plaq(0) * (beta_eff,L'(beta) - 1) = 5 beta^4 / 472392 + O(beta^5)`,

matching the differentiated mixed-cumulant theorem exactly.

## What this closes

- exact nonperturbative flow equation for the implicit reduction law
- exact integral representation of the reduction law in terms of connected
  Wilson susceptibility
- exact first nonlocal susceptibility coefficient
- exact identification of the remaining object as the full susceptibility
  profile, not a generic missing bridge

## What this does not close

- an explicit closed form for `chi_L(beta)` on the finite Wilson surface
- an explicit closed form for `beta_eff,L(beta)`
- analytic closure of `P(6)`
- repo-wide repinning of the canonical plaquette

## Support consequence for the live package

The live package can now say more sharply:

- reduction-law existence/uniqueness is exact;
- reduction-law transport is exact;
- the first nonlocal susceptibility correction is exact;
- the remaining gap is the explicit full connected susceptibility profile at
  the framework point.

That is a real derivation step, not just a numerical observation.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py
```

Expected summary:

- `THEOREM PASS=5 SUPPORT=3 FAIL=0`


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on **both** open gates:

1. **Staggered-Dirac realization derivation target** — canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`); in-flight supporting work: `PHYSICAL_LATTICE_NECESSITY_NOTE.md`, `THREE_GENERATION_STRUCTURE_NOTE.md`, `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, `scripts/frontier_generation_rooting_undefined.py`, `GENERATION_AXIOM_BOUNDARY_NOTE.md`.
2. **`g_bare = 1` derivation target** — canonical parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md) (`claim_type: positive_theorem`, `audit_status: audited_conditional`); in-flight supporting work: `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`, `G_BARE_RIGIDITY_THEOREM_NOTE.md`, `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`, `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`, `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`, `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`, `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`.

The note produces (or directly supports) a quantitative gauge prediction (Wilson plaquette content, `α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`, `g_2`, `β = 6`, CKM/quark/hadron mass hierarchy, action-unit metrology, etc.) by fixing `g_bare = 1` without independently deriving it — therefore both gates must close for the lane to upgrade.

Therefore `claim_type: bounded_theorem` until both gates close. When both gates close, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
