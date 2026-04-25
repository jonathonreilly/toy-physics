# Koide Q Lie/Clifford Radius-Map No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the Lie-theoretic,
Clifford-dimension, and Casimir-difference support routes but does not close
charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_lie_clifford_radius_map_no_go.py`

---

## 1. Theorem Attempt

The A1 support stack has several exact structural hits:

```text
dim(spinor)/dim(Cl+(3)) = 2/4 = 1/2,
|omega_{A1,fund}|^2 = 1/2,
T(T+1) - Y^2 = 1/2
```

for the retained lepton/Higgs `SU(2)_L` doublet data.

The tempting closure upgrade is:

> these retained constants force the charged-lepton circulant radius
> `|b|^2/a^2 = 1/2`.

The executable result is negative.

The constants are exact support. They do not by themselves define the map from
gauge/Clifford data into the generation-cyclic amplitude radius.

---

## 2. Radius Coordinate

For the charged-lepton circulant amplitude

```text
Y = a I + b C + bbar C^2,
```

write:

```text
x = |b|^2/a^2.
```

Then:

```text
c^2 = 4x,
Q(x) = 1/3 + 2x/3.
```

The Koide leaf is:

```text
x = 1/2
<=> c^2 = 2
<=> kappa = 2
<=> Q = 2/3.
```

---

## 3. What The Structural Constants Prove

The runner verifies exactly:

```text
dim(spinor)/dim(Cl+(3)) = 1/2,
|omega_{A1,fund}|^2 = 1/2,
T(T+1)-Y^2 = 1/2,
T(T+1)+Y^2 = 1.
```

These are strong structural coincidences. They remain useful evidence for the
candidate primitive.

---

## 4. What They Do Not Prove

If a gauge, Clebsch, Clifford, or Casimir factor enters as a scalar factor
common to the charged-lepton Yukawa matrix, then:

```text
|g b|^2 / |g a|^2 = |b|^2/a^2.
```

So any common retained factor cancels from the generation-space radius.

Likewise, the standard `SU(2)_L` Yukawa contraction is generation-blind:

```text
y_{alpha beta} L_alpha H e_{R,beta}.
```

The same `L.H -> singlet` contraction multiplies every generation pair
`(alpha,beta)`. It does not distinguish the diagonal `a` term from the cyclic
off-diagonal `b` term.

Thus a closure needs an extra theorem saying that the gauge/Clifford scalar
acts differently on the generation-cyclic blocks.

---

## 5. Exact Countermaps

Let the structural scalar be:

```text
s = 1/2.
```

Different maps from that scalar to the amplitude radius give different exact
`Q` values:

```text
x = s   -> Q = 2/3
x = s/2 -> Q = 1/2
x = 2s  -> Q = 1
x = s^2 -> Q = 1/2
```

Only the map

```text
x = s
```

closes Koide. The retained constants alone do not choose that map.

Equivalently, the same structural constants remain unchanged while the
generation radius varies:

```text
x = 1/4 -> c^2 = 1, Q = 1/2
x = 1/2 -> c^2 = 2, Q = 2/3
x = 1   -> c^2 = 4, Q = 1
```

---

## 6. Review Consequence

The Lie/Clifford/Casimir route proves:

```text
retained structure contains natural constants equal to 1/2.
```

It does not prove:

```text
charged-lepton generation radius |b|^2/a^2 equals that constant.
```

That missing equality is exactly a generation-sensitive radius-map primitive:

```text
generation_sensitive_radius_map
equiv |b|^2/a^2 = 1/2
equiv c^2 = 2
equiv K_TL = 0.
```

---

## 7. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_lie_clifford_radius_map_no_go.py
```

Result:

```text
PASSED: 11/11
KOIDE_Q_LIE_CLIFFORD_RADIUS_MAP_NO_GO=TRUE
Q_LIE_CLIFFORD_CONSTANTS_CLOSE_Q=FALSE
RESIDUAL_PRIMITIVE=generation_sensitive_radius_map_equiv_c^2=2_equiv_K_TL=0
```

No PDG masses, `K_TL = 0`, `K = 0`, `P_Q = 1/2`, `Q = 2/3`,
`delta = 2/9`, or `H_*` observational pin is used.

---

## 8. Boundary

This note does not demote:

- the Lie-theoretic triple match;
- the Clifford dimension-ratio identity;
- the Casimir-difference support route.

It rejects only the stronger claim that those scalar matches already derive
the charged-lepton generation-space radius law.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0` or an
  equivalent retained radius/source/map theorem;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
