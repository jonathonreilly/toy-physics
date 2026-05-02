# LHCM Y Normalization from Anomaly Cancellation and Electric-Charge Convention

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on the retained
graph-first surface — closes LHCM repair item (2) "U(1)_Y normalization"
modulo a single admitted SM-definition convention (`Q_e = −1` in elementary
charge units). NOT proposed_retained — see CLAIM_STATUS_CERTIFICATE.md.
**Primary runner:** `scripts/frontier_lhcm_y_normalization.py`
**Authority role:** Y-normalization closure of LHCM repair item (2);
sister theorem to PR #254 (R-A,B,C anomaly identities), PR #255 (matter
assignment), PR #253 (LH SU(2)²×Y).

## 0. Statement

**Theorem (LHCM Y normalization from anomaly cancellation and electric-charge convention).**

Let `α ∈ R*` be the unknown overall scale of the unique traceless abelian
generator on the LH-doublet sector with eigenvalue ratio 1:(−3) on
Sym²(C²):Anti²(C²). Set the scaled eigenvalues:
- `Y(Q_L) = α/3`     (quark doublet, eigenvalue +α/3 with α > 0)
- `Y(L_L) = −α`      (lepton doublet, eigenvalue −α)

Imposing the three remaining triangle anomaly cancellation conditions
`Tr[Y] = 0, Tr[Y³] = 0, Tr[SU(3)² Y] = 0` over the full one-generation
content (with structurally-determined SU(3) representation content from
`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02`), the RH
hypercharges as functions of `α`:

```text
Y(u_R) = +(4α)/3,  Y(d_R) = −(2α)/3,  Y(e_R) = −2α,  Y(ν_R) = 0.
```

Imposing the SM-definition convention `Q_e = −1` (elementary charge unit)
under `Q = T_3 + Y/2` for SU(2) singlets:
```text
Q(e_R) = Y(e_R) / 2 = −α = −1   ⟹   α = +1.
```

Therefore:
```text
Y(Q_L) = +1/3,  Y(L_L) = −1,  Y(u_R) = +4/3,  Y(d_R) = −2/3,
Y(e_R) = −2,   Y(ν_R) = 0.                                         (★)
```

The Y normalization scale `α = +1` is **forced** by the SM-definition
convention `Q_e = −1`. The eigenvalue *ratio* 1:(−3) on (Q_L, L_L) is
already retained from `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`.

## 1. Retained / admitted inputs

| Ingredient | Class | Reference | Role |
|------------|-------|-----------|------|
| traceless abelian generator with ratio 1:(−3) on Sym²:Anti² | retained | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | LH eigenvalue ratio (overall scale α free) |
| matter assignment Sym²(3) ↔ Q_L, Anti²(1) ↔ L_L | retained derived | [`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md) (cycle 2, PR #255) | identifies which sector is quark/lepton |
| (R-A,B,C) anomaly cancellation conditions | retained derived | [`RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md`](RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md) (cycle 1, PR #254) | constraint system for RH content |
| SU(2)²×U(1)_Y anomaly cancellation for LH | retained derived | PR #253 (open) | LH-doublet anomaly identity |
| electric-charge convention `Q = T_3 + Y/2` | admitted SM-definition convention | standard SM bookkeeping | charge formula on SU(2) singlets |
| **`Q_e = −1` in elementary charge units** | **admitted SM-definition convention** | standard SM particle labeling | overall scale of α |

No PDG observed values, no fitted selectors, no literature numerical
comparators are imported. The only admitted input fixing the overall scale
is the SM-definition convention `Q_e = −1`.

## 2. Derivation

### 2.1 Free overall scale on graph-first surface

`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` produces a unique traceless abelian
direction in the gl(3)⊕gl(1) commutant of {SU(2)_weak, τ} on the LH-doublet
sector, with eigenvalue ratio 1:(−3) on Sym²(C²):Anti²(C²) sub-decompositions.
This determines the Y direction *up to overall scale* — call it `α ∈ R*`:

```text
Y(Q_L) = +α/3    (3 colors × 2 isospin = 6 LH quark states)
Y(L_L) = −α      (1 singlet × 2 isospin = 2 LH lepton states)
```

(Tracelessness check: 6·(α/3) + 2·(−α) = 2α − 2α = 0. ✓)

### 2.2 Anomaly cancellation determines RH content as functions of α

From cycle 1 / `RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02`,
the three remaining anomaly conditions on the full one-generation content
(with structurally-derived SU(3) representations from cycle 2) take the form

```text
(A1)  3(Y_uR + Y_dR) + Y_eR + Y_νR  =  0          (Tr[Y] = 0)
(A2)  Y_uR + Y_dR  =  2 Y_QL  =  2α/3              (Tr[SU(3)² Y] = 0)
(A3)  3(Y_uR³ + Y_dR³) + Y_eR³ + Y_νR³  =  −16α³/9  (Tr[Y³] = 0)
```

Equation (A3)'s RHS uses LH cubic contribution
`6·(α/3)³ + 2·(−α)³ = 6α³/27 − 2α³ = 2α³/9 − 2α³ = −16α³/9`.

Imposing the neutral-singlet identification `Y_νR = 0` (admitted from
`HYPERCHARGE_IDENTIFICATION_NOTE.md`):

From (A1): `Y_eR = −3(Y_uR + Y_dR) = −3·(2α/3) = −2α`. Uniquely.

Substituting into (A3):
```text
3(Y_uR³ + Y_dR³) + (−2α)³ + 0  =  −16α³/9
3(Y_uR³ + Y_dR³) − 8α³           =  −16α³/9
3(Y_uR³ + Y_dR³)                  =  8α³ − 16α³/9  =  72α³/9 − 16α³/9  =  56α³/9
Y_uR³ + Y_dR³                     =  56α³/27.        (A3′)
```

From (A2): `Y_dR = 2α/3 − Y_uR`. Substituting into (A3′):
```text
Y_uR³ + (2α/3 − Y_uR)³  =  56α³/27
```

Letting `x = Y_uR/α`, this reduces to a single-variable cubic in `x`:
```text
9x² − 6x − 8 = 0    (after standard algebra)
```

Solutions: `x = (6 ± 18)/18 = 4/3` or `x = −2/3`. Therefore
`Y_uR = +4α/3 ∨ −2α/3`, with the partner `Y_dR = −2α/3 ∨ +4α/3` (related
by swap u_R ↔ d_R).

### 2.3 Electric-charge labeling fixes the swap branch

Identifying `u_R` as up-type means `Q(u_R) > 0`, i.e. `Y(u_R)/2 > 0`,
forcing `Y_uR = +4α/3` (and `Y_dR = −2α/3`).

### 2.4 SM-definition convention `Q_e = −1` fixes α = +1

The electron is the SU(2)-singlet with `Q(e_R) = Y(e_R)/2 = −α`.
Setting `Q_e = −1` (the SM-definition convention identifying the elementary
electron charge as `−1` in elementary charge units) gives:

```text
−α = −1   ⟹   α = +1.
```

Substituting `α = +1` into the eigenvalue scheme of §2.1–2.3:

| Field | Y |
|---|---|
| Q_L | +1/3 |
| L_L | −1 |
| u_R | +4/3 |
| d_R | −2/3 |
| e_R | −2 |
| ν_R | 0 |

These are exactly the SM hypercharges (★).

## 3. Closure of LHCM repair item (2)

LHCM's verdict-rationale named three repair items. Together with prior
cycles:

| Repair item | Closure |
|---|---|
| (1) matter assignment | cycle 2, PR #255 (Sym²(3) ↔ Q_L, Anti²(1) ↔ L_L from SU(3) rep content modulo SM-definition labels) |
| (2) U(1)_Y normalization | **THIS NOTE** (overall scale α = +1 from SM convention `Q_e = −1` modulo SM-definition convention) |
| (3) anomaly-complete chiral completion (LH SU(2)²×Y) | PR #253 (open) |
| (3) anomaly-complete chiral completion (R-A SU(3)²×Y) | cycle 1, PR #254 |
| (3) anomaly-complete chiral completion (R-B Y³) | cycle 1, PR #254 |
| (3) anomaly-complete chiral completion (R-C grav²×Y) | cycle 1, PR #254 |

After this PR + PR #255 + PR #254 + PR #253 land, **all 5 named LHCM repair
items are derived as exact identities or representation theorems on the
retained graph-first surface, modulo only SM-definition conventions** (the
labels "quark"/"lepton" and the elementary charge unit `Q_e = −1`).

## 4. What this block does NOT close

- The **derivation of the SM-definition convention itself**. The labels
  "quark"/"lepton" are naming conventions in SM; the elementary charge unit
  `Q_e = −1` is also a convention. Deriving these from physics first
  principles is not possible in physics — they are NAMING conventions.

- The **derivation of the SM photon `Q = T_3 + Y/2` from graph-first
  surface** as an explicit electromagnetic gauge field identification.
  This is a deeper Nature-grade target (electroweak symmetry breaking on
  the graph-first surface, identifying the unbroken U(1)_em).

- LHCM cannot lift to retained status until the audit ledger ratifies
  cycles 1, 2, 3 and PR #253, AND the SM-definition convention is
  explicitly admitted as a non-derivation labeling (allowed under
  Criterion 3 only as narrow non-derivation context).

## 5. Validation

- primary runner:
  [`scripts/frontier_lhcm_y_normalization.py`](../scripts/frontier_lhcm_y_normalization.py)
  — verifies (a) the cubic system in α reduces to the standard SM
  hypercharge solution; (b) the SM-definition convention `Q_e = −1`
  uniquely fixes α = +1; (c) the resulting eigenvalues match the SM
  hypercharge assignments (★) at exact rational `Fraction` precision.

## 6. Authority surface

- `actual_current_surface_status: exact algebraic identity / support theorem`
- `conditional_surface_status: closes LHCM repair item (2) modulo Q_e = −1 SM-definition convention`
- `proposal_allowed: false` — Criterion 3 fails (admitted SM-definition convention is load-bearing for the overall α scale)
- `bare_retained_allowed: false`
- `audit_required_before_effective_retained: yes`

## 7. Cross-references

- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) — parent
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained primitive supplying eigenvalue ratio 1:(−3)
- [`RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md`](RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md) — cycle 1 (PR #254): RH-sector anomaly identities
- [`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md) — cycle 2 (PR #255): matter assignment
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) — sister theorem proving RH uniqueness from anomaly cancellation
- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) — supplies neutral-singlet ν_R identification
- PR #253 (open) — LH SU(2)²×Y anomaly identity
