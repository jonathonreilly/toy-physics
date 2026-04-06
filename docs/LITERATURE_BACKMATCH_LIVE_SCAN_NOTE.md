# Literature Backmatch Live Scan Note

**Date:** 2026-04-06  
**Status:** one bounded retrospective backmatch candidate identified; resemblance only, not validation

## Scope

This note is the live literature backmatch pass for the retained query pack in
[`docs/EXPERIMENT_BACKMATCH_QUERY_PACK_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/EXPERIMENT_BACKMATCH_QUERY_PACK_NOTE.md).
The goal is not to prove prior validation. The goal is to identify at most one
credible published outcome that lines up with a retained prediction and to keep
the distinction between resemblance and verification explicit.

## Method

I searched for a candidate that matches the strongest diamond-facing retained
prediction:

- phase-sensitive readout
- lock-in `I/Q` style quadratures
- per-pixel or spatially resolved phase behavior
- dynamic rather than purely static imaging

The best match I found is a published widefield NV lock-in microscopy result.

## Top Candidate

### Sub-second temporal magnetic field microscopy using quantum defects in diamond

PubMed source:
[`https://pubmed.ncbi.nlm.nih.gov/35610314/`](https://pubmed.ncbi.nlm.nih.gov/35610314/)

Why it is the best retrospective match:

- it uses widefield diamond NV magnetometry
- it performs lock-in detection of NV photoluminescence across multiple pixels
- it explicitly forms in-phase and quadrature images
- it is dynamic, not only static
- it provides a clean experimental precedent for the kind of phase-sensitive
  bridge card we want for the diamond lane

The key abstract-level facts are:

- lock-in detection of NV PL is done simultaneously over multiple pixels
- frequency-modulated NV emission is synchronized with camera demodulation
- the protocol produces in-phase and quadrature images
- the technique images sub-second varying magnetic processes

## Why It Matches

The retained diamond prediction lane is not an absolute-force claim. It is a
phase-sensitive discriminator lane:

- raw `X` / `Y`
- `phi`
- phase-ramp slope
- sign and quadrature behavior under a controlled drive

This paper is a good retrospective backmatch because it already lives in the
same measurement family:

- lock-in readout
- quadrature decomposition
- pixel-resolved dynamic response

That makes it a strong analog for the bridge card, even though the target
physics is different.

## Why It Does Not Validate Our Claim

This is only resemblance, not confirmation.

The published experiment measures dynamic magnetic imaging in diamond NVs.
It does not test our retained gravitational or causal-field observables.
It does not establish our `Y`, `phi`, or phase-ramp prediction for the
retained physics model.

So the correct read is:

- good analog-platform backmatch
- useful for experiment framing
- not evidence that our prediction is already true

## Practical Use

This candidate is useful because it gives us a concrete shortcut for the next
diamond-facing search:

- look for a calibration path from proxy `X/Y/phi` to actual readout units
- look for an absolute phase/noise floor in lock-in NV imaging
- keep the bridge card in the same per-pixel, quadrature-based language

## Final Verdict

**Credible retrospective backmatch candidate found: a widefield NV lock-in
microscopy paper with per-pixel `I/Q` readout and dynamic imaging. It is a
strong analog for the diamond phase-ramp bridge, but it is not validation of
our retained prediction.**
