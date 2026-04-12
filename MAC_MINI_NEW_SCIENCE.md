# Mac Mini — Current Run List

Pull first:
```bash
cd Physics-compute
git pull origin claude/youthful-neumann
```

## PRIORITY A: SU(3) from Graph Structure (NEW — DEDICATED MAC MINI LANE)

SU(2) already emerges from the staggered lattice's bipartite Z₂ parity. SU(3) does NOT emerge from the cubic lattice because it's 2-colorable, not 3-colorable. We need to find a graph structure that produces SU(3).

This is a dedicated Mac Mini investigation because it needs systematic exploration across many graph types and may require heavy eigendecomposition.

### A1. Triangulated lattice (3-colorable → SU(3)?)

Build a 3D triangulated lattice (face-centered cubic or tetrahedral) that is naturally 3-colorable. The 3-coloring assigns one of 3 "colors" to each node. Build a 3-component propagator where the hopping matrices respect the color structure. Check if the resulting algebra contains su(3).

```bash
python3 scripts/frontier_su3_triangulated.py 2>&1 | tee ~/Desktop/su3_triangulated.txt
```

### A2. Kaluza-Klein with 3-cycles

Attach a 3-node cycle to each node of the 3D cubic lattice. The internal cycle has D₃ ~ S₃ ~ Weyl(SU(3)) symmetry. Build the propagator on this 4D graph (3 external + 1 internal) and check if SU(3) gauge structure emerges from the internal degree of freedom.

```bash
python3 scripts/frontier_su3_kaluza_klein.py 2>&1 | tee ~/Desktop/su3_kaluza_klein.txt
```

### A3. Honeycomb/graphene lattice (natural 3-sublattice)

The honeycomb lattice has a natural 3-sublattice structure (A, B, C sites). In 3D, the hexagonal close-packed lattice has a similar structure. Build the staggered propagator on this lattice and check if the 3-sublattice structure produces SU(3) generators.

```bash
python3 scripts/frontier_su3_honeycomb.py 2>&1 | tee ~/Desktop/su3_honeycomb.txt
```

### A4. Tensor product of SU(2) representations

SU(3) can be constructed from SU(2) subgroups: SU(3) ⊃ SU(2) × U(1). We already have SU(2) from the staggered lattice. Can we combine the SU(2) with an additional U(1) (from edge phases) to get the full SU(3) algebra?

Check: do the existing SU(2) generators and U(1) phase generators close into an su(3) Lie algebra?

```bash
python3 scripts/frontier_su3_from_su2.py 2>&1 | tee ~/Desktop/su3_from_su2.txt
```

### A5. Wilson loops and confinement test

Even without a microscopic derivation, test whether SU(3) gauge fields on the lattice show confinement (area-law Wilson loops). The non-Abelian gauge script already showed qualitative area-law behavior. Run a systematic string tension measurement.

```bash
python3 scripts/frontier_su3_confinement.py 2>&1 | tee ~/Desktop/su3_confinement.txt
```

### A6. Fermion doubling and generations

The staggered lattice produces 2³ = 8 taste species in 3D. The Standard Model has 3 generations. Investigate whether the 8 tastes can be organized into 3 generations plus exotics, or whether a different lattice structure (e.g., the triangulated lattice from A1) naturally produces 3 species.

```bash
python3 scripts/frontier_su3_generations.py 2>&1 | tee ~/Desktop/su3_generations.txt
```

**NOTE: Scripts A1-A6 may not exist yet on the branch. If a script is missing, skip it — the laptop will create them and push. Pull again before each run.**

## PRIORITY B: UV-IR Cosmological Constant (when script lands)

```bash
python3 scripts/frontier_uv_ir_cosmological.py 2>&1 | tee ~/Desktop/uv_ir_cosmological.txt
```

7 tests of whether the cosmological constant is set by the graph's global size. The most interesting test: does holographic mode counting (area-law) suppress the vacuum energy?

## PRIORITY C: Previous runs (if not already done)

```bash
for s in frontier_single_axiom_information frontier_single_axiom_hilbert frontier_single_axiom_computation frontier_hawking_sign_diagnosis frontier_conformal_boundary frontier_geodesic_equation frontier_self_energy_critical_dimension frontier_bound_state_selection frontier_deep_literature_search frontier_accessible_prediction frontier_non_abelian_gauge; do echo "=== $s ===" && python3 scripts/${s}.py 2>&1 | tee ~/Desktop/${s}.txt && echo "DONE: $s"; done
```

## SU(3) Run-all (when scripts are ready)

```bash
for s in frontier_su3_triangulated frontier_su3_kaluza_klein frontier_su3_honeycomb frontier_su3_from_su2 frontier_su3_confinement frontier_su3_generations; do echo "=== $s ===" && python3 scripts/${s}.py 2>&1 | tee ~/Desktop/${s}.txt && echo "DONE: $s"; done
```
