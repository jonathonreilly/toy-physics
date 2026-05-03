# ROUTE PORTFOLIO — VEV V-Singlet Derivation Campaign

**Date:** 2026-05-02

Routes scored by likely claim-state movement, blast radius, and risk.

## Route H2-A (PRIMARY) — f_vac V-singlet curvature reformulation

**Move:** Replace the W = log\|det(D+J)\| - log\|det D\| route in
`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` with a direct claim about
`f_vac = -1/(L_t·V_s)·log Z` and its V-singlet source curvature
`v² = -∂²f_vac/∂m²\|_{m=0}`.

**Bridges retired (target):** B1 (additivity), B2 (CPT-even phase blindness),
B3 (continuity).

**Bridges introduced:** C1 (v² is the curvature of f_vac at origin) — claim:
this is a definition rather than a bridge, but audit may push back.

**Score:** retained-positive probability HIGH (the algebra is closed; the
key question is audit-acceptance of C1 as a definition vs. bridge).

**Decisive artifacts:**
- new theorem note proving Lemmas H2.1 (V-invariance of f_vac), H2.2 (m²-curvature equals A(L_t) on minimal block), H2.3 (vacuum is V-singlet)
- main theorem: v(L_t=4) / v(L_t=2) = (A_4/A_2)^(1/2) = (8/7)^(1/2) ⟹ (7/8)^(1/4) factor
- runner that VERIFIES the (7/8) ratio by direct sum, not hard-coding

**Risk:** audit may rule that C1 is a "bridge of comparable weight" to B1+B2
combined. In that case, H2 is sideways, not retiring net admissions.

**Blast radius:** medium-high. If H2 lands as exact-support theorem, the v
lane gains a cleaner upstream and the OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE
gets a sister theorem that retires 3 of its 5 admitted bridges.

## Route H2-B (sister) — m_H representation-theoretic distinction

**Move:** Show that `m_H²` is NOT V-invariant in the same way `v²` is,
because `m_H` is the curvature at the *minimum* of `V_eff` (which is
V-broken once EWSB happens), while `v²` is set by the curvature at the
*origin* (V-singlet vacuum).

**Score:** medium. This is a side benefit of H2-A, not a primary target.
Worth recording as a corollary but not as a separate cycle unless H2-A
lands and audit asks for it.

## Route H1-Route2 (CHEAP PROBE) — β=6 from Cl(3) + Klein-four counting

**Move:** Search for an algebraic/group-theoretic counting argument that
forces `β = 2 N_c / g_bare² = 6` from Cl(3) generators (8) + Klein-four
irreps (4) + staggered tastes (4) + spatial dimension (3) etc. The
framework currently treats `β = 6` as derived via `g_bare² = 1` (A4 axiom);
the cheap probe is whether `g_bare² = 1` is itself forced.

**Score:** retained-positive probability LOW. The user's prompt itself
labels this as "obviously ad hoc" and "long shot". Cheap to attempt
(half-day).

**Decisive artifacts:** either a counting argument that lands `β = 6`
(unlikely but possible), or a no-go theorem that forces `β = 6` to
remain as the A4 normalization choice.

**Risk:** waste of a cycle if no structure emerges quickly.

## Route H1-Route1 (DEEP STRETCH) — minimal-block self-consistent saddle

**Move:** Self-consistent saddle on the V-invariant Klein-four block:
`⟨P⟩ = u_0⁴ = -∂lnZ_min/∂β\|_{u_0 = u_0*}`. The framework already has the
required determinant identity (A7) and the gauge action on the minimal
block. The hard step is "minimal-block-equals-bulk on the V-invariant
subspace" — the framework's `same-surface` claim, asserted but not proven.

**Score:** retained-positive probability LOW-MEDIUM. The bridge-support
stack (`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`) already pinned the analytic
candidate at `P(6) = 0.59353` from Perron solves, ~0.022% above canonical
MC `0.5934`. Closing the *exact* analytic gap is the famous open lattice
problem. A partial result (e.g., proving minimal-block-equals-bulk on the
V-invariant subspace) would still be a major win.

**Risk:** likely produces a stretch-attempt note with named obstruction
rather than closure. Per skill workflow, that is still valid output.

## Route H1-Route3 (PARALLEL/OPTIONAL) — bootstrap closure

**Move:** Use modern lattice bootstrap (Anderson-Kruczenski 2017,
Kazakov-Zheng 2022, Lin et al 2023) with framework-specific Cl(3)/Klein-four
positivity constraints to bracket ⟨P⟩(β=6) rigorously by SDP.

**Score:** retained-positive probability LOW for *this* campaign. Full
bootstrap implementation is ~6 months and requires SDP infrastructure not
in this repo. The cheap version is just to record the route as "future
work" in the no-go ledger / handoff.

**Decision:** NOT in this campaign. Record in HANDOFF.md as a future
direction.

## Selection rule

1. Cycle 1-4: Route H2-A (umbrella theorem note)
2. Cycle 5: Route H2-A (verification runner)
3. Cycle 6: Review-loop, certificate, PR for block 01
4. Cycle 7: Route H1-Route2 (cheap probe)
5. Cycle 8 (if budget remains): Route H1-Route1 (deep stretch)

If H2-A passes V1-V5 and review-loop returns `pass`/`passed_with_notes`,
open one PR for block 01. Then pivot to block 02 (H1-Route2) as a fresh
branch.
