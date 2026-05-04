# PR #230 O_sp/O_H Literature Bridge Note

**Status:** bounded-support / literature bridge; no current-surface closure import

## Purpose

This note records the targeted literature pass for the active PR #230
source-pole-to-canonical-Higgs blocker.  The question was not whether external
papers can prove `O_sp = O_H` for the Cl(3)/Z3 substrate; they cannot be
load-bearing proof authority on the current PR surface.  The useful question
was whether the literature identifies a concrete route shape worth
implementing next.

## Sources Checked

- [Sondenheimer, arXiv:1912.08680](https://arxiv.org/abs/1912.08680):
  FMS-style gauge-invariant composite Higgs operators can be related to
  remaining gauge-fixed objects after the gauge-Higgs system is supplied.
- [Maas and Sondenheimer, arXiv:2009.06671](https://arxiv.org/abs/2009.06671):
  FMS gives a gauge-invariant bound-state Higgs description whose pole
  structure can match the elementary-Higgs description in the appropriate
  expansion.
- [Martins et al., arXiv:2603.12882](https://arxiv.org/abs/2603.12882):
  recent lattice weak/Higgs work uses gauge-invariant FMS-connected
  observables as the lattice-facing language.
- [Blossier et al., arXiv:0902.1265](https://arxiv.org/abs/0902.1265):
  GEVP/correlation-matrix methods are standard for extracting energies and
  matrix elements from lattice operator bases.
- [Feynman-Hellmann transition matrix elements, arXiv:2305.05491](https://arxiv.org/abs/2305.05491):
  background-field/Feynman-Hellmann methods support source-response matrix
  element extraction.
- [Das, Francisco, Frenkel, arXiv:1308.5127](https://arxiv.org/abs/1308.5127):
  Nielsen-identity methods are useful pole/gauge-dependence guardrails, but
  not source-overlap theorems.

## Result

The literature does not close PR #230.  It does identify a sharper future
implementation route:

1. Build a same-surface gauge-invariant, FMS-inspired canonical-Higgs operator
   certificate for `O_H`.
2. Use a correlation matrix, not a single asserted row:
   `C_ss`, `C_sH`, `C_HH`, and any needed auxiliary operator rows.
3. Extract a nondegenerate isolated-pole residue matrix with GEVP or an
   equivalent pole-residue analysis.
4. Feed those rows into the existing source-Higgs builder and O_sp-normalized
   Gram-purity postprocessor.

## Non-Claim

This is methodology context only.  It does not import an external FMS theorem
as a PR #230 `O_H` certificate, does not identify the Cl(3)/Z3 scalar source
with the canonical Higgs field, and does not authorize retained or
proposed-retained top-Yukawa closure.

## Verification

Run:

```bash
python3 scripts/frontier_yt_osp_oh_literature_bridge.py
```

Expected current result:

```text
SUMMARY: PASS=13 FAIL=0
```
