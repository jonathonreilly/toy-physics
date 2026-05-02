# Assumptions and Imports — 3+1d Retained-Positive

## A_min on the framework
Single axiom: Cl(3) on Z^3, with the accepted minimal stack:
- A1. Local algebra: real Clifford algebra Cl(3), three generators γ_1, γ_2, γ_3,
  {γ_i, γ_j} = 2 δ_ij I.
- A2. Spatial substrate: Z^3 (countable, bipartite by ε(x)=(-1)^(x1+x2+x3)).
- A3. Finite local Grassmann/staggered-Dirac dynamics.
- A4. Hilbert/locality/information substrate semantics (one-axiom reduction).

## Retained primitives we may load (checked clean by ledger)

- `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` (retained, positive_theorem):
  per-site Hilbert space dim_C = 2; Cl(3) ⊗_R C ≅ M_2(C); Pauli irrep is unique
  up to unitary.
- `axiom_first_lattice_noether_theorem_note_2026-04-29` (positive_theorem;
  marked `unaudited` in ledger but the proof is internal — usable as bounded support).
- `axiom_first_coleman_mermin_wagner_theorem_note_2026-04-29` (retained,
  positive_theorem) — gives discrete-symmetry Mermin-Wagner; relevant only as
  background for "no spontaneous breaking adds chirality grading".
- `cpt_exact_note` (retained, positive_theorem): on Z^3 with even L, the
  staggered Cl(3) Hamiltonian is exactly CPT-invariant; C and P each map H -> -H,
  and the staggered "gamma_5" is the sublattice parity ε(x).
- `cl3_color_automorphism_theorem` (retained, positive_theorem).
- `physical_hermitian_hamiltonian_and_sme_bridge_note_2026-04-30` (retained,
  positive_theorem): handles H = iD lift and antiunitary T.
- `staggered_dag_note_2026-04-10` (retained_bounded): bipartite/oriented graph
  rules for staggered transport.
- `staggered_fermion_card_2026-04-10` (retained_bounded): "Chirality: Even/odd
  sublattice = staggered gamma5." Identifies the grading explicitly.
- `native_gauge_closure_note` (retained_bounded): SU(2) × SU(3) × U(1) gauge
  algebra emergence on the staggered surface.
- `graph_first_su3_integration_note` (retained_bounded): N_c=3 from graph.
- `lh_anomaly_trace_catalog_theorem_note_2026-04-25` (used as cross-reference;
  numerically verified arithmetic on retained content).
- `physical_lattice_necessity_note` (today): graph and unitary are one
  irreducible physical object on the one-axiom surface; substrate physicality.

## External imports the prior bounded version admitted

1. **ABJ inconsistency (Adler 1969 / Bell-Jackiw 1969).**
   Specifically: a chiral gauge theory in 3+1d with a nonzero ABJ anomaly trace
   violates Ward identities, longitudinal modes fail to decouple, and the theory
   is not a consistent quantum gauge theory.

2. **Singlet completion is the unique cancellation route.**
   Specifically: in this framework, the only way to render the LH content
   anomaly-free is to add SU(2)-singlet RH partners with ABJ-determined Y values.
   The prior note flags this as an admitted premise — there could in principle
   be: vector-like RH content cancelling differently, an exotic chirality
   grading without RH partners, or an extra gauge factor that absorbs the
   anomalies (Green-Schwarz style).

3. **Clifford-volume-element chirality is the only allowed grading.**
   Specifically: in a *local* QFT on a lattice in this framework, the only
   *algebraic* source of a Z_2 chirality grading on the spinor module is the
   Clifford volume element ω = γ_1 γ_2 ... γ_n.

4. **Ultrahyperbolic / multi-time Cauchy obstruction.**
   Specifically: for d_t ≥ 2 the wave equation is ultrahyperbolic;
   codimension-1 well-posedness for arbitrary local initial data fails,
   one must impose nonlocal Fourier support constraints (Craig-Weinstein,
   Tegmark).

## What "derived" means for closure
For each admission we want either:
- (a) a chain of inferences from A1-A4 + retained-clean primitives that closes
  the step on the actual current surface, or
- (b) the step re-cast as a structural fact about Cl(3)/Z^3 itself
  (e.g., a lattice obstruction provable in finite combinatorial terms), or
- (c) the step shown dispensable (an alternate proof route closes the
  theorem without it).

Anything that reduces to "well-known textbook fact" without an internal
derivation remains a literature import.
