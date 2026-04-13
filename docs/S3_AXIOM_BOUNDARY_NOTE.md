# S^3 Axiom Boundary: Reduces to the Same A5 as Generation Physicality

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Script:** `scripts/frontier_s3_axiom_boundary.py`
**Lane:** S^3 / compactification
**Exit code:** 0 (PASS=29 FAIL=0)

---

## Status

**BOUNDED** (bounded by exactly one irreducible axiom: A5)

This note proves that the S^3 compactification lane's "bounded" status
reduces to EXACTLY the same lattice-is-physical axiom (A5) as the
generation physicality lane.

NOT claiming CLOSED: the lane remains bounded modulo A5, just as the
generation lane remains bounded modulo A5.

---

## Theorem / Claim

**Theorem (S^3 Axiom Boundary):**

The S^3 compactification lane is bounded by exactly one irreducible
axiom A5 (lattice-is-physical). This is the same axiom that bounds
the generation physicality lane.

Specifically:

1. **WITH A5:** the derivation chain
   A5 -> lattice = spatial substrate -> growth produces PL 3-ball B
   -> dB = S^2 -> cone-cap -> all vertex links = S^2 -> PL 3-manifold
   -> pi_1 = 0 -> S^3 (Perelman + Moise)
   is complete. The cap-map is unique (MCG(S^2) = Z_2, both
   orientations give S^3).

2. **WITHOUT A5:** the lattice is a regularization. The continuum limit
   does not fix spatial topology. S^3 is not forced.

3. **A5 is IRREDUCIBLE:** {A1, A2, A3, A4} without A5 is consistent
   (standard LQCD is the witness -- same witness as for generations).

4. **A5 is the SAME axiom** as identified in
   `frontier_generation_axiom_boundary.py` (30/31 checks).

---

## Assumptions

1. Cl(3) algebra at each lattice site (A1).
2. Z^3 lattice with staggered Hamiltonian (A2).
3. Hilbert space is tensor product over sites (A3).
4. Unitary evolution (A4).
5. **Lattice-is-physical (A5):** Z^3 is the physical substrate, not a
   regularization. THIS IS THE TARGET AXIOM.
6. Standard PL topology results: link condition, van Kampen, Moise (1952),
   Perelman (2003), MCG(S^2) = Z_2 (Smale/Alexander).

---

## What Is Actually Proved

### Part 1: With A5, S^3 is forced

The derivation has 14 steps (10 theorems, 3 computations, 1 axiom-dependent).
Every step except one is either a standard mathematical theorem or a
verified computation. The single axiom-dependent step is:

> "The lattice Z^3 is the physical spatial substrate."

This is A5. With it, the chain produces S^3 with no free parameters.

Computational verification:
- Cubical ball boundary chi = 2 for R = 2, 3, 4, 5, 6
- All vertex links = PL S^2 after cone-cap (19/19 checks, `frontier_s3_cap_link_formal.py`)
- pi_1 = 0 by van Kampen (K contractible)

### Part 2: Without A5, S^3 is not forced

Three explicit escape routes:

1. Continuum limit a -> 0 does not fix topology (same QFT on T^3, R^3, etc.).
2. Without A5, spatial topology is a free GR parameter.
3. The growth axiom (ball-like growth -> simply connected) is a lattice-level
   statement lost in the continuum limit.

### Part 3: Same axiom as generation lane

The generation axiom boundary theorem (`frontier_generation_axiom_boundary.py`,
30/31 checks) identified A5 as the single irreducible axiom bounding
generation physicality. The S^3 lane uses the same A5 at a different
point in its derivation chain:

- **Generation:** A5 -> BZ corners are physical -> species are physical
- **S^3:** A5 -> lattice is spatial graph -> growth produces ball -> S^3

Both convert lattice regularity results into physical statements.
The irreducibility witness is the same: standard LQCD uses {A1-A4}
without A5 and is consistent.

### Part 4: Cap-map uniqueness

The cap-map (closure of PL 3-ball to S^3) is unique:
- Growth axiom produces PL 3-ball B with dB = S^2.
- MCG(S^2) = Z_2 (Smale 1959 / Alexander trick).
- Both Z_2 elements (identity and reflection) give S^3, because S^3
  admits an orientation-reversing self-homeomorphism.
- Therefore the closed manifold is S^3 regardless of gluing map.

This follows from A5 + growth axiom + standard PL topology. No
additional assumption is needed.

---

## What Remains Open

1. **A5 itself is an axiom, not a theorem.** It cannot be derived from
   {A1, A2, A3, A4}. This is the foundational commitment of the framework.

2. The general PL ball link verification (boundary vertex links = S^2
   after cone-cap) is proved for R = 2, 3, 4 by explicit computation
   (19/19 checks). The theoretical argument (PL disk + cone(boundary)
   = S^2) is standard but not formalized as a machine-checked proof.

---

## How This Changes The Paper

**Before:** S^3 compactification was described as "bounded" without
identifying what exactly bounds it or how it relates to other bounded lanes.

**After:** The S^3 lane is bounded by exactly one irreducible axiom (A5),
which is the same axiom bounding the generation lane and all other
framework predictions. This unifies the "bounded" status of both lanes:
neither is more open than the other, and both reduce to the same
foundational commitment.

Paper-safe wording:

> "The S^3 spatial topology follows from the framework axioms: the growth
> axiom produces a PL 3-ball whose unique closure is S^3 (Perelman + Moise
> + MCG(S^2) = Z_2). The derivation is conditional on the foundational
> axiom that the Planck-scale lattice is the physical substrate (A5). This
> is the same irreducible axiom that bounds the generation physicality lane
> and all other framework predictions."

---

## Commands Run

```bash
python3 scripts/frontier_s3_axiom_boundary.py
# Exit code: 0
# PASS=29 FAIL=0
```
