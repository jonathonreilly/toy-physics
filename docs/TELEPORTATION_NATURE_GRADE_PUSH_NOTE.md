# Teleportation Nature-Grade Push Note

---

**This is a planning / added-principle push note. It does not
establish any retained claim.** The "minimal action," "least-dwell
carrier," and "signed sparse 3D resource window" content below are
introduced as added selection principles plus finite numerical
evidence, not as derivations from retained framework premises; the noisy pulse
decoder and finite-temperature detector content are bounded
independent-error models, not hardware/material derivations.

---

**Date:** 2026-04-26
**Status:** support / planning record / added-principle push only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / planning record / added-principle push only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit outcome.
**Propagates retained-grade:** no
**Proposes new claims:** no
**Runner:** `scripts/frontier_teleportation_nature_grade_push.py`

## Review scope (relabel 2026-05-10)

This file is a **planning push note** that pushes the native
taste-qubit teleportation lane toward nature-grade standards by
**adding** explicit selection principles and noisy apparatus models. It
is **not** a retained theorem closure and **must not** be audited as
one. Generated-audit context identified this repair target:

> other: Derive the selection principles from retained framework premises or
> promote them explicitly as defended physical postulates, prove an
> asymptotic/preparation theorem for the signed sparse branch, and
> replace independent-error pulse/detector proxies with a fabricated
> controller/material-medium model or a theorem bounding the omitted
> correlations.

The minimal-scope response in this PR is to **relabel** this document
as a planning / added-principle push record. The alternatives —
deriving the selection principles from retained framework premises, promoting them
as defended physical postulates, proving an asymptotic preparation
theorem, or replacing the proxies with hardware/material models —
belong in dedicated review-loop or per-target audit passes. Until that
work is done:

This relabel does not promote any new physical postulate; that branch
would require explicit user approval before review-loop could land it.

- This file makes **no** retained-claim assertions of its own.
- The "Added Principle 1: Minimal Action Apparatus," "Added Principle
  2: Least-Dwell Carrier," and "Signed Sparse 3D Resource Window"
  sections are **conditional planning evidence** under the stated added
  assumptions, citeable only as a conditional open-gate planning
  bundle for ordinary state teleportation, with no matter, energy,
  object, or FTL transport claim.
- The retained-status surface for any teleportation-lane sub-claim is
  the audit ledger (`docs/audit/AUDIT_LEDGER.md`) plus dedicated
  per-claim notes, **not** this push.

## Scope

This artifact pushes the remaining native taste-qubit teleportation blockers
toward nature-grade standards by adding explicit selection principles and noisy
apparatus models.

It does not claim unconditional closure from the original sole axiom. The
result is conditional:

- causal-positive minimal action selects the lowest transducer winding;
- a least-dwell massless-carrier rule selects one amplitude law;
- a signed sparse 3D Poisson branch survives side `4,6,8`;
- noisy square-pulse records decode below the word-failure target;
- a finite-temperature/lost-fragment detector model remains classical.

The scope remains ordinary quantum state teleportation only. No matter, mass,
charge, energy, object, or faster-than-light transport is claimed.

## Added Principle 1: Minimal Action Apparatus

The hard-blocker pass showed that transducer windings

```text
theta_m = pi/2 + pi m
```

write the same Bell record. This runner adds a causal-positive minimal action
principle:

```text
minimize theta_m^2 over m >= 0.
```

Observed result:

```text
windings = 0..5
selected = 0
angle = 1.570796
action_gap = 19.739209
negative_orientation_degenerate = True
```

The remaining degeneracy is the negative orientation `-pi/2`, which has the
same action if negative pulse orientation is admitted. The added principle is
therefore "causal-positive minimal action," not bare action alone.

## Added Principle 2: Least-Dwell Carrier

The amplitude-level field obstruction showed that support/eikonal constraints
do not determine amplitudes. This runner adds a massless least-dwell carrier
rule inside the isotropic nearest-neighbor class:

```text
minimize center_weight^2
```

with cubic isotropy and one-step norm normalization. The selected law is:

```text
center_weight = 0
neighbor_weight = 1/sqrt(6) = 0.408248
```

Observed result:

```text
candidates = 4
selected_center = 0.000
dwell_gap = 0.062500
norm_error = 0.000e+00
isotropy_error = 0.000e+00
```

This is a unique law after adding least-dwell. It is not derived from the
original sole axiom.

## Signed Sparse 3D Resource Window

The hard-blocker pass showed that positive `G` side-6 controls do not preserve
the side-4 high-fidelity resource. A broader sweep revealed a signed branch:
fixed `G=-1000` gives high-fidelity retained Bell resources on side `4,6,8`.

Observed rows:

```text
side=4, G=-1000: Bell*=0.999702, Fbest=0.999802, CHSH=2.827585, gap=0.0244025
side=6, G=-1000: Bell*=0.999709, Fbest=0.999806, CHSH=2.827604, gap=0.0120618
side=8, G=-1000: Bell*=0.999711, Fbest=0.999807, CHSH=2.827608, gap=0.00704654
```

This repairs the finite sparse scaling evidence, but only as finite evidence.
The gap decreases with side, and no asymptotic preparation theorem is supplied.

## Noisy Pulse Decoder

The retained record code is decoded under independent slot flips caused by
area jitter plus leakage:

```text
p_area = sin(area_error)^2
p_eff = p_leak + (1 - p_leak) p_area
```

The default `area_error=0.01`, `p_leak=1e-5` gives:

```text
area_slot_error = 1.000e-04
effective_slot_error = 1.100e-04
mean_word_failure = 5.055e-11
worst_branch_failure = 5.055e-11
```

This gives a noisy independent-error record model. It is still not a physical
controller with bandwidth, leakage-spectrum, cross-talk, or calibration drift.

## Finite-Temperature Detector Robustness

The spin-bath detector model is hardened with thermal reset failure and fragment
loss. The effective single-fragment overlap bound is:

```text
q_eff = p_reset + (1 - p_reset) |cos(theta)|
```

and the number of fragments is reduced by the loss fraction.

Default result:

```text
coupling_angle = 0.800
thermal_reset_failure = 1.000e-02
fragment_loss = 5.000e-02
effective_fragments = 22/24
effective_fragment_overlap = 0.699740
max_record_overlap = 8.770e-18
entropy_defect = 0.000e+00
```

This remains a finite spin-bath robustness model. It is not a material medium or
continuum irreversible limit.

## First Run

Command:

```bash
python3 scripts/frontier_teleportation_nature_grade_push.py
```

Acceptance gates:

- minimal action selects the causal-positive transducer winding;
- least-dwell principle selects a unique amplitude carrier law;
- signed sparse 3D resource window survives sides `4,6,8`;
- noisy calibrated pulse decoder stays below word-failure target;
- finite-temperature detector model remains classical after losses;
- claim boundary stays state-only and not FTL.

## Retained Status

This pass moves the lane from "current axioms underdetermine the mechanisms" to
"extra selection principles and finite noisy models close the audited gates."

The remaining nature-grade issue is now philosophical and technical:

- either derive the added principles from the original framework;
- or state them as retained physical postulates and defend them;
- and still supply an asymptotic preparation theorem plus hardware/material
  models beyond independent-error proxies.
