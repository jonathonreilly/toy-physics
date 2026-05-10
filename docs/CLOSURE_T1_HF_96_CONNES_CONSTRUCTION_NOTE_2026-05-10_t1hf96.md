# T1.4 - 96-Dim Connes-Chamseddine H_F Construction Candidate on the Cl(3)/Z^3 Substrate

**Date:** 2026-05-10
**Claim type:** bounded_construction; no closure or theorem promotion
**Status authority:** source-note proposal only; audit verdict and effective
status are set by the independent audit lane.
**Primary runner:** [`scripts/cl3_closure_t1_hf_96_2026_05_10_t1hf96.py`](../scripts/cl3_closure_t1_hf_96_2026_05_10_t1hf96.py)
**Cached output:** [`logs/runner-cache/cl3_closure_t1_hf_96_2026_05_10_t1hf96.txt`](../logs/runner-cache/cl3_closure_t1_hf_96_2026_05_10_t1hf96.txt)

## Boundary

This note extends PR 1061's `C^8` staggered taste-cube assembly to a
candidate 96-dimensional finite Hilbert space `H_F_tot = C^8 x C^3 x C^4`
matching the Connes-Chamseddine `H_F^{Connes} = 3 generations x 32 spinor
components = 96`. The construction:

1. Confirms `8 * 3 * 4 = 96` matches the Connes-Chamseddine `H_F` dimension.
2. Lifts the per-site `C^8` staggered Cl(3) generators `Gamma_i` and the
   `C, Cl^+(3), M_3(C)` finite-algebra summands of PR 1061 to operators on
   `End(H_F_tot)`.
3. Lifts the retained `hw=1` `Z_3` three-generation orbit to a `C^3` factor.
4. Adds a `C^4` factor carrying the particle/antiparticle (CPT) doubling
   tensored with a weak-isospin chirality grading.
5. Assembles a `KO`-dimension-6 real structure `J` on `H_F_tot` with
   `J^2 = +I_96`, `J D_F = D_F J`, and `J gamma_F = -gamma_F J`.
6. Re-tests order-one on `H_F_tot` for scalar and minimal-staggered `D_F`.

The result is qualitatively the same as PR 1061 with the dimensions
extended to the full Connes-Chamseddine count: the lift co-locates the
summands on a single 96-dim finite Hilbert space and supports a `KO`-dim-6
`J`, but order-one-compatible nontrivial `D_F` selection remains open.

No new axiom, retained primitive, audit verdict, or retained-grade status is
introduced here. The note records the dimensional match `8 * 3 * 4 = 96` and
the corresponding bounded structural construction. It does not promote any
prior open gate to a theorem and does not close left-handed content.

## Source Dependencies

- Per-site Cl(3) local algebra and `Z^3` spatial substrate:
  [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md).
- PR 1061 staggered `C^8` taste cube and `C / Cl^+(3) / M_3(C)` co-location:
  [`CLOSURE_C_STAGGERED_DIRAC_GATE_NOTE_2026-05-10_cStaggered.md`](CLOSURE_C_STAGGERED_DIRAC_GATE_NOTE_2026-05-10_cStaggered.md),
  [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md).
- Three-generation `hw=1` `Z_3` orbit and `M_3(C)` generation observable:
  [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md).
- Particle/antiparticle (CPT) doubling on the staggered substrate:
  [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md).
- Order-one open gate inheritance from PR 1061:
  [`P_LH_ORDER_ONE_STAGGERED_DIRAC_OPEN_GATE_NOTE_2026-05-10_pPlh_order_one.md`](P_LH_ORDER_ONE_STAGGERED_DIRAC_OPEN_GATE_NOTE_2026-05-10_pPlh_order_one.md),
  [`PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE_2026-05-10_pPlh.md`](PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE_2026-05-10_pPlh.md),
  [`PRIMITIVE_P_LH_NCG_NATIVE_NOTE_2026-05-10_pPlh_ncg_native.md`](PRIMITIVE_P_LH_NCG_NATIVE_NOTE_2026-05-10_pPlh_ncg_native.md).

The references to Connes/Chamseddine/Krajewski spectral-triple machinery
are standard-mathematics comparators and vocabulary for the order-one
test. They are not used as a repo-wide axiom. The KO-dim-6 sign and the
particle/antiparticle doubling pattern are imported as candidate
structural ingredients only, with the same import boundary as in PR
1061 and the P-LH content proposal note.

## Construction

The runner builds the candidate finite Hilbert space

```text
H_F_tot   =   H_taste   (x)   H_gen   (x)   H_cpt_chir
=    C^8      (x)   C^3     (x)   C^4
```

with dimension `8 * 3 * 4 = 96`, where:

- `H_taste = C^8` is the one staggered taste cube of PR 1061, carrying the
  staggered Cl(3) Pauli-tensor generators

  ```text
  Gamma_1 = sigma_1 (x) I (x) I
  Gamma_2 = sigma_3 (x) sigma_1 (x) I
  Gamma_3 = sigma_3 (x) sigma_3 (x) sigma_1
  omega   = Gamma_1 Gamma_2 Gamma_3        (omega^2 = -I_8, real in this rep)
  gamma_stag = sigma_3 (x) sigma_3 (x) sigma_3
  ```

  with the `C` summand from `R[omega]`, the `Cl^+(3) ~= H` summand from
  `{I, Gamma_1 Gamma_2, Gamma_1 Gamma_3, Gamma_2 Gamma_3}`, and the `M_3(C)`
  summand from the projectors and cycle on the Hamming-weight-one triplet
  in `C^8`.

- `H_gen = C^3` carries the three-generation `hw=1` `Z_3` orbit. The three
  projectors `P_gen_i = e_i e_i^T` and the cyclic `C_3` permutation are
  lifted to `End(H_F_tot)` by acting trivially on `H_taste` and
  `H_cpt_chir`. The narrow theorem of PR 292/293/294 already shows these
  generate `M_3(C)` on `C^3`.

- `H_cpt_chir = C^4` carries two doubling factors:

  ```text
  H_cpt_chir = C^2_{p/ap}  (x)  C^2_{chir}
  ```

  The first `C^2` is the particle/antiparticle CPT doubling. We use an
  antisymmetric real form on this factor:

  ```text
  Cswap_real  =   [[ 0, -1], [1, 0]]
  ```

  with `Cswap_real^2 = -I_2` and `Cswap_real . conj(Cswap_real) = -I_2`
  (Cswap_real is real). The second `C^2` carries the weak-isospin
  chirality grading `sigma_3^{chir}`.

The candidate finite chirality grading on `H_F_tot` is

```text
gamma_F  =  gamma_stag (x) I_3 (x) (I_2 (x) sigma_3^{chir})
```

with `gamma_F^2 = I_96` and `gamma_F^* = gamma_F`.

The candidate `KO`-dimension-6 real structure on `H_F_tot` is

```text
J  =  J_unitary . K,    J_unitary  =  omega^{taste} . Cswap_real^{cpt}
```

where `K` is complex conjugation, `omega^{taste}` is the lift of `omega`
to `H_F_tot` (acts as identity on `H_gen` and `H_cpt_chir`), and
`Cswap_real^{cpt}` is the lift of the `C^2_{p/ap}` block.

Because `omega` and `Cswap_real` are both real in this representation,
`conj(J_unitary) = J_unitary`, and therefore

```text
J^2 = J_unitary . conj(J_unitary) = (omega^{taste})^2 . (Cswap_real^{cpt})^2
    = (-I_8 lift) . (-I_2 lift) = +I_96.
```

This is the `KO`-dim-6 sign. The chirality anticommutation
`J gamma_F = -gamma_F J` is checked in the runner directly.

## Candidate D_F and Order-One on H_F_tot

The minimal candidate `D_F` tested here is the lift of PR 1061's
`D_min = Gamma_1 + Gamma_2 + Gamma_3` to `H_F_tot`:

```text
D_min^{tot} = D_min (x) I_3 (x) I_4.
```

The runner verifies:

- `D_min^{tot}` is self-adjoint;
- `D_min^{tot}` is odd under `gamma_F` (the lifted taste chirality anti-
  commutes with `D_min` on `H_taste`, and `D_min^{tot}` is identity on the
  weak-chirality factor, so the full grading still anticommutes);
- `J D_min^{tot} = D_min^{tot} J` (the real `J_unitary` factors commute
  through to give `J D_min^{tot} J^{-1} = D_min^{tot}` modulo conjugation,
  which is `D_min^{tot}` since `D_min` is real in this rep).

The runner then tests the order-one condition

```text
[[D_F, a], J b J^{-1}] = 0
```

on the lifted taste-side algebra basis (the 14 elements `{I_96, Omega,
e12, e13, e23, M_3(C)_1, ..., M_3(C)_9}`, with flat rank 13) for two
`D_F` choices:

| D_F candidate | Order-one result on H_F_tot |
|---|---|
| scalar `D_F = 0.7 I_96` | zero violation (vacuous pass) |
| `D_min^{tot}` minimal staggered | nonzero violation (max ~5.5e1) |

This is the same qualitative boundary as PR 1061's `C^8` result. The
lift to `H_F_tot` does not change the order-one verdict; it amplifies the
violation footprint by the tensor identity on `H_gen (x) H_cpt_chir`.
The order-one selection problem for nontrivial `D_F` therefore carries
through unchanged to the candidate 96-dim finite Hilbert space.

## What This Note Closes

- It records the dimensional match `8 * 3 * 4 = 96` between the
  PR 1061 `C^8` taste cube + retained `Z_3` three-generation orbit +
  CPT particle/antiparticle x weak-chirality doubling, and the
  Connes-Chamseddine `H_F^{Connes} = 3 gen x 32 = 96`.
- It provides a concrete operator construction of the lifted finite-
  algebra summands and a `KO`-dim-6 real structure on `H_F_tot`.

## What This Note Does NOT Claim

- It does not close left-handed content, the Standard Model versus
  Pati-Salam discriminator, or the order-one open gate.
- It does not turn order-one into a derived theorem on `H_F_tot`.
- It does not identify the `M_3(C)` summand on `H_F_tot` with color
  (the `M_3(C)` here lives on the `hw=1` triplet of the `C^8` taste cube;
  identifying it as color requires a separate substrate-side derivation,
  see the P-LH NCG-native note).
- It does not select a physical Yukawa, mass-mixing matrix, or
  generation labelling.
- It does not change the audit status of any upstream dependency.
- It does not claim the resulting `H_F_tot` matches the Connes-Chamseddine
  spectral triple as bimodules, Krajewski diagrams, or as a representation
  of `A_F = C (+) H (+) M_3(C)`. Bimodule/Krajewski-level identification
  remains an open downstream problem.

## Additional Retention Needed

The construction here uses three retained or open-gate inputs:

1. PR 1061's `C^8` staggered taste cube (open_gate carrier).
2. The `hw=1` `Z_3` three-generation orbit (retained-bounded; see
   PR 292/293/294 narrow theorems and PR 952's three-generation
   no-proper-quotient).
3. CPT particle/antiparticle doubling on the staggered substrate
   (retained per `CPT_EXACT_NOTE.md`).

No further retention is required to write down the 96-dim candidate.
What remains open is the same as in PR 1061: order-one-compatible
selection of a nontrivial `D_F` on `H_F_tot`, and the bimodule-level
identification of the `M_3(C)` summand as color rather than as a
generation-triplet algebra. These are the same downstream open gates
listed in `PRIMITIVE_P_LH_NCG_NATIVE_NOTE_2026-05-10_pPlh_ncg_native.md`
and `P_LH_ORDER_ONE_STAGGERED_DIRAC_OPEN_GATE_NOTE_2026-05-10_pPlh_order_one.md`.

## Audit Queue Note

The intended audit row is `bounded_construction`, with dependencies seeded
by the markdown links above. The independent audit lane must decide
whether the 96-dim candidate `H_F_tot` and `KO`-dim-6 `J` are accepted,
and whether the unchanged order-one boundary is in scope for this note.

```yaml
claim_type_author_hint: bounded_construction
claim_scope: |
  96-dim candidate finite Hilbert space H_F_tot = C^8 x C^3 x C^4
  matching the Connes-Chamseddine H_F dimensional count, with PR 1061's
  C^8 finite-algebra summands lifted, the retained hw=1 Z_3 three-generation
  orbit on the C^3 factor, and a CPT particle/antiparticle x weak-chirality
  doubling on the C^4 factor. KO-dim-6 real structure J assembled on
  H_F_tot. Order-one selection of nontrivial D_F unchanged from PR 1061
  (open).
load_bearing_step_class: A
audit_required_before_effective_retained: true
contextual_inputs_not_dependencies:
  - PR 1061 C^8 staggered taste cube and finite-algebra summands
  - PR 292/293/294 + PR 952 hw=1 Z_3 three-generation narrow theorems
  - CPT_EXACT_NOTE.md particle/antiparticle doubling
contextual_imports_not_admitted:
  - Connes-Chamseddine A_F = C ⊕ H ⊕ M_3(C) bimodule identification
  - Krajewski diagram identification with the SM finite spectral triple
literature_references:
  - Chamseddine-Connes, JHEP 11 (2013) 132, arXiv:1304.8050
  - Connes, JHEP 11 (2006) 081, arXiv:hep-th/0608226
  - Chamseddine-Connes-Marcolli, Adv. Theor. Math. Phys. 11 (2007) 991
```
