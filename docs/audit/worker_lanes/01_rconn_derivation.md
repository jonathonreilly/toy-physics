# Lane 1: RCONN derivation → unblock EW color projection

**Status:** OPEN — accepting workers.
**Source claim:** [`yt_ew_color_projection_theorem`](../../../docs/YT_EW_COLOR_PROJECTION_THEOREM.md)
**Audit verdict:** `audited_conditional`
**Criticality:** `critical` · **Transitive descendants:** 278 · **Load-bearing class:** F (renaming)

This lane is the highest-leverage open science target. Closing it
ratifies one of the most-cited derivation roots in the package.

## Audit finding (verbatim from the ledger)

**Load-bearing step under audit:**

> The physical EW coupling (matched to the continuum where the SU(3) and
> EW sectors are factored) should use the connected color trace
> `N_c(N_c²−1)/N_c² = (N_c²−1)/N_c`.

**Why the chain does not close:**

The source note gives the Fierz identity and shows CMT is color-blind,
but it does not derive the physical lattice-to-continuum EW-current
matching rule that selects the connected trace as the coupling readout.
The 9/8 factor that produces the framework's percent-level match to
PDG `sin²θ_W` and `1/α_EM(M_Z)` is asserted via this matching ansatz,
not derived.

**Open one-hop dependency:** `docs/RCONN_DERIVED_NOTE.md`

## Repair target (what closure looks like)

A retained theorem (and registered runner) that derives the lattice-to-
continuum EW current matching from `Cl(3) / Z³` primitives. Specifically:

1. A first-principles derivation of the connected-color-trace selection
   for the physical EW current readout, **not** an assertion that this
   normalization is the right one.
2. A registered runner that **computes** the connected two-vertex
   observable / matching factor from the lattice action, rather than
   applying `8/9` as a closed-form post-hoc.
3. `RCONN_DERIVED_NOTE.md` registered as an explicit one-hop dependency
   on the audit ledger, with clean `effective_status` after the runner
   completes.

## Why this is high-leverage

`yt_ew_color_projection_theorem` has **278 transitive descendants**.
Many of these inherit `audited_conditional` only because the connected-
trace selection is conditional. Closing this lane promotes a large
fraction of the EW / Yukawa downstream surface in one move.

The framework's headline EW agreements
(`sin²θ_W = 0.2306` vs PDG `0.2312`, −0.26%; `1/α_EM(M_Z) = 127.67`
vs PDG `127.95`, −0.22%) all flow through this matching factor. Until
the matching is derived rather than asserted, those agreements register
as **numerically motivated** rather than first-principles — which is
exactly what the audit verdict says.

## Claim boundary while this lane is open

Per the audit verdict, it remains safe to say:

- CMT alone cannot produce the `9/8` factor.
- `8/9` is a motivated connected-color-trace / large-`N_c` matching
  ansatz with controlled corrections.
- Applying it improves the quoted `g_1` and `g_2` numerics.

It is **not** safe to claim a retained derivation of the EW couplings
from `Cl(3) / Z³` until this lane closes.

## Suggested approach (worker-side)

1. Read `docs/RCONN_DERIVED_NOTE.md` to understand the current state.
2. Identify what's missing: is the derivation incomplete, the runner
   missing, or both?
3. Derive the matching factor on the lattice surface — possibly via:
   - Direct two-vertex Wilson-loop / connected-correlator computation
     on `Z³`,
   - Continuum limit + `1/N_c` expansion with Cl(3)-native normalization,
   - Or an alternative route that selects the connected trace from
     primitives.
4. Implement a runner that **computes** the matching factor (not just
   asserts it).
5. Land the new theorem note plus runner; register
   `RCONN_DERIVED_NOTE.md` as a one-hop dependency on
   `YT_EW_COLOR_PROJECTION_THEOREM.md`.

## Success criteria (triggers re-audit)

- `RCONN_DERIVED_NOTE.md` audits as `audited_clean` under the standard
  rubric (load-bearing step is class C — first-principles compute).
- `yt_ew_color_projection_theorem` re-audits as `audited_clean` once
  the dependency is registered and the chain closes.

Cross-confirmation by a second auditor is required for ratification
because the source claim is `criticality=critical`.

## Branch / worker conventions

- Suggested proposal branch: `claude/rconn-derivation-2026-04-27` (or
  Codex equivalent).
- Suggested review branch (for the Codex pass): `codex/review-rconn-2026-04-27`.
- One commit per discrete sub-claim where possible; keep landing
  sequence small per the audit lane's hygiene rules.

## What this lane is NOT

- Not a request for a tightened numerical match to PDG. The framework
  already matches to ~0.25%; the audit issue is the **derivation
  surface**, not the numerical agreement.
- Not a request to remove `8/9` from the lane. If it survives audit
  as a derived factor, the existing numerical agreement re-ratifies.
- Not a Yukawa transport or top-mass attack — that is Lane 4
  (`yt_uv_to_ir_transport_obstruction`).
