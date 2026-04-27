# Charged-Lepton Mass Retirement Handoff

**Branch:** `frontier/charged-lepton-mass-retirement-20260426`

**Target:** retained charged-lepton mass closure, specifically removal of the
3-real PDG observational pin behind the bounded charged-lepton mass package.

## Current State

Cycles 1-3 are complete. The cooperative lock script is unavailable due to a
`/Users/jonreilly` permission error, so the run is isolated on the dedicated
science branch.

The first completed artifact is an exact retained-objective no-go:

- `docs/CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`
- `scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py`

The runner proves that one-Higgs gauge selection permits `bar L_L H e_R` but
leaves the full charged-lepton matrix `Y_e` free. The top Ward
`1/sqrt(6)` normalization is tied to a top-sector color x isospin `Q_L`
surface and does not transfer to the colorless charged-lepton monomial without
adding a new generation/source primitive.

The second completed artifact is a support firewall:

- `docs/CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md`
- `scripts/frontier_charged_lepton_radiative_tau_selector_firewall.py`

It preserves `alpha_LM/(4pi)` as useful charged-lepton scale support, but
blocks its promotion to a standalone retained `y_tau` theorem because the
charged-lepton electroweak Casimir is generation-blind:

```text
(C_e, C_mu, C_tau) = (1, 1, 1)
```

The third completed artifact is a ratio/source selector firewall:

- `docs/CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md`
- `scripts/frontier_charged_lepton_koide_ratio_source_selector_firewall.py`

It blocks promotion of existing Koide `Q` support plus Brannen/selected-line
phase support into a retained generation/tau-scale selector. The runner checks
that `Q` erases the selected-line phase, the `Q` source law and Brannen
endpoint remain conditional, cyclic relabelings preserve unordered ratios
while moving the largest slot label, and PDG charged-lepton masses are only
comparators.

## Verification

```text
python3 -m py_compile scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py scripts/frontier_charged_lepton_radiative_tau_selector_firewall.py scripts/frontier_charged_lepton_koide_ratio_source_selector_firewall.py
PASS

python3 scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py
TOTAL: PASS=26, FAIL=0

python3 scripts/frontier_charged_lepton_radiative_tau_selector_firewall.py
TOTAL: PASS=17, FAIL=0

python3 scripts/frontier_charged_lepton_koide_ratio_source_selector_firewall.py
TOTAL: PASS=35, FAIL=0
```

Review-loop was emulated for cycle 3 and recorded in `REVIEW_HISTORY.md`.
Disposition: `PASS WITH BOUNDED/NO-GO CLAIMS`; mass retirement remains open.

## Next Exact Action

Only continue with a genuinely new physical premise. The next exact action is
to derive or refute one of:

- the physical charged-lepton undeformed scalar source is strict-onsite and
  `C3`-fixed;
- the selected-line Brannen endpoint has a based/unit-preserving
  Type-B-to-radian readout;
- a non-observational generation/tau-scale selector ties the ratio vector to
  the radiative scale support.

Do not repeat `Q = 2/3` or `delta = 2/9` value-matching without one of those
new premises. Retained charged-lepton mass closure is not achieved.
