# Koide MRU Formal Demotion Note

**Date:** 2026-04-20
**Lane:** Charged-lepton Koide / kappa = 2
**Status:** support - structural or confirmatory support note
"SO(2)-quotient" closure route to supplementary / alternative-framing
support, and promotes the spectrum-operator bridge theorem as the
**primary** retained closure route for operator-side kappa = 2.
**Primary retained route (promoted):**
`docs/KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`
(runner PASS=9, symbolic zero residual).
**Independent second route:**
`docs/KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`
(runner PASS=16).
**Demoted route:**
`docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md` +
`docs/KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`.

---

## Cited authorities (one hop)

This note's load-bearing one-hop citations registered to the audit-graph
builder:

- [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
  — retained spectrum-operator bridge identity that carries operator-side
  `kappa = 2` as a corollary of spectrum-side `Q = 2/3` with symbolic zero
  residue. This is the **primary retained closure route** promoted by the
  present demotion note.
- [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
  — independent second route via real-isotype multiplicity counting on the
  block-total Frobenius-squared functional. Cited for completeness as the
  alternative non-MRU route. (Note: this authority is itself unaudited; the
  primary retained route above carries the demotion.)
- [`KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`](KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md)
  — the demoted MRU theorem note whose closure status this note formally
  reclassifies to supplementary / alternative-framing support.
- [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
  — the companion MRU obstruction note co-demoted by this reclassification.

These citations register the one-hop load-bearing dependency edges so the
citation-graph builder picks them up on the next pipeline run. The repair
addresses the `notes_for_re_audit_if_any` request to "add one-hop
dependencies for the spectrum-operator bridge theorem, block-total
Frobenius theorem" in the prior audit verdict on this note.

---

## 0. Why this note exists

A strict-reviewer audit of the scalar-selector cycle 1 stack found one
structural open import behind the MRU closure route for Koide kappa:

> The MRU + weight-class obstruction route relies on a postulate that
> "the scalar charged-lepton lane does not retain the Cartesian basis of
> the real doublet; it retains only the Frobenius radius
> `rho_perp^2 = E_perp`". This is an internal `SO(2)`-quotient of the
> doublet frame. The two MRU notes renamed the postulate as a
> derivation, but the underlying SO(2)-invariance check in the runner
> verifies only the trivial rotation identity
>
>     r_1'^2 + r_2'^2 = r_1^2 + r_2^2 under R(theta),
>
> not the physical claim that the lane observables **factor through**
> that radius.

That is a correct audit finding. This note accepts it, attempts the
retained-framework derivation (Path A), documents why it does not close,
and formally repositions the stack so the `kappa = 2` gate is carried by
the two independent retained routes that do not require the SO(2)
quotient at all.

---

## 1. Path A attempt: can the SO(2)-quotient be derived from the retained observable principle?

### 1.1 The candidate route

Path A would attempt to derive the SO(2)-quotient from the retained
observable principle:

- `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` — scalar bosonic
  observables are source derivatives of `W[J] = log|det(D + J)|`.
- `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` — on the retained
  `hw=1` triplet, the retained operator algebra is all of `M_3(C)`.
- `docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md` — on
  the sqrt-mass vector Fourier decomposition, Koide `Q = 2/3` is
  equivalent to `a_0^2 = 2 |z|^2`.
- `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` —
  `C_3[111]`-invariant Hermitian operators are circulants
  `H = a I + b C + bbar C^2`.

The naive Path A argument would go:

1. Scalar observables are determined by the spectrum (log|det| and its
   derivatives are symmetric functions of the eigenvalues).
2. Under the internal SO(2) frame rotation of the doublet
   `span_R{B_1, B_2} = span_R{C + C^2, i(C - C^2)}`, the parameter `b`
   transforms as `b -> e^{i theta} b`.
3. If this were a unitary conjugation, the spectrum would be invariant,
   and therefore all scalar observables would factor through the
   rotation-invariant data `(a, |b|)`.

### 1.2 Why Path A fails

Step 3 is false. Under `b -> e^{i theta} b`, the eigenvalues of
`H = a I + b C + bbar C^2` transform as

```text
lambda_k(theta) = a + 2 |b| cos(arg(b) + theta + 2 pi k / 3),   k = 0, 1, 2.
```

For a generic continuous `theta`, this is **not** a permutation of the
eigenvalue multi-set `{lambda_0, lambda_1, lambda_2}`. The multiset is
invariant only under the discrete subgroup `theta in {0, 2 pi / 3,
4 pi / 3}` (which cycles the index `k`). So the SO(2) continuous
rotation is not a spectral symmetry, hence not a unitary conjugation of
`H`, and spectral scalar observables are **not** SO(2)-invariant in
general.

Explicit check:

- `tr(H^2) = 3 a^2 + 6 |b|^2` is SO(2)-invariant (depends only on `|b|^2`).
- `tr(H^3)` has an `a (b^3 + bbar^3) = 2 a |b|^3 cos(3 arg b)` piece,
  which is **not** invariant under `b -> e^{i theta} b` for generic
  `theta`.
- `det(H) = a^3 + b^3 + bbar^3 - 3 a |b|^2` carries the same
  `cos(3 arg b)` dependence, so `log|det|` is **not** SO(2)-invariant.

Therefore the retained observable principle does **not** force the
SO(2)-quotient on its own. The generic scalar observable on
`Herm_circ(3)` depends on both `|b|` and `arg(b)` (through
`cos(3 arg b)`). The SO(2)-quotient is a genuinely additional
postulate, strictly stronger than "scalar observables are
spectrum-native".

### 1.3 What a broken Path A would look like

A putative Path A derivation could still try to restrict attention to
scalar observables that happen to be `arg(b)`-independent (such as
`tr(H^2)`, `|b|^2`, `E_perp`). But that selection is a non-trivial
choice — it is exactly the same SO(2) postulate written in a different
coordinate system ("use only `arg(b)`-independent invariants"). That is
the circular restatement the reviewer audit flagged.

**Verdict.** Path A cannot close at the Nature bar. The SO(2)-quotient
is not a corollary of any retained framework theorem currently on main
or on this branch.

---

## 2. Path B: formal demotion of MRU, promotion of the bridge

Path B observes that the MRU route is **not needed** for operator-side
`kappa = 2` closure. Two independent retained theorems on this branch
already give `kappa = 2` without any SO(2)-quotient assumption.

### 2.1 Primary route — spectrum-operator bridge

Source: `docs/KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`.

Content. On `Herm_circ(3)`, the cyclic-compression Fourier dictionary
delivers the **exact** polynomial identity

```text
a_0^2 - 2 |z|^2  =  3 (a^2 - 2 |b|^2)
```

where `(a_0, z)` are the Fourier scalars of the sqrt-mass eigenvalue
triple under the retained P1 identification `lambda_k = sqrt(m_k)`, and
`(a, b)` are the circulant parameters. The identity is symbolic with
zero residual. Consequently

```text
[spectrum-side]  a_0^2 = 2 |z|^2   (Koide Q = 2/3)
           <=>  [operator-side] a^2 = 2 |b|^2   (kappa = 2),
```

with **zero residue**, for any `Herm_circ(3)`. The operator-side
`kappa = 2` is a direct corollary of the spectrum-side Koide condition;
no SO(2)-quotient is used, because the identity is a genuine Fourier
bijection on `Herm_circ(3)` rather than an extremal-law argument on a
reduced carrier.

Runner: `scripts/frontier_koide_kappa_spectrum_operator_bridge_theorem.py`,
`PASS = 9, FAIL = 0`.

### 2.2 Independent second route — block-total Frobenius measure

Source: `docs/KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`.

Content. The block-total Frobenius-squared functional

```text
E_I(H) := || pi_I(H) ||_F^2
```

assigns one scalar slot per real isotype. At `d = 3` it gives the
`(1, 1)` multiplicity count from Frobenius reciprocity (one trivial
real isotype + one real doublet, each with multiplicity one), and the
equal-weight log-law

```text
S_MRU(H) = log E_+ + log E_perp
```

has its equal-weight extremum at `E_+ = E_perp`, equivalently
`kappa = 2`. The `(1, 1)` weights come from real-isotype multiplicity,
not from a frame rotation of the doublet. `d = 3` is the unique
dimension for which the multiplicity pattern is exactly
`(1 trivial + 1 doublet)` (runner enumerates d = 2..6).

Runner: `scripts/frontier_koide_kappa_block_total_frobenius_measure_theorem.py`,
`PASS = 16, FAIL = 0`.

### 2.3 What the two routes collectively carry

Both routes land at `kappa = 2`. Neither uses the SO(2)-quotient.

- The bridge gives a **symbolic equivalence** (zero residual) from
  spectrum-side to operator-side. It **inherits** closure from the
  retained spectrum-side route (Berry + Brannen at machine precision),
  so its axiom cost at the operator side is zero.
- The block-total Frobenius measure gives the `(1, 1)` weights
  **directly** from Frobenius reciprocity multiplicity counting, which
  is a standard representation-theoretic statement independent of any
  frame choice.

The `kappa = 2` gate is therefore carried by two retained independent
routes, neither of which requires the SO(2)-quotient.

---

## 3. Formal demotion statement

Effective from this note:

1. **MRU is no longer a primary closure route for operator-side
   kappa = 2.** The two MRU notes on the branch
   (`KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md` and
   `KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`) are
   reclassified as **supplementary / alternative-framing support**
   rather than load-bearing theorems.

2. **The MRU closure argument assumes a postulate not derivable from
   retained framework theorems.** Specifically, the scalar-lane
   SO(2)-quotient of the doublet frame is not a consequence of the
   retained observable principle (spectrum-native scalar observables
   are **not** SO(2)-invariant on `Herm_circ(3)` in general).

3. **The spectrum-operator bridge theorem is the primary retained
   closure route** for operator-side `kappa = 2`. It carries the gate
   with symbolic zero residual and no new axiom cost beyond what
   spectrum-side Berry + Brannen already pay.

4. **The block-total Frobenius measure theorem is the independent
   second closure route.** It produces the `(1, 1)` weight pattern
   from Frobenius reciprocity multiplicity without any frame
   postulate.

5. **The MRU notes retain their role as alternative pedagogical
   framings.** They correctly capture the content that, *if one
   imposes* the SO(2)-quotient by hand, the block log-volume extremum
   gives `kappa = 2`. That remains a valid conditional statement and
   is useful exposition. It is not a retained closure path.

---

## 4. Scientific consequence for the scalar-selector cycle 1 stack

The strict-reviewer audit's structural open import (I6) is hereby
closed via Path B: the postulate is **not** promoted to a theorem, and
the MRU route it sat under is demoted out of the closure stack.

Operator-side `kappa = 2` is retained **without any SO(2)-quotient
postulate**. The two retained routes that carry it
(bridge + block-total Frobenius) do not use or need that postulate.

The remaining load-bearing input for the full charged-lepton Koide
closure is the **spectrum-side** `Q = 2/3` (Berry + Brannen), which is
closed at machine precision on the retained spectrum-side route and is
not affected by this demotion.

---

## 5. Effect on cross-references

The following retained notes currently reference the MRU route as if
it were a primary closure path and should be read with this demotion
in mind:

- `docs/KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`
  already treats the bridge and itself as the two independent retained
  routes and flags the measure-choice residue as minor (section 4).
  The "MRU real-isotype quotient closure" paragraph in its preamble
  should be read as an alternative supplementary framing.
- `docs/KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`
  already states correctly (section 3) that the operator-side framing
  is a **corollary** of the spectrum-side closure via the bridge
  identity. No change of content is needed there; this note confirms
  the bridge's primary status.
- `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md` and
  `docs/KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
  are downgraded to supplementary status but remain useful exposition
  of the conditional MRU argument. Their runners
  (`frontier_koide_moment_ratio_uniformity_theorem.py` and
  `frontier_koide_mru_weight_class_obstruction_theorem.py`) continue
  to verify what they actually verify (the reduced-carrier
  log-volume extremum **given** the SO(2)-quotient); they do not
  claim to derive that quotient.

---

## 6. What is not claimed here

1. This note does not claim that the SO(2)-quotient is **false**. It
   may still be physically correct — e.g. if a future retained result
   establishes that the charged-lepton scalar lane decouples the
   `cos(3 arg b)` channel. What is claimed is only that no currently
   retained framework theorem delivers it.
2. This note does not invalidate the two MRU notes as technical
   documents. Their calculations remain correct within the conditional
   "assume SO(2)-quotient, then...". What changes is only their status
   in the closure stack.
3. This note does not change the spectrum-side Koide closure. Berry +
   Brannen remain the load-bearing spectrum-side input.

---

## 7. Reproduction

No new runner is required for this note. The load-bearing checks are:

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_kappa_spectrum_operator_bridge_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_koide_kappa_block_total_frobenius_measure_theorem.py
```

Both must continue to PASS cleanly on this branch. The MRU runners
continue to verify their own internal conditional statements but are
no longer load-bearing for operator-side `kappa = 2` closure.

---

## 8. Summary

| Route | Status | Requires SO(2)-quotient? |
|---|---|---|
| Spectrum-operator bridge (PASS=9, zero symbolic residue) | **Primary retained route** | No |
| Block-total Frobenius measure (PASS=16) | **Independent second route** | No |
| MRU + weight-class obstruction | **Supplementary / alternative framing** | Yes (not derivable from retained theorems) |

The `kappa = 2` gate is carried by two retained independent routes
neither of which requires the SO(2)-quotient postulate. The MRU route
is kept as supplementary support but is not load-bearing.
