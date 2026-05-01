# Review History

Self-review disposition: pass for boundary/support packaging; block for any
retained-closure claim.

Review checks performed:

- Status firewall: notes and loop pack use `open`, `exact negative boundary`,
  or `conditional-support`; no artifact claims retained closure.
- Definition trap: the operator-matching candidate does not define the top
  Yukawa by an `H_unit` matrix element.
- Observation trap: observed top mass and observed `y_t` are not proof inputs.
- Audit trap: existing non-clean parents are listed as open imports, not used
  as retained dependencies.
- Runner hygiene: all three new runners execute with `FAIL=0`; the Ward repair
  runner is a boundary runner rather than an intentionally failing CI check.
- SSB subderivation review: the runner correctly distinguishes the doublet
  Yukawa coefficient `sqrt(2) m/v` from the physical `h t t` vertex `m/v` and
  does not claim either determines source normalization.
- Kappa obstruction review: the countermodels vary only `kappa_H` and keep the
  same counts and SSB identity, so the negative boundary is targeted rather
  than a broad no-go against Ward repair.
- LSZ residue review: the countermodels preserve `R_conn` while varying pole
  residue, so the note does not attack color-channel arithmetic; it attacks
  only the unsupported promotion from channel ratio to physical external leg.
- Chirality selector review: the enumeration is complete over the four
  one-Higgs candidates in the repo hypercharge convention and keeps all
  non-clean parents behind the status firewall.
- Common dressing review: the countermodels vary scalar and gauge dressing
  separately while preserving the tree-level source ratio, which targets only
  the missing equality theorem and does not reuse alpha_LM or plaquette input.
- Scalar pole-residue current-surface review: the models hold all current
  visible algebraic data fixed and vary only the missing pole-residue/dressing
  data, so the no-go targets underdetermination rather than the tree-level
  `1/sqrt(6)` arithmetic.
- Closure route certificate review: the route list separates retained closure
  from new-premise/admitted-selector paths and keeps PR #230 draft/open.
- Direct measurement scale review: the calculation uses the existing
  mass-bracket certificate scale and does not claim production evidence; it
  blocks current-scale production as a closure strategy.
- Key-blocker closure-attempt review: the runner checks every plausible current
  authority family against both required missing pieces, scalar pole residue
  and relative scalar/gauge dressing, and finds no retained closure.
- Scalar source two-point stretch review: the logdet curvature formula uses
  only A_min and functional derivatives, while the free-bubble residue scan
  explicitly avoids observed values and H_unit readout authority.
- Stuck fan-out review: the finite-volume near-match is rejected by a direct
  volume-drift check; HS/RPA is selected only as a conditional successor.
- HS/RPA pole-condition review: the runner does not add a contact coupling to
  A_min; it records that deriving such a coupling from the Wilson gauge ladder
  is the next theorem.
- Ladder-kernel scout review: bounded-support only; explicit mass, IR, and
  simplified projector dependence prevent retained-proposal wording.
- Scalar ladder input-audit review: formula-level `D_psi`, `D_gluon`, and
  scalar/gauge kinematic equality are allowed as exact support, while
  alpha_LM, plaquette, `u0`, and `H_unit` surfaces are explicitly forbidden as
  proof inputs.
- Projector-normalization review: the same finite kernel can cross or fail the
  pole criterion under source/projector normalization changes, so the note is
  an exact negative boundary against using kinematic equality as LSZ readout.
- HQET direct-route review: the static normalized correlator is intentionally
  held fixed while absolute heavy masses vary; this proves an import boundary
  for absolute `m_t`, not a rejection of HQET as an engineering method.
- Static mass matching review: the runner separates raw and subtracted
  correlators and then varies the `am0 + delta_m` decomposition, so the result
  targets only the missing absolute-mass matching condition.
- Legendre normalization review: all tested `kappa` choices satisfy the
  Legendre identity while changing curvature and the Yukawa readout, so the
  artifact blocks only the source-normalization shortcut and leaves a
  pole/kinetic theorem as the positive target.
- Free scalar two-point review: the runner tests the exact free logdet bubble
  and only concludes absence of a free inverse-curvature zero; it does not
  claim interacting scalar poles are impossible.
- Same-1PI boundary review: the artifact distinguishes fixed four-fermion
  exchange coefficient from separately normalized scalar vertex and propagator,
  and it treats the existing same-1PI notes as conditional rather than PR230
  closure authorities.
- Campaign status review: the summary certificate only aggregates already
  generated certificates, verifies that none allows retained-proposal wording,
  and narrows the remaining route list.  It does not create a new authority or
  claim that the campaign reached closure.
- Scalar ladder IR/zero-mode review: the runner holds the source fixed and
  changes only zero-mode, IR, and finite-volume prescriptions.  The finite
  `lambda_max >= 1` pole test flips under those changes, so the artifact is an
  exact boundary on finite ladder witnesses, not a claim that scalar poles are
  impossible.
- Heavy kinetic-mass route review: the runner varies additive rest-mass shifts
  and verifies that `E(p)-E(0)` recovers `M_kin` in a synthetic dispersion.  The
  route is constructive support only; it explicitly requires a `1/M` kinetic
  action term, production nonzero-momentum correlators, and a matching theorem.
- Nonzero-momentum correlator scout review: the runner imports the production
  harness primitives, solves the cold-gauge staggered propagator, and measures
  even momentum-projected correlators.  The result is methodology support only
  because it has no gauge ensemble, statistics, top-scale matching, or physical
  production certificate.
- Momentum-harness extension review: the production harness now carries
  optional momentum modes and certificate fields, and the smoke validation
  runner verifies finite kinetic proxies.  The smoke certificate is
  reduced-scope and must remain rejected by strict production validation.
- Heavy kinetic matching review: the runner varies `c2`, `M0`, and matching
  factors while holding the measured splitting fixed.  It blocks only the
  shortcut from kinetic splitting to SM top mass; it does not reject the kinetic
  route once matching is independently derived.
- Momentum pilot scaling review: the small-volume cold pilot emits finite
  kinetic proxies but shows large finite-volume drift.  This is implementation
  and scaling evidence only, not a strict certificate.

## Review-Loop Backpressure — Campaign Block 2

Local review-loop disposition after the stretch/fan-out/kernel artifacts:

```text
Code / Runner: PASS
Physics Claim Boundary: OPEN / BOUNDED SUPPORT
Imports / Support: DISCLOSED
Nature Retention: OPEN
Repo Governance: PASS for PR230-local loop pack; no repo-wide authority surfaces updated
Audit Compatibility: PASS
```

Findings applied:

- no bare retained/promoted source-note status lines were introduced;
- observed `m_t`, observed `y_t`, and observed Higgs/top data are not proof
  inputs in any new runner;
- `H_unit` matrix-element readout appears only as a forbidden failure mode;
- scalar contact coupling `G`, scalar-channel ladder kernel, IR regulator, and
  scalar projector are now explicit open imports;
- the near-match to `1/sqrt(6)` is demoted by the volume-drift check rather
  than used as evidence.

Checks:

```bash
python3 -m py_compile scripts/frontier_yt_scalar_source_two_point_stretch.py scripts/frontier_yt_scalar_residue_stuck_fanout.py scripts/frontier_yt_hs_rpa_pole_condition_attempt.py scripts/frontier_yt_scalar_ladder_kernel_scout.py
python3 scripts/frontier_yt_scalar_source_two_point_stretch.py
PYTHONPATH=scripts python3 scripts/frontier_yt_scalar_residue_stuck_fanout.py
PYTHONPATH=scripts python3 scripts/frontier_yt_hs_rpa_pole_condition_attempt.py
python3 scripts/frontier_yt_scalar_ladder_kernel_scout.py
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict
git diff --check
```

The audit pipeline and strict lint completed with no errors and the same five
pre-existing warnings.

Open review risk:

- The next positive theorem must not smuggle in the physical Higgs carrier by
  simply renaming the scalar source.  It needs a functional readout theorem.
- The next scalar-ladder theorem must also derive the scalar projector/source
  normalization before using an eigenvalue crossing as physical evidence.
- The next HQET/direct theorem must derive additive mass and matching rather
  than calibrating the static mass to the observed top.
- A static matching theorem cannot be accepted if it simply chooses the
  residual mass that reproduces `172.56 GeV`.
- A Legendre/source theorem cannot be accepted if it fixes `kappa_H` by a field
  naming convention rather than by residue or kinetic normalization.
- A free-bubble theorem cannot be accepted as Higgs-carrier closure unless it
  introduces and derives an interacting denominator or a canonical kinetic term.
- A same-1PI theorem cannot be accepted as a top-Yukawa readout unless the
  scalar pole residue is fixed independently of the four-fermion coefficient.
- A scalar Bethe-Salpeter theorem cannot be accepted from a finite ladder scout
  unless it derives the gauge-zero-mode treatment and finite-volume/IR limiting
  order before applying `lambda_max >= 1`.
- A heavy-kinetic theorem cannot be accepted if it calibrates the matching mass
  from the observed top; the matching bridge must be derived or independently
  measured.

## Review-Loop Backpressure — Campaign Status Checkpoint

Local review-loop disposition for the campaign-status certificate:

```text
Code / Runner: PASS
Physics Claim Boundary: OPEN
Imports / Support: DISCLOSED
Nature Retention: OPEN
Repo Governance: PASS for PR230-local loop pack; no repo-wide authority surfaces updated
Audit Compatibility: PASS
```

Checks:

```bash
python3 -m py_compile scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
```

The certificate is a checkpoint, not a stop condition while campaign runtime
remains.

## Review-Loop Backpressure — Scalar Ladder IR / Zero-Mode Block

Local review-loop disposition:

```text
Code / Runner: PASS
Physics Claim Boundary: EXACT NEGATIVE BOUNDARY
Imports / Support: DISCLOSED
Nature Retention: OPEN
Repo Governance: PASS for PR230-local loop pack; no repo-wide authority surfaces updated
Audit Compatibility: PASS
```

Checks:

```bash
python3 -m py_compile scripts/frontier_yt_scalar_ladder_ir_zero_mode_obstruction.py
python3 scripts/frontier_yt_scalar_ladder_ir_zero_mode_obstruction.py
```

The result blocks a finite-eigenvalue shortcut only.  It leaves open a genuine
scalar-channel theorem with derived zero-mode, IR, volume, projector, and LSZ
residue.

## Review-Loop Backpressure — Heavy Kinetic-Mass Route

Local review-loop disposition:

```text
Code / Runner: PASS
Physics Claim Boundary: BOUNDED SUPPORT
Imports / Support: DISCLOSED
Nature Retention: OPEN
Repo Governance: PASS for PR230-local loop pack; no repo-wide authority surfaces updated
Audit Compatibility: PASS
```

Checks:

```bash
python3 -m py_compile scripts/frontier_yt_heavy_kinetic_mass_route.py
python3 scripts/frontier_yt_heavy_kinetic_mass_route.py
```

This route is now the most concrete lightweight compute successor: measure
nonzero-momentum correlator splittings rather than zero-momentum static
energies.

## Review-Loop Backpressure — Nonzero-Momentum Correlator Scout

Local review-loop disposition:

```text
Code / Runner: PASS
Physics Claim Boundary: BOUNDED SUPPORT
Imports / Support: DISCLOSED
Nature Retention: OPEN
Repo Governance: PASS for PR230-local loop pack; no repo-wide authority surfaces updated
Audit Compatibility: PASS
```

Checks:

```bash
python3 -m py_compile scripts/frontier_yt_nonzero_momentum_correlator_scout.py
python3 scripts/frontier_yt_nonzero_momentum_correlator_scout.py
```

The scout validates the measurement primitive and should be promoted into the
production harness only as an optional kinetic-mass route, not as a substitute
for production evidence.

## Review-Loop Backpressure — Momentum Harness Extension

Local review-loop disposition:

```text
Code / Runner: PASS
Physics Claim Boundary: BOUNDED SUPPORT
Imports / Support: DISCLOSED
Nature Retention: OPEN
Repo Governance: PASS for PR230-local loop pack; no repo-wide authority surfaces updated
Audit Compatibility: PASS
```

Checks:

```bash
python3 -m py_compile scripts/yt_direct_lattice_correlator_production.py scripts/frontier_yt_momentum_harness_extension_certificate.py
python3 scripts/yt_direct_lattice_correlator_production.py --volumes 4x8 --masses 2.0 --therm 0 --measurements 1 --separation 0 --overrelax 0 --ape-steps 0 --momentum-modes '0,0,0;1,0,0;1,1,0' --output outputs/yt_direct_lattice_correlator_momentum_harness_smoke_2026-05-01.json --production-output-dir outputs/yt_direct_lattice_correlator_momentum_smoke --engine python
python3 scripts/frontier_yt_momentum_harness_extension_certificate.py
```

The extension is ready for pilot/production use, but no current result is
strict evidence.

## Review-Loop Backpressure — Heavy Kinetic Matching Obstruction

Local review-loop disposition:

```text
Code / Runner: PASS
Physics Claim Boundary: EXACT NEGATIVE BOUNDARY
Imports / Support: DISCLOSED
Nature Retention: OPEN
Repo Governance: PASS for PR230-local loop pack; no repo-wide authority surfaces updated
Audit Compatibility: PASS
```

Checks:

```bash
python3 -m py_compile scripts/frontier_yt_heavy_kinetic_matching_obstruction.py
python3 scripts/frontier_yt_heavy_kinetic_matching_obstruction.py
```

The route remains actionable only as production evidence plus a matching
theorem.

## Review-Loop Backpressure — Momentum Pilot Scaling

Local review-loop disposition:

```text
Code / Runner: PASS
Physics Claim Boundary: BOUNDED SUPPORT
Imports / Support: DISCLOSED
Nature Retention: OPEN
Repo Governance: PASS for PR230-local loop pack; no repo-wide authority surfaces updated
Audit Compatibility: PASS
```

Checks:

```bash
python3 scripts/yt_direct_lattice_correlator_production.py --volumes 4x8,6x12 --masses 1.0,2.0,5.0 --therm 0 --measurements 1 --separation 0 --overrelax 0 --ape-steps 0 --momentum-modes '0,0,0;1,0,0;1,1,0' --output outputs/yt_direct_lattice_correlator_momentum_pilot_certificate_2026-05-01.json --production-output-dir outputs/yt_direct_lattice_correlator_momentum_pilot --engine python
python3 scripts/yt_direct_lattice_correlator_production.py --volumes 8x16 --masses 2.0 --therm 0 --measurements 1 --separation 0 --overrelax 0 --ape-steps 0 --momentum-modes '0,0,0;1,0,0;1,1,0' --output outputs/yt_direct_lattice_correlator_momentum_L8_probe_certificate_2026-05-01.json --production-output-dir outputs/yt_direct_lattice_correlator_momentum_L8_probe --engine python
python3 -m py_compile scripts/frontier_yt_momentum_pilot_scaling_certificate.py
python3 scripts/frontier_yt_momentum_pilot_scaling_certificate.py
```

Reduced-scope momentum pilots should not be extended as proof substitutes; the
next closure-grade work is production/statistics or a matching/scalar-LSZ
theorem.
