## Block105 W/Z Probe Refresh

Maintenance-only checkpoint for PR #230.

What changed:

- Updated the W/Z row-production and W/Z mass-fit path gates so they recognize
  the current production harness W/Z absent guard after the selected-mass /
  normal-cache optimization.
- Tightened the probe distinction between default-off synthetic W/Z smoke
  schema plumbing and a genuine W/Z correlator mass-fit path.

Validation:

```text
frontier_yt_wz_response_row_production_attempt.py PASS=12 FAIL=0
frontier_yt_wz_correlator_mass_fit_path_gate.py PASS=17 FAIL=0
py_compile PASS
full positive closure assembly PASS=200 FAIL=0
retained route PASS=325 FAIL=0
positive closure completion audit PASS=79 FAIL=0
campaign status PASS=427 FAIL=0
assumption/import stress PASS=111 FAIL=0
audit pipeline PASS with 5 existing warnings
strict audit lint PASS with 5 existing warnings
git diff --check PASS
```

No closure statement:

PR #230 remains open/draft.  This does not create W/Z production rows, does not
promote smoke rows, does not supply `O_H`, `C_sH/C_HH`, Schur pole authority,
neutral H3/H4 transfer authority, strict `g2`, or retained/proposed-retained
top-Yukawa closure.

