# Route Portfolio

Scores use 0-3, with overclaim risk subtracted qualitatively.

| Route | Type | Claim-state upgrade | Import retirement | Artifactability | Risk | Decision |
|---|---|---:|---:|---:|---|---|
| Direct top-Ward lift audit for charged leptons | no-go / obstruction | 2 | 2 | 3 | low if framed as no-go | completed: direct lift closed |
| Promote `y_tau = alpha_LM/(4pi)` radiative support | support firewall | 2 | 1 | 3 | high: generation selector is absent | completed: support retained, standalone tau selector closed |
| Koide `Q` physical source-domain closure | constructive theorem | 3 | 2 | 2 | high: existing no-go ledger is dense | audited in cycle 3 as conditional support, not closure |
| Brannen selected-line endpoint closure | constructive/literature bridge | 3 | 2 | 1 | high: prior topology routes no-go | audited in cycle 3 as conditional support, not closure |
| Koide `Q` + Brannen phase as generation selector | no-go / support firewall | 2 | 2 | 3 | low if framed as no-go | completed: standalone selector closed |
| Unbased selected-line orbit as generation selector | no-go / endpoint-source firewall | 2 | 2 | 3 | low if framed as a basedness obstruction | completed: unbased orbit selector closed |
| OP-local `C3`-fixed Q source plus selected-line phase as generation selector | no-go / source-endpoint firewall | 2 | 2 | 3 | low if framed as a no-go under granted source support | completed: source-symmetric unbased selector closed |
| Full absolute mass chain note from existing support | packaging | 1 | 1 | 3 | high: could promote support-only work | reject as first move |
| Literature-only Koide/tau mass synthesis | literature bridge | 1 | 0 | 3 | medium: not a derivation | use only for context |

## Selected Route

**Route:** direct top-Ward lift audit for charged leptons.

**Reason:** The open lane names a `y_tau` Ward identity as the first
parallel-worker target. The one-Higgs gauge-selection theorem already says
the charged-lepton Yukawa matrix is arbitrary, but that has not been packaged
as an explicit retained-objective no-go against a direct top-Ward lift. A
clean obstruction here changes the lane state by preventing a false retained
upgrade and narrowing the exact missing primitive.

## Expected Artifact

- `scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py`
- `docs/CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`

The artifact should prove:

1. the gauge-allowed charged-lepton monomial admits any complex generation
   matrix `Y_e`;
2. one-Higgs gauge selection and retained electroweak charges do not select
   eigenvalues;
3. the top Ward identity depends on a color/isospin composite-Higgs singlet
   surface not shared by the colorless charged-lepton monomial;
4. therefore `y_tau` cannot be retained by direct gauge-selection/top-Ward
   analogy alone.

## Cycle 1 Outcome

The expected artifact was produced and verified:

```text
python3 scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py
TOTAL: PASS=26, FAIL=0
```

The next route is not a direct top-Ward lift. It is an audit of the
support-only `y_tau = alpha_LM/(4pi)` radiative route, with the burden on loop
completeness, normalization, and tau-generation selection.

## Cycle 2 Outcome

The radiative audit was produced and verified:

```text
python3 scripts/frontier_charged_lepton_radiative_tau_selector_firewall.py
TOTAL: PASS=17, FAIL=0
```

The scale `alpha_LM/(4pi)` remains useful support, but the charged-lepton
Casimir is generation-blind: `(C_e, C_mu, C_tau) = (1, 1, 1)`. The next route
must therefore attack the retained ratio/source-domain selector, not repackage
the radiative scale as a standalone tau theorem.

## Cycle 3 Outcome

The ratio/source selector audit was produced and verified:

```text
python3 scripts/frontier_charged_lepton_koide_ratio_source_selector_firewall.py
TOTAL: PASS=35, FAIL=0
```

The result is an exact negative boundary for the retained mass objective.
Koide `Q` support and Brannen/selected-line phase support remain useful, but
their combination does not supply a retained generation/tau-scale selector:
`Q` erases the selected-line phase, the physical `Q` source and Brannen
endpoint laws remain conditional, and cyclic relabelings preserve unordered
ratios while moving the largest component label.

The next route must name a genuinely new premise, such as a retained theorem
that the undeformed charged-lepton source is strict-onsite and `C3`-fixed, or
a based selected-line endpoint/generation law. Further value-matching on
`Q = 2/3` or `delta = 2/9` is rejected as low-value churn.

## Cycle 4 Outcome

The selected-line basedness audit was produced and verified:

```text
python3 scripts/frontier_charged_lepton_selected_line_generation_selector_no_go.py
TOTAL: PASS=38, FAIL=0
```

The result is a narrower no-go under granted non-PDG support values. An
unbased free `C3` orbit cannot select one physical generation label in a
`C3`-natural way. Based equivariant selectors exist, but there are three of
them, one for each basepoint choice, so choosing one is precisely the missing
physical endpoint/source/generation primitive.

The next route must derive or refute an actual based endpoint/source law or a
non-observational tau-scale/generation selector. Repeating `Q = 2/3`,
`delta = 2/9`, or unbased-orbit value matching is now closed.

## Cycle 5 Outcome

The OP-local source plus selected-line audit was produced and verified:

```text
python3 scripts/frontier_charged_lepton_op_local_source_selected_line_selector_no_go.py
TOTAL: PASS=48, FAIL=0
```

This cycle named the new premise that was unavailable to the original broad
ratio/source route: the conditional OP-local support
`P_SOURCE => z=0 => Q=2/3`. Granting that premise still does not produce a
retained generation/tau-scale selector. A `C3`-fixed onsite source is a common
scalar, so it cannot supply a distinguished generation label or a selected-line
basepoint. The combined data still require a based endpoint/source law or a
non-observational tau-scale selector.

Do not repeat OP-local source support plus unbased selected-line matching as a
new route. The remaining viable route must add a genuinely physical basepoint,
endpoint readout, source-domain exclusion of commutant `Z` with a base, or
generation/tau-scale law.
