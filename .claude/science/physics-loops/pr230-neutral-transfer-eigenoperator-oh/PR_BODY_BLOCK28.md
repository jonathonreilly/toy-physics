## [physics-loop] PR230 block28 exact-support

Block28 adds a degree-one `O_H` support intake checkpoint for draft PR #230.

Artifacts:

- `scripts/frontier_yt_pr230_block28_degree_one_oh_support_intake_checkpoint.py`
- `docs/YT_PR230_BLOCK28_DEGREE_ONE_OH_SUPPORT_INTAKE_CHECKPOINT_NOTE_2026-05-11.md`
- `outputs/yt_pr230_block28_degree_one_oh_support_intake_checkpoint_2026-05-11.json`
- refreshed `scripts/frontier_yt_pr230_campaign_status_certificate.py`
- refreshed `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`
- updated loop pack under `.claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/`

Result:

- The committed degree-one radial-tangent `O_H` theorem is consumed as exact support: if a future same-surface EW/Higgs action proves canonical `O_H` is a linear Z3-covariant radial tangent, the unique axis is the implemented taste-radial source.
- Current surface remains open: the action premise, canonical `O_H`, strict `C_ss/C_sH/C_HH` pole rows, Gram/FV/IR authority, W/Z accepted-action response packet, and neutral H3/H4 authority are absent.
- `proposal_allowed=false`; no retained or `proposed_retained` wording is authorized.
- No live chunk worker output was touched or inspected.

Verification:

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block28_degree_one_oh_support_intake_checkpoint.py scripts/frontier_yt_pr230_degree_one_radial_tangent_oh_theorem.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_degree_one_radial_tangent_oh_theorem.py
# SUMMARY: PASS=14 FAIL=0
python3 scripts/frontier_yt_pr230_block28_degree_one_oh_support_intake_checkpoint.py
# SUMMARY: PASS=13 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=362 FAIL=0
```

Next:

Supply an accepted same-surface EW/Higgs action or canonical `O_H` certificate that makes the degree-one radial tangent premise current-surface authority, then produce strict `C_ss/C_sH/C_HH` pole rows with Gram/FV/IR checks. If unavailable, pivot to strict W/Z matched physical-response rows with accepted action, matched covariance, strict non-observed `g2`, `delta_perp`, and final W-response authority.
