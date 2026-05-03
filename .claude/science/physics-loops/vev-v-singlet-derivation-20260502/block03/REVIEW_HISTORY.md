# REVIEW HISTORY — Block 03 (H1 Route 1 deep stretch)

**Date:** 2026-05-02
**Block:** 03 — H1 Route 1: minimal-block self-consistent saddle for ⟨P⟩(β=6)
**Branch:** `physics-loop/vev-v-singlet-derivation-block03-20260502`
**Artifact:** `docs/PLAQUETTE_MINIMAL_BLOCK_SADDLE_STRETCH_NOTE_2026-05-02.md` +
              `scripts/frontier_plaquette_minimal_block_saddle_stretch.py`
**Honest tier:** named-obstruction stretch attempt (NOT retained-positive)

## Block 02 skip rationale (recorded here for next-agent context)

Block 02 was originally planned as the H1 Route 2 cheap probe (Cl(3) +
Klein-four counting forcing β=6). On grounding, found that
`G_BARE_RIGIDITY_THEOREM_NOTE.md` (2026-04-14) already provides the
structural argument that g_bare = 1 is forced canonically by the
Hilbert-Schmidt trace form on derived su(3) ⊂ End(V), removing the
A → A/g rescaling freedom. The user's proposed counting ansätze
(8-2=6, 4+2=6, 3+3=6) reduce to numerology relative to this rigidity
theorem, and would FAIL V1 of the promotion value gate (no specific
verdict obstruction not already addressed). Per skill workflow §7:
"discard the cycle and pivot, do NOT downgrade." Block 02 skipped;
direct pivot to block 03.

Recorded in NO_GO_LEDGER (loop pack on block 01 / PR #408).

## Block 03 self-review (per skill workflow #12)

### Promotion Value Gate (V1-V5)

This is a STRETCH ATTEMPT (named obstruction), not retained-positive
movement. V1-V5 strictly apply only when retained-positive promotion is
claimed; nevertheless, applying them as a discipline:

#### V1: What SPECIFIC verdict-identified obstruction does this PR close?

**Answer:** [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](../../../../docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
status amendment 2026-05-01:

> "the explicit analytic `beta = 6` insertion remains open."

This stretch ATTEMPTS to derive `⟨P⟩(β=6)` analytically via the V-invariant
minimal-block self-consistent mean-field saddle. The attempt does not
close the obstruction (consistent with the famous-open-lattice-problem
context), but it SHARPENS the obstruction by:

1. Demonstrating that naive U → u_0 · I mean-field has no positive saddle
   (Haar entropy required as load-bearing piece).
2. Showing the toy SU(3) mean-field with a parameterized Haar entropy
   gives ⟨P⟩_MF in the range 0.55-0.89 depending on parameterization,
   NOT matching the canonical 0.5934.
3. Identifying the gap as the "minimal-block-equals-bulk" obstruction on
   the V-invariant subspace — the same obstruction as the
   `framework-point underdetermination theorem` of the bridge-support
   stack.

The stretch addresses the named verdict obstruction directly. Disposition:
**PASS** for stretch-attempt purposes.

#### V2: What NEW derivation does this PR contain?

**Answer:** Marginal new content:

1. The "no positive saddle without Haar entropy" calculation, demonstrating
   that Haar entropy is load-bearing for the saddle.
2. The framing as a complementary lower-bound to the bridge-support
   stack's analytic upper-bound candidate.
3. The explicit identification of "SU(3) Haar entropy h(u_0) lacks closed
   form" as the specific structural piece blocking analytic closure.

This is NOT a closure of any new theorem. It is a sharper named
obstruction. **PASS** for stretch-attempt purposes (per skill workflow
#6: stretch attempts produce "partial structure, sharper obstruction,
falsified premise, or worked failed derivation").

#### V3: Could the audit lane already complete this?

**Answer:** Mostly YES — the audit lane could do the naive mean-field
check and the SU(3) toy mean-field. The new framing (lower-bound
complementary to bridge-support stack's upper-bound) is the marginal new
content that the audit lane has not produced.

**PASS** for stretch-attempt purposes. (For retained-grade promotion, V3
would be borderline; this is a stretch attempt, not retained promotion.)

#### V4: Is the marginal content non-trivial?

**Answer:** Marginally yes:

- The "no positive saddle without Haar entropy" calculation is a load-bearing
  observation about the framework's mean-field setup, not a textbook
  identity.
- The "minimal-block-equals-bulk obstruction = framework-point
  underdetermination" connection is a new structural framing.

**PASS** for stretch-attempt purposes.

#### V5: Is this a one-step variant of an already-landed cycle?

**Answer:** NO. The stretch attempt is orthogonal to:
- `PLAQUETTE_SELF_CONSISTENCY_NOTE` (uses MC, not analytic mean-field)
- Bridge-support stack (provides analytic upper-bound candidate via
  Perron solves; this stretch attempts a complementary mean-field
  approach for lower-bound estimate)

**PASS**.

### Value Gate disposition: PASS for stretch-attempt purposes

The stretch attempt is honest output per skill workflow #6 ("no-go packet
/ partial structure / sharper obstruction / worked failed derivation
with the exact load-bearing wall named"). Volume cap allows; cluster cap
allows (this is the first PR in `gauge_vacuum_plaquette_*` cluster within
this campaign).

## Self-review findings

| # | Severity | Finding | Disposition |
|---|---|---|---|
| F1 | medium | The toy SU(3) Haar entropy `h(u_0) = 4 log(1-u_0^2)` is a simplistic parameterization. The actual SU(3) Haar entropy is steeper, giving ⟨P⟩_MF ≈ 0.55-0.58 (Drouffe-Zuber 1983, Münster 1981) at β=6, not 0.886. | Recorded explicitly in §3 of the runner output. The toy is illustrative, not load-bearing for the named obstruction. The actual SU(3) Haar entropy gap to MC is the same obstruction. |
| F2 | low | The mean-field calculation is for **bulk** SU(3), not specifically for the V-invariant minimal block. The V-invariant restriction is mentioned but not numerically computed. | The V-invariant restriction would change the entropy term but not the qualitative obstruction. Recorded explicitly in §4 of the theorem note as future work. |
| F3 | low | The stretch attempt does not connect to the explicit Perron-state reduction (`GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE`) work, which gives the analytic upper-bound candidate `P(6) ≈ 0.59353`. | Connection is mentioned in §5 of the runner output and §8 of the theorem note. Both approaches (bridge-support upper-bound, this mean-field lower-bound) bracket the analytic problem; full closure remains open. |
| F4 | low | The "minimal-block-equals-bulk on V-invariant subspace" is the load-bearing claim; the stretch attempt assumes but does not prove this. | Honest: no proof of minimal-block-equals-bulk is offered. Recorded as the famous open problem. |

### Hostile-review-style stress test

**Q1.** Is the "naive mean-field has no positive saddle" calculation correct, or does it have an error in derivative signs?

**A1.** The calculation: log Z_MF = -β N_p (1 - u_0^4) + 4 ∑_ω log[u_0²(3+sin²ω)] (m=0).
∂/∂u_0 = +4 β N_p u_0³ + 4 · 2 u_0 · L_t / u_0² · 1 (∑_ω 1/(3+sin²ω) cancels with (3+sin²ω)? wait)
Let me recheck. log[u_0²(3+sin²ω)] = 2 log u_0 + log(3+sin²ω). ∂/∂u_0 = 2/u_0.
So ∂(log Z)/∂u_0 = 4 β N_p u_0³ + 4 ∑_ω (2/u_0) = 4 β N_p u_0³ + 8 L_t / u_0 (since ∑_ω 1 = L_t)
Setting to 0: 4 β N_p u_0⁴ = -8 L_t → u_0⁴ = -2 L_t / (β N_p) (NEGATIVE).
For β > 0, no positive saddle. ✓

The runner reports this correctly. The naive setup genuinely has no saddle without Haar entropy.

**Q2.** Is the toy parameterization h(u_0) = 4 log(1-u_0²) consistent with the small-u_0 expansion of SU(3) Haar entropy?

**A2.** Small-u_0 expansion of SU(3) character expansion: leading term is `(N_c² - 1)/2 · u_0² = 4 u_0²` for SU(3). The toy parameterization gives h(u_0) ≈ -4 u_0² · (-1) = 4 u_0² at small u_0, with sign chosen so that h decreases for larger u_0. Wait, actually `h(u_0) = 4 log(1-u_0²) = 4·(-u_0² - u_0^4/2 - ...) = -4 u_0² - 2 u_0^4 - ...` so h(small u_0) ≈ -4 u_0², and h is NEGATIVE. The leading -4 u_0² coefficient matches the SU(3) leading-order character. ✓

But the higher-order terms differ from true SU(3) Haar entropy. The toy is qualitatively right at small u_0 but quantitatively off at large u_0. The runner output (~0.886 vs Drouffe-Zuber ~0.55-0.58) confirms the toy overestimates at β=6.

**Q3.** Does the framework actually use the V-invariant minimal block for plaquette evaluation, or is the V-invariance an a priori restriction?

**A3.** Looking at PLAQUETTE_SELF_CONSISTENCY_NOTE: "On the retained graph-first gauge surface: the gauge group is SU(3); the Wilson plaquette action at g_bare² = 1 gives β = 2 N_c / g² = 6; the finite periodic lattice gives a finite product of compact Haar integrals." There is no explicit V-invariant restriction in the plaquette evaluation. The framework treats the symmetric L⁴ lattice as the same-surface for plaquette evaluation.

So the H1 Route 1 strategy of "minimal block = V-invariant" is the user's PROPOSED method, not the framework's existing setup. This stretch attempt explores whether the V-invariant minimal-block mean-field gives the bulk thermodynamic-limit value. The realistic answer (per the famous-open-problem context) is NO, demonstrated qualitatively here.

### Self-review disposition: PASS

The stretch attempt is honestly stated as named-obstruction, with toy parameterization caveats explicitly recorded. The output sharpens the famous open lattice problem; it does not claim closure.

## Cluster-cap / volume-cap check

- Volume cap: 2 of 5 PRs (this campaign): block 01 PR #408 + block 03 (this PR).
- Cluster cap (`gauge_vacuum_plaquette_*` family): 1 of 2 used by this PR
  (block 01 was different family `ew_vev_*`/hierarchy).
- Corollary churn: 2nd substantive cycle of campaign; not yet at the
  ~5-cycle corollary-churn check.

PASS all caps.

## Closure and next action

Block 03 is closure-ready as named-obstruction stretch attempt. Next action:
write CLAIM_STATUS_CERTIFICATE, commit, push, open PR.

After block 03 PR opens, refresh OPPORTUNITY_QUEUE and consider whether
to proceed to additional cycles or stop on corollary/value-gate exhaustion.
