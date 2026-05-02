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
# SUMMARY: PASS=40 FAIL=0
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
- scalar-source response harness extension;
- Feynman-Hellmann production protocol certificate;
- same-source scalar two-point LSZ measurement primitive;
- scalar Bethe-Salpeter kernel / residue degeneracy;
- scalar two-point production-harness extension;
- joint Feynman-Hellmann / scalar-LSZ harness certificate;
- joint Feynman-Hellmann / scalar-LSZ resource projection;
- Feynman-Hellmann / scalar-LSZ invariant readout theorem;
- scalar pole determinant gate;
- scalar ladder eigen-derivative gate;
- scalar ladder total-momentum derivative scout;
- scalar ladder derivative limiting-order obstruction;
- scalar ladder IR / zero-mode obstruction;
- heavy kinetic-mass route scout;
- nonzero-momentum correlator scout;
- momentum-harness extension certificate;
- heavy kinetic-matching obstruction;
- momentum pilot scaling certificate;
- assumption/import stress certificate;
- free staggered kinetic-coefficient support;
- interacting kinetic background sensitivity;
- direct measurement scale requirements.

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
| scalar-source response harness extension | production harness now emits `dE/ds`, but not physical `dE/dh` without `kappa_s` |
| Feynman-Hellmann production protocol | common-ensemble symmetric source shifts and correlated `dE/ds` fits are specified; `kappa_s` remains required |
| same-source scalar two-point LSZ measurement | `C_ss(q)` / `Gamma_ss(q)` object is executable, but no controlled pole/continuum limit fixes `kappa_s` |
| scalar Bethe-Salpeter kernel / residue degeneracy | finite same-source samples and a granted pole do not fix `dGamma/dp^2`; denominator remainders move `kappa_s` at `N_c=3` |
| scalar two-point production harness | stochastic same-source `C_ss(q)` estimator is production-facing, but smoke output is reduced-scope and not a pole/LSZ theorem |
| joint Feynman-Hellmann / scalar-LSZ harness | `dE/ds` and same-source `C_ss(q)` can be emitted together, but production data and `kappa_s` remain open |
| joint Feynman-Hellmann / scalar-LSZ resource projection | modest LSZ noise/momentum plan projects to about 3630 single-worker hours; planning only, not evidence |
| Feynman-Hellmann / scalar-LSZ invariant readout | exact formula avoids `kappa_s = 1` shortcut, but still needs same-source production pole data |
| scalar pole determinant gate | exact denominator condition identifies `K(x)` and `K'(pole)` as load-bearing open inputs |
| scalar ladder eigen-derivative gate | finite `lambda_max=1` crossing is not enough; `d lambda/dp^2` and momentum-dependent kernel remain open |
| scalar ladder total-momentum derivative scout | finite `d lambda/dp^2` can be computed, but its magnitude is prescription sensitive and no limiting theorem is derived |
| scalar ladder derivative limiting-order obstruction | zero-mode and IR limiting order change the derivative and pole crossing, so the finite derivative is not yet LSZ input |
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
- This note does not demote PR #230's scout/proposed evidence.
- This note does not use observed top mass or `y_t` as proof input.
- This note does not allow `H_unit` matrix-element definition as the `y_t`
  readout.
