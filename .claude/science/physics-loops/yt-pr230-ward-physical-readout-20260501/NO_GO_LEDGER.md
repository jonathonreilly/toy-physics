# No-Go Ledger

## Current Block

The current repo does not already contain an audit-retained top-Yukawa proof.

```text
scripts/frontier_yt_pr230_global_proof_audit.py
# SUMMARY: PASS=9 FAIL=0
```

The Ward repair is not closed on the current audit surface.  The missing pieces
are source/HS normalization, chirality selector, physical scalar carrier,
scalar LSZ leg, absence of extra factors, and common dressing.

```text
scripts/frontier_yt_ward_physical_readout_repair_audit.py
# SUMMARY: PASS=12 FAIL=0
```

Counts plus SSB do not select `kappa_H = 1`:

```text
scripts/frontier_yt_source_higgs_kappa_residue_obstruction.py
# SUMMARY: PASS=7 FAIL=0
```

The scalar two-point residue / LSZ normalization remains a real open theorem,
not bookkeeping.

`R_conn = 8/9` does not by itself derive the scalar pole residue:

```text
scripts/frontier_yt_scalar_lsz_residue_bridge.py
# SUMMARY: PASS=6 FAIL=0
```

The existing color-projection rows remain `audited_conditional`.

The chirality/right-handed selector is conditionally supported but not clean
because its parents are non-clean:

```text
scripts/frontier_yt_chirality_selector_bridge.py
# SUMMARY: PASS=8 FAIL=0
```

Common dressing is not enforced by current Ward/gauge identities:

```text
scripts/frontier_yt_common_dressing_obstruction.py
# SUMMARY: PASS=6 FAIL=0
```

The full current analytic surface underdetermines the physical readout:

```text
scripts/frontier_yt_scalar_pole_residue_current_surface_no_go.py
# SUMMARY: PASS=7 FAIL=0
```

Retained closure is not currently reached:

```text
scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=9 FAIL=0
```

The direct key-blocker closure attempt checked Ward/H_unit, R_conn/color
projection, source-Higgs/SSB, kappa, LSZ, common dressing, one-Higgs selection,
EW Higgs kinetic normalization, taste-scalar isotropy, and the neutrino scalar
two-point analogue.  No current candidate derives both scalar pole residue and
relative scalar/gauge dressing:

```text
scripts/frontier_yt_key_blocker_closure_attempt.py
# SUMMARY: PASS=14 FAIL=0
```

## Inherited No-Gos And Boundaries

- `YT_TOP_MASS_SUBSTRATE_PIN_NO_GO_NOTE_2026-04-30.md`: no direct substrate
  mass pin for top from the previously tested non-MC routes.
- `YT_TOP_MASS_WARD_DECOMP_NO_GO_NOTE_2026-04-30.md`: Ward decompositions
  reproduce the old obstruction unless the physical scalar/readout map is
  independently derived.
- `YT_BETA_LAMBDA_PLANCK_STATIONARITY_NO_GO_NOTE_2026-05-01.md`:
  `lambda(M_Pl)=0` does not imply `beta_lambda(M_Pl)=0`; the Planck selector
  route remains conditional.
- Direct correlator route: physically honest but needs production compute and
  cannot be certified by reduced-scope runs.
