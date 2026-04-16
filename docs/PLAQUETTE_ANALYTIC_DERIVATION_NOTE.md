# ⟨P⟩ Scalar-Bridge Theorem: Analytic Route on Main

**Status:** bridge theorem closed on main (2026-04-16); numeric migration across
downstream lanes pending.
**Authority:** `docs/GAUGE_VACUUM_PLAQUETTE_BRIDGE_THEOREM_NOTE.md`
**Runners:**
- `scripts/frontier_scalar_3plus1_temporal_ratio.py` — EXACT 4/4 PASS + 1 SUPPORT
- `scripts/frontier_gauge_vacuum_plaquette_bridge_theorem.py` — THEOREM 8/8 + COMPUTE 1/1 PASS

**Supersedes:** the earlier negative result on main-derived (N1, "⟨P⟩ not
analytically derivable") is retracted. The gauge-vacuum scalar bridge on main
closes the theorem gap.

## Summary

Main has closed the theorem gap on the plaquette scalar bridge. On the
route's chosen 3+1 scalar-bridge surface,

```
⟨P⟩(β) = ⟨P⟩_1plaq(β_eff),   β_eff = β · (3/2) · (2/√3)^(1/4)
```

At β = 6: the bridge yields ⟨P⟩ = 0.5935307… on the scalar bridge route.
This differs from the historical same-surface value 0.5934 at the fifth
decimal.

The bridge uses four exact ingredients:

1. **Local Wilson source-response** (plaquette = scalar generator derivative)
2. **Scalar 3+1 temporal ratio** A_inf/A_2 = 2/√3 (proved on the APBC block)
3. **Plaquette four-link coupling map** P(u_0 V) = u_0^4 P(V) (algebraic)
4. **3+1 incidence factor** Γ_coord = 6/4 = 3/2 (combinatorial)

See `GAUGE_VACUUM_PLAQUETTE_BRIDGE_THEOREM_NOTE.md` for the complete
theorem statement and proof chain.

## What this changes

Before: ⟨P⟩ was carried as "uniquely determined but computed via MC" —
defensible as an observable of the axioms but not analytically evaluated.

After: ⟨P⟩ has an analytic scalar-bridge derivation on the chosen 3+1
route. The historical MC value agrees to within ~10^−4 with the
analytic value from the bridge.

## Honest qualifiers

From the authority note (verbatim):

> "The bridge theorem is now closed. What is **not** done in this note
> is the full repo-wide numeric migration from the historical same-surface
> value `0.5934` to the analytic value above. That is a downstream
> implementation sweep, not a remaining theorem gap."

So:

- Theorem: closed on the chosen 3+1 scalar bridge route.
- Numeric migration across downstream consumers (which still quote
  0.5934): pending.
- Whether the bridge's 3+1 route is THE unique physical route vs. one of
  several valid routes: this note does not claim uniqueness beyond what
  the authority note asserts.

## For main-derived branch

The previous negative note N1 (⟨P⟩ not analytically derivable) is
retracted. This bridge theorem has now closed the gap on the chosen
3+1 route.

Whether this constitutes a FULL first-principles analytic derivation
of ⟨P⟩ that reviewers would accept without caveat depends on:

- Whether the 3+1 scalar bridge is the unique physical route (see above)
- Whether the downstream numeric migration to the analytic value
  (0.59353 vs 0.5934) is completed consistently

For the main-derived branch, we note the theorem is closed on main with
appropriate qualifiers. We do not promote it as a fully universal
analytic derivation beyond what the authority note says.

## Runner verification

```bash
python3 scripts/frontier_scalar_3plus1_temporal_ratio.py
# EXACT PASS=4 SUPPORT=1 FAIL=0

python3 scripts/frontier_gauge_vacuum_plaquette_bridge_theorem.py
# THEOREM PASS=8 COMPUTE PASS=1 FAIL=0
```

Both runners verify the theorem-level claims. See the authority note
for the complete structure and any remaining open questions.
