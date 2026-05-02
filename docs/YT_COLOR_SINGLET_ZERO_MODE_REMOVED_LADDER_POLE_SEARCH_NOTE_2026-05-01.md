# Color-Singlet Zero-Mode-Removed Ladder Pole Search

**Date:** 2026-05-01
**Status:** bounded-support / color-singlet zero-mode-removed ladder pole search
**Runner:** `scripts/frontier_yt_color_singlet_zero_mode_removed_ladder_pole_search.py`
**Certificate:** `outputs/yt_color_singlet_zero_mode_removed_ladder_pole_search_2026-05-01.json`

## Purpose

The color-singlet zero-mode theorem removes the exact `q=0` gauge mode, and
the finite-`q` IR regularity theorem shows the remaining massless kernel is
locally integrable in four dimensions.  The next question is whether the
zero-mode-removed finite Wilson-exchange ladder already provides a stable
scalar pole and LSZ derivative.

## Result

```text
python3 scripts/frontier_yt_color_singlet_zero_mode_removed_ladder_pole_search.py
# SUMMARY: PASS=9 FAIL=0
```

The scan uses the color-singlet `q=0` removal, `mu_IR^2 = 0`, grid sizes
`N = 3,4,5,6`, masses `0.20, 0.30, 0.35, 0.50, 0.75, 1.00`, and local plus
zero-momentum-normalized point-split source projectors.

It finds constructive finite pole witnesses, but not a retained pole theorem:

| Check | Witness |
|---|---|
| finite pole witnesses exist | 4 scan rows have `lambda_max >= 1` |
| volume stability fails | local `m=0.30`: `N3=0.266142696527`, `N4=1.46336779249`, `N5=0.126842907152`, `N6=0.365521262467` |
| projector stability fails | `N6,m=0.20`: local `1.48744308139`, point-split normalized `0.50986398468` |
| taste-corner aliasing is load-bearing | all crossing rows are on even `N=4,6` grids with `16` `sin(p)=0` corners; odd low-mass max is `0.58651601582` |
| derivative/residue proxy is not universal | crossing residue-proxy spread is `5.15346x` |

The finite pole witnesses are therefore route information, not scalar LSZ
closure.  They are sensitive to finite-volume parity, taste-corner aliasing,
source projector, and the total-momentum derivative.

## Claim Boundary

This block does not claim retained or proposed-retained `y_t` closure.  It does
not set `kappa_s = 1`, does not use `H_unit` or `yt_ward_identity`, does not
use observed top mass or observed `y_t`, and does not use `alpha_LM`,
plaquette, `u0`, `c2 = 1`, or `Z_match = 1` as proof inputs.

The remaining positive route is narrower: derive the continuum/taste/projector
limit of the interacting color-singlet scalar denominator and its
inverse-propagator derivative, or measure the same-source pole derivative in
production FH/LSZ data.
