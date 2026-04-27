# DM Neutrino Bosonic Normalization Theorem

**Date:** 2026-04-15
**Status:** EXACT normalization selector on the proposed_retained local Higgs family
**Script:** `scripts/frontier_dm_neutrino_bosonic_normalization_theorem.py`

---

## Question

Can the remaining `1` versus `1/sqrt(2)` ambiguity in the direct neutrino
bridge normalization be resolved by importing the retained mainline
observable-principle toolkit?

---

## Answer

Yes, on the retained local Higgs family.

The exact direct bridge audit was correct as an audit:

- full `C^16` Frobenius normalization gives `y_nu^(0) / g_weak = 1/sqrt(2)`
- active chiral-subspace normalization gives `1`

What that audit did **not** yet decide was which normalization is physically
admissible for a local bosonic observable.

The mainline observable principle now fixes that.

Physical local scalar observables must be source-response coefficients of the
unique additive CPT-even generator

`W[J] = log|det(D+J)| - log|det D|`.

On the direct neutrino bridge, that changes the story sharply.

---

## Exact Theorem

Let

- `Y = P_R Gamma_1 P_L` be the exact direct local chiral bridge
- `Gamma_1` be the weak-axis post-EWSB scalar operator from the retained Higgs
  family `M(phi) = sum_i phi_i Gamma_i`

Then:

1. `Y` is nilpotent:

   `Y^2 = 0`

2. On a scalar local baseline `m I`, the raw bridge has identically zero
   additive bosonic response:

   `det(m I + j Y) = m^16`

   so

   `W[jY] = 0`

   for all real `j`.

3. The retained scalar Hermitian completion of the bridge is exactly

   `Y + Y^dagger = Gamma_1`.

4. That completion has nontrivial even bosonic response:

   `det(m I + j Gamma_1) = (m^2 - j^2)^8`

   so

   `W[j Gamma_1] = 8 log|1 - j^2/m^2|`.

Therefore the physical normalization surface is **not** the active chiral
bridge by itself. It is the full bosonic `Gamma_1` family.

---

## Why This Selects `1/sqrt(2)`

Once the physical source family is assigned on `Gamma_1`, the branch's
canonical trace normalization becomes unambiguous:

- `Tr(Gamma_1^dag Gamma_1) / 16 = 1`
- `Tr(Y^dag Y) / 16 = 1/2`

so the canonically normalized bridge ratio is exactly

`sqrt( Tr(Y^dag Y) / Tr(Gamma_1^dag Gamma_1) ) = 1/sqrt(2)`.

The active-space ratio `1` remains a mathematically exact comparator, but it is
no longer the physical bosonic normalization because the raw chiral bridge
itself carries no scalar source-response.

So the branch can now promote the previously bounded full-space benchmark to
the retained normalization statement:

> within the retained local Higgs family and the axiom-native observable
> principle, the physical base normalization is
> `y_nu^(0) / g_weak = 1/sqrt(2)`.

Equivalently, the branch's correct base benchmark is

`y_nu^(0) = g_weak / sqrt(2)`,

not the active-space comparator `g_weak`.

---

## What This Does And Does Not Close

This closes one real blocker:

- the base-normalization ambiguity of the direct `Gamma_1` bridge

This note by itself does **not** close the whole denominator. But the next
local step is now closed by the downstream companion

- `docs/DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md`
- `scripts/frontier_dm_neutrino_schur_suppression_theorem.py`

That theorem fixes the exact retained local second-order coefficient

`y_nu^eff = g_weak^2 / 64`

and upgrades the old bounded `k_B = 8` attraction to an exact local Dirac-lane
statement.

So the live denominator problem is no longer

> choose `1` versus `1/sqrt(2)`

and it is no longer

> derive the local second-order `Gamma_1` suppression coefficient.

It is now downstream:

> derive or rule out the Majorana / `Z_3` activation law that turns on the
> unique charge-`2` source and feeds the three-generation `A/B/epsilon`
> structure without fitted leftovers.

---

## Consequence For The `k_B = 8` Candidate

The denominator boundary is now sharper than this note alone.

This note fixes the physical base surface:

`y_nu^(0) = g_weak / sqrt(2)`.

The downstream Schur theorem then fixes the retained local suppression:

`y_nu^eff = g_weak^2 / 64`,

which implies `k_eff ~= 8.01` on the present seesaw calibration.

So the honest remaining question is no longer whether the direct Dirac lane can
reach `k_B = 8`. On the retained local lane, it does. The remaining question is
whether the Majorana side is axiom-forced strongly enough to turn that local
Dirac result into a full zero-import `eta`.
