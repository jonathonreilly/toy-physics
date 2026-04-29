# Lane 5 `(C1)` Gate — A4 Parity-Gate-from-A_min No-Go

**Date:** 2026-04-28
**Status:** proposed_retained exact negative boundary note on
`frontier/hubble-c1-absolute-scale-gate-20260428`. Cycle 4 of the
(C1) gate loop. Stretch-attempt cycle. Closes the audit's `A4`
attack frame (parity-gate carrier ⇒ CAR semantics on `P_A H_cell`).
**Lane:** 5 — Hubble constant `H_0` derivation
**Loop:** `hubble-c1-absolute-scale-gate-20260428`
**Runner:** `scripts/frontier_hubble_c1_a4_parity_gate_no_go.py`
**Log:** `outputs/frontier_hubble_c1_a4_parity_gate_no_go_2026-04-28.txt`

---

## 0. Context

Cycles 2 and 3 closed `A1` and `A2` negatively
(`HUBBLE_LANE5_C1_A1_GRASSMANN_NO_GO_NOTE_2026-04-28.md`,
`HUBBLE_LANE5_C1_A2_ACTION_UNIT_NO_GO_NOTE_2026-04-28.md`). With the
`A1`+`A2` joint pathway retired, `A4` (parity-gate carrier route) is
the primary remaining direct-derivation candidate for `(G1)`.

The Cycle-1 audit's `A4` mechanism reads:

> the retained
> `AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md`
> establishes a primitive parity-gate carrier on the rank-four
> block. Parity-gate structure may force CAR (vs. non-CAR) semantics
> without needing to invoke the bulk Grassmann partition.
> ... parity-gate structure on `P_A H_cell` + Clifford module
> identification ⟹ CAR semantics (alternative to A1).

This note executes that check and closes `A4` negatively.

## 1. Setup

The retained primitive parity-gate carrier theorem
(`AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md`)
proves the Widom coefficient `c_Widom = 3/12 = 1/4` from five
explicit assumptions, the first of which is:

> 1. the primitive rank-four boundary block `P_A H_cell` **is** the
>    edge Fock space of two complex Gaussian horizon orbitals;

This assumption is exactly the `(G1)` edge-statistics principle on
`P_A H_cell`. The theorem therefore takes `(G1)` as input rather
than producing it as output. The remaining residual Z_2 half-zone
gate (Assumption 3 of the theorem) is a lattice-momentum-zone Z_2
involution `τ(q) = q + π` that fixes the self-dual threshold
`Δ_perp = 1`; this involution has eigenspaces `dim(+1) = dim(-1) =
2` on the rank-four block, hence half-zone measure 1/2.

The two structural questions for `A4` are therefore:

(i) does the parity-gate carrier theorem itself derive `(G1)`?

(ii) does the bare parity-gate Z_2 structure on the rank-four block
distinguish CAR from non-CAR semantics?

## 2. Theorem (no-go)

> **Theorem (A4 no-go).** Neither the primitive parity-gate carrier
> theorem nor the bare parity-gate Z_2 structure on `P_A H_cell`
> supplies a derivation of CAR semantics on `P_A H_cell`. Hence
> `A4` cannot close `(G1)` on `A_min` alone.

### Proof.

**(i) The carrier theorem assumes CAR as input.** Assumption 1 of
the parity-gate carrier theorem is `P_A H_cell ≅ F(C^2)`, exactly
the `(G1)` edge-statistics principle. The theorem's output `c_Widom
= 1/4` derives from the average Fermi-surface crossing count `⟨N_x⟩
= 3` for the two-orbital free-fermion dispersion. This crossing
count uses Gaussian fermion-orbital structure (creation/annihilation
operators on `F(C^2)`) and cannot be computed from a bare `Z_2`
parity grading alone. The theorem therefore cannot derive `(G1)` —
it presupposes it.

**(ii) The bare parity Z_2 structure is preserved by all three
rank-four semantics.** A bare Z_2 parity gate on the 4-dim block is
a Z_2 involution `P` with `P^2 = I` and a 2+2 eigenvalue signature.
The runner verifies that all three structurally distinct rank-four
semantics admit such an involution:

- **CAR** on `F(C^2)`: parity `(-1)^N` has eigenvalues `(+1, +1, -1,
  -1)` on `(|0⟩, |11⟩, |10⟩, |01⟩)`. Signature `(2, 2)`.
- **Two-qubit commuting spin** on `(C^2)^{⊗2}`: parity `Z ⊗ Z` has
  eigenvalues `(+1, -1, -1, +1)` on `(|00⟩, |01⟩, |10⟩, |11⟩)`.
  Signature `(2, 2)`.
- **Ququart clock-shift** on `C^4`: parity `Z_4^2 = \text{diag}(1, -1,
  1, -1)`. Signature `(2, 2)`.

All three give the same self-dual half-zone measure 1/2. None of the
three is distinguished from the others by the parity Z_2 alone.

The CAR-distinguishing structural feature — anticommuting Hermitian
generators `{γ_a, γ_b} = 2δ_{ab} I` — is not a Z_2 statement. The
runner verifies that the two-qubit `X ⊗ I, I ⊗ X` operators
**commute** rather than anticommute, despite respecting the same
`Z ⊗ Z` parity Z_2.

**(iii) The lattice involution τ is a Z_2 statement, not a CAR
statement.** The retained
`AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md`
uses the half-period involution `τ(q) = q + π · (1, …, 1)` to fix
the self-dual threshold `Δ_perp = 1` and the half-zone measure
`μ = 1/2`. This is a discrete lattice-momentum Z_2 symmetry of the
nearest-neighbor transverse Laplacian symbol `Δ_perp(q) = 1 - (1/n)
Σ_j cos(q_j)`; the runner verifies the symmetry exactly via
involution-partition counting on a 64^n grid (PASS for n ∈ {1, 2}).
The involution is a property of the lattice symbol, not of the
fermion semantics on the rank-four block. It is preserved by every
fermion realization on `P_A H_cell`, including the non-CAR ones.

Therefore neither (i) the parity-gate carrier theorem (which
presupposes `(G1)`) nor (ii) the bare parity-gate Z_2 structure
(which is preserved by all rank-four semantics) supplies a
derivation of CAR semantics on `P_A H_cell`. `A4` cannot close
`(G1)` on `A_min` alone. ∎

## 3. Numerical verification

The runner `scripts/frontier_hubble_c1_a4_parity_gate_no_go.py`
constructs explicit realizations of the three rank-four semantics
and verifies:

1. parity-gate carrier theorem assumes CAR (Assumption 1 cited);
2. CAR parity `(-1)^N`, two-qubit `Z ⊗ Z`, and ququart `Z_4^2` all
   have 2+2 eigenvalue signature on the rank-four block;
3. CAR has anticommuting Hermitian Majorana generators (`||{γ_0,
   γ_1}|| ≈ 0`); two-qubit `X ⊗ I, I ⊗ X` instead commute (`||[X
   ⊗ I, I ⊗ X]|| ≈ 0`) and have nonzero anticommutator (`= 4`);
4. self-dual half-zone measure 1/2 by exact `τ`-involution
   partitioning on a 64^n grid (n=1: low=high=31, boundary=2; n=2:
   low=high=1985, boundary=126).

Output: `SUMMARY: PASS=19  FAIL=0`.

The runner does not import any observed value, fitted parameter,
literature constant, or carrier-axiom posit. The verification is
entirely structural.

## 4. What this no-go closes

- `A4` (parity-gate ⇒ CAR semantics on `P_A H_cell`) is
  structurally falsified.
- The parity-gate carrier theorem is now exposed as conditional on
  `(G1)`, not a derivation of `(G1)`.
- All three direct-derivation candidates `A1`, `A2`, `A4` for
  `(G1)`/`(G2)` are now closed negatively.

## 5. What this no-go does not close

- `(G1)` itself remains open. `A5` (minimal-carrier-axiom audit
  fallback) is now the only remaining live attack frame.
- `(G2)` remains coupled to `(G1)`.
- `(C1)` gate as a whole remains open.

## 6. Implication for Cycle ordering

With `A1`, `A2`, and `A4` all closed negatively, the audit's revised
plan reduces to:

- **Cycle 5 (next):** `A5` minimal-carrier-axiom audit. Identify
  the minimal carrier axiom that would close `(G1)` without
  violating the framework's no-fitted-parameter posture, and audit
  its compatibility with the existing retained surface.
- **Cycle 6:** stuck fan-out across `(G1)` attack space (3-5
  orthogonal premises) per Deep Work Rules, since the audit's
  primary attack frames are now exhausted.
- **Cycles 7+:** review-loop pressure on the no-go cluster, possible
  pivot to `F3` DM-cluster on Lane 4F or `M1`/`M5-c` on Lane 6.

## 7. Cross-references

- Cycle 1 audit: `HUBBLE_LANE5_C1_GATE_RESIDUAL_PREMISE_ATTACK_AUDIT_NOTE_2026-04-28.md`.
- Cycle 2 (`A1` no-go): `HUBBLE_LANE5_C1_A1_GRASSMANN_NO_GO_NOTE_2026-04-28.md`.
- Cycle 3 (`A2` no-go): `HUBBLE_LANE5_C1_A2_ACTION_UNIT_NO_GO_NOTE_2026-04-28.md`.
- Primitive parity-gate carrier theorem (the `A4` anchor):
  `AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md`.
- Native CAR semantics tightening (intrinsic 4-dim Cl_4(C) action):
  `AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md`.
- Target 3 phase-unit / edge-statistics boundary:
  `PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md`.
- 2026-04-26 `(C1)` gate single-residual-premise audit:
  `HUBBLE_LANE5_PLANCK_C1_GATE_AUDIT_NOTE_2026-04-26.md`.
- Loop pack:
  `.claude/science/physics-loops/hubble-c1-absolute-scale-gate-20260428/`.

## 8. Boundary

This is a **no-go** stretch-attempt note. It closes the `A4` attack
frame negatively. It does not retain any premise, does not close
`(G1)` or `(C1)`, and does not promote any conditional theorem. It
produces a clean structural obstruction: the parity-gate carrier
theorem assumes CAR as input (Assumption 1), and the bare parity-gate
Z_2 structure is preserved by all rank-four semantics (CAR, two-qubit
spin, ququart). Cycle 5 must therefore turn to `A5` (minimal-carrier-
axiom audit fallback).

The result counts as a stretch attempt with a named structural
obstruction per the Deep Work Rules no-churn exception.
