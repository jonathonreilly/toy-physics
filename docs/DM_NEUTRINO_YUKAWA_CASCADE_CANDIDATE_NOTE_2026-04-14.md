# DM Neutrino Yukawa Cascade Candidate

**Date:** 2026-04-14
**Branch:** `codex/dm-main-derived`
**Script:** `scripts/frontier_dm_neutrino_yukawa_candidate.py`

---

## Status

**HISTORICAL BOUNDED PRECURSOR**

This note remains useful as the pre-theorem intuition for why `k_B = 8` kept
reappearing. It is no longer the live authority note for the Dirac coefficient.
That role now belongs to:

- `docs/DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md`
- `scripts/frontier_dm_neutrino_schur_suppression_theorem.py`

At the time this note was written, it did **not** close the neutrino Yukawa
theorem gap. It tightened the denominator story in one important way:

- `k_B = 8` is not just a numerology accident
- there is now a concrete bounded mechanism that explains why `k_B = 8` is the
  standout staircase level
- the mechanism is a **second-order EWSB cascade**, not a bare guess

So the branch gained a better answer than "maybe `alpha_LM^2` looks pretty."
It had a candidate derivation pattern before the exact Schur theorem landed.

The new exact geometry companion is:

- [`scripts/frontier_dm_neutrino_cascade_geometry.py`](/Users/jonBridger/Toy%20Physics-dm/scripts/frontier_dm_neutrino_cascade_geometry.py)
- [`docs/DM_NEUTRINO_CASCADE_GEOMETRY_NOTE_2026-04-14.md`](/Users/jonBridger/Toy%20Physics-dm/docs/DM_NEUTRINO_CASCADE_GEOMETRY_NOTE_2026-04-14.md)

That artifact does not fix the physical neutrino Yukawa either, but it does
show that the second-order cascade surface is the first exact operator surface
where the weak-axis insertion closes in a `1 + 2` pattern.

There is now also an exact bridge companion:

- [`scripts/frontier_dm_neutrino_dirac_bridge_theorem.py`](/Users/jonBridger/Toy%20Physics-dm/scripts/frontier_dm_neutrino_dirac_bridge_theorem.py)
- [`docs/DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md`](/Users/jonBridger/Toy%20Physics-dm/docs/DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)

That theorem closes the direct local operator-selection step:
the post-EWSB chiral surface is `Gamma_1`, not `Xi_5`. It also proves that
the first exact closed action on `T_1` is second order.

That coefficient/base-coupling gap is now closed by the later Schur theorem.
So this note should be read as the bounded precursor that correctly guessed the
right scale and mechanism before the exact retained local derivation existed.

---

## Core Observation

From the existing seesaw / staircase surface:

- `y_nu(k_B=7) ~ 2.21e-2`
- `y_nu(k_B=8) ~ 6.66e-3`
- `alpha_LM^2 ~ 8.22e-3`

So the `k_B = 8` target is indeed the only simple integer-power candidate near
the observed denominator lane.

The new point is that the EWSB cascade already used elsewhere on branch gives:

- one-step factor
  `epsilon_weak * log(M_Pl / v) ~ 1.04e-1`
- two-step factor
  `(epsilon_weak * log(M_Pl / v))^2 ~ 1.08e-2`

Multiplying that **two-step** factor by a bounded `O(0.5-0.65)` sector base
Yukawa gives

- top-like base `y_0 ~ 0.439` -> `y_nu^cand ~ 4.73e-3`
- weak/full-space benchmark `y_0 ~ 0.462` -> `y_nu^cand ~ 4.98e-3`
- weak/active-space benchmark `y_0 ~ 0.653` -> `y_nu^cand ~ 7.04e-3`

Those both correspond to an effective staircase level

- `k_eff ~ 7.97 - 8.30`

which is much closer to the `k_B = 8` denominator target than the
one-step cascade (`k_eff ~ 6.4`) or the unsuppressed base Yukawas (`k_eff ~ 4.5`).

---

## What This Buys Us

It gives a real structural explanation for why `k_B = 8` keeps reappearing:

1. the staircase/seesaw target demands a Dirac Yukawa of order `10^-3`
2. the EWSB cascade naturally produces a suppression of that order at **second**
   order
3. with an `O(0.5-0.65)` base coupling, that second-order cascade lands near the
   exact `k_B = 8` target

This now survives the direct-bridge normalization pass as well. The retained
bosonic-normalization theorem selects the unsuppressed local benchmark

`g_weak/sqrt(2)`,

while the old active-space `g_weak` value survives only as a non-physical
comparator. The useful robustness statement is therefore:

> the retained benchmark `g_weak/sqrt(2)` lands near `k_B = 8`, and even the
> rejected active-space comparator happens to stay in the same ballpark once
> the second-order cascade is applied.

That is materially stronger than saying "`alpha_LM^2` happens to be close."

---

## Why This Is Still Not Closure

The live Nature-bar objection has moved downstream.

This note is **bounded** because it is only the historical candidate surface.
The exact local Dirac-lane coefficient is now fixed by the Schur theorem, so
the branch no longer needs this note to defend the second-order mechanism.

What still prevents full closure is not the Dirac return coefficient. It is
the Majorana side:

- whether the unique charge-`2` Majorana source is axiom-forced to turn on
- how that one-slot source amplitude fixes the three-generation
  `A/B/epsilon` texture without fitted leftovers

So the correct current statement is:

> this note remains the bounded precursor that anticipated the right scale,
> while the remaining blocker has moved to the Majorana / `Z_3` activation law.

---

## Updated Harsh Blocker

The blocker is now sharper than before:

> derive or rule out an axiom-side activation law for the unique Majorana
> charge-`2` source, and show how that one amplitude fixes the
> three-generation `A/B/epsilon` structure.

If that lands, the exact local Dirac result can feed a full denominator
closure. If it fails, the honest claim remains the locally sharpened Dirac
lane plus the bounded leptogenesis / `R(eta)` surface.
