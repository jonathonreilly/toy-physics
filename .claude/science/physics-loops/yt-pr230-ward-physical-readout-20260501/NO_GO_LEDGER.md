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

The scalar source two-point stretch attempt derives the exact logdet curvature
as a fermion bubble but shows the free Wilson-staggered residue proxy is not
universal or selected to one:

```text
scripts/frontier_yt_scalar_source_two_point_stretch.py
# SUMMARY: PASS=12 FAIL=0
```

The required stuck fan-out rejects the finite-volume near-match shortcut,
identifies the HS/RPA pole equation as the only constructive analytic successor,
and keeps direct measurement as the empirical route:

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_scalar_residue_stuck_fanout.py
# SUMMARY: PASS=6 FAIL=0
```

The HS/RPA contact route is not closed by `A_min`; a contact coupling `G` is an
extra scalar-channel input unless derived from the Wilson gauge ladder:

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_hs_rpa_pole_condition_attempt.py
# SUMMARY: PASS=9 FAIL=0
```

The finite scalar-channel ladder scout builds the next route's kernel shape,
but its pole criterion is sensitive to mass, scalar projector, IR regulator,
and finite-volume treatment:

```text
python3 scripts/frontier_yt_scalar_ladder_kernel_scout.py
# SUMMARY: PASS=6 FAIL=0
```

The full-staggered PT formula layer can supply `D_psi`, `D_gluon`, and the
shared scalar/gauge kinematic factor, but it cannot be used wholesale because
the same runner also carries old alpha/plaquette/H_unit surfaces that are
forbidden as PR #230 proof inputs:

```text
python3 scripts/frontier_yt_scalar_ladder_kernel_input_audit.py
# SUMMARY: PASS=9 FAIL=0
```

The scalar ladder pole criterion is not invariant under scalar
projector/source normalization.  Raw versus zero-momentum-normalized
point-split scalar choices differ by a factor of 16 and can flip
`lambda_max >= 1`:

```text
python3 scripts/frontier_yt_scalar_ladder_projector_normalization_obstruction.py
# SUMMARY: PASS=6 FAIL=0
```

The HQET/static direct route removes the numerical `am_top >> 1` cutoff by
rephasing away the absolute heavy rest mass.  The normalized static correlator
therefore cannot determine the absolute top mass or `y_t` without an additive
mass and lattice-HQET-to-SM matching theorem:

```text
python3 scripts/frontier_yt_hqet_direct_route_requirements.py
# SUMMARY: PASS=7 FAIL=0
```

The static residual-mass matching obstruction makes the same boundary formal:
the subtracted correlator is invariant while the decomposition `am0 + delta_m`
is nonunique.  Absolute `m_t` is therefore not determined by the static
correlator alone:

```text
python3 scripts/frontier_yt_static_mass_matching_obstruction.py
# SUMMARY: PASS=6 FAIL=0
```

The source Legendre transform itself cannot select `kappa_H = 1`: source/field
rescaling preserves the Legendre relation while changing curvature and the
Yukawa readout.  A pole-residue or canonical kinetic normalization theorem is
still required:

```text
python3 scripts/frontier_yt_legendre_kappa_gauge_freedom.py
# SUMMARY: PASS=6 FAIL=0
```

The free Wilson-staggered logdet scalar bubble is finite and has no
inverse-curvature zero on the scanned momentum/mass surfaces.  The free source
formalism supplies curvature support, not an isolated physical scalar pole:

```text
python3 scripts/frontier_yt_free_scalar_two_point_pole_absence.py
# SUMMARY: PASS=6 FAIL=0
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
