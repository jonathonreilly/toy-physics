# Full Claim Ledger

**Date:** 2026-04-13  
**Purpose:** repo-wide publication ledger for the current `Cl(3)` / `Z^3`
program. Every paper-facing claim should land in one of the buckets below:

- `promoted`
- `bounded/open`
- `candidate-missed`
- `off-scope historical`
- `stale / not-for-paper`

This file is stricter than a backlog and broader than the retained paper
surface. It exists so claims are not silently lost between `review-active`,
`publication-prep`, `main`, and the Claude worktree.

## Bucket rules

### `promoted`

The claim is part of the current flagship paper surface or an exact supporting
theorem that the paper can cite directly.

### `bounded/open`

The claim is scientifically useful, but the paper must carry it with explicit
limitations or leave it out of the retained backbone.

### `candidate-missed`

The claim looks important enough that it should not be forgotten, but it is not
yet fully promoted into the public paper surface. These are the main audit
targets when branches drift.

### `off-scope historical`

The claim may matter for companion papers or repo history, but it should not be
treated as part of the flagship manuscript.

### `stale / not-for-paper`

The file is overclaiming, duplicated, or obsolete as publication authority.
Keep it in the repo if useful, but do not cite it in the paper path.

## 1. Flagship promoted claims

| Claim | Status | Placement | Authority | Runner / evidence |
|---|---|---|---|---|
| `Cl(3)` on `Z^3` is the physical theory | promoted | main text | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | framework statement |
| Single-axiom Hilbert/locality reduction | promoted as SI framing, not as the main theorem surface | SI framing only | [SINGLE_AXIOM_HILBERT_NOTE.md](../../SINGLE_AXIOM_HILBERT_NOTE.md), [SINGLE_AXIOM_INFORMATION_NOTE.md](../../SINGLE_AXIOM_INFORMATION_NOTE.md) | `frontier_single_axiom_hilbert.py`, `frontier_single_axiom_information.py` |
| Weak-field gravity from the Poisson/Newton chain | promoted | main text | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | [SELF_CONSISTENCY_FORCES_POISSON_NOTE.md](../../SELF_CONSISTENCY_FORCES_POISSON_NOTE.md), [POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md](../../POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md), [NEWTON_LAW_DERIVED_NOTE.md](../../NEWTON_LAW_DERIVED_NOTE.md) |
| Weak-field WEP from the derived lattice action | promoted weak-field corollary | main text or Extended Data corollary | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md), [GRAVITY_CLEAN_DERIVATION_NOTE.md](../../GRAVITY_CLEAN_DERIVATION_NOTE.md) | `frontier_broad_gravity.py` |
| Weak-field gravitational time dilation on the retained Poisson/Newton surface | promoted weak-field corollary | main text or Extended Data corollary | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md), [GRAVITY_CLEAN_DERIVATION_NOTE.md](../../GRAVITY_CLEAN_DERIVATION_NOTE.md) | `frontier_broad_gravity.py` |
| Exact native `SU(2)` from cubic `Cl(3)` | promoted | main text | [BOUNDED_NATIVE_GAUGE_NOTE.md](../../BOUNDED_NATIVE_GAUGE_NOTE.md) | `frontier_non_abelian_gauge.py` |
| Graph-first structural `SU(3)` | promoted | main text | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | `frontier_graph_first_su3_integration.py` |
| Left-handed `+1/3` / `-1` charge matching | promoted corollary | main text or SI corollary | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | `frontier_graph_first_su3_integration.py` |
| Anomaly-forced `3+1` closure | promoted | main text | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md) | `frontier_anomaly_forces_time.py` |
| Full-framework one-generation matter closure | promoted | main text | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | `frontier_right_handed_sector.py` |
| Three-generation matter structure in the framework | promoted | main text | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | `frontier_generation_fermi_point.py`, `frontier_generation_rooting_undefined.py`, `frontier_generation_axiom_boundary.py` |
| Exact `I_3 = 0` / no third-order interference | promoted exact companion | main text or Extended Data | [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md) | `frontier_born_rule_derived.py` |
| Exact CPT on the free staggered lattice | promoted exact companion | main text or Extended Data | [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md) | `frontier_cpt_exact.py` |

## 2. Live flagship gates

| Claim family | Status | Why not promoted yet | Authority |
|---|---|---|---|
| `S^3` compactification / topology closure | bounded/open | cap-map and cap-link work materially improve the lane, but the full topology closure still does not clear the paper bar | bounded `S3_*` notes on `review-active` and `youthful-neumann` |
| DM relic mapping | bounded/open | direct lattice enhancement is real; Stosszahlansatz / Boltzmann / Friedmann / relic bridge remain bounded at the paper bar | bounded `DM_*` notes on `review-active` and `youthful-neumann` |
| Renormalized `y_t` matching | bounded/open | UV theorem surface is strong; low-energy running / `alpha_s(M_Pl)` / matching still depend on bounded bridge structure | bounded `YT_*` notes on `review-active` and `youthful-neumann` |
| CKM / quantitative flavor closure | bounded/open | overnight NNI / coefficient work improves the fit, but Higgs `Z_3` universality and ab initio coefficient closure still do not clear the bar | bounded `CKM_*` notes on `review-active` and `youthful-neumann` |

## 3. Candidate-missed claims from the full audit

These are claims that do not belong in the “forgotten” bucket. They need an
explicit paper decision even if the answer is “bounded only.”

| Claim | Current decision | Why it is in this bucket | Primary sources |
|---|---|---|---|
| Residual weak-field GR-signature bundle (conformal metric, geodesic, light bending) | keep as bounded support, not retained backbone | the action-level chain is stronger now, but these steps still consume continuum / null-identification structure beyond the retained weak-field corollaries | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md), [EMERGENT_GR_SIGNATURES_NOTE.md](../../EMERGENT_GR_SIGNATURES_NOTE.md), [GEODESIC_EQUATION_NOTE.md](../../GEODESIC_EQUATION_NOTE.md) |
| Strong-field GR extension | bounded only | useful extension path, not a paper-safe closure surface | [STRONG_FIELD_EXTENSION_NOTE.md](../../STRONG_FIELD_EXTENSION_NOTE.md) |
| Gauge-coupling normalization (`g_bare`, `g_2`, `U(1)`) | bounded only | several notes exist, but the normalization vulnerability is still real | [G_BARE_DERIVATION_NOTE.md](../../G_BARE_DERIVATION_NOTE.md), [G2_EQUAL_PARTITION_BOUNDED_NOTE.md](../../G2_EQUAL_PARTITION_BOUNDED_NOTE.md) |
| Cosmology companions (`w=-1`, graviton mass, `Omega_Lambda`, `n_s`) | bounded / conditional companion only | good signals, but they sit on bounded topology / imported cosmology inputs | [W_MINUS_ONE_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/W_MINUS_ONE_NOTE.md), [GRAVITON_MASS_DERIVED_NOTE.md](../../GRAVITON_MASS_DERIVED_NOTE.md), [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md) |
| Newton / gravity title claim in the letter | promote weak-field only | the paper had drifted into omitting gravity entirely; the audit says weak-field Newton/Poisson belongs back, while the broader GR claim must stay narrower | authority docs above |
| Higgs / Coleman-Weinberg mass lane | bounded companion only | the structural Higgs mechanism and hierarchy result are real, but `m_H = 125 GeV` still needs bounded SM/Yukawa input | `claude/youthful-neumann: docs/HIGGS_MASS_DERIVED_NOTE.md`, `scripts/frontier_higgs_mass_derived.py` |
| Proton lifetime prediction | bounded companion only | sharp falsifiable prediction, but it still depends on imported EFT decay-rate machinery and unified-coupling input | `claude/youthful-neumann: docs/PROTON_LIFETIME_DERIVED_NOTE.md`, `scripts/frontier_proton_lifetime_derived.py` |
| Lorentz-violation cubic fingerprint | bounded companion only | the cubic-harmonic structure is real, but the phenomenology is a companion prediction rather than flagship backbone | `claude/youthful-neumann: docs/LORENTZ_VIOLATION_DERIVED_NOTE.md`, `scripts/frontier_lorentz_derived.py` |
| BH entropy / RT ratio | bounded companion only | area law and RT-ratio evidence are useful, but exact universal `1/4` closure is not yet retained | `claude/youthful-neumann: docs/BH_ENTROPY_DERIVED_NOTE.md`, `scripts/frontier_bh_entropy_derived.py` |
| Gravitational decoherence rate | bounded companion only | interesting prediction, but it depends on the Penrose-Diosi identification and sits outside the flagship theorem chain | `claude/youthful-neumann: docs/GRAV_DECOHERENCE_DERIVED_NOTE.md`, `scripts/frontier_grav_decoherence_derived.py` |
| Magnetic monopole mass | bounded companion only | the mass estimate is interesting, but it still depends on imported `alpha_EM(M_Pl)` / FRW / inflation inputs | `claude/youthful-neumann: docs/MONOPOLE_DERIVED_NOTE.md`, `scripts/frontier_monopole_derived.py` |
| GW echo timing | candidate-missed bounded companion | potentially important if the frozen-star surface package is retained, but too dependent on the strong-field / echo amplitude story for current promotion | `claude/youthful-neumann: docs/GW_ECHO_DERIVED_NOTE.md`, `scripts/frontier_gw_echo_derived.py` |

## 4. Historical or off-scope claims that should not be dropped

These are not flagship-paper claims, but they are not trash. They belong in
work history, companion-paper planning, or the methods story.

| Program family | Status | Why it matters | Authority |
|---|---|---|---|
| Mirror / exact geometry / `Z2 x Z2` coexistence program | off-scope historical | still one of the strongest older coexistence stories; useful for companion or historical framing | [POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md](../../POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md) entries `D01-D03` |
| Ordered-lattice / valley-linear / action-law families | off-scope historical | important older route to gravity diagnostics, but superseded by the current `Cl(3)` / `Z^3` paper surface | discovery log entries `D04-D06` |
| Coin / chiral / Dirac-walk program | off-scope historical with strong negatives | important for diagnostics and negative lessons, not for the flagship claim surface | discovery log entries `D07`, `D20` |
| Staggered portability / DAG / self-gravity / two-field packages | off-scope historical but methodologically important | these are part of the route that got the program here, but they do not belong in the current letter unless a specific claim is promoted separately | discovery log entries `D10-D17`, `D21-D39` |
| Branch entanglement / holography / BMV-style probes | off-scope historical / companion material | interesting and publishable in their own right, but not part of the flagship backbone | discovery log entries `D22-D28`, `D24`, `D26`, `D28` |

## 5. Stale or unsafe authority files

These files should not drive publication claims unless they are rewritten.

| File family | Status | Why unsafe |
|---|---|---|
| stale review packets / publication cards that overclaim closed gates | stale / not-for-paper | they repeatedly outran the audited state |
| older full-closure notes for DM, `y_t`, `S^3`, CKM, or gauge couplings | stale / not-for-paper | these often converted bounded sub-results into full-closure prose |
| misnamed “Born rule derived” notes | stale until renamed / narrowed | the safe claim is exact `I_3 = 0`, not a standalone Born-rule derivation |
| overnight summary / scorecard / unified-closure docs that mark `S^3`, DM, or `y_t` as closed | stale / not-for-paper | the overnight audit did not promote any of the four live gates, so these summary docs are not authority by themselves |

## 6. Ledger rule for manuscript work

Before a claim enters the manuscript, it must satisfy one of:

1. It already appears in Section 1 of this ledger as `promoted`.
2. It appears in Section 2 or 3 with explicit bounded wording.
3. It appears in Section 4 and is clearly labeled as off-scope or historical.

If a claim is not here, add it before using it.

In the publication package, that is still not sufficient. A manuscript-facing
claim must also appear in
[DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) with both its
safe theorem boundary and its validation path.
