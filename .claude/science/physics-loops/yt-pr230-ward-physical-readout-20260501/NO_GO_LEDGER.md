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

Large-`N_c` pole dominance is not finite-`N_c=3` closure:

```text
python3 scripts/frontier_yt_large_nc_pole_dominance_boundary.py
# SUMMARY: PASS=6 FAIL=0
```

At `N_c=3`, a `1/N_c^2` continuum allowance shifts the canonical Yukawa proxy
by `0.057191`.  Sub-percent closure needs an actual finite-`N_c` continuum
bound or direct residue measurement.

Direct production is not a 12-hour foreground certificate:

```text
python3 scripts/frontier_yt_production_resource_projection.py
# SUMMARY: PASS=7 FAIL=0
```

The existing `12^3 x 24` numba mass-bracket benchmark projects the requested
three-volume, three-mass strict protocol to about `228.48` single-worker hours.
This is planning support for the direct route, not production data, matching
evidence, or strict-runner certification.

Feynman-Hellmann source response moves but does not close the blocker:

```text
python3 scripts/frontier_yt_feynman_hellmann_source_response_route.py
# SUMMARY: PASS=6 FAIL=0
```

Energy slopes `dE/ds` with respect to a uniform scalar source can cancel the
additive heavy rest-mass ambiguity.  They still depend on the normalization of
the lattice source `s`; converting to the physical `dE/dh` Yukawa readout
requires a scalar source-to-Higgs normalization theorem or direct scalar LSZ
residue measurement.

Reduced mass-bracket response is bare-source evidence only:

```text
python3 scripts/frontier_yt_mass_response_bracket_certificate.py
# SUMMARY: PASS=7 FAIL=0
```

The existing reduced `12^3 x 24` mass scan gives positive local slopes
`dE/dm_bare`, but this does not fix the physical scalar-source normalization or
the lattice-to-SM matching.  It is a lightweight scout for a future production
response route, not retained closure.

Source-only analytic closure blocked by reparametrization gauge:

```text
python3 scripts/frontier_yt_source_reparametrization_gauge_no_go.py
# SUMMARY: PASS=6 FAIL=0
```

Source curvature, same-1PI products, and Feynman-Hellmann slopes remain
covariant under `h = kappa s`.  Setting `kappa = 1` is a hidden normalization
choice unless derived from scalar LSZ/canonical kinetic data or directly
measured.

Existing EW/Higgs notes do not supply hidden `kappa_s` closure:

```text
python3 scripts/frontier_yt_canonical_scalar_normalization_import_audit.py
# SUMMARY: PASS=7 FAIL=0
```

The EW Higgs gauge-mass note assumes a canonical Higgs doublet and kinetic
term; the SM one-Higgs selection note leaves Yukawa matrices arbitrary; the
observable-principle row is audited conditional; and `R_conn`/EW color
projection do not derive scalar LSZ normalization.

Explicit source-to-Higgs / LSZ closure attempt remains open:

```text
python3 scripts/frontier_yt_source_to_higgs_lsz_closure_attempt.py
# SUMMARY: PASS=7 FAIL=0
```

Allowed current-surface premises do not fix `kappa_s`.  Forbidden or
conditional premises are explicitly excluded.  The required theorem is an
actual scalar-pole/LSZ source-to-canonical-Higgs bridge or direct physical
response measurement.

Scalar-source response harness support is bounded, not closure:

```text
python3 scripts/frontier_yt_scalar_source_response_harness_certificate.py
# SUMMARY: PASS=8 FAIL=0
```

The production harness now accepts explicit uniform scalar-source shifts and
emits `scalar_source_response_analysis` with a finite `dE/ds` slope on a
reduced smoke certificate.  This advances the Feynman-Hellmann observable
route, but it is not physical `dE/dh`: the source coordinate is `s` in
`m_bare + s`, and `h = kappa_s s` remains open.  Setting `kappa_s = 1` remains
forbidden unless derived by scalar LSZ/canonical normalization, and the smoke
run is reduced-scope rather than production evidence.

Feynman-Hellmann production protocol is specified but remains open:

```text
python3 scripts/frontier_yt_fh_production_protocol_certificate.py
# SUMMARY: PASS=9 FAIL=0
```

The protocol uses common-ensemble symmetric source shifts and correlated
`dE_top/ds` fits across the strict PR230 volumes.  This is a production design,
not a closure theorem.  The physical conversion still requires a scalar
two-point LSZ/canonical-normalization measurement for `kappa_s`, plus any
lattice-to-SM response matching.

Same-source scalar two-point LSZ measurement primitive is bounded support:

```text
python3 scripts/frontier_yt_same_source_scalar_two_point_lsz_measurement.py
# SUMMARY: PASS=8 FAIL=0
```

For the same additive source used in `dE_top/ds`, the executable measurement
object is now explicit:

```text
C_ss(q) = Tr[S V_q S V_-q]
Gamma_ss(q) = 1 / C_ss(q)
```

A true LSZ bridge would derive an isolated pole and compute
`dGamma_ss/dp^2` at that pole.  The reduced cold primitive does not close the
route: no measured mode has a controlled pole, the finite residue proxy is
mass-dependent, and source rescaling changes inverse curvature until canonical
normalization is derived.

Scalar Bethe-Salpeter finite-sample pole-residue shortcut is blocked:

```text
python3 scripts/frontier_yt_scalar_bs_kernel_residue_degeneracy.py
# SUMMARY: PASS=6 FAIL=0
```

Even granting an isolated scalar pole, finite same-source Euclidean samples do
not fix the LSZ residue.  Analytic denominator deformations can preserve every
measured `Gamma_ss(q)` value and the granted pole location while changing
`dGamma/dp^2` at the pole.  At physical `N_c=3`, natural `1/N_c^2` denominator
remainders already move the `kappa_s` proxy by more than five percent without
changing the finite samples.  The route still needs a retained interacting
denominator theorem, finite-volume/IR/zero-mode limiting order, and a
finite-`N_c` pole-residue bound or production residue measurement.

Scalar two-point harness extension is production support, not closure:

```text
python3 scripts/frontier_yt_scalar_two_point_harness_certificate.py
# SUMMARY: PASS=9 FAIL=0
```

The production harness can now emit stochastic estimates of the same-source
`C_ss(q)` and `Gamma_ss(q)` object.  This removes an engineering blocker for
the Feynman-Hellmann/LSZ route, but the reduced smoke certificate is not
production evidence and does not derive a scalar pole, `dGamma/dp^2` at the
pole, or canonical Higgs normalization.  `kappa_s = 1` remains forbidden.

Joint Feynman-Hellmann / scalar-LSZ harness support is bounded:

```text
python3 scripts/frontier_yt_fh_lsz_joint_harness_certificate.py
# SUMMARY: PASS=10 FAIL=0
```

The harness can emit `dE_top/ds` and same-source `C_ss(q)`/`Gamma_ss(q)` in the
same reduced run.  This defines the exact production measurement bundle, but
the smoke output is not production evidence and cannot convert `dE/ds` to
`dE/dh` without `kappa_s` from a controlled scalar pole and canonical LSZ
normalization.

Joint FH/LSZ production is not a 12-hour foreground closure route:

```text
python3 scripts/frontier_yt_fh_lsz_joint_resource_projection.py
# SUMMARY: PASS=7 FAIL=0
```

Using four scalar-LSZ momentum modes and sixteen noise vectors per
configuration, the solve budget is about `15.8889x` the existing three-mass
direct resource projection, or about `3630.28` single-worker hours before
additional autocorrelation or pole-fit tuning.  This is exact next-action
planning, not evidence.

Same-source FH/LSZ readout formula is exact support, not closure:

```text
python3 scripts/frontier_yt_fh_lsz_invariant_readout_theorem.py
# SUMMARY: PASS=7 FAIL=0
```

If `dE_top/ds` and `C_ss` use the same source and a controlled scalar pole is
present, the invariant readout is
`(dE_top/ds) * sqrt(dGamma_ss/dp^2 at the pole)`, equivalently
`dE_top/ds / sqrt(Res[C_ss])`.  This blocks the forbidden `kappa_s = 1`
shortcut but does not supply the missing pole, derivative, or production
response data.

Scalar pole determinant gate is exact support, not closure:

```text
python3 scripts/frontier_yt_scalar_pole_determinant_gate.py
# SUMMARY: PASS=7 FAIL=0
```

In one-channel form `C_ss = Pi/D` with `D=1-K Pi`.  A pole location fixes
`K(x_pole)` but not `K'(x_pole)`, and `D'(x_pole)` controls the LSZ residue.
Therefore pole naming or contact tuning cannot close PR #230 without an
interacting scalar-channel kernel theorem or production pole-derivative
measurement.

Scalar ladder eigenvalue crossing is not yet an LSZ residue theorem:

```text
python3 scripts/frontier_yt_scalar_ladder_eigen_derivative_gate.py
# SUMMARY: PASS=7 FAIL=0
```

The matrix Bethe-Salpeter pole condition `lambda_max=1` fixes only a crossing.
Holding that crossing fixed while varying the momentum derivative of the ladder
kernel changes `d lambda_max/dp^2`, the residue proxy, and the FH/LSZ readout
factor.  The route still needs a momentum-dependent kernel theorem or
production pole-derivative data.

Scalar ladder total-momentum derivative scout is bounded support only:

```text
python3 scripts/frontier_yt_scalar_ladder_total_momentum_derivative_scout.py
# SUMMARY: PASS=9 FAIL=0
```

The finite Wilson-exchange scout computes `d lambda_max/dp^2` by shifting the
fermion bubble denominators with total scalar momentum.  The derivative is
finite and negative on the scanned surfaces, but its magnitude varies by about
`3903.98x` across mass, volume, IR regulator, zero-mode, and projector choices.
This is not a retained scalar-LSZ theorem and does not fix `kappa_s`.

Scalar ladder derivative limiting-order shortcut is blocked:

```text
python3 scripts/frontier_yt_scalar_ladder_derivative_limit_obstruction.py
# SUMMARY: PASS=8 FAIL=0
```

The total-momentum derivative has prescription-dependent IR behavior.  On the
same finite surface, retaining the gauge zero mode makes the derivative grow
by `13.882x` to `24.0129x` as `mu_IR^2` is lowered from `0.50` to `0.02`;
removing the zero mode keeps the derivative within about `1.11x`.  The pole
test crosses only in the zero-mode-included prescription.  Therefore the
finite derivative is not a retained LSZ residue input without a zero-mode/IR
limiting theorem or production pole data.

Scalar ladder pole-tuned residue-envelope shortcut is blocked:

```text
python3 scripts/frontier_yt_scalar_ladder_residue_envelope_obstruction.py
# SUMMARY: PASS=9 FAIL=0
```

Tuning each finite ladder surface to its own pole removes the pole-location
ambiguity, but the resulting LSZ residue proxy still has a `7.08739x` envelope
spread across allowed current-surface zero-mode, projector, IR, and volume
choices.  At `N=5`, fixed `mu_IR^2=0.05`, local-source zero-mode removal
changes the proxy by `5.21259x`, and the removed-zero-mode local versus
normalized point-split projectors differ by `2.09302x`.  Therefore finite
Bethe-Salpeter ladder residues are not retained scalar-LSZ input without the
limiting theorem or production pole-derivative data.

Scalar-kernel Ward-identity shortcut is blocked:

```text
python3 scripts/frontier_yt_scalar_kernel_ward_identity_obstruction.py
# SUMMARY: PASS=9 FAIL=0
```

The old `yt_ward_identity` surface is audited-renaming, Feshbach response
preservation is operator-specific, and common scalar/gauge dressing remains an
open bridge.  A rank-count model fixes only `K(x_pole)` from `D(x_pole)=0`;
`K'(x_pole)` and common dressing remain free.  A same-pole kernel family
preserves the pole while changing the scalar LSZ readout factor by `2.35319x`.
Therefore Ward/gauge identities cannot be used as the scalar denominator
derivative theorem.

Cl(3)/Z3 source-unit normalization shortcut is blocked:

```text
python3 scripts/frontier_yt_cl3_source_unit_normalization_no_go.py
# SUMMARY: PASS=8 FAIL=0
```

Unit lattice spacing, unit Clifford generator norms, `g_bare=1`, and the
additive source coefficient in `D+m+s` define the source coordinate and
operator insertion.  They do not define the canonical Higgs field metric.
Reassigning `h=kappa_s s` leaves same-source invariant readouts fixed while
changing `dE/dh` and canonical curvature.  Therefore `kappa_s=1` remains an
import unless derived by scalar pole/kinetic normalization or measured by
same-source LSZ data.

Joint FH/LSZ production manifest is not evidence:

```text
python3 scripts/frontier_yt_fh_lsz_production_manifest.py
# SUMMARY: PASS=9 FAIL=0
```

The manifest records exact production-targeted, resumable launch commands for
the strict three-volume physical-response route, but it does not run those
commands, produce correlators, fit `dE/ds`, fit `Gamma_ss(q)`, or derive a
scalar pole derivative.  It cannot authorize retained or proposed-retained
wording.

Retained-closure route certificate remains open after refresh:

```text
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=20 FAIL=0
```

The refreshed gate includes same-source invariant readout, scalar ladder
derivative limiting-order, scalar ladder residue-envelope, Cl(3)/Z3
source-unit, scalar-kernel Ward-identity, scalar zero-mode limit-order,
production-manifest, and joint resource blocks.  It still authorizes no
proposed-retained wording.

Scalar zero-mode limit-order shortcut is blocked:

```text
python3 scripts/frontier_yt_scalar_zero_mode_limit_order_theorem.py
# SUMMARY: PASS=8 FAIL=0
```

The retained gauge zero mode contributes an exact positive diagonal term
`(4/3) w_i/(V mu_IR^2)` to the finite Wilson-exchange scalar ladder.  At fixed
volume it diverges as `1/mu_IR^2`; at fixed regulator it vanishes as
`1/N^4`; and box-scaled regulators can leave a finite or growing contribution.
Therefore the scalar denominator and LSZ derivative remain path-dependent
until a retained gauge-fixing, zero-mode, IR, and finite-volume prescription is
derived or production pole data fixes the prescription.

Zero-mode prescription import audit is blocked:

```text
python3 scripts/frontier_yt_zero_mode_prescription_import_audit.py
# SUMMARY: PASS=8 FAIL=0
```

The strongest current repo candidates do not supply a retained prescription:
the BZ perturbative note has IR-regulator and gauge-parameter conventions but
not a PR #230 scalar zero-mode theorem; continuum identification warns about
alternative gauge fixings; the production manifest requires zero-mode control;
and scalar ladder certificates keep `proposal_allowed=false`.

Flat toron scalar-denominator shortcut is blocked:

```text
python3 scripts/frontier_yt_flat_toron_scalar_denominator_obstruction.py
# SUMMARY: PASS=7 FAIL=0
```

Constant commuting Cartan links have zero plaquette action but distinct
Polyakov phases.  In the finite scalar-source bubble proxy, those phases shift
charged fermion momenta and change the inverse scalar-denominator proxy by
`1.05244x` on the scan.  Therefore the compact action does not by itself select
the trivial gauge zero mode; a toron/zero-mode prescription remains
load-bearing.

Flat toron finite-volume ambiguity has thermodynamic washout support, but not
closure:

```text
python3 scripts/frontier_yt_flat_toron_thermodynamic_washout.py
# SUMMARY: PASS=6 FAIL=0
```

For fixed physical holonomy `phi`, the constant link angle is `theta=phi/N`.
The local massive scalar bubble is a shifted periodic Riemann sum, so it
converges to the same Brillouin-zone integral as the trivial sector.  The scan
shows the relative bubble and inverse-denominator shifts are below `1e-4` for
`N >= 20`.  This retires the flat-toron finite-volume ambiguity for that local
massive bubble, but not the interacting scalar pole, massless gauge-zero-mode
IR prescription, finite-`N_c` residue, or production evidence.

Color-singlet `q=0` gauge zero mode cancels, but closure remains open:

```text
python3 scripts/frontier_yt_color_singlet_zero_mode_cancellation.py
# SUMMARY: PASS=7 FAIL=0
```

The total color charge annihilates the `q qbar` singlet:
`(T_q^a + T_qbar^a)|S>=0`.  The quark self, antiquark self, and exchange
pieces cancel exactly as `C_F + C_F - 2 C_F = 0`.  This blocks the
exchange-only finite-ladder `q=0` divergence, but finite-`q` IR behavior,
the interacting scalar pole derivative, source/projector normalization, and
production FH/LSZ evidence remain open.

Color-singlet finite-`q` IR divergence concern is removed, but closure remains
open:

```text
python3 scripts/frontier_yt_color_singlet_finite_q_ir_regular.py
# SUMMARY: PASS=6 FAIL=0
```

After the exact color-singlet `q=0` cancellation, the remaining massless kernel
is locally integrable in four dimensions: `d^4q/q^2 ~ q dq`.  The
zero-mode-removed finite lattice kernel has a stable `mu_IR -> 0` limit and
stable large-volume sequence in the scan.  This does not derive the full
interacting scalar denominator, pole location, LSZ derivative, or production
evidence.

Zero-mode-removed finite ladder pole witnesses are constructive but not
closure:

```text
python3 scripts/frontier_yt_color_singlet_zero_mode_removed_ladder_pole_search.py
# SUMMARY: PASS=9 FAIL=0
```

After color-singlet `q=0` removal and finite-`q` IR regularity, the finite
Wilson-exchange ladder has four small-mass `lambda_max >= 1` witnesses.  They
are not stable: local `m=0.30` crosses at `N=4` but not at `N=3,5,6`;
`N=6,m=0.20` crosses for the local projector but not for the normalized
point-split projector; every crossing row sits on even grids with 16
`sin(p)=0` taste corners; and the crossing residue-proxy spread is `5.15346x`.
Therefore a finite zero-mode-removed ladder pole witness is not the retained
scalar pole/LSZ theorem.  The route still needs continuum/taste/projector
control plus the interacting inverse-propagator derivative, or production
same-source pole data.

Taste-corner finite pole witness is blocked as scalar evidence:

```text
python3 scripts/frontier_yt_taste_corner_ladder_pole_obstruction.py
# SUMMARY: PASS=8 FAIL=0
```

The four finite crossing witnesses are dominated by non-origin
Brillouin-zone taste corners.  The non-origin corners supply `70.4828%` to
`92.2308%` of the full crossing scale, and the corner-only kernel reproduces
`92.7618%` to `98.7049%`.  Filtering to the physical origin corner plus
non-corner modes removes every crossing, with maximum lambda `0.269595077382`.
Thus the finite crossings cannot be used as scalar pole evidence unless a
retained taste/corner scalar-carrier theorem admits them and derives the pole
derivative.

Taste-corner scalar-carrier hidden-import route is blocked:

```text
python3 scripts/frontier_yt_taste_carrier_import_audit.py
# SUMMARY: PASS=8 FAIL=0
```

The current ledger does not contain a retained authority admitting the
non-origin BZ corners as the physical scalar carrier.  The CL3 taste
generation row is an audited-renaming boundary, taste-scalar isotropy is
conditional for scalar-spectrum consequences, full staggered PT is conditional
and imports non-clean normalization surfaces, and the scalar ladder input
audit still lists the scalar color/taste/spin projector as missing.  Therefore
the taste-corner finite crossings remain non-closure evidence until a new
taste/scalar-carrier theorem or production pole data exists.

Taste-singlet normalization removes the finite ladder crossings:

```text
python3 scripts/frontier_yt_taste_singlet_ladder_normalization_boundary.py
# SUMMARY: PASS=6 FAIL=0
```

If the scalar carrier is a normalized taste singlet over the 16 BZ corners,
the finite ladder eigenvalue receives the expected `1/N_taste` source-vertex
normalization.  Applying that normalization divides every raw finite crossing
witness by `16`, giving normalized `lambda_max` values between
`0.0914604870307` and `0.442298920672`.  No finite crossing remains.  The
unnormalized taste multiplicity is therefore load-bearing and cannot be used
as scalar pole/LSZ evidence without a retained scalar taste/projector
normalization theorem.

Scalar taste/projector normalization theorem attempt is blocked at the
physical-carrier step:

```text
python3 scripts/frontier_yt_scalar_taste_projector_normalization_attempt.py
# SUMMARY: PASS=8 FAIL=0
```

The unit taste singlet over the 16 corners is algebraically available, with
`O_singlet=(1/sqrt(16)) sum_t O_t` and norm squared `1`.  The unnormalized
local corner sum has norm squared `16`.  This algebra explains the `1/16`
ladder rescaling, but it does not identify the physical scalar carrier:
`s O_local = (sqrt(16) s) O_singlet`, so the source-coordinate normalization
and canonical Higgs metric still require an LSZ/pole theorem or production
same-source pole data.  The current taste-carrier audit also still supplies no
retained authority for non-origin corners as the physical scalar carrier.

Unit-projector finite ladder has no retained-strength pole threshold:

```text
python3 scripts/frontier_yt_unit_projector_pole_threshold_obstruction.py
# SUMMARY: PASS=6 FAIL=0
```

After applying the unit taste projector, every finite crossing witness drops
below `lambda_max = 1`.  The best row has `lambda_max = 0.442298920672`, so a
finite pole would require a scalar-kernel multiplier `2.26091440260`.  No
current retained premise derives that enhancement; fitting it to force a pole
would be a new scalar-channel normalization/selector import.

Scalar-kernel enhancement hidden-import route is blocked:

```text
python3 scripts/frontier_yt_scalar_kernel_enhancement_import_audit.py
# SUMMARY: PASS=7 FAIL=0
```

The strongest current candidates do not supply the required multiplier:
HS/RPA needs an extra contact `G` or kernel theorem; the ladder input audit
lists the exact scalar-channel kernel, projector, limit, crossing, and residue
as missing; same-1PI fixes only `y^2 D_phi`; and Ward/Feshbach identities do
not fix `K'(x_pole)` or common dressing.

Fitted scalar-kernel residue selector is blocked:

```text
python3 scripts/frontier_yt_fitted_kernel_residue_selector_no_go.py
# SUMMARY: PASS=8 FAIL=0
```

Forcing a unit-projected finite pole with `g_eff = 1/lambda_unit` imports the
missing scalar-channel normalization.  Even after granting that fitted pole,
the LSZ residue proxy reduces to `lambda_raw / |d lambda_raw / dp^2|` and
varies across the current finite rows by a factor `2.00925585041`.  Therefore
the finite fitted-pole selector is not a retained interacting denominator or
`K'(x_pole)` theorem.

FH/LSZ production manifest-as-evidence route is blocked:

```text
python3 scripts/frontier_yt_fh_lsz_production_postprocess_gate.py
# SUMMARY: PASS=9 FAIL=0
```

The three-volume manifest is a valid launch surface, but the expected
production outputs are absent.  Even a future raw production bundle is not
physical `y_t` evidence until it passes the explicit postprocess gate:
production phase, common-ensemble `dE_top/ds`, same-source `Gamma_ss(q)`,
isolated-pole `dGamma_ss/dp^2`, FV/IR/zero-mode control, no forbidden
normalization imports, and retained-proposal certification.

FH/LSZ production foreground launch is blocked by checkpoint granularity:

```text
python3 scripts/frontier_yt_fh_lsz_production_checkpoint_granularity_gate.py
# SUMMARY: PASS=9 FAIL=0
```

The manifest's `--resume` support currently loads completed per-volume
`ensemble_measurement.json` artifacts only.  The harness writes that artifact
after `run_volume(...)` returns; no mid-volume configuration checkpoint is
detected.  Since the smallest joint shard is projected at `180.069` hours, a
12-hour foreground launch would be a partial run with no safely checkpointed
production evidence.

Chunked L12 production manifest is launch planning only:

```text
python3 scripts/frontier_yt_fh_lsz_chunked_production_manifest.py
# SUMMARY: PASS=8 FAIL=0
```

L12_T24 can be split into 63 production-targeted chunks of 16 saved
configurations, with a conservative estimate of `11.3186` hours per chunk.
This is not production evidence, does not cover L16/L24, and still requires a
multi-chain combination plus scalar-pole postprocess certificate.

FH/LSZ chunk combiner gate blocks partial evidence:

```text
python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=7 FAIL=0
```

The L12 route now has an acceptance gate, not evidence.  The gate reconstructs
63 expected chunks, requires production-phase metadata, same-source `dE/ds`,
same-source `C_ss(q)`, and `metadata.run_control` seed/command provenance, and
finds `0` present / `0` ready chunks.  Even a future complete L12 combination
would still be non-retained without L16/L24, isolated scalar-pole derivative,
FV/IR/zero-mode control, and retained-proposal certification.

FH/LSZ chunk artifact-collision shortcut is blocked:

```text
python3 scripts/frontier_yt_fh_lsz_chunked_production_manifest.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=8 FAIL=0
```

Chunk commands now include a chunk-local `--production-output-dir` plus
`--resume`, and the combiner verifies 63 unique artifact directories.  A future
chunk cannot be accepted by overwriting or reusing another chunk's completed
per-volume artifact.

FH/LSZ negative scalar-source CLI preflight blocker fixed:

```text
python3 scripts/frontier_yt_fh_lsz_production_manifest.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunked_production_manifest.py
# SUMMARY: PASS=10 FAIL=0
```

The first chunk launch failed before compute because `--scalar-source-shifts
-0.01,0.0,0.01` lets `argparse` treat the negative value as an option.  Both
FH/LSZ manifest emitters now use `--scalar-source-shifts=-0.01,0.0,0.01`.

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
