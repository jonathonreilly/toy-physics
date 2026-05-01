# Lane 5 `(C1)` Gate — A1 Grassmann-from-axiom-3 No-Go

**Date:** 2026-04-28
**Status:** proposed_no_go exact negative boundary note on
`frontier/hubble-c1-absolute-scale-gate-20260428`. Cycle 2 of the
(C1) gate loop. Stretch-attempt cycle. Closes the audit's highest-
rated single-cycle attack frame `A1` (Grassmann-from-axiom-3 ⇒ CAR
on `P_A H_cell`).
**Lane:** 5 — Hubble constant `H_0` derivation
**Loop:** `hubble-c1-absolute-scale-gate-20260428`
**Runner:** `scripts/frontier_hubble_c1_a1_grassmann_no_go.py`
**Log:** `outputs/frontier_hubble_c1_a1_grassmann_no_go_2026-04-28.txt`

---

## 0. Context

Cycle 1 of this loop landed
`docs/HUBBLE_LANE5_C1_GATE_RESIDUAL_PREMISE_ATTACK_AUDIT_NOTE_2026-04-28.md`,
which enumerated six candidate attack frames `A1`–`A6` on the coupled
`(G1+G2)` residual premise of the `(C1)` absolute-scale gate. The
audit named `A1` as the highest-promise single-cycle attempt and
explicitly flagged the load-bearing question as:

> ... need to verify the boundary projection `P_A` preserves the
> anticommutation structure (i.e., `P_A` is a Clifford-module
> morphism, not an arbitrary projection).

This note executes that verification and closes `A1` negatively.

## 1. Setup

The primitive event cell is the four-axis Boolean coframe register

```text
H_cell = ⊗_{a ∈ E} C^2_a ≅ C^16,    E = {t, x, y, z}.
```

The active primitive boundary block is the Hamming-weight-one packet

```text
P_A = P_1 = Σ_{a ∈ E} P_{ {a} },    rank P_A = 4.
```

The minimal accepted axiom stack `A_min`
(`MINIMAL_AXIOMS_2026-04-11.md`) supplies, as axiom 3, the **finite
local Grassmann/staggered-Dirac partition** on the spatial substrate
`Z^3`. The audit's `A1` attack frame proposes that this bulk axiom
forces Clifford-Majorana / CAR semantics on `P_A H_cell`.

The standard, structurally natural bulk-axiom-3 realisations on
`H_cell` are:

- **Boolean Jordan-Wigner.** Read the four coframe slots `E = {t, x,
  y, z}` as Jordan-Wigner sites on `H_cell ≅ (C^2)^{⊗ 4}` and define

  ```text
  γ_a = Z^{⊗ a} ⊗ X ⊗ I^{⊗ (4-a-1)}.
  ```

- **Staggered-Dirac CAR.** Read `H_cell ≅ F(C^4)` as the four-mode CAR
  Fock space with annihilators `c_a = Z^{⊗ a} ⊗ σ_- ⊗ I^{⊗ (4-a-1)}`
  and Hermitian Majoranas `γ_a = c_a + c_a^†`.

Both realisations satisfy the Cl_4(C) relations on `H_cell`:

```text
{γ_a, γ_b} = 2 δ_{ab} I_{16}.
```

These are the two structurally natural Cl_4(C) actions on `H_cell`
that any direct `A1`-style derivation could invoke as the bulk
Grassmann/staggered-Dirac response.

## 2. Theorem (no-go)

> **Theorem (A1 no-go).** Let `H_cell ≅ C^{16}` carry the natural
> bulk-axiom-3 Cl_4(C) action — either Boolean Jordan-Wigner or
> staggered-Dirac CAR. Then no element of the bulk Cl_4(C) action,
> nor any Hermitian linear combination of compressed generators
> `P_A γ_a P_A`, supplies four Hermitian anticommuting Cl_4(C)
> generators on `P_A H_cell`. In particular, `P_A` is **not** a
> Clifford-module morphism for any bulk-axiom-3 Cl_4(C) action on
> `H_cell`. Consequently `(G1)` (the native edge-statistics principle
> on `P_A H_cell`) is not closed by axiom 3 alone.

### Proof.

The bulk Majoranas in either realisation are linear (degree-one) in
the Boolean Jordan-Wigner / CAR ladder and therefore shift the
Hamming-weight grading on `H_cell` by exactly `±1`:

```text
γ_a P_w ⊆ P_{w-1} ⊕ P_{w+1},    w = 0, 1, 2, 3, 4.
```

Hence `γ_a P_A = γ_a P_1 ⊆ P_0 ⊕ P_2`, which is orthogonal to
`P_A = P_1`. Compression to `P_A` therefore vanishes:

```text
P_A γ_a P_A = 0,    a ∈ E.
```

So `γ_a` does not preserve `P_A H_cell` as a Clifford submodule,
and compressed generators give no Hermitian anticommuting element.

The only remaining bulk-axiom-3 candidates for Cl_4(C) generators on
`P_A H_cell` are bilinear products `γ_a γ_b` (`a ≠ b`) and their
Hermitised partners `i γ_a γ_b`. Bilinears preserve fermion-number
parity and therefore admit nonzero compressions onto `P_A`. There are
six independent bilinears `γ_a γ_b` for `a < b`, and their
compressions `i P_A γ_a γ_b P_A` are nonzero on `P_A H_cell`.

However, the bilinear bulk algebra closes on the Lie algebra `so(4)`
under commutators, **not** on a Clifford algebra under
anticommutators. Explicitly,

```text
{γ_a γ_b, γ_c γ_d} ≠ 2 (δ_{ab,cd}-pairing) · I,
```

so no four-element subset of the six compressed bilinears `i P_A γ_a
γ_b P_A` satisfies the Cl_4(C) relations `{G_i, G_j} = 2 δ_{ij}
P_A`. The runner verifies this by exhaustive check of all
`C(6,4) = 15` four-bilinear subsets: every subset fails.

Thus no element of the bulk-axiom-3 Cl_4(C) action — neither linear
generators nor compressed bilinears — can supply four anticommuting
Cl_4(C) generators on `P_A H_cell`. The bulk Grassmann anticommutation
structure does not descend to a Clifford-Majorana algebra on the
rank-four primitive boundary block. ∎

## 3. Numerical verification

The runner
`scripts/frontier_hubble_c1_a1_grassmann_no_go.py` constructs both
Boolean Jordan-Wigner and staggered-Dirac realisations explicitly,
verifies the Cl_4(C) relations on `H_cell`, computes the Hamming-
weight shift of each generator, and exhausts the six-bilinear
compressions. Output:

```text
SUMMARY: PASS=29  FAIL=0
```

The runner does not import any observed value, fitted parameter,
literature constant, or carrier-axiom posit. The verification is
entirely structural on the Boolean coframe register.

## 4. What this no-go closes

This Cycle-2 stretch attempt closes the audit's highest-rated single-
cycle attack frame on the `(G1)` edge-statistics principle:

- `A1` (Grassmann-from-axiom-3 ⇒ CAR on `P_A H_cell`) is **falsified**
  as a direct restriction or compression of bulk axiom-3 Cl_4(C)
  action.
- The audit's load-bearing question — "`P_A` is a Clifford-module
  morphism, not an arbitrary projection" — answers **negatively**.

It also re-narrows the residual structural obligation on `(G1)`. The
Cl_4(C) action on `P_A H_cell` that the
`AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md` two-mode
CAR construction uses is **internal** to the rank-four block: the
generators in that note act on a 4-dim space `≅ M_4(C)`-module,
unrelated to the bulk 16-dim Hilbert action via projection. Any
direct derivation of `(G1)` from `A_min` therefore cannot proceed via
projection of bulk Grassmann anticommutation; it requires a separate
structural mechanism that places a Clifford-Majorana algebra on the
4-dim `P_A H_cell` block intrinsically.

## 5. What this no-go does not close

- `(G1)` itself remains open. The no-go closes the `A1` mechanism but
  not the residual premise.
- `(G2)` (action-unit metrology) is independent and untouched by this
  result. Cycle 3 (`A2` stretch attempt) still applies.
- `A4` (primitive parity-gate carrier route) is untouched and remains
  the highest-promise remaining direct-derivation candidate. Per
  `AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md`,
  parity-gate structure is intrinsic to `P_A H_cell` and may force
  CAR semantics independently of bulk-axiom-3 projection.
- `A5` (minimal-carrier-axiom audit fallback) is now strongly
  indicated as the honest path forward if `A2` and `A4` also fail.
- `(C1)` gate itself remains open. No claim of retained `R_Λ`,
  `a/l_P = 1`, or `a^{-1} = M_Pl` is made.

## 6. Implication for Cycle ordering

The Cycle-1 audit proposed phase ordering `A1` → `A2` → `A3` (where
`A3` consolidates `A1`+`A2`). With `A1` falsified, this ordering must
be revised:

- **Cycle 3** (next): `A2` stretch attempt. `A2` targets `(G2)`
  action-unit metrology, which is structurally orthogonal to `(G1)`
  and not affected by the present no-go.
- **Cycle 4** (revised): `A4` parity-gate alternative attack on
  `(G1)`, replacing the now-impossible `A3` consolidation.
- **Cycle 5** (revised): `A5` minimal-carrier-axiom audit if `A2`
  and/or `A4` also fail to close.

The `A3` consolidation cycle is removed from the plan. There is no
combined `A1`+`A2` closure pathway because `A1` is closed negatively.

## 7. Cross-references

- Cycle-1 audit (anchor for `A1`–`A6`):
  `docs/HUBBLE_LANE5_C1_GATE_RESIDUAL_PREMISE_ATTACK_AUDIT_NOTE_2026-04-28.md`.
- 2026-04-26 `(C1)` gate single-residual-premise audit:
  `docs/HUBBLE_LANE5_PLANCK_C1_GATE_AUDIT_NOTE_2026-04-26.md`.
- Two-mode CAR tightening (intrinsic 4-dim Cl_4(C) action):
  `docs/AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md`.
- `A4` parity-gate anchor:
  `docs/AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md`.
- `A_min` foundation:
  `docs/MINIMAL_AXIOMS_2026-04-11.md`.
- Loop pack:
  `.claude/science/physics-loops/hubble-c1-absolute-scale-gate-20260428/`.

## 8. Boundary

This is a **no-go** stretch-attempt note. It closes the `A1` attack
frame negatively. It does not retain any premise, does not close
`(G1)` or `(C1)`, and does not promote any conditional theorem to
retained. It produces a sharper structural obstruction (no bulk
axiom-3 Cl_4(C) action descends to `P_A H_cell` as a Clifford
submodule) and revises the loop's phase ordering to drop the now-
impossible `A3` consolidation cycle.

The result counts as a stretch attempt with a named structural
obstruction per the Deep Work Rules no-churn exception: an honest
first-principles attempt with named obstructions is valid progress
even without closure.
