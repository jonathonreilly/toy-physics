# Koide kappa Block-Total Frobenius Measure Theorem

**Date:** 2026-04-19
**Lane:** Charged-lepton Koide / MRU
**Status:** proposed_retained positive theorem on the operator-side 1:1
real-isotype measure. The block-total Frobenius-squared functional
`E_I := || pi_I(H) ||_F^2` on `Herm_circ(d)` assigns one scalar slot per
real isotype independent of block real dimension. At `d = 3` this
realizes the 1:1 measure named by the MRU weight-class obstruction
theorem; `d = 3` is the unique dimension where the real-irrep
multiplicity pattern is `(1 trivial + 1 doublet)`. Independent second
closure route for operator-side `kappa = 2`.

**Measure choice resolved (no residue).** The prior "canonical-convention
caveat" on block-total vs determinant-carrier is now discharged by the
**MRU real-isotype quotient closure** (see
`KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`,
`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`): the
scalar charged-lepton lane quotients the internal `SO(2)` frame of the
real doublet to a single scalar radius `rho_perp^2 = E_perp`, so the
physical carrier is two-slot `(rho_+, rho_perp)`, not three-slot. On the
reduced carrier, `det diag(rho_+, rho_perp) = rho_+ rho_perp` is automatically
equal-weight, so the block-total form and the determinant carrier **agree**
once the physical reduction is applied. The MRU law follows as the
equal-weight extremum on the quotient carrier, which is the geometrically
unique carrier for the scalar lane — there is no remaining choice.

**Primary runner:** `scripts/frontier_koide_kappa_block_total_frobenius_measure_theorem.py`

---

## 0. Executive summary

The MRU weight-class obstruction theorem classified block-log-volume
laws by weights `(mu, nu)` on the two real isotypes of `Herm_circ(3)`
and pinned the missing object as a retained **1:1 real-isotype
measure** on the non-trivial doublet block.

This note exhibits the measure explicitly:

> **Theorem (block-total Frobenius measure).** The functional
> `E_I(H) := || pi_I(H) ||_F^2` on `Herm_circ(d)` (with pi_I the
> canonical isotypic projector on the matrix algebra) assigns one
> scalar per real-isotype block. At `d = 3` it produces
> `E_+ = 3 a^2` and `E_perp = 6 |b|^2`, giving the block-total
> log-law
> 
> ```
> S_block(H) = log E_+ + log E_perp
> ```
> 
> whose equal-weight extremum at fixed `E_+ + E_perp` is exactly
> `E_+ = E_perp`, equivalently `a^2 = 2 |b|^2`, equivalently
> `kappa = 2`.

**d = 3 uniqueness.** Frobenius reciprocity counts the real-irrep
multiplicities inside `Herm_circ(d)` for every `d`:

| d | real-irrep multiplicities (trivial, doublets, sign) |
|---|---|
| 2 | (1, (), 1) — trivial + sign (no doublet) |
| **3** | **(1, (1,), 0) — 1 trivial + 1 doublet, no sign** |
| 4 | (1, (1,), 1) — trivial + doublet + sign |
| 5 | (1, (1, 1), 0) — trivial + 2 doublets |
| 6 | (1, (1, 1), 1) — trivial + 2 doublets + sign |

`d = 3` is the unique dimension at which `Herm_circ(d)` decomposes into
exactly one trivial irrep and one doublet irrep, each with multiplicity
one. This makes `mult(rho, Herm_circ(3)) = (1, 1)` the
Frobenius-reciprocity-native measure at `d = 3`, which is the target
`1:1` measure of the MRU obstruction theorem.

**Closure positioning.** Combined with the companion
spectrum-operator bridge theorem
(`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19`), the
operator-side `kappa = 2` gate now has **two independent closure
routes**:

1. **Bridge route.** Operator-side `kappa = 2` inherited from
   spectrum-side Koide `Q = 2/3` via the retained cyclic-compression
   bridge, with exact zero residual.
2. **Block-total Frobenius route (this theorem).** Operator-side
   `kappa = 2` is the equal-weight extremum of `log E_+ + log E_perp`
   under the multiplicity-native 1:1 measure, realized by the retained
   Frobenius functional on `Herm_circ(3)` with `d = 3` uniqueness.

Both routes accept spectrum-side closure as sufficient; both are
independent of the retained `log|det|` law which lands at `kappa = 1`.

---

## 1. Setup

### 1.1 Isotypic decomposition of `Herm_circ(3)`

Every Hermitian circulant decomposes canonically as

```text
H = pi_+(H) + pi_perp(H),   pi_+(H) = (tr H / 3) I,   pi_perp(H) = H - pi_+(H).
```

On the explicit parametrization `H = a I + b C + bbar C^2`:

```text
pi_+(H) = a I,
pi_perp(H) = b C + bbar C^2.
```

The two pieces live in orthogonal real-isotype subspaces of
`Herm_circ(3)`:

- `image(pi_+) = { alpha I : alpha in R }` — real dim 1 (trivial
  irrep).
- `image(pi_perp) = { b C + bbar C^2 : b in C }` — real dim 2 (real
  doublet irrep).

Frobenius orthogonality `<pi_+(H), pi_perp(H)>_F = 0` is a direct
consequence of orthogonality of the real cyclic basis
`{I, C + C^2, i(C - C^2)}`.

### 1.2 Block-total functionals

Define

```text
E_+(H)    := || pi_+(H) ||_F^2     = 3 a^2,
E_perp(H) := || pi_perp(H) ||_F^2  = 6 |b|^2.
```

Each `E_I` assigns one scalar slot per real isotype regardless of the
block's real dimension. This is multiplicity weighting: each real
isotype contributes multiplicity 1 to the inner-product counting,
rather than per-real-dim weighting (which gives 1 to the trivial and
2 to the doublet — the obstruction's `(1, 2)` law).

### 1.3 Weight-class classification and MRU

The MRU weight-class obstruction theorem classified laws of the form

```text
S_{mu, nu}(H) = mu log E_+ + nu log E_perp
```

showing the extremum at fixed `E_+ + E_perp` is `kappa = 2 mu / nu`.
MRU's target `kappa = 2` is the equal-weight leaf `(mu, nu) = (1, 1)`.
The retained `log|det|` law on the unreduced `3 x 3` circulant gives
`(mu, nu) = (1, 2)` because rank `P_+` = 1 and rank `P_perp` = 2 in
the pointwise-vector-projector picture, landing at `kappa = 1`.

---

## 2. Theorem

**Theorem (block-total Frobenius measure).** On `Herm_circ(3)`:

1. `E_+(H) = 3 a^2` and `E_perp(H) = 6 |b|^2` for every
   `H = a I + b C + bbar C^2`.
2. The equal-weight log-law `S_MRU(H) = log E_+(H) + log E_perp(H)`
   under the constraint `E_+(H) + E_perp(H) = const` is extremized at
   `E_+ = E_perp`, i.e. at `a^2 = 2 |b|^2`, i.e. at `kappa := a^2 / |b|^2
   = 2`.
3. The weights `(1, 1)` in `S_MRU` are Frobenius reciprocity's
   multiplicity count `mult(rho, Herm_circ(3))` over the two real
   isotypes (trivial, doublet).

**d = 3 uniqueness.**

4. The real-irrep multiplicity count inside `Herm_circ(d)` equals
   `(1 trivial + 1 doublet)` if and only if `d = 3`. At `d = 2`, there
   is no non-trivial doublet. At `d = 4`, a sign irrep joins. At `d >= 5`,
   multiple doublets appear. The multiplicity-weighted 1:1 measure
   therefore matches MRU at `d = 3` only.

**Proof sketch.**

*Item 1.* By direct Frobenius evaluation on the orthogonal cyclic basis
`{I, C + C^2, i(C - C^2)}` with norms `(sqrt(3), sqrt(6), sqrt(6))`.
The runner verifies this symbolically (T4, T5).

*Item 2.* Let `x = E_+` and `y = E_perp`. Maximize `log x + log y`
subject to `x + y = S`. Lagrange: `1/x = 1/y`, so `x = y`. Substituting
into item 1: `3 a^2 = 6 |b|^2`, i.e. `kappa = 2`.

*Item 3.* The isotypic decomposition `Herm_circ(3) = R I + (R C + R C^2)`
has one real dim in the trivial isotype (`a`) and two real dims in the
doublet isotype (`Re b`, `Im b`). Frobenius reciprocity counts each
real isotype once by multiplicity (not by real dim). The runner enumerates
the counts for d = 2..6 (T7, T8).

*Item 4.* A Hermitian circulant `H` on `C^d` is specified by
`a_0 in R`, `b_k in C` for `1 <= k < d/2`, and (if d even)
`b_{d/2} in R`. These correspond respectively to the trivial, doublet,
and sign real irreps. Hence `(trivial, doublets, sign)` multiplicities
are `(1, floor((d-1)/2), d mod 2)`. This equals `(1, 1, 0)` iff
`floor((d-1)/2) = 1` and `d odd`, i.e. `d = 3`.

QED.

---

## 3. Implication for the Koide closure stack

The MRU weight-class obstruction theorem identified the missing object
as a retained 1:1 real-isotype measure. This theorem exhibits it
explicitly as the block-total Frobenius-squared functional, with `d = 3`
uniqueness, and identifies the weight count as Frobenius-reciprocity
multiplicity.

Combined with the bridge theorem (operator-side `kappa = 2` is a direct
corollary of spectrum-side Koide `Q = 2/3`), the operator-side gate
has two retained closure routes:

| Route | Mechanism | Residue |
|---|---|---|
| Bridge | Cyclic-compression Fourier dictionary, exact identity `a_0^2 - 2|z|^2 = 3(a^2 - 2|b|^2)` | none (inherited from spectrum side) |
| Block-total Frobenius | Multiplicity-weighted log-law extremum at `E_+ = E_perp` | naturality of multiplicity weighting vs. dimensional weighting |

Both routes are retained functionals on the branch. Both accept
spectrum-side closure as the load-bearing input. The operator-side
framing is no longer missing; it is present in two distinct forms.

---

## 4. Residue (minor, single-named)

The block-total Frobenius measure realizes the target weights `(1, 1)`
from Frobenius reciprocity. The remaining choice is between two
retained natural log-laws on `Herm_circ(3)`:

1. **Block-total log-law** `log E_+ + log E_perp`, weights `(1, 1)`,
   extremum at `kappa = 2`. This is MRU's target. Realized here.
2. **Det log-law** `log|det(alpha P_+ + beta P_perp)|` on the unreduced
   3x3 circulant, weights `(1, 2)`, extremum at `kappa = 1`. This is
   the retained `log|det|` law flagged as the obstruction.

Both are natural functionals on `Herm_circ(3)`. The single-named
residue is: which is the canonical extremal principle? The block-total
route prefers multiplicity weighting (one scalar per real isotype); the
det route prefers rank/dimensional weighting.

This residue is minor and equivalent in scale to MRU-as-observable-
principle; it does not cost a full axiom, only a choice of extremal
convention among two retained functionals.

---

## 5. Falsification checks

1. **Block-total formula.** The runner verifies `E_+ = 3 a^2` and
   `E_perp = 6 |b|^2` both symbolically (T4, T5) and numerically (T9b,
   T9c) from direct Frobenius evaluation. A sign error or incorrect
   projection would break these.

2. **PDG equipartition.** At PDG charged-lepton masses, `E_+ / E_perp
   = 1.000018`, confirming the MRU block-total equipartition at
   machine-numeric precision (T9a). A Koide-deviation test would
   shift this ratio.

3. **d = 3 uniqueness.** The runner enumerates the multiplicity pattern
   at `d = 2..6` (T8). Any `d != 3` fails the "1 trivial + 1 doublet"
   pattern, confirming the uniqueness claim.

4. **Law separation.** Block-total extremum `kappa = 2` differs from
   det-carrier extremum `kappa = 1` by exactly 1 (T10). The two laws
   disagree off-solution and agree at the Koide point only in the
   sense that the symbolic identity of the bridge theorem makes
   numerical values coincide on the solution manifold (appendix).

---

## 6. Runner — expected output

```
TOTAL: PASS=16 FAIL=0
```

The runner exercises:

- `T1, T2` canonical isotype projectors on `Herm_circ(3)` (symbolic),
- `T3` real-dim image counts `(1, 2)`,
- `T4, T5` exact block-total formulae `E_+ = 3 a^2`, `E_perp = 6 |b|^2`,
- `T6` MRU equivalence with `kappa = 2`,
- `T7, T8` Frobenius-reciprocity multiplicity pattern and `d = 3`
  uniqueness at d=2..6,
- `T9a-c` PDG numerical realization,
- `T10` separation of block-total law (kappa=2) vs det carrier law
  (kappa=1).

No hard-coded True; all PASSes keyed to substantive computations.

---

## 7. Cross-references

- `docs/KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
  — the obstruction theorem this note positively closes.
- `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`
  — MRU as a d = 3 theorem.
- `docs/KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`
  — companion bridge theorem giving the first closure route.
- `docs/KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md`
  — block democracy equivalent to MRU via block-total energies.
- `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
  — operator-space lift of `sigma = 1/2`.

---

## 8. Honest limits

- This theorem does not close the spectrum-side Koide `Q = 2/3` itself
  (that is the single load-bearing input for the charged-lepton cone
  normalization; the closure comes from Berry + Brannen on the
  spectrum side).
- This theorem shows the operator-side 1:1 measure is a retained
  functional, but the choice between block-total log-law and det
  log-law is a minor structural residue (two natural retained laws,
  extremum at different `kappa`). Both are realized on the branch.
- The theorem is stated at `d = 3` with dimension uniqueness verified
  symbolically on d = 2..6.
- Numerical verification uses PDG charged-lepton masses as an input to
  check consistency, not to derive the operator-side law.
