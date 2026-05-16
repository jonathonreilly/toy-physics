# Moment-Ratio Uniformity (MRU) on Cl(d)/Z_d — conditional support note

**Date:** 2026-04-19 (substantive status repair 2026-05-16: load-bearing
SO(2)-quotient explicitly demoted from "derived" to "admitted input").

**Lane:** Charged-lepton Koide / `kappa = 2`.

**Status:** support — conditional / alternative-framing only. This note is
**not** a retained closure route for operator-side `kappa = 2`. The
load-bearing carrier reduction (the SO(2)-quotient of the non-trivial real
doublet on the scalar charged-lepton lane) is an **admitted input** here, not
a derivation; the published demotion note
[`KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`](KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md)
proves that no currently retained framework theorem delivers this quotient on
`Herm_circ(3)`. The operator-side `kappa = 2` gate is carried by two
independent retained routes that do **not** use the SO(2)-quotient:

- [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
  (retained spectrum-operator bridge identity, symbolic zero residue);
- [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
  (real-isotype multiplicity counting via Frobenius reciprocity, no frame
  postulate).

**Primary runner:** `scripts/frontier_koide_moment_ratio_uniformity_theorem.py`
(certifies only the conditional algebra after the SO(2)-quotient is assumed;
does not derive the quotient itself).

**Companion runner:** `scripts/frontier_koide_mru_weight_class_obstruction_theorem.py`.

---

## 0. Executive summary

The same-day weight-class obstruction theorem proved an exact negative result
on the unreduced carrier:

```text
det(alpha P_+ + beta P_perp) = alpha beta^2,
```

so any log-volume law applied **there** counts the non-trivial sector with
weight `2`, not `1`, and lands at `kappa = 1`, not Koide's `kappa = 2`.

That theorem also identified the exact missing object:

```text
a retained 1:1 real-isotype measure, or an equivalent canonical reduction to a
two-slot (+, perp) carrier before applying the log-volume/extremal law.
```

This note records the **conditional** algebraic content of one candidate for
that missing object — the SO(2)-quotient of the non-trivial real doublet — and
its consequence chain to MRU and `kappa = 2`. Earlier drafts of this note
claimed the quotient was *derived* from retained charged-lepton structure.
That claim is **withdrawn**.

The demotion note proved (Section 1.2 of
[`KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`](KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md))
that the naive derivation fails:

```text
Under b -> e^{i theta} b (the SO(2) doublet phase rotation),
the eigenvalues lambda_k(theta) = a + 2 |b| cos(arg(b) + theta + 2 pi k / 3)
are not a permutation of the multiset for generic theta;
hence tr(H^3) and det(H) (and therefore log|det H|)
carry an explicit cos(3 arg b) dependence, which is not SO(2)-invariant.
```

Therefore the retained observable principle does **not** force the
SO(2)-quotient on its own. The generic scalar observable on `Herm_circ(3)`
depends on both `|b|` and `arg(b)` (through `cos(3 arg b)`). The SO(2)-quotient
is a strictly stronger physical postulate than "scalar observables are
spectrum-native".

This note therefore reads, in its retained form, as:

> *Given* the SO(2) frame-quotient on the charged-lepton scalar lane,
> the reduced two-slot carrier `(rho_+, rho_perp)` is exact, and the
> standard block log-volume / extremal law on that carrier forces
> `E_+ = E_perp <=> kappa = 2`.

That conditional content is genuine and is what the runner certifies. The
load-bearing physical premise (the SO(2)-quotient itself) is logged in
Section 2 as an admitted input and is not in scope of the runner.

---

## 1. Setup

On the retained `d = 3` cyclic compression,

```text
H = a I + b C + b^bar C^2,
```

with canonical real cyclic basis

```text
B_0 = I,
B_1 = C + C^2,
B_2 = i (C - C^2).
```

The real trace pairing gives

```text
||B_0||^2 = 3,
||B_1||^2 = ||B_2||^2 = 6,
<B_i, B_j> = 0  (i != j).
```

Writing

```text
H = (r_0 / 3) B_0 + (r_1 / 6) B_1 + (r_2 / 6) B_2,
```

the canonical block powers are

```text
E_+    = r_0^2 / 3,
E_perp = (r_1^2 + r_2^2) / 6.
```

In circulant variables this is

```text
E_+    = 3 a^2,
E_perp = 6 |b|^2.
```

So

```text
E_+ = E_perp
<=> 3 a^2 = 6 |b|^2
<=> kappa := a^2 / |b|^2 = 2.
```

That equivalence is exact and unconditional. The open question — whether the
scalar lane *physically* counts the non-trivial doublet once rather than twice
before applying any log-volume or extremal law — is what the SO(2)-quotient
postulate would answer. Section 2 documents that postulate as an admitted
input, not as a derivation.

---

## 2. Load-bearing admission: the SO(2)-quotient is an admitted input

### 2.1 The algebraic fact (not load-bearing)

The non-trivial sector is the real doublet

```text
V_perp := span_R{B_1, B_2}.
```

For every angle `theta` the orthogonal basis

```text
B_1' = cos(theta) B_1 + sin(theta) B_2,
B_2' = -sin(theta) B_1 + cos(theta) B_2
```

is another orthogonal basis of the same real isotype with the same norms.
Under this internal frame rotation,

```text
(r_1, r_2) -> (r_1', r_2') = R(theta) (r_1, r_2),
```

and the doublet radius is invariant:

```text
r_1'^2 + r_2'^2 = r_1^2 + r_2^2.
```

This is a trivial algebraic identity. It is *not* what carries the closure.

### 2.2 The load-bearing physical claim (admitted, not derived)

The load-bearing claim is the physical one:

> The charged-lepton scalar lane observables **factor through** the SO(2)
> orbit of the doublet plane. Equivalently, only the radius
> `r_1^2 + r_2^2 = 6 E_perp` is carried by the scalar lane; the angle
> `arg b` is not.

If this claim holds, the scalar lane has the exact two-slot quotient carrier

```text
(rho_+, rho_perp),  rho_+ := sqrt(E_+),  rho_perp := sqrt(E_perp),
```

which counts the non-trivial real isotype **once**, and the rest of the
argument (Section 3) goes through.

The demotion note (Section 1.2 of
[`KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`](KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md))
proves this claim is **not** a corollary of any retained framework theorem
currently on main or on this branch. Concretely the spectrum-native scalar
observables `tr(H^3)` and `det(H)` (and therefore `log|det H|`) carry an
explicit `cos(3 arg b)` dependence under `b -> e^{i theta} b`, so they do
**not** factor through `(|b|, a)` alone. Restricting attention to scalar
observables that happen to be `arg(b)`-independent (such as `tr(H^2)`) is the
same SO(2) postulate restated in a different coordinate system, not a
derivation of it.

Therefore the SO(2)-quotient enters this note as an **admitted input**, on
the same footing as the original obstruction theorem's identified missing
object. The note documents the conditional consequence of admitting it, not a
derivation of it.

### 2.3 Quotient coordinates under the admission

Under the admission of Section 2.2, the conditional quotient coordinates are

```text
rho_+    := sqrt(E_+)    = |r_0| / sqrt(3),
rho_perp := sqrt(E_perp) = sqrt(r_1^2 + r_2^2) / sqrt(6).
```

Then:

1. `rho_+` is the Frobenius amplitude of the trivial block;
2. `rho_perp` is the Frobenius amplitude of the whole non-trivial real
   doublet;
3. both are invariant under all internal `SO(2)` frame rotations of
   `V_perp` (algebraic, Section 2.1);
4. the scalar target itself can already be written on this quotient:

   ```text
   kappa = a^2 / |b|^2 = 2 E_+ / E_perp = 2 rho_+^2 / rho_perp^2.
   ```

So *if* the admission holds, the charged-lepton scalar lane has an exact
retained two-slot carrier `(rho_+, rho_perp)` that counts the non-trivial real
isotype once. The conditional closure of Sections 3-4 starts here.

---

## 3. The reduced log-volume law (conditional)

Under the admission of Section 2.2, the scalar lane is written on the
quotient carrier and the standard block log-volume law is applied to

```text
D_red = diag(rho_+, rho_perp),
```

not to the unreduced `3 x 3` carrier.

Then

```text
det(D_red) = rho_+ rho_perp,
log|det D_red| = log rho_+ + log rho_perp.
```

Fix the total reduced power

```text
rho_+^2 + rho_perp^2 = E_tot.
```

With one Lagrange multiplier,

```text
L = log rho_+ + log rho_perp - lambda (rho_+^2 + rho_perp^2 - E_tot),
```

the interior stationary equations are

```text
1 / rho_+ = 2 lambda rho_+,
1 / rho_perp = 2 lambda rho_perp.
```

Hence

```text
rho_+^2 = rho_perp^2 = E_tot / 2.
```

Because the Hessian is negative on the constrained positive branch, this is the
unique maximum.

So the reduced-carrier extremal law gives

```text
rho_+ = rho_perp
<=> E_+ = E_perp.
```

Pulling back to the cyclic carrier gives

```text
r_0^2 / 3 = (r_1^2 + r_2^2) / 6
<=> 3 a^2 = 6 |b|^2
<=> kappa = 2.
```

That is MRU at `d = 3`, **conditional on the Section 2.2 admission**.

---

## 4. Why the old obstruction remains true regardless

The unreduced determinant obstruction remains exact independent of the
Section 2.2 admission:

```text
det(alpha P_+ + beta P_perp) = alpha beta^2.
```

So if one insists on applying the log-volume law on the unreduced `3 x 3`
carrier, the non-trivial sector is counted with multiplicity `2` and the leaf
is wrong.

What changes between Sections 3 and 4 is **not** the obstruction calculation.
What changes is the carrier.

If the Section 2.2 admission holds, the scalar charged-lepton lane does not
retain the ordered pair of Cartesian doublet coordinates as physical slots; it
retains only the internal-rotation quotient of that plane, and the relevant
carrier has two slots, not three:

```text
(+) and (perp).
```

So the old obstruction theorem should be read in this branch's published form
as:

> on the unreduced carrier the weights are wrong; therefore *if* there is a
> canonical real-isotype reduction, the obstruction is resolved on that
> reduced carrier.

This note documents that conditional resolution. The unconditional retained
closure routes for operator-side `kappa = 2` are in the bridge and
block-total Frobenius notes cited in the header; they do not use the
SO(2)-quotient.

---

## 5. Dimensional uniqueness statement (conditional)

The dimensional uniqueness theorem from the earlier MRU note still stands as
a conditional statement: *if* the SO(2)-quotient closure is used, then the
single non-trivial singlet-vs-doublet scalar selector form holds only for the
real-isotype pattern

```text
1 singlet + 1 real doublet,
```

which occurs only at `d = 3`.

So the conditional MRU closure documented here is not a free weight trick
that would work uniformly for all `d`. It depends on:

- the exact retained `d = 3` real-isotype structure
  `R^3 = V_+ ⊕ V_perp` with `dim_R(V_+) = 1`, `dim_R(V_perp) = 2`; and
- the Section 2.2 admission (SO(2)-quotient on the charged-lepton scalar
  lane).

The retained `kappa = 2` routes (bridge and block-total Frobenius) carry
dimensional uniqueness on their own terms without the second hypothesis.

---

## 6. Scientific consequence

The scientific status of the MRU lane on this branch is now:

1. the old weight-class obstruction on the unreduced carrier is correct
   (unconditional);
2. the exact missing object it identified — a canonical reduction to a
   two-slot real-isotype carrier — is **not** derived from currently retained
   framework theorems (see demotion note Section 1.2);
3. *given* the SO(2)-quotient admission of Section 2.2, the reduced carrier
   `(rho_+, rho_perp)` is exact and the reduced log-volume / extremal law
   forces `E_+ = E_perp <=> kappa = 2`;
4. operator-side `kappa = 2` is independently carried, **without** the
   SO(2)-quotient admission, by the two retained routes in the header
   (bridge and block-total Frobenius); the MRU lane is supplementary
   exposition, not a retained closure route.

---

## 7. Scope

### What this note establishes (conditional)

1. *Given* the Section 2.2 admission that the charged-lepton scalar lane
   physically quotients the doublet frame, the reduced carrier is exactly
   `(rho_+, rho_perp)`, equivalently `(E_+, E_perp)`.
2. *Given* the same admission, applying the block log-volume / extremal law
   on that carrier forces MRU and therefore `kappa = 2`.
3. The doublet radius `r_1^2 + r_2^2` is algebraically SO(2)-invariant
   (Section 2.1) — this is unconditional and is what the runner verifies.

### What this note does not establish

1. This note does not derive the SO(2)-quotient on the charged-lepton scalar
   lane from any retained framework theorem; it admits it as input. The
   demotion note proves the naive derivation route (via the retained
   observable principle alone) fails because of explicit `cos(3 arg b)`
   dependence in `tr(H^3)` and `det(H)`.
2. This note is not a retained closure route for operator-side `kappa = 2`.
   That gate is carried by the bridge and block-total Frobenius theorems
   cited in the header, neither of which uses the SO(2)-quotient.
3. This note does not claim that the unreduced `3 x 3` determinant law is
   wrong; it claims only that the obstruction would be resolved on a reduced
   carrier *if* the Section 2.2 admission holds.
4. This note does not address the Berry / `delta = 2/9` lane.

---

## 8. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_moment_ratio_uniformity_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_koide_mru_weight_class_obstruction_theorem.py
```

The primary runner verifies the conditional algebra of Sections 1, 3, 4, 5
(class A) under the explicit Section 2.2 admission of the SO(2)-quotient
(class G, recorded by the runner as an admitted input and not certifiable in
its restricted packet). The companion runner verifies the unconditional
obstruction calculation on the unreduced carrier.
