# Sixth Family Sheared Boundary

The sixth-family sheared-shell basin has a clean local boundary.

What fails:
- all rows at `drift = 0.50` fail the signed-source gate
- several mid-drift rows fail by sign-orientation flip even though the exact
  zero and neutral controls remain clean

What does not fail:
- this is not a control leak
- the zero-source baseline is exact where measured
- the neutral `+1/-1` gate is exact where measured
- the weak-field exponent on passing rows remains near `1.0`

The diagnosed saturation edge is therefore:
- the sheared-shell rule supports a narrow basin
- it does not widen into a family-wide closure on this architecture

So the correct boundary language is:
- `drift = 0.5` is a clean sign-flip edge
- the failure is structural selectivity, not a broken harness

