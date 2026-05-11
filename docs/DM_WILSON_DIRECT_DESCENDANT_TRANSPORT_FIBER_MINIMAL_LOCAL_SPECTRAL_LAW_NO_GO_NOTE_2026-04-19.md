# DM Wilson Direct-Descendant Transport-Fiber Minimal Local Spectral-Law No-Go

**Date:** 2026-04-19  
**Status:** exact search-plus-no-go on the completed local spectral carrier
**Claim type:** no_go

**Audit-conditional perimeter (2026-04-30):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, `claim_type =
no_go`, `independence = cross_family`, and load-bearing step class
`B`. The audit chain-closure explanation is exact: "No. One-hop
dependencies are not all retained
(`dm_wilson_direct_descendant_transport_fiber_spectral_completion_theorem_note_2026-04-19=audited_conditional`,
`dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_note_2026-04-19=audited_conditional`,
`dm_wilson_direct_descendant_constructive_transport_plateau_normalized_schur_determinant_selector_note_2026-04-19=audited_conditional`),
so the chain does not close under the leaf audit rule." The
audit-stated repair target (`notes_for_re_audit_if_any`) is exact:
"dependency_not_retained: audit or repair the listed dependency
rows to retained / equivalent closure, then re-audit this claim."
The generated audit ledger remains the authority for any terminal status. This is a **leaf
no-go** on the dm_wilson direct-descendant transport-fiber lane:
it is a sibling of the canonical-fiber mixed-spectral-branch-weight
no-go (also `audited_conditional`) and of
`dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18`
(also `audited_conditional`, PR #718 landing pattern). It depends
on five named upstream rows registered in the audit
`dep_effective_status` block (transport-fiber spectral-completion
theorem, canonical transport-column fiber theorem, constructive
transport-plateau normalized-Schur-determinant selector,
constructive transport-plateau `J_iso` derivation + Schur-isotropy
no-go, constructive transport-plateau observable-affine no-go).
All five upstream rows are themselves `audited_conditional` at the
2026-04-30 leaf-resweep, so the chain does not close even though
this row's runner verifies `PASS=17 FAIL=0` and the no-go is
internally complete (`Q Delta = Tr(H_e^2) det(H_e)` as the unique
degree-2 packet-separating raw monomial; structural no-go for
scale-free, raw affine, and raw monomial low-complexity laws on
the completed `(T, Q, Delta)` carrier). The conditional perimeter
is therefore the audit-graph leaf-rule pending closure of the
five upstream transport-fiber rows, not the runner-replay outcome
or the structural no-go itself. Nothing in this edit promotes
audit status; the note remains a **conditional no-go** within the
transport-fiber chain. See "Citation chain and audit-stated repair
path (2026-05-10)" below.

After the same-day spectral-completion theorem, the unresolved direct-descendant
selector problem was no longer vague. The live local fiber above the canonical
transport column is exactly the `3`-scalar spectral carrier

```text
(T, Q, Delta) = (Tr(H_e), Tr(H_e^2), det(H_e)),
```

with

```text
H_e = (L_e^(-1) + (L_e^(-1))^*) / 2.
```

The honest next question is then:

> does a minimal exact law on those three local scalars already select the
> current interior physical-source candidate, or do the natural low-complexity
> classes still fail?

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_transport_fiber_minimal_local_spectral_law_no_go_2026_04_19.py`
(`PASS=17 FAIL=0`).

## Bottom line

No exact selector is found in the natural low-complexity local spectral
classes.

The result splits into one positive search outcome and one structural no-go.

### Positive search outcome

On the explicit competitor set

- the certified interior plateau witnesses `W0, W1, W2, W3`,
- the more-isotropic boundary-drifting certificate `B_major`,
- and the explicit shrinking-sign-floor boundary packet,

the unique minimal positive coefficient-free monomial that selects `W1` is

```text
Q Delta = Tr(H_e^2) det(H_e).
```

So the completed spectral carrier does support a first simple
boundary-suppressing candidate.

### Structural no-go

That still does **not** give an exact interior selector.

The exact reason is that the same-day spectral-completion theorem already made

```text
(T, Q, Delta)
```

local coordinates on the `3`-real transport fiber.

Therefore:

1. any nonconstant affine law in `(T, Q, Delta)` has constant nonzero gradient
   in those local coordinates, so it cannot have an interior exact maximizer;
2. any nontrivial monomial law

   ```text
   T^a Q^b Delta^c
   ```

   has gradient

   ```text
   law * (a/T, b/Q, c/Delta),
   ```

   which also never vanishes at a positive interior point unless the law is
   constant;
3. any scale-free law factors through the normalized pair

   ```text
   (q2, q3) = (Q/T^2, Delta/T^3),
   ```

   and that normalized map has rank `2` on the `3`-real transport fiber, so
   canonically normalized laws are locally under-complete: they leave a
   `1`-real local degeneracy.

So the completed spectral data identify the local selector coordinates, but no
natural exact low-complexity selector law on them survives.

## What the runner proves

### 1. No single completed scalar selects `W1`

On the explicit competitor set:

- `max T -> W0`,
- `max Q -> W0`,
- `max Delta ->` a boundary-drifting packet point,
- and the canonically normalized determinant ratio

  ```text
  q3 = Delta / T^3
  ```

  also prefers the boundary packet.

So the raw single-scalar and simplest normalized single-scalar routes are both
closed.

### 2. Scale-free laws are structurally too small

Because scale normalization collapses `(T, Q, Delta)` to `(q2, q3)`, any
scale-free law sees only two local spectral coordinates.

But the local transport fiber is `3`-real. The runner checks that the
restricted Jacobian of

```text
source5 -> (q2, q3)
```

has rank `2` at every known plateau witness.

So a scale-free local law cannot exactly isolate a point of the fiber. At
best it can reduce the `3`-real fiber to a `1`-real residual normalized-spectral
subfiber.

This is the exact local reason the earlier normalized Schur-isotropy and
`J_iso` programs could never have been the whole answer.

### 3. The first simple boundary-suppressing raw monomial is `Q Delta`

The runner searches positive coefficient-free monomials in `(T, Q, Delta)` by
total degree.

Results:

- degree `1`: no winner is `W1`;
- degree `2`: the unique `W1` winner is

  ```text
  Q Delta = Tr(H_e^2) det(H_e).
  ```

Moreover, on the explicit boundary-drift packet, `Q Delta` decreases as the
sign floor shrinks. So this candidate does exactly what one hoped a minimal
raw spectral law might do:

- it rejects the explicit normalized-isotropy drift;
- it keeps the current interior candidate `W1` above the known boundary packet.

### 4. Even that minimal candidate is not exact

The same runner then checks the exact transport-fiber tangent through `W1`.

For `Q Delta`, the projected transport-fiber gradient is nonzero:

```text
||P_fiber grad(Q Delta)(W1)|| = 0.080118232647...
```

and a small ascent step:

- increases `Q Delta`,
- keeps the favored column fixed to first order,
- keeps `eta_1` fixed to first order,
- and stays inside the constructive positive chamber.

So `Q Delta` is only a **packet-separating candidate**, not an exact local
selector.

This is not an accident of that one monomial. It is the generic monomial
no-go implied by the local-coordinate theorem above.

### 5. Affine laws are also not retained selector content

If one allows arbitrary coefficients, affine laws in `(T, Q, Delta)` can be
tuned to select `W1` on the finite competitor packet. But the same family can
also be tuned to select `B_major` instead.

So affine spectral laws fail for the same basic reason as the earlier
observable-affine lane:

> the coefficients are extra selector input, not derived physics.

And even beyond that discrete tuning issue, no nonconstant affine law can be
an exact interior selector because its gradient in the local spectral
coordinates is constant and nonzero.

## Verdict

The clean verdict on the completed local spectral carrier is:

```text
minimal exact low-complexity local spectral law: ruled out.
```

More sharply:

- **minimal explicit packet-separator found:**  
  `Q Delta = Tr(H_e^2) det(H_e)`;
- **exact selector in natural low-complexity classes:**  
  no-go for
  - scale-free / canonically normalized laws,
  - raw affine laws,
  - raw monomial laws.

The exact reason is now clear:

- normalized laws throw away one of the three required local spectral
  directions;
- raw affine/monomial laws keep all three directions but are too rigid to
  produce an interior critical selector on that local coordinate chart.

## Why this matters

This compresses the post-completion frontier further.

The branch no longer lacks the local data. It has the right local data exactly.
What it lacks is the **higher-order retained principle** that uses those three
scalars in a genuinely interior way.

So the remaining science is no longer

> “find some local scalar on `H_e`.”

It is now

> derive the retained local law on the completed spectral carrier that is
> neither merely scale-free nor merely low-order algebra in the raw
> coordinates.

## What this closes

- the hope that one raw completed scalar already selects the interior source;
- the hope that a canonically normalized scale-free spectral law can exactly
  fix the source after the `3`-scalar completion;
- the hope that the raw affine or monomial classes already contain the final
  selector.

## What this does not close

- a higher-order or otherwise retained local law on `(T, Q, Delta)`;
- a derivation from retained Wilson / `Cl(3)` physics of why one nontrivial
  interior law is physical;
- the final DM flagship selector.

## Cross-references

- [`docs/DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_NORMALIZED_SCHUR_DETERMINANT_SELECTOR_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_NORMALIZED_SCHUR_DETERMINANT_SELECTOR_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_J_ISO_DERIVATION_AND_SCHUR_ISOTROPY_NO_GO_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_J_ISO_DERIVATION_AND_SCHUR_ISOTROPY_NO_GO_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_OBSERVABLE_AFFINE_NO_GO_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_OBSERVABLE_AFFINE_NO_GO_NOTE_2026-04-19.md)

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_transport_fiber_minimal_local_spectral_law_no_go_2026_04_19.py
```

Expected:

- `PASS=17 FAIL=0`;
- no single raw or normalized scalar winner at `W1`;
- rank `3` for raw `(T,Q,Delta)` and rank `2` for normalized `(Q/T^2,Delta/T^3)`
  on the transport fiber;
- unique degree-2 packet-separating monomial `Q Delta`;
- exact no-go for normalized, affine, and monomial low-complexity laws.

## Citation chain and audit-stated repair path (2026-05-10)

The audit verdict (2026-04-30 leaf-resweep, see top of note) flags
that the five named upstream transport-fiber rows are themselves
`audited_conditional` and therefore the leaf-audit chain does not
close on this row. The cited authority chain is registered explicitly
below so the audit-graph one-hop edges from the source note to the
upstream transport-fiber rows are visible.

| Cited authority | File / log | Audit-graph status (2026-05-10) | Role on this row |
|---|---|---|---|
| Active runner | [`scripts/frontier_dm_wilson_direct_descendant_transport_fiber_minimal_local_spectral_law_no_go_2026_04_19.py`](../scripts/frontier_dm_wilson_direct_descendant_transport_fiber_minimal_local_spectral_law_no_go_2026_04_19.py) | runner-replay verified `PASS=17 FAIL=0` | computes the structural no-go: rank-3 raw `(T,Q,Delta)`, rank-2 normalized `(Q/T^2, Delta/T^3)`, unique degree-2 packet-separator `Q Delta = Tr(H_e^2) det(H_e)`, fiber-tangent gradient `‖P_fiber grad(Q Delta)(W1)‖ ≈ 0.080118` showing `Q Delta` is only a packet-separator (not exact selector), affine and monomial no-gos |
| Audit-lane runner cache | [`logs/runner-cache/frontier_dm_wilson_direct_descendant_transport_fiber_minimal_local_spectral_law_no_go_2026_04_19.txt`](../logs/runner-cache/frontier_dm_wilson_direct_descendant_transport_fiber_minimal_local_spectral_law_no_go_2026_04_19.txt) | runner-cache copy under `scripts/runner_cache.py` | runner-cache replay verifying `PASS=17 FAIL=0` |
| Upstream one-hop dep — transport-fiber spectral-completion theorem | [`docs/DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md) | `audited_conditional` | establishes `(T, Q, Delta) = (Tr(H_e), Tr(H_e^2), det(H_e))` as local coordinates on the 3-real transport fiber (cited at top of note) |
| Upstream one-hop dep — canonical transport-column fiber theorem | [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md) | `audited_conditional` | reduces the live object to a local scalar law on the positive source fiber over the canonical favored column orbit (sibling chain with the canonical-fiber mixed-spectral-branch-weight no-go) |
| Upstream one-hop dep — constructive transport-plateau normalized-Schur-determinant selector | [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_NORMALIZED_SCHUR_DETERMINANT_SELECTOR_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_NORMALIZED_SCHUR_DETERMINANT_SELECTOR_NOTE_2026-04-19.md) | `audited_conditional` | supplies the canonically normalized determinant ratio `q_3 = Delta / T^3` referenced in §1 of the runner check |
| Upstream one-hop dep — constructive transport-plateau `J_iso` derivation + Schur-isotropy no-go | [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_J_ISO_DERIVATION_AND_SCHUR_ISOTROPY_NO_GO_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_J_ISO_DERIVATION_AND_SCHUR_ISOTROPY_NO_GO_NOTE_2026-04-19.md) | `audited_conditional` | supplies the prior `J_iso` and normalized Schur-isotropy programs that this no-go subsumes (cited in §"This is the exact local reason the earlier normalized Schur-isotropy and J_iso programs could never have been the whole answer") |
| Upstream one-hop dep — constructive transport-plateau observable-affine no-go | [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_OBSERVABLE_AFFINE_NO_GO_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_OBSERVABLE_AFFINE_NO_GO_NOTE_2026-04-19.md) | `audited_conditional` | supplies the prior observable-affine no-go that this row's affine-law no-go generalizes (cited in §"affine spectral laws fail for the same basic reason as the earlier observable-affine lane") |
| Sibling no-go — canonical-fiber mixed spectral / branch-weight no-go | [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_FIBER_MIXED_SPECTRAL_BRANCH_WEIGHT_NO_GO_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_FIBER_MIXED_SPECTRAL_BRANCH_WEIGHT_NO_GO_NOTE_2026-04-19.md) | `audited_conditional` (this PR's other dm_wilson row) | sibling on the dm_wilson direct-descendant lane; same pattern of leaf no-go conditional on upstream canonical-fiber retention |
| Sibling no-go — constructive positive closure manifold theorem | [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MANIFOLD_THEOREM_NOTE_2026-04-18.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MANIFOLD_THEOREM_NOTE_2026-04-18.md) | `audited_conditional` (PR #718 landing) | sibling on the dm_wilson direct-descendant lane; PR #718 landing pattern for leaf no-go conditional on upstream rows |
| Repo baseline anchor | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | `unaudited` / `meta` | repo-baseline terminology anchor for the dm_wilson direct-descendant lane |

The audit-stated repair path (verbatim from the audit
`notes_for_re_audit_if_any`) is to **audit or repair the listed
dependency rows to retained / equivalent closure, then re-audit
this claim**. The five upstream rows are all leaf-resweep
`audited_conditional` at 2026-04-30; promotion of any one of them
would not by itself satisfy the leaf-audit closure rule, which
requires *all* one-hop dependencies to be retained or equivalent.
Until that upstream cluster lands as retained / retained_bounded,
the regenerated ledger leaves this row for independent audit, and the
safe read is the runner-replay-verified structural no-go (no single raw or normalized
scalar winner at `W1`; rank-3 raw, rank-2 normalized; unique
degree-2 packet-separator `Q Delta`; affine and monomial no-gos)
conditional on the upstream transport-fiber chain. The acknowledged
residual is the absence of upstream-row retention; everything else
(the structural no-go on the completed local spectral carrier, the
exact local-coordinate / rank arguments, the runner `PASS=17
FAIL=0`) is supported by the runner and the listed cited authorities.

This rigorization edit only sharpens the conditional perimeter and
registers the cited authority chain; it does not promote audit
status, hand-author audit JSON, modify the runner, or change the
no-go conclusion. The §Verdict and §"Why this matters" boundaries
continue to apply: the transport-fiber minimal-local-spectral-law
no-go is a real structural no-go on the 3-real `(T, Q, Delta)`
local-coordinate carrier, but its retained closure is conditional
on the five upstream transport-fiber rows landing as retained.
