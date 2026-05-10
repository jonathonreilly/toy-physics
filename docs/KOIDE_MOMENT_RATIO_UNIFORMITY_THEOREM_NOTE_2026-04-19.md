# Moment-Ratio Uniformity (MRU) Theorem on Cl(d)/Z_d

**Date:** 2026-04-19
**Lane:** Charged-lepton Koide / `kappa = 2`
**Status:** support - structural or confirmatory support note
weight-class obstruction remains correct on the unreduced `3 x 3` determinant
carrier, but the exact missing object it isolated is now derived: the scalar
charged-lepton lane lives on the canonical two-slot real-isotype quotient
carrier `(+ , perp)`, not on the unreduced `(+,1,2)` Cartesian split of the
doublet plane. On that reduced carrier the standard block log-volume / extremal
law forces MRU and hence `kappa = 2`.
**Primary runner:** `scripts/frontier_koide_moment_ratio_uniformity_theorem.py`
**Companion runner:** `scripts/frontier_koide_mru_weight_class_obstruction_theorem.py`

**Status authority and audit hygiene (2026-05-10):**
The audit lane has classified this row `audited_conditional` (claim_type
`positive_theorem`, audit_date 2026-05-05, auditor codex-cli-gpt-5.5,
auditor_confidence high). The verdict accepts the runner's symbolic
algebra — that, **given** the canonical `SO(2)` quotient of the
non-trivial real doublet to the two-slot pair `(rho_+, rho_perp)`, the
reduced log-volume / extremal law has its unique positive stationary
point at `rho_+ = rho_perp` and therefore forces `E_+ = E_perp` and
`kappa = 2` — but flags that the packet does not derive that this
quotient is the physical charged-lepton scalar carrier. The audit
therefore reads the load-bearing step (`load_bearing_step_class = E`)
as a **carrier choice introduced as exact** rather than a theorem from
an independent retained input. Audit verdict and effective status are
set by the independent audit lane only; nothing in this rigorization
edit promotes status. The companion `KOIDE_MRU_DEMOTION_NOTE_2026-04-20`
(retained on main) already reclassifies this MRU route as
**supplementary / alternative-framing support** for operator-side
`kappa = 2`, with two retained independent routes
(`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19` and
`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19`)
carrying the operator-side gate without any `SO(2)`-quotient postulate.

The audit-stated cheapest re-audit path (verbatim from the ledger
`notes_for_re_audit_if_any`):

> missing_bridge_theorem: provide a retained derivation that the
> charged-lepton scalar lane physically quotients the non-trivial real
> doublet's `SO(2)` frame before the log-volume/extremal law is applied.

---

## 0. Executive summary

The same-day obstruction theorem proved an exact negative result on the
unreduced carrier:

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

This note supplies that object.

The key step is that the charged-lepton scalar lane does **not** retain the
Cartesian basis of the non-trivial real doublet
`span_R{B_1, B_2}`. The only retained scalar datum on that plane is its
Frobenius radius. Equivalently, the scalar lane quotients the internal
`SO(2)` frame rotation of the doublet:

```text
(r_1, r_2) ~ R(theta) (r_1, r_2).
```

So the actual scalar carrier is the two-slot quotient

```text
(r_0, r_1, r_2)  ->  (rho_+, rho_perp),

rho_+^2    = E_+    = r_0^2 / 3,
rho_perp^2 = E_perp = (r_1^2 + r_2^2) / 6.
```

On that reduced carrier there are exactly two positive slots. Applying the
usual block log-volume / extremal law there gives

```text
log det diag(rho_+, rho_perp) = log rho_+ + log rho_perp,
```

whose unique fixed-power stationary point is

```text
rho_+ = rho_perp
<=> E_+ = E_perp
<=> a^2 = 2 |b|^2
<=> kappa = 2.
```

So the live MRU gap is now closed on this branch for the `kappa = 2` lane.

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

That equivalence was already exact. The open question was why the scalar lane
should count the doublet once rather than twice before applying a log-volume or
extremal law.

---

## 2. The load-bearing step: canonical real-isotype reduction

The non-trivial sector is the real doublet

```text
V_perp := span_R{B_1, B_2}.
```

Its internal basis is not physical data. The exact `Z_3` / circulant geometry
already identifies the whole plane, but any orthonormal basis of that plane is
equally valid. Concretely, for every angle `theta`,

```text
B_1' = cos(theta) B_1 + sin(theta) B_2,
B_2' = -sin(theta) B_1 + cos(theta) B_2
```

is another canonical orthogonal basis of the same real isotype with the same
norms. Under this internal frame rotation,

```text
(r_1, r_2) -> (r_1', r_2') = R(theta) (r_1, r_2),
```

but the only scalar carried by the plane is its radius:

```text
r_1'^2 + r_2'^2 = r_1^2 + r_2^2.
```

Therefore the scalar charged-lepton lane factors through the quotient

```text
R ⊕ R^2  / SO(2),
```

not through the unreduced ordered triple `(r_0, r_1, r_2)`.

### Canonical quotient coordinates

Define

```text
rho_+    := sqrt(E_+)    = |r_0| / sqrt(3),
rho_perp := sqrt(E_perp) = sqrt(r_1^2 + r_2^2) / sqrt(6).
```

Then:

1. `rho_+` is the Frobenius amplitude of the trivial block;
2. `rho_perp` is the Frobenius amplitude of the whole non-trivial real
   doublet;
3. both are invariant under all internal `SO(2)` frame rotations of
   `V_perp`;
4. the scalar target itself already lives on this quotient:

   ```text
   kappa = a^2 / |b|^2 = 2 E_+ / E_perp = 2 rho_+^2 / rho_perp^2.
   ```

So the charged-lepton scalar lane has an exact retained two-slot carrier

```text
(rho_+, rho_perp),
```

which counts the non-trivial real isotype **once**.

This is exactly the object the obstruction theorem said was missing.

---

## 3. The reduced log-volume law

Once the scalar lane is written on the quotient carrier, the standard
block log-volume law is applied to

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

That is exactly MRU at `d = 3`.

---

## 4. Why the old obstruction remains true but no longer blocks the lane

The unreduced determinant obstruction remains exact:

```text
det(alpha P_+ + beta P_perp) = alpha beta^2.
```

So if one insists on applying the log-volume law on the unreduced `3 x 3`
carrier, the non-trivial sector is counted with multiplicity `2` and the leaf
is wrong.

What changes here is **not** the obstruction calculation. What changes is the
carrier.

The scalar charged-lepton lane does not retain the ordered pair of Cartesian
doublet coordinates as physical slots. It retains only the internal-rotation
quotient of that plane. Once that quotient is taken, the relevant carrier has
two slots, not three:

```text
(+) and (perp).
```

So the old obstruction theorem should now be read as:

> on the unreduced carrier the weights are wrong; therefore closure requires a
> canonical real-isotype reduction first.

This note derives exactly that reduction.

---

## 5. Why `d = 3` is still the unique MRU dimension

The dimensional uniqueness theorem from the earlier MRU note still stands.

For `Herm_circ(d)`, MRU gives a single non-trivial singlet-vs-doublet scalar
selector iff the real-isotype pattern is exactly

```text
1 singlet + 1 real doublet.
```

That happens only at `d = 3`.

So the current closure is not a free weight trick that would work uniformly for
all `d`. It depends on the exact retained `d = 3` real-isotype structure:

```text
R^3 = V_+ ⊕ V_perp
with dim_R(V_+) = 1, dim_R(V_perp) = 2,
```

and on the fact that the scalar lane quotients the internal frame of the single
real doublet.

---

## 6. Scientific consequence

The scientific status of the MRU lane on this branch is now:

1. the old weight-class obstruction on the unreduced carrier is correct;
2. the exact missing object it identified is now derived from retained
   charged-lepton structure;
3. the scalar lane's physical carrier is the real-isotype quotient
   `(rho_+, rho_perp)`;
4. the usual reduced-carrier log-volume / extremal law forces

   ```text
   E_+ = E_perp
   <=> kappa = 2.
   ```

So the `kappa = 2` / MRU lane is closed on the current branch.

---

## 7. Scope

### What is established

1. The non-trivial `C_3` real doublet is counted once on the scalar
   charged-lepton lane because its internal `SO(2)` frame is quotient data,
   not physical slot data.
2. The exact reduced carrier is `(rho_+, rho_perp)`, equivalently
   `(E_+, E_perp)`.
3. Applying the block log-volume / extremal law on that carrier forces MRU and
   therefore `kappa = 2`.

### What is not claimed here

1. This note does not address the Berry / `delta = 2/9` lane.
2. This note does not by itself overwrite the broader current-main
   charged-lepton review boundary.
3. This note does not claim that the unreduced `3 x 3` determinant law was
   wrong; it claims only that it was being applied before the exact real-isotype
   scalar reduction.

---

## 8. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_moment_ratio_uniformity_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_koide_mru_weight_class_obstruction_theorem.py
```

Both runners now validate the load-bearing reduction step rather than only the
postulated equal-weight leaf.

## 9. Audit-conditional perimeter

The internal algebra of this note (Sections 1–7) is what the audit
verdict accepts as internally consistent on the admitted reduced
carrier:

| Internal algebra step | Audit-accepted as internal consistency |
|---|---|
| Real-trace pairing on the cyclic basis `(B_0, B_1, B_2)` (Section 1) | yes |
| `E_+ = r_0^2/3 = 3 a^2`, `E_perp = (r_1^2 + r_2^2)/6 = 6 |b|^2` (Section 1) | yes |
| `r_1^2 + r_2^2` is `SO(2)`-orbit invariant on the doublet plane (Section 2) | yes |
| Quotient-coordinate identification `rho_+^2 = E_+`, `rho_perp^2 = E_perp` (Section 2) | yes |
| Reduced log-volume law `log det diag(rho_+, rho_perp) = log rho_+ + log rho_perp` (Section 3) | yes |
| Lagrange stationarity at `rho_+^2 = rho_perp^2 = E_tot/2` and pullback to `kappa = 2` (Section 3) | yes |
| Unreduced `det(alpha P_+ + beta P_perp) = alpha beta^2` and `(1,2)` weight contrast (Section 4) | yes |
| `d = 3` real-isotype uniqueness (`1` singlet + `1` real doublet) (Section 5) | yes |

The audit-conditional perimeter (i.e. what stays open) is exactly the
load-bearing carrier-identification step:

1. derive the physical `SO(2)` quotient of the non-trivial real doublet
   on the **scalar charged-lepton lane** from a retained upstream
   theorem rather than introducing it as the exact scalar carrier
   (this is the `load_bearing_step_class = E` step the verdict flags);
2. equivalently, derive that the scalar charged-lepton observable
   principle on `Herm_circ(3)` factors through the two-slot real-isotype
   quotient `(rho_+, rho_perp)` from retained upstream inputs.

Until (1)/(2) is supplied by a retained upstream theorem, this row
remains a bounded conditional theorem on the admitted reduced carrier
(MRU follows once the quotient is granted), not a first-principles
closure of the operator-side `kappa = 2` lane. The companion
`KOIDE_MRU_DEMOTION_NOTE_2026-04-20` documents (Section 1.2) that
spectrum-native scalar observables on `Herm_circ(3)` are **not**
`SO(2)`-invariant in general — the determinant and `tr(H^3)` carry an
explicit `cos(3 arg b)` channel — so the `SO(2)` quotient is strictly
stronger than "scalar observables are spectrum-native" and is not a
corollary of the retained observable principle on this branch.

## 10. Path A future work (audit-stated repair target)

To move this row's `audit_status` from `audited_conditional` toward
retained-grade, the audit verdict's repair list requires:

1. a retained upstream theorem deriving that the physical
   charged-lepton scalar lane factors through the `SO(2)` quotient of
   the non-trivial real doublet — i.e. that the only retained scalar
   datum on `V_perp = span_R{B_1, B_2}` is its Frobenius radius — from
   a retained framework input rather than as a local definition or
   axiom;
2. equivalently, a retained upstream theorem that decouples the
   `cos(3 arg b)` channel of `Herm_circ(3)` scalar observables on the
   physical charged-lepton lane.

Per the demotion note already on main, the `kappa = 2` operator-side
gate does **not** depend on supplying (1)/(2): two retained independent
routes (`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19`
and `KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19`)
already carry it without any `SO(2)`-quotient postulate. The Path A
work above is the audit-stated path to promote **this** row's status,
not a prerequisite for the operator-side closure.

## 11. Boundaries

This note does **not**:

- modify the parent row's audit-ledger entry;
- promote the parent's `audit_status` from `audited_conditional`;
- derive the `SO(2)` quotient of the non-trivial real doublet on the
  scalar charged-lepton lane from retained upstream inputs;
- override the `KOIDE_MRU_DEMOTION_NOTE_2026-04-20` reclassification
  of this MRU route as supplementary / alternative-framing support;
- close the operator-side `kappa = 2` gate (already carried on main by
  the spectrum-operator bridge and block-total Frobenius routes
  without any `SO(2)`-quotient assumption);
- touch the spectrum-side `Q = 2/3` Berry / Brannen route or the
  `delta = 2/9` Brannen-phase bridge.

The same audit-named missing bridge theorem also blocks the companion
row `koide_mru_weight_class_obstruction_theorem_note_2026-04-19`
(`audited_renaming` for the same `SO(2)`-quotient carrier choice).
