# Koide `Z_3`-Qubit Radian-Bridge No-Go

**Date:** 2026-04-20  
**Lane:** charged-lepton Koide phase `delta = 2/9`  
**Status:** exact no-go on the obvious physical-base Berry / Pancharatnam
closures of the remaining unit bridge. This note does **not** refute the
actual-route statement that, once the physical phase value is given, it is read
as a Berry holonomy on the selected line. It proves the stronger closure claim
is still missing: the retained physical-base Berry geometry does not by itself
force the numerical value `delta = 2/9`.

**Primary runner:** `scripts/frontier_koide_z3_qubit_radian_bridge_no_go.py`
(`PASS=9 FAIL=0`).

---

## 0. Executive summary

After the linking-relation theorem, the live Berry-side gap is very specific:

```text
structural delta = 2/9
```

is already fixed as a **dimensionless** `Z_3` doublet-count ratio at retained
`d = 3`. What remains is the unit bridge that identifies this structural `2/9`
with the physical phase in radians.

This note tests the most natural physical-base candidates for that bridge and
shows they do not close it:

1. the direct one-step Pancharatnam phase on the actual `Z_3` qubit orbit is
   `pi/3`, not `2/9`;
2. the full three-step Bargmann invariant on that orbit has phase `pi`, not
   `2/9`;
3. on the actual selected-line `CP^1` carrier, the tautological Berry
   connection `A = d theta` gives a continuum of endpoint holonomies on the
   first branch, with `2/9` only one interior choice;
4. on the sign-relaxed quotient circle, the flat-holonomy family
   `Hol_t = exp(i 2 pi t)` likewise realizes `2/9` only by choosing `t = 2/3`.

So the remaining open object is now exact and narrow:

```text
derive the physical radian bridge itself,
or derive an equivalent physical-base quantization / endpoint law.
```

---

## 1. The actual `Z_3` qubit carrier

On the actual charged-lepton selected line, the moving physical datum is the
projective `C_3` doublet ray

```text
[1 : e^{-2 i theta}],
```

so a canonical normalized spinor representative is

```text
psi(theta) = (1, e^{-2 i theta}) / sqrt(2).
```

This is the genuine physical-base `Z_3` qubit carrier behind the selected-line
Berry route.

---

## 2. Direct one-step Pancharatnam phase fails

Apply one physical `C_3` step:

```text
theta -> theta + 2 pi / 3.
```

Then the Pancharatnam overlap is

```text
<psi(theta), psi(theta + 2 pi / 3)>
  = (1 + e^{-4 i pi / 3}) / 2
  = (1/2) e^{i pi / 3},
```

so its phase is exactly

```text
gamma_step = pi / 3.
```

If one tries to reduce that directly to a Brannen-style per-element phase by
dividing by `2 pi * 3`, one gets

```text
delta_step = 1 / 18,
```

not `2/9`.

So the direct one-step qubit Pancharatnam phase is not the missing bridge.

---

## 3. Full three-step Bargmann invariant also fails

Take the full `Z_3` orbit

```text
psi(theta), psi(theta + 2 pi / 3), psi(theta + 4 pi / 3).
```

The associated Bargmann invariant is the cyclic product of consecutive
overlaps. The runner verifies its phase is exactly

```text
gamma_orbit = pi
```

for the physical three-step orbit. Reducing that per `C_3` element gives

```text
delta_orbit = 1 / 6,
```

again not `2/9`.

So even the gauge-invariant three-step qubit orbit phase does not close the
radian bridge.

---

## 4. The actual selected-line Berry connection is continuum-valued

On the actual selected line, the theorem stack already shows

```text
A = d theta,
delta(m) = theta(m) - 2 pi / 3
```

on the positive first branch. That is real and useful, but it does not by
itself force the value `2/9`. The runner checks that:

- `delta(m)` is continuous and strictly monotone on the first branch;
- its range is an interval containing `2/9`;
- nearby target values pick nearby but distinct first-branch points.

So the physical selected-line Berry connection supplies the correct **carrier**
for the phase, but not its numerical value. The number `2/9` is one interior
endpoint choice on a continuum, not a discrete consequence of the connection
alone.

This is the precise honest split:

- the selected-line Berry theorem identifies **what kind of observable** the
  phase is;
- it does not, by itself, derive **which value** on that continuum is
  physical.

---

## 5. Flat-holonomy family remains non-unique

The sign-relaxed quotient-circle route already carried a flat-holonomy family

```text
Hol_t = exp(i 2 pi t),
delta(t) = t / 3.
```

Here `t = 2/3` realizes `delta = 2/9`, but nearby `t` values realize nearby
non-equal phases. So this auxiliary route is still a choice family, not a
forcing theorem.

---

## 6. Scientific consequence

This note narrows the Koide phase frontier further:

- the old ambient-`S^2` / monopole package is not the actual theorem on the
  physical base;
- the actual selected-line Berry carrier is real, but continuum-valued;
- the obvious direct `Z_3` qubit orbit phases do not equal `2/9`.

So the remaining live object is now explicit:

```text
one radian bridge / Wilson-line quantization / endpoint law
```

that identifies the structural `2/9` with the physical phase observable on the
actual base.

That is a smaller and cleaner gap than the old "derive Berry somehow" wording.

---

## 7. Runner summary

`scripts/frontier_koide_z3_qubit_radian_bridge_no_go.py` verifies:

- the one-step Pancharatnam phase on the physical `Z_3` qubit orbit is
  `pi/3`;
- its direct Brannen-style reduction gives `1/18`, not `2/9`;
- the full three-step Bargmann invariant has phase `pi`;
- its per-element reduction gives `1/6`, not `2/9`;
- the actual selected-line Berry offset runs through a continuum containing
  `2/9`, so the connection alone does not pick that value;
- the flat-holonomy family on the sign-relaxed quotient likewise realizes
  `2/9` only by choice.
