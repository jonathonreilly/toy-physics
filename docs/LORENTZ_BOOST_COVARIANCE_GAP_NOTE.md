# Lorentz Boost-Covariance Gap Note

**Date:** 2026-04-25
**Status:** retained scope-clarification note for the emergent-Lorentz lane
**Companions:**
[EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md),
[LORENTZ_VIOLATION_DERIVED_NOTE.md](LORENTZ_VIOLATION_DERIVED_NOTE.md),
[LIGHT_CONE_FRAMING_NOTE.md](LIGHT_CONE_FRAMING_NOTE.md)

## 1. Why this note exists

The emergent-Lorentz program on `Cl(3)/Z^3` currently retains a
**dispersion-isotropy** theorem and a Planck-suppressed dim-6 cubic-harmonic
LV bound. That is a statement about the *on-shell relation* `E^2(p)`. It is
**not** a statement about the **boost-covariance of correlators**.

This note pins the scope precisely so the next round of work knows which
target is open, which propagator object is on the retained surface, and what
the minimal non-trivial extension looks like.

## 2. What is already retained

### 2.1 Dispersion isotropy (retained theorem)

`EMERGENT_LORENTZ_INVARIANCE_NOTE.md` (37/37 PASS) proves, on the
single-component staggered/Laplacian construction:

- The staggered dispersion is `E^2 = (1/a^2) sum_i sin^2(p_i a)`.
- Taylor-expanding gives `E^2 = p^2 - (a^2 / 3) sum_i p_i^4 + O(a^4 p^6)`
  for the fermion (`-a^2 / 12` for the bosonic Laplacian).
- The leading non-isotropic correction is dim-6, CPT-even, P-even, and
  carries the unique `O_h` cubic harmonic at `l = 4`:
  `K_4 = Y_{40} + sqrt(5/14) (Y_{4,4} + Y_{4,-4})`.
- On the retained hierarchy surface `a ~ 1/M_Pl`, the correction is
  suppressed by `(E / M_Pl)^2`.

The SO(3) "spatial isotropy of the leading dispersion" piece is closed.

### 2.2 CPT and P (retained, exact)

`CPT` and `P` are exact on even periodic `Z^3`. This already forbids:

- all CPT-odd SME coefficients (`a_mu`, `b_mu`, `e_mu`, `f_mu`, `g_{lmn}`);
- all dim-3 LV operators (`CPT`-odd, mass-like);
- all dim-5 LV operators (`P`-odd).

So the leading allowed lattice LV operator is necessarily dim-6.

### 2.3 Light-cone framing (retained)

`LIGHT_CONE_FRAMING_NOTE.md` reaffirms the standard lattice-QFT posture:

- no lattice field theory has a strict `v = 1` light cone at finite `a`;
- the Lieb-Robinson cone is the discretization artifact;
- in the continuum (massless) limit `v_g -> 1` is recovered from the
  staggered dispersion.

`LATTICE_NN_LIGHT_CONE_NOTE.md` explicitly retires any emergent-relativity
reading of the NN cone; only the topological causal-bound reading is kept.

## 3. What is NOT yet covered

### 3.1 Boost covariance of the path-sum 2-point function

The dispersion theorem constrains `E^2(p)` only. The continuum-limit
2-point Wightman function

```text
W(Delta_t, Delta_x) = <phi(Delta_t, Delta_x) phi(0, 0)>
```

is *not* directly determined by the on-shell `E(p)` in the absence of an
independent positive Lorentz-invariant spectral measure.

In a continuum free-field theory the Kallen-Lehmann representation forces
`W` to depend only on the invariant interval `s^2 = Delta_t^2 - Delta_x^2`
(and on the `i epsilon` prescription). On a `Z^3 x Z` lattice the
microscopic spectral measure is only `O_h x time-translation`-invariant; the
SO(3,1) covariance of `W` in the continuum limit is therefore an additional
claim that does not follow from dispersion isotropy alone.

The open question is:

> Does `lim_{a -> 0} W_lat(Delta_t, Delta_x; a)` depend only on
> `s^2 = Delta_t^2 - Delta_x^2`?

This is what we mean by **"boost covariance of the 2-point function"**, as
distinct from "dispersion isotropy".

### 3.2 Time-space normalisation

The `Z^3` cubic dispersion is symmetric in the three spatial axes by `O_h`,
but the *time direction* is treated by a separate construction (e.g.
`Z^3 x Z` with a forward-time edge weight) and there is no microscopic
symmetry that mixes time and space. Boost covariance requires the time
and space lattice spacings to combine in the continuum into a single SO(3,1)
metric -- a normalisation question the dispersion theorem does not address.

In lattice units the staggered fermion already gives `v_max = 1` in the
massless limit, so the normalisation is not free, but the *exact* statement
that the continuum spacetime metric is Minkowski has not been written
down as a theorem on this surface.

### 3.3 Which propagator is on the retained surface?

This is a critical scoping question. The retained dispersion theorem
operates on the **staggered/Laplacian** construction:

- `frontier_emergent_lorentz_invariance.py` uses the staggered Hamiltonian
  `H_{xy} = (1/2) sum_mu eta_mu(x) [delta_{x+mu, y} - delta_{x-mu, y}]`,
  whose squared spectrum is the staggered dispersion.

The directional path measure of
`ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`,

```text
amplitude(edge) = exp(i k S_spent) / L^p * exp(-beta theta^2),
```

with `beta = 0.8` chosen empirically and `theta` an extrinsic edge angle,
is a **different object**. It is the unitary core used in the directional
gravity / decoherence stack, not the object on which the dispersion theorem
is proved. The boost-covariance question for **that** kernel is logically
separate and additionally needs `beta` either derived from primitives or
declared an imported parameter (see Phase 3 below).

### 3.4 `frontier_local_unitary_propagator.py`

This is the brick-wall beam-splitter unitary, also distinct from both the
staggered dispersion construction and the directional-measure construction.
It is included in the unification surface
(`PROPAGATOR_FAMILY_UNIFICATION_NOTE.md`) but its boost behaviour is not
on the retained claim surface.

## 4. The minimal non-trivial open case (1+1D)

The cleanest non-trivial test of "boost covariance from a discrete causal
DAG" is **1+1D SO(1,1)**:

- Lattice: `Z^2 = Z_t x Z_x`, lattice spacing `a` in both directions.
- Causal restriction: each edge `(t, x) -> (t', x')` requires
  `t' = t + 1` and `|x' - x| <= 1` (light-cone restricted; Margolus-style
  partition or staggered).
- Path sum: free scalar / staggered fermion two-point function
  `W_lat(Delta_t, Delta_x; a, m)` constructed from the lattice momentum
  integral

  ```text
  W_lat = integral dp/(2*pi) * exp(-i E_lat(p) Delta_t + i p Delta_x)
                                   / (2 E_lat(p))
  ```

  with `E_lat^2(p) = m^2 + (4/a^2) sin^2(p a / 2)` for the bosonic case
  and `E_lat^2(p) = m^2 + (1/a^2) sin^2(p a)` for the staggered fermion.

- Continuum limit: `a -> 0` with `(Delta_t, Delta_x, m, p)` in physical
  units. Standard lattice QFT gives
  `W_lat -> W_cont(Delta_t, Delta_x, m)`.

- **Open structural claim:** `W_cont` depends on `(Delta_t, Delta_x)` only
  through `s^2 = Delta_t^2 - Delta_x^2` and is therefore SO(1,1)-covariant.

There is no rotation group in 1D, so the only emergent symmetry to prove is
the boost. This isolates the boost question cleanly from the cubic-harmonic
dispersion question and is the natural Phase 2 target.

The 1+1D case is structurally non-trivial because:

1. The lattice has a microscopic preferred frame (the row direction).
2. The lattice dispersion `E_lat(p)` is **not** of the relativistic form at
   finite `a` (it has lattice corrections at `O(a^2 p^4)` in the bosonic
   case and `O(a^2 p^4)` in the fermionic case).
3. SO(1,1) acts on `W_cont` as a non-compact transformation that mixes
   time and space, so it cannot be implemented by any finite lattice
   automorphism.

The claim being proved is that despite (1)-(3), the continuum limit
recovers full SO(1,1) covariance.

## 5. Could the dispersion theorem already imply boost covariance?

This is the audit's "stop early if implicit closure" branch.

The Kallen-Lehmann theorem states that a Lorentz-invariant local positive
spectral measure forces the 2-point function to be Lorentz-invariant. The
spectral measure of a free lattice scalar is

```text
rho(s) = integral d^d p / (2 pi)^d * delta(s - E_lat(p)^2 + p^2)
        + (lattice-induced terms),
```

i.e. it is supported on the dispersion shell.

The dispersion theorem proves the leading shell is at
`s = m^2 + p^2 - p^2 = m^2`, i.e. relativistic, plus an `O(a^2 p^4)`
correction. **In the strict continuum limit**, the spectral measure becomes
the Lorentz-invariant Kallen-Lehmann measure of a free relativistic scalar,
and a textbook result then implies the 2-point function depends only on
`s^2`.

However, this argument requires explicit verification:

- **Positivity** of the lattice spectral measure must be checked (staggered
  fermions have known sign-flip patterns; the bosonic Laplacian is positive
  by construction).
- **Convergence** of the lattice 2-point function to the continuum 2-point
  function as `a -> 0` is a non-trivial analytic statement (uniform on
  compact subsets of `s^2 != 0`, with care at the light cone).
- **Time direction** is treated identically to the spatial directions in
  the abstract Wightman construction, but on the lattice the time direction
  is **not** part of the staggered Hamiltonian; it is an additional
  evolution direction with its own continuum limit.

So the implicit-closure reading is "almost there" but not formally written
on the retained claim surface, and the time-direction normalisation issue
in particular needs an explicit statement.

The honest read is therefore:

> The dispersion theorem makes boost covariance of the continuum 2-point
> function **plausible by Kallen-Lehmann**, but does not by itself provide
> a formally retained theorem. Phase 2 lands the explicit 1+1D theorem.

## 6. Specific boost-covariance statement that remains open

The minimal open theorem to prove is:

> **Theorem (target, 1+1D):**
> Let `W_lat(Delta_t, Delta_x; a, m)` be the free staggered or Laplacian
> 2-point function on `Z_t x Z_x` with lattice spacing `a` and bare mass
> `m`. Then in the continuum limit `a -> 0` with `(Delta_t, Delta_x, m)`
> held fixed in physical units,
>
> ```text
> W_lat(Delta_t, Delta_x; a, m)
>     -> W_cont(s^2; m),       s^2 = Delta_t^2 - Delta_x^2,
> ```
>
> i.e. the limit depends on `(Delta_t, Delta_x)` only through the SO(1,1)
> invariant interval `s^2`.

The 3+1D version of the same statement (with full SO(3,1) covariance) is
the Phase 4 target and is conditional on Phase 3 closing the angular-kernel
question.

## 7. Phase 3 dependency: angular kernel structure

In 3+1D the boost question is entangled with two further structural
questions:

1. The dispersion theorem is on the staggered/Laplacian construction. The
   gravity-card directional path measure has a **separate** angular kernel
   `exp(-beta theta^2)` with empirical `beta = 0.8` (see
   `ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`, "Next work" item 3).
   That kernel is not on the dispersion-theorem surface; if any 3+1D boost
   claim invokes it, the empirical `beta` becomes a load-bearing input.
2. The cubic-harmonic dim-6 LV operator is only a *leading-order* statement.
   Higher-order LV terms can mix into the 2-point function through the
   spectral integral; these need to be tracked or shown to die in the
   continuum limit at the same rate as the leading term.

A clean Phase 3 either (a) derives the angular kernel form from retained
primitives (Cl(3) trace structure, action extremization, isotropy
restoration) so `beta` becomes structural, or (b) proves a no-go that
pins the missing axiom. Either outcome unlocks Phase 4.

## 8. What this note does not claim

This note is a **scope clarification**, not a new theorem. It does not:

- weaken the dispersion theorem (it stands as proved);
- claim a new positive boost-covariance result;
- supersede any retained note;
- declare the framework Lorentz-non-covariant beyond what is already known
  (octahedral spatial symmetry at the lattice scale).

It simply pins the precise statement that is open and identifies the
1+1D toy as the natural first non-trivial target.

## 9. Relation to causal-set Lorentz program

Causal-set theory (Bombelli-Lee-Meyer-Sorkin 1987; Bombelli-Henson-Sorkin
2009 theorem) achieves Lorentz invariance at the lattice scale by
**Poisson-sprinkling** points into Minkowski spacetime, so no preferred
frame exists microscopically. This is qualitatively different from the
`Z^3` framework, where octahedral symmetry is microscopic and Lorentz
invariance is *emergent* in the continuum limit only.

Both programs converge on the same continuum statement (Lorentz-covariant
correlators) but via different mechanisms:

| Program             | Microscopic symmetry | Continuum mechanism            |
|---------------------|----------------------|--------------------------------|
| Causal sets (BHS)   | none (Poisson)       | sprinkling theorem             |
| `Cl(3)/Z^3` (here)  | `O_h` cubic         | dispersion isotropy + suppression |

The Phase 2 1+1D theorem in this lane is the lattice analogue of the
causal-set sprinkling result, but in the framework's native discrete-graph
setting rather than via random sprinkling.

## 10. Summary table

| Object                                  | Retained? | Boost-covariant in continuum? |
|-----------------------------------------|-----------|--------------------------------|
| Staggered dispersion `E^2(p)`           | Yes       | dispersion-level only         |
| Cubic-harmonic dim-6 LV bound           | Yes       | bound, not derivation         |
| 1+1D path-sum 2-point function          | No        | open (Phase 2 target)         |
| 3+1D staggered 2-point function         | No        | open (Phase 4 target)         |
| Directional kernel `exp(-beta theta^2)` | Provisional | open, `beta` not derived    |
| `frontier_local_unitary_propagator.py`  | Companion | not on this lane              |

Phase 2 lands the 1+1D row.
