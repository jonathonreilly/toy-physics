# Charged-Lepton — Route Portfolio

**Date:** 2026-04-28
**Loop:** `charged-lepton-pickup-20260428`

## R1 — Lane 6 dependency audit + theorem plan (Tier A; **audit-grade**)

Lane file's "first parallel-worker target": the `y_τ` Ward identity
construction. R1 produces the closure roadmap, dependency map onto
Koide flagship + retained gauge cluster, and Phase-1/2/3 ordering.

- **Score:** HIGH for grounding; counts toward audit-quota.
- **Blockers:** none.

## R2 — `y_τ` Ward identity construction attempt (Tier B; **stretch**)

Phase-1 priority. Construct the `y_τ` Ward identity on the
charged-lepton carrier as analog of retained `y_t(M_Pl)/g_s(M_Pl)
= 1/√6`. Combined with retained Koide ratios (in flight),
pins absolute lepton scale `V_0` and chains to retained
`m_e, m_μ, m_τ`.

**Key structural difference from YT-lane:** charged leptons are
gauge-singlet under `SU(3)` (no `g_s` anchor). The Ward identity
must be anchored on `SU(2)` weak coupling `g_2` or hypercharge
`g_1` (or a representation-theoretic structure not directly tied
to a gauge coupling).

- **Score:** HIGH. Phase-1 closure target per lane file.
- **Blockers:** depends on what structural anchor the identity
  uses — `g_2`, `g_1`, or a non-gauge structural anchor.

## R3 — Koide flagship integration audit (Tier A; **audit-grade**)

Survey the Koide flagship lane's recent retentions (Q=2/3, δ=2/9
support routes; OP-locality / C3-fixed source landing) and check
consistency with R2. Identify any cross-lane consistency check or
shared structural anchor.

- **Score:** MEDIUM.

## R4 — V_0 absolute-scale construction (Tier B-C; downstream of R2)

Once `y_τ` Ward identity lands, `V_0 = √2 m_τ / y_τ`. With Koide
ratios retained, all three masses retained from one axiom.

- **Score:** HIGH conditional on R2; otherwise blocked.

## R5 — Cross-lane impact study (Tier A; **audit-grade**)

If R2 lands, cross-lane impact: does `y_τ` Ward identity extend by
analogy to `y_ν` for neutrinos (4A Route A in the neutrino loop's
Cycle 10 stretch-attempt note)? Likely answer: anchor mismatch
(τ_R hypercharge -1, ν_R hypercharge 0) — needs a separate route.

- **Score:** MEDIUM. Audit-grade analytical work.

## R6 — Stretch attempt: `y_τ` Ward via SU(2)-weak structure (Tier B-C; **stretch**)

Specific R2 sub-attack: try anchoring the `y_τ` Ward identity on
`SU(2)` weak coupling `g_2`. Tau is in the lepton doublet `L_L
= (ν_L, τ_L)^T`, weak-doublet. Yukawa `y_τ L̄_L H τ_R` couples
the doublet to `H` and `τ_R`. `g_2` is retained; if a structural
identity `y_τ / g_2 = const` exists, R6 closes.

**Why this might work:** parallels the YT-lane's structural
anchor pattern (top quark also weak-doublet via `q_L = (t_L,
b_L)^T`).

**Why it might not:** the YT-lane `y_t/g_s = 1/√6` rests on
**color** structure (`SU(3)` representation theory). The
weak-doublet structure is shared between top and tau, but the
`SU(3)` color anchor is unique to the top.

- **Score:** MEDIUM-HIGH. Concrete single-cycle attempt;
  honest partial output likely.

## R7 — Stretch fallback: `y_τ` Ward via hypercharge (Tier B-C; **stretch**)

If R6 fails, try anchoring on `g_1` hypercharge. Tau's hypercharge
is -1 (right-handed), -1/2 (left-handed). Construct identity
`y_τ / g_1 = const`.

- **Score:** MEDIUM. Plausible but the YT-lane analogy is weakest
  here.

## R8 — Stuck fan-out (per Deep Work Rules; required before any
"no route" stop)

Before any honest stop, generate 3-5 orthogonal `y_τ` anchor
candidates: (i) `g_2`, (ii) `g_1`, (iii) `g_3=g_s` via off-diagonal
mixing (unlikely), (iv) Koide-structural anchor (use Q=2/3
combinatorial structure), (v) gauge-doublet structural anchor
(combined SU(2)×U(1)).

## Selection — Cycle 1

Cycle 1 = R1 dependency audit + theorem plan (audit-grade).

After Cycle 1, Cycle 2 candidate is R2 / R6 (the y_τ Ward identity
attempt with SU(2)-weak structural anchor first).

## Rejected for this loop

- Direct attack on Yukawa derivation outside Ward-identity structure
  (closed by `CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26`).
- Any route in §1 of NO_GO_LEDGER.
- Pure prose audit without structural content.
