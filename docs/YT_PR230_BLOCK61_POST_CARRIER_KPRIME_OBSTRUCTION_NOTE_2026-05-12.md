# PR230 Block61 Post-Carrier K-Prime Obstruction

**Status:** no-go / exact negative boundary for the current PR230 surface:
Block60 source-carrier support does not fix `K'(pole)` or pole residue
**Runner:** `scripts/frontier_yt_pr230_block61_post_carrier_kprime_obstruction.py`
**Certificate:** `outputs/yt_pr230_block61_post_carrier_kprime_obstruction_2026-05-12.json`

## Claim

Block60 fixes the compact additive source-channel taste-singlet carrier.  This
block tests the tempting follow-on shortcut

```text
fixed source carrier + fixed scalar pole location
=> fixed K'(pole) / scalar LSZ residue
```

The shortcut is not valid on the current PR230 surface.  The scalar residue
depends on the derivative of the inverse denominator at the pole, not only on
the source carrier and the pole location.

## Counterfamily

The runner constructs the same-carrier denominator family

```text
D_z(x) = z (x - x_pole) + (x - x_pole)^2
```

with fixed `x_pole` and fixed source carrier.  For every `z`, the pole
location is preserved because `D_z(x_pole)=0`, but

```text
D'_z(x_pole) = z.
```

With fixed numerator at the pole, the residue proxy `N/D'_z(x_pole)` varies by
a factor of eight across the checked family.  Therefore a fixed source carrier
and a fixed pole position do not determine the scalar LSZ residue, `K'(pole)`,
or the strict source-Higgs pole rows.

## Boundary

This result preserves Block60 as useful exact support: the compact additive
source fixes the source-channel taste-singlet carrier coordinate.  It also
narrowly blocks the post-Block60 promotion path.  A positive route must supply
one of the missing pieces directly:

- a same-surface theorem for `K'(pole)` or the scalar pole residue;
- a strict direct pole-row measurement with contact/threshold/FVIR authority;
- a canonical `O_H`/source-overlap theorem or physical-response bridge that
  authorizes the `C_ss/C_sH/C_HH` rows.

## Parent Surface

- [Block60 compact source taste-singlet carrier](YT_PR230_BLOCK60_COMPACT_SOURCE_TASTE_SINGLET_CARRIER_GATE_NOTE_2026-05-12.md)
- [K-prime closure attempt](YT_KPRIME_CLOSURE_ATTEMPT_NOTE_2026-05-02.md)
- [Scalar kernel Ward-identity obstruction](YT_SCALAR_KERNEL_WARD_IDENTITY_OBSTRUCTION_NOTE_2026-05-01.md)
- [Scalar ladder residue-envelope obstruction](YT_SCALAR_LADDER_RESIDUE_ENVELOPE_OBSTRUCTION_NOTE_2026-05-01.md)
- [Scalar ladder eigen-derivative gate](YT_SCALAR_LADDER_EIGEN_DERIVATIVE_GATE_NOTE_2026-05-01.md)

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not identify the source carrier with canonical `O_H`.  It does not
infer `K'(pole)`, pole residue, threshold/FVIR authority, or strict
`C_ss/C_sH/C_HH` pole rows from source-carrier normalization.

It does not use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed top/Yukawa
values, `alpha_LM`, plaquette, `u0`, `kappa_s=1`, `c2=1`, or `Z_match=1`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block61_post_carrier_kprime_obstruction.py
python3 scripts/frontier_yt_pr230_block61_post_carrier_kprime_obstruction.py
# SUMMARY: PASS=9 FAIL=0
```
