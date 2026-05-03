# Hierarchy H1 Route 2 — `beta = 6` From Cl(3) + Wilson Canonical Normalization

**Date:** 2026-05-03
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Primary runner:** `scripts/frontier_hierarchy_closure_program.py` (Section H1-R2)
**Targets:** H1 Route 2 of the closure program — pin the gauge evaluation
point `beta = 6` to a derived consequence of Cl(3) gauge geometry plus the
canonical Wilson normalization, rather than treating it as a free input.

## Claim scope (proposed)

> The Wilson lattice gauge evaluation point `beta = 6` is a forced consequence
> of the chain
>
> ```
>   spatial dim d = 3        (admitted Cl(3) axiom: 3 spatial generators e_1, e_2, e_3)
>   --> N_c = 3              (graph-first SU(3) integration, retained)
>   --> g_bare^2 = 1         (Wilson canonical normalization, admitted convention)
>   --> beta = 2 N_c / g_bare^2  =  6.
> ```
>
> The only admitted convention in this chain is the Wilson canonical
> normalization `g_bare^2 = 1`. Once that convention is fixed (which is
> exactly what `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`
> already does), `beta = 6` is class (A) algebraic substitution.

The narrow theorem **explicitly does NOT** claim:

- that `g_bare^2 = 1` is uniquely forced by Cl(3) axioms (this is the open
  Nature-grade target of the broader G_BARE_* family);
- that `N_c = 3` is uniquely forced by `d = 3` independently of the
  graph-first SU(3) integration result (separate retained chain).

What this note **does** close: the perception that `beta = 6` is a "famous
hard input that has to come from MC" is corrected. `beta = 6` is forced
once the Wilson canonical normalization convention is selected. The
remaining open question is the convention selection, which is well-scoped
and structurally distinct from the lattice gauge theory plaquette evaluation
problem.

## Admitted dependencies

| Authority | Audit-lane status | Role |
|---|---|---|
| `MINIMAL_AXIOMS_2026-04-11.md` (axiom A1) | retained-axiom | spatial dim d = 3 as Cl(3) axiom |
| `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` | retained | N_c = 3 from spatial d = 3 |
| `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md` | bounded_theorem | g_bare^2 = 1 as Wilson canonical convention |

## Load-bearing step (class A — algebraic substitution chain)

```text
Step 1 (admitted Cl(3) axiom):
  Cl(3) generators: 1 scalar, e_1, e_2, e_3, e_1 e_2, e_2 e_3, e_3 e_1, I = e_1 e_2 e_3.
  Spatial dimension d = 3.

Step 2 (retained graph-first SU(3) integration):
  Spatial d = 3
    => the Cl(3) bivector subalgebra spans su(2) at each spatial point
       (3 bivectors {e_1 e_2, e_2 e_3, e_3 e_1} with the [.,.] commutator
        give the so(3) ~ su(2) Lie algebra)
    => the gauge sector built on the bivector subalgebra coupled to the
       graph-first integration produces SU(N_c) with N_c = 3.

Step 3 (admitted Wilson canonical convention):
  g_bare^2  =  1.
  This is the Wilson canonical-normalization choice on the lattice gauge
  action: F^{lattice} = Omega^{Cl(3)} without rescaling.

Step 4 (class A algebraic substitution):
  Wilson action: S_W = (beta / N_c) * sum_p Re Tr(I - U_p).
  beta-g relation: beta = 2 N_c / g_bare^2.
  Substituting:
    beta  =  2 * 3 / 1  =  6.   []
```

This is class (A) — algebraic substitution, exact rational arithmetic.

## What this re-frames in the hierarchy program

The hierarchy formula

```text
v  =  M_Pl * alpha_LM^16 * (7/8)^(1/4),
        |
        |  alpha_LM = alpha_bare / u_0,
        |     u_0 = <P>(beta = 6)^(1/4)
```

depends on `<P>(beta = 6)`. The framework previously treated `beta = 6`
as a "famous hard input requiring MC evaluation." This is wrong:
`beta = 6` is forced by the canonical Wilson normalization on the
graph-first SU(3) gauge surface. The actual hard input is `<P>(beta)`
viewed as a function of beta, evaluated at the *specific point* `beta = 6`.

The reframing matters for two reasons:

1. **The ground truth is one specific number, not a function.** The
   bridge-support stack already gives a specific candidate
   `P(6) = 0.59353` from the explicit Perron / tensor-transfer chain.
   That candidate is 0.022% above the canonical MC value 0.5934. The
   discrepancy is a single-number gap, not a function-fitting problem.

2. **The convention chain is well-scoped.** The Wilson canonical
   normalization `g_bare^2 = 1` is one of three logically distinct
   admissions in the framework:
   - Wilson form of the action (S_W = (beta/N_c) sum_p Re Tr(I - U_p));
   - canonical normalization of the field strength
     (F^{lattice} = Omega^{Cl(3)} without rescaling);
   - the constraint `g_bare = 1` that selects this normalization.

   The third admission is the only one that is genuinely open. The
   first two are standard Wilson lattice gauge theory, and the
   `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md` note
   already makes the convention status explicit.

## Path to upgrading `g_bare^2 = 1` to a derived constraint

The `G_BARE_*` family of notes contains several distinct attempts at
upgrading the convention to a derivation:

- `G_BARE_RIGIDITY_THEOREM_NOTE.md` — argues the convention is rigid
  under specific Ward identities.
- `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md` — closes a 2-Ward
  identity chain.
- `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md` —
  shows the closure is representation-independent.
- `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md` —
  pins the choice on the same 1PI surface.
- `G_BARE_DERIVATION_NOTE.md` — currently demoted to bounded
  normalization proposal under audit (2026-05-02).
- `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md` — explicit
  obstruction to dynamical fixation.

The cleanest available route is the **A-rescaling-freedom closure**:

Show that the framework's lattice action has a residual gauge-coupling
rescaling freedom `A -> A / lambda` (for any `lambda > 0`) that is
fixed by the requirement `F^{lattice} = Omega^{Cl(3)}` without
rescaling, equivalently `lambda = g_bare = 1`. This is the content of
`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE` and is the most
direct route — but it requires resolving the obstruction in
`G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md` (currently
the binding open issue).

A second route: **the constraint is rep-independent by Two-Ward
closure.** The `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md` gives two
Ward identities that together pin `g_bare^2 = 1` on a specific 1PI
surface, with the rep-B-independence theorem showing the closure is
representation-independent. The remaining gap is the same-surface
question (the 2-Ward closure is on a specific surface; the question
is whether the same-surface choice is itself forced).

Either route, if closed, upgrades `g_bare^2 = 1` from convention to
derivation, and `beta = 6` from "convention chain conclusion" to
"axiom-derived gauge evaluation point."

## Why this matters for the hierarchy

If `g_bare^2 = 1` is upgraded to a derivation, the hierarchy formula

```text
v  =  M_Pl * alpha_LM^16 * (7/8)^(1/4)
   =  M_Pl * (alpha_bare / u_0)^16 * (7/8)^(1/4)
```

has only two remaining inputs that are not derived from axioms:

1. `M_Pl` (admitted lattice spacing identification);
2. `<P>(beta = 6)` evaluation (bounded by the bridge-support stack).

The `alpha_bare = 1/(4 pi)` is the Wilson canonical convention itself
(with `g_bare^2 = 1`, the bare fine-structure constant equals
`1/(4 pi)` from the action normalization). And `(7/8)^(1/4)` is now
the H2 V-orbit-measure-normalized correction
(`HIERARCHY_H2_ORDER_PARAMETER_SELECTION_THEOREM_NOTE_2026-05-03.md`).

This isolates the remaining bounded inputs to two cleanly-stated items,
both of which have explicit closure paths via the bridge-support stack
(Route 1) and the V-invariant bootstrap (Route 3).

## Closure status of Route 2

This note **closes**:

1. `beta = 6` is no longer a "famous hard MC input." It is forced by
   `g_bare^2 = 1` + `N_c = 3` + canonical Wilson normalization.
2. The remaining open piece is `g_bare^2 = 1` itself, which is a
   well-scoped convention/constraint question with two explicit closure
   paths in the existing G_BARE_* family of notes.
3. The reframing isolates the genuinely-open hierarchy inputs to two
   cleanly-stated items.

This note **does not close**:

- The upgrade of `g_bare^2 = 1` from convention to constraint
  (separate audit row; binding open issue is the dynamical-fixation
  obstruction).
- The numerical value of `<P>(beta = 6)` (Route 1 + Route 3).

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_closure_program.py
```

Verifies, at exact rational precision via `Fraction`:

1. `beta = 2 * 3 / 1 = 6` is exact rational.
2. The Cl(3) bivector subalgebra has 3 generators
   `{e_1 e_2, e_2 e_3, e_3 e_1}` and the commutator algebra is `so(3) ~ su(2)`.
3. The Wilson action normalization `S_W = (beta/N_c) * sum_p Re Tr(I - U_p)`
   with `g_bare^2 = 1` gives `F^{lattice} = Omega^{Cl(3)}` without rescaling.
4. The action coefficient is `beta = 6` for `(N_c, g_bare) = (3, 1)`.

## Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  beta = 6 follows by class-A algebraic substitution from the chain
  d = 3 (Cl(3) axiom) -> N_c = 3 (graph-first SU(3) integration, retained)
  -> g_bare^2 = 1 (Wilson canonical convention, admitted) -> beta = 2N_c/g_bare^2 = 6.
  The note does NOT upgrade g_bare^2 = 1 from convention to constraint;
  that is the binding open issue in the broader G_BARE_* family.
proposed_load_bearing_step_class: A
status_authority: independent audit lane only
```

## Cross-references

- `MINIMAL_AXIOMS_2026-04-11.md` — d = 3 spatial dimension axiom.
- `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` — N_c = 3 from d = 3.
- `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md` — the
  convention statement.
- `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md` — the
  binding open issue if g_bare = 1 is to be upgraded to a constraint.
- `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md` — closest available
  closure route (2-Ward identity pinning).
- `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` — beta = 6 already documented as
  the framework-point convention conclusion in §"Framework-point context".
- `HIERARCHY_H1_SELF_CONSISTENT_SADDLE_NOTE_2026-05-03.md` — Route 1.
- `HIERARCHY_H1_BOOTSTRAP_VINVARIANT_NOTE_2026-05-03.md` — Route 3.
- `HIERARCHY_CLOSURE_PROGRAM_NOTE_2026-05-03.md` — top-level program.
