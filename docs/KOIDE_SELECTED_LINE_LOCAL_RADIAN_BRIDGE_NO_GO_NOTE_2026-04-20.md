# Koide Selected-Line Local Radian-Bridge No-Go

**Date:** 2026-04-20  
**Lane:** Scalar-selector cycle 1 — sharpened obstruction for the residual
radian-bridge postulate `P`.  
**Status:** **No-go.** On the actual selected-line `CP^1` base, the canonical
local geometric packet is too small to canonically select the interior point
`δ = 2/d²`. The selected-line base is only `1`-real-dimensional, its canonical
Berry packet is almost trivial, and any closure of `P` must therefore be
nonlocal on the branch or add extra Wilson/lattice transport data.  
**Primary runner:**
`scripts/frontier_koide_selected_line_local_radian_bridge_no_go_2026_04_20.py`

---

## 0. Executive summary

The cycle-2 linking theorem and direct no-go already isolate the live open
content of `I2 / P`:

```text
ρ_δ := 2/d²
```

is a retained structural number, while

```text
δ(m) = Hol(m_0 -> m)
```

is the actual selected-line Berry holonomy on the physical `CP^1` carrier.

The remaining question is whether the actual selected-line base itself
canonically identifies

```text
δ(m_*) = ρ_δ.
```

This note proves a sharper negative statement than the existing four-candidate
no-go:

> On the actual selected-line first branch, every intrinsic **local**
> gauge-invariant datum from the canonical tautological geometry is constant,
> while `δ(m)` varies strictly along the branch. Therefore no intrinsic local
> selected-line law built from that geometric packet can select the interior
> point `δ = 2/d²`.

So the residual bridge is not “find a smarter local Berry scalar.” The
remaining live routes must be:

- a **nonlocal** continuation / endpoint / transport law on the actual branch,
- or an **extra retained Wilson/lattice datum** that injects new phase content.

On the repo's physical `3+1` reading, that means the missing content cannot be
intrinsic to the `1`-dimensional selected-line base itself. It has to come from
ambient continuation/transport data or from extra retained `3+1` Wilson/lattice
structure.

---

## 1. The actual selected-line local packet is almost too simple

On the retained actual route, the physical phase carrier is the projective
doublet ray

```text
[e^{iθ} : e^{-iθ}] = [1 : e^{-2 i θ}]
```

on the equator of `CP^1`, with canonical unit section

```text
χ(θ) = (1, e^{-2 i θ}) / √2.
```

So the selected-line base is only `1`-real-dimensional, parameterized by the
Berry angle `θ`.

The tautological Berry connection is

```text
A = i⟨χ, dχ⟩ = dθ.
```

The Fubini-Study line element on the equator is also constant in the same
coordinate:

```text
ds² = dθ².
```

So the canonical local geometric packet on the selected-line carrier is:

```text
(A = dθ,  F = dA = 0,  g_FS = 1)
```

up to the usual gauge/reparameterization conventions.

Meanwhile the structural scalar singled out by the evening support packet is

```text
ρ_δ = |Im(b_F)|² = 2/d²,
```

and on the exact selected line this quantity is branch-constant.

Therefore the full canonical **local** packet available on the actual route is

```text
(F = 0, g_FS = const, ρ_δ = const).
```

This is the clean structural reason the residual bridge is hard: the actual
selected-line local packet is almost featureless.

---

## 2. Why this cannot pick the physical interior point

Let `B_1st` be the physical first branch, parameterized by the Berry coordinate

```text
δ(m) = θ(m) - 2π/3.
```

The branch endpoints are:

- the unique unphased point `m_0`, where `δ = 0`;
- the positivity threshold `m_pos`, where `δ = π/12`.

So the actual physical branch is the interval

```text
δ(B_1st) = [0, π/12].
```

The target value

```text
2/d² = 2/9
```

lies strictly inside that interval:

```text
0 < 2/9 < π/12.
```

At the same time, the runner verifies:

- `δ(m)` is strictly monotone on the first branch;
- `ρ_δ = |Im(b_F)|²` is constant on the first branch;
- the local geometric packet `(F, g_FS)` is constant everywhere on the
  selected-line carrier.

So two distinct interior points `m_a != m_b` can have:

```text
(F, g_FS, ρ_δ)_{m_a} = (F, g_FS, ρ_δ)_{m_b}
```

while

```text
δ(m_a) != δ(m_b).
```

This proves the key obstruction:

> The actual selected-line local packet does not distinguish points along the
> branch. Therefore the equation `δ(m) = 2/d²` is not a local geometric
> identity on the branch; it is an additional point-selection law.

---

## 3. Formal no-go statement

Call a **selected-line local radian-bridge law** any gauge-invariant scalar law
on the actual route built from finitely many local jets of:

- the tautological selected-line Berry geometry, and
- the retained structural scalar `ρ_δ = |Im(b_F)|²`.

Then:

> **Theorem.** No selected-line local radian-bridge law canonically singles out
> the physical interior point `δ = 2/d²` on the first branch.

**Reason.**

1. On the actual selected-line carrier, the local tautological geometry is flat:
   `F = 0`.
2. The equator metric density is constant.
3. The structural scalar `ρ_δ = |Im(b_F)|²` is branch-constant.
4. Hence every local gauge-invariant scalar built from that packet is constant
   along the branch.
5. But `δ(m)` is nonconstant and strict-monotone on the branch.

So the branch point with `δ = 2/d²` cannot be obtained from local selected-line
geometry alone. `square`

Within the repo's `3+1` interpretation, the honest reading is that the missing
phase content must live off this `1`-dimensional local base: in branch-global
continuation, ambient transport, or additional retained Wilson/lattice data.

---

## 4. Consequence for `I2 / P`

This note does **not** refute the dependent evening route

```text
Q -> CPC -> δ.
```

Instead it sharpens what that route must mean if it succeeds:

- it is **not** a local theorem of the actual selected-line Berry packet;
- it must be a **nonlocal** endpoint/continuation law on the branch,
  or a theorem importing extra Wilson/lattice transport data.

That is a narrower and more actionable statement than the earlier
four-candidate no-go alone.

So the honest current split is:

- **Closed:** `δ(m)` is the actual Berry holonomy on the selected-line `CP^1`
  carrier.
- **Still open:** why the physical branch picks the specific interior value
  `δ = 2/d² = 2/9`.
- **New sharpened obstruction:** no intrinsic local law on the actual
  selected-line geometric packet can do that.

---

## 5. What remains worth trying

After this note, the live radian-bridge targets are reduced to:

1. **Nonlocal selected-line continuation law.**
   A branch-global endpoint/transport rule that canonically identifies the
   physical interior point.
2. **Wilson/lattice transport law.**
   A retained physical-base phase identity such as:
   - lattice propagator radian quantum,
   - `4×4 hw=1+baryon` Wilson holonomy,
   - `Z_3` Wilson-line `d²`-power quantization.
3. **Dependent `Q -> CPC -> δ` promotion.**
   The evening support route can still succeed, but only as a genuinely
   nonlocal/structural bridge, not as an intrinsic local selected-line theorem.

That is exactly what one should expect if the framework is fundamentally
physical `3+1`: the local selected-line carrier is too simple to close `P` by
itself, so the remaining live content has to come from the ambient transport
story rather than from a smarter scalar on the line.

---

## 6. Runner summary

The companion runner verifies:

- the canonical equator spinor has `A = dθ`,
- the equator Fubini-Study density is constant,
- the Berry curvature is zero,
- the physical first branch runs from `δ = π/12` to `δ = 0`,
- `2/d² = 2/9` lies strictly inside that interval,
- `δ(m)` is strict-monotone on the branch,
- `|Im(b_F)|² = 2/d²` is constant on the branch,
- two distinct branch points have the same local invariant packet but different
  holonomies.

That is exactly the selected-line-local no-go.
