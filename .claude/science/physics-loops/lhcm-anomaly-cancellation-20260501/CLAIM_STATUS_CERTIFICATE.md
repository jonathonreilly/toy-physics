# Claim Status Certificate — LH-Doublet SU(2)²×U(1)_Y Anomaly Cancellation

**Block:** lhcm-anomaly-cancellation-block01-20260501
**Branch:** physics-loop/lhcm-Q-T3-Y-derivation-block01-20260501
**Artifact:** docs/LH_DOUBLET_SU2_SQUARED_HYPERCHARGE_ANOMALY_CANCELLATION_NOTE_2026-05-01.md
**Runner:** scripts/frontier_lh_doublet_su2_squared_hypercharge_anomaly.py

## Status

```yaml
actual_current_surface_status: support / structural anomaly-cancellation theorem (partial repair of LHCM audit)
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: "Standard SU(2) Dynkin index T(2) = 1/2 admitted; standard QFT triangle-anomaly formula A = Σ T(R) Y(R) admitted; SM photon-definition convention Q = T_3 + Y/2 named but NOT used as proof input."
proposal_allowed: false
proposal_allowed_reason: "Closes ONE of three repair-target items in the LHCM audit verdict (the SU(2)² × U(1)_Y anomaly cancellation for LH doublets). Items (1) matter assignment, (2) U(1)_Y normalization, and the remaining anomaly identities (R-A) SU(3)² × Y, (R-B) Y³, (R-C) gravitational × Y all remain open. LHCM stays audited_conditional after this."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Disposition

**Goal:** address ONE of the three repair-target items named in the
2026-05-01 audit verdict on `LEFT_HANDED_CHARGE_MATCHING_NOTE.md`
(LHCM, rank 3 in the LHF leverage map, **267 transitive descendants**).
The audit asked for "anomaly-complete chiral completion from the
graph-first surface."

**This block closes:** SU(2)² × U(1)_Y triangle anomaly cancellation
for the LH-doublet sector, derived from the framework's retained
graph-first eigenvalues (`y_Sym = +1/3`, `y_Anti = −1`) and the SU(2)
doublet Dynkin index `T(2) = 1/2`.

**Key structural insight:** the cancellation `3 · (+1/3) + 1 · (−1) = 0`
is identically the **trace-freeness condition** on the gl(3) ⊕ gl(1)
commutant's u(1) direction. The anomaly identity is the same equation
as the trace-free constraint — it is forced by the framework's
structural surface, not tuned. Verified at exact-rational precision
across a range of trace-free `(y_Sym, y_Anti)` pairs.

**This block does NOT close:**
- Repair-target items (1) "matter assignment" and (2) "U(1)_Y
  normalization" — these go to ONE_GENERATION_MATTER_CLOSURE.
- (R-A) SU(3)² × Y anomaly — needs RH-quark sector.
- (R-B) Y³ anomaly — needs full one-generation matter content.
- (R-C) Gravitational × Y anomaly — needs full one-generation matter content.

## Allowed PR/Status Wording

- "support / structural anomaly-cancellation theorem"
- "partial repair of LHCM audit"
- "closes one of three repair-target items"
- "the cancellation is the trace-freeness condition restated"
- "exact rational arithmetic"

## Forbidden PR/Status Wording

- bare "retained" / "promoted"
- "promotes LHCM to retained-grade"
- "closes the anomaly-complete chiral completion"
- "derives Q = T_3 + Y/2 from first principles" (it does not — that's admitted convention)

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_lh_doublet_su2_squared_hypercharge_anomaly.py
# expected: PASS=24 FAIL=0
```

The runner verifies:
- Note structure (title, status, retained authorities cited; no
  load-bearing import from parent LHCM).
- Eigenvalue pattern (+1/3, −1) is the unique trace-free direction with
  the 1-dim block normalized to −1 (Fraction equality).
- SU(2) doublet Dynkin index `T(2) = 1/2` from `Tr[T_i T_j] = (1/2) δ_{ij}`
  (machine precision).
- Anomaly contribution `A = 3 · (1/2) · (+1/3) + 1 · (1/2) · (−1) = 0`
  exactly as a Fraction (not floating-point).
- The cancellation identity = the trace-freeness condition: holds for
  ALL (y_Sym, y_Anti) satisfying `3 y_Sym + y_Anti = 0`, not just the
  retained values.
- Remaining (R-A), (R-B), (R-C) anomaly identities explicitly named as
  out-of-scope.
- Q = T_3 + Y/2 named as admitted convention NOT used as proof input.

## Independent Audit

Audit must verify:

1. The cited retained-grade upstreams (`GRAPH_FIRST_SU3_INTEGRATION_NOTE`,
   `GRAPH_FIRST_SELECTOR_DERIVATION_NOTE`, `NATIVE_GAUGE_CLOSURE_NOTE`)
   have retained-grade `effective_status` on `main` at the time of audit.
2. The eigenvalue pattern `+1/3, −1` is correctly retained-cited from
   `GRAPH_FIRST_SU3_INTEGRATION_NOTE` (the runner's Part 2 reproduces
   it from first principles via the trace-free constraint).
3. The SU(2) Dynkin index `T(2) = 1/2` matches the convention used in
   `NATIVE_GAUGE_CLOSURE_NOTE`'s native cubic SU(2) generators.
4. The anomaly-coefficient formula `A = Σ T(R) Y(R)` is the standard
   QFT triangle-anomaly result (textbook bridge, admitted).
5. The note does not import any load-bearing content from the parent
   LHCM (verified by Part 1 of the runner).
6. After this note lands and the audit ledger regenerates, the LHCM
   open_dependency_paths surface should narrow to exclude the
   SU(2)²×Y anomaly piece for LH doublets, while continuing to flag
   the (R-A), (R-B), (R-C) and items (1), (2) as open.

## What this changes for the leverage map

LHCM's LHF leverage entry (PR #248 rank 3, 488 transitive descendants)
moves slightly: from "blocked by missing anomaly-complete chiral
completion + matter assignment + U(1)_Y normalization" to "blocked by
matter assignment + U(1)_Y normalization + remaining anomalies (R-A,
R-B, R-C)". Net: one of three repair-target items closed, two remain;
plus the 3 sub-anomalies (R-A, R-B, R-C) for the RH sector.

LHCM stays `audited_conditional` until ONE_GENERATION_MATTER_CLOSURE
provides the remaining inputs.
