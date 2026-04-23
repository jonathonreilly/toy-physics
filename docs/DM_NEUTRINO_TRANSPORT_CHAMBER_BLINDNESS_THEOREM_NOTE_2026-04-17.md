# Transport Chamber-Blindness Theorem — eta/eta_obs at Z_3 Doublet-Block Selector Candidates

**Date:** 2026-04-17
**Status:** NARROWER-GAP + STRUCTURAL FACTORISATION + NO-PHYSICS-SELECTOR
**Script:** `scripts/frontier_dm_neutrino_transport_chamber_blindness_theorem.py`
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Scope and discipline

The selector gate, on the integration branch, carries:

- one partial-closure theorem (Schur baseline forces `D = m I_3`),
- three obstruction / cross-check theorems (information-geometric,
 cubic variational, holonomy / Z_3 parity-split).

Collectively these retain FOUR candidate `(delta, q_+)` selector points (or
curves) on the chamber `q_+ >= sqrt(8/3) - delta`:

| Candidate | `(m, delta, q_+)` | Source |
|-----------|-------------------|--------|
| A | `(0.5, sqrt(6)/3, sqrt(6)/3)` | Schur-Q chamber-boundary minimum |
| B | `(0.613372, 0.964443, 1.552431)` | `det(H)` chamber-interior critical point |
| C | `(0.385132, 1.267881, 0.365112)` | the Z_3 parity-split theorem `Tr(H^2)` chamber-boundary minimum |
| D | `delta ~ 0.800, q_+ free` | the Z_3 parity-split theorem `K_12` character-match (a curve) |

This note asks the single sharpest physics question:

> Does the requirement `eta / eta_obs = 1` uniquely pick one of A/B/C/D?

The answer, derivable from the current retained atlas alone, is **no**.

## Theorem (retained-atlas-native): chamber is a level manifold of `eta/eta_obs`

**Statement.** On the live DM-neutrino source-oriented sheet with affine
chart `H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`, the
atlas-native transport value

```
eta / eta_obs
 = (s/n_gamma) * C_sph * d_N * epsilon_1 * kappa_axiom(k_decay) / eta_obs
```

is **constant** as a function of `(delta, q_+)` on the chamber, with the
retained exact value

```
eta / eta_obs = 0.188785929502 .
```

In particular:

- `eta / eta_obs` at candidate A = at candidate B = at candidate C =
 at candidate D = 0.188785929502;
- the level set `{ (delta, q_+) : eta/eta_obs = 1 }` is **empty** on
 the chamber.

**Proof sketch.** The transport chain factorises through the
source-package observables `(gamma, E1, E2, K00, cp1, cp2)`:

```
kappa_axiom = kappa_axiom(k_decay),
k_decay = m_tilde / m_star, m_tilde = K00 Y0^2 V_EW^2 / m1 * 1e9,
epsilon_1 = (Y0^2 / 8 pi) (cp1 f(x23) + cp2 f(x3)) / K00,
cp1 = - 2 gamma E1 / 3, cp2 = 2 gamma E2 / 3.
```

By the retained atlas theorem
`DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM`,
moving `(delta, q_+)` along `T_delta, T_q` on the chamber preserves
each of `gamma, E1, E2, K00, cp1, cp2`. Therefore every factor in the
product above is invariant, and `eta/eta_obs` is constant on the
chamber. The chamber value is the retained radiation-branch transport
result `eta/eta_obs = 0.188785929502`. No chamber point reaches
`eta/eta_obs = 1`. QED.

## Runner-verified content

The runner `scripts/frontier_dm_neutrino_transport_chamber_blindness_theorem.py`
performs the following clean numerical checks and closes with
`PASS = 16, FAIL = 0`:

### Part 1 — Authoritative retained transport value

Pulls `eta/eta_obs` directly from the retained
`dm_leptogenesis_exact_common.exact_package()` and
`kappa_axiom_reference()`, reproducing

```
eta / eta_obs = 0.188785929502, epsilon_1 = 7.178e-08,
kappa_axiom = 0.004829545291.
```

### Part 2 — Source-package bank blindness at each candidate

At each candidate `(m, delta, q_+)` the runner computes
`H(m, delta, q_+)`, lifts to the positive-representative, and extracts
`(gamma, E1, cp1, cp2)` from the carrier normal form. All four
candidates reproduce the retained absolute values

```
|gamma| = 0.5,
|E1| = sqrt(8/3) = 1.632993...,
|cp1| = 0.544331...,
|cp2| = 0.314269... .
```

The CP-sheet branch sign of `gamma` can flip under the
positive-representative lift at some candidates (this is a known atlas
branch, not a new object); `eta/eta_obs` depends only on the absolute
values, so the transport value is unchanged.

### Part 3 — Chamber scan

On a 25x25 grid with `(delta, q_+)` in `[-1.5, 1.8] x [-1.0, 2.0]`
restricted to `q_+ + delta >= sqrt(8/3)`, the runner confirms

```
max | |gamma| - 1/2  | ~ 1.7e-16
max | |cp1| - |cp1|_retained | ~ 1.2e-15
max | |cp2| - |cp2|_retained | ~ 2.6e-15
eta/eta_obs spread on chamber = 0 (to machine precision)
eta/eta_obs never reaches 1 on the chamber.
```

The `E1` normal-form branch value does occasionally flip for `|delta|`
approaching `sqrt(8/3)` (this is a known feature of the
positive-representative lift, not the transport chain). The transport
chain itself does not re-read `E1` from `H`; it uses the atlas-fixed
`E1 = sqrt(8/3)`, so these branch flips have no effect on
`eta/eta_obs`. The runner logs this as a diagnostic.

### Part 4 — Candidate table and verdict

```
Candidate | (delta, q_+)  | eta/eta_obs | closes (==1)?
----------+------------------------------+------------------+---------------
 A | ( 0.816497, 0.816497) | 0.188785929502 | NO
 B | ( 0.964443, 1.552431) | 0.188785929502 | NO
 C | ( 1.267881, 0.365112) | 0.188785929502 | NO
 D | ( 0.799987, 1.000000) | 0.188785929502 | NO
```

### Part 5 — Structural factorisation record

The factorisation of `eta/eta_obs` through the six-tuple
`(gamma, E1, E2, K00, cp1, cp2)` is reproduced in full, matched to the
retained blindness theorem, and the level-manifold consequence is
recorded.

## PMNS-assisted witness is not on the chamber

The PMNS-assisted transport-extremal witness recorded in
[DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16.md)
achieves `eta / eta_obs = 1` on an **off-seed** `5`-real source on the
PMNS-assisted `N_e` route, with parameters

```
(xbar, ybar) = (0.5633, 0.3067),
x_close ~ (0.13, 1.41, 0.15),
y_close ~ (0.29, 0.20, 0.43),
delta_PMNS ~ -2.04 .
```

This parameter space is **not** the `(m, delta, q_+)` affine chart on
the DM-neutrino source-oriented sheet. The witness is therefore not one
of the chamber candidates A, B, C, or D, and there is no `(delta, q_+)`
on the chamber that corresponds to it. The PMNS route is a separate
physics lane.

## Verdict

**SELECTOR GATE NOT CLOSED by the physics-validation test.**

- No chamber candidate achieves `eta/eta_obs = 1`.
- The level set `{ eta/eta_obs = 1 }` is **empty** on the chamber.
- The PMNS-assisted witness is not on the chamber.

**Narrower-gap statement.** The atlas-native transport chain is provably
blind to `(delta, q_+)` on the chamber, so physics alone (via the
currently-retained transport machinery) cannot uniquely pick a chamber
point. Any future selector for `(delta, q_+)` must couple to an
observable that the current bank is **not** blind to. The already-
identified candidates for such an observable are:

1. **Right-sensitive cubic structure.** The Z_3 circulant norm form
 `m^3 - 3 m |w|^2 + 2 Re(w^3)` contains an exact right-sensitive
 cubic term `2 Re(w^3)` with `w = q_+ + i delta`. Any selector that
 reads this cubic (rather than the bank's blind quadratic invariants)
 would escape the blindness theorem.

2. **Independent microscopic consistency condition.** A
 holonomy/transport condition on `H` that is not a function of
 `sym(H)` or `anti(H)` alone (parity-split Theorem 2 obstruction) and does
 not factor through the bank-invariants.

3. **PMNS-assisted lift.** Treat the `(delta, q_+)` chamber as a
 spectator of a larger source-surface problem that includes the PMNS
 phase and off-seed `5`-real source; the witness at `eta/eta_obs = 1`
 lives on that larger surface.

None of 1/2/3 is closed by the present note. The note's unique
contribution is the **negative** structural result that the existing
transport chain is blind to the chamber.

## Position on publication surface

- This note is a **narrower-gap obstruction** (explicit constancy-on-chamber),
 not a closure.
- It is **not** flagship publication-grade on its own.
- Appropriate placement: obstruction row under the DM neutrino
 source-surface / selector family in
 `docs/publication/ci3_z3/DERIVATION_ATLAS.md`.
- This note does not close the DM flagship lane (the integrated closure
  is the downstream PMNS-as-f(H) closure).
- The Schur-baseline partial closure, the three the info-geometric selection obstruction/B/C obstruction
 theorems, and this physics-validation obstruction together delimit
 the selector gate open object as: *a selector that couples to a bank-unblinded
 observable on the chamber*.

## Atlas inputs used

All retained / theorem-grade on the current ``:

- [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)
 — candidate A and Schur `D = m I_3` baseline.
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_PARITY_SPLIT_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_PARITY_SPLIT_THEOREM_NOTE_2026-04-17.md)
 — candidates B, C, D.
- [DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md)
 — authoritative transport chain on the one-flavor radiation branch.
- [DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md)
 — factorisation of `eta/eta_obs` through the source-package.
- [DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md)
 — `kappa_axiom(k_decay)` closed form.
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
 — chamber `q_+ >= sqrt(8/3) - delta`.
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
 — `(delta, q_+)` -> H matrix embedding.
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM_NOTE_2026-04-16.md)
 — invariance of source-package observables under `T_delta, T_q`.
- [DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16.md)
 — off-chamber witness at `eta/eta_obs = 1`.

No new axioms are introduced. The factorisation and blindness chain
are already-retained, and the level-manifold statement is an immediate
consequence.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_transport_chamber_blindness_theorem.py
```

Current expected: `PASS = 16, FAIL = 0`.

## What this file must never say

- that selector is closed;
- that any chamber candidate is physics-selected;
- that `eta/eta_obs = 1` is achievable on the chamber by the current
 transport chain;
- that the PMNS-assisted witness lives on the chamber;
- that the Schur-Q candidate A has been ruled out (it has not; this
 note only states that the current transport chain cannot distinguish
 it from B, C, or D);
- that transport alone is sufficient to close selector (it is not).

If any future revision tightens those boundaries, it must cite a new
source on the live retained/promoted surface. Until then, the safe
read is: **narrower-gap obstruction; the selector gate open; transport chain
chamber-blind**.
