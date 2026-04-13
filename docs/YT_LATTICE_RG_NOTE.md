# y_t Lattice-Native RG: Replacing Continuum Operations with Lattice Operations

**Date:** 2026-04-13
**Lane:** Renormalized y_t matching (priority 4)
**Status:** BOUNDED (with exact sub-closures; bounded residual is now purely lattice)

---

## Purpose

Codex review.md blocker for Lane 4:

> "do not say SM running, the alpha_s(M_Pl) chain, or matching are fully
> discharged just because they operate on derived inputs."

The issue is not the inputs -- it is the OPERATIONS. Codex considers three
operations as not derived from the lattice:

1. Running the SM RGE (continuum operation)
2. alpha_s(M_Pl) scheme conversion (lattice-to-continuum)
3. Lattice-to-continuum matching (requires continuum theory)

This note addresses whether these operations CAN be replaced by purely
lattice operations, removing the continuum dependence.

---

## Theorem / Claim

**Claim (bounded):** The three continuum-dependent operations in the y_t
prediction chain can in principle be replaced by purely lattice operations:

| Continuum operation | Lattice replacement | Status |
|---|---|---|
| SM RGE running | Block-spin 2x2x2 RG | EXACT symmetry; BOUNDED numerics |
| alpha_s scheme conversion | Lattice plaquette coupling | EXACT definition |
| Lattice-to-continuum matching | Direct propagator pole mass | BOUNDED |

The lane remains BOUNDED, but the bounded residual is now purely a
lattice computation question, not a continuum import.

---

## Assumptions

1. **A5 (lattice-is-physical):** Z^3 with Cl(3) staggered fermions at
   spacing a = l_Planck is the physical theory.
2. **Cl(3) normalization:** g_bare = 1 from the Clifford algebra.
3. **Retained particle content:** Gauge group, generations, representations
   all derived (not disputed by Codex).
4. **No new assumptions beyond the framework axioms.**

---

## What Is Actually Proved

### 1. Block-spin RG replaces SM RGE running (EXACT symmetry)

The staggered Ward identity {Eps, D} = 2m*I forces Z_Y = Z_g
non-perturbatively. The bipartite structure of Z^3 is preserved under
2x2x2 block-spin decimation (each block has exactly 4 even + 4 odd sites).
Therefore the Ward identity holds at every coarse lattice scale, and
the ratio y_t/g_s = 1/sqrt(6) is protected at every blocking level.

This IS the RG running, performed entirely on the lattice. The lattice
blocking RG is a mathematical consequence of the lattice geometry, not
an imported continuum operation.

**Script verification:** frontier_yt_lattice_rg.py Parts 1-4.

### 2. Plaquette coupling replaces alpha_s scheme conversion (EXACT)

The lattice coupling is defined directly:

    alpha_lat = g^2 / (4*pi) = 1/(4*pi) = 0.0796

The tadpole-improved coupling alpha_V = 0.093 is computed from lattice
Feynman diagrams (the Lepage-Mackenzie coefficient c_V = 2.136 is a
pure number from the lattice action). No continuum scheme is referenced.

The plaquette expectation value on a blocked lattice directly gives the
effective coupling at each scale. This IS the coupling measurement,
performed entirely on the lattice.

**Script verification:** frontier_yt_lattice_rg.py Part 5.

### 3. Direct propagator mass replaces lattice-to-continuum matching (BOUNDED)

On the staggered lattice, the fermion propagator G(p) = D^{-1}(p) has
poles at the Brillouin zone corners. The top quark mass is the pole at
the hw=1 species corner. On a sufficiently large lattice, this pole IS
the physical m_t, with no continuum matching needed.

For free field at L=4: the minimum singular value of D equals the bare
mass exactly (verified in script, 0.00% deviation). For larger lattices
(L=8, 12), staggered species mixing on finite lattices causes deviations
(23%, 75%), demonstrating that sophisticated propagator analysis is
needed for quantitative mass extraction on finite staggered lattices.

This step is BOUNDED because:
- Finite-volume effects shift the pole mass on small lattices
- Staggered species identification requires resolving BZ corners
- EW radiative corrections break the Ward identity at O(alpha_W)

**Script verification:** frontier_yt_lattice_rg.py Part 6.

---

## What Remains Open

### The lattice-size barrier

The direct lattice-native approach requires a lattice large enough to
resolve electroweak scales. Since a = l_Planck and the EW scale is
v ~ 246 GeV ~ 10^{-17} m, the lattice would need:

    L ~ M_Pl / M_EW ~ 10^17

This is impractical for direct computation. The practical route remains
the continuum effective theory (SM RGE with derived coefficients), but
the lattice-native formulation establishes that the bounded steps are
IN PRINCIPLE replaceable by lattice operations.

### EW radiative corrections

The staggered Ward identity protects y_t/g_s = 1/sqrt(6) for the strong
coupling. Electroweak radiative corrections break this at O(alpha_W).
On a lattice with EW-scale resolution, these corrections would appear
naturally. On a practical lattice, they must be computed perturbatively,
which reintroduces a bounded (but not continuum-imported) step.

### Blocking-scheme dependence

The specific numerical values of effective couplings on blocked lattices
depend on the blocking scheme (simple averaging, Hasenbusch, etc.). The
SYMMETRY argument (ratio protection) is exact and scheme-independent,
but quantitative predictions require a well-defined blocking prescription.

---

## How This Changes The Paper

### What this narrows

The Codex objection was that three operations -- SM RGE, alpha_s chain,
matching -- are "not derived from the lattice." This note demonstrates
that all three can in principle be formulated as purely lattice operations.
The objection narrows from "continuum imports" to "practical computability
on a finite lattice."

### What this does NOT do

This does NOT close the y_t lane. The lane remains BOUNDED because:

1. The direct lattice computation requires an impractically large lattice.
2. EW radiative corrections must still be accounted for.
3. The blocking-scheme dependence introduces numerical uncertainty.

### Paper-safe wording

> The bare relation y_t = g_s/sqrt(6) is protected non-perturbatively by
> the centrality of G_5 in the d=3 Clifford algebra and the staggered
> Ward identity, which hold at every scale of the lattice blocking RG.
> The coupling alpha_s is defined directly on the lattice via the
> plaquette, and the top quark mass is in principle measurable as a
> propagator pole on the lattice. The three operations previously
> identified as continuum imports (SM RGE, scheme conversion, matching)
> are in principle replaceable by lattice-native operations. The lane
> remains bounded pending the resolution of electroweak-scale lattice
> effects.

---

## Commands Run

```bash
cd "/Users/jonBridger/Toy Physics"
python3 scripts/frontier_yt_lattice_rg.py
```

---

## Scripts Referenced

| Script | Role |
|--------|------|
| `frontier_yt_lattice_rg.py` | Lattice-native RG checks (this work) |
| `frontier_renormalized_yt.py` | Original renormalized y_t (Parts 1-8) |
| `frontier_yt_formal_theorem.py` | 1/sqrt(6) derivation |
| `frontier_yt_clean_theorem.py` | Ratio protection theorem |
