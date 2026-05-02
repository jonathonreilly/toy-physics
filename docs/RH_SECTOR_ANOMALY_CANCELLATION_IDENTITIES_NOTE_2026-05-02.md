# RH-Sector Anomaly Cancellation Identities: SU(3)²×Y, Y³, and Gravitational²×Y

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on the LHCM-conditional
one-generation content surface (NOT retained, NOT proposed_retained — see
CLAIM_STATUS_CERTIFICATE.md). Closes the explicit verification of LHCM repair
items (R-A), (R-B), (R-C) as exact rational identities given LH eigenvalue
inputs from graph-first SU(3) integration and RH content from
`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24`.
**Primary runner:** `scripts/frontier_rh_sector_anomaly_cancellation_identities.py`
**Authority role:** support companion to PR #253's SU(2)²×U(1)_Y theorem,
extending the trace-freeness structural pattern to the full one-generation
LH+RH commutant surface.

## 0. Statement

**Theorem (RH-sector anomaly cancellation as exact identities).**
Given:

1. the retained left-handed eigenvalue pattern on the graph-first selected-axis
   surface
   `Y(Q_L) = +1/3, Y(L_L) = −1`
   (graph_first_su3_integration ⇒ Sym²/Anti² 3⊕1 split with traceless
   abelian generator at eigenvalue ratio 1:(−3); convention-fixed by
   lepton-doublet normalization to −1);

2. the right-handed sector content from
   `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24`
   `Y(u_R) = +4/3, Y(d_R) = −2/3, Y(e_R) = −2, Y(ν_R) = 0`,

then the three remaining triangle-anomaly traces over the full one-generation
content vanish **identically as exact rational arithmetic**:

```text
(R-A)  Tr[SU(3)² Y]_one-gen        = 0   exactly (Fraction equality)
(R-B)  Tr[Y³]_one-gen              = 0   exactly (Fraction equality)
(R-C)  Tr[Y]_one-gen × grav²       = 0   exactly  (the grav²×Y identity reduces to
                                                   the linear hypercharge sum)
```

These are LHCM verdict-rationale repair items (R-A), (R-B), (R-C) explicitly
named in `LEFT_HANDED_CHARGE_MATCHING_NOTE.md`'s audit verdict.

## 1. Retained / admitted inputs

| Ingredient | Class | Reference | Role |
|------------|-------|-----------|------|
| LH eigenvalue pattern (+1/3, −1) | retained corollary on graph_first_su3 surface | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md), [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) | LH side of the trace |
| RH eigenvalues (+4/3, −2/3, −2, 0) | derived from anomaly cancellation under (LH + ν_R neutral + Q(u_R)>0) | [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) | RH side of the trace |
| SU(3) Dynkin index `T(3) = 1/2` for fundamental | standard QFT machinery | Dynkin/Casimir bookkeeping | quark contributions to SU(3)² Y |
| chirality sign convention (LH `+`, RH `−`) | admitted bookkeeping | standard SM trace convention | sign assignment in trace |

No observed charge, mass, or running coupling is used. The convention
`Q = T_3 + Y/2` is **not** load-bearing in this note — only the hypercharge
values themselves enter the traces.

## 2. The three trace identities

We use the doubled-hypercharge convention `Y` from
[`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md): per
that note, `Q = T_3 + Y/2` and on `SU(2)` singlets `Q = Y/2`.

Per-generation matter content (LH and conjugates of RH):

| Field | SU(3) rep | SU(2) rep | multiplicity | Y | chirality |
|-------|-----------|-----------|--------------|---|-----------|
| Q_L (u_L, d_L) | 3 | 2 | 1 | +1/3 | +1 |
| L_L (ν_L, e_L) | 1 | 2 | 1 | −1 | +1 |
| u_R | 3 | 1 | 1 | +4/3 | −1 |
| d_R | 3 | 1 | 1 | −2/3 | −1 |
| e_R | 1 | 1 | 1 | −2 | −1 |
| ν_R | 1 | 1 | 1 | 0 | −1 |

In the LH-conjugate frame (all chiralities counted as left-handed),
the contributions are weighted by the signed multiplicity
`m = (multiplicity) × (chirality sign)`:

```text
Q_L:  m = +1, weight = SU(3)-rep × SU(2)-rep × multiplicity = 3 × 2 × 1 = 6 fermions
L_L:  m = +1, weight = 1 × 2 × 1 = 2 fermions
u_R:  m = −1, weight = 3 × 1 × 1 = 3 fermions
d_R:  m = −1, weight = 3 × 1 × 1 = 3 fermions
e_R:  m = −1, weight = 1 × 1 × 1 = 1 fermion
ν_R:  m = −1, weight = 1 × 1 × 1 = 1 fermion
```

### 2.1 (R-A) Tr[SU(3)² Y]

Only fermions in the SU(3) fundamental contribute. SU(3) Dynkin index
`T(3) = 1/2` per colour fundamental. SU(2) doublet multiplicity 2 enters for
LH quarks.

```text
Tr[SU(3)² Y] = T(3) × [ (+1) × 2 × Y(Q_L)
                       + (−1) × 1 × Y(u_R)
                       + (−1) × 1 × Y(d_R) ]

             = (1/2) × [ 2 × (+1/3) − (+4/3) − (−2/3) ]

             = (1/2) × [ 2/3 − 4/3 + 2/3 ]

             = (1/2) × [ (2 − 4 + 2)/3 ]

             = (1/2) × [ 0/3 ]

             = 0   ∎
```

**Structural insight:** the cancellation is the trace-freeness condition
`2 · Y(Q_L) − Y(u_R) − Y(d_R) = 0`, equivalently `Y(u_R) + Y(d_R) = 2 · Y(Q_L)`,
which expresses the requirement that the U(1)_Y direction be traceless on the
SU(3)-fundamental subspace of the full one-generation content (3 LH quark
flavours minus 3 RH up-type minus 3 RH down-type, weighted by Y).

This identity is the (R-A) repair item from LHCM's audit verdict.

### 2.2 (R-B) Tr[Y³]

Cubic trace over all chirality-signed fermions:

```text
Tr[Y³]   = (+1) × 6 × (1/3)³        # Q_L
         + (+1) × 2 × (−1)³         # L_L
         + (−1) × 3 × (4/3)³        # u_R
         + (−1) × 3 × (−2/3)³       # d_R
         + (−1) × 1 × (−2)³         # e_R
         + (−1) × 1 × 0³            # ν_R

         =     6 × (1/27)
             − 2
             − 3 × (64/27)
             − 3 × (−8/27)
             − 1 × (−8)
             − 0

         =     6/27
             − 2
             − 192/27
             + 24/27
             + 8

         =   (6 − 192 + 24)/27 + (−2 + 8)

         =   (−162)/27 + 6

         =   −6 + 6

         =   0   ∎
```

**Structural insight:** the cubic trace splits into a quark-sector contribution
`6/27 − 192/27 + 24/27 = −162/27 = −6` and a lepton-sector contribution
`−2 − (−8) = +6`, which cancel exactly.

Equivalently, separating colour and weak-isospin:
- Quark contribution: `6 · (1/3)³ − 3 · (4/3)³ − 3 · (−2/3)³ = −6`
- Lepton contribution: `2 · (−1)³ − 1 · (−2)³ − 1 · 0³ = +6`

This identity is the (R-B) repair item from LHCM's audit verdict.

### 2.3 (R-C) Tr[Y · gravity²]

The mixed gravitational-U(1) anomaly trace for a single U(1) generator `Y`
reduces to the **linear** sum `Tr[Y]` (the `gravity²` factor is the same
universal constant for every Weyl fermion):

```text
Tr[Y · gravity²]  =  c_grav × Tr[Y]
```

where `c_grav` is the universal gravitational-anomaly constant (independent of
fermion species). Therefore (R-C) reduces to verifying

```text
Tr[Y]   = (+1) × 6 × (+1/3)         # Q_L
         + (+1) × 2 × (−1)           # L_L
         + (−1) × 3 × (+4/3)         # u_R
         + (−1) × 3 × (−2/3)         # d_R
         + (−1) × 1 × (−2)           # e_R
         + (−1) × 1 × 0              # ν_R

         =   2 − 2 − 4 + 2 + 2 + 0

         =   0   ∎
```

**Structural insight:** the linear trace splits as
- LH contribution: `6 · (1/3) + 2 · (−1) = 2 − 2 = 0` — already zero on the
  retained LH eigenvalue surface (this is the LH trace-freeness identity used
  in `HYPERCHARGE_IDENTIFICATION_NOTE.md`);
- RH contribution: `−3 · (4/3) − 3 · (−2/3) − 1 · (−2) − 1 · 0 = −4 + 2 + 2 = 0`
  — also zero, in particular because (Y(u_R) + Y(d_R) + Y(e_R) + Y(ν_R)) =
  `4/3 − 2/3 − 2 + 0 = −4/3` and the multiplicity-weighted sum over RH content
  involving SU(3) fundamental multiplicity 3 cancels to zero.

The total `Tr[Y] = 0` is the (R-C) repair item from LHCM's audit verdict.

## 3. Structural unification

The three (R-A, R-B, R-C) cancellations and PR #253's SU(2)²×U(1)_Y
cancellation share a common structural pattern: each is a **trace-freeness
condition** on the U(1)_Y direction, restricted to a specific commutant
sub-decomposition:

| Anomaly | Sub-decomposition | Trace-freeness condition |
|---------|-------------------|---------------------------|
| SU(2)²×Y (PR #253) | LH-doublet sector (Sym² ⊕ Anti²) on weak C² | `3 · Y(Q_L) + 1 · Y(L_L) = 0`, i.e. `(+1) + (−1) = 0` |
| (R-A) SU(3)²×Y | SU(3)-fundamental sector | `2 · Y(Q_L) − Y(u_R) − Y(d_R) = 0` |
| (R-B) Y³ | full one-generation cubic | `6 · Y(Q_L)³ + 2 · Y(L_L)³ − 3 · Y(u_R)³ − 3 · Y(d_R)³ − Y(e_R)³ − Y(ν_R)³ = 0` |
| (R-C) Tr[Y]·grav² | full one-generation linear | `6 · Y(Q_L) + 2 · Y(L_L) − 3 · Y(u_R) − 3 · Y(d_R) − Y(e_R) − Y(ν_R) = 0` |

PR #253's structural insight that "the cancellation IS the trace-freeness
condition" generalizes: each anomaly cancellation in the SM corresponds to
trace-freeness of the U(1)_Y direction over a specific representation-theoretic
sub-decomposition of the full one-generation content.

## 4. What this note does NOT close

This note does **not**:

- **derive** the LH eigenvalue pattern (+1/3, −1) — that is the structural
  output of `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` (retained) plus a
  lepton-eigenvalue normalization convention (admitted; LHCM repair item (2));
- **derive** the RH content (+4/3, −2/3, −2, 0) — that is what
  `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24` derives
  given LH + ν_R neutral + Q(u_R) > 0;
- **derive** the matter assignment Sym(3)=quark vs Anti(1)=lepton — that
  follows from SU(3) representation content and is LHCM repair item (1);
- **derive** the SM photon `Q = T_3 + Y/2` from graph-first surface;
- **promote** LHCM, HYPERCHARGE_IDENTIFICATION_NOTE, or
  STANDARD_MODEL_HYPERCHARGE_UNIQUENESS to retained — those depend on
  upstream items still conditional under the current audit ledger.

This note ratifies (R-A), (R-B), (R-C) as **exact rational identities** given
the LH and RH inputs. It is a support theorem in the LHCM repair chain, not
itself a closure of LHCM.

## 5. Validation

- primary runner:
  [`scripts/frontier_rh_sector_anomaly_cancellation_identities.py`](../scripts/frontier_rh_sector_anomaly_cancellation_identities.py)
  — verifies (R-A), (R-B), (R-C) as exact `Fraction` identities (rational
  arithmetic, not floating-point) and cross-checks PR #253's
  SU(2)²×U(1)_Y cancellation as a sister identity.

## 6. Authority surface

- `actual_current_surface_status: exact algebraic identity / support theorem`
- `conditional_surface_status: companion to STANDARD_MODEL_HYPERCHARGE_UNIQUENESS conditional on LHCM and HYPERCHARGE_IDENTIFICATION`
- `proposal_allowed: false` — does not promote LHCM or SM-hypercharge-uniqueness; only documents (R-A,B,C) as exact identities given those theorems' conclusions
- `bare_retained_allowed: false`
- `audit_required_before_effective_retained: yes`

## 7. Cross-references

- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) — parent of repair items (R-A,B,C)
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) — supplies RH content
- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) — supplies LH eigenvalue pattern
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained primitive
- [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) — trace catalog this note extends
- PR #253 (open) — sister theorem for SU(2)²×U(1)_Y on LH-doublet sector
