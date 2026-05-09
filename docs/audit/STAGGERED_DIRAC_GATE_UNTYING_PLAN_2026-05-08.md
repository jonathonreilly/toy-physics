# Staggered-Dirac Gate Untying Plan

**Date:** 2026-05-08
**Status:** campaign roadmap — actionable sequence for the codex audit lane
**Lane:** audit-strategy. No physics claims added or removed; this is a
navigation artifact for the audit lane.

---

## Why this doc exists

The audit-graph leverage map (refreshed 2026-05-08) shows the
**staggered-Dirac realization gate** as the single highest-leverage
non-retained root in the repo: `staggered_dirac_realization_gate_note_2026-05-03`
gates **660 transitive descendants**, and ranks 2–10 of the leverage map
are tightly coupled axiom-first descendants that wait on it.

This doc captures the specific 18-node cluster the gate-untying campaign
must clear, in dependency-aware order, with exact `codex_audit_runner.py`
invocations.

## Cluster snapshot (audit-readiness as of 2026-05-08)

All 18 nodes have **runners present** and **cached logs in
`logs/runner-cache/`** — the cluster is fully audit-ready in the
mechanical sense.

### The four substep theorem notes (drafted 2026-05-07; unaudited)

| substep | claim_id | claim_type | runner |
|---|---|---|---|
| 1 — Grassmann partition forcing | `staggered_dirac_grassmann_forcing_theorem_note_2026-05-07` | bounded_theorem | `scripts/probe_grassmann_forcing_dependency_chain.py` (PASS=9/0) |
| 2 — Kawamoto-Smit phase forcing | `staggered_dirac_kawamoto_smit_forcing_theorem_note_2026-05-07` | bounded_theorem | `scripts/probe_kawamoto_smit_phase_forcing.py` (PASS=24/0) |
| 3 — BZ-corner 1+1+3+3 forcing | `staggered_dirac_bz_corner_forcing_theorem_note_2026-05-07` | bounded_theorem | `scripts/probe_bz_corner_decomposition.py` (PASS=5/0) |
| 4 — Physical-species algebraic support | `staggered_dirac_physical_species_direct_theorem_note_2026-05-07` | bounded_theorem | `scripts/probe_three_states_direct_derivation.py` (PASS=15/0) |

Each substep note is `bounded_theorem` and explicitly hedges retained-grade
closure on dependency state, so the audit lane can land them as
`audited_clean bounded_theorem` even if upstream deps are conditional —
their `effective_status` would then become `audited_clean` (or
`retained_pending_chain`) until the upstream cluster clears.

### The 14-node upstream cluster (deps of the substeps)

| audit_status | claim_id | td | crit |
|---|---|---:|---|
| `audited_conditional` | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | 531 | critical |
| `unaudited` | `axiom_first_spin_statistics_theorem_note_2026-04-29` | — | — |
| `unaudited` | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | 522 | critical |
| `audited_conditional` | `axiom_first_cluster_decomposition_theorem_note_2026-04-29` | 517 | critical |
| `audited_conditional` | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | 514 | critical |
| `audited_conditional` | `axiom_first_lattice_noether_theorem_note_2026-04-29` | 51 | high |
| `audited_conditional` | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | 514 | critical |
| `unaudited` | `axiom_first_reeh_schlieder_theorem_note_2026-05-01` | — | — |
| `unaudited` | `cl3_per_site_hilbert_dim_two_theorem_note_2026-05-02` | — | — |
| `unaudited` | `fermion_parity_z2_grading_theorem_note_2026-05-02` | — | — |
| `unaudited` | `three_generation_observable_theorem_note` | 235 | critical |
| `unaudited` | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | 371 | critical |
| `unaudited` | `three_generation_structure_note` | 370 | critical |
| `audited_conditional` | `s3_taste_cube_decomposition_note` | 396 | critical |

## The dependency cycle and how to break it

5 of the 6 currently-conditional upstream rows are blocked on the
staggered-Dirac gate itself or its descendants:

- `axiom_first_cl3_per_site_uniqueness` — auditor: "close or retain-grade the staggered-Dirac/Grassmann one-pair-per-site bridge" (= substep 1)
- `axiom_first_lattice_noether` — auditor: "close or explicitly admit the staggered-Dirac realization gate"
- `s3_taste_cube_decomposition` — auditor: "close or remove the admitted staggered-Dirac realization dependency"
- `axiom_first_microcausality_lieb_robinson` — depends on RP + spectrum + cluster + Lorentz
- `axiom_first_single_clock_codimension1_evolution` — depends on RP + spectrum + cluster + microcausality + cl3_per_site

This is a small **2-cycle**:

```
substep 1 (Grassmann forcing)
  ↑ depends on
axiom_first_cl3_per_site_uniqueness (currently audited_conditional)
  ↑ auditor's repair target says: re-audit narrowly
substep 1
```

The auditor's repair target on `cl3_per_site_uniqueness` already names the
break: **"re-audit U4 separately from the already-clean A1-only Cl(3)
representation classification"**.

So the cycle break is a **scope narrowing**: cl3_per_site_uniqueness re-audit
restricted to U1–U3 + A1-only Cl(3) classification (auditor explicitly says
this part is clean). U4 (the per-site Hilbert-space conclusion) becomes
out-of-scope of that note and is what substep 1 supplies.

## Recommended audit-lane execution order

### Phase 1 — break the cycle (1 row, ~10 min codex time)

Re-audit `cl3_per_site_uniqueness` with a scope narrowing. The auditor
already named this in the existing verdict; the scope-narrowing should
land `audited_clean bounded_theorem` for the A1-only restatement.

```bash
python3 scripts/codex_audit_runner.py --claim-id axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29
```

Possibly preceded by a small note edit narrowing the claim_scope, but
that should land cleanly with the existing runner cache.

### Phase 2 — audit the eight unaudited upstream rows (~80 min)

After Phase 1 reseats `cl3_per_site_uniqueness`, fresh-context audit each
unaudited upstream row. The audit lane will land verdicts; some will
be `audited_clean`, some will be conditional with concrete repair targets.

```bash
for cid in \
    axiom_first_spin_statistics_theorem_note_2026-04-29 \
    axiom_first_reflection_positivity_theorem_note_2026-04-29 \
    axiom_first_reeh_schlieder_theorem_note_2026-05-01 \
    cl3_per_site_hilbert_dim_two_theorem_note_2026-05-02 \
    fermion_parity_z2_grading_theorem_note_2026-05-02 \
    three_generation_observable_theorem_note \
    three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02 \
    three_generation_structure_note; do
  python3 scripts/codex_audit_runner.py --claim-id "$cid"
done
```

### Phase 3 — re-audit the five conditional upstream rows (~50 min)

The five rows whose conditional verdict was "wait on the staggered-Dirac
gate" can be re-audited once Phase 1 narrows the gate dependency. Some
will land `audited_clean` after the dep narrows; others may still need
substantive repair (`axiom_first_cluster_decomposition` is the one that's
NOT blocked on the gate — it needs Hastings-Koma assumption verification).

```bash
for cid in \
    axiom_first_lattice_noether_theorem_note_2026-04-29 \
    axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01 \
    axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03 \
    s3_taste_cube_decomposition_note \
    axiom_first_cluster_decomposition_theorem_note_2026-04-29; do
  python3 scripts/codex_audit_runner.py --claim-id "$cid" --retry-conditional
done
```

`axiom_first_cluster_decomposition` may need a separate scope-narrowing
PR before re-audit (auditor: "either restrict to L1/L3/L4 LR consequences,
or add a separate retained theorem proving the spectral gap hypotheses").

### Phase 4 — audit the four substep notes (~40 min)

Once the upstream cluster is at retained-grade or audited-clean, audit
each substep:

```bash
for cid in \
    staggered_dirac_grassmann_forcing_theorem_note_2026-05-07 \
    staggered_dirac_kawamoto_smit_forcing_theorem_note_2026-05-07 \
    staggered_dirac_bz_corner_forcing_theorem_note_2026-05-07 \
    staggered_dirac_physical_species_direct_theorem_note_2026-05-07; do
  python3 scripts/codex_audit_runner.py --claim-id "$cid"
done
```

### Phase 5 — retag the parent gate

Once all four substeps are `audited_clean retained_bounded`, the parent
gate note becomes eligible for retagging from `open_gate` to
`positive_theorem` (per the gate note's own statement: *"When the
in-flight chain closes, the parent identity here can become eligible for
independent audit/governance retagging as a `positive_theorem`-typed
theorem note"*).

Recommended retag PR makes a single edit to
`docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` changing
`Type: open_gate` to `Type: positive_theorem`, with a "Closure
status" update referencing the four audit-clean substeps.

## Estimated propagation impact

After Phase 5, the audit pipeline (`compute_effective_status.py`)
recomputes `effective_status` across 660 transitive descendants. Many of
the leverage-map ranks 2–10 should advance:

- `axiom_first_cl3_per_site_uniqueness` (td=531) → potentially `retained_bounded`
- `axiom_first_reflection_positivity` (td=522) → audit-eligible
- `axiom_first_cluster_decomposition` (td=517) → still needs Hastings-Koma fix but its other blockers clear
- `axiom_first_microcausality_lieb_robinson` (td=514) → audit-eligible
- `axiom_first_single_clock_codimension1_evolution` (td=514) → audit-eligible
- `cpt_exact_note` (td=520) → unblocked once `physical_hermitian_hamiltonian_and_sme_bridge` clears
- `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` (td=430) → audit-eligible

Conservative estimate: **400–500 transitive descendants** move from
`unaudited`/`audited_conditional` toward retained-grade after the
cluster clears, depending on how Phase 3 conditional re-audits land.

## Risks and known gaps

- **Phase 1 cycle-break may need a small pre-PR.** If the audit lane's
  fresh-context look at `cl3_per_site_uniqueness` insists on the original
  scope rather than the auditor-suggested narrowing, a small note edit
  (narrowing the claim_scope to "A1-only Cl(3) classification") is
  the prerequisite. The existing verdict already telegraphs the auditor
  would accept the narrower scope.
- **`axiom_first_cluster_decomposition` is genuinely science-grade.**
  Its repair (verifying Hastings-Koma assumptions for the canonical
  Hamiltonian) is research-grade work, not an audit-only fix. Phase 3
  may leave this row `audited_conditional` even after the rest clears.
  Downstream impact: ~517 transitive descendants stay
  `retained_pending_chain` until cluster_decomposition closes.
- **Phase 4 may surface gaps in the substep notes themselves.** The
  substep notes are 1 day old and were authored by the same family
  that will not re-audit them; codex GPT-5.5 fresh-context may find
  scope or rigor issues that need substep-side repairs before landing.

## Out of scope

- This doc does NOT close the gate. Closure happens in the audit lane
  and (for cluster_decomposition) in research-grade follow-up PRs.
- This doc does NOT modify any audit ledger fields. The pipeline
  recomputes those after audit verdicts land.
- This doc does NOT supersede the broader frontier roadmap (option 2 of
  the conditional-review session) — that doc would map all 67 non-retained
  roots with td≥100, of which the staggered-Dirac cluster is one.

## Cross-references

- Parent gate: `docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
- Substeps: `docs/STAGGERED_DIRAC_*_THEOREM_NOTE_2026-05-07.md` (4 notes)
- Audit lane: `docs/audit/README.md`, `docs/audit/AUDIT_AGENT_PROMPT_TEMPLATE.md`
- Audit runner: `scripts/codex_audit_runner.py`
- Conditional cohort routing: `docs/audit/MISSING_DERIVATION_PROMPTS.md`
  (sections `audited_conditional_runner_artifact_issue` etc., used by
  `scripts/science_fix_loop.py`)
- Refreshed leverage map data: this PR (`#693`) regenerates
  `docs/audit/data/audit_ledger.json` and the audit queue.
