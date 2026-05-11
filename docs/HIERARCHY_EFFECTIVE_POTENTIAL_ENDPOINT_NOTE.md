# Hierarchy Effective-Potential Endpoint Note

**Status:** scope-narrowed bounded note — algebraic class-A closure of the
small-m expansion and endpoint sums conditional on the imported Matsubara
free-energy density formula. Prior independent audit feedback on the
pre-refresh row (2026-05-05) recorded a conditional verdict on two named
missing bridge theorems (the Matsubara free-energy formula itself + the
dimension-4 normalization insertion into the electroweak scale map).
**Date:** 2026-04-13 (originally); 2026-05-10 (audit-narrowing refresh:
explicit class-A conditional framing under named imported authority).
**Claim type (in-note framing):** bounded_theorem — class-A algebraic
extraction of `A_2`, `A_4`, `A_inf`, and `C_inf^(4D)` from the imported
Matsubara free-energy density formula. The pre-refresh audit-ledger row
recorded `claim_type: bounded_theorem` with a conditional verdict; this
source refresh records that boundary without proposing any audit-side
verdict or `claim_type` revision.
**Status authority:** independent audit lane only.
**Authority role:** records that the small-m endpoint algebra closes as a
class-A consequence of the imported Matsubara free-energy density formula.
**Does not** propose retained, positive-theorem, or hierarchy-closure
promotion. The hierarchy theorem itself remains open.
**Script:** `scripts/frontier_hierarchy_effective_potential_endpoint.py`
(SCORECARD 7/0 on current main; the prior `NameError: CANONICAL_ALPHA_BARE`
in PART 4 was repaired by importing from `canonical_plaquette_surface`)

## Audit boundary (2026-05-10 refresh of prior 2026-05-05 feedback)

The 2026-05-05 independent audit on the previous note revision recorded a
conditional verdict (load-bearing-step class A, criticality `critical`,
transitive descendants 265).
The audit's `chain_closure_explanation`:

> *The algebra from the stated free-energy formula to A_2, A_4, A_inf,
> and C_inf^(4D) closes. The restricted packet does not derive the exact
> Matsubara free-energy density formula itself from the axiom, so the
> full claimed endpoint theorem is conditional on that imported starting
> formula.*

The audit's `verdict_rationale`:

> *The runner genuinely checks the small-m expansion and endpoint sums
> from the encoded Matsubara formula, but it does not derive that
> formula from first principles; it takes the temporal modes and
> free-energy density ansatz as inputs. Part 4 also imports canonical
> plaquette/alpha constants and compares to the observed electroweak
> prefactor, which is comparator evidence rather than closure of the
> physical insertion map. The note itself explicitly states that the
> physical selection/insertion of the dimension-4 normalization remains
> open.*

The audit's `notes_for_re_audit_if_any`:

> *missing_bridge_theorem: provide a retained derivation of the exact
> Matsubara free-energy density formula from the stated axiom and a
> separate bridge theorem for inserting the dimension-4 temporal
> normalization into the electroweak scale map.*

This note adopts the explicit class-A conditional framing. The two named
missing bridge theorems are listed in §"Imported authorities and missing
bridges" below; each is a real upstream gap, not an import-redirect. The
load-bearing step is `(imported Matsubara free-energy density formula) ⇒
(A_2, A_4, A_inf, C_inf^(4D)) algebraic identities`, evaluated mechanically
by the runner.

**Imported authorities (cited, not re-derived in this note):**

1. The exact Matsubara free-energy density formula
   `Delta f(L_t, m) = (1 / (2 L_t)) sum_omega ln(1 + m^2 / [u_0^2 (3 + sin^2 omega)])`
   — taken as input. The runner encodes this expression directly.
2. Canonical `u_0` from
   [`scripts/canonical_plaquette_surface.py`](../scripts/canonical_plaquette_surface.py)
   — used in PART 4 only for comparator scoring against the observed
   electroweak prefactor `C_obs`.
3. Observed hierarchy prefactor `C_obs = v_obs / v_pred ~= 0.966921519`
   — comparator evidence (PDG-style external input), used for the
   "endpoint band" scoring claim only, not for any in-scope algebraic
   identity.

**Named missing bridge theorems (audit-recorded; both required for full
hierarchy closure):**

- **Bridge 1 — Matsubara free-energy derivation.** Derive the exact
  Matsubara free-energy density formula from the framework axiom set, so
  the small-m expansion below is no longer conditional on an imported
  starting expression.
- **Bridge 2 — Dimension-4 insertion theorem.** Derive the bridge that
  inserts the exact dimension-4 temporal normalization
  `C_inf^(4D) = (3/4)^(1/8)` (or a derived function of the exact
  endpoint pair `(A_2, A_inf)`) into the physical electroweak scale map
  `det -> v`, including the sign and placement of the correction.

Until at least Bridge 1 is supplied, the small-m endpoint algebra below
remains a class-A extraction conditional on the imported formula.
Until at least Bridge 2 is supplied, the comparator-scored "endpoint
band" claim in §"Why this matters" is comparator evidence, not closure
of the physical insertion map.

## Question (scope-narrowed)

Given the imported Matsubara free-energy density formula on the minimal
`L_s = 2` APBC block, do the small-m coefficient and the
`L_t = 2` / `L_t -> infinity` endpoint sums close mechanically as
class-A algebraic identities?

## Exact result

Yes.

Starting from the exact free-energy density formula:

`Delta f(L_t, m) = (1 / (2 L_t)) sum_omega ln(1 + m^2 / [u_0^2 (3 + sin^2 omega)])`

the small-m expansion is:

`Delta f(L_t, m) = A(L_t) m^2 + O(m^4)`

with exact coefficient:

`A(L_t) = (1 / (2 L_t u_0^2)) sum_omega 1 / (3 + sin^2 omega)`

This coefficient is the cleanest intensive candidate for the temporal
normalization surface, because it is directly extracted from the exact
dimension-4 effective-potential density.

## Exact endpoint formulas

The APBC endpoints are now explicit:

- `A_2 = 1 / (8 u_0^2)`
- `A_4 = 1 / (7 u_0^2)`
- `A_inf = 1 / (4 sqrt(3) u_0^2)`

So the exact full temporal-averaging correction between the minimal UV block
and the `L_t -> infinity` temporal average is:

`A_inf / A_2 = 2 / sqrt(3) ~= 1.154700538`

This is the exact analytic version of the earlier numerical `1.15469...`
ratio.

## Why this matters

If the physical normalization sits on a **dimension-4** effective-potential
density, the corresponding scale correction is the fourth root:

`C_inf^(4D) = (A_2 / A_inf)^(1/4) = (sqrt(3) / 2)^(1/4) = (3/4)^(1/8)`

Numerically:

- `C_inf^(4D) ~= 0.964678630`
- observed hierarchy prefactor
  `C_obs = 246.22 / 254.643210673818 ~= 0.966921519`

So the observed prefactor lies **inside the exact 3+1 endpoint band**
between:

- no temporal normalization correction: `1`
- full `L_t -> infinity` dimension-4 correction: `0.964678630`

That is much sharper than the old "maybe a prefactor" language.

## What is closed inside the audited scope (class-A conditional algebra)

Conditional on the imported Matsubara free-energy density formula
(§"Imported authorities and missing bridges" above), the following are
exact algebraic identities, verified by the runner:

1. the small-m effective-potential coefficient `A(L_t)` is exact
2. the `L_t = 2` endpoint coefficient `A_2 = 1/(8 u_0^2)` is exact
3. the `L_t -> infinity` coefficient `A_inf = 1/(4 sqrt(3) u_0^2)` is exact
4. the full temporal normalization ratio `A_inf / A_2 = 2/sqrt(3)` is exact

These four identities are class-A consequences of the imported starting
formula; none of them re-derives the starting formula itself.

## What remains open (named missing bridge theorems)

This still does **not** close the full hierarchy theorem. The two named
missing bridges from the audit are restated below.

The remaining Part 3 question is now:

> where, between the exact `L_t = 2` UV endpoint and the exact temporal
> average, does the physical EWSB normalization live?

Equivalently:

1. why the physical order parameter should pick the `L_t = 2` endpoint,
   or a derived function of this exact endpoint pair
2. how that exact intensive normalization enters the `det -> v` map
3. whether the remaining `~0.22%` difference is then just the plaquette / `u_0`
   input uncertainty

This question is the audit's **Bridge 2** (dimension-4 insertion theorem).
The Matsubara free-energy density formula itself remains the audit's
**Bridge 1**.

## Honest conclusion

The hierarchy route is still **not fully closed**. The prior audit feedback
recorded this row as conditional on two named bridge theorems; after this
source edit, the independent audit lane owns any current verdict.

But the open surface is now very tight:

- the exponent `16` is structural
- the temporal algebra is exact (class-A, conditional on Bridge 1)
- the relevant intensive endpoint normalization is exact (class-A,
  conditional on Bridge 1)

So the two remaining theorems are:

- **Bridge 1.** A retained derivation of the Matsubara free-energy
  density formula from the framework axiom set.
- **Bridge 2.** The physical selection / insertion of the exact
  dimension-4 temporal normalization into the electroweak scale map,
  including sign and placement.

This note does **not**:

- modify the parent audit-ledger row;
- promote any current or prior audit verdict;
- derive the Matsubara free-energy density formula from the axiom;
- supply a retained insertion theorem from `det -> v`;
- extend the audited scope beyond the class-A endpoint algebra.
