# PR230 Key-Blocker Closure Attempt Note

**Date:** 2026-05-01  
**Status:** open / key blocker not closed  
**Runner:** `scripts/frontier_yt_key_blocker_closure_attempt.py`  
**Certificate:** `outputs/yt_key_blocker_closure_attempt_2026-05-01.json`

## Purpose

This note records the direct closure attempt on the narrowed PR #230 blocker.
The previous physics-loop passes reduced the analytic Ward repair to one
question:

```text
Can the current Cl(3)/Z^3 surface derive the scalar source two-point pole
residue and the relative scalar/gauge dressing needed to convert the
Ward/source coefficient into a physical top-Yukawa readout?
```

## Candidate Authorities Tested

The runner checks the current repo surfaces that could plausibly close that
question:

| Candidate family | Ledger status where present | Result |
|---|---|---|
| old Ward / `H_unit` route | `audited_renaming` | computes the `1/sqrt(6)` overlap, not the physical readout |
| `R_conn` / color projection | `audited_conditional` | channel arithmetic, not a pole-residue theorem |
| source-Higgs Legendre / SSB bridge | local PR #230 artifact | SSB bookkeeping only; leaves `kappa_H` open |
| source-Higgs `kappa_H` obstruction | local PR #230 artifact | proves counts + SSB do not select `kappa_H` |
| scalar LSZ bridge | local PR #230 artifact | proves `R_conn` alone is not scalar LSZ |
| common dressing obstruction | local PR #230 artifact | proves current Ward/gauge identities do not force common dressing |
| one-Higgs selector | `proposed_retained` | selects operator pattern, not coefficient/residue |
| EW Higgs mass diagonalization | `proposed_retained` | uses canonical Higgs convention, not composite/source residue |
| taste scalar isotropy | `audited_conditional` | direction/isotropy data, not pole residue |
| neutrino scalar two-point analogue | support | not a top-sector residue or dressing theorem |

## Runner Result

```text
python3 scripts/frontier_yt_key_blocker_closure_attempt.py
# SUMMARY: PASS=14 FAIL=0
```

The runner found no candidate that closes both required pieces:

1. source-selected scalar pole residue / `Z_phi` / `kappa_H`;
2. relative scalar/gauge dressing.

It also found no retained authority that closes the blocker.

## Required Closure Theorem

The analytic route still needs a theorem with this content:

```text
Construct C_OO(p) for the source-selected scalar operator O on the retained
Cl(3)/Z^3 Wilson-staggered action, prove that it has the physical Higgs-carrier
pole used by the Yukawa readout, compute or bound the pole residue Z_phi and
the source-to-canonical factor kappa_H, and derive or independently measure the
scalar/gauge dressing ratio.
```

Only after that theorem exists can the Ward/source coefficient be mapped to a
physical `y_t/g_s` readout without re-entering the `H_unit` matrix-element
definition trap.

## Honest PR #230 Consequence

PR #230 does not yet have retained top-Yukawa closure.  The two remaining
honest closure routes are:

1. derive the scalar two-point pole-residue/common-dressing theorem above;
2. produce a strict direct-correlator measurement certificate at a physically
   suitable top/heavy-quark scale.

This note does not promote the Ward theorem, does not define `y_t_bare` by an
`H_unit` matrix element, does not use observed `m_t` or `y_t` as inputs, and
does not certify production measurement.
