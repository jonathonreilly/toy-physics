# PR230 Block62 Compact-Source K-Prime Identifiability Obstruction

**Status:** no-go / exact negative boundary for the current PR230 surface:
compact source support and fixed carrier do not identify `K'(pole)` or pole
residue
**Runner:** `scripts/frontier_yt_pr230_block62_compact_source_kprime_identifiability_obstruction.py`
**Certificate:** `outputs/yt_pr230_block62_compact_source_kprime_identifiability_obstruction_2026-05-12.json`

## Claim Tested

Blocks 57 and 58 give an exact compact finite-volume scalar-source functional
and a positive finite-volume source-channel spectral representation.  Block60
fixes the source-channel taste-singlet carrier, and Block61 blocks the simpler
fixed-carrier plus fixed-pole-location shortcut.  This block tests the
remaining compact-source shortcut:

```text
compact source functional
+ finite positive source spectrum
+ fixed source carrier
=> K'(pole) / pole residue
```

The shortcut fails on the current surface.  Compact finite-volume source
support constrains source moments and positivity, but it does not identify the
denominator derivative at the scalar pole or the corresponding LSZ residue.

## Positive Spectral Counterfamily

The runner constructs positive three-atom source spectral measures with common
pole mass, common source carrier, common source curvature
`C0 = sum_i w_i`, and common one-step source correlator
`C1 = sum_i w_i exp(-m_i)`.  The pole residue is varied while the two
background weights are solved to keep `C0` and `C1` fixed:

```text
rho = r_pole delta(m - 1.0)
    + w_light delta(m - 1.4)
    + w_heavy delta(m - 8.0).
```

The checked rows keep all weights nonnegative and preserve the same compact
source support invariants while moving the pole residue from `0.18` to `0.58`,
a factor of about `3.2`.  Therefore the current compact-source data and fixed
source carrier are compatible with different pole residues.

## Boundary

Block62 preserves Blocks 57, 58, and 60 as useful support.  It narrows the
remaining scalar-root obligation: a positive closure route must supply one of
the missing objects directly rather than replaying compact-source support as
pole authority:

- same-surface Schur `A/B/C` kernel rows with pole derivatives;
- strict direct `C_ss/C_sH/C_HH` pole rows with Gram, FV/IR, threshold, and
  contact authority;
- a thermodynamic scalar denominator theorem deriving `K'(pole)` and the pole
  residue;
- canonical `O_H`/source-overlap authority or a strict physical-response bridge.

## Parent Surface

- [Block57 compact source-functional foundation](YT_PR230_BLOCK57_COMPACT_SOURCE_FUNCTIONAL_FOUNDATION_GATE_NOTE_2026-05-12.md)
- [Block58 compact source-channel spectral support](YT_PR230_BLOCK58_COMPACT_SOURCE_SPECTRAL_SUPPORT_GATE_NOTE_2026-05-12.md)
- [Block60 compact source taste-singlet carrier](YT_PR230_BLOCK60_COMPACT_SOURCE_TASTE_SINGLET_CARRIER_GATE_NOTE_2026-05-12.md)
- [Block61 post-carrier K-prime obstruction](YT_PR230_BLOCK61_POST_CARRIER_KPRIME_OBSTRUCTION_NOTE_2026-05-12.md)
- [Source-functional LSZ identifiability theorem](YT_SOURCE_FUNCTIONAL_LSZ_IDENTIFIABILITY_THEOREM_NOTE_2026-05-03.md)
- [Schur complement K-prime sufficiency](YT_SCHUR_COMPLEMENT_KPRIME_SUFFICIENCY_NOTE_2026-05-03.md)
- [Schur K-prime row absence guard](YT_SCHUR_KPRIME_ROW_ABSENCE_GUARD_NOTE_2026-05-03.md)

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not identify the source carrier with canonical `O_H`.  It does not
infer `K'(pole)`, pole residue, threshold/FVIR authority, contact authority, or
strict `C_ss/C_sH/C_HH` pole rows from compact source support, finite-volume
source spectral positivity, or source-carrier normalization.

It does not use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed top/Yukawa
values, `alpha_LM`, plaquette, `u0`, `kappa_s=1`, `c2=1`, or `Z_match=1`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block62_compact_source_kprime_identifiability_obstruction.py
python3 scripts/frontier_yt_pr230_block62_compact_source_kprime_identifiability_obstruction.py
# SUMMARY: PASS=11 FAIL=0
```
