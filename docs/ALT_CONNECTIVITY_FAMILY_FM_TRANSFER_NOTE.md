# ALT Connectivity Family F~M Transfer Note

**Date:** 2026-04-06  
**Status:** proposed_retained weak-field linearity on the alternative connectivity family

## Artifact Chain

- [`scripts/ALT_CONNECTIVITY_FAMILY_FM_TRANSFER.py`](/Users/jonreilly/Projects/Physics/scripts/ALT_CONNECTIVITY_FAMILY_FM_TRANSFER.py)
- [`logs/2026-04-06-alt-connectivity-family-fm-transfer.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-alt-connectivity-family-fm-transfer.txt)
- [`docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md)
- [`docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md)

## Question

Does the alternative structured connectivity family preserve the weak-field mass
scaling law on the no-restore grown slice?

## Result

Yes. The mass-scaling law is retained across the full tested drift range.

Sweep summary:

- tested drifts: `0.0, 0.1, 0.2, 0.3, 0.5`
- tested seeds: `0, 1, 2`
- passing rows: `15/15`
- mean `F~M`: `0.999994`

## Safe Read

This family is not just a signed-source basin.
It also preserves weak-field linearity across the full tested range.

That makes the alternative sector-transition family a stronger retained
structured-connectivity lane than a narrow one-off sign-law patch.

## Conclusion

The parity-rotated sector-transition family now has three retained features:

- exact zero / neutral controls on the signed-source package
- a bounded basin for sign transfer
- weak-field `F~M ~ 1` across the full tested drift sweep

That is a real alternative structured connectivity family on the no-restore
grown slice.
