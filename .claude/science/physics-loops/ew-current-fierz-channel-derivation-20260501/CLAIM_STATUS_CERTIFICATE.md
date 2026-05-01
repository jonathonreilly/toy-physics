# Claim Status Certificate — EW Current Fierz-Channel Derivation

**Block:** ew-current-fierz-channel-derivation-block01-20260501
**Branch:** physics-loop/ew-current-fierz-channel-derivation-block01-20260501
**Artifact:** docs/EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md
**Runner:** scripts/frontier_ew_current_fierz_channel_decomposition.py

## Status

```yaml
actual_current_surface_status: support / exact group-theory derivation (cycle-breaking)
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: "Matching rule (M) — that the physical EW vacuum polarization projects onto the adjoint channel after CMT factorization — is named as a structural input from the framework's already-audited lattice gauge surface. Not derived in this note."
proposal_allowed: false
proposal_allowed_reason: "The exact group-theory ratio (N_c^2 - 1)/N_c^2 IS derived inline from the SU(N_c) Fierz identity + Hilbert-space dimension counting. But the package-level 9/8 EW coupling correction also depends on the matching rule (M), which this note does not derive. So the partial result here is 'support / exact group-theory ratio + admitted matching', not retained 9/8 closure."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Disposition

The note is a **cycle-breaking artifact**. The 2026-05-01 audit ledger
flagged a 3-node citation graph cycle:

```
yt_ew_color_projection_theorem  ↔  rconn_derived_note  ↔
    ew_current_matching_ozi_suppression_theorem_note_2026-04-27
```

with the explicit gap "missing direct EW-current matching coefficient
computation." This note breaks the cycle by deriving the load-bearing
`(N_c^2 − 1)/N_c^2` ratio through an **exact** group-theory route — the
SU(N_c) Fierz completeness identity + Hilbert-space dimension counting.

The note depends only on retained upstream notes
(`NATIVE_GAUGE_CLOSURE_NOTE`, `GRAPH_FIRST_SU3_INTEGRATION_NOTE`) and
explicitly does NOT cite any of the 3 cycle nodes.

The package-level 9/8 EW coupling correction is split into two pieces:
- **(F) exact group-theory ratio (N_c^2 − 1)/N_c^2 = 8/9 at N_c=3:** derived in this note.
- **(M) matching rule:** named as load-bearing structural input, NOT derived here.

Closing (M) is left to a future research lane.

## Allowed PR/Status Wording

- "support / exact group-theory derivation (cycle-breaking)"
- "exact at any finite N_c"
- "no 1/N_c expansion required"
- "cites only retained upstreams"
- "does not cite the 3 cycle nodes"
- "matching rule (M) named as structural input"

## Forbidden PR/Status Wording

- bare "retained" / "promoted"
- "closes the 9/8 EW coupling correction"
- "retires `RCONN_DERIVED_NOTE`"
- "derives the matching rule (M)"
- "promoted to retained"

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_ew_current_fierz_channel_decomposition.py
# expected: PASS=31 FAIL=0
```

The runner verifies:
- Note structure (title, status language, no bare retained, matching rule named).
- Cited upstreams are retained; the 3 cycle nodes are NOT cited via markdown link.
- SU(N_c) Fierz identity holds numerically for N_c = 2, 3, 4, 5.
- Hilbert-space dimension count `1 + (N_c^2 − 1) = N_c^2` is exact.
- `(N_c^2 − 1)/N_c^2` evaluates to exactly 8/9 at N_c = 3 (Fraction-equality, no `O(1/N_c^4)`).
- Matching rule (M) is explicitly named as not-derived.
- Forbidden-imports clause + import-roles table are present.

## Independent Audit

Audit must verify:

1. The note's load-bearing arithmetic (Fierz identity, dimension count) is
   textbook group theory and exact at any N_c.
2. The cited upstreams (`NATIVE_GAUGE_CLOSURE_NOTE`,
   `GRAPH_FIRST_SU3_INTEGRATION_NOTE`) are at `effective_status: retained`
   on `main`.
3. The note does not import any of the 3 cycle nodes via markdown links
   (the runner's Part 2 checks this).
4. After this note lands, the 3 cycle nodes should be eligible for
   re-audit with the cycle broken: each can cite this new note for the
   (N_c^2 − 1)/N_c^2 ratio rather than each other.
5. The matching rule (M) is correctly identified as a structural input
   not closed by this note. The 9/8 package-level coefficient remains
   bounded until (M) is derived.
6. The runner's PASS=31 FAIL=0 reproduces from a clean checkout.

## Cycle-breaking outcome

After this PR lands and the audit pipeline regenerates the citation graph:

- `yt_ew_color_projection_theorem` and
  `ew_current_matching_ozi_suppression_theorem_note_2026-04-27` should be
  edited (separately) to cite this note as the primary derivation of the
  `(N_c^2 − 1)/N_c^2` ratio. That edit is OUT OF SCOPE for this PR — it's
  a follow-up cycle-cleanup PR.
- `rconn_derived_note` remains as the 1/N_c topological-expansion derivation,
  complementary to this note's Hilbert-space-counting derivation.
- The audit graph should re-evaluate without the cycle, allowing all 3 cycle
  nodes' downstream `proposed_retained` rows (385 transitive descendants)
  to propagate to clean status — provided the matching rule (M) is named
  honestly in each.
