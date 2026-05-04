# PR #230 SM One-Higgs To O_H Import Boundary

```yaml
actual_current_surface_status: exact negative boundary / SM one-Higgs gauge selection is not PR230 O_H identity
proposal_allowed: false
bare_retained_allowed: false
```

This block closes a tempting O_H shortcut.  The SM one-Higgs gauge-selection
theorem proves the allowed one-doublet Yukawa monomial pattern, and its runner
now passes on the current note status:

```bash
python3 scripts/frontier_sm_one_higgs_yukawa_gauge_selection.py
# TOTAL: PASS=43, FAIL=0
```

That support does not identify the PR230 scalar source or source-pole operator
with the canonical Higgs radial operator.  The theorem assumes canonical `H`
after it is supplied, leaves the numerical Yukawa matrices free, and supplies
no `C_sH/C_HH` pole residues, no `O_sp = O_H` identity, and no selection rule
removing orthogonal neutral scalar top couplings.

## Verification

```bash
python3 scripts/frontier_yt_sm_one_higgs_oh_import_boundary.py
# SUMMARY: PASS=11 FAIL=0
```

## Claim Boundary

This does not claim retained or `proposed_retained` top-Yukawa closure.  It
does not define `O_H` by one-Higgs notation, does not identify `O_sp` with
`O_H`, does not set the orthogonal scalar top coupling to zero, and does not
use `H_unit`, `yt_ward_identity`, observed target values, `alpha_LM`,
plaquette, or `u_0`.

Positive closure still requires certified `O_H/C_sH/C_HH` pole rows, a
genuine rank-one neutral-scalar theorem, a same-source W/Z response harness,
or honest production evidence.
