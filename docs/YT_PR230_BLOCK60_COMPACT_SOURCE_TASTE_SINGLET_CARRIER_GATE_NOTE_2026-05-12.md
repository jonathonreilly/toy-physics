# PR230 Block60 Compact Source Taste-Singlet Carrier Gate

**Status:** exact-support / compact additive source fixes the source-channel
taste-singlet carrier coordinate; canonical `O_H`, pole residue, `K'(pole)`,
and threshold/FVIR authority remain open  
**Runner:** `scripts/frontier_yt_pr230_block60_compact_source_taste_singlet_carrier_gate.py`  
**Certificate:** `outputs/yt_pr230_block60_compact_source_taste_singlet_carrier_gate_2026-05-12.json`

## Claim

The compact additive scalar source fixes the source-channel taste carrier.
For the staggered source shift

```text
D_KS(m) -> D_KS(m+s)
```

the source derivative couples to the unnormalized taste-singlet local scalar
sum

```text
O_s = sum_{taste=1}^{16} psi_taste^\dagger psi_taste.
```

Equivalently,

```text
O_1 = O_s / sqrt(16)
```

is the unit taste singlet, and the additive source coordinate couples to it
with the fixed source-coordinate factor `sqrt(16)=4`.

## Boundary

This is source-channel support only.  It does not identify the source taste
singlet with canonical `O_H`, does not supply scalar LSZ residue authority,
does not derive `K'(pole)`, and does not provide threshold/FVIR/contact
control.  It preserves the previous taste-normalization no-gos: unit
taste-singlet normalization removes the finite ladder crossings, and the
factor can still be moved between source coordinate and operator unless a
canonical Higgs normalization or physical response bridge is supplied.

## Parent Surface

- [Block57 compact source-functional foundation](YT_PR230_BLOCK57_COMPACT_SOURCE_FUNCTIONAL_FOUNDATION_GATE_NOTE_2026-05-12.md)
- [Block58 compact source-channel spectral support](YT_PR230_BLOCK58_COMPACT_SOURCE_SPECTRAL_SUPPORT_GATE_NOTE_2026-05-12.md)
- [Scalar taste-projector normalization theorem attempt](YT_SCALAR_TASTE_PROJECTOR_NORMALIZATION_ATTEMPT_NOTE_2026-05-01.md)
- [Taste-singlet ladder normalization boundary](YT_TASTE_SINGLET_LADDER_NORMALIZATION_BOUNDARY_NOTE_2026-05-01.md)
- [Scalar carrier/projector closure attempt](YT_SCALAR_CARRIER_PROJECTOR_CLOSURE_ATTEMPT_NOTE_2026-05-02.md)

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not set `kappa_s=1`, `c2=1`, or `Z_match=1`.  It does not use
`H_unit`, `yt_ward_identity`, `y_t_bare`, observed top/Yukawa values,
`alpha_LM`, plaquette, or `u0`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block60_compact_source_taste_singlet_carrier_gate.py
python3 scripts/frontier_yt_pr230_block60_compact_source_taste_singlet_carrier_gate.py
# SUMMARY: PASS=11 FAIL=0
```
