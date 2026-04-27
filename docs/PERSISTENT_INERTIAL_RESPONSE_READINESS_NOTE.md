# Persistent Inertial-Response Readiness Note

**Date:** 2026-04-04  
**Status:** bounded readiness audit; packet re-identification control now exists, and quasi-persistent relaunch/compression probes are now proposed_retained, but no persistent-mass theorem yet

## Purpose

This note answers a narrow question:

- is the current ordered-lattice codebase ready for a real persistent or
  quasi-persistent inertial-response experiment?

The honest answer is: **not yet**.

## What is already available

The nearest reusable pieces are:

- [`scripts/equivalence_principle_harness.py`](/Users/jonreilly/Projects/Physics/scripts/equivalence_principle_harness.py)
  - amplitude-level invariance and packet-shape dependence on the retained
    3D ordered-lattice family
- [`scripts/two_body_momentum_harness.py`](/Users/jonreilly/Projects/Physics/scripts/two_body_momentum_harness.py)
  - bounded two-body momentum comparison on the same family
- [`scripts/composite_source_additivity_harness.py`](/Users/jonreilly/Projects/Physics/scripts/composite_source_additivity_harness.py)
  - weak-field same-site and disjoint-source additivity on the same family
- [`scripts/amplitude_packet_mobility.py`](/Users/jonreilly/Projects/Physics/scripts/amplitude_packet_mobility.py)
  - older packet-motion machinery on a different rectangular/DAG lane
- [`scripts/gravity_pulsating_source.py`](/Users/jonreilly/Projects/Physics/scripts/gravity_pulsating_source.py)
  - older persistent-source exploration on a different rule-driven lane
- [`scripts/ordered_lattice_packet_reidentification.py`](/Users/jonreilly/Projects/Physics/scripts/ordered_lattice_packet_reidentification.py)
  - localized packet re-identification control on the retained 3D ordered-
    lattice family
  - frozen log:
    [`logs/2026-04-04-ordered-lattice-packet-reidentification.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-ordered-lattice-packet-reidentification.txt)
  - result: the packet is easy to re-identify under weak fields on the tested
    family, with best-shift scores at `1.000` and width ratios staying near
    `1.000` for `valley-linear`; `spent-delay` broadens slightly but still
    remains re-identifiable on this bounded control
- [`scripts/ordered_lattice_quasi_persistent_relaunch.py`](/Users/jonreilly/Projects/Physics/scripts/ordered_lattice_quasi_persistent_relaunch.py)
  - minimal ordered-lattice packet carry-through / relaunch probe on the same
    retained valley-linear family
  - frozen log:
    [`logs/2026-04-04-ordered-lattice-quasi-persistent-relaunch.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-ordered-lattice-quasi-persistent-relaunch.txt)
  - result: compact packets can be re-identified and relaunched with high
    overlap (`0.9516` and `0.9839` on the frozen rows), but this is still a
    surrogate rather than a persistent-mass theorem
- [`scripts/ordered_lattice_quasi_persistent_relaunch_2d.py`](/Users/jonreilly/Projects/Physics/scripts/ordered_lattice_quasi_persistent_relaunch_2d.py)
  - 2D cross-family sanity check for the same surrogate idea
  - frozen log:
    [`logs/2026-04-04-ordered-lattice-quasi-persistent-relaunch-2d.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-ordered-lattice-quasi-persistent-relaunch-2d.txt)
  - result: the surrogate idea is family-generic enough to remain useful, but
    still only as a bounded control
- [`scripts/quasi_persistent_relaunch_probe.py`](/Users/jonreilly/Projects/Physics/scripts/quasi_persistent_relaunch_probe.py)
  - smallest support-compression probe on the retained ordered-lattice family
  - frozen log:
    [`logs/2026-04-04-quasi-persistent-relaunch-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-quasi-persistent-relaunch-probe.txt)
  - result: moderate compression keeps the downstream response similar, but
    sharp localization fails and the best bounded surrogate still needs a broad
    support (roughly `196-225` sites on the frozen rows)
- [`scripts/mesoscopic_surrogate_backreaction_harness.py`](/Users/jonreilly/Projects/Physics/scripts/mesoscopic_surrogate_backreaction_harness.py)
  - one-step source/backreaction extension of the broad surrogate lane on the
    retained 3D ordered-lattice family
  - frozen log:
    [`logs/2026-04-04-mesoscopic-surrogate-backreaction.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-backreaction.txt)
  - result: the broad surrogate sources an additive weak field and supports
    bounded one-step two-body symmetry, but still only as a broad mesoscopic
    control object
- [`scripts/broad_surrogate_point_source_compare.py`](/Users/jonreilly/Projects/Physics/scripts/broad_surrogate_point_source_compare.py)
  - 3D interpretive diagnostic comparing the broad surrogate source against an
    equivalent-strength point source on the retained family
  - frozen log:
    [`logs/2026-04-04-broad-surrogate-point-source-compare.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-broad-surrogate-point-source-compare.txt)
  - result: on the tested retained 3D family, the broad surrogate behaves like
    a soft point source to high accuracy
- [`scripts/mesoscopic_surrogate_source_2d.py`](/Users/jonreilly/Projects/Physics/scripts/mesoscopic_surrogate_source_2d.py)
  - 2D companion check for the surrogate-source idea
  - frozen log:
    [`logs/2026-04-04-mesoscopic-surrogate-source-2d.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-source-2d.txt)
  - result: the source stays stable as a mesoscopic control, but its breadth
    still materially changes the response amplitude on the retained 2D family
- [`scripts/mesoscopic_surrogate_threshold_2d.py`](/Users/jonreilly/Projects/Physics/scripts/mesoscopic_surrogate_threshold_2d.py)
  - 2D support-threshold sweep for the same mesoscopic surrogate family
  - frozen log:
    [`logs/2026-04-04-mesoscopic-surrogate-threshold-2d.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-threshold-2d.txt)
  - result: no sharp support threshold appears on the retained 2D family;
    every scanned `topN` remains stable, so shrinking support is not the lever
    that breaks two-stage sourced-response stability there

## Minimal blocker

What is still missing is a reusable object on the **retained ordered-lattice
family** that satisfies all three of these at once:

1. it remains localized enough to be treated as a persistent or quasi-persistent pattern
2. it can source a field with a well-defined strength parameter
3. it has an inertial response that can be measured separately from ordinary
   test-particle steering

The current retained ordered-lattice harnesses only close the test-particle
regime. They do not yet produce a localized pattern whose own persistence and
response can both be measured on the same family.

## Safe read

The current Newton-selection lane is now strong enough to say:

- amplitude-level equivalence is frozen
- same-family momentum is frozen
- same-family additivity is frozen

But it is **not** strong enough to say:

- persistent-pattern inertial mass has been produced or measured

So the one-parameter-mass step remains open.

The new packet re-identification control narrows the blocker slightly:

- localized packets on the retained ordered family do stay recognizable after
  propagation
  - that makes a future inertial-response experiment plausible
  - but the control does **not** by itself produce a persistent pattern with a
    separately measurable inertial mass

The relaunch probe narrows the blocker further:

- the quasi-persistent surrogate survives re-identification well enough to be
  relaunched
- the relaunch overlap is high enough to be interesting
- but we still do not have a self-maintaining object that carries its own
  inertial mass in the model

The compression probe narrows it further:

- the surrogate only remains faithful when the support is still mesoscopic
- the best bounded surrogate is broad, not sharply localized
- that is progress beyond the readiness note, but still not persistent-mass
  closure

The 2D control suggests this is not a one-off 3D artifact:

- the compressed surrogate survives on a second ordered-lattice family too
- that makes the control more credible
- but it still stops short of a persistent-mass experiment

The broader relaunch probe sharpens the remaining gap:

- moderate compression is tolerable
- sharp compression is not
- so the missing inertial-response object is still not in hand

The source/backreaction extension sharpens it further:

- the broad surrogate can now source a weak additive field
- one-step two-body symmetry stays at the sub-percent level on the tested 3D
  rows
- but this still only closes a mesoscopic control object, not a localized
  persistent mass

The 3D vs 2D source diagnostics keep the boundary honest:

- on the retained 3D family, the broad surrogate behaves almost like a soft
  point source
- on the retained 2D family, the same source idea stays stable but its breadth
  still matters materially for the response amplitude
- so the surrogate-source lane is real, but still bounded and family-sensitive

The multistage probe sharpens the positive side:

- on the retained 3D family, the broad surrogate survives a second sourced
  response stage with high best-shift score and a stable centroid-shift scale
- so the mesoscopic source lane is now more than a one-step curiosity
- but it is still broad-control physics, not localized persistent-mass closure

The 2D two-stage companion sharpens the family-generic side:

- the broad surrogate also survives two sourced-response stages on the
  retained 2D family
- so the mesoscopic-source picture is not just a one-family 3D quirk
- but it still remains a bounded control picture rather than a persistent-mass
  theorem

The 2D support-threshold sweep sharpens the blocker further:

- shrinking the source support across `topN = 1 .. 81` does not produce a
  collapse on the retained 2D family
- the scanned 2D family is stable throughout the tested range
- so the missing inertial-response object is not hidden behind a simple
  support threshold in that family

The constrained 3D compact-family sweep sharpens it again:

- compact Gaussian and tapered compact families can survive explicit
  support/capture floors on the retained 3D `h = 0.5` family
- but they still do not beat the broad `topN` control on the admissible
  score/capture tradeoff
- so merely excluding degenerate point-like winners does not reopen the
  retained coarse 3D family

The constrained 3D annular / hollow / tapered sweep sharpens it one more time:

- no admissible non-degenerate annular, hollow, or tapered ellipsoid family
  beats the broad `topN` frontier on the retained 3D `h = 0.5` family
- so that family now looks closed as a broad-source control lane rather than a
  hidden sharp-localization lane

The localization frontier now looks like this:

- there is no single sharp collapse threshold in the retained 2D family
- on the retained 3D `h = 0.5` family, broad `topN` still owns the admissible
  frontier even after compact-floor and annular/hollow sweeps
- on the retained 3D `h = 0.25` family, the final constrained replay keeps the
  same conclusion under explicit support/capture floors: broad `topN 196`
  remains the best admissible row
- the new localized source-response sweep adds a narrower comparison: smaller
  source objects can remain admissible, but they still do not beat the broad
  `topN 196` frontier on the retained `h = 0.25` family
- very compact sources can stay extremely self-similar while becoming weak
- broader sources can carry much stronger response while remaining stable
- so the open question is no longer “is there a hidden 3D `h = 0.5` winner?”
- the localization lane is now frozen as a bounded broad-source control result,
  not an open hidden-winner search

## Best next experiment

The smallest viable next move is:

- do **not** keep treating the retained 2D support threshold as the next
  lever; the frozen sweep shows that family has no sharp support cutoff in the
  scanned range
- do **not** keep sweeping the retained 3D `h = 0.5` family for compact or
  annular winners; the new bounded negatives close that branch
- do **not** reopen the retained 3D `h = 0.25` lane without a genuinely new
  object family or mechanism; the constrained replay already closes the last
  cheap localization shot
- do **not** reopen the smaller-source comparison unless a new family is
  introduced; the latest sweep already shows that smaller sources stay
  admissible without beating the broad control
- the next honest escalation is now a true persistent/quasi-persistent
  inertial-response probe beyond the broad mesoscopic surrogate, or a bounded
  negative explaining why the current codebase still cannot realize it
