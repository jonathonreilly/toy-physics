# Assumptions And Imports

**Workstream:** charged-lepton mass retirement  
**Target status:** retained absolute charged-lepton masses  
**Rule:** any retained objective must remove the 3-real PDG observational pin
currently used by the bounded package.

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| `m_e, m_mu, m_tau` PDG values | Existing bounded package pin and comparator | observational comparator / fitted pin | `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`; PDG 2024 lepton summary | yes in bounded package | yes, must be removed as derivation input | derive `y_tau`, derive ratios, then use PDG only as comparator | open blocker |
| Electroweak scale `v = 246.282818... GeV` | Ambient scale for charged-lepton masses | retained framework-derived | `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`, `docs/lanes/open_science/06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md` | yes | yes | already retained on repo surface | usable retained input |
| SM relation `M_e = Y_e v/sqrt(2)` or repo convention equivalent | Converts Yukawa eigenvalues into masses | admitted standard bridge | `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`; Weinberg 1967 SM lepton model | yes | yes | keep explicit; cannot determine eigenvalues | admitted bridge, not a mass derivation |
| One-Higgs gauge selection | Allows `bar L_L H e_R` and excludes crossed monomials | retained structural guardrail | `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` | yes | yes | already exact, but leaves `Y_e` free | usable guardrail only |
| `Y_e` generation matrix | Charged-lepton Yukawa eigenvalues | unsupported/free in SM gauge-selection theorem | `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`; `CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md` | yes | yes | needs new retained generation/loop/source primitive | open blocker; direct top-Ward lift closed |
| `y_tau = alpha_LM/(4pi)` | Candidate tau absolute-scale anchor | support-only scale, not standalone tau selector | `scripts/frontier_charged_lepton_radiative_yukawa_theorem.py`; `CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md`; Koide support stack | yes for tau-scale route | yes if retained | needs retained generation/source primitive to assign the scale to the tau eigenvalue without PDG input | support retained as comparator; standalone tau-selector promotion closed |
| Charged-lepton Koide `Q = 2/3` | Ratio constraint on mass-square-root vector | support/open | `KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md` | yes for `m_e/m_mu/m_tau` ratios | yes | source-domain physical-selection theorem | open blocker |
| Brannen phase / selected-line parameter | Second relation needed for the three ratios | support/open | `KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md` | yes for full ratio vector | yes | physical endpoint/readout theorem | open blocker |
| Koide `Q` plus Brannen phase as generation/tau-scale selector | Candidate route to assign ratio vector and radiative scale without PDG masses | exact negative boundary / support firewall | `CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md` | no standalone proof | no, route is closed without new primitive | requires a new physical source/endpoint/generation law; value matching is insufficient | no-go for standalone selector |
| Unbased selected-line/Brannen orbit as physical generation selector | Candidate route from ratio/phase support to a tau/e/mu label | exact negative boundary | `CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md` | no standalone proof | no, route is closed without a basepoint/source law | derive a retained based endpoint/source law or non-observational generation selector | no-go for unbased orbit selector |
| OP-local `C3`-fixed source plus selected-line/Brannen support as generation selector | Strongest current non-PDG `Q` premise combined with phase support | exact negative boundary under granted source support | `CHARGED_LEPTON_OP_LOCAL_SOURCE_SELECTED_LINE_SELECTOR_NO_GO_NOTE_2026-04-27.md`; `KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md` | no standalone proof | no, route is closed without a based endpoint/source/tau-scale law | derive an actual physical basepoint/source/generation theorem, not just `z=0` source erasure | no-go for source-symmetric unbased selector |
| Type-B-to-radian scalar readout plus OP-local `Q` source support as generation selector | Stronger Brannen-side premise: grant scalar `delta=2/9 rad` readout and `z=0 => Q=2/3` | exact negative boundary under granted scalar readout/source support | `CHARGED_LEPTON_TYPEB_RADIAN_READOUT_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md` | no standalone proof | no, route is closed without a based endpoint/source/tau-scale law | derive a based endpoint/source/generation law; scalar unit/readout law alone is insufficient | no-go for scalar readout generation selector |
| Non-observational generation label / tau-scale selector | Needed to attach the retained/support scale to a charged-lepton eigenvalue | open primitive | `CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md`; `CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md` | yes | yes | derive from source-domain, endpoint, or generation-label theorem | open blocker |
| Top Ward identity template `y_t/g_s = 1/sqrt(6)` | Candidate pattern for charged-lepton `y_tau` | retained for top sector only | `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`; `CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md` | no direct lepton proof | no unless lifted | direct lift tested and closed; only a new primitive could reopen a lepton-scale theorem | no-go for direct lift |
| Literature Koide formula | External context for charged-lepton mass relation | background context | Koide 1983 PRD via OSTI/APS DOI | no as derivation input | no | comparator/history only | disclosed literature |

## Retained Objective Gate

Retained absolute charged-lepton mass closure requires all of:

1. a retained `y_tau` or equivalent absolute-scale theorem;
2. retained dimensionless charged-lepton ratio structure, either through
   Koide `Q` plus selected-line phase or a different two-relation mechanism;
3. no use of PDG lepton masses except as comparators;
4. review-loop acceptance that no hidden selector, normalization, or observed
   target remains load-bearing.

The first execution cycle tested whether one-Higgs gauge selection plus the
top Ward template can directly force `y_tau`. It cannot. Gate 1 remains open
only through a new generation-selection, loop-normalization, or source-domain
primitive.

The second execution cycle tested whether the existing radiative
`alpha_LM/(4pi)` stack can serve as a standalone `y_tau` selector. It cannot:
the charged-lepton Casimir is generation-blind. The scale remains useful
support only after a separate retained generation/ratio primitive identifies
the tau eigenvalue.

The third execution cycle tested whether the current Koide `Q` support plus
selected-line/Brannen phase support can supply that retained generation
selector. It cannot on the current surface: `Q` erases the Brannen phase,
the `Q` source route is conditional on a still-open physical source premise,
the Brannen endpoint/radian readout remains open, and cyclic relabelings keep
the unordered ratio vector fixed while moving the largest slot label. PDG
charged-lepton masses remain comparator-only.

The fourth execution cycle sharpened the selected-line side. Even granting the
non-PDG support values, an unbased free `C3` orbit has no natural single-label
selector: no generation label is fixed by all cyclic relabelings, and the only
nonempty invariant label subset is the full generation orbit. Based
equivariant selectors exist, but the basepoint choice is exactly the still-open
physical endpoint/source/generation law.

The fifth execution cycle granted the strongest current OP-local `Q` support:
strict-onsite plus `C3`-fixed undeformed source implies `z = 0` and therefore
`Q = 2/3` on the admitted criterion carrier. This still does not supply a
generation selector. The source is a common scalar, so combining it with the
selected-line/Brannen phase leaves the same unbased orbit obstruction: cyclic
relabeling preserves the quotient data while moving every single generation
label.

The sixth execution cycle granted the stronger Brannen-side scalar readout
premise `P_RADIAN`, namely that the Type-B rational `2/9` is physically read as
`delta = 2/9 rad`, while also granting OP-local `z = 0 => Q = 2/3` support.
This still does not supply a generation selector. A scalar unit/readout law is
`C3`-fixed quotient data; it narrows the unit problem but does not provide a
selected-line basepoint or attach the heavy/middle/light profile to the
physical charged-lepton labels.
