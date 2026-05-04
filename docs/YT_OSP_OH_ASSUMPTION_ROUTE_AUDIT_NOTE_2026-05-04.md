# PR #230 O_sp/O_H Assumption-Route Audit Note

**Status:** open / assumption-route audit complete; retained closure still blocked

## Purpose

This note records the current physics-loop assumption exercise for the active
PR #230 blocker:

```text
Legendre/LSZ source-pole operator O_sp  ->  canonical Higgs radial operator O_H
```

The runner `scripts/frontier_yt_osp_oh_assumption_route_audit.py` verifies that
the loop pack and paired certificates keep the allowed support statements,
forbidden shortcuts, and remaining positive routes separated.  It is not a
top-Yukawa derivation and it does not authorize retained or proposed-retained
wording.

## What Is Allowed

The current surface allows the following as support:

- `O_sp` from the Legendre/LSZ source-pole construction.
- The isolated-pole Gram-factorization theorem as exact support for a future
  source-Higgs pole-residue test.
- The source-Higgs Gram-purity contract witness as an executable future
  acceptance surface.
- W/Z response, Schur K-prime, and neutral-sector rank-one gates as future
  route contracts or support.
- In-progress FH/LSZ chunks as bounded production support only.

## What Is Forbidden As Closure

The audit explicitly rejects:

- `H_unit` or the old Ward matrix-element readout.
- Observed `m_t`, observed `y_t`, observed W/Z values, or PDG comparators as
  selectors.
- Setting `kappa_s = 1` or `cos(theta) = 1` without deriving or measuring it.
- Treating static EW gauge-mass algebra as a same-surface `O_H` operator.
- Promoting finite Schur support into same-surface `A/B/C` neutral kernel rows.
- Importing gauge Perron/reflection positivity as neutral-sector
  irreducibility.
- Treating default-off guards, contracts, or reduced pilots as production
  evidence.

## Current Route Matrix

| Route | Current status | Missing premise |
|---|---|---|
| Source-Higgs Gram purity | support contract only | certified `O_H` plus production `C_sH/C_HH` pole residues |
| Same-source W/Z response | path absent | same-source EW action, W/Z correlator mass fits, sector-overlap identity |
| Schur K-prime rows | exact negative boundary | same-surface `A/B/C` neutral scalar kernel rows |
| Neutral scalar rank one | exact negative boundary | neutral-sector irreducibility / positivity improvement |
| FH/LSZ chunks | bounded production support | response-window acceptance and `O_H`/source-overlap closure |

## Non-Claim

This artifact does not derive `O_sp = O_H`, does not compute a physical
`y_t`, does not promote PR #230, and does not change the theorem status.  The
status remains open until one real missing premise is supplied and the retained
route certificate authorizes a proposal.

## Verification

Run:

```bash
python3 scripts/frontier_yt_osp_oh_assumption_route_audit.py
```

Expected current result:

```text
SUMMARY: PASS=18 FAIL=0
```
