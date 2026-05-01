# PR230 Top-Yukawa Physics-Loop Campaign Status Certificate

**Date:** 2026-05-01  
**Status:** open / campaign exhausted for current analytic shortcuts  
**Runner:** `scripts/frontier_yt_pr230_campaign_status_certificate.py`  
**Certificate:** `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: open
conditional_surface_status: conditional-support for future production evidence or new scalar-LSZ/heavy-matching theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Open imports remain across every non-production shortcut route."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

This note summarizes the current PR #230 physics-loop campaign.  It does not
claim retained closure.  It records which shortcut routes were tested and what
still remains.

## Runner Result

```text
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=20 FAIL=0
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

The campaign did not reach retained top-Yukawa closure.  It did retire the
visible shortcut routes:

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

## Non-Claims

- This note does not claim retained closure.
- This note does not demote PR #230's scout/proposed evidence.
- This note does not use observed top mass or `y_t` as proof input.
- This note does not allow `H_unit` matrix-element definition as the `y_t`
  readout.
