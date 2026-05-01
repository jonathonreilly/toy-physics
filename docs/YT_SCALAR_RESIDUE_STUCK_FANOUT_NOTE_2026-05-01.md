# Top-Yukawa Scalar Residue Stuck Fan-Out

**Date:** 2026-05-01  
**Status:** open fan-out / no retention proposal  
**Runner:** `scripts/frontier_yt_scalar_residue_stuck_fanout.py`  
**Certificate:** `outputs/yt_scalar_residue_stuck_fanout_2026-05-01.json`

```yaml
actual_current_surface_status: open
conditional_surface_status: conditional-support for an HS/RPA pole route if a scalar-channel coupling theorem is supplied
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Fan-out exposes the next missing input rather than retiring it."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The physics-loop skill requires a stuck fan-out after repeated no-go or blocker
cycles.  This note records five orthogonal attempts on the scalar
pole-residue/common-dressing blocker after the source two-point stretch
attempt.

## Frames Tested

| Frame | Result |
|---|---|
| F1 free/logdet source curvature | exact support: source curvature is a fermion bubble |
| F2 finite-volume near-match to `1/sqrt(6)` | no-go shortcut: the near-match is not stable |
| F3 HS/RPA scalar pole equation | conditional-support only: needs scalar-channel coupling/pole theorem |
| F4 common scalar/gauge dressing | open: source bubble does not force dressing equality |
| F5 direct measurement / HQET | open empirical route: needs fine-scale or heavy-top treatment |

## F2: Near-Match Check

The stretch runner exposed a tempting numerical coincidence:

```text
L=8, T=16, m=0.10 -> Z_proxy = 0.406810214752
1/sqrt(6)          -> 0.408248290464
```

The fan-out checks whether this is stable.  It is not:

```text
L=24, T=48, m=0.10 -> Z_proxy = 0.299432554066
drift              -> 0.107377660686
```

So the near-match is not a retained closure route.

## F3: HS/RPA Pole Equation

The source curvature can be used as a bubble input for an auxiliary scalar
pole equation of the schematic form

```text
D_H(p)^-1 = G^-1 - Pi(p).
```

Holding the same free bubble fixed while varying `G^-1` changes whether a
positive real pole exists and changes the residue when it does:

| `G^-1` | positive real pole? | residue |
|---:|---|---:|
| `0.01` | no | - |
| `0.03` | no | - |
| `0.06` | yes | `116.163450526767` |
| `0.12` | yes | `36.022461813679` |

This is the sharpest positive next route: derive the scalar-channel coupling
or pole condition from the retained action.  Without that, the bubble alone is
not a Higgs pole-residue theorem.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_scalar_residue_stuck_fanout.py
# SUMMARY: PASS=6 FAIL=0
```

## Selected Next Route

The campaign should continue with F3:

```text
derive or rule out a retained scalar-channel HS/RPA pole condition from A_min.
```

This is the only fan-out route that could turn the exact source-bubble
curvature into a physical scalar pole-residue theorem without importing
observed `y_t`, observed `m_t`, or the old `H_unit` matrix-element definition.

## Non-Claims

- This note does not prove a physical Higgs pole.
- This note does not promote the Ward theorem.
- This note does not define `y_t_bare` by an `H_unit` matrix element.
- This note does not use observed top mass or observed Yukawa values.
