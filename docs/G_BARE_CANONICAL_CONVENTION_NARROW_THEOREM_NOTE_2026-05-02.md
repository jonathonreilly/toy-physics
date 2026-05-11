# g_bare Canonical Wilson Normalization (Convention) — Narrow Theorem

**Date:** 2026-05-02
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Primary runner:** `scripts/frontier_g_bare_canonical_convention_narrow.py`

> **Supersession (2026-05-09):** the convention narrowing in this note is
> superseded — once retained — by the forced-determination upgrade in
> `G_BARE_FORCED_BY_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-05-09.md`
> (reader pointer; see-also cross-reference, not a load-bearing
> dependency of this note's narrow convention claim).
> The upgrade leverages the retained Ward Rep-B-independence theorem
> ([`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md))
> and the same-1PI pinning theorem
> (`G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`,
> see-also cross-reference, not a load-bearing dependency of this note)
> to demote `g_bare = 1` from "admitted Wilson convention" to "forced
> determination". The scoped algebraic consequences below (`β = 6`,
> `F^lattice = Ω^Cl(3)` at `g_bare = 1`) remain valid; the convention
> status of `g_bare = 1` itself is replaced by the forced-determination
> reading once the upgrade row reaches retained-grade audit status. Do
> not change this note's intrinsic status from this header — let the
> independent audit lane decide.

## Claim scope (proposed)

> **Given** the Wilson gauge-action canonical-normalization convention
> `g_bare = 1` (an admitted convention, NOT a derivation), and given
> the declared graph-first SU(3) gauge surface (from
> [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)), the Wilson
> action coefficient is
> ```
> β  =  2 N_c / g_bare²  =  2 · 3 / 1  =  6
> ```
> and the lattice field strength `F^{lattice}` is identical to the
> Cl(3) curvature `Ω^{Cl(3)}` without any rescaling factor.

The narrow theorem **explicitly classifies** `g_bare = 1` as an admitted
convention (the standard Wilson canonical-normalization choice), not as a
constraint or a derived value. The audit row's previously-named blocker —
*"the note explicitly leaves open whether that is a constraint or a
convention"* — is resolved here by stating the convention status directly.

The narrow theorem **does not** claim:

- that `g_bare = 1` is uniquely forced by Cl(3) framework axioms;
- that the Wilson canonical normalization is the only possible normalization;
- the absence of a continuum limit (a separate axiom from
  `MINIMAL_AXIOMS_2026-04-11.md`);
- closure of the broader G_BARE_* family or the gauge-coupling-derivation
  lane.

## Declared audit dependency (one-hop)

| Authority | Audit-lane status | Role |
|---|---|---|
| [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | pipeline-derived; may be audit-pending after dependency-graph strengthening | provides the graph-first SU(N_c) gauge surface with N_c = 3 from spatial dimension d = 3 |

The convention `g_bare = 1` is admitted but is **not** a load-bearing
proof input — it parameterizes the action coefficient, not the proof of
the action's closure. The conclusion `β = 6` is class (A) algebraic
substitution.

## Load-bearing step (class A)

```text
Given:
  g_bare := 1                      (admitted Wilson canonical convention)
  N_c = 3                          (retained from graph_first_su3, spatial d=3)
  Wilson action: S_W = (β/N_c) Σ_p Re Tr(I - U_p)   (standard Wilson form)
  β  ↔  g_bare relation: β = 2 N_c / g_bare²

Substitution:
  β  =  2 · 3 / 1  =  6           (class A algebraic)

Cl(3) curvature relation (admitted standard Wilson lattice gauge theory):
  F^{lattice}_μν(p)  =  (1/g_bare) · Ω^{Cl(3)}_μν(p) · (1 + O(a²))
  At g_bare = 1:  F^{lattice}  =  Ω^{Cl(3)}  (no rescaling)
```

This is class (A) — algebraic substitution into a standard Wilson formula
on the declared graph-first input.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_g_bare_canonical_convention_narrow.py
```

Verifies, at exact rational precision:

1. β = 2 N_c / g_bare² with (N_c, g_bare) = (3, 1) gives β = 6.
2. β formula is consistent for general N_c (e.g. N_c=2 → β=8, N_c=4 → β=8 with g_bare=1).
3. The Wilson formula `S_W = (β/N_c) Σ Re Tr(I - U_p)` is the standard form
   (admitted convention).
4. `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` is graph-visible via live ledger
   lookup.
5. The convention-vs-derivation distinction is explicit in note prose.

## Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem
proposed_claim_scope: |
  Given g_bare = 1 as admitted Wilson canonical-normalization convention
  + retained graph-first SU(N_c=3), the Wilson action coefficient is β = 6
  and the lattice field strength equals the Cl(3) curvature without
  rescaling. NO claim that g_bare = 1 is uniquely forced.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
```

Audit status is set only by the independent audit lane. This note is safe to
land as an unaudited, graph-visible bounded-theorem candidate; retained-family
effective status requires independent audit of this row and retained-grade
closure of its declared dependency chain.

## What this theorem closes

A clean, audit-ready statement of the Wilson canonical normalization
convention as a CONVENTION (not a derivation), resolving the parent
`G_BARE_DERIVATION_NOTE.md`'s previously-named "constraint vs convention
ambiguity." The narrow theorem provides a clean retained-bounded primitive
that downstream rows depending on `g_bare = 1` for the Wilson action
setup can cite without inheriting the conditional ambiguity, once the audit lane
ratifies this row and its dependency chain.

## What this theorem does NOT close

- The deeper question of whether g_bare = 1 is uniquely forced by Cl(3)
  axioms (the parent's broader claim — separate Nature-grade target).
- The G_BARE_* family (separate sister theorems on rigidity, Ward-identity
  closure, dynamical fixation, etc.).
- The `A → A/g` rescaling-freedom obstruction (separate audit row).

## Cross-references

- `G_BARE_DERIVATION_NOTE.md` — parent with a conditional audit verdict; this
  narrow theorem resolves the convention-vs-derivation
  ambiguity by stating `g_bare = 1` as convention.
- `G_BARE_RIGIDITY_THEOREM_NOTE.md` — sister rigidity argument.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — declared dependency.
- Cycles 1-4 (PRs #292, #293, #294, #297) — sister narrow theorems on different lanes.
