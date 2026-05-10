# g_bare = 1 Wilson-Action-Internal Proof-Walk Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_gbare_wilson_action_internal_proof_walk.py`](../scripts/frontier_gbare_wilson_action_internal_proof_walk.py)

## Claim

Given the existing constraint-vs-convention disambiguation theorem in
[`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`](G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md),
the proof of

```text
g_bare = 1   at   N_c = 3
```

depends load-bearingly on the Wilson plaquette small-a matching identity

```text
beta = 2 N_c / g_bare^2     (cited from G_BARE_TWO_WARD_*)
```

The remaining steps use only:

- the canonical Cl(3) connection normalization
  `Tr(T_a T_b) = delta_{ab} / 2`, which is an admitted convention already
  classified on the source note's surface;
- exact rational arithmetic in the matching identity at `N_c = 3` and
  `beta = 2 N_c = 6`.

This is a bounded proof-walk of an existing theorem note. **The proof is
NOT lattice-action-independent — it is Wilson-action-form-internal.** This
note records that scope honestly and walks the steps. It does not add a
new axiom, does not introduce a new repo-wide theory class, and does not
make a retained-status promotion claim.

## Scope guard

Honest narrower scope — distinct from the hypercharge proof-walk at
[`HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md`](HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md):

- The hypercharge proof-walk **is** lattice-action-independent: no Wilson
  plaquette quantity, no staggered phase, no link unitary appears in the
  load-bearing path.
- The present proof-walk is **not** lattice-action-independent. The
  Wilson plaquette small-a matching `beta = 2 N_c / g_bare^2` is a
  load-bearing input. Replacing the Wilson plaquette action with a
  Symanzik-improved or tadpole-improved or general non-Wilson lattice
  action changes the matching identity and therefore changes the value of
  `g_bare^2` forced at `beta = 2 N_c`.

The present proof-walk is **internal to the canonical Wilson-action
choice** already forced by other framework content. It does **not** show
that the result holds across alternative lattice-action choices. The
honest scope is "Wilson-action-form-internal".

## Proof-Walk

| Step in the cited constraint-vs-convention theorem | Load-bearing input | Wilson plaquette small-a matching? |
|---|---|---|
| (CN) canonical Cl(3) generator normalization `Tr(T_a T_b) = delta_{ab}/2` | admitted convention (already on source note surface) | no |
| (WM) matching identity `beta = 2 N_c / g_bare^2` | Wilson plaquette small-a expansion (cited from `G_BARE_TWO_WARD_*`) | yes |
| (RR) rescaling-freedom-removal under (CN) | one-hop dep theorem (algebraic) | no |
| `N_c = 3` substitution | structural-content input | no |
| `beta = 2 N_c = 6` substitution at canonical normalization | algebraic substitution | no |
| `g_bare^2 = 2 N_c / beta = 6/6 = 1` exact arithmetic | exact rational arithmetic | no |
| `g_bare = 1` square-root branch via `g_bare > 0` convention | sign convention (admitted) | no |

The (WM) step is the unique load-bearing entry that depends on the
Wilson plaquette action form. Five of seven steps use only canonical
Cl(3) normalization (admitted convention) plus exact algebra; one step
((WM)) is Wilson-action-form-internal.

## Exact Arithmetic Check

Substitute `N_c = 3` and the canonical-normalization-forced
`beta = 2 N_c = 6` into the Wilson plaquette small-a matching identity:

```text
g_bare^2 = 2 N_c / beta = (2 * 3) / 6 = 6/6 = 1.
```

The runner repeats this calculation with `fractions.Fraction` so the
final identity `g_bare^2 = 1` is checked as an exact rational, not a
floating-point comparison. The runner then takes the positive
square-root branch under the admitted `g_bare > 0` sign convention to
recover `g_bare = 1`.

## Dependencies

- [`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`](G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md)
  for the constraint-vs-convention disambiguation theorem being proof-walked.
- [`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md)
  for the one-hop rescaling-freedom-removal dep that closes
  alternative-`g_bare` case (a) under the canonical normalization.
- [`G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`](G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md)
  for the two-Ward closure that supplies the off-surface 1PI-amplitude
  route to the same `g_bare = 1` value.
- [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
  for the broader Cl(3) -> End(V) -> su(3) -> Wilson chain (Section C
  of that note covers the same Wilson plaquette small-a matching cited
  by the (WM) step here).
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  for the canonical Cl(3) generator basis and `Tr(T_a T_b) = delta_{ab}/2`
  normalization carried to (CN).
- [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](G_BARE_RIGIDITY_THEOREM_NOTE.md)
  for the upstream rigidity theorem (no scalar dilation of `T_a`).
- `MINIMAL_AXIOMS_2026-05-03.md`
  for the open realization-gate context that this note does not close.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does **not** show:

- lattice-action-independence of the `g_bare = 1` proof — the Wilson
  plaquette small-a matching is explicitly a load-bearing input, so the
  proof is internal to the canonical Wilson-action choice;
- that the canonical Cl(3) connection normalization (CN) is itself
  uniquely forced by the framework axioms (its convention status
  remains an admitted convention layer carried by
  `cl3_color_automorphism_theorem`);
- that the Wilson plaquette action form is uniquely forced by Cl(3)
  structure (Symanzik-improved, tadpole-improved, and other non-Wilson
  lattice actions remain outside this scope; see
  `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md` Claim 3
  for the explicit caveat);
- closure of the broader `G_BARE_*` family or the deeper gauge-coupling
  derivation lane;
- any retained-status promotion of the parent `G_BARE_DERIVATION_NOTE.md`
  surface;
- any continuum-limit numerical claim such as fitted plaquette, mass,
  or coupling values;
- any follow-on proof-walk for other algebraic bookkeeping notes.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_gbare_wilson_action_internal_proof_walk.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: bounded proof-walk passes; g_bare = 1 derivation depends
load-bearingly on Wilson plaquette small-a matching, with all other
steps reduced to canonical normalization (admitted convention) plus
exact rational arithmetic. Scope is Wilson-action-form-internal,
NOT lattice-action-independent.
```
