# Claim-Status Certificate — Bridge Gap New Physics Loop

**Date:** 2026-05-06
**Loop:** bridge-gap-new-physics-20260506

---

## Block 01 (R1.A) — HK Brownian Time from Canonical Tr-Form

**Block path:** [`docs/BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md)
**Runner:** [`scripts/probe_hk_time_derivation.py`](../../../../scripts/probe_hk_time_derivation.py) — PASS=7 FAIL=0 verified 2026-05-06
**Branch:** physics-loop/bridge-gap-new-physics-block01-20260506

```yaml
actual_current_surface_status: bounded support theorem
target_claim_type: bounded_theorem
conditional_surface_status: |
  Conditional on:
   (a) canonical trace form Tr(T_a T_b) = δ_{ab}/2 (premise TR, retained
       per G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02);
   (b) g_bare = 1 (open gate per MINIMAL_AXIOMS_2026-05-03);
   (c) heat-kernel as the Cl(3)-native action candidate (Block 04 target —
       uniqueness vs Wilson NOT yet derived);
   (d) leading-order small-U matching as the Brownian-time selection
       criterion (finite-β / O(a²) corrections are Block 02 / Block 04
       targets).
hypothetical_axiom_status: null
admitted_observation_status: |
  Heat-kernel-Wilson small-U matching (Menotti-Onofri 1981 conventions)
  and Brownian motion on compact Lie groups (Helgason, Liao 2004) are
  admitted standard machinery in narrow non-derivation roles. No PDG/MC
  numerical values are load-bearing.
claim_type_reason: |
  Theorem 1 derives a specific exact-rational Brownian time t = 2 N_c / β
  = g_bare² from canonical Tr-form (retained) + standard small-U
  matching. Verified in exact arithmetic by paired runner (PASS=7/0).
  This is bounded support: it gives one specific structural input that
  the project has not previously closed in writing, but does NOT close
  the bridge gap on its own. Action-form uniqueness (Block 04) and
  thermodynamic limit (Block 03) remain open.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

### Seven retained-proposal certificate criteria

| # | Criterion | Pass? | Notes |
|---|---|---|---|
| 1 | `proposal_allowed: true` | **NO** | This is `bounded_theorem`, not `proposed_retained`. Conditional on (b)-(d). |
| 2 | No open imports for the claimed target | **NO** | g_bare = 1 is an open gate per MINIMAL_AXIOMS_2026-05-03. Heat-kernel uniqueness is open (Block 04). |
| 3 | No load-bearing observed/fitted/admitted values | **YES** | No PDG/MC values. Tr-form is retained. Brownian-motion / Menotti-Onofri are standard machinery in narrow non-derivation roles. |
| 4 | Every dependency is retained, retained corollary, or explicit allowed exact support | **PARTIAL** | Tr-form (retained), C_2 (retained), Schur (standard). g_bare = 1 dependency is open-gate, hence the bounded conditional status. |
| 5 | Runner checks dependency classes, not only numerical output | **YES** | `scripts/probe_hk_time_derivation.py` does symbolic verification of K1-K7 in exact rational arithmetic; not a numerical comparison to PDG. |
| 6 | Review-loop disposition `pass` | **PENDING** | Block-local self-review pending. |
| 7 | PR body explicitly says independent audit required | **WILL_DO** | PR body to be drafted with explicit independent-audit notice. |

**Verdict:** `bounded_theorem` is the honest tier. Criteria 1, 2, 4 partial/no
explicitly map the claim's bounded scope. Criteria 3, 5 pass cleanly. The
note's status text uses `bounded support theorem` consistently and avoids
all banned wording.

### Promotion-Value Gate self-record (V1-V5)

(Recorded in `OPPORTUNITY_QUEUE.md` for Block 01.) **PASS** — V1 closes
parent cluster-obstruction Resolution-A target on the framework's
algebraic structure; V2 contains a derivation chain not currently
retained; V3 audit lane has not done this combination; V4 marginal
content is non-trivial (~70% difference from Wilson 0.4225); V5 not a
one-step variant of any landed cycle.

### Corollary-churn check

Block 01 introduces a new load-bearing structural premise (canonical
bi-invariant metric → Brownian time matching) not present in any prior
landed cycle. It is not "plug-and-chug" — the Tr-form / small-U
expansion / matching chain is a genuine derivation, not arithmetic
verification of an already-implicit identity. **PASS.**
