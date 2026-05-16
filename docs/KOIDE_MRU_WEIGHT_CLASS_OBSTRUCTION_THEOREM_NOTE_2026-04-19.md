# Koide MRU Weight-Class Obstruction Theorem

**Date:** 2026-04-19
**Lane:** Charged-lepton Koide / MRU
**Status:** support - structural or confirmatory support note
its resolution. The theorem itself is unchanged: the unreduced
`3 x 3` determinant carrier counts weights `(1,2)` and therefore cannot force
MRU by itself. What has changed is that the exact missing object is now
derived: the scalar charged-lepton lane reduces canonically to the two-slot
real-isotype carrier `(+ , perp)` before the log-volume / extremal law is
applied.
**Primary runner:** `scripts/frontier_koide_mru_weight_class_obstruction_theorem.py`

**Status authority and audit hygiene (2026-05-16):**
The audit lane has classified this row `audited_renaming` (claim_type
`positive_theorem`, audit_date 2026-05-05, auditor codex-cli-gpt-5.5,
auditor_confidence high). The verdict accepts the runner's symbolic
algebra — that the unreduced `det(alpha P_+ + beta P_perp) = alpha beta^2`
carries weights `(1, 2)` and the weighted block-log-volume family has
unique stationary leaf `kappa = 2 mu / nu`, that `r_1^2 + r_2^2` is
`SO(2)`-orbit invariant, and that the reduced determinant
`det diag(rho_+, rho_perp) = rho_+ rho_perp` is equal-weight — but flags
that the decisive assertion that the scalar charged-lepton lane must
quotient the ordered doublet frame to a one-radius carrier is
introduced as a carrier choice / definition rather than derived from
an independent axiom or cited retained theorem. The verdict therefore
reads the load-bearing step (`load_bearing_step_class = E`) as
**renaming** of the missing carrier-identification primitive into an
exact-by-definition reduction, not a first-principles closure. Audit
verdict and effective status are set by the independent audit lane
only; nothing in this rigorization edit promotes status. The companion
`KOIDE_MRU_DEMOTION_NOTE_2026-04-20` (retained on main) already
reclassifies this row's MRU route as **supplementary /
alternative-framing support** for operator-side `kappa = 2`, with two
retained independent routes
(`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19` and
`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19`)
carrying the operator-side gate without any `SO(2)`-quotient postulate.

The audit-stated cheapest re-audit path (verbatim from the ledger
`notes_for_re_audit_if_any`):

> Re-check whether a separate retained bridge theorem exists that
> derives the scalar-lane `SO(2)` quotient from the repository's axioms
> rather than defining it locally.

---

## 0. Executive summary

On the `d = 3` cyclic carrier,

```text
E_+    = r_0^2 / 3   = 3 a^2,
E_perp = (r_1^2 + r_2^2) / 6 = 6 |b|^2.
```

For the weighted block-log-volume family

```text
S_{mu,nu} = mu log(E_+) + nu log(E_perp)
```

at fixed `E_tot = E_+ + E_perp`, every interior stationary leaf is

```text
kappa := a^2 / |b|^2 = 2 mu / nu.
```

So:

- MRU is the equal-weight leaf `(mu, nu) = (1,1)`;
- the unreduced determinant carrier

  ```text
  det(alpha P_+ + beta P_perp) = alpha beta^2
  ```

  carries weights `(1,2)` and lands at `kappa = 1`.

That obstruction remains exact.

The resolution is not to dispute that calculation. It is to
derive the carrier reduction the theorem said was missing:

```text
(r_0, r_1, r_2)  ->  (rho_+, rho_perp)
```

with

```text
rho_+^2    = E_+,
rho_perp^2 = E_perp,
```

because the scalar lane quotients the internal `SO(2)` frame of the real
doublet. On that reduced carrier,

```text
det diag(rho_+, rho_perp) = rho_+ rho_perp,
```

so the same log-volume law is equal-weight automatically and lands at MRU.

---

## 1. Setup

On the retained `hw=1` cyclic compression,

```text
H = a I + b C + b^bar C^2,
```

with canonical real cyclic basis

```text
B_0 = I,
B_1 = C + C^2,
B_2 = i (C - C^2).
```

Writing

```text
H = (r_0/3) B_0 + (r_1/6) B_1 + (r_2/6) B_2,
```

the real-trace norms give

```text
||B_0||^2 = 3,
||B_1||^2 = ||B_2||^2 = 6,
```

and therefore

```text
E_+    = r_0^2 / 3 = 3 a^2,
E_perp = (r_1^2 + r_2^2) / 6 = 6 |b|^2.
```

Hence

```text
E_+ = E_perp
<=> a^2 = 2 |b|^2
<=> kappa = 2.
```

---

## 2. Weighted block-log-volume classification

Define

```text
S_{mu,nu}(H) := mu log(E_+) + nu log(E_perp),
```

with `mu, nu > 0`, under fixed total block power

```text
E_+ + E_perp = E_tot.
```

The Lagrange equations give the unique interior stationary point

```text
E_+^*    = mu / (mu + nu) * E_tot,
E_perp^* = nu / (mu + nu) * E_tot.
```

So

```text
E_+^* / E_perp^* = mu / nu,
```

and therefore

```text
kappa = 2 mu / nu.
```

This theorem is exact and unchanged.

---

## 3. The unreduced determinant obstruction

Let `P_+` and `P_perp` be the `C_3` singlet and doublet projectors on the
unreduced `3 x 3` carrier, with ranks `1` and `2`.

Any positive operator that is scalar on these two isotypic blocks has the form

```text
D = alpha P_+ + beta P_perp.
```

Because the non-trivial block has multiplicity `2`,

```text
det(D) = alpha beta^2,
log|det D| = log alpha + 2 log beta.
```

So the unreduced determinant law carries weight pair `(1,2)` and therefore
selects

```text
kappa = 2 * 1 / 2 = 1.
```

That is the exact obstruction:

> no log-volume law applied on the unreduced `3 x 3` isotypic-scalar carrier
> can force MRU.

---

## 4. The exact missing object, now derived

The missing object identified above was:

```text
a retained 1:1 real-isotype measure, or an equivalent canonical reduction to a
two-slot (+, perp) carrier before applying the log-volume / extremal law.
```

The branch now derives it.

The non-trivial real doublet

```text
V_perp = span_R{B_1, B_2}
```

has an internal orthonormal frame freedom

```text
(B_1, B_2) -> (B_1', B_2') = (B_1, B_2) R(theta),
```

under which

```text
(r_1, r_2) -> R(theta) (r_1, r_2)
```

but

```text
r_1^2 + r_2^2
```

is invariant. So the scalar lane does not retain the ordered Cartesian pair
inside the doublet plane. It retains only the doublet radius.

Therefore the exact scalar reduction is

```text
(r_0, r_1, r_2)  ->  (rho_+, rho_perp),
```

with

```text
rho_+    = |r_0| / sqrt(3),
rho_perp = sqrt(r_1^2 + r_2^2) / sqrt(6).
```

Equivalently,

```text
rho_+^2    = E_+,
rho_perp^2 = E_perp.
```

This is the exact retained two-slot real-isotype carrier the earlier theorem
said would be sufficient.

---

## 5. Resolution on the reduced carrier

Apply the same log-volume / extremal law on the reduced carrier

```text
D_red = diag(rho_+, rho_perp).
```

Then

```text
det(D_red) = rho_+ rho_perp,
log|det D_red| = log rho_+ + log rho_perp.
```

At fixed reduced total power

```text
rho_+^2 + rho_perp^2 = E_tot,
```

the unique positive stationary point is

```text
rho_+^2 = rho_perp^2 = E_tot / 2.
```

So

```text
E_+ = E_perp
<=> a^2 = 2 |b|^2
<=> kappa = 2.
```

In other words:

> the obstruction remains exact on the unreduced carrier, but it no longer
> blocks the lane because the branch has now derived the carrier reduction it
> said was missing.

---

## 6. Scientific consequence

The theorem should now be read in two layers:

1. **negative layer:** unreduced determinant multiplicities alone do not force
   MRU;
2. **positive layer:** the scalar charged-lepton lane does not live on that
   unreduced carrier. It lives on the real-isotype quotient, where there are
   only two slots and the log-volume law is exactly the MRU leaf.

So the weight-class obstruction has been converted from a blocker into the
load-bearing explanation of why the quotient step was necessary.

---

## 7. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_mru_weight_class_obstruction_theorem.py
```

The runner now certifies both:

1. the old obstruction on the unreduced `3 x 3` carrier, and
2. the exact real-isotype quotient reduction that resolves it on this branch.

## 8. Audit-conditional perimeter

The internal algebra of this note (Sections 1–6) is what the audit
verdict accepts as internally consistent on the admitted reduced
carrier:

| Internal algebra step | Audit-accepted as internal consistency |
|---|---|
| Real-trace pairing on the cyclic basis `(B_0, B_1, B_2)` (Section 1) | yes |
| `E_+ = r_0^2/3 = 3 a^2`, `E_perp = (r_1^2 + r_2^2)/6 = 6 |b|^2` (Section 1) | yes |
| Weighted family `S_{mu,nu} = mu log E_+ + nu log E_perp` has unique stationary leaf `kappa = 2 mu / nu` (Section 2) | yes |
| `rank(P_+) = 1`, `rank(P_perp) = 2`, and `det(alpha P_+ + beta P_perp) = alpha beta^2` (Section 3) | yes |
| Unreduced weights `(1, 2)` land at `kappa = 1` (Section 3) | yes |
| `r_1^2 + r_2^2` is `SO(2)`-orbit invariant on `V_perp = span_R{B_1, B_2}` (Section 4) | yes |
| Reduced determinant `det diag(rho_+, rho_perp) = rho_+ rho_perp` and equal-weight extremum at `rho_+^2 = rho_perp^2 = E_tot/2` (Section 5) | yes |

The audit-conditional perimeter (i.e. what stays open) is exactly the
load-bearing carrier-identification step:

1. derive that the physical scalar charged-lepton lane must replace
   the ordered Cartesian pair `(r_1, r_2)` on the doublet plane by the
   single radius `rho_perp = sqrt(r_1^2 + r_2^2) / sqrt(6)` from a
   retained upstream theorem rather than introducing the quotient as
   the exact retained two-slot carrier (this is the
   `load_bearing_step_class = E` step the verdict flags as renaming);
2. equivalently, derive that the scalar charged-lepton observable
   principle on `Herm_circ(3)` factors through the `SO(2)`-orbit
   invariant `r_1^2 + r_2^2` rather than the ordered pair
   `(r_1, r_2)`, from a retained framework input.

Until (1)/(2) is supplied, the algebraic result of this note is
exactly the conditional statement: *given* the `SO(2)`-quotient
carrier, the unreduced `(1, 2)` obstruction is converted into the
equal-weight reduced determinant, which lands at `kappa = 2`. That is
a correct conditional theorem on the admitted reduced carrier; it is
not a first-principles closure of the operator-side `kappa = 2` lane.
The companion `KOIDE_MRU_DEMOTION_NOTE_2026-04-20` documents
(Section 1.2) that spectrum-native scalar observables on
`Herm_circ(3)` are **not** `SO(2)`-invariant in general — `tr(H^3)`
and `det(H)` carry an explicit `cos(3 arg b)` channel — so the
`SO(2)` quotient is strictly stronger than "scalar observables are
spectrum-native" and is not a corollary of the retained observable
principle on this branch.

## 9. Path A future work (audit-stated repair target)

To move this row's `audit_status` from `audited_renaming` toward
retained-grade, the audit verdict's repair list requires:

1. a retained upstream theorem that derives the scalar-lane `SO(2)`
   quotient from the repository's axioms rather than defining it
   locally;
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

## 10. Boundaries

This note does **not**:

- modify the parent row's audit-ledger entry;
- promote the parent's `audit_status` from `audited_renaming`;
- derive the scalar-lane `SO(2)` quotient of the non-trivial real
  doublet from retained upstream inputs;
- override the `KOIDE_MRU_DEMOTION_NOTE_2026-04-20` reclassification
  of this row's MRU route as supplementary / alternative-framing
  support;
- close the operator-side `kappa = 2` gate (already carried on main by
  the spectrum-operator bridge and block-total Frobenius routes
  without any `SO(2)`-quotient assumption);
- dispute the unreduced `(1, 2)` weight-class obstruction calculation
  itself, which the audit accepts as exact algebra on the unreduced
  `3 x 3` carrier.

The same audit-named missing bridge theorem also blocks the companion
row `koide_moment_ratio_uniformity_theorem_note_2026-04-19`
(`audited_conditional` for the same `SO(2)`-quotient carrier choice).
