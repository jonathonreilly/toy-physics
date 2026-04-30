# GOAL — axiom-first-foundations block02

Continuation of block01's axiom-first-foundations loop. Block01
delivered six theorems (PR #191): spin-statistics, reflection
positivity, cluster decomposition / Lieb–Robinson, CPT (stretch),
lattice Noether, and Cl(3) per-site uniqueness.

Block02 adds two more axiom-first theorems on the same `A_min`,
on an independent branch from `origin/main`:

- **B2-C1 — Spectrum condition.** The reconstructed Hamiltonian
  `H = -(1/a_τ) log(T)` on the physical Hilbert space `H_phys` is
  self-adjoint and bounded below. Direct continuation of block01's
  reflection-positivity result (R2), cited as parallel theorem.
- **B2-C2 — Coleman–Mermin–Wagner lattice analogue.** On
  Cl(3) ⊗ Z^d with `d ≤ 2`, no continuous global symmetry can be
  spontaneously broken at finite temperature; on `d ≥ 3` it can.
  Structurally confirms the `d_s = 3` substrate choice as the
  *minimal* dimension allowing both a long-range force law and
  spontaneous symmetry breaking of continuous symmetries.

## Hard scope (same as block01)

- new theorems / derivations only;
- branch-local audit-grade status;
- A_min is fixed; no extension proposals;
- no imports from forbidden list;
- no edits to repo-wide authority surfaces during the run.
