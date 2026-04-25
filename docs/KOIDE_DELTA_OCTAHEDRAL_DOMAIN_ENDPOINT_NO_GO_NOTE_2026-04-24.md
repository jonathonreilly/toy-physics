# Koide Delta Octahedral-Domain Endpoint No-Go Note

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_delta_octahedral_domain_endpoint_no_go.py`
**Status:** executable no-go

RESIDUAL_SCALAR=`selected_octahedral_branch_fraction_minus_8_over_3pi`

## Theorem Attempt

The next delta route after the fractional-period audit was to use the
selected-line octahedral-domain geometry. The retained support runner shows
that the first selected-line branch has the span of one octahedral fundamental
domain. The attempted theorem was that this branch geometry selects the
physical Brannen endpoint and hence the ambient APS support value.

## Brainstormed Variants

1. **Fundamental-domain endpoint:** maybe the physical point is forced to be a
   boundary of the octahedral domain.
2. **Interior fraction:** maybe `eta_APS = 2/9` is a distinguished fraction of
   the branch span.
3. **Group-order arithmetic:** maybe `|O| = 24` combines with `d = 3` to pick
   the endpoint.
4. **Positivity endpoint:** maybe the branch endpoint where one coordinate
   vanishes selects the physical phase.
5. **Assumption inversion:** perhaps the octahedral theorem supplies only an
   interval, and the interior endpoint is an independent physical datum.

## Executable Result

The retained octahedral rotation group has order

```text
|O| = 24.
```

Therefore one first-branch fundamental domain has span

```text
L_O = 2*pi/|O| = pi/12.
```

The ambient support value

```text
eta_APS = 2/9
```

lies inside the interval because `2/9 < pi/12`. But its branch fraction is

```text
(2/9)/(pi/12) = 8/(3*pi).
```

The octahedral group order selects the branch boundaries `f = 0` and `f = 1`.
It does not select the interior fraction `8/(3*pi)`.

The runner checks a continuum of branch endpoints:

```text
f = 0
f = 1/2
f = 8/(3*pi)
f = 1
```

All preserve the same octahedral branch geometry. Only the third gives the
ambient support value as the endpoint offset, and it does so because that
interior fraction was chosen.

## Group-Order Fractions

The obvious group-order fractions also miss the raw selected endpoint:

```text
1/24 of full turn = pi/12
1/12 of full turn = pi/6
1/9  of full turn = 2*pi/9
2/9  of full turn = 4*pi/9
2/9  of branch    = pi/54
```

None equals `2/9` as a selected-line endpoint offset.

## Hostile Review

- **Circularity:** the runner does not choose the physical interior point; it
  checks whether the octahedral branch does.
- **Target import:** no mass matching or observational pin enters this audit.
- **Hidden primitive:** selecting `f = 8/(3*pi)` would be the missing endpoint
  law.
- **Axiom link:** octahedral geometry fixes the branch interval and endpoint
  boundaries, not the physical interior endpoint.
- **Scope:** this no-go does not weaken the octahedral support theorem. It
  rejects only promoting it to the physical delta bridge by itself.

## Verdict

Octahedral-domain geometry is support, not delta closure.

```text
KOIDE_DELTA_OCTAHEDRAL_DOMAIN_ENDPOINT_NO_GO=TRUE
DELTA_OCTAHEDRAL_DOMAIN_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_SCALAR=selected_octahedral_branch_fraction_minus_8_over_3pi
```

