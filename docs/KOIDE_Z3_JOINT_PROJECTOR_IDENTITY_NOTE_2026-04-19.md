# Koide / Z_3 Joint Projector Identity

**Date:** 2026-04-19
**Scope:** Structural identity on `C^3` showing that the charged-lepton
Koide isotypic decomposition and the DM neutrino source-surface Z_3
decomposition are the same `C_3` isotypic split. Retained scaffolding
underneath MRU and Berry-phase on the Koide side and DPLE on the DM side.
**Primary runner:**
`scripts/frontier_koide_z3_joint_projector_identity.py` (PASS=55 FAIL=0)

## Summary

On `C^3` with the regular 3-cycle `C : e_i -> e_{i+1 mod 3}`, the
isotypic projectors used by the charged-lepton Koide lane (trivial vs.
non-trivial `C_3` irreps on the cyclic commutant) are **literally the
same 3x3 matrices** as the singlet/doublet block projectors used by the
DM neutrino source-surface lane (Z_3 basis via `U_Z3 = DFT_3`). Not just
unitarily equivalent — equal as matrices.

Formally, with `omega = exp(2 pi i / 3)` and the DFT_3 unitary

```text
U_Z3 = (1/sqrt(3)) * [[1, 1,     1    ],
                      [1, omega, omega^2],
                      [1, omega^2, omega ]],
```

let

```text
Pi_triv    := v_triv v_triv^dagger,   v_triv = (1,1,1)/sqrt(3)
Pi_om      := v_om v_om^dagger,       v_om = (1, omega, omega^2)/sqrt(3)
Pi_ombar   := v_ombar v_ombar^dagger, v_ombar = (1, omega^2, omega)/sqrt(3)
Pi_K_doublet := Pi_om + Pi_ombar

Pi_Z3_singlet := U_Z3 diag(1,0,0) U_Z3^dagger
Pi_Z3_doublet := U_Z3 diag(0,1,1) U_Z3^dagger.
```

Then, as exact 3x3 matrix identities,

```text
Pi_Z3_singlet  ==  Pi_triv                                                   (I)
Pi_Z3_doublet  ==  Pi_om + Pi_ombar  ==  I - Pi_triv                        (II)
```

The Koide and DM lanes inherit **one and the same** `C_3` isotypic
decomposition of `C^3`.

## Shared decomposition, not shared matrix

Identities (I)–(II) are exact matrix equalities between the two
projector families, but the *democracy principles that each lane
applies on top of this decomposition are different*:

- Koide lane: block democracy applied to the **cyclic compression of
  `dW_e^H`** (the charged amplitude operator) on its 3-real response
  image `(r_0, r_1, r_2)`.
- DM lane: block democracy applied to the **live Hermitian kernel
  `K_Z3(m, delta, q_+)`** with frozen intrinsic slots `(a_*, b_*)`.

These are *different matrices* living in the same `C_3` isotypic
decomposition. Block democracy on each yields the same ansatz form
`E_+ = E_perp`, but the resulting equation on one side constrains the
charged amplitude operator and the equation on the other side
constrains the live source-oriented kernel. In particular, DM block
democracy at representative `m` values places its maximum at
`(delta, q_+) ~= (0, 2)`, *orthogonal* to the selected slice
`delta = q_+ = sqrt(6)/3`; the shared decomposition is real but does
not collapse into a one-equation closure for both gates.

**Consequence for the paper:** the joint-projector identity is a
cross-lane structural bridge (confirmed), *not* a one-principle-closes-
two-gates result. It sharpens both gates but does not close them
simultaneously.

## Derivation

The three canonical `C_3` isotypic projectors on `C^3` have closed
Fourier form

```text
Pi_triv   = (I + C + C^2) / 3,
Pi_om     = (I + omega^* C + omega C^2) / 3,
Pi_ombar  = (I + omega C + omega^* C^2) / 3.
```

Their sum is `I` (Peter–Weyl completeness).

The DM Z_3-basis unitary in the repo is literally the discrete Fourier
transform on `Z_3`:

```text
(U_Z3)_{ij} = (1/sqrt(3)) * omega^{ij}
with i,j in {0,1,2} and (U_Z3)_{:,0}=v_triv,
(U_Z3)_{:,1}=v_ombar, (U_Z3)_{:,2}=v_om (convention-dependent).
```

Because `U_Z3` is DFT_3, its columns are precisely the `C` eigenvectors
`{v_triv, v_om, v_ombar}` up to a labeling of the two non-trivial
characters. Therefore

```text
U_Z3 diag(1,0,0) U_Z3^dagger = v_triv v_triv^dagger = Pi_triv,
U_Z3 diag(0,1,1) U_Z3^dagger = I - v_triv v_triv^dagger = Pi_om + Pi_ombar,
```

which are identities (I) and (II). The runner verifies both numerically
to machine precision.

## Interpretation

The `C^3` surface the Koide lane uses and the `C^3` source-surface the
DM lane uses are **decomposed along the same pair of projectors**. Any
mechanism acting natively on the `C_3` singlet/doublet split is
structurally available to both lanes simultaneously, modulo the
different underlying Hermitians the mechanism is applied to:

- Koide: `kappa = g_0^2 / |g_1|^2` is a `Pi_triv / Pi_doublet` amplitude
  ratio on `G = D^{-1}` via the cyclic compression of `dW_e^H`.
- DM: `(delta, q_+)` is the free pair inside the Z_3 doublet block on
  the live Hermitian source surface `K_Z3`.

Both live on the same Hilbert-space decomposition. This is a non-trivial
structural bridge: it was not guaranteed a priori that the two lanes'
"projector" language refers to the same matrices.

The CKM ray `sqrt(1/6) + i sqrt(5/6)`, by contrast, embeds as a rank-1
projector on `C^3` with no distinguished alignment with
`{v_triv, v_om, v_ombar}` (see the runner's overlap check). The
licensed two-component SSP statement is: **one `C_3` isotypic
decomposition (shared by Koide and DM), plus one CKM-specific rank-1
ray**.

## Falsification checks (runner)

All performed numerically at machine precision:

1. `Pi_triv`, `Pi_om`, `Pi_ombar` are rank-1 Hermitian idempotents with
   `Tr = 1` each and pairwise orthogonal (`Pi_a Pi_b = 0` for `a != b`).
2. `Pi_triv + Pi_om + Pi_ombar == I` (Peter–Weyl completeness).
3. `||Pi_Z3_singlet - Pi_triv|| < 1e-14`.
4. `||Pi_Z3_doublet - (Pi_om + Pi_ombar)|| < 1e-14`.
5. `||Pi_Z3_doublet - (I - Pi_triv)|| < 1e-14`.
6. Columns of `U_Z3` are `C`-eigenvectors with eigenvalues in
   `{1, omega, omega^*}`.
7. The CKM-ray embedding `u_CKM = (1, 0, sqrt(1/6) + i sqrt(5/6))/norm`
   has no distinguished overlap with `{v_triv, v_om, v_ombar}`.
8. `sign(H_framework)` at representative retained DM points does not
   coincide with `Pi_triv`, `Pi_Z3_singlet`, or `Pi_Z3_doublet` — the
   Koide/Z_3 unification is at the `C_3` character level, not at the
   `H_framework` sign-projector level.

## Scope

### What is established

1. Exact 3x3 matrix equality between the Koide isotypic projectors and
   the DM Z_3 block projectors on the retained `hw=1` / source-surface
   setup.
2. Both lanes inherit a single shared `C_3` isotypic decomposition of
   `C^3`.
3. The CKM ray is a separate rank-1 direction; no single projector
   governs Koide, CKM, and DM together.

### What is not established

- The shared decomposition is **not** a shared matrix in the operator
  sense: the Koide cyclic compression of `dW_e^H` and the DM live
  kernel `K_Z3` are *different* Hermitians whose democracy principles
  must be applied separately.
- No statement about `kappa = 2` itself (closed by MRU; see
  `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`).
- No statement about the DM `(delta, q_+)` point selector (the runner
  only inspects shared decomposition structure).
- No unification at the level of `H_framework` — the sign-projector of
  the live Hermitian is basin-dependent and does not track the
  `C_3` singlet/doublet split.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_z3_joint_projector_identity.py
```

Expected: final line emits `PASS=55 FAIL=0`.

## Citations

- `docs/KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md`
- `docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md`
- `docs/QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md`
- `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- Companion notes:
  - `docs/KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md`
  - `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`
  - `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`
  - `docs/SCALAR_SELECTOR_SYNTHESIS_NOTE_2026-04-19.md`
