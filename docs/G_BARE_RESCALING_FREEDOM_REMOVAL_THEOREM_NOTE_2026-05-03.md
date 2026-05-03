# g_bare Rescaling-Freedom Removal Theorem (Cl(3) Canonical Normalization)

**Date:** 2026-05-03
**Claim type:** positive_theorem
**Status:** unaudited candidate. This note is graph-visible only so the
independent audit lane can decide whether the candidate is retained. Do not
update or promote `G_BARE_DERIVATION_NOTE.md` or downstream status surfaces
from this note unless this row and its declared dependency chain become
retained-grade through independent audit.
**Primary runner:** `scripts/frontier_g_bare_derivation.py`

## 0. Audit context

This note is repair target #2 of the
`G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md` packet, which
identified the missing theorem that removes the continuum-gauge-theory
`A -> A/g` rescaling freedom on the framework's canonical Cl(3) connection
normalization surface. The repair target was:

> *"supply a retained theorem that removes the A -> A/g rescaling
> freedom."*

The present note is a theorem candidate, scoped narrowly enough that the
load-bearing step is a class (A) algebraic identity on the canonical
`Tr(T_a T_b) = delta_ab / 2` normalization carried by the framework's
[`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md) row.

## 1. Claim scope

> **Theorem (Rescaling-freedom removal).**
> Let `T_a` be the canonical orthonormal Hermitian generators of `su(3)` on the
> canonical triplet block, normalized by
> ```
> Tr(T_a T_b) = delta_{ab} / 2                                     (CN)
> ```
> as carried by `CL3_COLOR_AUTOMORPHISM_THEOREM.md`.
> Let `A_op = sum_a A^a T_a` be the operator-valued connection. Then the
> continuum-gauge-theory rescaling
> ```
> A -> c * A,    with c in R, c != 1                               (RES)
> ```
> applied to the operator basis `T_a -> c * T_a` produces a new generator
> Gram `Tr((c T_a)(c T_b)) = c^2 delta_{ab} / 2`, which violates (CN). The
> Wilson plaquette small-a matching condition
> ```
> beta = 2 N_c / g_bare^2                                          (WM)
> ```
> then transforms as `beta -> c^2 * beta`, leaving `g_bare` unchanged. In
> particular: under (CN), the rescaling (RES) is not a free reparametrization
> of `g_bare`; it is a violation of (CN) that shifts the action coefficient
> `beta`.
>
> Equivalently, on the (CN)-fixed surface, `g_bare` carries no independent
> scalar freedom: the rescaling redundancy of the abstract continuum gauge
> theory is removed.

The theorem **does not** claim:

- that the canonical normalization (CN) is itself uniquely forced by the
  framework axioms (the convention-vs-derivation status of (CN) is the
  subject of `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`,
  not this note);
- that the Wilson plaquette action form is uniquely forced by Cl(3)
  structure (see `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`
  Claim 3 for the explicit caveat);
- closure of the broader G_BARE_* family or the deeper gauge-coupling
  derivation lane.

## 2. Declared audit dependency (one hop)

| Authority | Audit-lane status | Role |
|---|---|---|
| [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md) | unaudited at rendered ledger; reviewed exact algebraic support theorem on current main | provides the canonical Gell-Mann generators with `T_F = 1/2` (i.e., `Tr(T_a T_b) = delta_{ab} / 2`) on the canonical triplet block, anchoring the (CN) normalization used in the load-bearing step |

The single one-hop dep is the canonical Cl(3) color automorphism / generator
basis, which already carries `T_F = 1/2`. No other live note is load-bearing
for the present theorem.

## 3. Load-bearing step (class A)

```text
Given:
  Tr(T_a T_b) = delta_{ab} / 2     (CN, from cl3_color_automorphism)
  A_op  = sum_a A^a T_a            (operator-valued connection)
  beta = 2 N_c / g_bare^2          (WM, Wilson small-a matching;
                                    derived in section C of the runner)

Apply rescaling T_a -> c T_a, c != 1, and recompute the matched beta:
  Tr((c T_a)(c T_b)) = c^2 delta_{ab} / 2                    (violates CN)
  Tr((c F)^2)        = c^2 Tr(F^2)
  beta_new           = c^2 * (2 N_c / g_bare^2)               (matched)
                     = c^2 * beta_old                          (class A algebra)

Conclusion (class A algebraic identity):
  beta_new / beta_old = c^2,  WITH g_bare UNCHANGED.

Therefore: under (CN), the rescaling (RES) is not a free reparametrization
of g_bare; it is a (CN)-violating shift in beta. With (CN) held fixed,
g_bare carries no independent scalar freedom.
```

The load-bearing step is class (A) — algebraic substitution on the canonical
trace normalization (CN) carried by `cl3_color_automorphism_theorem`. No
admitted convention, observed value, or fitted selector is load-bearing for
the conclusion.

## 4. Why this differs from the existing rigidity theorem

The existing `G_BARE_RIGIDITY_THEOREM_NOTE.md`
proves that the canonical generator basis admits no scalar dilation
ambiguity once the Hilbert-Schmidt trace form is fixed. The present
theorem packages a different, narrower statement: *given* the canonical
trace normalization (CN), the rescaling freedom of the abstract continuum
gauge theory routes itself into `beta`, not `g_bare`. The two theorems are
complementary:

- the rigidity theorem addresses the *generator-basis* freedom (no scalar
  dilation of `T_a`);
- the present candidate addresses the *connection-rescaling* freedom (no
  scalar rescaling of `A` that lives in `g_bare` rather than `beta`).

Both are needed to remove the full continuum rescaling redundancy. The
rigidity theorem is the upstream input; the present theorem is the
downstream consequence on the Wilson-action surface.

## 5. Verification

```bash
python3 scripts/frontier_g_bare_derivation.py
```

Verifies, in `Section D` of the runner:

1. Rescaling `T_a -> c T_a` with `c in {1/2, sqrt(2), 2, 3}` produces
   `Gram = c^2 delta/2`, violating (CN) for every `c != 1`.
2. The matched Wilson coefficient `beta_new = c^2 * beta_old` is recovered
   exactly.
3. The matched `g_bare` is unchanged: the rescaling routes itself into
   `beta`, not into `g_bare`.

Representative runner checks:

```
[PASS] rescale T -> c T at c = 0.5000: Gram = c^2 * delta/2
[PASS] rescale T -> c T at c = 0.5000: Gram NOT equal to canonical delta/2
[PASS] rescale shifts beta by c^2 = 0.2500: beta_new = 1.5000
... (repeated for c = sqrt(2), 2, 3)
```

## 6. Audit-lane disposition (proposed)

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Under canonical Cl(3) connection normalization Tr(T_a T_b) = delta_ab/2
  (carried by cl3_color_automorphism_theorem), the continuum-gauge-theory
  rescaling A -> c * A is removed, in the precise sense that the rescaling
  shifts the Wilson coefficient beta = 2 N_c / g_bare^2 by c^2 rather than
  altering g_bare. NO claim that the canonical normalization itself is
  uniquely forced (that is a separate audit row).
proposed_load_bearing_step_class: A
declared_one_hop_dep: cl3_color_automorphism_theorem
audit_required_before_effective_retained: true
parent_update_allowed_only_after_retained: true
```

Audit status is set only by the independent audit lane. This note may land as
an unaudited, graph-visible positive_theorem candidate; retained-family
effective status requires independent audit of this row and retained-grade
closure of the declared dependency. The parent `G_BARE_DERIVATION_NOTE.md`
must not be updated or promoted from this candidate before that happens.

## 7. What this candidate can support after retention

- The continuum-gauge-theory `A -> A/g` rescaling-freedom objection on the
  canonical Cl(3) connection normalization surface, in the precise sense
  that any nontrivial rescaling shifts `beta` rather than introducing
  `g_bare` freedom.
- A clean class (A) algebraic identity that the `g_bare = 1` lane can cite
  only after this row and its dependency chain are retained by independent
  audit.
- A candidate answer for repair target #2 from
  `G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02`.

## 8. What this theorem does NOT close

- The convention-vs-derivation status of the canonical normalization
  itself (carried by the narrow convention theorem
  `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`).
- The choice of the Wilson plaquette action form (Symanzik / improved
  actions remain outside this scope; see
  `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md` Claim 3).
- The deeper question of whether the canonical Cl(3) normalization is
  uniquely forced by Cl(3) algebraic structure alone (a separate
  Nature-grade target).
- The downstream `g_bare = 1` retention claim by itself; this theorem
  queues one named obstruction (rescaling freedom) for audit but is not the
  only step required for any later parent promotion.

## 9. Cross-references

The declared one-hop dependency is the cl3_color_automorphism row, linked once
in section 2. The remaining cross-references are reader pointers (plain text,
not load-bearing for the citation graph):

- Parent: `G_BARE_DERIVATION_NOTE.md` — may cite this candidate only after
  this row and its dependency chain are retained by independent audit.
- `G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md` — the
  demotion / status correction packet that names the three repair targets.
- `G_BARE_RIGIDITY_THEOREM_NOTE.md` — upstream rigidity theorem (no scalar
  dilation of `T_a`). This note is the downstream Wilson-action consequence.
- `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md` — the broader
  Cl(3) -> End(V) -> su(3) -> Wilson chain. Section C of that note covers
  the same plaquette small-a matching used here.
- `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md` — the
  sister narrow theorem classifying the canonical normalization itself
  as an admitted convention.
- `G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md` — the
  companion theorem (repair target #3) that uses the present theorem
  as a one-hop input.

## 10. Honest scoping summary

The theorem is genuinely narrow: it is a class (A) algebraic identity that
holds *given* the canonical Cl(3) connection normalization. It does NOT
upgrade the convention status of the canonical normalization itself; that
remains an admitted convention layer carried by
`cl3_color_automorphism_theorem` and clarified by the narrow convention
theorem. The novelty is the explicit packaging of the rescaling-freedom
removal as a standalone audit-ready positive theorem candidate, separating two
distinct objections that the existing literature had bundled together:

1. *generator-basis dilation* (addressed by the rigidity theorem),
2. *connection rescaling* (queued here for independent audit),

and exposing the residual convention-vs-derivation status of the canonical
normalization itself as the cleanly named remaining boundary.
