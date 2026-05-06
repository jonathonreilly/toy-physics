# Source-Higgs Gram-Purity Contract Witness

**Status:** exact-support / contract witness; current rows absent  
**Runner:** `scripts/frontier_yt_source_higgs_gram_purity_contract_witness.py`  
**Certificate:** `outputs/yt_source_higgs_gram_purity_contract_witness_2026-05-03.json`

## Purpose

The selected source-Higgs route now has an executable builder and
postprocessor.  This witness tests that acceptance surface without writing a
production row file.

It builds four in-memory candidates:

- a fully firewalled future pure candidate with
  `Res(C_ss)=4`, `Res(C_sH)=6`, and `Res(C_HH)=9`;
- a mixed orthogonal candidate with the same `C_ss` and `C_HH` but
  `Res(C_sH)=3`;
- a forbidden-import candidate that sets the Ward-authority firewall bad;
- a pure candidate that lacks retained-route authorization.

The postprocessor accepts only the first in-memory candidate.

The witness also now requires the PR230 genuine source-pole artifact intake:
`O_sp` must be present as same-surface source-side support, must remain
non-closing by itself, and must not be identified with canonical `O_H`.

## Validation

```text
python3 scripts/frontier_yt_source_higgs_gram_purity_contract_witness.py
# SUMMARY: PASS=13 FAIL=0
```

The witness also confirms that the current surface remains open: the real
source-Higgs builder has no rows, the O_sp-Higgs postprocessor is awaiting a
production certificate, the canonical-Higgs operator certificate is absent,
and the retained-route certificate is open.

## Claim Boundary

This is schema and acceptance-surface support only.  It does not write
production `O_H/C_sH/C_HH` pole rows, does not define `O_H`, does not use
`H_unit`, static EW algebra, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0`, and does not authorize retained or
`proposed_retained` top-Yukawa closure.

The next action is unchanged: supply a real same-surface canonical-Higgs
operator certificate plus production `C_sH/C_HH` pole residues, then rerun the
builder, postprocessor, and retained-route certificate.
