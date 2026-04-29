# Science Worker Queue — First Pass Retrospective + Next Tier

**Status:** first audit pass complete. Second-pass queue derived from current ledger state.
**Last updated:** 2026-04-27 (post first review-loop)

This document supersedes the original 5-lane queue. The original lane
handoff docs are preserved under `worker_lanes/` as context for future
re-promotion attempts.

---

## First pass: outcome table

| # | Lane | Canonical PR | Plan B PR | Outcome | Reading |
|---|---|---|---|---|---|
| 1 | RCONN derivation → unblock EW color projection | **#92 merged (salvaged)** | — | OZI matching theorem registered as **bounded support** (not retained); 9/8 coefficient kept on the existing reading | structural OZI argument is real but **does not by itself ratify** the matching coefficient |
| 2 | Native gauge runners — registration + cross-confirm | **#91 merged** | — | Hygiene wires landed; underlying claim subsequently re-audited by Codex and **flipped to `audited_failed`** | registration alone doesn't carry; the gauge-closure aggregator's chain doesn't close even with deps visible |
| 3 | Equivalence principle chain repair | #93 closed | **#96 merged** | Plan B honest downgrade landed; EP narrowed to "near-unity exponents" | structural chain-rule derivation didn't close on its own terms; the action-form selector remains open |
| 4 | YT UV-to-IR transport — first principles | **#94 merged** | #97 closed | 27 sub-theorem deps wired; master assembly subsequently **flipped to `audited_failed`** when each sub-theorem was individually audited | dep-registration exposed the chain; many P1/P2/P3 sub-theorems individually fail audit |
| 5 | DM neutrino Z3 phase lift — derive or downgrade | #95 closed | **#98 merged** | Plan B bounded reading landed; bridge family kept as candidate algebraic family | character-transfer derivation overclaimed exact physical closure; bounded reading was the safe landing |

**Pattern surfaced by the first pass:**

- Pure registration / hygiene PRs (#91, #94) **land procedurally but expose underlying audit failures** in the chain they make visible. This is exactly what the audit lane was built to do.
- Substantive new derivations attempted from inside an LLM session (#92, #93, #95) **were caught as overclaims** and either salvaged to bounded support (#92) or replaced by the Plan B downgrade (#96, #98). Two-of-three caught is a strong signal that fresh-look audits work.
- Honest downgrade was the right move on **all three lanes where it was prepared as Plan B**.

---

## Current ledger state (post first pass)

After 305 audits applied (up from 164 at the time of the first queue):

| audit_status | count | delta vs. first-pass snapshot |
|---|---:|---:|
| `unaudited` | 1,309 | −141 |
| `audited_conditional` | 143 | +59 |
| **`audited_clean`** | **72** | **+27** |
| **`audited_failed`** | **77** | **+55** |
| `audited_numerical_match` | 5 | 0 |
| `audited_decoration` | 3 | 0 |
| `audited_renaming` | 3 | +1 |
| `audit_in_progress` | 3 | 0 |

The ratio of `audited_failed` to `audited_clean` rose substantially (was 22/45, now 77/72). This reflects the second-order effect of dep-registration PRs (#91, #94) making chains visible to Codex; many sub-claims individually fail when actually audited.

---

## Second-pass queue: highest-leverage open work

Derived from current ledger by `(descendants × adverse-verdict-weight × criticality)`. Top targets:

### Tier A — substantive failed claims with high reach

| Rank | Claim | Audit | Desc | Notes |
|---:|---|---|---:|---|
| 1 | `native_gauge_closure_note` | `audited_failed` | 278 | Lane 2 aggregator re-failed after the hygiene PR. Needs **substantive science work** on the gauge-closure aggregator itself (not just dep registration). |
| 2 | `framework_bare_alpha_3_alpha_em_dimension_fixed_ratio_support_note_2026-04-25` | `audited_failed` | 121 | Bare α_3/α_EM = 9 dimension-ratio card. Re-audit this lane's chain. |
| 3 | YT P1/P2/P3 sub-theorem cluster (8 notes at desc=121, `audited_failed`) | `audited_failed` | 121 each | The 27-dep chain registered by #94 surfaced individual sub-theorem failures. Each needs targeted attention. |

### Tier B — decoration cluster (boxing, not science)

| Rank | Claim | Audit | Desc | Action |
|---:|---|---|---:|---|
| B1 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | `audited_decoration` | 175 | Box per `ALGEBRAIC_DECORATION_POLICY.md`. |
| B2 | `retained_cross_lane_consistency_support_note_2026-04-22` | `audited_decoration` | 121 | Same. |
| B3 | `koide_q_eq_3delta_identity_note_2026-04-21` | `audited_decoration` | 119 | Same. |

These don't need science workers; they need **publication-side hygiene** to roll up under their parent claims and stop appearing as separately-retained rows on `CLAIMS_TABLE.md`.

### Tier C — numerical-match dependencies

| Rank | Claim | Audit | Desc | Notes |
|---:|---|---|---:|---|
| C1 | `ckm_down_type_scale_convention_support_note_2026-04-22` | `audited_numerical_match` | 130 | Tuned input dependence; either derive or honest downgrade. |
| C2 | `bell_inequality_derived_note` | `audited_numerical_match` | 123 | Bell/CHSH support depends on tuned input rather than the axiom. |
| C3 | `yt_p1_delta_1_bz_computation_note_2026-04-17` | `audited_numerical_match` | 121 | Inside the YT P1 chain unblocked by #94. |
| C4 | `koide_higgs_dressed_resolvent_root_theorem_note_2026-04-20` | `audited_numerical_match` | 121 | Charged-lepton Koide approach depends on tuned input. |

---

## What changed since the first queue

**Closed in first pass:** Lanes 1, 3, 5 are closed (2 via Plan B downgrade, 1 via salvage). They no longer appear in this queue.

**Re-opened by audit:** Lane 2 (gauge closure) and Lane 4 (YT UV-to-IR) had their hygiene PRs land but then re-failed under audit. They appear in Tier A of the second-pass queue with substantive science requirements.

**New surfaces:** the Tier B decoration cluster (3 high-reach decorations to box) and the Tier C numerical-match cluster (4 high-reach tuned-input claims).

---

## Recommended dispatch for second pass

1. **Tier A is hard.** `native_gauge_closure_note` re-failed even with deps registered, which suggests the gauge-closure aggregator has a load-bearing step that doesn't close from the cited authorities. This is real science work that may or may not be tractable from an LLM session.

2. **Tier B is easy and high-leverage.** Boxing decoration claims is mechanical and addresses 175+121+119 = ~415 descendants worth of inheritance noise. Could be done as a single "decoration boxing" PR.

3. **Tier C requires per-lane judgment.** Each numerical-match claim has the same shape as the original Lane 4 — either derive (hard) or honest downgrade (cheap). Plan B → Plan A dichotomy applies.

The first pass demonstrated that **honest downgrade is the highest-yield move** when an LLM session attempts derivation. Second-pass workers should default to Plan B framing and only attempt Plan A when the structural argument is genuinely independent of the audit's specific complaint.

---

## Cross-references

- Lane handoff docs from the first pass: `worker_lanes/01_*.md` … `worker_lanes/05_*.md`
  (preserved as context; kept for re-audit if any of the closed lanes needs re-promotion)
- Audit lane policy: [README.md](README.md), [FRESH_LOOK_REQUIREMENTS.md](FRESH_LOOK_REQUIREMENTS.md), [ALGEBRAIC_DECORATION_POLICY.md](ALGEBRAIC_DECORATION_POLICY.md)
- Mechanical pipeline: `scripts/run_pipeline.sh`
- Current rendered ledger: [AUDIT_LEDGER.md](AUDIT_LEDGER.md)
- Pending audit queue (mechanical): [AUDIT_QUEUE.md](AUDIT_QUEUE.md)
