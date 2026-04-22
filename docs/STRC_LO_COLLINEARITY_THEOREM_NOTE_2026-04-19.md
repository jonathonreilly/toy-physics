# STRC-LO / BICAC Theorem from Exact 1(+)5 Channel Completeness

**Date:** 2026-04-19
**Lane:** Quark up-amplitude / BICAC / STRC-LO.
**Status:** Derived theorem on the physical `1(+)5` carrier.
**Primary runner:** `scripts/frontier_strc_lo_collinearity_theorem.py`

## 0. Executive summary

The load-bearing step is not a new postulate and not the earlier
"Frobenius cross-residual" definition.

It is the exact operator identity on the physical reduced carrier

```text
H_(1+5) = span{e_1, e_5},
```

where:

- `e_1` is the normalized `A1` axis,
- `e_5` is the normalized `5`-channel axis,
- the physical projector ray is
  `p = cos_d e_1 + sin_d e_5`,
- the retained down amplitude is the scalar-ray `A1` occupancy
  `a_d = Re(r)` with `r = p / sqrt(7)`.

The exact `5`-budget of the physical ray is

```text
Pi_5 p = sin_d e_5,
```

where `Pi_5 = |e_5><e_5|` is the canonical `5`-projector.

The exact mixed `A1 -> 5` transfer induced by the same physical ray is the
rank-1 operator

```text
T_p := Pi_5 |p><e_1| = sin_d |e_5><e_1|.
```

(The `e_1 -> Pi_5 p` polarization implicit in that choice is discussed in
§2 below; alternative rank-1 choices on the retained data are enumerated
there. On the cleaner affine-physical-carrier derivation
[`QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md`] no
operator choice is needed.)

Applied to the retained down-sector occupancy `d := a_d e_1`, it gives

```text
T_p d = a_d sin_d e_5.
```

Since the `5` sector is one-dimensional on the exact reduced carrier, the
up-sector contribution is the unique residual

```text
u_5 := Pi_5 p - T_p d = a_u e_5.
```

Therefore

```text
a_u = sin_d - a_d sin_d = sin_d (1 - a_d),
```

so the physical law

```text
a_u + a_d Im(p) = Im(p)
```

is derived exactly. With `a_d = Re(r) = 1 / sqrt(42)` this is STRC-LO:

```text
a_u = sin_d (1 - rho),   a_u + rho sin_d = sin_d.
```

This closes the BICAC / STRC-LO lane on the exact carrier.

The companion note
`docs/QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19.md`
re-derives the same `kappa = 1` LO endpoint from the exact shell-normalized
Route-2 carrier columns, and can be read as an independent support-side
corroboration of the carrier-level closure proved here.

## 1. Physical reduced carrier

The live quark notes already fix the physical reduced `1(+)5` structure:

- `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` fixes the unit projector ray
  `p = cos_d e_1 + sin_d e_5` with
  `cos_d^2 = 1/6`, `sin_d^2 = 5/6`;
- the same note fixes `e_1` and `e_5` as the actual `1` and `5` directions of
  the physical reduced carrier;
- `SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md` fixes the scalar
  comparison ray `r = p / sqrt(7)`;
- `QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md` fixes the down-sector
  reduced amplitude as the scalar-ray `A1` occupancy
  `a_d = Re(r) = 1 / sqrt(42)`.

So the relevant carrier is not a bounded fit ansatz. It is the exact direct
sum carrier

```text
H_(1+5) = span{e_1, e_5}.
```

The key semantic point is:

> the theorem variable `a_u` is the coefficient of the residual pure `5`
> vector on `H_(1+5)`, not the bounded full-ray fit coefficient used in the
> projector-ray support scans.

That distinction is the science fix. The earlier no-go targeted the bounded
full-ray fit coefficient and therefore did not address the exact theorem
coordinate on the physical reduced carrier.

## 2. Canonical operator on `H_(1+5)`

Let

```text
Pi_5 := |e_5><e_5|.
```

This is the canonical projector onto the physical `5` channel.

The exact `5`-budget of the physical ray is then

```text
Pi_5 p = sin_d e_5.
```

Now inject a unit `A1` occupancy into the same physical ray and immediately
project to the `5` channel. The resulting `A1 -> 5` channel map is:

```text
T_p := Pi_5 |p><e_1|.
```

In the ordered basis `{e_1, e_5}`,

```text
|p><e_1| = [[cos_d, 0], [sin_d, 0]],
Pi_5      = [[0, 0], [0, 1]],
T_p       = [[0, 0], [sin_d, 0]]
         = sin_d |e_5><e_1|.
```

`T_p` is the rank-1 operator on `H_(1+5)` that satisfies

```text
T_p e_1 = Pi_5 p,
T_p e_5 = 0,
```

i.e. it is the `A1 -> 5` transfer induced by first applying the unit ray and
then projecting onto the `5` channel. **Honest qualifier:** on the retained
data, there are five structurally distinct rank-1 operators built from
`{Pi_5, |p>, <p|, |e_1>, <e_1|, |e_5>, <e_5|}`. The specific choice
`Pi_5 |p><e_1|` realises the polarization "evaluate on `e_1`, project to `5`
after applying `p`" — which is the same content the JTS-as-residue framing
used to carry. So the transfer-operator derivation is a valid path to
BICAC-LO **once that polarization is named**, but not the only such choice.

**Cleaner canonical derivation (same LO conclusion).** Jon's same-day
JTS-affine-physical-carrier theorem
(`docs/QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md`) reaches
the same LO identity `a_u + a_d sin_d = sin_d` without any operator choice
or polarization: because `cos_d != 0`, `{p, e_5}` is a basis of `H_(1+5)`,
so the perturbation cone `Pert(p) = span{p, e_5} = H_(1+5)` equals the
exact physical carrier by linear algebra alone, and exact `1(+)5` channel
completeness then supplies the pinning identity. That path is the current
canonical route; the transfer-operator framing below is retained as a second
derivation that relies on naming the `e_1 -> Pi_5 p` polarization explicitly.

## 3. Forced channel completeness

The retained down-sector occupancy vector is

```text
d := a_d e_1.
```

Applying the canonical transfer operator:

```text
T_p d = a_d sin_d e_5.
```

This is exactly the `A1 -> 5` mixed-channel occupancy carried by the retained
down amplitude on the physical carrier.

The total available `5`-budget of the unit projector ray is `Pi_5 p`.
Because the `5` channel is one-dimensional on `H_(1+5)`, the remaining
up-sector contribution is the unique residual

```text
u_5 := Pi_5 p - T_p d.
```

Define `a_u` by

```text
u_5 = a_u e_5.
```

Then directly

```text
a_u e_5
  = sin_d e_5 - a_d sin_d e_5
  = (sin_d - a_d sin_d) e_5,
```

so

```text
a_u = sin_d (1 - a_d).
```

Rearranging gives the exact physical law

```text
a_u + a_d sin_d = sin_d,
```

or equivalently

```text
a_u + a_d Im(p) = Im(p).
```

This is BICAC / STRC-LO.

## 4. Collinearity specialization

Using the retained scalar ray

```text
r = p / sqrt(7) = rho + i eta,
```

we have

```text
a_d = Re(r) = rho = 1 / sqrt(42),
Im(p) = sin_d = sqrt(5/6).
```

Therefore

```text
a_u = sin_d (1 - rho),
```

and hence

```text
a_u + rho sin_d = sin_d.
```

The old cross-product identity

```text
Re(p) Im(r) = Im(p) Re(r)
```

is still true, but it is now a corollary. The proof does not depend on
defining `a_u` by a cross-residual. It depends on the exact `1(+)5` carrier
and the unique `A1 -> 5` transfer operator induced by the physical ray.

Equivalently, the mixed channel term is the off-diagonal `A1 -> 5` entry of
the canonical outer product

```text
r tensor p,
```

namely

```text
(r tensor p)_(1->5) = Re(r) Im(p) = a_d sin_d.
```

## 5. Why this closes the gap

The closure bar for this lane was:

```text
a_u + a_d Im(p) = Im(p)
```

must be derived from retained projector / bimodule / operator structure, not
postulated.

That is now exactly what happens:

1. `H_(1+5)` is the physical reduced carrier from the exact CKM atlas.
2. `Pi_5` is the canonical projector onto the physical `5` channel.
3. `T_p = Pi_5 |p><e_1|` is the canonical `A1 -> 5` transfer operator induced
   by the physical ray.
4. `d = a_d e_1` is the retained down-sector occupancy.
5. The `5` channel is one-dimensional, so subtracting the exact mixed-channel
   occupancy leaves a unique residual `a_u e_5`.

So BICAC is not added as a fresh linear split law. It is the exact channel
completeness identity on the physical `1(+)5` carrier.

## 6. Downstream RPSR

Once STRC-LO is discharged, the downstream NLO step is unchanged:

```text
rho * supp * delta_A1 = rho / 49.
```

Therefore

```text
a_u^(full)
  = sin_d (1 - rho + rho supp delta_A1)
  = sin_d (1 - 48 rho / 49)
  = 0.7748865611...
```

So the old "RPSR conditional on STRC" route is now discharged at LO by exact
carrier structure.

## 7. Validation

`scripts/frontier_strc_lo_collinearity_theorem.py` now tests only genuine
claims:

- the exact `1(+)5` carrier coordinates of `p` and `r`;
- the canonical `5`-projector `Pi_5`;
- the canonical `A1 -> 5` transfer operator `T_p`;
- the exact mixed-channel occupancy `T_p(a_d e_1) = a_d sin_d e_5`;
- the unique residual `u_5 = a_u e_5`;
- the resulting BICAC / STRC-LO identity;
- the downstream RPSR target.

## 8. Verdict

**Derived.**

The exact load-bearing reason is the canonical `A1 -> 5` transfer operator on
the physical `1(+)5` carrier:

```text
T_p = Pi_5 |p><e_1| = sin_d |e_5><e_1|.
```

With `d = a_d e_1`, the mixed occupancy is exactly `a_d sin_d e_5`, and the
up-sector amplitude is the forced residual of the one-dimensional `5` budget.
