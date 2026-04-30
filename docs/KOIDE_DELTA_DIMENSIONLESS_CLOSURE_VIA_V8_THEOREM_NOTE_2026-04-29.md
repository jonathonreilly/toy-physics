# Koide δ Dimensionless Closure via V8 Theorem (V1)

**Date:** 2026-04-29
**Status (actual current surface):** `proposed_retained` author proposal for
the DIMENSIONLESS `δ = 2/9` closure on the A_min surface, composing
V8 (Block 1, Koide Q OP-Locality Source-Domain Closure) with the
retained Brannen phase reduction theorem and Plancherel identity. The
RADIAN-BRIDGE postulate P (Type-B-to-radian identification) remains an
explicitly named residual; the literal `δ = 2/9 rad` Brannen-PDG match
is recorded as `support-grade` numerical witness, NOT promoted by this
note. Bare `retained` / `promoted` is NOT used.
**Primary runner:** `scripts/frontier_koide_delta_dimensionless_closure_via_v8.py`

**Cited authorities (one-hop deps):**
- [KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md](KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md)
  — V8 Q closure (Block 1; `proposed_retained`); load-bearing input
  for the dimensionless δ chain.
- [KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
  — Brannen phase reduction theorem (`δ = Q/d` from doublet
  conjugate-pair `n_eff = 2` and `d = 3`); retained on `main`.
- [KOIDE_A1_BRANNEN_PLANCHEREL_IDENTITY_SUPPORT_NOTE_2026-04-25.md](KOIDE_A1_BRANNEN_PLANCHEREL_IDENTITY_SUPPORT_NOTE_2026-04-25.md)
  — Plancherel identity `arg(b) = δ (mod 2π)` inside the Brannen
  parameterization; support-grade.
- [KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md](KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md)
  — Q-δ linking relation; the `δ = Q/d` chain, retained as conditional.
- [KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md](KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md)
  — `Q = p · δ` arithmetic identity; retained.
- [KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)
  — radian-bridge no-go through canonical R/Z → U(1) qubit lift;
  retained negative result.

---

## 0. Headline

The Koide `δ = 2/9` closure has two distinct semantic layers:

1. **Dimensionless layer:** `δ = n_eff/d² = 2/9` as a pure rational
   from doublet conjugate-pair structure (`n_eff = 2`) + cubic Z_3
   order (`d = 3`).
2. **Radian layer:** `δ_observed ≈ 2/9 rad` from Brannen-PDG match
   (`<0.1%`), with `δ = 4π/9 rad` (canonical R/Z → U(1) lift) failing
   PDG outright.

The Brannen phase reduction theorem and the Q-δ linking relation
already retained the dimensionless chain CONDITIONAL on `Q = 2/3`
(I1 in V4's terminology). Block 1 (V8) closed `Q = 2/3` as
`proposed_retained` from the A_min surface via the OP-locality
structural argument.

**This V1 note composes V8 (Block 1) with the retained Brannen pieces
to lift the dimensionless `δ = 2/9` from CONDITIONAL to UNCONDITIONAL
on A_min**, modulo audit ratification of V8 (Block 1).

The RADIAN bridge (literal 2/9 rad ≡ dimensionless 2/9) is NOT closed
by this note. It remains the named residual postulate P, with the
empirical Brannen-PDG match recorded as support-grade numerical
witness only.

---

## 1. Composed chain

```text
A_min  +  PHYSICAL_LATTICE_NECESSITY §9  +  OP T1+T2  +  ONSITE no-go
       +  Canonical-descent T1  +  CRIT
   ─[V8 chain (Block 1, 2026-04-29)]─→  Q = 2/3 (proposed_retained)

Q = 2/3  +  Brannen phase reduction theorem
   ─[δ = Q/d at d = 3]─→  δ = 2/9 (DIMENSIONLESS, proposed_retained)

Brannen Plancherel identity
   ─[arg(b) = δ (mod 2π) inside Brannen parameterization]─→
       arg(b) = 2/9 (mod 2π) on the Brannen carrier
```

The composition uses only retained authorities + V8 (Block 1). No
observed lepton mass enters.

The retained `Q = p·δ` arithmetic identity (`Q = 2/3 = 3 · (2/9) =
p · δ`) is now structurally forced rather than an arithmetic
coincidence on the support-route values: V8 closes Q, and Brannen
phase reduction gives δ = Q/d = Q/p, so `Q · 1 = p · (Q/p) = p · δ`
identically.

---

## 2. Theorem statement

**Theorem (Koide δ Dimensionless Closure on A_min via V8).**
On the A_min surface (with V8 closure of Q from Block 1):

1. The dimensionless Brannen phase satisfies `δ = n_eff/d² = 2/9`,
   where `n_eff = 2` is the doublet conjugate-pair effective charge
   (Brannen phase reduction theorem §1.3) and `d = 3 = |C_3|` is the
   cyclic Z_3 order.
2. The Plancherel identity gives `arg(b) = δ (mod 2π) = 2/9 (mod 2π)`
   inside the Brannen parameterization.
3. The retained `Q = p·δ` arithmetic identity (`Q = 3δ` at p = d = 3)
   is now structurally forced rather than coincidental.

**Status:** `proposed_retained` for the DIMENSIONLESS reading on A_min.
Audit-required-before-effective-retained flag carried per skill.

The identification of dimensionless `2/9` with `2/9 rad` (postulate P)
is NOT closed by this theorem.

### Proof

**Step 1 (Q closure).** By V8 (Block 1, 2026-04-29), `Q = 2/3` is
`proposed_retained` on A_min via the OP-locality structural chain.

**Step 2 (Brannen phase reduction).** By KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM
§1.3 + §2.3:
- `n_eff = 2` is structurally derived from the doublet conjugate-pair
  forcing (`L_ω̄ = conj(L_ω)` ⇒ projective ratio `e^{-2iθ}` with
  winding number 2).
- `d = 3 = |C_3|` is structural (cubic Z_3 order).
- `δ = n_eff/d² = 2/9` follows from the Brannen normalization
  (per-step phase advance / total Z_3 period).
- Equivalently `δ = Q/d` since `Q = n_eff/d`.

**Step 3 (Plancherel identity).** By KOIDE_A1_BRANNEN_PLANCHEREL_IDENTITY
§1, `b = (√3/2) V_0 c · exp(iδ)` inside the Brannen parameterization,
hence `arg(b) = δ (mod 2π)`. Composing with Step 2: `arg(b) = 2/9
(mod 2π)`.

**Step 4 (Q = p·δ identity).** Substituting `Q = 2/3` (V8) and
`δ = Q/d = 2/9` (Step 2), the retained KOIDE_Q_EQ_3DELTA_IDENTITY
`Q = p · δ` reads `2/3 = 3 · (2/9)`, which is structural rather than
an arithmetic coincidence on observed values.

**QED on the dimensionless reading.**

The radian-bridge step (postulate P) is not part of this theorem.

---

## 3. Status firewall fields (per skill SKILL.md §Claim-Status Firewalls)

```yaml
actual_current_surface_status: proposed_retained
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: true
proposal_allowed_reason: |
  Composes V8 (Block 1 proposed_retained Q closure) with retained
  Brannen phase reduction theorem and Plancherel identity. No new
  axiom, no observed mass. The dimensionless δ = 2/9 chain is
  axiom-to-readout once V8 lands.
audit_required_before_effective_retained: true
bare_retained_allowed: false
radian_bridge_postulate_P_status: open  # not closed by this note
literal_2_over_9_rad_pdg_match_status: support_grade_numerical_witness
```

The bare `retained` wording is BANNED on this branch-local source note
per the skill's claim-status firewall. The radian-bridge postulate P
is NOT presented as closed; the literal 2/9 rad PDG match is recorded
as support-grade only.

---

## 4. What is and is NOT closed

### Closed by V1 (this note)

1. dimensionless `δ = 2/9 = n_eff/d²` on A_min (proposed_retained,
   composed with V8);
2. structural status of the `Q = p·δ` arithmetic identity (now forced
   rather than coincidental);
3. Plancherel `arg(b) = 2/9 (mod 2π)` inside the Brannen parameterization
   on A_min.

### NOT closed by V1 (carried forward)

1. **Postulate P (radian-bridge):** identification of dimensionless
   `2/9` with `2/9 rad` as a physical Berry holonomy. The Brannen
   normalization gives 2/9 dimensionless via division by `2π·d = 6π`;
   to convert back to radians per Z_3 step, multiply by 2π gives
   `4π/9 rad`, NOT `2/9 rad`. The Brannen-PDG match `δ = 2/9 rad
   ≈ 0.222 rad` matches PDG `<0.1%` empirically, but no structural
   chain on A_min derives this radian value.
2. The Z_3 qubit no-go closes the canonical R/Z → U(1) lift route
   (`χ(2/9) = exp(2πi · 2/9)`) — the lift gives 4π/9 rad, which fails
   PDG. Other routes to P remain.
3. Selected-line dynamics selection of `m_*` (Berry phase identification
   on H_sel(m) at the dynamics-selected `m_*`) — this is the
   "promotion of the Berry-phase theorem stack to retained-main"
   target named in KOIDE_A1_BRANNEN_PLANCHEREL_IDENTITY §6.
4. Callan-Harvey-style anomaly bridge to identify the dynamics value
   with a retained ambient anomaly/Plancherel rational — current best
   candidate is KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22,
   bridge-conditioned support.
5. Overall lepton scale `v_0`.
6. Down-type quark cross-sector universality of the V8 chain (Block 3).

### Codex-level pressure points

**P1 (whether dimensionless `δ = 2/9` is genuine progress without P).**
The Brannen-PDG match makes the literal radian reading the PHYSICAL
observable. Without P, the dimensionless 2/9 is not the observed δ.
Response: V1 closes the dimensionless half because it composes V8
with retained Brannen pieces; the PDG match becomes a sharp
falsifiable target for postulate P (rather than two independent open
imports). This is genuine import retirement at the dimensionless
layer, even if P remains.

**P2 (wishful composition).** The Brannen phase reduction theorem
(2026-04-20) was retained CONDITIONAL on Q = 2/3 (I1 open at the time).
V8 (Block 1, 2026-04-29) closes Q on A_min. Composing the two is the
intended use of "conditional theorem becomes unconditional once
condition closes." V1 does not introduce new content beyond the
composition; the strict-reading worry sits entirely inside V8.

---

## 5. Comparison with prior δ work

| Element | KOIDE_BRANNEN_PHASE_REDUCTION (2026-04-20) | KOIDE_A1_BRANNEN_PLANCHEREL_IDENTITY (2026-04-25) | This V1 (2026-04-29) |
|---|---|---|---|
| `δ = Q/d` chain | retained conditional on Q | unchanged | retained unconditional via V8 |
| Plancherel `arg(b) = δ` | retained | support-grade | composed support |
| Postulate P | open | open | open (unchanged) |
| `Q = 2/3` source | I1 open | unchanged | V8 (Block 1) proposed_retained |
| Closure status | conditional | conditional | dimensionless δ = 2/9 proposed_retained |
| Audit required | yes | yes | yes |

V1 does NOT supersede prior notes. It composes them with V8.

---

## 6. Cascade unlocked (proposed for later weaving)

If V1 is audit-ratified (depends on V8 audit ratification first):

- **line 192 (charged-lepton Koide bridge package):** δ residual moves
  from "open" to "dimensionless closed; radian-bridge open" status —
  the cascade is partially complete.
- **line 166 (charged-lepton Koide support package Q=2/3, δ=2/9):**
  dimensionless half promotable; radian-bridge half remains support.
- **lines 158–162 (CKM Koide-bridge supports):** "no Koide closure"
  qualifier removable for both Q and the dimensionless δ.

Repo-wide weaving is DEFERRED to later review.

---

## 7. Verification

```bash
python3 scripts/frontier_koide_delta_dimensionless_closure_via_v8.py
```

The runner audits:

1. V8 (Block 1) note exists on disk + carries `proposed_retained` +
   audit-required flag + Q = 2/3 chain.
2. Brannen phase reduction theorem exists on disk + `n_eff = 2` +
   `d = 3` + `δ = n_eff/d²`.
3. Plancherel identity exists on disk + `arg(b) = δ (mod 2π)`.
4. Q = p·δ identity exists on disk + p = d = 3.
5. Z_3 qubit radian-bridge no-go exists on disk + closes canonical
   R/Z → U(1) lift route.
6. Algebraic identities (sympy):
   - `n_eff = 2` (doublet conjugate-pair winding number);
   - `d = 3` (|C_3|);
   - `δ = 2/9` (n_eff/d²);
   - `Q = 2/3 = 3 · (2/9) = p · δ`.
7. No observed lepton mass enters proof.
8. Postulate P explicitly NOT closed (status flag `radian_bridge_postulate_P_status: open`).

Expected: PASS=N, FAIL=0.

---

## 8. Stretch-attempt addendum: radian-bridge structural candidates

Recorded for future investigation (not part of V1 closure):

### S1: Z_3 representation natural angle unit

Hypothesis: the framework's natural angle output for `arg(b)` on the
Z_3 doublet is in radians, and the dimensionless 2/9 from Brannen
normalization happens to be the radian value because the framework's
fundamental-domain choice for arg() puts the Z_3 doublet phase in
the small-angle regime [0, 2π/3) rather than [0, 2π).

**Status:** speculative; not pursued in V1.

### S2: Callan-Harvey anomaly bridge

Hypothesis: an η-invariant or APS-style anomaly on the Z_3 fixed locus
gives a radian value of 2/9 directly, identifying the
representation-theoretic dimensionless 2/9 with a physical anomaly
phase in radians.

**Status:** carried in KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE
(2026-04-22) as bridge-conditioned support; not closed.

### S3: Selected-line dynamics selection

Hypothesis: the selected-line dynamics on `H_sel(m)` selects `m_*`
via a structural framework principle (not by matching PDG). At the
selected `m_*`, the Berry holonomy on the doublet evaluates to
`2/9 rad` exactly.

**Status:** open; depends on a selected-line dynamics theorem that
the framework's authority on `main` does not yet have.

These three candidates are recorded for future Block work or for
review-loop assignment. None is closed in V1.

---

## 9. Honest residual

After V1 lands as `proposed_retained` (composed with V8), the
remaining Koide closure residuals are:

- **Postulate P (radian-bridge):** literal 2/9 rad ≡ dimensionless 2/9
  identification — open.
- Selected-line dynamics selection of `m_*` (S3 above) — open.
- Overall lepton scale `v_0` — out of campaign scope.
- Down-type quark cross-sector universality (Block 3) — pending.

The dimensionless half of Koide δ is now structurally on A_min modulo
audit ratification of V8 (Block 1) and V1 (this note).
