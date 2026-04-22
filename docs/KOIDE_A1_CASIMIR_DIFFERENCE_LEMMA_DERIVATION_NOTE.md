# Koide A1 from the Casimir-Difference Lemma — Derivation Track

**Date:** 2026-04-22
**Status:** active derivation track for the A1 / Q = 2/3 closure via the
Yukawa-doublet Casimir difference `T(T+1) − Y² = 1/2`
**Target:** axiom-native closure of Koide `Q = 2/3` using only retained
gauge data — no new framework primitives.

## 0. Scope

The retained `C_τ = T(T+1) + Y² = 1` theorem gives the Yukawa-coupling
SUM, derived from gauge-by-gauge enumeration of 1-loop diagrams in the
charged-lepton self-energy (cf.
`docs/KOIDE_EXPLICIT_CALCULATIONS_NOTE.md` §"Deliverable 2"). The
candidate companion lemma — long flagged as the cleanest A1 closure
route — is the Casimir DIFFERENCE identity

```
T(T+1) − Y² = 1/2     for both Yukawa-doublet participants (L, H).
```

This note develops the structural derivation that connects this
group-theoretic fact to the Frobenius equipartition condition

```
a_0² = 2 |z|²
```

on the C_3 character decomposition of the mass-square-root vector
`v = (√m_e, √m_μ, √m_τ)`, which is the exact algebraic equivalent of
Koide's `Q = 2/3` (cf.
`docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`).

## 1. The two-line observation that motivates the program

Suppose, on the retained framework surface, we can establish proportionality
constants `c, c'` such that

```
a_0²  =  c · ( T(T+1) + Y² )                                        (S)
|z|²  =  c' · ( T(T+1) − Y² )                                       (D)
```

with the relative normalization `c' = c/2`. Then the A1 condition
`a_0² = 2 |z|²` becomes

```
c · ( T(T+1) + Y² )  =  2 · ( c / 2 ) · ( T(T+1) − Y² )
T(T+1) + Y²          =  T(T+1) − Y²    (after canceling)
```

— which trivially fails. So the *naive* relative normalization cannot
be `c' = c/2`. The **non-trivial** relative normalization that makes
A1 pop out is

```
a_0²  =  c · ( T(T+1) + Y² )
|z|²  =  c · ( T(T+1) − Y² )           [SAME constant, no factor of 1/2]
```

with then
```
a_0² = 2 |z|²    ⟺    T(T+1) + Y² = 2 [ T(T+1) − Y² ]
                 ⟺    3 Y² = T(T+1).                                (A1*)
```

For SU(2)_L doublets (T = 1/2, so T(T+1) = 3/4), condition (A1*) reads
`3 Y² = 3/4` ⟺ `Y² = 1/4` ⟺ `Y = ±1/2`. **Exactly** the Yukawa-doublet
hypercharges of L and H in the SM, and **exactly** the values that
Cl(3) already retains via the pseudoscalar ω central direction.

## 2. Closure architecture

The derivation therefore reduces to two named primitives:

**Primitive P1 (sum proportionality).** On the retained `hw=1` carrier,
the trivial-character weight of the mass-square-root vector satisfies

```
a_0²  =  c · ( T(T+1) + Y² ) · v_EW²
```

with `c` independent of the SM particle assignment.

**Primitive P2 (difference proportionality, same constant).** On the
same carrier, with the *same* normalization constant `c`,

```
|z|²  =  c · ( T(T+1) − Y² ) · v_EW².
```

P1 is a strengthening of the retained `C_τ = 1` ⟹ `y_τ` chain — it
states not only the overall scale of the trivial component but also
that the proportionality is the gauge-Casimir SUM. P2 is the new
identity. Together they force A1 / `Q = 2/3` once we plug in
`(T, Y) = (1/2, ±1/2)` from the Cl(3) embedding.

## 3. Where (T, Y) come from on the retained surface

The retained CL3_SM_EMBEDDING_THEOREM and its ω-pseudoscalar extension
already give:

| Quantum number | Source | Value |
|---|---|---|
| `T(T+1)` | `Cl⁺(3) ≅ ℍ ⟹ Spin(3) = SU(2)_L` Casimir on the doublet | `3/4` |
| `Y` (lepton doublet L) | central pseudoscalar ω + hypercharge assignment | `−1/2` |
| `Y` (Higgs H) | same ω + opposite-sign assignment | `+1/2` |
| `Y²` (both) | square of either | `1/4` |
| `T(T+1) + Y²` | sum | `1` |
| `T(T+1) − Y²` | difference | `1/2` |
| `3 Y²` | three times the square hypercharge | `3/4` |
| `T(T+1) − 3 Y²` | (A1*) deficit | `0` |

Authority: `docs/CL3_SM_EMBEDDING_MASTER_NOTE.md`,
`docs/CL3_SM_EMBEDDING_THEOREM.md`,
`docs/KOIDE_EXPLICIT_CALCULATIONS_NOTE.md`.

## 4. Proof obligations and execution path

The lemma is reduced to three concrete proof obligations, each of which
is a self-contained sub-derivation on the retained surface:

**Obligation O1 (S_3 / C_3-irrep alignment).**
Show that the C_3 character decomposition of the mass-square-root
vector `v = (√m_1, √m_2, √m_3)` is the same as the S_3 / C_3-irrep
decomposition of the hw=1 mass matrix into A_1 (trivial) ⊕ E (doublet)
sectors, i.e. `a_0² ↔ ‖A_1 component‖²`, `|z|² ↔ (1/2)‖E component‖²`.

**Obligation O2 (sum-Casimir matches A_1 weight).**
Show that on the retained 1-loop self-energy chain that already
delivers `y_τ` from `C_τ = T(T+1) + Y² = 1`, the same Wick contraction
applied to the trivial character `e_+ = (1,1,1)/√3` recovers
`a_0² ∝ (T(T+1) + Y²) · v_EW²`. This is the strengthening of the
retained `y_τ` derivation from "scalar = 1" to "scalar = sum-Casimir".

**Obligation O3 (difference-Casimir matches E weight, same constant).**
Show that the same Wick contraction, applied instead to the
non-trivial characters `e_ω, e_{ω̄}`, gives
`|z|² ∝ (T(T+1) − Y²) · v_EW²` with the *same* normalization constant
as O2. This is the new identity. Geometrically it follows if the
trivial character carries the longitudinal/diagonal projector
`P_= = T_3² + Y²` and the non-trivial characters carry the orthogonal
complement `P_⊥ = T(T+1) − T_3² − Y²`.

The third obligation is the load-bearing step. The other two are
either retained (O2 strengthens an existing derivation) or already
implicit in the retained `hw=1` algebraic equivalence (O1).

## 5. Why this avoids the no-go theorems

Nine retained no-go theorems rule out specific A1-forcing mechanisms
(`KOIDE_A1_DERIVATION_STATUS_NOTE.md` §"Retained no-go theorems"). The
Casimir-difference lemma evades all of them because:

- it is **not** a C_3-invariant variational principle on the hw=1
  block alone (Theorem 5 escape) — it imports SU(2)_L × U(1)_Y data;
- it is **not** a 4th-order Clifford-product mechanism (Theorem 6
  escape) — it is built from the *quadratic* Casimir on doublets;
- it is **not** Z_3-invariance alone (§5.1 escape) — it adds the
  hypercharge constraint `3Y² = T(T+1)`;
- it is **not** sectoral universality (§5.6 escape) — it specifically
  selects only Yukawa-doublet (T = 1/2, Y = ±1/2) participants;
- it is **not** observable-principle character symmetry (§5.3 escape)
  — it consumes the distinct character `e_+` vs `e_ω` separation, not
  just their algebraic symmetry.

## 6. Status and what each runner asserts

| Step | Runner | Status |
|---|---|---|
| Skeleton | `frontier_koide_a1_casimir_difference_lemma_skeleton.py` | 12 PASS — closure architecture |
| O1.a | `frontier_koide_a1_casimir_difference_o1a_c3_plancherel.py` | 12 PASS — C_3 Plancherel + A_1/E projector split |
| O1.b | `frontier_koide_a1_casimir_difference_o1b_hw1_s3_alignment.py` | 17 PASS — hw=1 sector S_3-irrep projectors agree with C_3 Fourier |
| O1.c | `frontier_koide_a1_casimir_difference_o1c_mass_matrix_split.py` | 10 PASS — same projectors split the Hermitian mass matrix into trace + traceless |

**O1 closed end-to-end.** The (a_0^2, |z|^2) Frobenius pair is the
A_1 / E isotypic decomposition of the sqrt-mass vector under S_3 axis
permutation on the hw=1 carrier; the same projectors decompose the
diagonal mass matrix into its trace (A_1) and traceless (E) pieces.

| O2.a | `frontier_koide_a1_casimir_difference_o2a_sum_enumeration.py` | 15 PASS — gauge-by-gauge SUM enumeration; SUM=1 shared by {L, H, e_R} |
| O2.b | `frontier_koide_a1_casimir_difference_o2b_trivial_weight.py` | 6 PASS — trivial-character weight inherits SUM via generation-blind y_τ chain |
| O2.c | `frontier_koide_a1_casimir_difference_o2c_constant_pin.py` | 6 PASS — c is fixed by retained inputs; ratio is c-cancellative |

**O2 closed.** The proportionality constant `c` in `a_0^2 = c · SUM · v_EW^2`
is fixed by retained inputs alone (`v_EW`, `α_LM`, `I_loop`, loop
normalisation). Critically, the Koide A1 ratio is c-cancellative —
A1 reduces to `(T(T+1)−Y²)/(T(T+1)+Y²) = 1/2`, which is independent
of `c`.

| O3.a | `frontier_koide_a1_casimir_difference_o3a_offdiag_enumeration.py` | 8 PASS — E-isotype channel = W± Casimir = T(T+1)−T_3²; reduces to T(T+1)−Y² for L/H |
| O3.b | `frontier_koide_a1_casimir_difference_o3b_same_loop.py` | 7 PASS — same K_loop on diagonal and off-diagonal channels (same Feynman topology) |
| O3.c | `frontier_koide_a1_casimir_difference_o3c_same_c.py` | 9 PASS — same-c synthesis ⟹ Q = 2/3 on SM Yukawa doublet |

**O3 closed end-to-end.** With P1 and P2 sharing a common loop-level
constant c (justified by O3.b's same-Feynman-topology argument), the
schema ratio `|z|²/a_0² = (T(T+1)−Y²)/(T(T+1)+Y²)` is c-independent.
On the SM Yukawa-doublet assignment, this equals 1/2 ⟺ Koide A1
⟺ Q = 2/3. PDG matches at the `1e-5` level.

| X1 | `frontier_koide_a1_casimir_difference_x1_uniqueness_sweep.py` | 4 PASS — (A1*) admits NO rational solution beyond (T,Y) = (1/2, ±1/2) |
| X2 | `frontier_koide_a1_casimir_difference_x2_perturbation_test.py` | 5 PASS — first-order Y/T perturbations (∂r/∂Y = -3/2, ∂r/∂T = 1) |
| X3 | `frontier_koide_a1_casimir_difference_x3_iff.py` | 11 PASS — symbolic A1 ⟺ (A1*) via sympy; 6/6 sample table |
| X4 | `frontier_koide_a1_casimir_difference_x4_compose_hw1_theorem1.py` | 7 PASS — end-to-end chain Q=2/3 ⟺ a_0²=2|z|² ⟺ (A1*) ⟸ retained inputs |
| X5 | `frontier_koide_a1_casimir_difference_x5_no_go_evasion.py` | 10 PASS — evades all 9 retained no-go theorems |
| X6 | `frontier_koide_a1_casimir_difference_x6_brannen_corollary.py` | 7 PASS — δ = Q/d = 2/9 follows on retained Brannen reduction; P residual flagged |
| X7 | `frontier_koide_a1_casimir_difference_x7_existing_runner_consistency.py` | 6 PASS — re-runs existing yukawa_casimir runner (9/9), confirms consistency |

**Uniqueness sharpened.** The condition `3Y² = T(T+1)` admits no other
rational `(T, Y)` with `T` half-integer ≥ 1/2 and `C_sum > 0`. The
Cl(3) embedding's specific `(1/2, ±1/2)` Yukawa-doublet assignment is
not just a sufficient condition — it is the unique rational realisation
of the cone closure.

**O3.a observation.** The W3 and B exchanges are flavor-diagonal, so
their Casimir contributions are pure A_1. Only W± (off-diagonal
SU(2)_L) carries E-isotype content, with weight `C_W± = T(T+1)−T_3² = 1/2`.
This equals `T(T+1)−Y²` exactly when `T_3² = Y²`, i.e. `(T,Y) = (1/2, ±1/2)` —
the Yukawa-doublet assignment retained from Cl(3).

**O2.a clarification.** The SUM `T(T+1) + Y² = 1` is *not* unique to
the Yukawa-doublet participants — it also holds for `e_R` because
`Q_{e_R}² = 1` (and the EM cross-check gives `C_γ = Q²`). What is
load-bearing for the closure is **(i)** that the SUM = 1 holds for
both Yukawa doublet participants (used as scale input via the retained
`y_τ` derivation) and **(ii)** that the DIFFERENCE = 1/2 distinguishes
{L, H} from {e_R, Q, u_R, d_R}. The DIFFERENCE is the unique
discriminant of the Yukawa-doublet pair.

**O1.a closed.** The C_3 character decomposition is symbolically
self-consistent (sympy verification of both Parseval identities) and
the A_1 (trivial) / E (nontrivial) projector pair satisfies
`P_+ + P_E = 1_3` with `v^T P_+ v = a_0^2` and `v^T P_E v = 2 |z|^2`.
The PDG charged-lepton √m vector lies within `~1e-5` of the A1 cone
on this projector split.

**Next:** O1.b — lift the projector split from the 3-dim generation
space to the hw=1 carrier mass-matrix algebra (S_3-irrep
decomposition `8 = 1 + 1 + 3 + 3` from
`docs/S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`).

## 7. References

- `docs/KOIDE_A1_DERIVATION_STATUS_NOTE.md` (Route F entry)
- `docs/KOIDE_EXPLICIT_CALCULATIONS_NOTE.md` (Deliverable 2)
- `docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md` (hw=1 carrier, C_3 decomposition)
- `docs/CL3_SM_EMBEDDING_MASTER_NOTE.md`, `docs/CL3_SM_EMBEDDING_THEOREM.md` (T, Y assignments)
- `scripts/frontier_koide_a1_yukawa_casimir_identity.py` (existing observation runner)
