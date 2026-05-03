# Non-Source Response Rank-Repair Sufficiency

**Date:** 2026-05-03
**Status:** exact-support / rank-repair sufficiency theorem; current rows absent
**Runner:** `scripts/frontier_yt_non_source_response_rank_repair_sufficiency.py`
**Certificate:** `outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json`

## Purpose

This note sharpens the positive closure route after the `O_sp/O_H` identity
stretch blocked.  The Legendre/LSZ source-pole operator `O_sp` removes the
source-coordinate normalization, but the source-only FH/LSZ response still
provides only one linear row in the neutral scalar top-coupling space.

The exact repair is one of:

- pole-level source-Higgs Gram purity proving `O_sp = +/- O_H`;
- an independent non-source response row plus identity certificates strong
  enough to remove the orthogonal top-coupling null direction;
- a genuine dynamical rank-one theorem for the neutral scalar response space.

## Theorem Surface

In a two-component neutral scalar basis `(O_H, O_chi)`, source-only data give

```text
dE_top/ds = u_H y_H + u_chi y_chi.
```

With only the row `u = (u_H, u_chi)`, the null vector `(u_chi, -u_H)` leaves
`dE_top/ds` unchanged while changing `y_H`.  Therefore source-only FH/LSZ rows
cannot identify the canonical-Higgs Yukawa unless a purity or rank theorem
removes the null direction.

The runner records two exact repairs:

- If `O_sp = +/- O_H`, equivalently `Delta_spH = 0` and `|rho_spH| = 1` at the
  isolated pole, then the source response is the canonical-Higgs response.
- If a second independent non-source row is present and certified to live on
  the canonical-Higgs one-pole sector, the two-row matrix has rank two and the
  top-coupling vector is determined.

Generic W/Z slope data alone are not enough.  The W/Z route must still certify
same-source sector overlap and canonical-Higgs pole identity; otherwise an
orthogonal top-coupled neutral scalar can still contaminate `dE_top/ds`.

## Current Result

```bash
python3 scripts/frontier_yt_non_source_response_rank_repair_sufficiency.py
# SUMMARY: PASS=17 FAIL=0
```

The sufficiency theorem passes as exact support, but current PR #230 closure
does not pass:

- no production `C_sH/C_HH` pole rows are present;
- no accepted canonical `O_H` operator certificate is present;
- the O_sp-Higgs Gram-purity postprocessor is waiting for production rows;
- no same-source W/Z mass-response rows are present;
- the W/Z response gate and retained-route gate remain open.

## Claim Boundary

This is not retained or `proposed_retained` closure.  It does not set
`kappa_s = 1`, `cos(theta) = 1`, `c2 = 1`, or `Z_match = 1`.  It does not use
`H_unit`, `yt_ward_identity`, observed top or W/Z masses, observed `y_t`,
`alpha_LM`, plaquette, `u0`, or reduced pilots as proof authority.

## Next Action

Produce one rank-repair input:

- a certified same-surface canonical `O_H` plus production `C_sH/C_HH` pole
  rows passing O_sp-Higgs Gram purity; or
- production same-source W/Z mass-response rows with sector-overlap and
  canonical-Higgs identity certificates.
