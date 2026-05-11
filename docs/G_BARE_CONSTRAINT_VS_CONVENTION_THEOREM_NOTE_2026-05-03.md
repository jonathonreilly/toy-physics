# g_bare Constraint vs Convention Disambiguation Theorem

**Date:** 2026-05-03
**Claim type:** positive_theorem
**Status:** unaudited candidate. This note is graph-visible only so the
independent audit lane can decide whether the candidate is retained. Do not
update or promote `G_BARE_DERIVATION_NOTE.md` or downstream status surfaces
from this note unless this row, the rescaling-freedom row, and their declared
dependency chain become retained-grade through independent audit.
**Primary runner:** `scripts/frontier_g_bare_derivation.py`

## 0. Audit context

This note is repair target #3 of the
`G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02` packet, which
identified the unresolved constraint-vs-convention ambiguity in the parent
`G_BARE_DERIVATION_NOTE.md` row. The repair target was:

> *"the decisive step identifies the canonical Cl(3) connection
> normalization with unit gauge coupling, while the note explicitly leaves
> open whether that is a constraint or a convention."*

The present note proposes a disambiguation of the two readings by exhibiting the precise
sense in which `g_bare = 1` is a structural constraint (relative to the
framework's canonical Cl(3) connection normalization), and locating the
honest convention layer one level upstream: at the canonical normalization
itself, not at `g_bare`.

## 1. Claim scope

> **Theorem (Constraint-vs-convention disambiguation).**
> Let
> ```
> Tr(T_a T_b) = delta_{ab} / 2                                     (CN)
> ```
> be the canonical Cl(3) connection normalization on the canonical triplet
> block carried by `CL3_COLOR_AUTOMORPHISM_THEOREM.md` (two-hop dep via the
> rescaling-freedom-removal theorem below),
> and let the rescaling-freedom-removal theorem
> [`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md)
> apply: under (CN) the Wilson plaquette small-a matching forces
> ```
> beta = 2 N_c / g_bare^2.                                         (WM)
> ```
> Then:
>
> 1. **Structural constraint.** The unique value of `g_bare` compatible with
>    (CN) and (WM) at `N_c = 3` and `beta = 2 N_c = 6` is `g_bare = 1`. Any
>    alternative `g_bare != 1` either (a) violates (CN) by introducing a
>    `c != 1` generator dilation (forbidden by the rescaling-freedom-removal
>    theorem), OR (b) requires importing an external scale beyond the
>    framework axioms `A1` (Cl(3)) and `A2` (Z^3). In either case, the
>    alternative is not a free convention within the framework.
>
> 2. **Honest convention layer.** The convention status of `g_bare = 1` is
>    not at `g_bare` itself; it is one level upstream, at the canonical
>    normalization (CN). With (CN) treated as an admitted convention (its
>    classification on the
>    `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`
>    surface), `g_bare = 1` follows as a structural constraint, not a
>    separate convention choice.
>
> Equivalently: the framework has one canonical normalization convention
> (CN), and `g_bare = 1` is its derived constraint. There is no second,
> independent `g_bare` convention layer.

The theorem **does not** claim:

- that the canonical normalization (CN) is itself uniquely forced by the
  framework axioms (the convention-vs-derivation status of (CN) is
  precisely what the narrow convention theorem documents as an admitted
  convention);
- that the Wilson plaquette action form is uniquely forced (see Claim 3
  caveat in `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`);
- closure of the deeper question of whether the framework's normalization
  axioms `A4` are themselves derivable from `A1 + A2` alone.

## 2. Declared audit dependency (one hop)

| Authority | Audit-lane status | Role |
|---|---|---|
| [`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md) | unaudited (proposed positive_theorem in same PR) | provides the load-bearing identity that the rescaling A -> c * A under (CN) shifts beta = c^2 * beta, leaving g_bare unchanged. Without this identity, the alternative-g_bare reading (a) would be open. |

The single one-hop dep is the rescaling-freedom-removal theorem proposed
in the same PR. Its dep on `cl3_color_automorphism_theorem` propagates as
two-hop. The present theorem does not introduce any further admitted
convention or fitted selector; the entire convention layer is
encapsulated by the rescaling-freedom-removal theorem's dep chain.

## 3. Load-bearing step (class A)

```text
Given:
  (CN) Tr(T_a T_b) = delta_{ab} / 2     (admitted convention layer; carried
                                         by cl3_color_automorphism_theorem
                                         via the rescaling-freedom-removal
                                         theorem dep)
  (WM) beta = 2 N_c / g_bare^2          (Wilson small-a matching;
                                         derived in the runner Section C)
  (RR) Rescaling-freedom-removal theorem (one-hop dep): under (CN), the
       continuum rescaling A -> c * A shifts beta = c^2 * beta, with
       g_bare unchanged; alternative g_bare values either violate (CN)
       (case a) or require an external scale (case b).

At N_c = 3, the canonical normalization (CN) places the connection on
the operator-valued one-form A_op = sum_a A^a T_a with no pre-factor
g_bare. The Wilson small-a matching at this normalization gives
beta = 2 N_c = 6, and the unique compatible g_bare^2 follows by exact
algebra:

  g_bare^2 = 2 N_c / beta = 6 / 6 = 1                       (class A)

i.e., g_bare = 1.

For any alternative g_bare^2 != 1 at the same N_c = 3:
  case (a): the alternative requires a generator dilation T_a -> c T_a
            with c^2 = g_bare^(-2) != 1, which violates (CN).
  case (b): the alternative requires keeping (CN) but supplying an
            external scale that introduces beta != 2 N_c at fixed
            normalization. A1 (Cl(3) algebra anticommutator) and A2
            (Z^3 substrate) provide no such scale; supplying one would
            require an additional axiom or external import.

Therefore: the unique g_bare consistent with the framework axioms +
canonical normalization (CN) is g_bare = 1, which is a structural
constraint relative to (CN). The honest convention layer is (CN)
itself (a single convention), not g_bare (no separate convention).
```

The load-bearing step is class (A) — algebraic substitution into the
matching identity (WM), specialized to the canonical normalization (CN)
at `N_c = 3`. No admitted convention beyond (CN) is load-bearing for the
conclusion.

## 4. Why this differs from the narrow convention theorem

The existing
`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`
classifies `g_bare = 1` itself as an admitted Wilson canonical-normalization
convention, settling that the narrow theorem's status row is honest about
its convention layer. The narrow convention theorem **does not** claim
that `g_bare = 1` is structurally forced; it explicitly classifies it as
a convention.

The present theorem is the complementary *constraint reading*: with the
canonical Cl(3) connection normalization (CN) carried at the
`cl3_color_automorphism_theorem` row treated as the admitted convention
layer, `g_bare = 1` follows as a structural constraint, not as a separate
convention. The two readings of the parent
`G_BARE_DERIVATION_NOTE.md` are reconciled as follows:

- **Convention reading (narrow theorem):** `g_bare = 1` is itself the
  Wilson canonical convention. The convention layer is at `g_bare`.
- **Constraint reading (present theorem):** the convention layer is at
  the canonical Cl(3) normalization (CN). With (CN) fixed, `g_bare = 1`
  is a derived constraint.

The two readings are not contradictory — they place the convention layer
at different levels of the chain. The narrow theorem accepts the
convention status as a Wilson-action-side admission; the present theorem
moves the convention status one level upstream (to the Cl(3) generator
basis) and shows that, once that upstream convention is fixed,
`g_bare = 1` is structurally forced.

The honest disambiguation: **`g_bare = 1` is a constraint relative to the
canonical Cl(3) connection normalization, which is itself the convention
layer.**

## 5. Verification

```bash
python3 scripts/frontier_g_bare_derivation.py
```

Verifies, in `Section E` of the runner:

1. The canonical `beta = 2 N_c = 6` for `SU(3)` is computed exactly via
   `Fraction` arithmetic.
2. The unique `g_bare^2 = 2 N_c / beta = 1` is derived as a class (A)
   exact rational.
3. Alternative `g^2` values (`1/2`, `2`, `4`) require `beta != 6`,
   incompatible with the canonical normalization-forced `beta = 2 N_c`.
4. The convention layer is explicitly identified: canonical
   `Tr(T_a T_b) = delta/2` is the framework normalization, carried by
   `cl3_color_automorphism_theorem`.
5. The constraint layer is explicit: given the canonical normalization,
   `g_bare = 1` is structurally forced, with no separate `g_bare`
   convention layer.

Representative runner checks:

```
[PASS] canonical beta = 2 N_c = 6 for SU(3) (exact)
[PASS] given canonical normalization + beta = 6, g_bare^2 = 1 forced (exact)
[PASS] alternative g^2 = 1/2 requires beta = 12 != 6
[PASS] alternative g^2 = 2 requires beta = 3 != 6
[PASS] alternative g^2 = 4 requires beta = 3/2 != 6
[PASS] convention layer: canonical Tr(T_a T_b) = delta_ab/2 is the framework normalization
[PASS] constraint layer: given canonical normalization, g_bare = 1 is structurally derived
```

## 6. Audit-lane disposition (proposed)

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  g_bare = 1 is a structural constraint (not a separate convention choice)
  relative to the canonical Cl(3) connection normalization
  Tr(T_a T_b) = delta_ab/2, which itself is the admitted framework
  convention carried by cl3_color_automorphism_theorem (via the
  rescaling-freedom-removal theorem dep). The disambiguation locates the
  convention layer one level upstream from g_bare: there is one
  canonical-normalization convention, and g_bare = 1 is its derived
  constraint.
proposed_load_bearing_step_class: A
declared_one_hop_dep: g_bare_rescaling_freedom_removal_theorem_note_2026-05-03
audit_required_before_effective_retained: true
parent_update_allowed_only_after_retained: true
```

Audit status is set only by the independent audit lane. This note may land as
an unaudited, graph-visible positive_theorem candidate; retained-family
effective status requires independent audit of this row and retained-grade
closure of the declared dependency chain. The parent
`G_BARE_DERIVATION_NOTE.md` must not be updated or promoted from this
candidate before that happens.

## 7. What this candidate can support after retention

- The constraint-vs-convention ambiguity named on the parent
  `G_BARE_DERIVATION_NOTE.md` row, if independent audit retains this
  candidate and its dependency chain.
- A candidate answer for repair target #3 from
  `G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02`.
- A clean handoff to downstream rows depending on `g_bare = 1`: such
  rows may cite this note for the constraint reading only after retention;
  until then they should keep the current conditional/convention wording.

## 8. What this theorem does NOT close

- The convention-vs-derivation status of the canonical Cl(3) normalization
  (CN) itself. This is **not** closed here; it is precisely what the narrow
  convention theorem documents as an admitted convention layer. Promoting
  (CN) from convention to derivation would require closing the deeper
  question of whether the canonical Gell-Mann normalization is uniquely
  forced by Cl(3) algebraic structure alone — a separate Nature-grade
  target outside the present scope.
- The choice of the Wilson plaquette action form (Symanzik / improved
  actions remain outside this scope; see
  `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md` Claim 3).
- The deeper question of whether `A4` (the framework's canonical
  normalization axiom) is derivable from `A1 + A2` alone.
- The retained promotion of `G_BARE_DERIVATION_NOTE.md` itself; this
  candidate queues one of the three named repair targets for audit but does
  not close the full promotion pathway.

## 9. Honest scoping summary

The genuine science: the parent's "constraint or convention?" question is
ambiguous because it conflates two distinct convention layers. There is
exactly *one* admitted convention layer in the framework's `g_bare` chain:
the canonical Cl(3) connection normalization `Tr(T_a T_b) = delta/2`,
carried by `cl3_color_automorphism_theorem`. Once that single convention
is fixed:

- the rescaling-freedom-removal theorem (the one-hop dep) shows that the
  continuum rescaling `A -> c * A` cannot rescue an alternative `g_bare`
  (case a in the load-bearing step);
- the framework axioms `A1 + A2` provide no external scale that could
  introduce an alternative `g_bare` (case b);

so the unique compatible value is `g_bare = 1`, derived as a class (A)
algebraic constraint.

What this theorem is honestly **not**: a derivation of (CN) itself from
`A1 + A2`. The upstream convention status of (CN) remains an open
foundational question, separately tracked. If retained by independent audit,
this theorem would close the *relative* constraint reading; the *absolute*
derivation of `g_bare = 1` from `A1 + A2` alone (independent of the canonical
normalization) is a strictly stronger Nature-grade target outside the present
scope.

## 10. Cross-references

The declared one-hop dependency is the rescaling-freedom-removal theorem,
linked once in section 2. The remaining cross-references are reader pointers
(plain text, not load-bearing for the citation graph):

- Parent: `G_BARE_DERIVATION_NOTE.md` — may cite this candidate only after
  this row and its dependency chain are retained by independent audit.
- `G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md` — the
  demotion / status correction packet that names the three repair targets.
- `CL3_COLOR_AUTOMORPHISM_THEOREM.md` — two-hop dep (carries the canonical
  Gell-Mann generator basis).
- `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md` — the
  complementary convention-reading narrow theorem (g_bare = 1 itself
  classified as an admitted Wilson convention). The two readings are
  reconciled in Section 4 above.
- `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md` — the
  broader Cl(3) -> End(V) -> su(3) -> Wilson chain.
- `G_BARE_RIGIDITY_THEOREM_NOTE.md` — upstream rigidity theorem (no scalar
  dilation of T_a, used in the rescaling-freedom-removal theorem).
- `MINIMAL_AXIOMS_2026-04-11.md` — `A4` records the canonical normalization
  as the framework's normalization-and-evaluation surface input. The
  present theorem clarifies the relationship between `A4` and `g_bare = 1`.

## 11. Current audit-lane disposition (informational)

This row was audited on 2026-05-05 by `codex-audit-loop-gpt5-20260505` and
returned `audited_conditional`. The chain-closure rationale recorded in the
ledger is:

> *The algebra closes locally, but the one-hop rescaling-freedom-removal
> authority is not retained-grade; it is currently an audited decoration
> boxed under `cl3_color_automorphism_theorem`.*

The named one-hop dep
[`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md)
carries effective status `decoration_under_cl3_color_automorphism_theorem`.
That is a terminal classification under the audit lane, so this row's
conditional status cannot be lifted along the rescaling-freedom path without
re-architecting the dep chain. The local algebra (class A substitution into
the canonical Wilson matching identity) is unchanged; only the upstream
authority status is the gating issue.

Independent of this row, the audit lane has a separate Ward-route program
that reaches `g_bare = 1` via different upstream authorities — see
[`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md)
(now `retained_bounded`) and
`G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`
(`audited_conditional`; see-also cross-reference, not a load-bearing
dependency — backticked to break cycle-0001 in the citation graph).
That route is **not** the rescaling-freedom path
this note depends on; it is a parallel disambiguation that does not change
this row's intrinsic dep chain. Cross-reference only — the present theorem
remains scoped to the rescaling-freedom reading and is not promoted by the
parallel Ward-route work.
