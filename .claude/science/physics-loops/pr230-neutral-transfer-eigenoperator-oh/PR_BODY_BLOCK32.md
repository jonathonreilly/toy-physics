## 2026-05-12 complete-packet promotion-contract refresh

This checkpoint refreshes the taste-radial-to-source-Higgs promotion contract
after the chunk063 final package.

What changed:

- `scripts/frontier_yt_pr230_taste_radial_to_source_higgs_promotion_contract.py`
  now requires the completed finite packet rather than the old partial-packet
  state;
- the certificate records `ready_chunks=63`, `expected_chunks=63`,
  `combined_rows_written=true`, `complete_packet=true`, and
  `current_promotion_allowed=false`;
- the paired note and loop pack now state that finite `C_sx/C_xx` production
  is complete and no longer a closure path by itself.

Validation:

- promotion contract: `PASS=11 FAIL=0`;
- full positive closure assembly: `PASS=163 FAIL=0`;
- retained closure route certificate: `PASS=317 FAIL=0`;
- positive closure completion audit: `PASS=72 FAIL=0`;
- campaign status certificate: `PASS=364 FAIL=0`.

Claim boundary: this is exact support for the promotion rule only.  The
complete finite `C_sx/C_xx` packet is not canonical `C_sH/C_HH` evidence until
same-surface `x=canonical O_H` identity/action/LSZ authority, strict
source-Higgs pole rows, Gram/FV/IR authority, and aggregate proposal gates
exist.  No retained or `proposed_retained` closure is claimed; PR #230 remains
draft/open.
