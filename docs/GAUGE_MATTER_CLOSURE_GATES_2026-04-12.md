# Gauge/Matter Closure Gates

**Date:** 2026-04-12  
**Status:** focused review memo for the remaining full-paper theory gates  
**Scope:** anomaly-complete hypercharge / chiral completion and physical generation closure

---

## Bottom line

The structural gauge backbone is now materially stronger:

- exact native `Cl(3)` / `SU(2)`
- graph-first weak-axis selector
- graph-first structural `su(3)` closure
- bounded left-handed `+1/3` / `-1` abelian charge matching

The two remaining theory gates that most affect the ultimate paper impact are:

1. anomaly-complete hypercharge / chiral completion
2. physical generation closure

Both are real open gates. Neither is fixed by the new graph-first `SU(3)` result
alone.

---

## Gate 1. Anomaly-Complete Hypercharge / Chiral Completion

### What is already closed

- The graph-first selected-axis construction yields structural
  `su(3) \oplus u(1)` on the left-handed `8`-state surface.
- The unique traceless abelian direction gives the correct left-handed
  eigenvalue pattern:
  - `Q_L : (2,3)_{+1/3}`
  - `L_L : (2,1)_{-1}`
- The charge formula `Q = T_3 + Y/2` matches the left-handed Standard Model
  doublet charges on that surface.

### Exact obstruction

The present `8`-state surface is left-handed only. It does **not** contain the
right-handed singlet sector needed for anomaly cancellation.

Missing states:

- `u_R`, `d_R`, `e_R`
- or equivalently the left-handed conjugates
  - `u_R^c`
  - `d_R^c`
  - `e_R^c`
- `nu_R` / `nu_R^c` is optional, not required for the Standard Model anomaly
  sums

That is why the current left-handed surface still has:

- `Tr[Y] = 0`
- but `Tr[Y^3] != 0`

So the current result is:

- left-handed hypercharge-like matching

not yet:

- anomaly-complete `U(1)_Y`

### New search result on the current surface

The new graph-first chiral-completion search sharpens this obstruction:

- there are **no** weak singlets on the one-particle `8`-state surface
- in a permissive tensor-power scan:
  - `d_R`-like singlets appear by degree `2`
  - `e_R`-like singlets appear by degree `2`
  - `u_R`-like singlets do **not** appear until degree `4`

This does not prove that all completions are impossible.

It does prove that the present left-handed one-particle surface does **not**
contain a natural, symmetric, low-degree chiral completion by itself.

### New conditional completion result

The newer `CHIRAL_COMPLETION` lane materially strengthens the gate, but only in
conditional form.

What it now establishes:

- if the 4D temporal doubling is used to supply an additional `8`-state chiral
  sector
- and if that sector is parameterized as
  - `(1,3)_{y_1} + (1,3)_{y_2} + (1,1)_{y_3} + (1,1)_{y_4}`
- and if the neutrino singlet is required to be electrically neutral
  (`y_4 = 0`)

then anomaly cancellation uniquely fixes:

- `u_R : (1,3)_{+4/3}`
- `d_R : (1,3)_{-2/3}`
- `e_R : (1,1)_{-2}`
- `nu_R : (1,1)_0`

This is a real upgrade over the earlier left-handed-only state:

- the anomaly equations are now solved explicitly
- the full one-generation anomaly sums close
- the resulting spectrum matches the standard `\bar{5} + 10 + 1` bookkeeping

But this does **not** yet remove the core missing theorem:

- the script does not derive that right-handed representation template from the
  graph/taste surface itself
- it does not derive the colour assignments of the right-handed sector from the
  graph-first module
- and the uniqueness statement depends on the added `y_4 = 0` neutrality
  condition

### What theorem is needed

**Chiral completion theorem**

Hypotheses:

- the graph-selected axis gives the left-handed module
  `V_L = C^2 \otimes (C^3 \oplus C^1)`
- the graph-first commutant gives structural `su(3) \oplus u(1)`

Needed conclusion:

- derive or identify a graph-canonical completion sector `V_R` carrying the
  missing singlets
- extend the `Y` assignment to the full one-generation Weyl module
- verify:
  - `Tr[Y] = 0`
  - `Tr[Y^3] = 0`
  - `Tr[SU(3)^2 Y] = 0`
  - `Tr[SU(2)^2 Y] = 0`

### Current decision

- keep hypercharge anomaly completion **open**
- paper-safe wording remains:
  - hypercharge-like
  - left-handed charge matching
- use `GRAPH_FIRST_CHIRAL_COMPLETION_SEARCH_NOTE.md` as the current obstruction
  memo for why the right-handed sector is still missing
- treat `CHIRAL_COMPLETION_NOTE.md` as a **conditional anomaly-completion
  theorem**, not yet as a graph-canonical derivation of the full chiral sector

---

## Gate 2. Physical Generation Closure

### What is already closed

- The orbit algebra is exact:
  - `8 = 1 + 1 + 3 + 3`
- This follows from the `Z_3` action on the `8` taste states via
  Burnside/orbit-stabilizer.
- The two triplets are genuine `Z_3` orbits.
- The result is fragile in the expected way under Wilson/anisotropy deformations,
  which supports that it is structural rather than accidental.

### Exact obstruction

The orbit theorem is algebraic. It does **not** by itself prove that those
triplets are physical fermion generations.

The core unresolved issue is taste physicality:

- in standard lattice usage, tastes are regulator artifacts
- in this framework, they are supposed to be physical because the graph is
  fundamental

That step is not yet a derived theorem. It is still an ontological /
matter-assignment gap.

There is also a smaller representation-theoretic gap:

- the orbit theorem does not canonically assign physical family labels
- the two singlets still need interpretation

The newer `GENERATION_PHYSICALITY` lane improves the pressure on this gate but
does **not** close it cleanly:

- the Wilson-entanglement argument correlates the fate of some structures under
  deformation, but it does not yet canonically derive physical family labels
- the CKM and singlet sections still rely on modeled anisotropy and speculative
  singlet interpretation rather than a closed matter-assignment theorem

### What theorem is needed

**Generation physicality theorem**

Hypotheses:

- the graph/taste structure is fundamental, not a regulator
- the exact orbit algebra on the taste surface is `8 = 1 + 1 + 3 + 3`

Needed conclusion:

- provide a canonical matter assignment making the two `3`-orbits into physical
  family multiplets
- explain the role of the two singlets
- show why the taste-space triplets should be read as physical generations rather
  than a representation artifact

### Current decision

- keep physical three-generation closure **open**
- at most it can be framed as **conditional** on taste physicality

---

## What Dark Matter / CC Do And Do Not Change

Dark matter and cosmological-constant lanes remain major impact multipliers for
the full paper.

They do **not** close either of the two theory gates above.

So the correct hierarchy is:

1. structural backbone
2. hypercharge/chiral completion
3. generation physicality
4. bounded high-impact phenomenology such as dark matter and `Omega_Lambda`

Those numerics raise the paper ceiling, but they do not remove the need to close
the gauge/matter gates cleanly.

---

## Practical next move

If effort is focused correctly, the next two theorem lanes should be:

1. `graph-first chiral completion`
2. `generation physicality / matter assignment`

Everything else is secondary until those are either closed or honestly bounded.
