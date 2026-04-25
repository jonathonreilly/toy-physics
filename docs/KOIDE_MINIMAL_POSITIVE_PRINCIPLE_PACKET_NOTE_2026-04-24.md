# Koide minimal positive-principle packet

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_minimal_positive_principle_packet.py`  
**Status:** conditional positive theorem; not retained closure

## Purpose

This note states the smallest currently visible positive closure packet for
the charged-lepton Koide lane.  It proves what would close the lane if the
needed physical principles are retained, while keeping the Nature-grade
boundary explicit.

## Candidate principles

### Q principle

The physical charged-lepton source is Morita-normalized and component
anonymous after passing to the finite quotient-center source object:

```text
p = (w, 1-w)
swap(p) = p.
```

The runner verifies:

```text
w = 1/2
K_TL = 0
Q = 2/3.
```

### Delta principle

The selected Brannen line is the whole physical APS boundary segment:

```text
eta_closed = delta_open + tau
tau = 0.
```

The runner verifies:

```text
delta_open = eta_APS = 2/9.
```

## Conditional theorem

If both principles are derived or accepted as retained physical laws, then:

```text
Q = 2/3
delta_physical = eta_APS = 2/9.
```

The scale `v0` remains separate unless a later theorem couples it.

## Why this is not current retained closure

The runner also verifies counter-states when either principle is absent:

```text
w = 1/3 -> Q = 1, K_TL = 3/8
tau = 1/9 -> delta_open = 1/9, eta_closed = 2/9.
```

So the current packet is a conditional theorem, not Nature-grade closure.  The
remaining work is to derive:

```text
RESIDUAL_Q_PRINCIPLE = derive_quotient_center_component_anonymity
RESIDUAL_DELTA_PRINCIPLE = derive_identity_endpoint_gluing_tau_zero.
```

## Falsifiers

- A retained source preparation that is Morita-normalized but not component
  anonymous.
- A physical reason the C3 character-orbit distinction must remain visible to
  the source after quotient-center reduction.
- A selected-line endpoint transition with `tau != 0` that preserves the
  closed APS value.
- A complement segment in the physical APS boundary that is not trivial.

## Reviewer objections answered

- **"You imported Q by uniformity."**  Correct unless component anonymity is
  independently derived.  The packet names that as the residual principle.
- **"You imported delta by identity gluing."**  Correct unless `tau=0` is
  independently derived.  The packet names that as the residual principle.
- **"This is still useful."**  Yes: it reduces the positive closure target to
  two exact physical principles with executable counterexamples.

## Verification

Run:

```bash
python3 scripts/frontier_koide_minimal_positive_principle_packet.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_MINIMAL_POSITIVE_PRINCIPLE_PACKET=TRUE
KOIDE_CONDITIONAL_Q_CLOSURE_UNDER_COMPONENT_ANONYMITY=TRUE
KOIDE_CONDITIONAL_DELTA_CLOSURE_UNDER_IDENTITY_GLUING=TRUE
KOIDE_CURRENT_RETAINED_Q_CLOSURE=FALSE
KOIDE_CURRENT_RETAINED_DELTA_CLOSURE=FALSE
RESIDUAL_Q_PRINCIPLE=derive_quotient_center_component_anonymity
RESIDUAL_DELTA_PRINCIPLE=derive_identity_endpoint_gluing_tau_zero
```
