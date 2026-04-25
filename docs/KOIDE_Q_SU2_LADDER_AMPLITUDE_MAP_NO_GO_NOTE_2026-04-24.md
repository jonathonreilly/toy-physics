# Koide Q SU(2) Ladder-Amplitude Map No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This audits the charged-current
`SU(2)_L` ladder half-strength route and rejects it as a Koide closure without
a retained cross-basis amplitude-map theorem.
**Primary runner:** `scripts/frontier_koide_q_su2_ladder_amplitude_map_no_go.py`

---

## 1. Theorem Attempt

The strongest charged-current variant is:

> the charged lepton sits in an `SU(2)_L` doublet, and the transverse ladder
> Casimir remainder is exactly `1/2`. Perhaps retained electroweak embedding
> maps this half-strength to the cyclic amplitude ratio
> `rho = |b|^2/a^2`, closing `Q`.

The executable result is negative. The half-strength is exact support, but
the map from `SU(2)_L` ladder data to the `C_3` cyclic amplitude radius is not
currently retained.

---

## 2. Exact Support Arithmetic

For the charged-lepton member of a weak doublet:

```text
T = 1/2,
T_3 = -1/2.
```

Therefore:

```text
T(T+1) = 3/4,
T_3^2 = 1/4,
T(T+1) - T_3^2 = 1/2.
```

If the cyclic amplitude map were supplied:

```text
rho = |b|^2/a^2 = 1/2,
```

then:

```text
Q = 2/3,
K_TL = 0.
```

---

## 3. Why This Does Not Close Q

Several exact electroweak scalars are available:

```text
charged ladder C2 - T3^2 = 1/2 -> Q = 2/3
hypercharge square         = 1/4 -> Q = 1/2
neutral T3 square          = 1/4 -> Q = 1/2
total SU2 plus Y           = 1   -> Q = 1
```

Only the charged-ladder scalar lands on Koide. Selecting it as the cyclic
amplitude ratio is the missing theorem:

```text
rho_amp = T(T+1) - T3^2.
```

The retained electroweak embedding does not currently supply that cross-basis
map.

---

## 4. Hostile Review

This route does not import mass-table data, observational pins, `Q = 2/3`,
`P_Q = 1/2`, `delta = 2/9`, or `K_TL = 0` as an assumption. Its failure is:

```text
exact SU(2)_L ladder half-strength
```

but not:

```text
retained theorem mapping ladder half-strength to cyclic amplitude ratio.
```

Without that theorem, the route is support, not closure.

---

## 5. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_su2_ladder_amplitude_map_no_go.py
```

Result:

```text
PASSED: 9/9
KOIDE_Q_SU2_LADDER_AMPLITUDE_MAP_NO_GO=TRUE
Q_SU2_LADDER_AMPLITUDE_MAP_CLOSES_Q=FALSE
RESIDUAL_SCALAR=rho_amp_minus_su2_ladder_half_equiv_K_TL
```

---

## 6. Boundary

This note preserves the `1/2` ladder arithmetic as a strong support clue. It
rejects only the promotion from support to theorem without the retained
amplitude-map bridge.
