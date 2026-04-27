# Koide δ = 2/9 Closure-Chain Audit (post-Target-B)

**Date:** 2026-04-25
**Status:** chain-audit / progress-tracking note. **Does NOT close `δ = 2/9` on the live authority surface.** It composes the now-retained
cross-sector identification (Target B, this branch) with the retained
April-20 IDENTIFICATION and retained reduction theorem to map the
remaining open gap precisely. The remaining gap is the Q-side primitive
`P_Q = 1/2` (Target A articulated as candidate, not derived).
**Companion notes:**
- `docs/CL3_N_COLOR_EQUALS_N_GEN_SHARED_D3_ORIGIN_THEOREM_NOTE_2026-04-25.md` (Target B closure)
- `docs/CL3_YUKAWA_CASIMIR_DIFFERENCE_BRIDGE_CANDIDATE_NOTE_2026-04-25.md` (Target A candidate)

---

## 0. Purpose

After this branch lands, the live authority surface has the following
closure chain for the charged-lepton Brannen `δ = 2/9 rad`:

```text
IDENTIFICATION:    δ(m) = Berry holonomy on selected-line CP¹      [retained]
                                           ↓
REDUCTION/SHAPE:   δ = n_eff / d² = 2/9 (n_eff = 2, d = 3)         [retained]
                                           ↓
CROSS-SECTOR:      Bernoulli (N − 1)/N² = 2/9 on BOTH sectors      [Target B, this branch]
                                           ↓
SELECTION:         δ_Berry(m_*) = 2/9 rad ⟸ Q_l = 2/3              [conditional on Target A]
                                           ↓
Q-SIDE:            Q_l = 2/3 from P_Q = |b|²/a² = 1/2              [STILL OPEN]
```

This note audits the chain in detail, identifies what's now retained vs
still conditional, and names the precise remaining gap. It does not
itself prove any new theorem; it is a composition / progress-tracking
note.

---

## 1. Chain step audit

### 1.1 IDENTIFICATION — retained on main (April 20)

[`KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)
§4 explicitly retains:

> **Closed:** `δ(m)` is the actual Berry holonomy on the selected-line
> `CP¹` carrier.

The Berry holonomy is `Hol(m_0 → m) = θ(m) − 2π/3` where `θ(m)` is the
continuous Berry coordinate of the projective `C_3` doublet ray. By the
universal definition of an integral of a connection 1-form
`A = dθ` (where `θ` is the angle around the unit circle), `δ(m)` is a
**continuous-rad observable**, in radians by construction, with no
`R/Z → U(1)` exponential lift.

**Status:** retained closed. The audit's `P_A1` framing
(`R/Z → U(1)` period convention on a Type-B invariant) is conditional
on the *wrong* identification: under the live April-20 IDENTIFICATION,
`δ` is already rad-valued and the convention question doesn't arise.

### 1.2 REDUCTION/SHAPE — retained on main (April 20 reduction theorem)

[`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
retains:

```text
δ = n_eff / d²   with n_eff = 2 (from C_3 conjugate-pair forcing)
                       d     = 3 (from A0 |C_3|).
Equivalently: δ = Q/d (Q = n_eff/d = 2/d at d = 3).
```

`n_eff = 2` is **structurally forced** by the projective doublet
coordinate `[1 : e^{−2iθ}]` (winding number 2), not chosen.
`d = 3` is from A0.

**Status:** retained, conditional on (i) `Q_l = 2/d = 2/3` and (ii) the
radian-bridge postulate `P` (lifting dimensionless `n_eff/d²` to literal
radians).

The (ii) condition is the audit's `P_A1` — but per §1.1, the
IDENTIFICATION is already to a continuous-rad observable, so there is no
R/Z lift to perform. The dimensionless `n_eff/d²` is then read directly
as a rad value of the Berry holonomy.

### 1.3 CROSS-SECTOR — retained on this branch (Target B)

[`CL3_N_COLOR_EQUALS_N_GEN_SHARED_D3_ORIGIN_THEOREM_NOTE_2026-04-25.md`](CL3_N_COLOR_EQUALS_N_GEN_SHARED_D3_ORIGIN_THEOREM_NOTE_2026-04-25.md)
(this branch) closes the cross-sector identification:

```text
N_color = N_gen = d = 3   from shared A0 origin.
```

This **promotes** the retained CKM Bernoulli identity
`(N_color − 1)/N_color² = 2/9` ([`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md))
to the lepton side: `(N_gen − 1)/N_gen² = 2/9`.

**Status:** retained on this branch. The "promotion of `N_color = N_gen`
to retained status would still require a separate theorem" gap named
in the Bernoulli note's §3 is filled.

**Multi-route convergence on `2/9`:** with this promotion, the value
`2/9` is now multi-route determined on retained data:
- reduction theorem: `δ = n_eff/d² = 2/9` (n_eff = 2, d = 3)
- Bernoulli K6 on lepton side: `(N_gen − 1)/N_gen² = 2/9` (N_gen = 3)
- Bernoulli K6 on CKM side: `(N_color − 1)/N_color² = 2/9` (N_color = 3)
- April 22 geometry support: `α(m_*) − α(m_0) = −2/9` exact at `1e-12` on
  retained selected-line `H_sel(m)` (numerical witness)

All four routes give the same value, with shared origin in `d = 3`
from A0 (and `n_eff = 2 = d − 1` at d = 3, a numerical coincidence at
the framework's retained `d = 3`).

### 1.4 SELECTION — conditional on Target A

The April-20 no-go § 4 explicitly identifies the remaining open question:

> **Still open:** why the physical branch picks the specific interior
> value `δ = 2/d² = 2/9`.

The reduction theorem (§1.2) provides the route: `δ = Q/d` with
`Q = 2/3` and `d = 3` gives `δ = 2/9`. This is the April-20 no-go's
exit route #3 (dependent `Q → CPC → δ` promotion).

**Status:** the SELECTION question reduces to closing `Q_l = 2/3` on
retained main. Once that is retained, the reduction theorem composes
with the retained IDENTIFICATION (§1.1) to give:

```text
δ = Q/d = (2/3)/3 = 2/9   AND   δ is the Berry holonomy in radians
                                ⇒ δ = 2/9 rad on retained data.
```

### 1.5 Q-SIDE — STILL OPEN (Target A articulates candidate)

The Q-side primitive remains:

```text
P_Q = |b|² / a² = 1/2   ⇔   Q_l = 2/3.
```

Three retained support faces all give `1/2`
(`KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md`):

- `dim(spinor) / dim(Cl⁺(3)) = 2/4 = 1/2`
- `T(T+1) − Y² = 1/2` (lepton L doublet)
- `(T(T+1) − Y²) / (T(T+1) + Y²) = 1/2`

[`CL3_YUKAWA_CASIMIR_DIFFERENCE_BRIDGE_CANDIDATE_NOTE_2026-04-25.md`](CL3_YUKAWA_CASIMIR_DIFFERENCE_BRIDGE_CANDIDATE_NOTE_2026-04-25.md)
(this branch) sharpens the candidate physical bridge into a single
named lemma:

> Yukawa Casimir-difference candidate lemma:
> `|b|² / a² = T(T+1) − Y²` on the physical lepton Yukawa amplitude.

The RHS = 1/2 is **retained** from `CL3_SM_EMBEDDING_THEOREM`. The LHS
is the Q-bridge primitive. The bridge between them is the open closure
step.

**Status:** STILL OPEN. The candidate lemma is articulated and its RHS
is retained, but the structural derivation chain identifying LHS = RHS
on the physical Yukawa amplitude is not supplied.

---

## 2. What this branch retains for the δ-closure chain

After this branch lands, the chain status is:

| Step | Status before this branch | Status after this branch |
|---|---|---|
| 1.1 IDENTIFICATION (δ = Berry holonomy in rad) | retained (April 20) | retained (April 20) |
| 1.2 REDUCTION (δ = n_eff/d² = 2/9) | retained, conditional on (i) Q + (ii) radian-bridge | retained, conditional on Q only (radian-bridge is moot per §1.1) |
| 1.3 CROSS-SECTOR (N_color = N_gen = 3) | open (named blocker) | **retained on this branch (Target B)** |
| 1.4 SELECTION (δ_Berry(m_*) = 2/9) | open | conditional on Q (Target A) |
| 1.5 Q-SIDE (P_Q = 1/2) | open | candidate articulated, still open (Target A) |

The single remaining open primitive is `P_Q = |b|² / a² = 1/2` (Q-side).
All other steps are retained on the live authority surface (or
conditional on Q only).

---

## 3. The remaining gap is one named primitive

This audit reduces the `δ = 2/9 rad` open closure to a single named
primitive:

```text
[OPEN]  P_Q := |b|² / a² = 1/2 on the physical charged-lepton Yukawa amplitude.
```

The candidate physical bridge for `P_Q` is the Yukawa Casimir-difference
lemma `|b|² / a² = T(T+1) − Y²` (Target A). Its RHS is retained. Its LHS
is the primitive. The structural derivation chain identifying LHS=RHS
is the named missing step.

Once `P_Q = 1/2` is closed:

```text
P_Q = 1/2  ⇒  c = √2  ⇒  Q_l = 2/3                           (Brannen, retained)
            ⇒  δ = Q/d = 2/3 / 3 = 2/9                       (reduction theorem, retained)
            and δ = Berry holonomy in radians                (April 20, retained)
            ⇒  δ = 2/9 rad on retained main inputs.
```

Cross-sector consistency from Target B: `(N − 1)/N² = 2/9` on both
CKM and lepton sectors via shared `N = 3` from A0.

**This is the precise open primitive after this branch.**

---

## 4. Closeout flags

```text
DELTA_2_OVER_9_RAD_CLOSURE_ON_RETAINED_MAIN=NOT_CLOSED
IDENTIFICATION_DELTA_AS_BERRY_HOLONOMY_RAD_VALUED=RETAINED_ON_APRIL_20
REDUCTION_THEOREM_DELTA_EQ_N_EFF_OVER_D_SQ=RETAINED_CONDITIONAL_ON_Q
CROSS_SECTOR_N_COLOR_EQ_N_GEN_EQ_3=RETAINED_THIS_BRANCH_TARGET_B
P_Q_BRIDGE_PHYSICAL_DERIVATION=STILL_OPEN_TARGET_A_ARTICULATED_NOT_CLOSED
NUMBER_OF_OPEN_PRIMITIVES_FOR_DELTA_CLOSURE=1
SINGLE_REMAINING_PRIMITIVE=P_Q_EQ_HALF_VIA_YUKAWA_CASIMIR_DIFFERENCE_BRIDGE
```

---

## 5. Verification

This is a chain-audit / composition note. The verification consists of
running the upstream and Target-B/Target-A runners in sequence:

```bash
# Target B runner — closes cross-sector identification:
python3 scripts/frontier_cl3_n_color_equals_n_gen_shared_d3_origin.py

# Target A runner — articulates candidate lemma, retains RHS pieces:
python3 scripts/frontier_cl3_yukawa_casimir_difference_bridge_candidate.py

# Upstream retained runners (already on main) for chain steps 1.1, 1.2, 1.3:
python3 scripts/frontier_koide_selected_line_local_radian_bridge_no_go_2026_04_20.py
python3 scripts/frontier_koide_brannen_phase_reduction_theorem.py
python3 scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py
python3 scripts/frontier_koide_brannen_route3_geometry_support.py
```

This audit note adds no new runner of its own — it is a composition map.

---

## 6. Cross-references

- [`CL3_N_COLOR_EQUALS_N_GEN_SHARED_D3_ORIGIN_THEOREM_NOTE_2026-04-25.md`](CL3_N_COLOR_EQUALS_N_GEN_SHARED_D3_ORIGIN_THEOREM_NOTE_2026-04-25.md) — Target B closure
- [`CL3_YUKAWA_CASIMIR_DIFFERENCE_BRIDGE_CANDIDATE_NOTE_2026-04-25.md`](CL3_YUKAWA_CASIMIR_DIFFERENCE_BRIDGE_CANDIDATE_NOTE_2026-04-25.md) — Target A candidate
- [`KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md) — April 20 IDENTIFICATION (retained Closed)
- [`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md) — REDUCTION shape `δ = n_eff/d² = 2/9`
- [`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md) — CKM-side Bernoulli K6, names Target B as missing
- [`KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md`](KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md) — Q-side single primitive `P_Q = 1/2`
- [`KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`](KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md) — geometry support, numerical witness
- [`KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`](KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md) — original audit (P_A1 framing now superseded by April 20 IDENTIFICATION)
