# PR230 Additive-Source / Radial-Spurion Incompatibility Gate

**Status:** exact support/boundary / current additive source is incompatible
with accepted radial-spurion action closure

**Runner:** `scripts/frontier_yt_pr230_additive_source_radial_spurion_incompatibility.py`

**Certificate:** `outputs/yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json`

```yaml
actual_current_surface_status: exact support/boundary / current additive source is incompatible with accepted radial-spurion action closure
conditional_surface_status: exact-support for a future accepted action if the independent additive top source is removed or separately measured/subtracted
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

This block attacks the shared canonical `O_H` / accepted EW-Higgs action root
directly.  The tempting shortcut is:

```text
keep current PR230 top FH/LSZ additive source S_top[m+s]
+ add EW/Higgs source term s sum_x O_H(x)
+ say the same coordinate s is now the accepted same-source action
```

That is not enough.

The W/Z response route needs `s` to be a single canonical-Higgs radial
spurion.  In that case top, W, and Z masses respond only through one branch
`v(s)`:

```text
m_t(s) = y_t v(s) / sqrt(2)
M_W(s) = g2 v(s) / 2
```

and the unknown `dv/ds` cancels in

```text
y_t = g2 (dm_t/ds) / (sqrt(2) dM_W/ds).
```

If the current additive top source remains, the source derivative is not
canonical `O_H` alone:

```text
dS/ds = O_top_additive + O_H.
```

Then

```text
dm_t/ds = y_t (dv/ds) / sqrt(2) + a_top,
```

while `dM_W/ds = g2 (dv/ds) / 2`.  The inferred response-ratio value depends
on the independent additive slope `a_top`.

## Result

The runner checks both sides:

- in the pure radial-spurion witness with `a_top = 0`, the top/W response
  formula recovers the input `y_t`;
- in the current-risk witness with an independent additive top slope, the
  inferred value changes as `a_top` varies;
- the current same-source EW/Higgs ansatz contains both the existing additive
  top source and the Higgs composite source under the same coordinate;
- existing PR230 gates still reject the accepted action certificate, sector
  overlap identity, source-Higgs pole rows, and aggregate closure.

So the shared root is now sharper:

1. replace the current additive source by a true same-surface radial-spurion
   action;
2. or measure/subtract the independent additive top component with row-level
   authority;
3. or bypass W/Z response by supplying canonical `O_H` plus
   `C_ss/C_sH/C_HH` pole rows directly.

## Load-Bearing Dependencies

- [YT_PR230_SAME_SOURCE_EW_HIGGS_ACTION_ANSATZ_GATE_NOTE_2026-05-06.md](YT_PR230_SAME_SOURCE_EW_HIGGS_ACTION_ANSATZ_GATE_NOTE_2026-05-06.md)
- [YT_PR230_SAME_SOURCE_EW_ACTION_ADOPTION_ATTEMPT_NOTE_2026-05-06.md](YT_PR230_SAME_SOURCE_EW_ACTION_ADOPTION_ATTEMPT_NOTE_2026-05-06.md)
- [YT_PR230_RADIAL_SPURION_SECTOR_OVERLAP_THEOREM_NOTE_2026-05-06.md](YT_PR230_RADIAL_SPURION_SECTOR_OVERLAP_THEOREM_NOTE_2026-05-06.md)
- [YT_PR230_RADIAL_SPURION_ACTION_CONTRACT_NOTE_2026-05-06.md](YT_PR230_RADIAL_SPURION_ACTION_CONTRACT_NOTE_2026-05-06.md)
- [YT_PR230_CANONICAL_OH_WZ_COMMON_ACTION_CUT_NOTE_2026-05-07.md](YT_PR230_CANONICAL_OH_WZ_COMMON_ACTION_CUT_NOTE_2026-05-07.md)
- [YT_PR230_SOURCE_HIGGS_POLE_ROW_ACCEPTANCE_CONTRACT_NOTE_2026-05-06.md](YT_PR230_SOURCE_HIGGS_POLE_ROW_ACCEPTANCE_CONTRACT_NOTE_2026-05-06.md)

## Non-Claims

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not write or validate an accepted EW/Higgs action certificate.  It
does not identify the current additive top source with canonical `O_H`, does
not relabel `C_sx/C_xx` as `C_sH/C_HH`, does not use `H_unit`,
`yt_ward_identity`, observed targets, `alpha_LM`, plaquette, `u0`, or unit
normalization conventions, and does not touch the live chunk worker.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_additive_source_radial_spurion_incompatibility.py
python3 scripts/frontier_yt_pr230_additive_source_radial_spurion_incompatibility.py
# SUMMARY: PASS=15 FAIL=0
```
