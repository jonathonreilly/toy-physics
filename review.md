# Review: `science/w-mass-derived`

## Verdict

Reject for `main` as currently framed.

The branch contains a real arithmetic runner, and the note is already careful
to keep the lane bounded rather than retained. But the current authority
surface is still too strong for two reasons:

1. it treats the remaining `M_W` gap after the one-loop running step as if it
   were of ordinary missing `2`-loop / `Delta r_rem` size, and
2. it says the RGE readout does not import pole values into the derivation,
   while the runner explicitly uses the PDG `M_W` value as the logarithmic
   anchor.

## Findings

### 1. The residual-size interpretation is too strong

The note says the one-loop readout

```text
M_W^RGE = 80.5589 GeV
```

is only missing standard `2`-loop / mixing cleanup. But the branch's own
comparison table shows

- `+0.1897 GeV` vs the PDG average,
- `+0.1254 GeV` vs CDF-II,
- `+0.1924 GeV` vs ATLAS,
- `+0.1987 GeV` vs CMS,
- `+0.2049 GeV` vs LHCb.

Those are not small residuals on the scale of precision `M_W` physics. They
are `13`-to-`14 sigma` offsets against the direct-measurement uncertainties
quoted in the note itself. More importantly, the note invokes standard SM
`Delta r` / two-loop language, but the current SM indirect prediction is at the
few-MeV level, not the `O(0.1-0.2 GeV)` level. So the lane may still be a
useful same-surface proxy readout, but it cannot honestly be sold as "within
typical missing two-loop / `Delta r_rem` magnitude" in its present wording.

### 2. The runner does import a measured pole value into the readout

The note says no SM pole values enter the derivation and that the W-pole anchor
is only a harmless ppm-level detail. The dependence is indeed numerically small
across reasonable W-scale anchors, but the actual runner still sets

```python
TARGET_MW = M_W_PDG[0]
```

and uses that value inside `log(M_W / v)` to compute `g_2(M_W)` and the final
`M_W^RGE`.

So the reported `80.5589 GeV` number is not a pure framework-only readout in
the strong sense claimed by the note. The branch either needs to solve this
self-consistently or state plainly that the bounded RGE readout uses an
experimental W-scale anchor, albeit weakly.

## Recommendation

Do not land this lane as-is.

If you want to salvage it, the minimal acceptable rewrite is:

- demote the lane from "bounded companion against pole measurements" to a
  weaker same-surface consistency probe,
- remove the claim that the `~0.2 GeV` residual is of ordinary missing
  two-loop / `Delta r_rem` size,
- explicitly disclose the PDG-anchor use in the runner or replace it with a
  self-consistent fixed-point solve, and
- if you later want it on `main`, wire the accepted version through the repo's
  package surfaces rather than leaving it as a free-floating root note.
