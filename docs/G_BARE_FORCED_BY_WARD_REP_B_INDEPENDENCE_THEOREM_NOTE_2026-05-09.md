# g_bare Forced (Not Chosen) via Ward Rep-B-Independence — Upgrade Theorem

**Date:** 2026-05-09
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Primary runner:** [`scripts/frontier_g_bare_canonical_convention_narrow.py`](../scripts/frontier_g_bare_canonical_convention_narrow.py)
**Role:** upgrades the canonical convention narrowing
[`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md)
to a forced determination by leveraging the retained two-Ward Rep-B
bare-scale independence theorem.

## 0. Honest scoping

The retained Ward Rep-B-independence theorem
[`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md)
(audit status: `retained_bounded`, cross-confirmed) proves a precise tree-level
identity: the unit-normalized scalar-singlet form factor `F_Htt^(0)(g_bare) =
<0|H_unit|t̄ t>_tree` evaluates to `1/sqrt(6)` for **all** `g_bare`. That
identity does not by itself solve for `g_bare`; it only establishes that the
Rep-B side of the same-1PI pinning identity is `g_bare`-independent.

The complementary Path-2 ingredient is supplied by the same-1PI pinning
theorem
[`G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md)
(audit status: `audited_conditional` at the time of writing), which equates
the same projected `Γ_S^(4)` four-fermion coefficient computed two ways and
solves `g_bare^2 = 1`.

The present note's upgrade is therefore conditional on the same-1PI pinning
theorem becoming retained-grade. The bounded conditional statement is review
clean: the load-bearing algebra is class (A) substitution into one retained
identity and one still-conditional candidate identity. The note does **not** claim that a
single retained authority alone forces `g_bare = 1`.

## 1. Claim scope

> **Theorem (Forced determination of `g_bare`, conditional on same-1PI
> pinning).** Fix the retained `Cl(3) × Z^3` Wilson-plaquette + staggered-
> Dirac bare action on the `Q_L = (2,3)` block, with `Q_L`-block field
> content fixed by the retained narrow authorities. Then, **assuming**
> 1. the retained Ward Rep-B-independence identity
>    `F_Htt^(0)(g_bare) = 1/sqrt(6)` for all `g_bare`
>    (carried by [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md),
>    `retained_bounded`); **and**
> 2. the same-1PI pinning identity `F_Htt^(0)(g_bare)^2 = g_bare^2/(2 N_c)`
>    for arbitrary `g_bare` on the same retained block
>    (carried by [`G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md),
>    `audited_conditional`),
>
> the unique `g_bare` consistent with the retained Rep-B identity and
> the same-1PI candidate identity is
> ```
> g_bare = 1                                                          (FD)
> ```
> as a class (A) algebraic constraint at `N_c = 3`. The canonical Wilson
> normalization `g_bare = 1` is therefore **not a free convention choice**
> within the framework: it is forced by the joint Rep-B form-factor identity
> and the same-1PI coefficient identity on the retained block.

The theorem **does not** claim:

- that `g_bare = 1` follows from the Ward Rep-B-independence theorem alone
  (it does not — Rep-B-independence proves the Rep-B side is `g_bare`-flat,
  not that `g_bare` itself is forced);
- that the same-1PI pinning theorem is itself retained-grade (it is currently
  `audited_conditional`; the upgrade is conditional on its retention);
- closure of the broader `G_BARE_*` family or the Nature-grade absolute
  derivation of `g_bare = 1` from `A1 + A2` alone (the upstream Layer-L3
  convention scalar `N_F = 1/2` remains the framework's single admitted
  convention, as documented in
  `G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`
  (reader pointer; see-also cross-reference, not a load-bearing dependency
  of this Ward-route upgrade));
- that the historical narrow convention reading
  ([`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md))
  was incorrect — its scoped claim (`β = 6` given `g_bare = 1` admitted as a
  convention) remains valid; the upgrade is that, conditional on the two
  Ward-route inputs, the convention itself is not a free choice.

## 2. Upgrade chain (one-paragraph statement)

The retained Rep-B-independence theorem proves that the tree-level scalar-
singlet form factor on `Q_L` is `1/sqrt(6)` regardless of `g_bare`. The
same-1PI pinning theorem proves that the same retained projected `Γ_S^(4)`
coefficient on the same block, computed off-surface via bare-action Feynman
rules, equals `g_bare^2/(2 N_c)` regardless of `g_bare`. Because the two
expressions are two algebraically equivalent representations of the same
amputated Green's-function coefficient on the same retained block, equating
them yields `g_bare^2/(2 N_c) = 1/6`, hence `g_bare^2 = 1` at `N_c = 3`. On
the positive bare-coupling branch this is `g_bare = 1`. The upgrade therefore
relabels the canonical Wilson normalization from "admitted convention" to
"derived constraint" — under the Ward-route authorities once the same-1PI
row is retained — and
demotes the historical convention narrowing
([`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md))
to a corollary that is superseded once the same-1PI pinning row reaches
retained-grade audit status.

## 3. Declared audit dependencies (one hop)

| Authority | Audit-lane status | Role |
|---|---|---|
| [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md) | `retained_bounded` in the current audit ledger | provides the `g_bare`-independent Rep-B form factor `F_Htt^(0)(g_bare) = 1/sqrt(6)` |
| [`G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md) | `audited_conditional` | provides the same-1PI coefficient identity `F_Htt^(0)(g_bare)^2 = g_bare^2/(2 N_c)` for arbitrary `g_bare` |

The conditional upgrade would close under both authorities if both are
retained-grade. The current `audited_conditional` status of the same-1PI
pinning row is acknowledged in the bounded scope: until that row is
ratified, this candidate remains chain-blocked and cannot promote a parent
status surface.

## 4. Load-bearing step (class A)

```text
Inputs (cited at one-hop):
  (W1) F_Htt^(0)(g_bare) = 1 / sqrt(6)            (retained Ward Rep-B,
                                                   for all g_bare)
  (W2) F_Htt^(0)(g_bare)^2 = g_bare^2 / (2 N_c)   (same-1PI pinning,
                                                   for all g_bare)
  (NC) N_c = 3                                    (graph_first_su3)

Substitute (W1) into the LHS of (W2):
  (1 / sqrt(6))^2 = g_bare^2 / (2 N_c)
  1 / 6           = g_bare^2 / (2 · 3)
  1 / 6           = g_bare^2 / 6
  g_bare^2        = 1                              (class A algebraic)

Positive bare-coupling branch:
  g_bare = 1.                                      (FD)

Therefore the canonical Wilson normalization g_bare = 1 is a forced
determination, not a free convention, within the retained block under
the cited two Ward-route authorities.
```

The load-bearing step is class (A) — algebraic substitution into two retained
or candidate identities. No new admitted convention, no new fitted selector,
and no new physics input is introduced beyond the two cited rows.

## 5. Relationship to the convention narrowing

The historical narrow convention reading
[`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md)
classified `g_bare = 1` itself as the Wilson canonical-normalization
convention. Under the present upgrade chain, that classification is
superseded:

- **Convention reading (narrow, 2026-05-02):** `g_bare = 1` is itself the
  Wilson canonical convention; it could in principle have been any other
  positive value within Wilson conventions, but the framework adopts `1`.
- **Forced determination (present, 2026-05-09):** `g_bare = 1` is the unique
  positive solution of `g_bare^2 / (2 N_c) = 1/6` at `N_c = 3`, given the
  retained Rep-B form factor and the same-1PI coefficient identity. It is
  therefore not a free choice.

The two readings are reconcilable as follows: the narrow convention reading
is **honest within its scoped scope** (it explicitly classifies `g_bare = 1`
as an admitted convention without claiming uniqueness), but it is **not
maximally tight**. The present upgrade tightens the framework's `g_bare`
status from "admitted convention" to "forced determination" by leveraging
the retained Ward Rep-B-independence theorem and the same-1PI pinning theorem
that the framework already carries.

The four-layer stratification of
`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`
(reader pointer; see-also cross-reference, not a load-bearing dependency
of this Ward-route upgrade)
remains in place: the framework's single admitted convention is at Layer L3
(the overall HS scalar `N_F = 1/2`), and the present note adds an independent
route to the same conclusion that `g_bare = 1` is a derived (not admitted)
quantity — this time via the Ward two-route off-surface argument rather than
the Wilson small-`a` matching argument used by the L3 framing.

## 6. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_g_bare_canonical_convention_narrow.py
```

The runner now verifies, in addition to the original convention checks:

1. The Ward Rep-B form factor `F_Htt^(0) = 1/sqrt(6)` (cited identity W1) is
   `g_bare`-independent across a representative grid of bare-coupling values
   `g_bare ∈ {1/2, 1, 2, 3, 7/11}`.
2. The same-1PI coefficient identity `F_Htt^(0)^2 = g_bare^2 / (2 N_c)`
   (cited identity W2) is checked algebraically: substituting `F_Htt^(0) =
   1/sqrt(6)` and `N_c = 3` yields `g_bare^2 = 1`.
3. The forced determination `g_bare^2 = 1` is invariant under the
   representative grid: every `g_bare^2` value in the grid that does not
   equal `1` produces a contradiction with `F_Htt^(0)^2 = 1/6`, confirming
   the unique solution.

Representative runner checks:

```
[PASS] Rep-B form factor F_Htt^(0) = 1/sqrt(6) is g_bare-independent across grid
[PASS] same-1PI identity at g_bare = 1 satisfies F_Htt^(0)^2 = 1/6 = 1/(2·3) ✓
[PASS] same-1PI identity at g_bare = 2 contradicts F_Htt^(0)^2 = 1/6 (would need 4/6 = 2/3)
[PASS] same-1PI identity at g_bare = 1/2 contradicts F_Htt^(0)^2 = 1/6 (would need 1/24)
[PASS] forced determination: unique positive g_bare with F_Htt^(0)^2 = g_bare^2/(2·3) = 1/6 is g_bare = 1
```

## 7. Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem
proposed_claim_scope: |
  Given the retained Ward Rep-B-independence theorem
  (F_Htt^(0)(g_bare) = 1/sqrt(6) for all g_bare on the retained Q_L block)
  and the same-1PI pinning theorem
  (F_Htt^(0)(g_bare)^2 = g_bare^2/(2 N_c) for all g_bare on the same block),
  the unique positive g_bare consistent with the retained Rep-B identity
  and same-1PI candidate identity at
  N_c = 3 is g_bare = 1. The canonical Wilson normalization is therefore
  a forced determination, not a free convention, within the retained
  block under the cited Ward-route authorities. Conditional on the
  same-1PI pinning row being retained-grade.
proposed_load_bearing_step_class: A
declared_one_hop_deps:
  - g_bare_two_ward_rep_b_independence_theorem_note_2026-04-19
  - g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19
audit_required_before_effective_retained: true
parent_supersession_allowed_only_after_retained: true
```

Audit status is set only by the independent audit lane. This note is safe
to land as an unaudited graph-visible bounded candidate; retained-family
effective status requires independent audit of this row and retained-grade closure of
its declared dependency chain (in particular, retention of the same-1PI
pinning row, currently `audited_conditional`).

## 8. What this candidate can support after retention

- If retained with a retained-grade dependency chain, retire the historical narrow convention reading
  [`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md)
  to a corollary scope: the `β = 6` and `F^lattice = Ω^Cl(3)` algebraic
  consequences remain valid, but the convention status of `g_bare = 1`
  is replaced by the forced-determination status of the present note.
- A clean handoff to downstream rows depending on `g_bare = 1`: such rows
  may cite this note for the forced-determination reading after retention,
  removing the convention-vs-derivation ambiguity at the `g_bare` row
  itself (the framework's single admitted convention layer remains at
  L3 / `N_F = 1/2` upstream, as documented in
  `G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md` —
  reader pointer; see-also cross-reference, not a load-bearing dependency
  of this Ward-route upgrade).

## 9. What this theorem does NOT close

- The convention status of `N_F = 1/2` itself (the Layer L3 admitted scalar
  in the four-layer stratification). That remains the single admitted
  convention in the framework's `g_bare` chain. Reclassifying `N_F = 1/2`
  from convention to derivation is a strictly stronger Nature-grade target
  outside the present scope.
- The same-1PI pinning row's own audit status. The present note depends on
  it as a one-hop authority; retention of that row is a prerequisite for
  retention of this row.
- The terminal Standard Model top-Yukawa Ward-identification readout (the
  retained Ward Rep-B theorem explicitly excludes this; the present note
  inherits the same exclusion).

## 10. Cross-references

- [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md)
  — declared one-hop dep providing the retained Rep-B form factor identity.
- [`G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md)
  — declared one-hop dep providing the same-1PI coefficient identity.
- [`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md)
  — historical narrow convention reading, superseded by the present
  forced-determination upgrade once retained.
- `G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`
  (reader pointer; see-also cross-reference, not a load-bearing dependency)
  — four-layer stratification placing the framework's single convention at
  Layer L3 (`N_F = 1/2`); the present note provides an independent route
  to the same `g_bare = 1` conclusion via the Ward two-route argument.
- `G_BARE_DERIVATION_NOTE.md` — parent row that may cite this candidate as
  the forced-determination reading after retention.

## 11. Honest scoping summary

The genuine science: the retained Ward Rep-B-independence theorem proves a
narrow tree-level identity (the form factor is `g_bare`-flat). It does not
by itself force `g_bare`. The full forced-determination conclusion requires
combining it with the same-1PI pinning theorem, which is currently
`audited_conditional`. Once that row is retained, `g_bare = 1` becomes a
class (A) algebraic consequence of two retained-grade identities — i.e., a
forced determination, not a free convention.

The framework's single remaining admitted convention layer is at L3 (the
overall HS scalar `N_F = 1/2`), as documented in the 2026-05-07 four-layer
restatement. The present note adds an independent (Ward-route) confirmation
of the L4 conclusion that `g_bare = 1` is derived, not admitted.
