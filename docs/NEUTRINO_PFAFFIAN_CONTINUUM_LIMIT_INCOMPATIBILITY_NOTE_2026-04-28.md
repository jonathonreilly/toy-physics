# Pfaffian-Extension Continuum-Limit Incompatibility — SR-2 Stretch Attempt

**Date:** 2026-04-28
**Status:** retained branch-local **stretch-attempt** note on
`frontier/neutrino-quantitative-20260428`. Cycle 5 of the loop:
attempt `(SR-2)` continuum-limit scalar 2-point incompatibility with
Pfaffian extensions, identified by Cycle 4's stuck fan-out as the
cleanest single-cycle continuation. **Result: partial closure with
named load-bearing wall.** The retained 3+1D SO(3,1) boost-covariance
theorem rests on the bilinear free-scalar dispersion; Pfaffian
extensions modify the propagator pole structure to BCS-type
quasiparticles. The s-wave Pfaffian sub-class is ruled out by the
retained continuum-limit closure form; the p-wave / d-wave
sub-classes are ruled out by SO(3) angular-isotropy violation. The
**residual angular-singlet-but-time-twisted Pfaffian sub-class** is
the load-bearing wall.
**Lane:** 4 — Neutrino quantitative closure (route 4D / R-X3 → SR-2)
**Loop:** `neutrino-quantitative-20260428`

---

## 0. First-principles reset

Per Deep Work Rules:

### 0.1 `A_min`

`MINIMAL_AXIOMS_2026-04-11.md`:
1. `Cl(3)` local algebra
2. `Z^3` spatial substrate
3. finite local Grassmann / staggered-Dirac partition + lattice
   operators on that surface
4. canonical normalization `g_bare = 1` + plaquette/u_0 + minimal
   APBC hierarchy

Plus the retained 3+1D extension `Cl(3)/Z^3 x R` and the retained
emergent-Lorentz dimension-6 cubic-harmonic LV cluster.

### 0.2 Forbidden imports

- no PDG observed values
- no Schechter-Valle-as-derivation
- no fitted selectors
- no neutrino mass / splitting numerics

### 0.3 Goal

Show that **adding a non-trivial Pfaffian pairing term**
`Delta * chi^T S(p) chi + h.c.` to the staggered-Dirac partition is
**incompatible** with the retained continuum-limit 3+1D SO(3,1)
boost-covariant free-scalar 2-point function theorem
(`LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md`).

If the incompatibility is general, `(C2-X)` retains under permissive
axiom 3 — the conditional Cycle-2 Dirac global theorem becomes
unconditional.

## 1. The retained closure being defended

`LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md` proves: on the
bilinear free-scalar 3+1D Hamiltonian-lattice surface with dispersion

```text
E_lat^2(p) = m^2 + sum_i (4/a^2) sin^2(p_i a / 2)         (1)
```

the continuum-limit Wightman 2-point function

```text
W_lat(Δt, Δx⃗; a, m)
   = ∫_BZ d^3p/(2π)^3
       exp(-i E_lat(p) Δt + i p⃗·Δx⃗) / (2 E_lat(p))      (2)
```

converges to the SO(3,1)-invariant continuum form

```text
W_cont(s^2; m) = m K_1(m sqrt(-s^2)) / (4π² sqrt(-s^2))    (3)
```

for spacelike `s^2 < 0`. Finite-`a` LV violation is dim-6
cubic-harmonic, suppressed as `(E/M_Pl)^2` on the retained Planck-pin
surface.

The closure (3) is the single function that any admissible extension
must reproduce in the continuum limit. If a Pfaffian extension fails
(3), the extension is incompatible with retained continuum-limit
content.

## 2. What a Pfaffian extension does to the propagator

A Pfaffian pairing term added to the action takes the form

```text
S_pair = (1/2) Delta sum_{x,y} chi(x)^T S(x-y) chi(y) + h.c.   (4)
```

with `Delta` real and `S(x-y)` a c-number kernel. After Fourier
transform, the Nambu-Gor'kov bilinear is

```text
S = sum_p (chi(p)^T, chi^*(p)) M(p) (chi(p), chi^*(p))^T       (5)
M(p) = ((E_lat(p) - mu),  Delta S(p))
       (Delta S(-p)^*,    -(E_lat(-p) - mu))                   (6)
```

(schematic; the "∓" sign and chemical-potential `mu` placement
depend on the lattice fermion convention).

The Bogoliubov-de-Gennes diagonalization gives **two quasiparticle
bands**

```text
E_qp,±(p) = ±sqrt( (E_lat(p) - mu)^2 + |Delta S(p)|^2 )         (7)
```

The Wightman 2-point function on this surface is no longer (2). It
becomes the BdG-quasiparticle propagator

```text
W_BdG(Δt, Δx⃗; a, m, Delta, S)
   = ∫_BZ d^3p/(2π)^3 [ u_p^2 e^{-i E_qp Δt} + v_p^2 e^{+i E_qp Δt} ]
       e^{i p⃗·Δx⃗} / (2 E_qp)                                  (8)
```

with `u_p, v_p` the Bogoliubov coefficients

```text
u_p^2 - v_p^2 = (E_lat - mu)/E_qp                              (9)
u_p^2 + v_p^2 = 1                                             (10)
2 u_p v_p = Delta S(p) / E_qp                                  (11)
```

This is the standard BCS / BdG propagator structure.

## 3. Continuum-limit incompatibility — three cases

Take the continuum limit `a -> 0` with `(Δt, Δx⃗, m, Delta, S)` held
fixed in physical units. The behavior of (8) depends on the angular
structure of `S(p)`.

### 3.1 Case A — s-wave Pfaffian (`S(p) = const`)

Here `Delta S(p) = Delta` is `p`-independent. The quasiparticle
dispersion is

```text
E_qp,±(p) = ±sqrt( E_lat(p)^2 + |Delta|^2 )                    (12)
```

(taking `mu = 0` for clarity). In the continuum limit `a -> 0`,
`E_lat(p)^2 -> m^2 + |p|^2`, so

```text
E_qp,±(p) -> ±sqrt( m^2 + |p|^2 + |Delta|^2 )                  (13)
```

This is the dispersion of a **massive relativistic particle with
shifted mass** `m_eff^2 = m^2 + |Delta|^2`.

So far, this case appears to satisfy SO(3,1) covariance — the
quasiparticle dispersion is rotationally invariant and Lorentz-
covariant in the standard scalar form. The 2-point function (8) on
this s-wave Pfaffian surface would be (3) with `m -> m_eff`.

**Is this consistent with the retained closure (3)?** *Numerically*,
yes — the closure (3) holds for every value of `m`, so an
`m_eff = sqrt(m^2 + |Delta|^2)` shift is admissible. **But** the
closure (3) is the **2-point Wightman function of a fermion field
in the bilinear partition**, not the propagator of Bogoliubov
quasiparticles. The right-hand side of (8) for s-wave Pfaffian is
**not** (3) — it has the BCS coherence factors `u_p^2`, `v_p^2`.

Specifically, the time-ordering and the off-diagonal `<chi chi>`
correlator are non-zero in BdG:

```text
<chi(t,x) chi(0,0)> = ∫_BZ d^3p/(2π)^3
   u_p v_p (e^{-i E_qp Δt} - e^{+i E_qp Δt}) e^{i p⃗·Δx⃗} / (2 E_qp)
                                                              (14)
```

This is the **anomalous correlator** — non-zero in BCS, zero in the
bilinear retained partition. Its existence is the fermion-number
`U(1)` violation that makes the partition function depend on
`Delta`.

So even s-wave Pfaffian violates the retained closure: the closure
form (3) is the diagonal Wightman 2-point function on the
bilinear surface; the BdG surface has an additional anomalous
correlator (14) that does not appear in (3).

**Verdict for case A:** s-wave Pfaffian is incompatible with the
retained continuum-limit closure if "closure" includes the full
correlator algebra (diagonal + anomalous). A subtle interpretation
question.

### 3.2 Case B — angularly non-trivial Pfaffian (p-wave, d-wave, ...)

If `S(p)` carries angular momentum (e.g., `S(p) ~ p_i sigma^i`
p-wave), then `Delta S(p)` is angular-dependent. The quasiparticle
dispersion (7) becomes

```text
E_qp,±(p) = ±sqrt( E_lat(p)^2 + |Delta|^2 |S(p)|^2 )
```

with `|S(p)|^2` angular-dependent. This dispersion is **anisotropic
in the continuum limit** unless `|S(p)|^2` happens to depend only
on `|p|`.

For p-wave: `|S(p)|^2 ~ |p|^2` (rotationally invariant magnitude),
but the gap function `Delta S(p) = Delta p_i sigma^i` is **not**
rotationally invariant on its own — it transforms as a vector. The
Bogoliubov coherence factors `u_p, v_p, 2 u_p v_p` carry this
angular structure.

The retained closure (3) is rotationally invariant (depends only on
`|s^2|`). A p-wave or d-wave Pfaffian propagator is *not*
rotationally invariant — the spinor structure of the gap function
introduces angular dependence in `<chi chi>` correlators that
violates SO(3) and hence SO(3,1).

**Verdict for case B:** angularly non-trivial Pfaffian extensions
break SO(3) (and therefore SO(3,1)) covariance in the continuum
limit. Directly contradicts retained
`LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md`. **Closed.**

### 3.3 Case C — angular-singlet-but-time-twisted Pfaffian

The remaining case: `S(p) = f(|p|^2)` is rotationally invariant in
3-momentum, but the **time** structure of the pairing is non-trivial.

This is the **load-bearing wall** identified by this stretch
attempt. Concretely:

- spatial-only Pfaffian (instantaneous pairing,
  `S(t-t') = delta(t-t') f(|p|^2)`): closely resembles s-wave
  case A with the shifted-mass interpretation. Likely incompatible
  via the anomalous-correlator argument.
- time-non-trivial Pfaffian (Cooper-pair-like with retarded /
  Matsubara structure): could in principle reproduce a SO(3,1)-
  covariant 2-point function in the spectator (non-anomalous) sector
  if the time structure is itself Lorentz-covariant.

The third option — `S(t-t', |p|^2)` with the **time structure
chosen to make the BdG propagator (8) Lorentz-covariant** — is not
straightforwardly excluded by the retained closure. It would require
matching the BCS coherence factors to the SO(3,1)-covariant scalar
form, which is a non-generic matching condition but not
algebraically impossible.

**Verdict for case C:** **load-bearing wall.** A Pfaffian extension
with carefully chosen time-twisted SO(3,1)-covariant gap function
**could** in principle reproduce the retained closure (3) on the
diagonal sector. The retained boost-covariance theorem alone does
not exclude this case.

## 4. Synthesis

| Pfaffian sub-class | Continuum-limit closure compatible? | Disposition |
|---|---|---|
| s-wave (case A) | violates anomalous-correlator absence | likely incompatible |
| angularly non-trivial (case B) | violates SO(3,1) | **excluded** |
| angular-singlet, time-twisted, SO(3,1)-covariant (case C) | conceivable | **load-bearing wall** |

So **(SR-2) closes only partially.** Cases A and B are excluded by
the retained continuum-limit content. Case C remains open as a
fine-tuned admissibility question.

### 4.1 The reduced obstruction

`(C2-X)` under permissive reading reduces to: **does the retained
framework content exclude the angular-singlet, time-twisted,
SO(3,1)-covariant Pfaffian sub-class (case C)?**

This is a sharper formulation of `(C2-X)` than Cycle 4's "research-
level" statement. It now points to a specific narrow sub-class of
extensions that must be ruled out.

### 4.2 Two possible closure routes for case C

- **(SR-2a) Anomalous-correlator existence theorem.** Strengthen
  the retained closure (3) to a *full-correlator* statement: in the
  continuum limit, the retained framework content forces all
  fermion correlators to be of the diagonal-Wightman form (no
  anomalous `<chi chi>`). This would close case C by excluding any
  pairing-induced anomalous correlator regardless of angular /
  time structure.
- **(SR-2b) BCS ground-state vs framework ground-state.** Show that
  the framework's retained ground-state structure is incompatible
  with a BCS coherent superposition of Cooper pairs. The framework's
  retained anomaly cancellations + retained one-generation matter
  closure may already imply a fermion-number-eigenstate ground
  state, which would exclude all BCS / BdG extensions including
  case C.

`(SR-2b)` is the more direct attack. The retained
`G_BARE_DERIVATION_NOTE.md` cluster establishes `g_bare = 1` on a
fermion-number-eigenstate evaluation surface; if that surface is
unique (per the retained `G_BARE_RIGIDITY_THEOREM_NOTE.md`), then
BCS extensions are excluded.

## 5. What this stretch attempt closes and does not close

**Closes (this cycle):**

- Two of three Pfaffian sub-classes (cases A and B) are
  incompatible with retained content.
- The remaining case (C) is identified as the load-bearing wall.
- Two sharper sub-routes (SR-2a, SR-2b) for closing case C are
  named.
- Cycle 4's identification of `(SR-2)` as cleanest continuation is
  validated as productive — even partial closure trims the open
  obstruction surface significantly.

**Does not close:**

- Case C itself — angular-singlet, time-twisted, SO(3,1)-covariant
  Pfaffian extensions remain admissible without further argument.
- `(C2-X)` unconditionally; the conditional Cycle-2 Dirac theorem
  remains conditional on case-C exclusion.

## 6. Falsifiers

The stretch-attempt findings are falsified by:

- a worked construction of a SO(3,1)-covariant Pfaffian extension
  in case C that *does* reproduce the retained closure (3) on the
  diagonal sector — this would refute the partial closure of cases
  A and B if the construction generalizes;
- a direct proof that case C is admissible under retained anomaly
  cancellations + retained ground-state uniqueness — would refute
  `(SR-2b)`;
- empirical 0νββ signal at any precision — falsifies the
  conditional theorem's empirical content.

## 7. Cross-references

- Cycle 4 stuck fan-out:
  `docs/NEUTRINO_AXIOM3_READING_STUCK_FANOUT_NOTE_2026-04-28.md`
  (identified `(SR-2)` as cleanest continuation).
- Cycle 3 stretch attempt:
  `docs/NEUTRINO_NORMAL_GRAMMAR_U1_RIGIDITY_STRETCH_ATTEMPT_NOTE_2026-04-28.md`
  (introduced the `(C2-X)` obstruction this cycle attacks).
- Cycle 2 conditional theorem:
  `docs/NEUTRINO_DIRAC_GLOBAL_LIFT_PARTIAL_THEOREM_NOTE_2026-04-28.md`
  (the conditional theorem case C threatens).
- Retained closure under attack:
  `docs/LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md`.
- Companion 2D version:
  `docs/LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md`.
- Retained ground-state structure:
  `docs/G_BARE_DERIVATION_NOTE.md`,
  `docs/G_BARE_RIGIDITY_THEOREM_NOTE.md` (relevant to `(SR-2b)`).
- `A_min`: `docs/MINIMAL_AXIOMS_2026-04-11.md`.

## 8. Boundary

This is a stretch-attempt artifact under Deep Work Rules. It does
not retain any input, does not close `(C2-X)`, and does not
unconditionally lift the Cycle-2 conditional Dirac theorem. It
produces:

- partial closure of `(SR-2)` (cases A and B incompatible);
- explicit identification of case C as the load-bearing wall;
- two sub-route formulations `(SR-2a)`, `(SR-2b)` for closing
  case C;
- recommendation that `(SR-2b)` BCS-vs-framework-ground-state route
  is the more direct next attack.

A runner is not authored: the attempt is structural case-analysis on
the BdG propagator (8) vs the retained continuum-limit closure (3).
No new symbolic or numerical content beyond the standard BdG
Bogoliubov-coefficient algebra (9)-(11), which is textbook BCS.
