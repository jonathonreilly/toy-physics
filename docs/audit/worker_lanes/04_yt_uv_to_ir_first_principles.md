# Lane 4: YT UV-to-IR transport — replace numerical match with first-principles

**Status:** OPEN — accepting workers.
**Source claim:** [`yt_uv_to_ir_transport_obstruction_theorem_note_2026-04-17`](../../../docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md)
**Audit verdict:** `audited_numerical_match`
**Criticality:** `high` · **Transitive descendants:** 120 · **Load-bearing class:** G (numerical match at tuned input)
**Runner:** `scripts/frontier_yt_uv_to_ir_transport_obstruction.py` (registered, but post-arithmetic)

This is the lane that gates the framework's top-mass prediction.
`m_t(pole) = 172.57 ± 6.50 GeV` (PDG 172.69, agreement to 0.07%) flows
through the residual envelope tracked here.

## Audit finding (verbatim from the ledger)

**Load-bearing step under audit:**

> The packaged residuals (P1, P2, P3) = (1.92%, 0.50%, 0.30%) are
> combined in quadrature as `σ_YT = √(P1² + P2² + P3²) ≈ 1.95%` to
> define the retained master envelope on the Ward ratio.

**Why the chain does not close (verdict_rationale):**

The runner reproduces the arithmetic of the packaged envelope and the
qualitative P1/P2/P3 partition, but the residual centrals are
**imported, heuristic, or hard-coded** rather than derived from
registered one-hop authorities. The source note itself states the
per-primitive central values and transport primitives remain open
downstream work.

Specifically:

- `P2` (0.50%, UV-to-IR transport residual) is heuristic / hard-coded.
- `P3` (0.30%, K-series tail) is heuristic / hard-coded.
- `P1` (1.92%, lattice-to-MS̄ correction) is a selected single-channel
  packaged magnitude, not a derived quantity.

The runner verifies the **quadrature arithmetic** after these are
supplied; it does not derive any of them.

**Numerical inconsistency flag:** the runner currently outputs
`σ_YT = 2.010%` and `Δm_t = 3.47 GeV` while the prose rounds this as
~1.95% and ~3.4 GeV. Minor but should be reconciled.

**Unregistered / open dependencies:**

- `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` — not registered as
  one-hop dependency (should be).
- `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` — not registered (and is
  itself blocked by Lane 1).
- `docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md` — not registered.
- `P1` lattice-to-MS̄ residual theorem — not registered.
- `P2` UV-to-IR transport residual theorem — open or unregistered.
- `P3` K-series tail residual theorem — open or unregistered.

## Repair target

This lane has **two halves**: hygiene (registration) and science
(derivation).

### Hygiene half

1. Register the three existing notes as explicit one-hop dependencies
   (they're cited in prose but not in the dependency graph).
2. Make the runner assert the rounded envelope (`~1.95%`) and
   `m_t` uncertainty (`~3.4 GeV`) from the supplied inputs with
   explicit correlation rules, rather than printing one number
   while prose says another.

### Science half

3. Derive `P1` (lattice-to-MS̄) from registered Ward + color-projection
   inputs rather than asserting a packaged magnitude.
4. Derive or honestly downgrade `P2` (UV-to-IR transport residual).
   This is genuine new theory work — the source note acknowledges
   it's open.
5. Derive or honestly downgrade `P3` (K-series tail).

Replace each hard-coded residual with either a runner computation or
a cited retained output.

## Why this is high-leverage

This is the lane behind the framework's most-cited quantitative win:
top-mass to 0.07% of PDG. Until the residuals are derived rather than
asserted, that win is — per the audit verdict — a numerical match,
not a first-principles prediction. 120 transitive descendants.

The downstream effect is not just `m_t`; the same residual envelope
feeds the Higgs vacuum stability lane and the broader Yukawa lane.

## Claim boundary while this lane is open

Per the audit verdict, it remains safe to claim:

- An **organizational obstruction** that direct Ward-identity promotion
  to `y_t(v)` or `m_t(pole)` requires separate UV matching, transport,
  and pole-conversion inputs.
- The supplied packaged numbers arithmetically give about a 2.01%
  Ward-ratio envelope.

It is **not** an audited retained theorem-grade quantitative envelope
or a first-principles YT transport result.

## Suggested approach (worker-side)

This lane is large enough to potentially split into sub-lanes per
residual primitive. Suggested decomposition:

### Sub-lane 4a: P1 derivation
The lattice-to-MS̄ matching factor at the canonical surface. Should
follow from registered Ward + color-projection theorems once Lane 1
closes (Lane 1 also re-audits P1 by inheritance).

### Sub-lane 4b: P2 derivation or downgrade
The UV-to-IR transport residual. The source note says it's open.
Worker should either derive it from the same-surface running bridge
or downgrade the master envelope to an organizational obstruction
(see "claim boundary" above) without the quantitative claim.

### Sub-lane 4c: P3 derivation or downgrade
The K-series tail. Same options as 4b.

### Sub-lane 4d: runner reconciliation
Hygiene-only: make runner output and prose agree on the rounded
envelope and m_t uncertainty.

## Success criteria

- All three residuals (P1, P2, P3) are either derived from registered
  one-hop authorities or honestly downgraded with the master envelope
  scoped accordingly.
- The runner asserts the envelope from the inputs with explicit
  correlation rules, not from hard-coded constants.
- `yt_uv_to_ir_transport_obstruction_theorem_note_2026-04-17` re-audits
  away from `audited_numerical_match` toward `audited_clean`.

## Branch / worker conventions

- Suggested top-level proposal: `claude/yt-uv-to-ir-residual-derivation-2026-04-27`.
- Sub-branches per residual: `claude/yt-p1-derivation-2026-04-27`,
  `claude/yt-p2-derivation-2026-04-27`, etc.
- Each sub-residual is its own focused branch and review pair.

## What this lane is NOT

- Not a request to weaken the m_t numerical agreement. PDG agreement
  to 0.07% is real. The audit issue is the **derivation** behind it,
  not the comparator match.
- Not a request to redo the Ward identity itself. That's the parent
  authority and the audit treats it as registered.
- Not blocked on Lane 1 — sub-lanes 4b, 4c, and 4d can proceed in
  parallel. Sub-lane 4a's full closure depends on Lane 1.
