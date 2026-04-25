# Koide Delta Fractional-Period Endpoint No-Go Note

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_delta_fractional_period_endpoint_no_go.py`
**Status:** executable no-go

RESIDUAL_SCALAR=`selected_endpoint_unit_map_to_eta_APS`

## Theorem Attempt

After the selected-line Berry endpoint audit, the next delta route was the
fractional-period variant: derive the physical Brannen endpoint from the
projective period of the retained `CP^1` selected line and the native `C3`
angular step, then identify that endpoint with the ambient APS support value
`eta_APS = 2/9`.

## Brainstormed Variants

1. **Raw-radian route:** use `eta_APS = 2/9` directly as a selected-line
   endpoint offset.
2. **Projective-period route:** multiply the dimensionless APS value by the
   selected-line projective period `pi`.
3. **Full-cycle route:** multiply the APS value by `2*pi`.
4. **C3 endpoint lattice:** require the endpoint to lie in the lattice generated
   by the native `2*pi/3` step modulo projective period.
5. **Assumption inversion:** treat the endpoint/unit map as the unknown and
   test whether period arithmetic fixes it.

## Executable Result

The selected-line ray

```text
chi(theta) = (1, exp(-2i theta))/sqrt(2)
```

has projective period

```text
pi.
```

The retained `C3` step on the base angle is

```text
2*pi/3.
```

Modulo the projective period, the retained endpoint residues are therefore

```text
{0, pi/3, 2*pi/3}.
```

The runner checks three natural conversions of the ambient APS support value:

```text
raw radians:              2/9
projective-period scaled: 2*pi/9
full-cycle scaled:        4*pi/9
```

None is a retained endpoint residue in `{0, pi/3, 2*pi/3}`.

Equivalently, expressed in units of the endpoint lattice step `pi/3`, these
would require:

```text
(2/9)/(pi/3)      = 2/(3*pi)
(2*pi/9)/(pi/3)  = 2/3
(4*pi/9)/(pi/3)  = 4/3
```

These are not selected by the retained `C3` projective-period arithmetic.

## Unit-Map Obstruction

A free conversion

```text
theta_offset = u * eta_APS
```

can hit any chosen endpoint residue. For example:

```text
theta_offset = pi/3    -> u = 3*pi/2
theta_offset = 2*pi/3  -> u = 3*pi
```

Thus the endpoint result depends on a unit/endpoint map `u`. The retained
period lattice does not select that map.

## Hostile Review

- **Circularity:** the runner does not impose an endpoint equality. It tests
  whether the period lattice forces one.
- **Target import:** no Q-side target, mass data, or observational pin enters
  this audit.
- **Hidden primitive:** choosing the conversion from ambient APS number to
  selected-line endpoint offset is precisely the missing primitive.
- **Axiom link:** `C3` and projective periodicity fix the endpoint lattice, not
  the physical endpoint.
- **Scope:** this no-go rejects only the fractional-period route. The ambient
  APS result and selected-line Berry support remain intact.

## Verdict

Fractional-period arithmetic does not derive the physical delta bridge.

```text
KOIDE_DELTA_FRACTIONAL_PERIOD_ENDPOINT_NO_GO=TRUE
DELTA_FRACTIONAL_PERIOD_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_SCALAR=selected_endpoint_unit_map_to_eta_APS
```

