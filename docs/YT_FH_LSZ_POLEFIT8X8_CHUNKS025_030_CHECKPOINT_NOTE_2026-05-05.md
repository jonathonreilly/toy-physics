# PR #230 FH/LSZ Polefit8x8 Chunks025-030 Checkpoint

Status: bounded production support only.

Chunks025-030 of the separate L12/T24 eight-mode/x8 FH/LSZ pole-fit stream
completed with fixed seeds `2026051925` through `2026051930`, selected mass
`0.75`, eight scalar two-point momentum modes, x8 noise, and isolated
production output directories.

The dedicated polefit8x8 combiner now audits `30/63` ready chunks and writes
the combined diagnostic support surface:

```text
python3 scripts/frontier_yt_fh_lsz_polefit8x8_chunk_combiner_gate.py
# SUMMARY: PASS=6 FAIL=0
```

The postprocessor consumes that combined surface and records a finite-shell
diagnostic fit with `480` saved configurations:

```text
python3 scripts/frontier_yt_fh_lsz_polefit8x8_postprocessor.py
# SUMMARY: PASS=5 FAIL=0
```

Because the combined rows changed, the scalar-LSZ shortcut diagnostics were
rerun.  The current `C_ss(q_hat^2)` proxy still fails necessary Stieltjes
monotonicity, with adjacent violations now at least `76.267 sigma`; finite-row
contact-subtraction restoration remains non-identifying, with representative
contact choices shifting the max-q residual by `2653.846` row standard errors.

This checkpoint is not retained or proposed-retained top-Yukawa closure.  The
stream remains a partial L12 support surface and still lacks the complete L12
target, L16/L24 finite-volume scaling, FV/IR and zero-mode control,
pole-saturation/model-class authority, a same-surface contact-subtraction or
denominator theorem, and the canonical-Higgs/source-overlap bridge.  It also
does not set `kappa_s`, `c2`, `Z_match`, or any source/Higgs overlap to one,
and it does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0` as proof authority.

Aggregate gates after packaging remain open:

```text
python3 scripts/frontier_yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_fh_lsz_contact_subtraction_identifiability.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=187 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=213 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=38 FAIL=0

python3 scripts/frontier_yt_pr230_non_chunk_closure_worklist.py
# SUMMARY: PASS=19 FAIL=0
```

Next action: continue the polefit8x8 stream only after a fresh global
production collision guard allows capacity, or pivot to the non-chunk closure
routes: same-surface `O_H/C_sH/C_HH` rows, real W/Z response rows with
strict `g2` and identity certificates, Schur `A/B/C` rows, a rank-one
neutral-scalar theorem, or a same-surface scalar contact/denominator theorem.
