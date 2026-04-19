# Charged-Lepton Z_3 Source-Response Cross-Check Note (Option D)

**Date:** 2026-04-17
**Status:** cross-check runner; independence verdict on the primary-lane Koide-cone derivation
**Script:** `scripts/frontier_charged_lepton_z3_source_response_crosscheck.py`
**Authority role:** Option-D cross-check lane for item 6 of the attack chain
in [charged-lepton-mass-vector-from-hw1-observable.md](../.claude/science/hypotheses/charged-lepton-mass-vector-from-hw1-observable.md).
This note is NOT a primary authority for the charged-lepton mass-square-root
vector. It is the companion negative-independence result that rules out one
specific null hypothesis (a Z_3-only shortcut to the Koide cone) and frames
the independent content of the primary lane.

## Safe statement

On the retained `Cl(3)` on `Z^3` framework surface, construct the
Z_3-invariant bilinear source-response kernel on the `hw=1` triplet from
the left/right Z_3-character idempotents at the canonical charge assignment

    q_L = (0, +1, -1)   mod 3    ->   (0, 1, 2)
    q_R = (0, -1, +1)   mod 3    ->   (0, 2, 1)

with sources

    s_i = e_{q_L(i)}  (x)  e_{q_R(i)}     in    C[Z_3]  (x)  C[Z_3]

and Plancherel pairing `S_ij = Tr(s_i^dagger s_j)` on the regular
representation.

The runner establishes the following exact algebraic statements
symbolically:

1. `C[Z_3]` character idempotents `e_q = (1/3) sum_k omega^{-qk} T^k` are
   pairwise orthogonal idempotents with `sum_q e_q = I` and
   `Tr(e_p^dagger e_q) = delta_{pq}` on the regular representation.
2. Each generation source element `s_i` is diagonal-Z_3 invariant under
   `(T^g) (x) (T^g)` conjugation, by `q_L(i) + q_R(i) = 0 mod 3`.
3. The resulting kernel is
       S = I_3,
   i.e. real, symmetric, diagonal in the source basis, and a scalar
   multiple of the identity.
4. `S = I_3` is the degenerate point `(a, b) = (1, 0)` of the primary-lane
   `(a, b)` circulant family `a*I + b*(J - I)`. Its spectrum is
   `{1, 1, 1}` (triply degenerate), so every nonzero 3-vector is an
   eigenvector of `S`.
5. The Koide cone `a_0^2 = 2 |z|^2` is realizable inside the full
   eigenspace of `S` (any parameterized cone vector lives in `C^3`
   trivially), but `S` does NOT force any direction onto the cone -- it
   does not distinguish any direction at all.
6. The Z_3-invariant bilinear pairing is unique up to overall scale by
   Schur's lemma on `C[Z_3]`, so the diagonal form `S = c I` is the
   unique Z_3-invariant kernel on the three Cl(3)-charged sources given.

**Therefore:** Z_3 invariance alone on the hw=1 triplet, with the
canonical left/right Z_3 charge assignments and Plancherel pairing, is
*insufficient* to force a unique charged-lepton mass-square-root ray
on the Koide cone. The primary-lane Koide-cone derivation
[charged-lepton-koide-cone-2026-04-17.md](../.claude/science/derivations/charged-lepton-koide-cone-2026-04-17.md)
requires independent structural content (the Dirac spectral amplitudes
of Step 3 and the observable-principle curvature kernel of Step 1)
that is NOT reproducible from Z_3 invariance alone.

## Script reference

Runner: [frontier_charged_lepton_z3_source_response_crosscheck.py](../scripts/frontier_charged_lepton_z3_source_response_crosscheck.py)

Canonical final line:

    Z3_CROSSCHECK_AGREES_WITH_PRIMARY=INDEPENDENT

Current local runner state (framework-native inputs only, no observed
mass data):

- `frontier_charged_lepton_z3_source_response_crosscheck.py`: `PASS=41`, `FAIL=0`.

The runner uses sympy for the symbolic derivation (character idempotents
constructed from `exp(2 pi i / 3)`, simplified via `rewrite(cos)` and
`nsimplify` with `sqrt(3)` basis) and numpy for the numerical sanity
check.

## Relationship to the primary lane

Formally three scenarios were available a priori:

- **TRUE.** Option D reproduces the primary lane's
  spectral vector `v_L` to symbolic equality. The Z_3-source-response
  kernel would be of primary-lane circulant form with `b != 0` and its
  principal eigenvector would match `v_L`. This outcome would strongly
  reinforce the primary lane by providing an independent second
  derivation of the same direction.
- **FALSE.** Option D forces a DIFFERENT spectral vector incompatible
  with the primary lane (principal eigenvector off the Koide cone, or
  explicitly orthogonal to the observed hierarchy). This outcome would
  kill the composite hypothesis by internal framework contradiction.
- **INDEPENDENT.** Option D's Z_3-invariance condition does not by itself
  discriminate among spectral directions. This outcome neither
  reinforces nor contradicts the primary lane, and sharpens the
  structural claim by locating the *actual* forcing content of the
  derivation.

The runner output is `INDEPENDENT`. Specifically:

- `S = I_3` has `(a, b) = (1, 0)`, while the primary-lane Koide-cone
  forcing requires `b != 0` in its Step-2 circulant kernel. The two
  kernels are of the same algebraic shape only at the degenerate point
  `(a, 0)`.
- `S` has trivial Z_3 representation content: the three source elements
  are all invariant under the diagonal Z_3 action because
  `q_L(i) + q_R(i) = 0 mod 3` by construction. The Z_3 quantum numbers
  therefore carry no dynamical weight in the source-response kernel.
- The Koide cone is available inside `S`'s eigenspace (the entire space),
  but `S` does not select it preferentially over any other ray.

This is a *cleanly interpretable* INDEPENDENT outcome: Z_3 invariance
alone is a weaker condition than the primary-lane observable-principle
curvature, because the diagonal Z_3 charges cancel and the Plancherel
pairing becomes blind to the flavor index. The additional structural
content that closes the primary lane (Dirac spectral amplitudes on the
APBC block, observable-principle curvature `K_{ij}`) is NOT
reconstructible from Z_3 characters alone, which sharpens rather than
weakens the primary-lane claim.

## Honest labeling of what remains open

This note does not close:

- The primary-lane Koide-cone forcing (item 3 of the attack chain):
  that still requires one of the candidate mechanisms A / B / C from
  [charged-lepton-koide-cone-2026-04-17.md §Step 6](../.claude/science/derivations/charged-lepton-koide-cone-2026-04-17.md)
  to be promoted to theorem status.
- The residual-ratio extraction (item 5 of the attack chain): the
  position `phi` of the physical charged-lepton vector on the Koide
  cone is NOT constrained by the Z_3-source-response kernel constructed
  here.
- The uniqueness theorem for the charged-lepton ray (item 4 of the
  attack chain): the Z_3 source-response kernel confirms
  uniqueness-of-Z_3-invariant-pairing up to scale, which is a strictly
  weaker statement than uniqueness-of-the-charged-lepton-ray.
- Any statement about whether the same Z_3 source-response construction
  applied to the down-type quark sector, the up-type quark sector, or
  the neutrino sector would or would not force a Koide-like outcome in
  those sectors.

## What this does NOT claim

- This cross-check does **not** claim that Z_3 invariance is vacuous on
  the retained `hw=1` triplet. It is a nontrivial structural constraint
  (the three source pairs being distinct mod 3 is an input condition).
  The cross-check claim is narrower: for this specific canonical source
  construction with the canonical left/right charges, the resulting
  bilinear kernel is proportional to the identity and therefore
  degenerate.
- It does **not** claim that all possible Z_3-invariant source-response
  kernels on `H_hw=1` are trivial. A different Cl(3)-charged source
  construction -- for example, linear combinations of the character
  idempotents with Cl(3)-valued coefficients beyond the pure-projector
  form, or sources coupling multiple hw sectors -- could give a
  nontrivial kernel. The claim is restricted to the canonical pure
  Cl(3)-charge idempotent source `s_i = e_{q_L(i)} (x) e_{q_R(i)}` used
  here.
- It does **not** claim that the primary-lane Koide derivation is
  redundant, wrong, or numerically unsupported. The INDEPENDENT verdict
  means the Z_3 character route and the observable-principle curvature
  route carry genuinely different structural content; the primary lane
  is not merely a restatement of Z_3 invariance.
- It does **not** import any observed charged-lepton mass, quark mass,
  Yukawa coupling, or any other fitted flavor datum. Only framework-
  native integer Z_3 charges and the Plancherel pairing on `C[Z_3]` are
  used.

## Paper-safe wording

> As an independent structural check of the charged-lepton mass-vector
> hypothesis, we constructed the Z_3-invariant bilinear source-response
> kernel on the retained `hw=1` triplet, with sources given by the
> tensor products of the left/right Z_3-character idempotents at the
> canonical charge assignment `(0, +1, -1)` and `(0, -1, +1)`. The
> Plancherel pairing on `C[Z_3]` then yields `S = I_3`. Its spectrum is
> triply degenerate, so Z_3 invariance by itself does not select any
> direction on the Koide cone. We therefore record an INDEPENDENT
> verdict: the cross-check does not contradict the primary
> observable-principle derivation, but it does not reproduce it either.
> The structural content that forces the charged-lepton ray onto the
> Koide cone lives in the observable-principle curvature kernel of the
> primary lane and NOT in the Z_3 character data alone. This sharpens
> rather than weakens the primary claim: the Dirac spectral amplitudes
> and the `log|det(D + J)|` curvature are essential inputs and cannot be
> absorbed into Z_3 invariance.

## Dependency contract

Every input used in the cross-check is framework-native and symbolic:

- `C[Z_3]` generator and cyclic shift `T` (exact integer matrix);
- character idempotents `e_q` built from `omega = exp(2 pi i / 3)` with
  symbolic reduction `1 + omega + omega^2 = 0`;
- left/right Z_3 charge assignment from
  [THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md);
- Plancherel pairing `<a, b> = Tr(a^dagger b)` on the regular
  representation;
- no observed masses, Yukawas, mixing angles, or fitted constants.

Retained authorities that frame this cross-check (revalidation contract
per the hypothesis scope):

- [THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md) --
  supplies the canonical left/right Z_3 charge assignment;
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) --
  establishes the retained `hw=1` triplet algebra `M_3(C)` on which the
  bilinear kernel is restricted;
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) --
  the primary-lane authority for the `log|det(D+J)|` curvature kernel
  whose shape the cross-check compares against.

Before this cross-check is trusted at the paper level, each of those
retained authorities must re-pass its own authority runner on the same
branch, per the hypothesis scope's top-to-bottom revalidation
requirement.

## Validation

- [frontier_charged_lepton_z3_source_response_crosscheck.py](../scripts/frontier_charged_lepton_z3_source_response_crosscheck.py): `PASS=41`, `FAIL=0`, verdict `INDEPENDENT`.

The runner prints a final line

    Z3_CROSSCHECK_AGREES_WITH_PRIMARY=INDEPENDENT

which is the machine-readable verdict tag for downstream wrapper runners
(in particular item 7 of the attack chain,
`frontier_charged_lepton_mass_vector_end_to_end.py` when it is spun up).

## Next steps from this cross-check

- Route the charged-lepton mass-vector attack entirely through the
  primary lane (items 1-5 of the hypothesis experiment chain), because
  Option D confirms that the Z_3-character data alone is insufficient.
- Preserve this note as the negative-independence authority in the null
  rejection audit (item 8), documenting that the algebraic-permissiveness
  null has been exhibited explicitly in the simplest honest Z_3-only
  setting (`S = I_3`), and therefore the primary lane's forcing content
  cannot be an artifact of Z_3 invariance alone.
- If a later structural upgrade produces a nontrivial Cl(3)-charged
  source beyond the pure character idempotent form `s_i = e_{q_L} (x) e_{q_R}`,
  rerun this cross-check in the extended setting to see whether Option D
  recovers non-degeneracy (potentially flipping the verdict to TRUE).
