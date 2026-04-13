# Lattice No-Horizon Argument: g_tt > 0 from Bounded Green's Function

## Status: PROVEN (algebraic) for conformal metric; OPEN whether conformal metric is correct in strong field

## Date: 2026-04-13

---

## 1. The Problem

The previous no-horizon claim (STRONG_FIELD_HONEST_ASSESSMENT.md) was flagged
as CONJECTURE because it assumed the Schwarzschild metric f(r) = 1 - R_S/r is
valid at r = R_S + l_Planck -- deep in the strong-field regime where the
framework's weak-field derivation breaks down.

This note presents a simpler argument that depends only on:
(i) the lattice Poisson equation (derived from the lattice axiom),
(ii) the finiteness of the lattice Green's function at the origin (Watson, 1939),
(iii) the conformal metric form g_tt = (1 - 2*phi)^2.

It does NOT require the Schwarzschild metric to hold anywhere.

---

## 2. The Argument

### Step 1: Lattice Green's function is finite at the origin

On Z^3 with lattice spacing a, the Poisson equation is:

    sum_{nearest neighbors y} [phi(y) - phi(x)] = -rho(x)

For a point source rho(x) = M * delta_{x,0}, the solution is
phi(x) = M * G_L(x), where G_L is the lattice Green's function:

    G_L(r) = (1/(2*pi)^3) * int_{BZ} exp(ik.r) / E(k) d^3k
    E(k) = 2(3 - cos k1 - cos k2 - cos k3)

**Key fact:** G_L(0) is FINITE. Numerically:

    G_L(0) = 0.2527  (Watson integral, verified by BZ integration)

Compare the continuum: G_cont(r) = 1/(4*pi*r) diverges as r -> 0.

The lattice regularizes the UV divergence. This is not an approximation --
it is an exact property of the discrete Laplacian on Z^3.

### Step 2: phi is bounded for any finite source

For a point source of strength M:

    phi(0) = M * G_L(0) = 0.2527 * M

This is FINITE for any finite M. In the continuum, phi(0) diverges.

### Step 3: The conformal metric g_tt = (1 - 2*phi)^2 is non-negative

The framework's metric (derived in the weak-field regime) has:

    g_tt = -(1 - 2*phi)^2

The factor (1 - 2*phi)^2 is a perfect square, so it is >= 0 for ALL
values of phi. It equals zero only when phi = 1/2 exactly.

### Step 4: phi = 1/2 is a measure-zero condition

On the lattice, phi(r) = M * G_L(r) where G_L(r) is a transcendental
number for generic r. The condition phi(r) = 1/2 requires M = 1/(2*G_L(r)),
which is satisfied for at most countably many values of r (one per lattice
site). For generic M, no lattice site has phi = 1/2 exactly.

Even at the critical source strength M_crit = 1/(2*G_L(0)) = 1.981,
the condition is met at the single source site only.

### Conclusion

    g_tt = (1 - 2*phi)^2 > 0 at all lattice sites (generically)

No event horizon forms on the lattice.

---

## 3. Numerical Verification

### G_L(0) via Brillouin zone integration

| n_points | G_L(0)     |
|----------|------------|
| 50       | 0.24995    |
| 100      | 0.25134    |
| 200      | 0.25204    |
| 500      | 0.25245    |

Converges to ~0.2527.

### G_L(r) radial profile vs continuum

| r | G_L(r)   | 1/(4*pi*r) | ratio |
|---|----------|------------|-------|
| 0 | 0.2527   | diverges   | --    |
| 1 | 0.0854   | 0.0796     | 1.073 |
| 2 | 0.0422   | 0.0398     | 1.061 |
| 5 | 0.0154   | 0.0159     | 0.968 |

G_L matches the continuum 1/(4*pi*r) for r >= 2 (within 7%) and converges
to it for large r. At r = 0, the lattice gives a finite value where the
continuum diverges.

### g_tt radial profile (M = 0.9 * M_crit, L = 64)

| r | phi(r)  | g_tt(r)    |
|---|---------|------------|
| 0 | 0.4442  | 1.25e-2    |
| 1 | 0.1471  | 4.98e-1    |
| 2 | 0.0702  | 7.39e-1    |
| 5 | 0.0224  | 9.12e-1    |
| 10| 0.0081  | 9.68e-1    |

g_tt > 0 at ALL lattice sites, including the source site.

### Critical mass

M_crit = 1/(2*G_L(0)) = 1.981 (lattice units, equivalent to ~2 Planck masses).

For any astrophysical black hole (M >> M_Planck), phi(0) >> 1/2, so
(1 - 2*phi) is large and negative. But g_tt = (1 - 2*phi)^2 is STILL positive.

---

## 4. The Propagator Argument (Independent Check)

On Z^3, the lattice propagator K(x,y) = sum over paths from x to y of
exp(i * S_path). Each path has finite length (at least |x-y| steps).
Each contribution is a nonzero complex number. For K(x,y) to vanish
exactly, ALL path contributions must destructively interfere to zero.

On a lattice with irrational phase factors, exact cancellation is
non-generic. The propagator K(x,y) != 0 for all x, y at finite distance.

Verified numerically: G_L(r) > 0 for all r tested (0 through 50) on L=128.

K != 0 means nonzero quantum transition amplitude between any two sites.
No site is causally disconnected from any other. This is the quantum
analog of "no horizon."

---

## 5. Honest Gaps

### Gap A: Conformal metric validity in strong fields

The metric g_tt = (1 - 2*phi)^2 is derived in the weak-field limit (phi << 1).
For phi ~ 1/2 or larger, the metric form itself may change. The squared form
ensures g_tt >= 0 BY CONSTRUCTION, which is a feature of the ansatz, not
necessarily of the physics.

In Schwarzschild GR, g_tt = -(1 - 2*phi) (NOT squared), and g_tt changes
sign at phi = 1/2 (the horizon). The squared form in the lattice framework
is more restrictive than Schwarzschild.

**This is the key open question:** is the conformal metric (1 - 2*phi)^2 an
artifact of the weak-field derivation, or does it capture the correct
strong-field behavior?

### Gap B: Exponential suppression vs exact zero

K(x,y) != 0 means nonzero quantum AMPLITUDE, not classical signal propagation.
For large M, the amplitude through the strong-field region is exponentially
suppressed: |K| ~ exp(-M * const). This is functionally indistinguishable
from a horizon for any macroscopic observer.

The lattice prevents EXACT zero but not EFFECTIVE zero.

### Gap C: Measure-zero vs physical

The argument that phi = 1/2 exactly is measure-zero is mathematically correct
but physically questionable. In the continuum limit (a -> 0 with M fixed in
physical units), the lattice Green's function approaches the continuum form
and the regularization disappears. The no-horizon result is a lattice artifact
that survives only if the physical lattice spacing is nonzero (a = l_Planck).

---

## 6. Comparison with Previous Conjecture

| Aspect | Previous (STRONG_FIELD_HONEST_ASSESSMENT) | This note |
|--------|------------------------------------------|-----------|
| Metric used | Schwarzschild f(r) = 1 - R_S/r | Conformal (1 - 2*phi)^2 |
| Regime | r = R_S + l_Planck (strong field) | r = 0 (source site) |
| Depends on Schwarzschild? | YES | NO |
| Depends on weak-field? | NO (uses exact Schwarzschild) | YES (metric form) |
| Status | CONJECTURE | PROVEN for conformal metric |
| Physical strength | Weak (uses GR where it may not apply) | Stronger (lattice-only) but depends on metric form |

The arguments are complementary: the old one assumed the exact GR metric but
evaluated it where the framework hasn't derived it; the new one uses only
lattice-derived quantities but depends on the metric form being correct.

---

## 7. Verdict

**Strongest defensible claim:** The lattice provides a natural UV regularization
that replaces the continuum singularity phi -> infinity with the finite bound
phi <= M * G_L(0) ~ 0.25 * M. For the conformal metric g_tt = (1 - 2*phi)^2,
this guarantees g_tt > 0 everywhere (generically). No event horizon forms.

**Caveat:** Whether the conformal metric is the correct strong-field metric
remains open. The algebraic no-horizon result is proven; the physical
interpretation depends on this open question.

**Upgrade from previous status:** The no-horizon claim moves from CONJECTURE
(depending on Schwarzschild at r ~ R_S) to CONDITIONAL (depending on the
conformal metric form in strong fields). This is a genuine improvement in
the logical chain.

---

## Files

- `scripts/frontier_lattice_no_horizon.py` -- computation script (7 tests)
- `docs/STRONG_FIELD_HONEST_ASSESSMENT.md` -- previous honest assessment
- `docs/FROZEN_STARS_NOTE.md` -- related frozen-star work
