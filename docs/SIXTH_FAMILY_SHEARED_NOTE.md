# Sixth Family Sheared Basin

**Status:** bounded - bounded or caveated result note
The sixth-family scout tests a parity-sheared shell connectivity rule on the
no-restore grown slice. It is deliberately different from the earlier retained
families:

- not the original drift/restore grown family
- not the sector-transition family
- not the quadrant-reflection family
- not the radial-shell family
- not the cross-quadrant load-balanced family

The construction is a sheared-shell rule:
- shells are computed in a layer-dependent sheared `y/z` coordinate system
- the shear direction flips with layer parity
- each source keeps its shell, then a neighboring shell, then a small
  structured fallback floor

The narrow retained read is:
- exact zero-source baseline survives
- exact neutral `+1/-1` cancellation survives
- sign orientation survives on a subset of the sampled rows
- weak-field charge scaling stays very close to linear on the passing rows

Sweep result:
- `12/21` rows pass the exact gate
- drift coverage on the passes: `[0.0, 0.05, 0.1, 0.15, 0.2, 0.3]`
- mean exponent among passes: `0.999895`

The honest interpretation is:
- this is a real sixth-family basin
- it is narrow, not family-wide
- it extends the structured-family story one step outward without becoming a
  generic theorem

