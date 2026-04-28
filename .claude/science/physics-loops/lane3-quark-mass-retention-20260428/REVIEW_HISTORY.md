# Lane 3 Review History

**Updated:** 2026-04-28T09:26:03Z

## Preflight Review

Scope reviewed:

- required physics-loop methodology docs;
- Lane 3 open-lane note;
- repo organization and controlled vocabulary;
- active review workflow and canonical harness index;
- Lane 3 quark firewall landed on current `origin/main`.

Findings:

1. The current repo already has an exact Lane 3 firewall: bounded companion
   matches are not retained five-mass closure.
2. The branch was behind `origin/main` by eight commits but had no committed
   divergence, so it was fast-forwarded to `e3c108de`.
3. The default automation lock path is unavailable for this SSH user with a
   permission error at `/Users/jonreilly`; the local lock is held under
   `/Users/jonBridger/.codex/memories/physics_worker_lock.json`, and the
   supervisor flock is active.

Disposition:

- proceed with block-local science artifacts only;
- do not update repo-wide authority surfaces;
- selected route is 3C-Q, an exact boundary/no-go for direct
  generation-stratified quark Ward identities under current primitives.

## Artifact Review: 3C-Q Direct Quark Ward Boundary

**Time:** 2026-04-28T07:37:31Z

Artifact reviewed:

- `docs/QUARK_GENERATION_STRATIFIED_WARD_FREE_MATRIX_NO_GO_NOTE_2026-04-28.md`
- `scripts/frontier_quark_generation_stratified_ward_free_matrix_no_go.py`
- `logs/2026-04-28-quark-generation-stratified-ward-free-matrix-no-go.txt`

Verification:

```text
python3 scripts/frontier_quark_generation_stratified_ward_free_matrix_no_go.py
TOTAL: PASS=42, FAIL=0

python3 -m py_compile scripts/frontier_quark_generation_stratified_ward_free_matrix_no_go.py
PASS

python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0

python3 scripts/frontier_quark_mass_ratio_review.py
TOTAL: PASS=46, FAIL=0
```

Review-loop emulation:

1. Claim wording is bounded to an exact negative boundary for direct 3C; it
   does not claim retained non-top quark masses.
2. The runner uses field charges, generation-blind gauge action, top Ward
   block dimension, and a same-CKM/two-spectrum SVD witness; observed quark
   masses are not proof inputs.
3. The theorem is compatible with the 2026-04-27 Lane 3 firewall and narrows
   the species-differentiated Ward residual.

Disposition:

- keep artifact;
- claim status remains `open`;
- continue into a 3B route-2 endpoint stretch because one no-go/boundary cycle
  has now landed and runtime remains.

## Artifact Review: 3B-R2 Route-2 E-Channel Naturality

**Time:** 2026-04-28T07:43:21Z

Artifact reviewed:

- `docs/QUARK_ROUTE2_E_CHANNEL_READOUT_NATURALITY_NO_GO_NOTE_2026-04-28.md`
- `scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py`
- `logs/2026-04-28-quark-route2-e-channel-readout-naturality-no-go.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py
TOTAL: PASS=28, FAIL=0

python3 -m py_compile scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_exact_readout_map.py
PASS=11 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_exact_time_coupling.py
PASS=8 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_endpoint_ratio_chain_law.py
PASS=14 FAIL=0
```

Review-loop emulation:

1. Claim wording is correctly bounded to a minimal-naturality no-go. It does
   not claim an up-type retained scalar law.
2. The runner proves `rho_E` remains free under exact carrier columns,
   endpoint algebra, and granted T-side candidates.
3. The runner classifies the nearest-rational `21/4` selection as bounded
   endpoint-distance evidence rather than derivation.
4. The stuck fan-out is explicit across carrier-only, T-side transfer,
   symmetry/naturality, small-rational, and endpoint-ratio-chain frames.

Disposition:

- keep artifact;
- claim status remains `open`;
- next exact Lane 3 target is the E-center source/readout primitive, especially
  a theorem for `gamma_T(center)/gamma_E(center) = -8/9`, or a broader no-go
  showing endpoint-only naturality cannot select it.

## Artifact Review: 3B-R2-Rconn Center-Ratio Bridge

**Time:** 2026-04-28T07:59:31Z

Artifact reviewed:

- `docs/QUARK_ROUTE2_RCONN_CENTER_RATIO_BRIDGE_OBSTRUCTION_NOTE_2026-04-28.md`
- `scripts/frontier_quark_route2_rconn_center_ratio_bridge_obstruction.py`
- `logs/2026-04-28-quark-route2-rconn-center-ratio-bridge-obstruction.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_route2_rconn_center_ratio_bridge_obstruction.py
TOTAL: PASS=26, FAIL=0

python3 -m py_compile scripts/frontier_quark_route2_rconn_center_ratio_bridge_obstruction.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_exact_readout_map.py
PASS=11 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py
TOTAL: PASS=28, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_endpoint_ratio_chain_law.py
PASS=14 FAIL=0
```

Review-loop emulation:

1. The note uses `R_conn=8/9` only as a retained-support conditional bridge
   candidate; it does not treat the numeric coincidence as a derivation.
2. The runner proves the exact implication
   `c_TE=-R_conn => q_E=15/8 => rho_E=21/4`.
3. The runner also proves the import boundary: current Route-2 carrier columns
   do not type a color-projection/source-domain map to the E/T center endpoint
   ratio.
4. No observed quark masses, fitted Yukawa values, or CKM/J target errors are
   proof inputs.

Disposition:

- keep artifact;
- claim status remains `open`;
- stacked review PR opened: https://github.com/jonathonreilly/cl3-lattice-framework/pull/101;
- next exact Lane 3 target is a typed source-domain theorem deriving
  `gamma_T(center)/gamma_E(center) = -R_conn`, or an orthogonal 3A down-type
  local theorem target if the next fan-out route shifts away from 3B.

## Artifact Review: 3B-R2-Source Typed Bridge Inventory

**Time:** 2026-04-28T08:14:45Z

Artifact reviewed:

- `docs/QUARK_ROUTE2_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md`
- `scripts/frontier_quark_route2_source_domain_bridge_no_go.py`
- `logs/2026-04-28-quark-route2-source-domain-bridge-no-go.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_route2_source_domain_bridge_no_go.py
TOTAL: PASS=33, FAIL=0

python3 -m py_compile scripts/frontier_quark_route2_source_domain_bridge_no_go.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_rconn_center_ratio_bridge_obstruction.py
TOTAL: PASS=26, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py
TOTAL: PASS=28, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_exact_readout_map.py
PASS=11 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_endpoint_ratio_chain_law.py
PASS=14 FAIL=0

python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0

python3 scripts/frontier_quark_mass_ratio_review.py
TOTAL: PASS=46, FAIL=0
```

Review-loop emulation:

1. Claim wording is bounded to an exact current-bank no-go / exact negative
   boundary. It does not claim a retained up-type scalar law or retained
   non-top quark masses.
2. The runner proves the conditional algebra remains exact: adding
   `gamma_T(center)/gamma_E(center) = -R_conn` forces
   `beta_E/alpha_E = 21/4`.
3. The runner also proves the current typed-edge inventory has no path from
   `su3_R_conn_8_9` to `route2_rho_E_21_4` unless exactly that missing bridge
   is added.
4. Observed quark masses, fitted Yukawa entries, CKM/J target minimization,
   live endpoint nearest-rational selection, and untyped color-to-endpoint
   identification are all excluded as proof inputs.

Disposition:

- keep artifact;
- claim status remains `open`;
- stacked review PR opened: https://github.com/jonathonreilly/cl3-lattice-framework/pull/102;
- next exact Lane 3 action requires genuinely new source-domain theorem
  content, an alternate 3B readout primitive, or a sharp 3A local theorem.

## Artifact Review: 3A Five-Sixths Scale-Selection Boundary

**Time:** 2026-04-28T08:26:17Z

Artifact reviewed:

- `docs/QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md`
- `scripts/frontier_quark_five_sixths_scale_selection_boundary.py`
- `logs/2026-04-28-quark-five-sixths-scale-selection-boundary.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_five_sixths_scale_selection_boundary.py
TOTAL: PASS=34, FAIL=0

python3 -m py_compile scripts/frontier_quark_five_sixths_scale_selection_boundary.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_ckm_five_sixths_bridge_support.py
EXACT PASS=5, BOUNDED PASS=7, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_mass_ratios_taste_staircase_support.py
TOTAL: PASS=55, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0
```

Review-loop emulation:

1. Claim wording is correctly bounded to an exact negative boundary /
   theorem-target isolation for 3A. It does not claim retained `m_d`, `m_s`,
   or `m_b`.
2. The runner keeps PDG masses and one-loop `alpha_s` values in the inherited
   comparator/transport context; they are not derivation inputs.
3. The theorem distinguishes the exact Casimir rational `C_F - T_F = 5/6`
   from the missing non-perturbative exponentiation and scale-selection
   theorems.
4. The decisive obstruction is numerical and structural: `p_self =
   0.832890...` is close to `5/6`, but `p_same = 0.803802...`; the same fixed
   exponent cannot be exact on both scale surfaces because the inherited
   transport factor is nontrivial.

Disposition:

- keep artifact;
- claim status remains `open`;
- next exact Lane 3 action requires either a genuine 3A NP exponentiation plus
  scale-selection theorem, a new 3B source/readout primitive, or a new 3C
  species-differentiated Ward primitive.

## Artifact Review: 3C Generation-Equivariant Ward Degeneracy

**Time:** 2026-04-28T08:35:11Z

Artifact reviewed:

- `docs/QUARK_GENERATION_EQUIVARIANT_WARD_DEGENERACY_NO_GO_NOTE_2026-04-28.md`
- `scripts/frontier_quark_generation_equivariant_ward_degeneracy_no_go.py`
- `logs/2026-04-28-quark-generation-equivariant-ward-degeneracy-no-go.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_generation_equivariant_ward_degeneracy_no_go.py
TOTAL: PASS=44, FAIL=0

python3 -m py_compile scripts/frontier_quark_generation_equivariant_ward_degeneracy_no_go.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_s3_action_taste_cube_decomposition.py
TOTAL: PASS=57, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_generation_stratified_ward_free_matrix_no_go.py
TOTAL: PASS=42, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_three_generation_observable_theorem.py
TOTAL: PASS=47, FAIL=0
```

Review-loop emulation:

1. Claim wording is bounded to an exact negative boundary for the
   generation-equivariant 3C route. It does not claim retained non-top quark
   masses.
2. The runner proves the `S_3` commutant on the triplet has form `a I + b J`
   and gives an `E` double degeneracy, so the retained carrier alone cannot
   yield three generation-stratified Ward eigenvalues.
3. The runner explicitly shows that a `C_3` oriented example can split three
   eigenvalues only after reflection breaking; that is recorded as a possible
   future source/readout premise, not as current retained support.
4. Observed quark masses, fitted Yukawa entries, CKM eigenvalue input, and
   hidden generation projectors are excluded from the proof.

Disposition:

- keep artifact;
- claim status remains `open`;
- next 3C progress requires a named source/readout/symmetry-breaking primitive
  that orients or splits the retained generation triplet.

## Artifact Review: 3C Oriented `C3` Ward Splitter

**Time:** 2026-04-28T08:46:53Z

Artifact reviewed:

- `docs/QUARK_C3_ORIENTED_WARD_SPLITTER_SUPPORT_NOTE_2026-04-28.md`
- `scripts/frontier_quark_c3_oriented_ward_splitter_support.py`
- `logs/2026-04-28-quark-c3-oriented-ward-splitter-support.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_c3_oriented_ward_splitter_support.py
TOTAL: PASS=51, FAIL=0

python3 -m py_compile scripts/frontier_quark_c3_oriented_ward_splitter_support.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_generation_equivariant_ward_degeneracy_no_go.py
TOTAL: PASS=44, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_three_generation_observable_theorem.py
TOTAL: PASS=47, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_z2_hw1_mass_matrix_parametrization.py
TOTAL: PASS=10, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_s3_mass_matrix_no_go.py
TOTAL: PASS=13, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_s3_action_taste_cube_decomposition.py
TOTAL: PASS=57, FAIL=0
```

Review-loop emulation:

1. Claim wording is bounded to exact support/boundary for the missing 3C
   source/readout primitive. It does not claim retained non-top quark masses.
2. The runner proves the complete `C3`-equivariant Hermitian normal form
   `W(a,b,c) = a I + b(C+C^2) + c(C-C^2)/(i sqrt(3))`.
3. The reflection-odd coefficient `c` generically splits the block-05
   `S_3` doublet, but `a,b,c` remain free and the physical quark-Yukawa
   readout is not derived.
4. The runner checks the generation-basis diagonal boundary: a diagonal
   `C3`-equivariant readout is scalar, so the split is in cyclic Fourier
   channels unless a future readout theorem says otherwise.
5. Observed quark masses, fitted Yukawa entries, CKM eigenvalue input,
   endpoint nearest-rational selectors, and hidden generation projectors are
   excluded from the proof.

Disposition:

- keep artifact;
- claim status remains `open`;
- stacked review PR opened: https://github.com/jonathonreilly/cl3-lattice-framework/pull/105;
- next 3C progress requires a physical source law for `c` and the remaining
  Ward coefficients, or a readout theorem mapping the cyclic Fourier strata
  to quark Yukawa channels.

## Artifact Review: 3C `C3` Circulant Source-Law Boundary

**Time:** 2026-04-28T09:00:43Z

Artifact reviewed:

- `docs/QUARK_C3_CIRCULANT_SOURCE_LAW_BOUNDARY_NOTE_2026-04-28.md`
- `scripts/frontier_quark_c3_circulant_source_law_boundary.py`
- `logs/2026-04-28-quark-c3-circulant-source-law-boundary.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_c3_circulant_source_law_boundary.py
TOTAL: PASS=43, FAIL=0

python3 -m py_compile scripts/frontier_quark_c3_circulant_source_law_boundary.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_yt_generation_hierarchy_primitive.py
RESULT: PASS=51, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_class_6_c3_breaking.py
RESULT: PASS=43, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_koide_circulant_character_bridge.py
PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_koide_sqrtm_amplitude_principle.py
PASS=11 FAIL=0
```

Review-loop emulation:

1. Claim wording is bounded to exact support/boundary for a future 3C
   source-law theorem. It does not claim retained non-top quark masses.
2. The runner proves the Hermitian `C3` circulant family can represent any
   real generation spectrum, so carrier status alone is not predictive.
3. A1/P1 are kept as inherited support/open primitives: A1 gives `Q=2/3` for
   amplitude triples, while P1 still requires a positive parent/readout
   theorem for the physical quark Yukawa amplitudes.
4. Species phases, relative scales, and the amplitude-vs-Yukawa dictionary
   remain open quark-specific theorem content.
5. Observed quark masses, fitted Yukawa entries, CKM mass inputs,
   charged-lepton phase import, and hidden species selectors are excluded
   from the proof.

Disposition:

- keep artifact;
- claim status remains `open`;
- stacked review PR opened: https://github.com/jonathonreilly/cl3-lattice-framework/pull/106;
- next exact Lane 3 action requires deriving A1/equivalent source ratio, a
  P1-style quark positive parent/readout theorem, sector-specific phases and
  scales, a genuine 3A exponent/scale theorem, or a new 3B scalar/readout
  primitive.

## Artifact Review: 3C A1 Source-Domain Bridge No-Go

**Time:** 2026-04-28T09:08:58Z

Artifact reviewed:

- `docs/QUARK_C3_A1_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md`
- `scripts/frontier_quark_c3_a1_source_domain_bridge_no_go.py`
- `logs/2026-04-28-quark-c3-a1-source-domain-bridge-no-go.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_c3_a1_source_domain_bridge_no_go.py
TOTAL: PASS=50, FAIL=0

python3 -m py_compile scripts/frontier_quark_c3_a1_source_domain_bridge_no_go.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_koide_q_bridge_single_primitive.py
PASSED: 10/10

PYTHONPATH=scripts python3 scripts/frontier_koide_a1_lie_theoretic_triple_match.py
PASSED: 10/10

PYTHONPATH=scripts python3 scripts/frontier_koide_circulant_character_bridge.py
PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_c3_circulant_source_law_boundary.py
TOTAL: PASS=43, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_sm_one_higgs_yukawa_gauge_selection.py
TOTAL: PASS=43, FAIL=0
```

Review-loop emulation:

1. Claim wording is bounded to an exact current-bank no-go / support boundary.
   It does not claim retained non-top quark masses.
2. The runner proves A1 algebra is exact on a `C3` circulant carrier and that
   existing Koide support faces all hit `1/2`.
3. The typed-edge inventory has no path from A1 support faces to the physical
   quark `C3` Ward source ratio; adding exactly that edge creates the path.
4. The missing edge is therefore new theorem content, not latent support.
5. Observed quark masses, fitted Yukawa entries, CKM mass input,
   charged-lepton A1 physical bridge import, and hidden quark block-extremum
   assumptions are excluded from the proof.

Disposition:

- keep artifact;
- claim status remains `open`;
- stacked review PR opened: https://github.com/jonathonreilly/cl3-lattice-framework/pull/107;
- next exact Lane 3 action requires a typed quark source-domain theorem for
  A1, an alternate source ratio, a P1/readout theorem plus sector phase/scale
  laws, a genuine 3A scale theorem, or a new 3B scalar/readout primitive.

## Artifact Review: 3C P1 Positive-Parent Readout No-Go

**Time:** 2026-04-28T09:16:23Z

Artifact reviewed:

- `docs/QUARK_C3_P1_POSITIVE_PARENT_READOUT_NO_GO_NOTE_2026-04-28.md`
- `scripts/frontier_quark_c3_p1_positive_parent_readout_no_go.py`
- `logs/2026-04-28-quark-c3-p1-positive-parent-readout-no-go.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_c3_p1_positive_parent_readout_no_go.py
TOTAL: PASS=54, FAIL=0

python3 -m py_compile scripts/frontier_quark_c3_p1_positive_parent_readout_no_go.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_koide_sqrtm_amplitude_principle.py
PASS=11 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_c3_circulant_source_law_boundary.py
TOTAL: PASS=43, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_c3_a1_source_domain_bridge_no_go.py
TOTAL: PASS=50, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_sm_one_higgs_yukawa_gauge_selection.py
TOTAL: PASS=43, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_koide_circulant_character_bridge.py
PASS=9 FAIL=0
```

Review-loop emulation:

1. Claim wording is bounded to an exact current-bank no-go / support boundary.
   It does not claim retained non-top quark masses.
2. The runner proves the positive-parent square-root algebra is exact and
   `C3` covariance is preserved by the square root.
3. The runner also proves the dictionary can represent arbitrary positive
   triples once a parent is supplied, so it is not predictive by itself.
4. The typed-edge inventory lacks both a physical quark positive parent and a
   readout theorem from square-root spectrum to quark Yukawa amplitudes.
5. Observed quark masses, fitted Yukawa entries, CKM mass input,
   charged-lepton parent import, and hidden quark parent/readout assumptions
   are excluded from the proof.

Disposition:

- keep artifact;
- claim status remains `open`;
- stacked review PR opened: https://github.com/jonathonreilly/cl3-lattice-framework/pull/108;
- next exact Lane 3 action requires a physical quark parent/readout theorem,
  sector phase/scale law, alternate source/readout route, genuine 3A scale
  theorem, or new 3B scalar/readout primitive.

## Artifact Review: 3B RPSR Up-Amplitude Mass-Retention Boundary

**Time:** 2026-04-28T09:26:03Z

Artifact reviewed:

- `docs/QUARK_UP_AMPLITUDE_RPSR_MASS_RETENTION_BOUNDARY_NOTE_2026-04-28.md`
- `scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py`
- `logs/2026-04-28-quark-up-amplitude-rpsr-mass-retention-boundary.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py
TOTAL: PASS=50, FAIL=0

python3 -m py_compile scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_strc_lo_collinearity_theorem.py
PASS=12 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_rpsr_conditional.py
PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_projector_parameter_audit.py
TOTAL: PASS=6, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_bicac_endpoint_obstruction_theorem.py
PASS=12 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0
```

Review-loop emulation:

1. Claim wording is bounded to exact 3B up-amplitude support/boundary.
2. The runner verifies exact STRC/RPSR algebra and the reduced amplitude
   `a_u = 0.7748865611...`.
3. The runner blocks direct promotion from `a_u` to `m_u/m_c`, `m_c/m_t`, or
   non-top masses without a typed amplitude-to-Yukawa readout theorem.
4. Observed quark masses, fitted Yukawa entries, CKM mass input,
   amplitude-as-mass shortcut, and species-uniform top Ward import are
   excluded from the proof.

Disposition:

- keep artifact;
- claim status remains `open`;
- stacked review PR opened: https://github.com/jonathonreilly/cl3-lattice-framework/pull/109;
- next exact Lane 3 action requires an amplitude-to-Yukawa readout theorem,
  sector/scale bridge, 3C source/readout theorem, 3A scale theorem, or new 3B
  scalar/readout primitive.

## Artifact Review: 3B RPSR Single-Scalar Readout Underdetermination

**Time:** 2026-04-28T09:35:38Z

Artifact reviewed:

- `docs/QUARK_RPSR_SINGLE_SCALAR_READOUT_UNDERDETERMINATION_NOTE_2026-04-28.md`
- `scripts/frontier_quark_rpsr_single_scalar_readout_underdetermination.py`
- `logs/2026-04-28-quark-rpsr-single-scalar-readout-underdetermination.txt`

Verification:

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_rpsr_single_scalar_readout_underdetermination.py
TOTAL: PASS=80, FAIL=0

python3 -m py_compile scripts/frontier_quark_rpsr_single_scalar_readout_underdetermination.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py
TOTAL: PASS=50, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_rpsr_conditional.py
PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_sm_one_higgs_yukawa_gauge_selection.py
TOTAL: PASS=43, FAIL=0
```

Review-loop emulation:

1. Claim wording is bounded to exact readout underdetermination, not retained
   up-type mass closure.
2. The runner verifies the exact block-10 RPSR scalar and shows that a
   scale-covariant power readout `R_{p,q}(a_u)` admits a continuum of ordered
   ratio pairs for the same scalar.
3. Synthetic ratio-pair reconstruction demonstrates fit-capacity, not
   prediction: choosing `p` and `q` is an additional readout theorem.
4. The typed-edge inventory has no path from the RPSR scalar to physical
   up-type ratio pair without readout functions, generation-gap assignment,
   and sector/scale bridge.
5. Observed quark masses, fitted Yukawa entries, CKM singular values, hidden
   exponent selectors, hidden generation-gap assignment, and species-uniform
   top Ward import are excluded from the proof.

Disposition:

- keep artifact;
- claim status remains `open`;
- stacked review PR pending packaging;
- next exact Lane 3 action requires a derived two-ratio readout law,
  generation/source assignment, sector/scale bridge, 3C source/readout
  theorem, 3A scale theorem, or new 3B scalar/readout primitive.
