# Quark CP-Carrier Completion on the Live Mass-Ratio Lane

**Date:** 2026-04-18 (demoted 2026-05-16)
**Status:** bounded numerical-match note (tuned fit to imported comparators)
**Audit class:** G — load-bearing step is a numerical match, not a derivation
**Primary runner:** `scripts/frontier_quark_cp_carrier_completion.py`

## Scope (honest framing)

This note is **not** a derivation that sector-specific complex `1-3` quark
carriers exist as a consequence of the retained framework. It is a bounded
*existence-of-fit* check: given imported comparator targets

```text
(m_u/m_c, m_c/m_t, |V_us|, |V_cb|, |V_ub|, J)
```

drawn from observation/atlas conventions, two complex carrier coefficients
`xi_u` and `xi_d` (four real numerical degrees of freedom in total) can be
solved numerically to reproduce that target surface to about `1%` or better,
while keeping `arg det(M_u M_d) = 0 mod 2pi` closed.

The comparator targets are imported, not derived. The carrier coefficients
`xi_u` and `xi_d` are solved by numerical optimization against those
imported targets; they are not derived from any retained primitive. The
chosen carrier slot (one determinant-neutral complex `1-3` carrier per
sector, on top of the Schur-generated `1-3` term) is asserted by ansatz,
not derived as the unique admissible extension of the minimal Schur-NNI
carrier.

This is therefore a Class-G numerical-match result in the project's audit
taxonomy, not a closed first-principles derivation. The prior audit recorded
this boundary as `audited_numerical_match`; after this source edit, independent
re-audit owns the current status. The remaining structural gaps are recorded
below in "What remains open (load-bearing gaps)".

A scope-narrowing companion already records the same boundary explicitly:
`QUARK_CP_CARRIER_COMPLETION_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md`.
A complementary reduced-closure attempt with fewer free parameters is in
`QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md`; that note
continues to live as a separate bounded surface and is **not** load-bearing
for the present note.

## Safe statement

The minimal Schur-NNI quark full-solve note remains valid:

- the minimal surface closes the quark magnitudes well;
- the same surface does **not** close the CKM CP area;
- phase-only relaxation on that surface does not repair `J`.

This note adds the next bounded step:

- keep the live down-type anchor and the historical `c12/c23` surface;
- keep the quark mass ratios `m_u/m_c`, `m_c/m_t` on their observation comparators;
- add one independent complex `1-3` carrier in each sector,
  `xi_u`, `xi_d`, on top of the Schur-generated `1-3` term;
- require the full atlas target surface
  `(|V_us|, |V_cb|, |V_ub|, J)`.

On that bounded extended surface there is a numerical existence-of-fit at
the comparator surface:

- `m_u/m_c = 1.688494 x 10^-3`
- `m_c/m_t = 7.400356 x 10^-3`
- `|V_us| = 0.227270122`
- `|V_cb| = 0.042179824`
- `|V_ub| = 0.003917067`
- `J = 3.313653 x 10^-5`

all within about `1%` or better of the chosen comparator/atlas targets, while
`arg det(M_u M_d) = 0 mod 2pi` stays closed numerically. The comparator
values are imported from observation/atlas conventions and the carrier
coefficients are solved numerically against them; this is a tuned-fit
existence statement, not a derivation.

So the live quark work can now be stated more sharply:

- no self-contained full closure on the minimal Schur-NNI carrier;
- bounded full closure **does** exist once one adds an explicit complex
  determinant-neutral `1-3` carrier in each sector;
- this is still bounded support, not a retained theorem, because `xi_u`,
  `xi_d` are solved rather than derived.

## Carrier form

The completed `1-3` coefficients are taken to be

```text
c13_u(total) = c12_u c23_u sqrt(m_u/m_t) + xi_u
c13_d(total) = c12_d c23_d sqrt(m_d/m_b) + xi_d
```

with `xi_u`, `xi_d` complex and sector-specific.

The solved completion on this branch is:

```text
xi_u = +0.340735 - 0.063203 i
xi_d = +0.078186 + 0.108371 i
```

The corresponding Schur-base terms are:

```text
c13_u(base) = 3.400566 x 10^-3
c13_d(base) = 2.011511 x 10^-2
```

so the completion is numerically strong, not perturbative:

- `|xi_u| / c13_u(base) ~ 101.9`
- `|xi_d| / c13_d(base) ~ 6.64`

That is the key caveat. This is a real bounded completion surface, but not yet
the small retained correction one would ideally want.

## What closes

1. **Full quark package on a bounded extended surface.**
   The quark mass ratios and full atlas CKM package can be matched at once.
2. **Determinant-neutral completion.**
   The solve keeps `arg det(M_u M_d) = 0 mod 2pi`, so this is a weak-sector
   CP completion, not a strong-CP reopening.
3. **Sharper primitive target.**
   The missing ingredient is no longer a generic “more phase.” It is an
   independent complex `1-3` carrier.

## What does not close

1. **Retained derivation of `xi_u`, `xi_d`.**
   These remain numerical bounded carrier coefficients.
2. **Perturbative-small correction.**
   The completion dominates the bare Schur `1-3` term, especially in the
   up sector.
3. **Minimal-surface theorem upgrade.**
   The old minimal Schur-NNI note remains a CP no-go on its own carrier.

## Cross-checks on this branch

Two independent bounded scans reinforce the same endpoint:

- [scripts/frontier_quark_jarlskog_closure_scan.py](../scripts/frontier_quark_jarlskog_closure_scan.py)
  finds local `c13`-enhanced families that reach `J ~ J_atlas` inside the
  current CKM corridor, while phase-only motion fails.
- [scripts/frontier_quark_cp_primitive_projector_scan.py](../scripts/frontier_quark_cp_primitive_projector_scan.py)
  finds that wide projector-like `1+5` deformations can supply the missing
  area, while the literal `1/42` tensor lower-row dressing stays far too weak.

So the branch now has three aligned statements:

- minimal surface: strong quark magnitudes, CP no-go;
- bounded scan surface: `c13`/projector deformations can lift `J`;
- bounded completion surface: an explicit complex `1-3` carrier admits a
  numerical fit to the imported comparator surface for the full quark
  package.

## What remains open (load-bearing gaps)

To upgrade this row from numerical-match/support scope to a retained
first-principles derivation, the following structural gaps must be closed,
none of which the present runner addresses:

1. **Derive the carrier coefficients `xi_u` and `xi_d`** from retained
   primitives, including their normalization, readout convention, and
   determinant-neutral constraint. The present note solves them numerically
   against imported comparators.
2. **Derive why the determinant-neutral complex `1-3` carrier is the unique
   minimal admissible CP-carrier slot** beyond the Schur-NNI base, rather
   than choosing it by ansatz. Other carrier slots (different index pairs,
   different determinant-charge sectors, non-Hermitian completions) are
   not ruled out by the present note.
3. **Derive the comparator targets `(m_u/m_c, m_c/m_t, |V_us|, |V_cb|,
   |V_ub|, J)`** from framework primitives, or supply an audited bridge that
   maps the imported observational values onto framework-defined readouts.
   The present note imports these values directly from atlas/observation
   conventions.
4. **Derive a small-correction interpretation**, or accept that the
   completion is non-perturbative relative to the Schur `1-3` base
   (`|xi_u|/c13_u^{base} ~ 102`, `|xi_d|/c13_d^{base} ~ 6.6`) and is
   therefore not a retained small correction but a bounded completion
   ansatz of comparable magnitude to the base term.

All four are theorem/derivation problems and are out of scope for this
note. The note therefore stops at the bounded numerical-match claim and
does not attempt to upgrade beyond it.

## Audit history

The 2026-05-05 audit recorded this row as `audited_numerical_match` with
Class-G load-bearing step. That is historical audit context; this source
edit resets the row for independent re-audit. The auditor verdict was:

> The load-bearing step is an optimized numerical completion using
> explicit solved carrier coefficients and imported comparator targets.
> The runner is not a trivial printout: it builds Hermitian mass matrices,
> diagonalizes them, computes CKM observables, and checks the determinant
> phase. However, the parameters xi_u and xi_d are tuned degrees of
> freedom rather than derived from the stated axiom, and the success
> criteria are external observation/atlas matches, so this is class G
> rather than first-principles class C.

The 2026-05-16 demotion edit (this revision) rewrites the title sub-line,
adds a "Scope (honest framing)" lead-in, retitles the headline closure
phrase as a numerical existence-of-fit, and enumerates the four
load-bearing structural gaps that any future clean audit upgrade would have
to close. The underlying runner output (`PASS=11, FAIL=0`) is unchanged;
the current audit status is owned by the regenerated audit pipeline and the
next independent re-audit.

This demotion is graph-bookkeeping only. It does not change the numerical
match status, does not promote the row, does not introduce new axioms,
does not derive `xi_u` or `xi_d`, and does not alter the Schur-NNI
minimal-surface CP no-go.

## Validation

Run:

```bash
python3 scripts/frontier_quark_cp_carrier_completion.py
python3 scripts/frontier_quark_jarlskog_closure_scan.py
python3 scripts/frontier_quark_cp_primitive_projector_scan.py
```

Current expected results on this branch:

- `frontier_quark_cp_carrier_completion.py`: `PASS=11 FAIL=0`
- `frontier_quark_jarlskog_closure_scan.py`: `PASS=5 FAIL=0`
- `frontier_quark_cp_primitive_projector_scan.py`: summary scan with strongest
  candidate `J/J_atlas = 1.075`
