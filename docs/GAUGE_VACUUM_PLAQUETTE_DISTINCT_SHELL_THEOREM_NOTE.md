# Gauge-Vacuum Plaquette Distinct-Shell Theorem

**Date:** 2026-04-16
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** (1) staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`); (2) g_bare = 1 derivation target (canonical parent: `G_BARE_DERIVATION_NOTE.md` — bookkeeping pointer, see-also cross-reference; not a load-bearing dependency of this distinct-shell theorem's local algebra).
**Status:** exact support theorem on the accepted Wilson `3 spatial + 1 derived-time` surface
**Script:** `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py`

## Question

What exact geometric strong-coupling statement can already be proved for the
full interacting plaquette after the naive constant-lift law has been ruled out?

## Answer

The exact distinct-shell statement is:

> On the accepted Wilson `3 spatial + 1 derived-time` surface, the minimal
> distinct connected shell containing a marked plaquette is the six-face
> elementary cube boundary.

Equivalently:

- the first **distinct connected** nonlocal numerator shell uses five action
  plaquettes;
- the first connected vacuum shell uses six action plaquettes.

This is a real reusable theorem, but it is **not** by itself the full onset
theorem for `beta_eff(beta)`. That next step is now carried separately by
[GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md).

## Theorem 1: the minimal distinct shell around a marked plaquette is the cube boundary

Fix the observed plaquette `p0` in the `(0,1)` plane.

Any **distinct** plaquette sharing the boundary of `p0` shares exactly one of
its four edges. A distinct plaquette cannot share two edges with `p0`; that
would force it to be the same plaquette.

Therefore any distinct shell closing the four marked edges must use at least
four action plaquettes.

The script exhaustively checks all `5^4 = 625` one-per-edge distinct choices on
the accepted local `3+1` patch and finds:

`no four-action shell closes the boundary of p0`.

An explicit five-action shell does close it: the other five faces of an
elementary cube containing `p0`.

So the minimal distinct connected shell containing a marked plaquette has total
size `6`, i.e. one observed face plus five action faces.

## Corollary 1: the first distinct connected numerator shell is order `beta^5`

In the plaquette numerator, the marked plaquette is already supplied by the
observable insertion. A distinct connected shell therefore first appears when
the action contributes the other five faces of the cube boundary.

So the first distinct connected nonlocal numerator shell is order `beta^5`.

## Corollary 2: the first connected vacuum shell is order `beta^6`

For the vacuum partition function there is no marked face supplied in advance.
Any connected closed shell must therefore contain a seed plaquette plus at least
five others.

The same cube boundary realizes that minimum.

So the first connected vacuum shell is order `beta^6`.

## What this closes

- the exact minimal distinct-shell geometry around a marked plaquette
- the exact first distinct-shell orders for the numerator and vacuum sectors
- a reusable atlas tool for future plaquette strong-coupling work

## What this does not close

- the full analytic reduction law `P_full(beta) = P_1plaq(beta_eff(beta))`
- the full nonperturbative continuation of `beta_eff(beta)` to `beta = 6`
- repo-wide replacement of the current canonical same-surface plaquette value

The open coefficient problem is therefore sharper, but it is still open:

> extend the now-closed onset theorem beyond its first exact nonlinear
> coefficient and derive the full nonperturbative reduction law at `beta = 6`.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=1 FAIL=0`


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on **both** open gates:

1. **Staggered-Dirac realization derivation target** — canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`); in-flight supporting work: `PHYSICAL_LATTICE_NECESSITY_NOTE.md`, `THREE_GENERATION_STRUCTURE_NOTE.md`, `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, `scripts/frontier_generation_rooting_undefined.py`, `GENERATION_AXIOM_BOUNDARY_NOTE.md`.
2. **`g_bare = 1` derivation target** — canonical parent: `G_BARE_DERIVATION_NOTE.md` (`claim_type: positive_theorem`, `audit_status: audited_conditional`); bookkeeping pointer / see-also cross-reference, not a load-bearing dependency of this distinct-shell theorem's local algebra. In-flight supporting work: `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`, `G_BARE_RIGIDITY_THEOREM_NOTE.md`, `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`, `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`, `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`, `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`, `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`.

The note produces (or directly supports) a quantitative gauge prediction (Wilson plaquette content, `α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`, `g_2`, `β = 6`, CKM/quark/hadron mass hierarchy, action-unit metrology, etc.) by fixing `g_bare = 1` without independently deriving it — therefore both gates must close for the lane to upgrade.

Therefore `claim_type: bounded_theorem` until both gates close. When both gates close, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
