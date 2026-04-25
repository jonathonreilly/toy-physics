# Koide Q Full-Taste-Carrier Source-Neutral No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the new-physical-carrier
escape hatch but does not close charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_full_taste_carrier_source_neutral_no_go.py`

---

## 1. Theorem Attempt

After the controlled-`C_3` and non-Schur metric audits, the strongest remaining
Q-side escape hatch is:

```text
the physical charged-lepton carrier is not an isolated T_1 target but the full
taste-cube carrier upstream of the Gamma_1 return.
```

The attempted closure upgrade is:

> source neutrality on the full intermediate taste carrier `O_0 + T_2 + O_3`
> forces the normalized first-live second-order Koide source law `K_TL = 0`.

The executable result is negative.

Full taste-cube source neutrality gives the degenerate point. Once the weak
axis is selected, the only nontrivial full-carrier scalar visible to the
first-live return is the `O_0:T_2` ratio, and that ratio is not fixed by
full-carrier neutrality.

---

## 2. Brainstorm And Route Ranking

The cycle surveyed five live variants:

```text
1. full-taste source neutrality on O_0 + T_2 + O_3;
2. all-axis averaging before weak-axis selection;
3. higher-order O_3 return as a source-balancing law;
4. Q-delta bootstrap from the residual identity Q = 3 delta;
5. nonlocal spectral readout beyond the axis/eigenvalue no-go.
```

The full-taste source-neutral route ranked first because it directly attacks
the remaining "new physical carrier" escape hatch and is not a repeat of the
controlled-breaking, non-Schur metric, or eigenvalue-channel audits.

---

## 3. Exact Full-Taste Geometry

On the retained taste cube:

```text
O_0 = {(0,0,0)},
T_1 = {(1,0,0), (0,1,0), (0,0,1)},
T_2 = {(1,1,0), (0,1,1), (1,0,1)},
O_3 = {(1,1,1)}.
```

The retained `C_3[111]` action fixes `O_0` and `O_3` and rotates `T_1` and
`T_2` as three-cycles.

The weak-axis operator `Gamma_1` reaches:

```text
(1,0,0) -> (0,0,0) = O_0,
(0,1,0) -> (1,1,0) in T_2,
(0,0,1) -> (1,0,1) in T_2.
```

The fourth `T_2` state `(0,1,1)` is unreachable at this order, and `O_3` is
not reached by one `Gamma_1` hop from `T_1`.

---

## 4. Full Source Neutrality

A `C_3`-equivariant full intermediate scalar source has independent weights:

```text
u on O_0,
t on T_2,
o on O_3.
```

Pullback through the exact first-live `Gamma_1` return gives:

```text
P_T1 Gamma_1 W_full Gamma_1 P_T1 = diag(u, t, t).
```

The `O_3` weight and the unreachable `T_2` slot drop out exactly.

Full state-neutral source sets:

```text
u = t = o.
```

Then the charged-lepton square-root slots are proportional to:

```text
(1,1,1),
```

and:

```text
Q = 1/3.
```

So full source neutrality does not give the Koide point. It gives the
mass-degenerate axis readout.

---

## 5. The Residual Scalar

Let:

```text
s = sqrt(u/t).
```

Then the full-carrier first-live family gives:

```text
Q(s) = (s^2 + 2)/(s + 2)^2.
```

The Koide leaf is:

```text
Q(s) = 2/3
<=> s^2 - 8s - 2 = 0
<=> s = 4 + 3 sqrt(2)
<=> u/t = 34 + 24 sqrt(2).
```

That exact ratio is not supplied by `C_3` covariance, full taste-cube
neutrality, or `Gamma_1` reachability.

The same full-carrier form realizes inequivalent exact values:

```text
s = 1             -> Q = 1/3
s = 2             -> Q = 3/8
s = 4 + 3 sqrt(2) -> Q = 2/3
s = 10            -> Q = 17/24
```

Only the third line lands on the Koide leaf, and it does so by imposing the
ratio.

---

## 6. Source-Law Reading

On this carrier:

```text
c^2(s) = 6(Q(s) - 1/3).
```

The runner verifies:

```text
c^2(s) - 2 has numerator s^2 - 8s - 2.
```

Thus:

```text
K_TL = 0
<=> c^2 = 2
<=> sqrt(u/t) = 4 + 3 sqrt(2).
```

The full-carrier route has not derived the missing source law; it has renamed
it as an `O_0:T_2` full-carrier ratio law.

---

## 7. Musk Simplification Pass

Requirements made less wrong:

```text
Do not require a theorem about every possible full-carrier readout. Test the
retained first-live Gamma_1 return geometry directly.
```

Deleted structure:

```text
O_3 and the unreachable T_2 slot are irrelevant to the first-live Q law.
```

Simplified proof:

```text
The route reduces to one scalar equation in s = sqrt(u/t).
```

Acceleration:

```text
The decisive check is symbolic: Q(s) = (s^2+2)/(s+2)^2.
```

Automation:

```text
The runner now records this as a reusable no-go for future full-carrier claims.
```

---

## 8. Review Consequence

The full-taste route proves:

```text
the retained full taste-cube carrier can be pulled back exactly through
Gamma_1, and the first-live visible data reduce to an O_0:T_2 ratio.
```

It does not prove:

```text
retained Cl(3)/Z^3 charged-lepton structure -> sqrt(u/t)=4+3sqrt(2).
```

The residual scalar is:

```text
sqrt(u/t)=4+3sqrt(2)
equiv c^2 = 2
equiv K_TL = 0.
```

So this route cannot be promoted as a Koide closeout unless a retained theorem
selects that full-carrier ratio without importing the target.

---

## 9. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_full_taste_carrier_source_neutral_no_go.py
```

Result:

```text
PASSED: 14/14
KOIDE_Q_FULL_TASTE_CARRIER_SOURCE_NEUTRAL_NO_GO=TRUE
Q_FULL_TASTE_SOURCE_NEUTRAL_CLOSES_Q=FALSE
RESIDUAL_RATIO_LAW=sqrt(u/t)=4+3sqrt(2)_equiv_c^2=2_equiv_K_TL=0
```

No PDG masses, `K_TL = 0`, `K = 0`, `P_Q = 1/2`, `Q = 2/3`,
`delta = 2/9`, or `H_*` observational pin is used as an input.

---

## 10. Boundary

This note does not demote:

- the full-lattice Schur-inheritance theorem;
- the exact first-live second-order carrier;
- future higher-order `O_3` audits, which must be treated separately.

It rejects only the stronger claim that full taste-cube source neutrality
itself derives the Koide radius.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0` or an
  equivalent retained radius/source/full-carrier ratio theorem;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
