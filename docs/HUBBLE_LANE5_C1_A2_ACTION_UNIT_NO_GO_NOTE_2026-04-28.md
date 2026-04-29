# Lane 5 `(C1)` Gate — A2 g_bare-Action-Unit No-Go

**Date:** 2026-04-28
**Status:** proposed_retained exact negative boundary note on
`frontier/hubble-c1-absolute-scale-gate-20260428`. Cycle 3 of the
(C1) gate loop. Stretch-attempt cycle. Closes the audit's `A2`
attack frame (`g_bare = 1` ⇒ action-unit metrology on `P_A H_cell`).
**Lane:** 5 — Hubble constant `H_0` derivation
**Loop:** `hubble-c1-absolute-scale-gate-20260428`
**Runner:** `scripts/frontier_hubble_c1_a2_action_unit_no_go.py`
**Log:** `outputs/frontier_hubble_c1_a2_action_unit_no_go_2026-04-28.txt`

---

## 0. Context

Cycle 2 of this loop closed the `A1` attack frame negatively
(`HUBBLE_LANE5_C1_A1_GRASSMANN_NO_GO_NOTE_2026-04-28.md`): the bulk
axiom-3 Cl_4(C) action does not preserve `P_A` as a Clifford
submodule. `(G1)` is therefore not closeable by direct restriction.

This Cycle-3 stretch attempt examines `A2`, which targets `(G2)`
action-unit metrology rather than `(G1)` edge-statistics. The
Cycle-1 audit's `A2` mechanism reads:

> retained `g_bare = 1` (axiom 4) plus retained `Cl(3) -> SU(2)`
> gauge structure plus admitted lattice unit `a` fixes the action-
> unit scale on `P_A H_cell` to natural units, breaking the `(S, κ)`
> rescaling degeneracy.

The audit assigned `A2` MEDIUM-HIGH promise contingent on showing
that axiom 4 projects onto the boundary block. This note executes
that check and closes `A2` negatively for an independent structural
reason: `(G2)` is **coupled** to `(G1)` through the only on-package
route to break the `(S, κ)` rescaling degeneracy, the Gauss-flux
source-unit identification (`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`).
Hence the Cycle-2 `A1` no-go propagates to `A2`.

## 1. Setup

The Target 3 phase-unit / edge-statistics boundary note
(`PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md`)
established that the bare Hilbert/unitary-flow surface admits

```text
amplitude(H, t, κ) = ⟨ψ_1| exp(-i H t / κ) |ψ_0⟩
```

on `V = P_A H_cell`, and that this amplitude is

- invariant under `(H, t) -> (λ H, t / λ)`;
- invariant under joint `(S, κ) -> (λ S, λ κ)`, where `S = H t`,
  realised either by `H -> λ H` with `κ -> λ κ` and `t` fixed, or
  symmetrically;
- shifted only by a global U(1) phase under `H -> H + a I`.

The absolute action quantum `κ` is therefore a free parameter of the
finite Hilbert/unitary flow on `V`. Breaking it requires an external
metrology bridge or an internal source-unit identification.

The retained framework provides exactly one on-package source-unit
identification: the Gauss-flux theorem of
`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`.
That theorem reads

```text
c_cell = Tr (ρ_cell P_A) = 4/16 = 1/4,
c_cell = 1/(4 G_λ)  =>  λ = 1, G_Newton,lat = 1.
```

The middle equation reads `c_cell` as the **physical Newton
coefficient** rather than as an arbitrary primitive trace, and the
identification is conditional on the Clifford phase bridge
(`PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`)
which is itself conditional on the metric-compatible
Clifford/Majorana coframe response on `P_A H_cell` — i.e., on
`(G1)` edge-statistics.

## 2. Theorem (no-go)

> **Theorem (A2 no-go).** Let `V = P_A H_cell`, with the standard
> finite Hilbert/unitary-flow structure inherited from `H_cell`, and
> let `g_bare = 1` (axiom 4 of `A_min`) plus `Cl(3) -> SU(2)` plus
> the lattice unit `a` be the only structural inputs available on
> `V`. Then no Hermitian generator `H` and no value of the absolute
> action quantum `κ` is forced on `V` by these inputs alone.
> Equivalently, the `(S, κ)` rescaling degeneracy is preserved.
> Breaking the degeneracy requires the Gauss-flux source-unit
> identification `c_cell = 1/(4 G_λ)`, which is conditional on the
> Clifford phase bridge, which is conditional on `(G1)`. The Cycle-2
> result on `(G1)` therefore propagates to `(G2)`: `A2` cannot close
> `(G2)` on `A_min` alone.

### Proof.

The amplitude on `V` is invariant under joint `(S, κ) -> (λ S, λ
κ)` for every Hermitian `H` on `V`, every state pair, and every
positive `λ`:

```text
exp(-i (λ H) t / (λ κ)) = exp(-i H t / κ).
```

The runner verifies this for random Hermitian `H` on the 4-dim
block, with `λ ∈ {0.5, 1.0, 1.7, 3.3, 11.0}`, max amplitude error
`~10^{-15}`.

The Hermitian generator `H` itself is determined (up to overall
scale) on `V` by the projection of the bulk action density. Setting
`g_bare = 1` is a dimensionless gauge-coupling normalization on the
bulk plaquette/Wilson action; it constrains the **ratio** of
plaquette entries to a fixed reference, not their absolute scale in
units of `κ`. On the projection to `V`, `g_bare = 1` fixes a
particular Hermitian matrix up to overall scale, but does not pick
out an absolute `κ`. The runner verifies this by computing
amplitudes for fixed `H` and varying `κ`; distinct `κ` yields
distinct amplitudes.

The lattice unit `a` is a length scale; combined with a temporal
unit it would carry units of `[a]^{-1} = [\text{action}/\text{time}]`,
but the absolute scale of `a` (in external units) is exactly the
Planck-pin quantity that `(C1)` is trying to derive. Using `a` to
fix `κ` would be circular.

The on-package route to fix `κ` therefore reduces to the source-unit
identification

```text
c_cell = 1/(4 G_λ),    G_Newton,lat = 1,    a/l_P = 1,
```

which the 2026-04-25 source-unit support theorem provides
**conditional** on reading the primitive trace `c_cell = 1/4` as
the physical Newton coefficient. That conditional is the Target 3
Clifford phase bridge, which the
`PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`
shows is conditional on the metric-compatible Clifford/Majorana
coframe response on `P_A H_cell` — i.e., on `(G1)`.

By Cycle 2 (`HUBBLE_LANE5_C1_A1_GRASSMANN_NO_GO_NOTE_2026-04-28.md`),
`(G1)` is not closeable by direct restriction of bulk axiom-3
Cl_4(C) action. The other live `(G1)` candidates are `A4`
(parity-gate) and `A5` (minimal-carrier-axiom audit), neither of
which has been retained. The chain

```text
(G2) source-unit
  -> Gauss-flux identification
  -> Clifford phase bridge
  -> (G1) edge-statistics
  -> (Cycle 2: A1 no-go; A4/A5 still pending)
```

shows that closing `(G2)` on `A_min` alone requires `(G1)` to be
closed first, by some non-`A1` mechanism. `A2` therefore cannot
close `(G2)` independently.

The runner verifies all six load-bearing structural facts:
amplitude invariance under joint `(S, κ)` rescaling and under `(H,
t)` rescaling; finite-trace canonical-commutator obstruction;
`κ`-dependence of amplitude with `H` fixed; `c_cell = 1/4`
primitive trace; conditional Gauss-flux pin `λ = 4 c_cell = 1`. ∎

## 3. Numerical verification

The runner
`scripts/frontier_hubble_c1_a2_action_unit_no_go.py` constructs a
4-dim block with random Hermitian generators (seeded for
reproducibility) and verifies:

1. amplitude well-defined on `V` (bound `|⟨ψ_1|U|ψ_0⟩| ≤ 1`);
2. invariance under `(H, t) -> (λ H, t / λ)` (max error `~10^{-15}`);
3. invariance under `(S, κ) -> (λ S, λ κ)` realised as `H -> λ H,
   κ -> λ κ` (max error `~10^{-15}`);
4. global U(1) phase under `H -> H + a I` (error `~10^{-16}`);
5. `Tr [X, P] = 0` for any finite Hermitian `X`, `P`;
6. `[X, P] = i κ I_4` is impossible on a finite block;
7. amplitudes vary with `κ` when `(H, t)` are fixed;
8. `g_bare = 1` does not constrain absolute `κ`;
9. `c_cell = Tr(ρ_cell P_A) = 1/4`;
10. Gauss-flux identification `λ = 4 c_cell = 1`.

Output: `SUMMARY: PASS=16  FAIL=0`.

The runner does not import any observed value, fitted parameter,
literature constant, or carrier-axiom posit. The verification is
entirely structural on `P_A H_cell` plus the documented chain of
prior conditional theorems.

## 4. What this no-go closes

- `A2` (g_bare=1 + Cl(3)→SU(2) + lattice unit `a` ⇒ action-unit on
  `P_A H_cell`) is **falsified** as an independent closure of `(G2)`
  on `A_min` alone.
- The audit's MEDIUM-HIGH promise rating for `A2` is corrected: `A2`
  cannot close `(G2)` independently because `(G1)` and `(G2)` are
  **coupled** via the Gauss-flux source-unit identification.
- The `A1` Cycle-2 no-go propagates to `A2`: closing `(G2)` requires
  closing `(G1)` first, by some non-`A1` mechanism.

## 5. What this no-go does not close

- `(G1)` itself remains open. `A4` (parity-gate carrier route) and
  `A5` (minimal-carrier-axiom audit fallback) remain available.
- `(G2)` itself is not retired. It remains coupled to `(G1)` via
  the Gauss-flux identification, and would close conditionally if
  `(G1)` were closed by `A4` or `A5`.
- `(C1)` gate itself remains open. No claim of retained `R_Λ`,
  `a/l_P = 1`, or `a^{-1} = M_Pl` is made.
- Per the source-unit theorem, the conditional chain `(G1) ⇒ Clifford
  bridge ⇒ Gauss-flux ⇒ (G2)` remains intact; the present no-go does
  not weaken this chain — it only forbids `A2` from acting as an
  independent attack on `(G2)`.

## 6. Implication for Cycle ordering

Cycle 4 must attack `(G1)` directly via `A4` (parity-gate carrier
route), since `(G2)` is coupled to `(G1)`. The audit's revised plan
is now:

- **Cycle 4:** `A4` parity-gate stretch attempt on `(G1)`.
- **Cycle 5:** `A5` minimal-carrier-axiom audit if `A4` fails.
- **Cycles 6+:** stuck fan-out, review-loop, possible pivot (per
  prior session's identified continuations: `F3` DM-cluster on Lane
  4F, `M1`/`M5-c` on Lane 6).

There is no `A2`-only closure pathway and no `A1`+`A2` joint
closure. The Cycle-1 audit's "highest-leverage A1+A2=A3" plan is
fully retired by Cycles 2 and 3.

## 7. Cross-references

- Cycle 1 audit: `HUBBLE_LANE5_C1_GATE_RESIDUAL_PREMISE_ATTACK_AUDIT_NOTE_2026-04-28.md`.
- Cycle 2 (`A1` no-go): `HUBBLE_LANE5_C1_A1_GRASSMANN_NO_GO_NOTE_2026-04-28.md`.
- 2026-04-26 `(C1)` gate single-residual-premise audit:
  `HUBBLE_LANE5_PLANCK_C1_GATE_AUDIT_NOTE_2026-04-26.md`.
- Target 3 phase-unit / edge-statistics boundary:
  `PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md`.
- Source-unit normalization support theorem:
  `PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`.
- Clifford phase bridge:
  `PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`.
- `A_min` foundation: `MINIMAL_AXIOMS_2026-04-11.md`.
- `g_bare = 1` retained authority:
  `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`.
- `A4` parity-gate anchor:
  `AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md`.
- Loop pack:
  `.claude/science/physics-loops/hubble-c1-absolute-scale-gate-20260428/`.

## 8. Boundary

This is a **no-go** stretch-attempt note. It closes the `A2` attack
frame negatively. It does not retain any premise, does not close
`(G2)` or `(C1)`, and does not promote any conditional theorem. It
produces a sharper structural obstruction: `(G1)` and `(G2)` are
coupled via the Gauss-flux source-unit identification, so closing
`(G2)` requires `(G1)` first by some non-`A1` mechanism. Cycle 4
must therefore attack `(G1)` via `A4`.

The result counts as a stretch attempt with a named structural
obstruction per the Deep Work Rules no-churn exception: an honest
first-principles attempt with a sharp coupled-obstruction is valid
progress even without closure.
