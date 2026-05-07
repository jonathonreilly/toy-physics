# Bridge Gap — Gauge-Group Taste-Cube Exploration (Block 05)

**Date:** 2026-05-06
**Type:** exploration / partial structural finding
**Claim type:** open_gate
**Status:** exploratory note on the framework's potentially-richer gauge
group structure (SU(3) × U(1) instead of just SU(3)), motivated by the
gl(3) ⊕ gl(1) commutant of the staggered taste-cube SU(3) embedding.
NOT a closure of action-form uniqueness. Documents the taste-cube
decomposition structure, identifies the U(1) factor's origin, and
analyzes whether SU(3) × U(1) symmetry breaks Block 04's action-form
no-go.
**Authority role:** branch-local exploratory note. Audit verdict and
effective status are set only by the independent audit lane.
**Loop:** bridge-gap-new-physics-20260506 (Block 05 / R4.B)
**Branch:** physics-loop/bridge-gap-new-physics-block02-20260506 (commits-only; PR_BACKLOG)

## Question

The framework's [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
embeds SU(3)_c into the staggered taste-cube `V = {0,1}^3` (8-dim) via
the 3-dim symmetric base. The COMMUTANT of this SU(3) embedding is
`gl(3) ⊕ gl(1)` per the round-3 action-form-derivation agent's analysis
of the project audit graph. The `gl(1)` factor is a U(1) phase action.

Is the framework's actually-derived gauge group `SU(3) × U(1)` rather
than just `SU(3)`? If yes, does SU(3) × U(1) symmetry tighten the
action-form constraint enough to break Block 04's no-go on action-form
uniqueness?

## Step 1: Taste-cube decomposition

The 8-dim staggered taste cube `V = {0,1}^3` carries a natural action of:
- `S_3` permuting the three axes
- `(Z_2)^3` flipping individual axes
- The 3-dim symmetric base subspace `V_3` (Hamming weight 1) carrying
  the SU(3)_c fundamental

The `S_3` action decomposes V into irreps:

| Hamming weight | Vertices | S_3 irrep | dim |
|---:|:---:|:---:|---:|
| 0 | (0,0,0) | trivial | 1 |
| 1 | (1,0,0), (0,1,0), (0,0,1) | trivial ⊕ standard | 1 + 2 |
| 2 | (1,1,0), (1,0,1), (0,1,1) | trivial ⊕ standard | 1 + 2 |
| 3 | (1,1,1) | trivial | 1 |

Total: 4 trivials (dim 4) + 2 standard reps (dim 4) = 8. ✓

## Step 2: The 3-dim symmetric base — SU(3) "3"

Following [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md):
the Hamming-weight-1 triplet `{(1,0,0), (0,1,0), (0,0,1)}` carries the
fundamental "3" of SU(3)_c when an off-diagonal SU(3) transformation
mixes the three single-axis vertices. The symmetric (S_3-trivial)
subspace of weight-1 vertices is the SU(3) singlet projection on the
3-dim subspace; the standard (S_3-non-trivial 2-dim) subspace gives
the off-diagonal SU(3) generators.

This is a known framework structural result. The gl(3) Lie algebra
acting on the 3-dim base is su(3) ⊕ u(1). Decomposing:
- su(3) = traceless 3×3 matrices = 8 generators (Gell-Mann basis)
- u(1) = trace = 1-dim factor

The su(3) is gauged via canonical Tr-form (Block 01 premise TR).

## Step 3: The gl(1) commutant — what is the U(1)?

The commutant of SU(3)_c on V is operators commuting with all SU(3)
generators. Under the embedding above, SU(3) acts ONLY on the 3-dim
weight-1 base subspace, leaving:
- weight-0 trivial vertex (1-dim)
- weight-2 triplet (3-dim) with its OWN S_3 standard rep
- weight-3 trivial vertex (1-dim)

The commutant decomposes:

```
Commutant(SU(3)_c, V) = gl(V_0) ⊕ gl(V_2-traceless) ⊕ gl(V_3) ⊕ gl(V_1-trace),
```

where `V_0`, `V_3` are the 1-dim trivial Hamming-weight-0/3 subspaces,
`V_1-trace` is the trace projection on the weight-1 triplet, and
`V_2-traceless` is the traceless part of the weight-2 triplet.

This is more than `gl(1) ⊕ gl(3)` — it's `gl(1) ⊕ gl(3) ⊕ gl(1)' ⊕ gl(1)''`
or similar finer decomposition.

**Key observation:** the gl(1) "phase" factor has multiple sources in
this decomposition:
- (a) phase on `V_0` (weight-0 trivial)
- (b) trace projection on weight-1 (separate from SU(3) traceless action)
- (c) phase on `V_2` (weight-2 trace-projected)
- (d) phase on `V_3` (weight-3 trivial)

These are FOUR independent U(1) factors. The framework's "U(1) hypercharge
candidate" must specify which one (or which linear combination).

## Step 4: Is this U(1) the SM hypercharge?

Standard Model U(1)_Y acts on ALL fermion fields with specific
hypercharges (left-handed quarks: Y = 1/3, right-handed up-quarks:
Y = 4/3, etc.). The hypercharges are NOT all-equal across fermion species.

For the taste-cube U(1) factors above, each acts on a SPECIFIC
sub-sector of the taste cube. The Hamming-weight projection is a
well-defined topological labeling of taste-cube vertices.

**Match attempt:** if Hamming weight `n` corresponds to SM hypercharge
`Y(n) = (some function)`, the four U(1) factors are linearly related
to a single hypercharge generator.

Concretely:
- Weight 0 = "no taste indices on" = scalar singlet
- Weight 1 = "one taste index on" = quark/lepton triplet
- Weight 2 = "two taste indices on" = anti-triplet
- Weight 3 = "all taste indices on" = pseudo-scalar / topological

Hmm — the SM has quarks (Y = 1/3 left-handed, Y = 4/3 right up, Y = -2/3
right down) and leptons (Y = -1 left-handed doublet, Y = -2 right-handed
electron). The four hypercharges {-2, -1, 0, 1/3, 4/3, -2/3} don't
immediately map to four Hamming-weight projections.

**This is suggestive but not load-bearing.** Without a deeper structural
argument identifying the framework's taste-cube U(1) generators with SM
hypercharge generators, the connection is conjectural.

## Step 5: Does SU(3) × U(1) tighten the action-form constraint?

Question: if the framework's gauge group is SU(3) × U(1), does the
gauge action need to be U(1)-invariant on the link variables, and if
so, does this break Block 04's no-go?

The Wilson, HK, and Manton actions ALL respect the SU(3) gauge structure
trivially (they're functions of `Re Tr U` which is SU(3)-invariant by
construction).

Adding U(1)-invariance of the gauge action is automatic if the link
variable is SU(3)-valued (no U(1) phase on the link). But if the link
variable carries a U(1) phase (i.e., it's `U(3) = SU(3) × U(1)` or
`SU(3) × U(1)` separately), then the gauge action needs to specify how
the U(1) phase enters.

**Wilson with U(1):** S_W = -β · Re Tr U, where U ∈ U(3). For
U = e^{iθ} · V with V ∈ SU(3): Re Tr U = cos θ · Re Tr V - sin θ · Im Tr V.
This is NOT U(1)-invariant unless we project onto the SU(3) part.

**HK with U(1):** P_t(U) defined on U(3) as Brownian heat kernel; it's
a function on the group that's automatically U(1)-invariant under the
center action only if t is correctly normalized for the larger group.

**Conclusion:** if the framework's gauge group is SU(3) × U(1), the
action-form constraint becomes more restrictive — at least in the U(1)
sector. **But the no-go on action-form uniqueness within SU(3) is NOT
broken** by adding U(1) symmetry, because the SU(3) action functional
ambiguity (Wilson vs HK vs Manton) is independent of U(1) considerations.

## Step 6: Honest exploratory finding

The taste-cube structure does support the existence of multiple U(1)
factors in the framework's full gauge structure. Whether one of these
is identifiable with SM hypercharge requires:

1. A structural argument that the four U(1) factors collapse under
   physical-state projection to a single generator.
2. A specific assignment of taste-cube vertices to SM fermion species
   (currently the staggered-Dirac open gate per
   [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)).
3. Match of generator coefficients to the SM `Y = T_3 - Q` relation.

None of (1)-(3) is currently in the framework's retained chain. The
gl(3) ⊕ gl(1) commutant gives a NECESSARY condition (consistent with
SU(3) × U(1) gauge group) but not a SUFFICIENT condition (doesn't
prove U(1) = U(1)_Y).

## Conclusion: Block 05 partial finding

The Cl(3) ⊗ taste-cube structure naturally supports a gauge group
larger than just SU(3) — specifically SU(3) × U(1)^k for some k ≥ 1
related to taste-cube Hamming-weight projections. **However**, this
structural finding does NOT break Block 04's no-go on action-form
uniqueness, because the SU(3) action-functional ambiguity (Wilson vs
HK vs Manton) is independent of whether U(1) symmetry is also present.

The richer gauge structure is potentially significant for the framework's
SM derivation (specifically, deriving U(1)_Y from the taste-cube
commutant), but is not currently a Resolution-A path for the bridge gap.

## Status

```yaml
actual_current_surface_status: exploration / partial structural finding
target_claim_type: open_gate
conditional_surface_status: |
  Conditional on:
   (a) staggered-Dirac realization (open gate per MINIMAL_AXIOMS_2026-05-03);
   (b) cl3_color_automorphism deferred physical-color bridge;
   (c) the gl(3) ⊕ gl(1) commutant analysis being correct (cited from
       round-3 action-form-derivation agent's project audit-graph trace).
hypothetical_axiom_status: null
admitted_observation_status: |
  Standard Lie-algebra commutant analysis on tensor product modules
  (admitted standard machinery in narrow non-derivation role).
claim_type_reason: |
  This is exploratory: identifies that the taste-cube structure
  naturally supports SU(3) × U(1)^k gauge symmetry (partial structural
  finding) but does NOT close action-form uniqueness or the bridge gap.
  Useful documentation of an unattacked angle for future research.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## What this closes

- The Cl(3) ⊗ Cl(3) → SU(4) ⊃ SU(3) × U(1) angle (R4.B from
  `OPPORTUNITY_QUEUE.md`) is partially explored and shown to NOT
  resolve Block 04's no-go on action-form uniqueness (which was the
  Block 05 hope).
- Documents the gl(3) ⊕ gl(1) commutant structure for future reference.

## What this does NOT close

- The bridge gap.
- Action-form uniqueness (Block 04's no-go stands).
- The structural identification of U(1)_Y with one of the taste-cube
  U(1) factors (open research target, not in current retained chain).
- The SM-fermion assignment to taste-cube vertices (open staggered-Dirac
  realization gate).

## Cross-references

- New-physics opening: [`BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md`](BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md)
- Block 04 (sister no-go): [`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)
- Color automorphism: [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
- Three-generation structure: [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
- LHCM family (hypercharge derivation): [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
- Standard methodology: standard Lie-algebra commutant analysis (Fulton-Harris "Representation Theory")
