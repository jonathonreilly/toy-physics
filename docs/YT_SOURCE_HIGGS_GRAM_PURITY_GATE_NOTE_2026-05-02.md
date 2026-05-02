# PR #230 Source-Higgs Gram Purity Gate

**Status:** open / source-Higgs Gram purity gate not passed
**Runner:** `scripts/frontier_yt_source_higgs_gram_purity_gate.py`
**Certificate:** `outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json`

## Purpose

This note makes the future `C_sH` route executable.  If a canonical Higgs
radial operator `H` is supplied on the same source surface, then pole-level
residues of `C_ss`, `C_sH`, and `C_HH` can certify source-pole purity.

## Gate

At the isolated pole:

```text
Delta = Res(C_ss) Res(C_HH) - Res(C_sH)^2
rho_sH = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH))
```

The purity gate requires `Delta = 0` and `|rho_sH| = 1`.  A positive Gram
determinant detects an orthogonal component in the source pole.

## Current Result

The algebraic gate is valid as an acceptance condition, but it is not passed
on the current PR surface.  The branch has no canonical-Higgs source operator,
no `C_sH` pole cross residue, and no `C_HH` pole residue.  The source-Higgs
cross-correlator import audit confirms those objects are not hidden in the
current harness or EW/SM Higgs notes.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not define canonical `H` by fiat, does not set `kappa_s = 1`, and does
not treat missing `C_sH` / `C_HH` data as evidence.

## Next Action

Implement or derive the canonical-Higgs operator and `C_sH` / `C_HH` pole
residue measurements, or pivot to same-source W/Z response, sector-overlap
equality, or FH/LSZ production chunk processing.
