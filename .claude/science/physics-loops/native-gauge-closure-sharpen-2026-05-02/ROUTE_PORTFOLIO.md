# Route portfolio — iteration 4

## Routes considered

### Route A: promote claim_type to positive_theorem (REJECTED)

Promote `native_gauge_closure_note.claim_type` from `bounded_theorem`
to `positive_theorem`, targeting `effective_status: retained` after
audit ratification.

**Why rejected:**
- The prior audit history shows this row WAS at `claim_type=positive_theorem`
  on 2026-05-01 with cross-confirmation `confirmed`. It got auto-invalidated
  with reason `dep_weakened:graph_first_su3_integration_note:retained->retained_bounded`.
  That is, the deps explicitly weakened to bounded, taking this row with
  them.
- Both deps were re-audited 2026-05-02T14:40 with `claim_type=bounded_theorem`,
  `claim_type_provenance=audited` (intentional, not legacy backfill),
  `cross_confirmation status=confirmed`. The auditor verdict was explicit:
  "The abelian factor remains explicitly bounded as hypercharge-like, so
  no anomaly-complete physical bridge is imported."
- Promoting this row to positive without re-promoting the deps would
  fail compute_effective_status — `retained_bounded` deps satisfy
  `is_retained_grade` but the correct downstream propagation respects
  the scope boundary.
- More importantly: the bounded scope of the deps reflects a real
  physics boundary. Anomaly-complete U(1)_Y identification on the
  bounded eigenvalue surface requires the `nu_R = 0` selection (the
  anomaly-cancellation argument that picks the SM branch). That bridge
  is genuinely a separate audit lane.

### Route B: split deps' notes (REJECTED, out of scope)

Split `graph_first_selector_derivation_note` and
`graph_first_su3_integration_note` into separate positive-algebra
notes (commutant, eigenvalue spectrum) and bounded-support notes
(physical hypercharge identification).

**Why rejected:**
- Out of scope per campaign awareness rule: "touch only NATIVE_GAUGE_CLOSURE
  and any rows you discover are actually blocking it". The deps are not
  blockers — their bounded scope is genuine.
- Iteration 3 (microcausality upstream chain) is in flight and may touch
  related rows; avoid duplication.
- Major rewrite, not a narrow PR.

### Route C: anomaly-complete U(1)_Y theorem on bounded eigenvalue surface (DEFERRED)

Write a new theorem deriving anomaly-complete `U(1)_Y` from the
graph-first commutant `+1/3 / -1` eigenvalue spectrum, completing
the abelian identification.

**Why deferred:**
- This is exactly the "separate matter-completion theorem" the bounded
  notes refer to.
- It is a substantive new derivation, not a documentation tightening.
- Should be its own campaign target, not packaged with this iteration.

### Route D: NARROW honest scope-intrinsic clarification (CHOSEN)

Document on `NATIVE_GAUGE_CLOSURE_NOTE.md` that the bounded scope is
intentional and cannot be sharpened by closing more sub-derivations
of the existing inputs. Explicitly link to the WZ theorem at PR #392
to record that `retained_bounded` is the intended input strength.

**Why chosen:**
- Honest: bounded is genuinely correct; the sharpening blocker is a
  whole separate theorem.
- Narrow: documentation-only, stays at `claim_type=bounded_theorem`,
  no claim promotion.
- Useful: prevents future iterations from spending cycles attempting
  Route A; isolates the real next-blocker (Route C) for the next
  campaign target.
- Per task spec: "If sharpening to positive_theorem isn't possible
  on the current bank, that's fine — ... NARROW honest > FIX
  dishonest."

## Score table

| Route | Likely claim-state move | Honest? | In scope? | Cost | Selected |
|-------|-------------------------|---------|-----------|------|----------|
| A | retained_bounded → retained | NO (deps genuinely bounded) | yes | low | — |
| B | retained_bounded → retained (eventually) | yes | NO (campaign rule) | high | — |
| C | new positive_theorem | yes | NO (defer) | high | — |
| D | scope-intrinsic clarification | yes | yes | low | YES |
