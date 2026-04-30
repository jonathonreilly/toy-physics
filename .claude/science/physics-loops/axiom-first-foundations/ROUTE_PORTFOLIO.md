# ROUTE PORTFOLIO — axiom-first-foundations block01

## Scoring rubric

For each candidate route the loop weighs:

- **claim-state movement (CSM):** how much program-wide claim state moves
  if the route succeeds. Retiring an implicit import everywhere is high CSM.
- **independence (IND):** does the proof live *strictly inside* `A_min`
  + permitted infrastructure, with no hidden imports?
- **verifiability (VER):** can a runner exhibit the structural content
  numerically/symbolically in finite time on a small lattice?
- **reuse (REU):** how many downstream lanes get to cite the result as
  a theorem rather than an admitted import?

Each scored 1–5; total out of 20.

## Candidate routes

| ID | Route | CSM | IND | VER | REU | Total |
|----|-------|-----|-----|-----|-----|-------|
| R1 | Spin-statistics from finite Grassmann + Cl(3) | 4 | 5 | 5 | 5 | **19** |
| R2 | Reflection positivity for canonical staggered + Wilson plaquette action | 4 | 4 | 4 | 5 | **17** |
| R3 | Cluster decomposition / Lieb–Robinson on Cl(3) ⊗ Z^3 with finite-range H | 4 | 4 | 4 | 5 | **17** |
| R4 | CPT theorem for the canonical Cl(3) staggered Grassmann action | 5 | 3 | 4 | 4 | **16** |
| R5 | Lattice Reeh–Schlieder analogue (cyclicity of polynomial algebra on the vacuum) | 3 | 3 | 3 | 3 | 12 |
| R6 | No-cloning / linearity-from-A2 lifted to the Cl(3) tensor product | 2 | 4 | 4 | 2 | 12 |
| R7 | Spectrum-condition analogue (positivity of the lattice transfer-matrix logarithm) | 3 | 4 | 4 | 4 | 15 |
| R8 | Discrete CP-symmetry no-go for a real-mass staggered determinant | 3 | 4 | 4 | 3 | 14 |

## Selected for execution this block

1. **Cycle 1 — R1 (spin-statistics).** Highest total. Cleanest derivation:
   spin-statistics is *literally* the Grassmann anticommutation rule once
   we attach to the Cl(3) local algebra and identify the Hilbert
   reconstruction.
2. **Cycle 2 — R2 (reflection positivity).** Direct prerequisite for any
   transfer-matrix / Hilbert-reconstruction language used elsewhere; used
   *implicitly* across the program.
3. **Cycle 3 — R3 (cluster decomposition / Lieb–Robinson).** Gives every
   downstream lane an honest exponential-clustering certificate. Many
   support routes silently assume it.
4. **Stretch — R4 (CPT theorem).** Riskier because lattice CPT is a
   composition of three discrete operations and the proof must commute
   them through Cl(3) charge conjugation. Run as the stretch attempt
   after Cycles 1–3 if budget allows; otherwise produce a partial
   structure / named obstruction for the next loop.

## Routes deliberately deferred

- R5–R8 are valuable but have lower CSM × VER for a 12h block. Logged
  here so the next loop can pick them up without re-scoring.
