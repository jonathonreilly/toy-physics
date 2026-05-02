# PR230 Top-Yukawa Physics-Loop Campaign Status Certificate

**Date:** 2026-05-01  
**Status:** open / active campaign continuing after current shortcut blocks
**Runner:** `scripts/frontier_yt_pr230_campaign_status_certificate.py`  
**Certificate:** `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: open / active campaign continuing after current shortcut blocks
conditional_surface_status: conditional-support for future production evidence or new scalar-LSZ/heavy-matching theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Open imports remain across every non-production shortcut route."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

This note summarizes the current PR #230 physics-loop checkpoint.  It does not
claim retained closure.  It records which shortcut routes were tested and what
still remains.

## Runner Result

```text
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=72 FAIL=0
```

The certificate consumes the PR-local route certificates for:

- key-blocker closure attempt;
- scalar source two-point stretch;
- HS/RPA pole-condition attempt;
- scalar ladder scout;
- scalar ladder input audit;
- projector-normalization obstruction;
- HQET direct-route requirements;
- static mass matching obstruction;
- Legendre normalization boundary;
- free scalar two-point pole absence;
- same-1PI scalar-pole boundary;
- scalar LSZ normalization cancellation;
- Feshbach operator-response boundary;
- bridge-stack import audit;
- scalar spectral-saturation no-go;
- large-`N_c` pole-dominance boundary;
- production resource projection;
- Feynman-Hellmann source-response route;
- mass-response bracket certificate;
- source-reparametrization gauge no-go;
- canonical scalar-normalization import audit;
- source-to-Higgs LSZ closure attempt;
- Cl(3)/Z3 source-unit normalization no-go;
- gauge-VEV source-overlap no-go;
- scalar renormalization-condition source-overlap no-go;
- scalar source contact-term scheme boundary;
- scalar-source response harness extension;
- Feynman-Hellmann production protocol certificate;
- same-source scalar two-point LSZ measurement primitive;
- scalar Bethe-Salpeter kernel / residue degeneracy;
- scalar two-point production-harness extension;
- joint Feynman-Hellmann / scalar-LSZ harness certificate;
- joint Feynman-Hellmann / scalar-LSZ resource projection;
- joint Feynman-Hellmann / scalar-LSZ production manifest;
- joint Feynman-Hellmann / scalar-LSZ production postprocess gate;
- joint Feynman-Hellmann / scalar-LSZ production checkpoint granularity gate;
- joint Feynman-Hellmann / scalar-LSZ chunked production manifest;
- joint Feynman-Hellmann / scalar-LSZ chunk combiner gate;
- joint Feynman-Hellmann / scalar-LSZ pole-fit kinematics gate;
- joint Feynman-Hellmann / scalar-LSZ pole-fit postprocessor scaffold;
- joint Feynman-Hellmann / scalar-LSZ pole-fit mode/noise budget;
- joint Feynman-Hellmann / scalar-LSZ eight-mode noise variance gate;
- joint Feynman-Hellmann / scalar-LSZ noise-subsample diagnostics harness;
- joint Feynman-Hellmann / scalar-LSZ variance calibration manifest;
- Feynman-Hellmann / scalar-LSZ invariant readout theorem;
- scalar pole determinant gate;
- scalar ladder eigen-derivative gate;
- scalar ladder total-momentum derivative scout;
- scalar ladder derivative limiting-order obstruction;
- scalar ladder residue-envelope obstruction;
- scalar kernel Ward-identity obstruction;
- scalar zero-mode limit-order theorem;
- zero-mode prescription import audit;
- flat toron scalar-denominator obstruction;
- flat toron thermodynamic washout support;
- color-singlet gauge-zero-mode cancellation;
- color-singlet finite-`q` IR regularity;
- color-singlet zero-mode-removed ladder pole search;
- taste-corner ladder pole-witness obstruction;
- taste-corner scalar-carrier import audit;
- taste-singlet ladder normalization boundary;
- scalar taste-projector normalization theorem attempt;
- unit-projector pole-threshold obstruction;
- scalar-kernel enhancement import audit;
- fitted scalar-kernel residue selector no-go;
- scalar ladder IR / zero-mode obstruction;
- heavy kinetic-mass route scout;
- nonzero-momentum correlator scout;
- momentum-harness extension certificate;
- heavy kinetic-matching obstruction;
- momentum pilot scaling certificate;
- assumption/import stress certificate;
- free staggered kinetic-coefficient support;
- interacting kinetic background sensitivity;
- direct measurement scale requirements;
- retained-closure route certificate refresh.

All loaded runner certificates have `FAIL=0`.  None authorizes a retained
proposal.

## Campaign Verdict

This checkpoint has not reached retained top-Yukawa closure.  It did retire
the visible shortcut routes:

| Route | Current result |
|---|---|
| old Ward / `H_unit` | audited-renaming trap remains forbidden |
| `R_conn` only | channel arithmetic, not scalar LSZ |
| source Legendre transform | exact source formalism, normalization freedom remains |
| free logdet bubble | finite curvature, no scalar pole denominator |
| contact HS/RPA | needs scalar coupling or kernel theorem |
| simplified ladder | projector/source normalization sensitive |
| finite ladder eigenvalue | IR/zero-mode and finite-volume prescription sensitive |
| same-1PI | fixes `y^2 D_phi`, not `y` and residue separately |
| scalar LSZ normalization cancellation | source scaling can cancel only when kernel and residue are derived together |
| Feshbach operator response | exact projection preserves responses but does not prove scalar/gauge residue equality |
| axiom-first / constructive bridge stack | bounded transport support; imports accepted endpoints/surfaces |
| scalar spectral saturation | positivity and low-order moments do not fix pole residue |
| large-`N_c` pole dominance | not a finite-`N_c=3` continuum bound |
| production resource projection | direct route is a planned multi-day production job, not 12-hour foreground evidence |
| Feynman-Hellmann source response | additive rest mass cancels, scalar source normalization remains open |
| mass-response bracket | reduced data show positive `dE/dm_bare`, not physical `dE/dh` |
| source-reparametrization gauge | source-only analytic routes need canonical scalar normalization |
| canonical scalar normalization import audit | existing EW/Higgs notes assume or structure canonical `H`, not derive source `kappa_s` |
| source-to-Higgs LSZ closure attempt | no allowed current-surface premise fixes `kappa_s` |
| Cl(3)/Z3 source-unit normalization | unit substrate/source conventions fix `s`, not the canonical Higgs field metric |
| gauge-VEV source-overlap no-go | canonical `v` and gauge-boson masses fix an already identified Higgs metric, not the source overlap `h = kappa_s s` |
| scalar renormalization-condition source-overlap no-go | canonical `Z_h = 1` fixes the Higgs field residue, not the source operator matrix element `<0|O_s|h>` |
| scalar source contact-term scheme boundary | source contact terms can fix low-`q` curvature conventions while leaving the isolated pole residue different |
| scalar-source response harness extension | production harness now emits `dE/ds`, but not physical `dE/dh` without `kappa_s` |
| Feynman-Hellmann production protocol | common-ensemble symmetric source shifts and correlated `dE/ds` fits are specified; `kappa_s` remains required |
| same-source scalar two-point LSZ measurement | `C_ss(q)` / `Gamma_ss(q)` object is executable, but no controlled pole/continuum limit fixes `kappa_s` |
| scalar Bethe-Salpeter kernel / residue degeneracy | finite same-source samples and a granted pole do not fix `dGamma/dp^2`; denominator remainders move `kappa_s` at `N_c=3` |
| scalar two-point production harness | stochastic same-source `C_ss(q)` estimator is production-facing, but smoke output is reduced-scope and not a pole/LSZ theorem |
| joint Feynman-Hellmann / scalar-LSZ harness | `dE/ds` and same-source `C_ss(q)` can be emitted together, but production data and `kappa_s` remain open |
| joint Feynman-Hellmann / scalar-LSZ resource projection | modest LSZ noise/momentum plan projects to about 3630 single-worker hours; planning only, not evidence |
| joint Feynman-Hellmann / scalar-LSZ production manifest | exact production-targeted, resumable three-volume launch commands exist, but no production data or pole fit has been run |
| joint Feynman-Hellmann / scalar-LSZ production postprocess gate | manifest and partial outputs are blocked as evidence until production phase, same-source `dE/ds`, `Gamma_ss(q)`, isolated-pole derivative, and FV/IR/zero-mode control are all present |
| joint Feynman-Hellmann / scalar-LSZ production checkpoint granularity gate | current `--resume` is whole-volume only; the smallest shard is projected at `180.069` hours, so a 12-hour foreground launch is not safely checkpointed evidence |
| joint Feynman-Hellmann / scalar-LSZ chunked production manifest | L12 can be chunked into 63 production-targeted 16-measurement chunks estimated at `11.3186` hours each, with chunk-local artifact dirs and per-chunk resume; this is launch planning only and does not cover L16/L24 |
| joint Feynman-Hellmann / scalar-LSZ chunk combiner gate | requires all 63 L12 chunks to be production phase with run-control provenance, numba seed-control metadata, unique chunk artifact dirs, same-source FH/LSZ observables, and no duplicate gauge signatures; historical chunks now fail the seed-independence gate |
| joint Feynman-Hellmann / scalar-LSZ chunk001 production checkpoint | one L12 production-format chunk exists, but it lacks the numba seed-control marker and cannot count as independent production evidence until rerun or excluded |
| joint Feynman-Hellmann / scalar-LSZ chunk002 production checkpoint | a second L12 production-format chunk exists, but it shares the historical duplicate gauge signature and cannot count as independent production evidence until rerun or excluded |
| joint Feynman-Hellmann / scalar-LSZ pole-fit kinematics gate | current four modes provide only one nonzero momentum shell, enough for a finite-difference secant but not an isolated-pole derivative |
| joint Feynman-Hellmann / scalar-LSZ pole-fit postprocessor scaffold | concrete future fit path exists, but combined production input is absent/nonready |
| joint Feynman-Hellmann / scalar-LSZ finite-shell identifiability no-go | finite Euclidean `Gamma_ss` shell rows can share the same sampled values and pole while changing `dGamma_ss/dp^2`; a model-class theorem or acceptance gate is still required |
| joint Feynman-Hellmann / scalar-LSZ pole-fit model-class gate | future finite-shell pole fits remain blocked as evidence unless a model-class, analytic-continuation, pole-saturation, continuum, or scalar-denominator certificate excludes the derivative ambiguity |
| joint Feynman-Hellmann / scalar-LSZ Stieltjes model-class obstruction | positive spectral/Stieltjes form alone does not fix the finite-shell ambiguity; positive continuum models can keep shell values and pole while changing residue |
| joint Feynman-Hellmann / scalar-LSZ pole-saturation threshold gate | positive-Stieltjes pole-residue acceptance is now an LP interval gate; the current interval has zero lower bound and remains open/blocking |
| joint Feynman-Hellmann / scalar-LSZ threshold-authority import audit | no current threshold certificate, scalar denominator theorem certificate, or combined L12 output supplies the premise required by the residue-interval gate |
| joint Feynman-Hellmann / scalar-LSZ finite-volume pole-saturation obstruction | finite-L discreteness is not a uniform pole-saturation theorem; near-pole continuum levels with gaps closing like `1/L^2` keep the residue lower bound at zero |
| joint Feynman-Hellmann / scalar-LSZ numba seed-independence audit | historical chunk001/chunk002 metadata seeds differ, but their gauge-evolution signatures match and they lack `numba_gauge_seed_v1`; they are diagnostics only until rerun under the patched harness |
| joint Feynman-Hellmann / scalar-LSZ pole-fit mode/noise budget | eight modes with eight noises fit the current L12 chunk estimate and give pole-fit kinematics, but this is planning only until a variance gate and production data exist |
| joint Feynman-Hellmann / scalar-LSZ eight-mode noise variance gate | x8 lowers solve cost but raises stochastic stderr by `sqrt(2)` versus x16; current reduced smoke and four-mode/x16 chunk surfaces do not provide same-source production variance calibration |
| joint Feynman-Hellmann / scalar-LSZ noise-subsample diagnostics harness | scalar two-point outputs now emit split-noise stability diagnostics needed by future x8/x16 calibration, but the current smokes are reduced-scope instrumentation support only |
| joint Feynman-Hellmann / scalar-LSZ variance calibration manifest | paired x8/x16 L12 commands now match seed, source, modes, and run controls, but no calibration output has completed |
| Feynman-Hellmann / scalar-LSZ invariant readout | exact formula avoids `kappa_s = 1` shortcut, but still needs same-source production pole data |
| scalar pole determinant gate | exact denominator condition identifies `K(x)` and `K'(pole)` as load-bearing open inputs |
| scalar ladder eigen-derivative gate | finite `lambda_max=1` crossing is not enough; `d lambda/dp^2` and momentum-dependent kernel remain open |
| scalar ladder total-momentum derivative scout | finite `d lambda/dp^2` can be computed, but its magnitude is prescription sensitive and no limiting theorem is derived |
| scalar ladder derivative limiting-order obstruction | zero-mode and IR limiting order change the derivative and pole crossing, so the finite derivative is not yet LSZ input |
| scalar ladder residue-envelope obstruction | even after tuning each finite ladder to its own pole, the residue proxy is not single-valued across zero-mode, projector, and volume choices |
| scalar kernel Ward-identity obstruction | existing Ward/gauge/Feshbach surfaces do not fix `K'(x_pole)` or common scalar/gauge dressing |
| scalar zero-mode limit-order theorem | the retained zero mode contributes `1/(V mu_IR^2)`, so IR and volume limits are path-dependent until a prescription is derived |
| zero-mode prescription import audit | existing PT, continuum-identification, manifest, and ladder surfaces do not hide the missing prescription |
| flat toron scalar-denominator obstruction | flat Cartan gauge zero modes have zero plaquette action but change scalar denominator proxies |
| flat toron thermodynamic washout | fixed-holonomy flat-sector dependence washes out for the local massive bubble, but pole/IR LSZ remains open |
| color-singlet gauge-zero-mode cancellation | exact `q=0` gauge mode cancels in the singlet after self and exchange pieces are included; finite-`q` pole derivative remains open |
| color-singlet finite-`q` IR regularity | after q=0 cancellation, the remaining massless kernel is locally integrable in four dimensions; pole derivative remains open |
| color-singlet zero-mode-removed ladder pole search | finite small-mass crossings exist, but they are volume, projector, taste-corner, and derivative sensitive |
| taste-corner ladder pole-witness obstruction | finite crossings are dominated by non-origin taste corners and vanish under physical-origin-only filtering |
| taste-corner scalar-carrier import audit | no retained/audit-clean authority admits those non-origin corners as the PR #230 physical scalar carrier |
| taste-singlet ladder normalization boundary | normalized taste-singlet source weighting rescales the finite witnesses by `1/16` and removes every crossing |
| scalar taste-projector normalization theorem attempt | unit taste-singlet algebra exists, but the physical scalar carrier and interacting pole derivative remain open |
| unit-projector pole-threshold obstruction | after unit projection, the best finite row needs an underived kernel multiplier `2.26091440260` to cross |
| scalar-kernel enhancement import audit | no current HS/RPA, ladder-input, same-1PI, or Ward/Feshbach surface derives that multiplier |
| fitted scalar-kernel residue selector | fitting the multiplier to force a pole imports the missing scalar-kernel normalization and leaves the residue proxy finite-row dependent |
| current-scale direct MC | `am_top = 81.423`, not a useful relativistic top run |
| HQET/static shortcut | removes rest mass, therefore needs matching |
| heavy kinetic mass | cancels additive rest mass, but needs nonzero-momentum data and matching |
| nonzero-momentum scout | method runs on cold gauge, still needs production ensembles and matching |
| momentum harness extension | certificate fields exist, smoke run is reduced-scope only |
| heavy kinetic matching | `c2` and lattice-to-SM matching remain load-bearing |
| momentum pilot scaling | small cold-volume pilot has large finite-volume drift |
| assumption/import stress | no shortcut authorizes retained proposal wording |
| free kinetic coefficient | free `c2` fixed, interacting matching still open |
| interacting kinetic sensitivity | fixed gauge backgrounds change kinetic proxy |
| retained-closure route certificate | refreshed gate includes new source-unit, gauge-VEV source-overlap no-go, scalar renormalization-condition source-overlap no-go, scalar source contact-term scheme boundary, derivative-limit, residue-envelope, Ward-kernel, zero-mode limit-order, zero-mode import-audit, flat-toron obstruction/washout, color-singlet zero-mode/finite-q IR support, zero-mode-removed ladder pole search, taste-corner obstruction/import audit, taste-singlet normalization boundary, scalar taste-projector normalization attempt, unit-projector pole-threshold obstruction, scalar-kernel enhancement import audit, fitted-kernel selector no-go, manifest block, postprocess-gate block, checkpoint-granularity block, chunked-manifest block, chunk-combiner gate, chunk001/chunk002 checkpoints, pole-fit kinematics gate, pole-fit postprocessor scaffold, finite-shell identifiability no-go, pole-fit model-class gate, Stieltjes model-class obstruction, pole-saturation threshold gate, threshold-authority import audit, finite-volume pole-saturation obstruction, numba seed-independence audit, pole-fit mode/noise budget, eight-mode noise variance gate, noise-subsample diagnostics harness, and variance calibration manifest; still no proposed-retained authorization |

## Remaining Honest Routes

1. Strict production direct measurement:
   fine-scale relativistic top campaign or validated heavy-quark treatment with
   matching.

2. New scalar LSZ/canonical normalization theorem:
   interacting scalar two-point denominator, isolated pole or canonical kinetic
   term, and residue `kappa_H`.

3. New heavy-matching observable/theorem:
   nonzero-momentum kinetic-mass correlators plus lattice-HQET/NRQCD-to-SM top
   mass matching without observed top calibration.

4. Feynman-Hellmann source-response measurement:
   production `dE/ds` data plus scalar LSZ/canonical-Higgs normalization
   `kappa_s` and response matching.

## Non-Claims

- This note does not claim retained closure.
- This note does not count non-independent historical chunks as production
  evidence.
- This note does not use observed top mass or `y_t` as proof input.
- This note does not allow `H_unit` matrix-element definition as the `y_t`
  readout.
