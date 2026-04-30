# Artifact Plan

**Slug:** axiom-to-main-lane-cascade-20260429
**Date:** 2026-04-29

For each science block, the deliverable is a coherent set of:

1. one theorem/support/no-go note (`docs/<TOPIC>_NOTE_2026-04-29.md` or
   similar), with claim-status firewall fields;
2. one paired runner script (`scripts/frontier_<topic>.py`) that checks the
   theorem's dependency classes (not just numerical output);
3. one paired output log (`outputs/frontier_<topic>_2026-04-29.txt`);
4. one branch-local `CLAIM_STATUS_CERTIFICATE.md` for the block;
5. one PR-body draft in `.claude/science/physics-loops/.../PR_BODY_BLOCKNN.md`.

## Block 1: Koide Q canonical-descent closure

**Branch:** `physics-loop/axiom-to-main-lane-cascade-20260429-block01-20260429`

**Files (planned):**
- `docs/KOIDE_Q_AXIOM_CYCLIC_LINE_CLOSURE_THEOREM_NOTE_2026-04-29.md`
- `scripts/frontier_koide_q_axiom_cyclic_line_closure.py`
- `outputs/frontier_koide_q_axiom_cyclic_line_closure_2026-04-29.txt`
- block certificate + PR body draft

**Acceptance:**
- proves `(Σ√x_i)^2 / (Σ x_i) = 3/2` from A_min + Q23 surface theorem
  + cubic Z_3 source rotation, with NO observed mass input;
- runner audits dependency classes (each load-bearing input is `zero-input
  structural`, `framework-derived`, or `retained support`);
- runner PASS=ALL FAIL=0;
- block-local `proposed_retained` allowed only if certificate passes.

**Honest stop conditions:**
- if R-Q1 walls and R-Q2/R-Q3 also wall → land structured no-go note +
  proceed to Block 2.
- if R-Q1 partially closes (e.g., proves source-free reduced carrier
  uniqueness but cannot fix Q value without further premise) → land
  exact-support note explicitly stating the residual.

## Block 2: Koide δ = 2/9 rad

**Branch:** `physics-loop/axiom-to-main-lane-cascade-20260429-block02-20260429`

**Files (planned):**
- `docs/KOIDE_DELTA_BERRY_HOLONOMY_CLOSURE_THEOREM_NOTE_2026-04-29.md`
- `scripts/frontier_koide_delta_berry_holonomy_closure.py`
- `outputs/frontier_koide_delta_berry_holonomy_closure_2026-04-29.txt`

**Acceptance:**
- derives `δ = 2/9 rad` from Berry holonomy on the cyclic Z_3 orbit of
  the source-free reduced carrier (uses Q1 closure or runs as a
  conditional theorem if Q1 lands as exact support only);
- explicit period convention forced by the source-free reduced carrier;
- runner PASS=ALL FAIL=0.

## Block 3: Quark mass-ratio first-principles endpoint chain

**Branch:** `physics-loop/axiom-to-main-lane-cascade-20260429-block03-20260429`

**Files (planned):**
- `docs/QUARK_MASS_RATIO_AXIOM_ENDPOINT_THEOREM_NOTE_2026-04-29.md`
- `scripts/frontier_quark_mass_ratio_axiom_endpoint.py`
- `outputs/frontier_quark_mass_ratio_axiom_endpoint_2026-04-29.txt`

**Acceptance:**
- proves an exact endpoint ratio chain for down-type masses from A_min +
  retained Wilson reduction stack (R-M1) OR
- proves cross-sector universality of Q1's source-domain readout for
  quarks (R-M2);
- closes or honestly bounds the +15% common-scale gap;
- runner PASS=ALL FAIL=0.

## Block 4: Cl_4(C) module derivation (Axiom*)

**Branch:** `physics-loop/axiom-to-main-lane-cascade-20260429-block04-20260429`

**Files (planned):**
- `docs/CL4C_MODULE_FROM_AXIOMS_DERIVATION_THEOREM_NOTE_2026-04-29.md`
  OR
- `docs/AXIOM_STACK_MINIMALITY_NO_GO_NOTE_2026-04-29.md`
- `scripts/frontier_cl4c_module_from_axioms_derivation.py`
- `outputs/frontier_cl4c_module_from_axioms_derivation_2026-04-29.txt`

**Acceptance:**
- EITHER derives Cl_4(C) module on `P_A H_cell` from A_min + retained
  anomaly-forced 3+1 + retained Hilbert i (R-A1), retiring Axiom* as a
  separate science decision;
- OR proves an exact no-go that A_min cannot generate irreducible
  Cl_4(C) on any quotient (R-A3), forcing Axiom* adoption as the unique
  minimal extension;
- runner PASS=ALL FAIL=0.

## Block 5: BH 1/4 carrier from framework Wald-Noether charge

**Branch:** `physics-loop/axiom-to-main-lane-cascade-20260429-block05-20260429`

**Files (planned):**
- `docs/BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`
- `scripts/frontier_bh_quarter_wald_noether_framework_carrier.py`
- `outputs/frontier_bh_quarter_wald_noether_framework_carrier_2026-04-29.txt`

**Acceptance:**
- derives `c_cell = 1/4` BH coefficient via `S_Wald = A·c_cell ↔
  S_BH = A/(4G)` matching, using retained Universal QG canonical action
  surface + retained PRIMITIVE_COFRAME_BOUNDARY_CARRIER theorem
  (R-B1);
- explicit dependency on Wald formula universality declared as
  admitted-context input;
- runner PASS=ALL FAIL=0.

## Block 6: DM η freezeout-bypass

**Branch:** `physics-loop/axiom-to-main-lane-cascade-20260429-block06-20260429`

**Files (planned):**
- `docs/DM_ETA_FRAMEWORK_NSITES_DERIVATION_THEOREM_NOTE_2026-04-29.md`
- `scripts/frontier_dm_eta_framework_nsites_derivation.py`
- `outputs/frontier_dm_eta_framework_nsites_derivation_2026-04-29.txt`

**Acceptance:**
- derives N_sites from retained 3-generation count + retained Oh
  automorphism order, computes m_DM = N_sites · v, compares to η_obs
  comparator with explicit derivation residual;
- runner PASS=ALL FAIL=0.

## Block 7 (if reached): Plaquette β=6 Perron

**Branch:** `physics-loop/axiom-to-main-lane-cascade-20260429-block07-20260429`

**Files (planned):**
- `docs/PLAQUETTE_BETA_6_PERRON_BOUNDARY_THEOREM_NOTE_2026-04-29.md`
- `scripts/frontier_plaquette_beta_6_perron_boundary.py`
- `outputs/frontier_plaquette_beta_6_perron_boundary_2026-04-29.txt`

**Acceptance:**
- explicit Perron eigenvector solve on `Z_6^env` representation OR
- structural analytic identification via spatial-environment
  tensor-transfer theorem (R-P2);
- runner PASS=ALL FAIL=0.

## Honest-status discipline

For every artifact:
- branch-local source-note `Status:` lines must use the controlled
  vocabulary: `proposed_retained`, `proposed_promoted`, `exact support`,
  `bounded support`, `conditional / support`, `open`, `no-go`,
  `demotion`, `hypothetical consequence map`.
- bare `retained` / `promoted` and `retained branch-local` are BANNED.
- `proposed_retained` / `proposed_promoted` allowed only with passing
  certificate + explicit independent-audit handoff.
