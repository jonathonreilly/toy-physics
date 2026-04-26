# Signed Gravity Mechanism Separation Note

**Date:** 2026-04-25
**Status:** mechanism-separation gate for AWAY / repulsive-looking rows; not a
claim surface
**Script:** [`../scripts/signed_gravity_mechanism_separator.py`](../scripts/signed_gravity_mechanism_separator.py)

This note separates signed-response consequences from other ways an AWAY read
can appear in the current harnesses.

The language boundary is strict. This is not negative mass, gravitational
shielding, propulsion, reactionless force, or physical antigravity. A signed
gravity promotion requires a native or naturally hosted `chi_g = +/-1`, a
branch-stable signed source, source/response locking by the same label,
positive inertial mass, and two-body action-reaction closure.

## Required Buckets

Every future AWAY or repulsive-looking row in this lane must be assigned one
mechanism before interpretation:

| mechanism | tag | class | signed-gravity status |
|---|---|---|---|
| `locked_chi_response` | `SIGNED_RESPONSE_CANDIDATE` only if all gates pass | conservative candidate | conditional; currently blocked by selector/source P0 gates |
| `lensing_phase_flip` | `LENSING_PHASE_ONLY` | interference | not selector evidence |
| `complex_absorptive_away` | `COMPLEX_ABSORPTIVE_ONLY` | absorptive / nonunitary transport | not conservative repulsive gravity |
| `boundary/proxy` | `BOUNDARY_PROXY_ONLY` | boundary or readout proxy | not promotable |
| `inserted_control_no_go` | `CONTROL_NO_GO` | inserted sign or failed control | no-go/control only |

The bucket is part of the result. A row with no bucket is not eligible for a
signed-gravity read.

## Locked `chi` Response

The locked algebraic harness is the only current mechanism with the desired
four-pair consequence table:

```text
++ and --: same-sector attraction
+- and -+: opposite-sector repulsion
positive inertial mass
two-body action-reaction only when source and response signs are locked
```

This is a consequence harness, not a derivation. The local/taste-cell selector
scan currently returns `NO_GO_STRICT_SELECTOR` in
[`SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md`](SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md).
The local source-density audit currently returns
`SOURCE_PRIMITIVE_BLOCKED_LOCAL` in
[`GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md`](GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md).

Therefore the locked rows are classified as:

```text
mechanism = locked_chi_response
claim tag = CLAIM_SURFACE_BLOCKED
reason = selector/source gates are not passed
```

They can become `SIGNED_RESPONSE_CANDIDATE` only after both gates are supplied
and the locked two-body action-reaction gate remains passed.

## Lensing Phase Flip

The lensing rows are phase-interference diagnostics. The `k*h` sweep in
[`LENSING_K_SWEEP_NOTE.md`](LENSING_K_SWEEP_NOTE.md) shows sign changes across
phase windows, including repulsive reads at low and high `k*h`. The signed
gravity companion script
[`../scripts/lensing_sign_phase_diagram.py`](../scripts/lensing_sign_phase_diagram.py)
explicitly separates `chi_product` from wave phase and reports sign-clean,
wave-dominated, and phase-flipped rows.

Safe interpretation:

- a lensing AWAY row may diagnose wave phase or centroid interference
- it does not derive `chi_g`
- it does not prove negative gravitational mass, shielding, propulsion, or
  physical antigravity
- it cannot promote a signed sector without the selector/source and two-body
  closure gates

Classification:

```text
mechanism = lensing_phase_flip
claim tag = LENSING_PHASE_ONLY
```

## Complex Absorptive AWAY

The complex-action lane uses

```text
S = L(1 - f) + i gamma L f
```

as recorded in [`COMPLEX_ACTION_NOTE.md`](COMPLEX_ACTION_NOTE.md). At larger
`gamma`, near-source paths are preferentially attenuated, so the surviving
detector centroid can move AWAY. Born cleanliness can remain machine-clean
because the propagation is still linear in the amplitude; it is not by itself a
signed-gravity sector test.

The complex-action family notes also classify the effect as anchor-local and
boundary-sensitive:
[`COMPLEX_SELECTIVITY_COMPARE_NOTE.md`](COMPLEX_SELECTIVITY_COMPARE_NOTE.md)
and
[`COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md`](COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md).

Safe interpretation:

- the AWAY row is absorptive path selection
- it is not conservative repulsive gravity
- `gamma = 0` reduction and Born cleanliness are necessary controls, not
  selector evidence
- no physical signed-gravity promotion follows from complex-action AWAY alone

Classification:

```text
mechanism = complex_absorptive_away
claim tag = COMPLEX_ABSORPTIVE_ONLY
```

## Boundary / Proxy

Some rows use centroids, detector-line reads, boundary windows, graph-family
proxies, finite-path observables, or architecture-specific directional
proxies. These may be useful diagnostics, but the readout can change sign
because the observable changed, the family boundary was crossed, or the proxy
lost its intended meaning.

Classification:

```text
mechanism = boundary/proxy
claim tag = BOUNDARY_PROXY_ONLY
```

Boundary/proxy rows are never selector evidence unless separately replayed on a
conservative locked-source/locked-response two-body gate.

## Inserted Control / No-Go

Inserted signs are useful controls. They are also the easiest way to produce
misleading signed tables.

Current controls:

- source-only and response-only signs fail mixed-pair action-reaction
- inserted `chi_g |psi|^2` source bookkeeping can pass normalization checks
  but does not derive `chi_g`
- electrostatics-style signed source lanes start with charge sign by
  construction and cannot be imported as a gravitational selector

Classification:

```text
mechanism = inserted_control_no_go
claim tag = CONTROL_NO_GO
```

## Promotion Rule

An AWAY row may be described as a signed-response candidate only if all of the
following are true:

1. mechanism is `locked_chi_response`
2. native selector or protected superselection gate passes
3. signed source primitive gate passes
4. source and response are locked by the same label
5. two-body action-reaction closure passes
6. inertial mass remains positive
7. Born, norm, null-field, and `F~M` controls remain clean

At the current P0 state, the first two derivation gates do not pass:

```text
NO_GO_STRICT_SELECTOR
SOURCE_PRIMITIVE_BLOCKED_LOCAL
```

So all signed gravitational response reads remain consequence/control reads,
not physical antigravity claims.
