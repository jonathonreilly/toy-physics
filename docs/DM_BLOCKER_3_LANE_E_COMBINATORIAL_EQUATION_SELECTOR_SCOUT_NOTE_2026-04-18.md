# DM Blocker 3 Lane E — Combinatorial / Equation Selector Attack (Scout Note)

**Date:** 2026-04-18
**Status:** SCOUT / OBSTRUCTION. Lane E drops assumption A3.1 (selection is
variational) from the Case 3 Microscopic Polynomial Impossibility Theorem and
probes whether a non-variational axiom-native algebraic equation can pin
`(delta_*, q_+*)`.
**Verdict:** DEAD (with a residual PARTIAL flag on the Z_3 reality equation).
**Runner:** `scripts/frontier_dm_blocker_3_lane_e_combinatorial_equation_selector.py`

## Unit system and framework

- Framework axiom: `Cl(3)` on `Z^3`, single retained axiom.
- Retained surface: `H_hw=1 ≅ C^3` with the `C_3[111]` cyclic generator.
- Active affine chart:
 `H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`,
 with `gamma = 1/2`, `E_1 = sqrt(8/3)`, `E_2 = sqrt(8)/3`.
- All scalars natural-unit dimensionless on the active chart.
- Observational content is FLAGGED SEPARATELY (see §Observational).

## Statement of the lane

Case 3 impossibility (see
`DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md`)
proved no retained local polynomial functional of `H` on `H_hw=1` has an
extremum at `(delta_*, q_+*)` that is gauge-invariant across all retained
candidates. The proof relies on (A3.1) the assumption that selection is via
an extremum `∂f/∂x = 0`.

Lane E drops (A3.1) and asks: can an **algebraic equation** of the form
`g(delta, q_+, m) = 0`, built from axiom-native retained content but not
derivable as `∂f/∂(delta, q_+) = 0` for any `f`, pin `(delta_*, q_+*)`?

## Derivation (every step shown)

### Step 1. Retained axiom-native scalar content

On `H_hw=1`, the retained operator algebra is `M_3(C)` (three-generation
observable theorem note). Retained algebra-generators:
`{I, C_3, C_3^2, P_1, P_2, P_3}` (sector projectors + Z_3 cycle).
`T_x, T_y, T_z` translations have images in the projector algebra.

The axiom-native REAL scalars of `H` are:
- Trace powers `Tr(H^k)` for `k = 1, 2, 3, ...`;
- `Re Tr(H^k C_3)` and `Im Tr(H^k C_3)` for `k = 1, 2, 3, ...`;
- Matrix entries `P_i H P_j` and their absolute values;
- `Z_3`-projected scalars `Tr(H^k (I + C_3 + C_3^2)/3) = v^T H^k v / 3`,
 where `v = (1,1,1)^T` is the Z_3-singlet vector.

### Step 2. Exact symbolic computation of δ-parity

Let `H_src = m T_m + delta T_delta + q_+ T_q` and `H_full = H_base + H_src`.

- Source-only `Tr(H_src^k)`: symbolic computation verifies these are EVEN in
 `delta` for `k = 1, 2, 3, 4`. (Consistent with impossibility Theorem 3.)

- Full `Tr(H^k)`: symbolic computation shows `Tr(H^2)` has δ-odd term
 `-16 sqrt(6) delta / 3`; `Tr(H^3)` has δ-odd term
 `16 sqrt(6) delta q_+ - 32 sqrt(3) delta/3 - 3 delta/4`;
 `det(H)` has δ-odd term
 `8 sqrt(6) delta m/3 + 16 sqrt(6) delta q_+/3 - 32 sqrt(3) delta/9 - delta/4`.

So **the full H (with H_base) has δ-odd retained scalars**. The
impossibility-theorem δ-evenness claim (Thm 3) is about the SOURCE-ONLY
chart; Thm 4 inherits a subtle baseline restriction and does not directly
cover H_base-inclusive δ-odd pieces.

This is the first real crack visible to Lane E.

### Step 3. δ-odd equations (the `f(δ) − f(−δ) = 0` attack)

Isolate `[det H]_odd / delta`:
```
f_1 := 8 sqrt(6) m/3 + 16 sqrt(6) q_+/3 - 32 sqrt(3)/9 - 1/4.
```
Linear in `(m, q_+)`. Zero-locus is a line in `(m, q_+)`-plane.

Isolate `[Tr H^3]_odd / delta`:
```
f_2 := 16 sqrt(6) q_+ - 32 sqrt(3)/3 - 3/4.
```
Linear in `q_+` only, no `m` or `delta`. Zero-locus:
`q_+ = (32 sqrt(3)/3 + 3/4) / (16 sqrt(6)) ≈ 0.392`.

Isolate `[v^T H^3 v]_odd / delta`:
```
g_3 := -32 sqrt(3)/9 - 3/4.
```
**NON-ZERO CONSTANT.** Cannot be set to zero. Structurally, this means
`v^T H^3 v` has a δ-odd piece LINEAR in δ with fixed nonzero slope, which
does not enable a δ-parity equation.

**Verdict on δ-odd class:** candidate zero-loci do NOT pass through the
Schur-Q candidate pin `(sqrt(6)/3, sqrt(6)/3)` or any other retained
candidate, and they DO NOT respect the physical chamber `q_+ ≥ E_1 − δ`.

### Step 4. Z_3-character reality (Im Tr(H^k C_3) = 0) equations

Compute symbolically (full H, including H_base):
```
Im Tr(H C_3) = 1/2 (IDENTITY, axiom-native γ value; not a constraint).
Im Tr(H^2 C_3) = -q_+ - sqrt(6)/3 + sqrt(2)/3.
Im Tr(H^3 C_3) = 3 delta^2/2 - 4 sqrt(6) delta/3 + m^2/2 - sqrt(6) m/3
                - sqrt(2) m/3 + 3 q_+^2/2 - 2 sqrt(2) q_+/3 + 233/72.
Im Tr(H^4 C_3) = ... (degree 2 in delta, m, q_+; mixes all three).
```

The equation `Im Tr(H^2 C_3) = 0` is axiom-native: it states that the Z_3
projected trace moment is real, i.e. `Tr(H^2 C_3) = Tr(H^2 C_3^{-1})`. This
is a **discrete-symmetry reality condition**, not a variational extremum.

Solving `Im Tr(H^2 C_3) = 0`:
```
q_+ = (sqrt(2) - sqrt(6))/3 ≈ -0.345.
```

This is OUTSIDE the physical chamber `q_+ ≥ E_1 − δ ≥ 0` (since `delta ≤ E_1`
and `E_1 > 0`).

So the axiom-native Z_3-reality equation PINS `q_+` to a value that
CONTRADICTS the chamber-boundary theorem. This is an **obstruction**, not
a closure. The axiom-level equation exists; it just doesn't land in the
chamber.

Adding `Im Tr(H^3 C_3) = 0` to the system gives three equations in three
variables `(delta, q_+, m)`. Substituting `q_+ = (sqrt(2) - sqrt(6))/3`
into `Im Tr(H^3 C_3) = 0` gives a quadratic in `delta` with **NEGATIVE
DISCRIMINANT** in m-independent form, so **no real joint solution
exists**.

### Step 5. Commutator equations (`[H, X] = 0` attack)

Computed symbolically for `X ∈ {T_m, T_delta, T_q, C_3}`:
```
Tr([H, T_q]^2) = -347/9 (CONSTANT, negative. No real zero.)
det([H, T_q]) = 0 (IDENTITY. Not a constraint.)
Tr([H, T_m]^2) = -24 delta^2 + 64 sqrt(6) delta/3 - 131/3.
 Discriminant = -4384/3 < 0. No real zero.
det([H, T_m]) = 0. (IDENTITY.)
Tr([H, T_delta]^2) = -24 m^2 + 64 sqrt(2) m/3 - 73/3.
 Discriminant = -12832/9 < 0. No real zero.
det([H, T_delta]) = pure imaginary in m. Not a real constraint.
det([H, C_3]) = -485 delta/36 + 3 m/4 + 32 sqrt(3) m/9 - sqrt(2)/3
              + 119 sqrt(6)/27.
 Linear in (delta, m); no q_+ dependence; one equation in two vars.
```

**Verdict on commutator class:** either the equation is an identity (not a
constraint), or has negative discriminant (no real solution in chamber),
or provides insufficient dimensional constraint.

### Step 6. Z_3 doublet-block matrix-element equations

On the Z_3 basis, the kernel `K_Z3 = U_Z3^† H U_Z3` has doublet block
entries:
```
K_11 = -q_+ + 2 sqrt(2)/9 - 1/(2 sqrt(3)).
K_22 = -q_+ + 2 sqrt(2)/9 + 1/(2 sqrt(3)).
K_12 = (m - 4 sqrt(2)/9) + i (sqrt(3) delta - 4 sqrt(2)/3).
```

Retained axiom-native SCALAR equations on this block:
- `K_11 − K_22 = −sqrt(3)/3`. CONSTANT IDENTITY. Not a constraint.
- `Tr K_doublet = K_11 + K_22 = -2 q_+ + 4 sqrt(2)/9`. Linear in q_+;
 setting equal to a specific axiom-native constant pins q_+.
- `K_11 K_22 = q_+^2 - 4 sqrt(2) q_+/9 + 5/324`. Purely quadratic in q_+.
- `|Im K_12|^2 = 3 delta^2 - 8 sqrt(6) delta/3 + 32/9`. Purely quadratic
 in delta. Takes value `2/9` at Schur-Q pin `delta = sqrt(6)/3`.
- `Re K_12 = m - 4 sqrt(2)/9`. Purely linear in m.

The Z_3 block decomposes into three axes: `q_+` is the trace axis,
`m` is the Re K_12 axis, `delta` is the Im K_12 axis. These are
INDEPENDENT axiom-native axes.

**Pin check.** The two candidate equations
```
(A) q_+ + delta = E_1 (chamber boundary, upstream theorem)
(B) delta^2 + q_+^2 = E_1^2/2
```
jointly give `delta = q_+ = E_1/2 = sqrt(6)/3`, matching Schur-Q. But
equation (B) rewritten as `Tr(H_src^2)|_{m=0} = 3 E_1^2` is the
`Tr(H^2)` variational chamber-boundary MINIMUM (impossibility note Thm 6,
retained candidate (b)). So **(B) reduces to A3.1**, the assumption we
dropped. Hence not a new non-variational equation.

### Step 7. Quantization / integrality check

Schur-Q pin `(sqrt(6)/3, sqrt(6)/3)` has:
- `Tr(H)|_{Schur-Q, m free} = m`. Trivial.
- `Tr(H^2)|_{Schur-Q, m=0} = 8 + 233/18 − 8/3 = ...` (complicated);
 not a simple axiom-native integer.
- `det(H)|_{Schur-Q, m=0} = 32 sqrt(2)/9 - sqrt(2) · (16/9 - ...)`; not
 simple.
- `Tr K_doublet|_{Schur-Q} = -2 sqrt(6)/3 + 4 sqrt(2)/9`; not simple.

No retained scalar evaluates to an axiom-native clean constant (0, 1, γ,
E_1, E_1^2, E_2, etc.) at Schur-Q pin, other than those already covered
by A3.1.

### Step 8. Lattice loop / plaquette identities

The retained atlas has lattice translations `T_x, T_y, T_z` acting as
`diag(-1, +1, +1)`, `diag(+1, -1, +1)`, `diag(+1, +1, -1)` on `H_hw=1`.
Plaquette loops `T_x T_y T_x^{-1} T_y^{-1} = I` are automatic (translations
commute). No axiom-native nontrivial loop equation descends to the active
chart.

### Step 9. 3+1D temporal Ward identity

The retained atlas is purely spatial `Z^3`. A 3+1D temporal lift is not in
the retained axiom. Speculative.

## Robustness checks (mandated by lane spec)

### Check 1 — Lattice-is-physical

All candidate equations probed (Im Tr, commutator, doublet-block matrix
entries) are MOMENTUM-SPACE constructs on the reduced `H_hw=1` sector,
not spatial-lattice loop/plaquette identities. No candidate passes a
strict "lattice-physical loop" filter.

**Fail.** Any HIT would be an abstract momentum-space algebraic relation,
not a lattice loop identity.

### Check 2 — 3+1D temporal Ward

The Z_3 spatial structure is retained; 3+1D temporal structure requires
an axiom extension. The `gamma = 1/2` parameter in H_base is a SPATIAL
CP signature, not a temporal Ward content. Speculative.

**Fail.** No 3+1D temporal Ward identity is currently in the retained atlas.

### Check 3 — hw=1 convergence with Koide κ=2

Koide's κ=2 selector (charged-lepton lane) is ONE-SCALAR: the remaining
Koide datum is a single real coordinate `m_*` on the selected slice
`delta = q_+ = sqrt(6)/3` (see
`KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md`). The DM
Lane E target is a TWO-real pair `(delta_*, q_+*)` on a distinct surface.
The two are structurally different: Koide's κ=2 already assumes DM's
(delta_*, q_+*) fixed and adds one scalar m_*. Lane E therefore cannot be
resolved by the Koide κ=2 equation.

**Fail.** Koide's κ=2 is downstream of DM's two-real pin; cannot
converge.

## Verdict

**DEAD, with a PARTIAL flag on the Z_3-reality obstruction:**

- The axiom-native Z_3-reality equation `Im Tr(H^2 C_3) = 0` IS derivable
 axiom-natively and IS non-variational. But its zero-locus gives `q_+ =
 (sqrt(2) - sqrt(6))/3 ≈ -0.345`, OUTSIDE the physical chamber. Hence
 this is a NEW OBSTRUCTION: an axiom-level equation whose zero-locus
 cannot host the physical pin. It sharpens (but does not close) the
 Case 3 impossibility.
- No other axiom-native algebraic equation in the retained content pins
 the physical chamber's Schur-Q candidate or any other retained
 candidate. Commutator equations have negative discriminants; Z_3 doublet
 block equations reduce to either identities or to the variational chamber
 boundary + Tr(H^2) minimum (which IS A3.1).
- δ-odd equations are all linear in δ with zero locus `δ = 0` (off the
 pin) or otherwise fail to intersect chamber.

Lane E therefore CONFIRMS the impossibility theorem's conclusion, with a
strengthened structure: the axiom-native Z_3-reality equation actively
CONTRADICTS chamber membership, so not only do variational selectors fail
to converge, but the distinguished non-variational algebraic equation also
misses the physical region.

Exit class: **DEAD**.

## Observational verification (flagged separately)

**Not performed.** This note makes no claim about PDG mass ratios, eta/eta_obs,
neutrino hierarchy, or any observable. All claims are axiom-internal algebraic
analysis on the retained `Cl(3)/Z^3` atlas.

## What this lane adds to the obstruction package

1. The Case 3 impossibility theorem (assumption A3.1 active) is now
 SHOWN to be stable without A3.1. Dropping A3.1 does not open a new
 selector lane.
2. A specific axiom-native algebraic equation (the Z_3-reality
 equation `Im Tr(H^2 C_3) = 0`) is derived and SHOWN to pin `q_+` to a
 value OUTSIDE the physical chamber. This is a new structural
 obstruction on the retained atlas.
3. Commutator identities `Tr([H, T_m]^2) < 0`, `Tr([H, T_δ]^2) < 0`,
 `Tr([H, T_q]^2) = -347/9` are derived as axiom-native algebraic
 identities with no real zeros in the active chart.

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_blocker_3_lane_e_combinatorial_equation_selector.py
```

## What this note must never say

- That Lane E closes the selector (it does not).
- That the Z_3-reality equation or any other axiom-native equation pins
 the physical `(delta_*, q_+*)` (none does).
- That A3.1 was removable without new structure (it was; the conclusion
 is unchanged).
- That this note invalidates or replaces the impossibility theorem (it
 reinforces it with one new angle).
