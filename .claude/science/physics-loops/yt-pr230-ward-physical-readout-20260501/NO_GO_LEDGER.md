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

The same-1PI route is not a hidden PR #230 closure: the existing same-1PI notes
use `H_unit`/Rep-B matrix-element data and are audited conditional, and a fixed
four-fermion exchange coefficient constrains only `y^2 D_phi`, not `y` and the
scalar LSZ residue separately:

```text
python3 scripts/frontier_yt_same_1pi_scalar_pole_boundary.py
# SUMMARY: PASS=6 FAIL=0
```

Campaign-status synthesis:

```text
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=8 FAIL=0
```

The synthesis does not create a new no-go theorem by itself.  It records that
the current analytic shortcut set has not authorized retained-proposal wording.
Remaining routes are production evidence, a scalar LSZ/canonical-normalization
theorem, or a heavy-matching observable/theorem.

Finite scalar ladder IR/zero-mode shortcut blocked:

```text
python3 scripts/frontier_yt_scalar_ladder_ir_zero_mode_obstruction.py
# SUMMARY: PASS=7 FAIL=0
```

Holding the scalar source fixed, the same finite Wilson-exchange ladder pole
test flips under the open zero-mode prescription:

```text
N=4, m=0.50, mu_IR^2=0.10, zero mode included: lambda_max = 1.02120376891
N=4, m=0.50, mu_IR^2=0.10, zero mode removed:  lambda_max = 0.236938829531
```

The same finite prescription also flips under volume and IR-regulator changes.
Therefore a finite `lambda_max >= 1` scalar ladder witness cannot close PR #230
until the gauge-zero-mode, finite-volume/IR limiting order, projector, and LSZ
residue are derived.

Heavy kinetic-mass route is constructive but still open:

```text
python3 scripts/frontier_yt_heavy_kinetic_mass_route.py
# SUMMARY: PASS=6 FAIL=0
```

The additive static rest mass cancels in nonzero-momentum splittings
`E(p)-E(0)`, so this route avoids the static zero-momentum no-go.  It is not a
closure proof because pure static correlators have no kinetic splitting and the
route still requires a `1/M` kinetic action term, nonzero-momentum data, and a
lattice-HQET/NRQCD-to-SM matching theorem.

Nonzero-momentum correlator primitive now exists but remains scout-only:

```text
python3 scripts/frontier_yt_nonzero_momentum_correlator_scout.py
# SUMMARY: PASS=7 FAIL=0
```

The tiny cold-gauge scout reuses the production harness Dirac builder and CG
solve, then constructs even momentum-projected correlators.  It validates the
observable machinery, but it cannot certify `m_t` or `y_t` without gauge
ensembles, production statistics, and matching.

Momentum-harness extension remains smoke-only:

```text
python3 scripts/frontier_yt_momentum_harness_extension_certificate.py
# SUMMARY: PASS=6 FAIL=0
```

The production harness can now emit momentum-analysis fields, but the current
certificate is a one-configuration cold-gauge smoke artifact.  It is not
production evidence and does not remove the heavy-action matching import.

Kinetic-to-SM matching shortcut blocked:

```text
python3 scripts/frontier_yt_heavy_kinetic_matching_obstruction.py
# SUMMARY: PASS=5 FAIL=0
```

The same measured splitting can be represented by different `c2, M0` pairs.
Even with a lattice `M_kin`, changing the lattice-to-SM matching factor changes
the inferred `m_t` and `y_t` without changing the correlator.  Therefore the
kinetic route requires a retained matching theorem or independent production
matching evidence.

Reduced momentum pilot does not certify closure:

```text
python3 scripts/frontier_yt_momentum_pilot_scaling_certificate.py
# SUMMARY: PASS=6 FAIL=0
```

The small-volume cold pilot gives finite `M_kin` proxies but full relative
spread `0.950562`; it confirms the implementation route and rejects
reduced-scope pilot data as strict evidence.

Assumption shortcut stress:

```text
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=8 FAIL=0
```

No current route certificate authorizes retained-proposal wording.  The stress
certificate explicitly forbids hidden use of `H_unit`, observed target values,
alpha/plaquette/u0, reduced pilots, `c2 = 1`, or `Z_match = 1`.

Free kinetic coefficient is positive support but not closure:

```text
python3 scripts/frontier_yt_free_staggered_kinetic_coefficient.py
# SUMMARY: PASS=6 FAIL=0
```

The free action fixes `M_kin^free = m sqrt(1+m^2)`, but the interacting kinetic
renormalization and lattice-to-SM matching import remain open.

Interacting kinetic background sensitivity blocks the free-c2 shortcut:

```text
python3 scripts/frontier_yt_interacting_kinetic_background_sensitivity.py
# SUMMARY: PASS=6 FAIL=0
```

On three small fixed backgrounds at `m=2.0`, the `p_min` kinetic proxy changes
from `39.7541468294` to `46.7925766809` to `12.1021659111`, with relative
spread `1.05497`.  Therefore the free kinetic coefficient is not sufficient to
certify the interacting top kinetic readout.  The route still needs production
ensemble measurement or a retained interacting kinetic/matching theorem.

Scalar LSZ source-scaling covariance is conditional support only:

```text
python3 scripts/frontier_yt_scalar_lsz_normalization_cancellation.py
# SUMMARY: PASS=6 FAIL=0
```

If `O -> c O`, a covariantly transformed scalar denominator scales the bubble
and inverse residue by `c^2`, while the source vertex scales by `c`; the
canonical `vertex/sqrt(Z_inverse)` proxy is invariant.  This repairs only the
source-normalization bookkeeping.  It does not derive the interacting
denominator, pole location, or residue derivative needed for PR #230 closure.

Exact Feshbach response preservation does not derive common dressing:

```text
python3 scripts/frontier_yt_feshbach_operator_response_boundary.py
# SUMMARY: PASS=5 FAIL=0
```

Schur/Feshbach projection preserves low-energy responses for projected scalar
and gauge sources, and it preserves their response ratio.  But it is
operator-specific: rescaling the microscopic scalar source changes the
scalar/gauge response ratio while Feshbach errors remain at numerical zero.
Thus crossover response preservation cannot replace a microscopic scalar
residue/common-dressing theorem.

Retained-closure route certificate refreshed:

```text
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=12 FAIL=0
```

The refreshed certificate includes LSZ normalization cancellation, Feshbach
operator response, and interacting kinetic sensitivity.  It still finds no
retained-proposal route on the current surface.

Existing bridge stack is not a missed PR230 proof:

```text
python3 scripts/frontier_yt_bridge_stack_import_audit.py
# SUMMARY: PASS=7 FAIL=0
```

The axiom-first / constructive UV bridge stack remains bounded transport
support.  It imports an accepted endpoint or accepted plaquette/`u_0` surface
and its ledger rows are bounded, unaudited, or audited conditional.  It cannot
replace the direct measurement or scalar-residue theorem.

Scalar spectral saturation is not supplied by positivity/low moments:

```text
python3 scripts/frontier_yt_scalar_spectral_saturation_no_go.py
# SUMMARY: PASS=6 FAIL=0
```

Positive pole-plus-continuum spectral models can share the same `C(0)` and
`C'(0)` while carrying different isolated pole residues.  Therefore a future
scalar LSZ route must prove pole saturation or continuum control.

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
