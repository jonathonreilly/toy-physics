# PR230 Block58 Compact Source-Channel Spectral Support Gate

**Status:** exact-support / finite-volume compact source-channel spectral
support, with thermodynamic pole/FVIR and canonical-Higgs roots still open  
**Runner:** `scripts/frontier_yt_pr230_block58_compact_source_spectral_support_gate.py`  
**Certificate:** `outputs/yt_pr230_block58_compact_source_spectral_support_gate_2026-05-12.json`

## Claim

Block57 established the exact compact finite-volume source functional as a
support foundation.  This block adds the next finite-volume step: on the
current reflection-positive Cl(3)/Z3 surface, the compact scalar-source channel
has a positive finite-volume spectral representation.

Load-bearing parent surfaces:

- [Block57 compact source-functional foundation](YT_PR230_BLOCK57_COMPACT_SOURCE_FUNCTIONAL_FOUNDATION_GATE_NOTE_2026-05-12.md)
- [Axiom-first reflection positivity theorem](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- [Axiom-first spectrum condition theorem](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md)
- [Reflection-positivity LSZ shortcut no-go](YT_REFLECTION_POSITIVITY_LSZ_SHORTCUT_NO_GO_NOTE_2026-05-02.md)
- [Source-functional LSZ identifiability theorem](YT_SOURCE_FUNCTIONAL_LSZ_IDENTIFIABILITY_THEOREM_NOTE_2026-05-03.md)

The finite-volume source-channel statement is:

```text
C_ss(t) = sum_{n>0} |<0|O_s|n>|^2 exp(-(E_n - E_0)t)
```

with nonnegative spectral weights for the connected source correlator.  This
is the right support object for future pole work.

## Boundary

This does not close PR230.  The existing reflection-positivity LSZ shortcut
no-go still applies: positive spectral representation alone does not determine
pole saturation, a pole residue interval, the thermodynamic/FVIR limiting
order, or canonical `O_H` identity.

The current support says:

```text
exact compact finite-volume source functional
+ reflection-positive transfer matrix
=> finite-volume positive source-channel spectral sum
```

The missing theorem remains:

```text
finite-volume positive spectral sum
=> thermodynamic scalar pole/residue with FVIR control
=> canonical O_H/source-overlap or strict physical response bridge
```

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not treat reflection positivity as pole saturation.  It does not infer
a thermodynamic scalar mass gap or isolated pole from a finite-volume transfer
spectrum.  It does not identify `O_s` or the LSZ-normalized source-pole
operator with canonical `O_H`.

It does not use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed top/Yukawa
values, `alpha_LM`, plaquette/`u0`, `kappa_s=1`, `c2=1`, or `Z_match=1`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block58_compact_source_spectral_support_gate.py
python3 scripts/frontier_yt_pr230_block58_compact_source_spectral_support_gate.py
# SUMMARY: PASS=13 FAIL=0
```

