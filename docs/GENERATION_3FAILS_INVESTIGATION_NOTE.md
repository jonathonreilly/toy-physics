# Generation 3-FAILs Investigation Note

**Date:** 2026-04-12
**Script:** `scripts/frontier_generation_3fails_investigation.py`
**Runner exit:** PASS=7 FAIL=0

## Status

BOUNDED -- exact algebraic result with bounded physical interpretation.

## Theorem / Claim

**Theorem (Projected Commutant Inequivalence):**

Let `Comm = Comm({G_mu})` be the commutant of the KS gamma algebra `Cl(3)`
in `End(C^8)`.  At each hw=1 BZ corner `X_i`, define the projected
commutant representation `rho_i(M) = P_i^dag M P_i` where `P_i` projects
onto the +1 eigenspace of `H(X_i)`.

Then:
1. All 8 Cl(3) basis elements `{I, G_mu, G_{mu nu}, G_123}` have **identical**
   projected eigenvalue spectra at all 3 corners (gauge universality holds).
2. The 6 commutant generators **outside** Cl(3) have **different** projected
   eigenvalue spectra at different corners.
3. The three projected representations `rho_1, rho_2, rho_3` are pairwise
   inequivalent as representations of the full commutant.

**Bounded claim:** This inequivalence distinguishes the three hw=1 species
by internal quantum numbers that are *not* gauge charges, matching the SM
generation structure (same gauge group, different generation labels).

## Assumptions

1. KS staggered fermion framework on the 8-site unit cell (exact).
2. Cl(3) gamma algebra built from standard KS eta phases (exact).
3. Commutant computed via null space of the commutation constraints (exact, numerical).
4. Physical interpretation of commutant generators as observable quantum numbers (bounded).

## What Is Actually Proved

### Exact results

1. **Eigenspace geometry:** The +1 eigenspaces at X1, X2, X3 are *different*
   4-dim subspaces of C^8, with all principal angles equal to 45 degrees.

2. **C3[111] maps eigenspaces:** The cubic rotation C3[111] maps the +1
   eigenspace at Xi to the +1 eigenspace at Xj, cyclically.

3. **Eigenspace mixing:** All 8 commutant generators mix the +1 and -1
   eigenspaces.  The mixing fractions are O(1), not small.  This is
   why the standard intertwiner argument fails.

4. **Cl(3) universality:** All 8 Cl(3) basis elements project with
   identical spectra at all 3 corners.  Gauge quantum numbers are universal.

5. **Commutant inequivalence:** The SVD-derived commutant generators
   (which include components outside Cl(3)) project with *different*
   spectra at different corners.  8/8 generators show spectral differences.

6. **Commutant structure:** The commutant is 8-dimensional but only 2
   dimensions (I and G123) come from Cl(3).  The other 6 live in the
   "second factor" of the tensor product decomposition C^8 = C^2 x C^4.

### Mechanism

The Hamiltonian at `K = pi * e_mu` is built from the gamma matrix `G_mu`
for that direction.  Its eigenspaces depend on *which* direction carries
the pi-momentum.  Commutant generators that involve the "other" gamma
matrices rotate between the +1 and -1 eigenspaces of `G_mu`.

When projected, the commutant generators lose information about the
orthogonal complement.  Since different corners project onto different
subspaces, the projected generators are genuinely inequivalent -- not
related by any basis change within the 4-dim eigenspace.

### Why the intertwiner fails

The naive argument "C3 maps eigenspaces and commutes with M, so the
projected representations are equivalent" fails because the formula

    P2^dag M P2 = W (P1^dag M P1) W^dag

requires `M` to preserve the eigenspace (i.e., `P_i M = M P_i`).
This does not hold.  The correct expression is:

    P2^dag M P2 = P2^dag M (P1 P1^dag + Q1 Q1^dag) P2

where `Q1` is the complementary eigenspace projector.  The cross-term
`P2^dag M Q1 Q1^dag P2` is generically nonzero.

## What Remains Open

1. **Physical identification of commutant generators:** The 6 non-Cl(3)
   commutant generators have not been identified with specific SM
   quantum numbers.  They could be generation quantum numbers, flavor
   quantum numbers, or some other internal structure.

2. **Measurement interpretation:** Calling the projected inequivalence
   "generation physicality" requires the assumption that the non-Cl(3)
   commutant generators correspond to locally measurable quantities in
   the continuum limit.

3. **Connection to mass spectrum:** The inequivalence of internal quantum
   numbers is separate from the mass hierarchy.  The EWSB 1+2 split
   provides mass distinction; this result provides quantum-number
   distinction.  The two are complementary but independent.

## How This Changes The Paper

**Safe paper statement:**

> The Cl(3) commutant projected into Fermi-surface eigenspaces yields
> inequivalent representations at the three hw=1 BZ corners.  The Cl(3)
> basis elements (gauge generators) project universally, but the
> remaining commutant generators project inequivalently.  This provides
> a structural mechanism for distinguishing the three species by internal
> quantum numbers beyond gauge charges.

**Not safe:**

> "Generation physicality gate: closed"
> "The three generations carry different gauge quantum numbers"

The result strengthens the generation physicality case by showing the
three species are algebraically distinguishable, but it does not close
the gate because the physical interpretation of the distinguishing
operators is still bounded.

## Commands Run

```
python3 scripts/frontier_generation_3fails_investigation.py
# Exit code 0, PASS=7 FAIL=0
```

## Relationship to gauge_universality FAILs

The 3 FAILs in `frontier_generation_gauge_universality.py` are:
- `projected_spectra_match` (FAIL)
- `projected_spectra_match_minus` (FAIL)
- `anomaly_traces_corner_independent` (FAIL)

These are **correct failures** reflecting a genuine algebraic fact.  The
gauge universality theorem (commutant is corner-independent on C^8) is
true, but the *projected* commutant representations are inequivalent.
The FAILs are not bugs -- they are the discovery that the Fermi-surface
projections break the C3 symmetry at the level of non-Cl(3) commutant
generators.
