# Koide Brannen Geometry / Dirac Support Note (2026-04-22)

## Scope

This note records an additional April 22 support layer for the charged-lepton
Brannen lane `δ = 2/9`.

It does **not** claim closure of the physical Brannen-phase bridge. The live
open issue remains:

> why the physical Brannen phase on the actual selected-line `CP^1` carrier is
> the ambient APS / ABSS quantity `η = 2/9`.

What this note adds is narrower and useful:

1. a clean exact geometric interpretation of `δ(m)` on the retained selected
   line;
2. a conditional Route-3 Wilson-line support construction showing how the same
   rational `2/9` can arise from a one-clock natural-time phase law;
3. an explicit finite-lattice Wilson-Dirac illustration on the physical
   `L = 3` carrier, showing recurrence of per-fixed-site `2/9`.

## 1. Exact selected-line geometry

The selected-line Brannen phase can be read as a plain Euclidean rotation
angle of the real Koide amplitude vector in the 2-plane orthogonal to the
singlet axis `(1,1,1)/√3`.

The support runner verifies:

- the perpendicular radius is constant on the first branch;
- the unphased point satisfies `α(m_0) = -π/2` exactly;
- the positivity endpoint satisfies `α(m_pos) - α(m_0) = -π/12` exactly;
- the physical point still satisfies `α(m_*) - α(m_0) = -2/9`;
- the full first-branch span is exactly `π/12 = 2π/|O|` with `|O| = 24`.

This is a real strengthening of the lane. It shows that the selected-line
Brannen value sits inside an exact retained cubic/octahedral geometry rather
than only as an unexplained numerical target.

What it still does **not** prove is that the physical interior point must be
chosen by that geometry alone.

## 2. Conditional Route-3 support

The same runner also verifies the conditional Route-3 Wilson-line relation

```text
W^{d^2} = exp(2i) · 1
```

with `d = 3` and `n_eff = 2`, giving per-step phase `2/d^2 = 2/9`.

This is useful support for the one-clock natural-time route, but it remains
conditional because the load-bearing step is still the physical
identification:

> the one-clock natural-time phase law is the physical radian bridge on the
> selected-line carrier.

That identification is not discharged here and should not be promoted beyond
conditional support.

## 3. Explicit finite-lattice Dirac support

The second runner builds an explicit Euclidean Hermitian `Z_3`-equivariant
Wilson-Dirac operator on the `3 × 3 × 3` cubic lattice.

It verifies:

- Euclidean `Cl(4)` gamma relations on the lattice carrier;
- the body-diagonal `Z_3` spinor action;
- the three fixed body-diagonal sites of the `L = 3` lattice;
- Hermiticity and `Z_3` equivariance of the Wilson-Dirac operator;
- recurrence of per-fixed-site `η = 2/9` at discrete Wilson-parameter
  plateaus;
- exact symbolic ABSS evaluation of `η = 2/9`.

This is best read as a concrete **finite-lattice descent illustration**:
the ambient `2/9` value is not floating abstractly; it appears naturally on a
physical `L = 3` `Z_3` carrier with the right generation count.

What it still does **not** prove:

- that the physical selected-line charged-lepton phase is already this Dirac
  quantity;
- or that the `L = 3` finite-lattice plateaus already give the full
  continuum/regulator-robust theorem.

## 4. Package status after this note

This note strengthens the charged-lepton Brannen lane materially, but it does
not change the public package status:

- `Q = 2/3` remains open on the physical/source-law bridge;
- `δ = 2/9` remains open on the physical Brannen-phase bridge;
- `v_0` remains a separate support lane.

## 5. Artifacts

### Notes

- `docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`

### Runners

- `scripts/frontier_koide_brannen_route3_geometry_support.py`
- `scripts/frontier_koide_brannen_dirac_support.py`

## 6. Bottom line

The real scientific value of this batch is:

- exact selected-line geometry for the Brannen phase;
- a clearly named conditional Route-3 support law;
- a concrete finite-lattice Wilson-Dirac realization of the ambient `2/9`
  value on the physical `L = 3` carrier.

That is worth landing as support science and atlas material. It is not a
closure theorem.
