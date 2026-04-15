# Historical Frozen-Out Registry

**Date:** 2026-04-15
**Status:** historical publication registry; not part of the live front-door
read path
**Purpose:** explicit registry of significant work that exists in the repo but
is not promoted into the current flagship paper surface.

This file prevents two failure modes:

1. good work gets silently lost
2. unsafe work gets silently promoted

Every frozen-out family has:

- a reason it is not on the main paper surface
- a source branch/workstream
- a condition for re-entry

## Frozen-out families

### `F01` Dark-matter quantitative portfolio

**Status:** frozen out of the retained paper core; bounded companion only.  
**Why frozen out:** the structural DM ratio result is real, but full relic
mapping still depends on bounded transport / normalization steps.

**Captured work:**

- DM ratio `R = 5.48` vs `5.47`
- conditional `\Omega_b`, `\Omega_{\rm DM}`, `\Omega_m`, `\Omega_\Lambda` chain
- Sommerfeld, Stosszahlansatz, and graph-native relic sub-results

**Primary sources:**

- [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md)
- [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md)

**Needed to unfreeze:**

- internalize the remaining graph-to-relic bridge
- retire the remaining imported/assumed transport ingredients

### `F02` Superseded YT / EW / Higgs route-history stack

**Status:** frozen out as publication authority; retained only as route history.
**Why frozen out:** the old bounded `y_t` / `\alpha_s` and pre-final Higgs notes
were superseded by the complete prediction chain and its support stack.

**Captured work:**

- earlier zero-import `m_t = 169.4 GeV` route
- import-allowed `m_t \approx 171 GeV` companion route
- earlier bounded EW-normalization route notes
- pre-final Higgs/CW route notes that no longer define the promoted package

**Primary sources:**

- [COMPLETE_PREDICTION_CHAIN_2026_04_15.md](../../COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- superseded note history such as `YT_ZERO_IMPORT_CLOSURE_NOTE.md`,
  `YT_BOUNDARY_THEOREM.md`, `YT_EFT_BRIDGE_THEOREM.md`,
  `ALPHA_S_DERIVED_NOTE.md`, `YT_VERTEX_POWER_DERIVATION.md`,
  `YT_GAUGE_CROSSOVER_THEOREM.md`

**Needed to unfreeze:**

- nothing; this family is kept as history rather than a live promotion target

### `F03` Older CKM bounded route-history portfolio

**Status:** frozen out as superseded authority.
**Why frozen out:** the promoted CKM atlas/axiom closure package now controls
the live authority surface on `main`; the older bounded Cabibbo / mass-basis /
Jarlskog rows remain useful only as route history and comparison material.

**Captured work:**

- mass-basis NNI `|V_us|`, `|V_cb|`, `|V_ub|` package
- bounded Cabibbo companion on `main`
- bounded Jarlskog phase companion
- historical combined Cabibbo/Jarlskog route note
- multiple CKM route diagnostics, negative results, and sharpenings

**Primary sources:**

- promoted authority on `main`: `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`
- bounded historical companions on `main`: `CKM_MASS_BASIS_NNI_NOTE.md`,
  `CABIBBO_BOUND_NOTE.md`, `JARLSKOG_PHASE_BOUND_NOTE.md`
- work history: `CABIBBO_JARLSKOG_ROUTE_NOTE_2026-04-12.md`
- `codex/review-active`: bounded `CKM_*` notes

**Needed to unfreeze:**

- nothing; this family is retained only as superseded bounded route history

### `F04` Cosmology companion portfolio

**Status:** frozen out of the retained paper core; bounded/conditional companion only.  
**Why frozen out:** these results are interesting and sometimes very close to
observation, but they still consume topology, cosmology, or matching inputs
beyond the retained flagship backbone.

**Captured work:**

- cosmological constant `\Lambda`
- vacuum-energy no-go / UV-IR audit behind the `\Lambda` companion
- dark energy EOS `w = -1`
- `n_s`
- conditional `\Omega_\Lambda`
- graviton mass

**Primary sources:**

- [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md)
- [COSMOLOGICAL_CONSTANT_VACUUM_ENERGY_AUDIT_NOTE.md](../../COSMOLOGICAL_CONSTANT_VACUUM_ENERGY_AUDIT_NOTE.md)
- [DARK_ENERGY_EOS_NOTE.md](../../DARK_ENERGY_EOS_NOTE.md)
- [PRIMORDIAL_SPECTRUM_NOTE.md](../../PRIMORDIAL_SPECTRUM_NOTE.md)
- [GRAVITON_MASS_DERIVED_NOTE.md](../../GRAVITON_MASS_DERIVED_NOTE.md)
- [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md)

**Needed to unfreeze:**

- same-surface derivation of the remaining cosmological scale bridge
- closure of the matter-content bridge behind present-day `\Omega_\Lambda`
- removal of conditional input dependence where applicable

### `F05` Higgs and mass-spectrum companions beyond the promoted package

**Status:** frozen out of the retained paper core.  
**Why frozen out:** the promoted package now carries the accepted Higgs /
vacuum rows, but the broader mass-spectrum and neutrino programs remain outside
the flagship spine.

**Captured work:**

- Higgs mechanism support notes beyond the promoted package card
- neutrino hierarchy / spectrum notes
- generation-hierarchy and mass-spectrum notes

**Primary sources:**

- [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md)
- [HIGGS_MECHANISM_NOTE.md](../../HIGGS_MECHANISM_NOTE.md)
- [HIGGS_FROM_LATTICE_NOTE.md](../../HIGGS_FROM_LATTICE_NOTE.md)

**Needed to unfreeze:**

- same-surface mass-spectrum closure beyond the promoted package
- accepted neutrino closure if that program is later promoted

### `F06` Gravity companions beyond the retained core

**Status:** frozen out of the retained paper core.  
**Why frozen out:** the package now retains weak-field gravity and a restricted
strong-field theorem, but broader gravity phenomenology and full-generality GR
are still bounded.

**Captured work:**

- broader GR-signature bundle
- Born-gravity cross-constraint
- BMV / experimental prediction cards
- frozen-star / null-echo program
- full nonlinear GR / tensor-completion gap

**Primary sources:**

- gravity no-go and tensor-gap notes on `main`
- [ACCESSIBLE_PREDICTION_NOTE.md](../../ACCESSIBLE_PREDICTION_NOTE.md)
- [FROZEN_STARS_RIGOROUS_NOTE.md](../../FROZEN_STARS_RIGOROUS_NOTE.md)
- [GW_ECHO_NULL_RESULT_NOTE.md](../../GW_ECHO_NULL_RESULT_NOTE.md)

**Needed to unfreeze:**

- full tensor-valued matching/completion theorem for general strong-field GR

### `F08` Branch-local inventories and stale strategy docs

**Status:** frozen out as publication authority; retained only as branch-local inventory.  
**Why frozen out:** these files are useful for capture and planning, but they
mix retained, bounded, fitted, conditional, and stale claims.

**Captured work:**

- `STANDALONE_PREDICTIONS_INVENTORY_2026-04-12.md`
- `MASTER_DERIVATION_SCORECARD.md`
- `PAPER_STRATEGY_2026-04-12.md`
- older publication cards and review packets

**Primary sources:**

- local package inventories and historical branch capture retained only as
  non-authority history

**Needed to unfreeze:**

- rewrite as cleaned authority notes or incorporate claim-by-claim into the
  canonical matrix / ledger

## Registry rule

The flagship paper may reference frozen-out work only if:

1. it is clearly labeled as bounded / companion / later-paper material
2. it is already recorded in [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
3. the corresponding frozen-out family above is cited

If a result is too important to disappear but not safe to promote, it belongs
here.
