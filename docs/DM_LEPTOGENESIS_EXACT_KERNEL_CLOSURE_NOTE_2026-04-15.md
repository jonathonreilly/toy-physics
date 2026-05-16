# DM Leptogenesis Exact-Kernel Closure (claim narrowed 2026-05-01)

**Date:** 2026-04-15 (eta benchmark corrected 2026-05-01)
**Status:** bounded - exact source-and-CP-channel package closed; exact-kernel eta closure does NOT land at percent-level on the consistent benchmark
**Script:** `scripts/frontier_dm_leptogenesis_exact_kernel_closure.py`

## Framework sentence

In this note, "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

After the refreshed branch closes

- `c_odd = +1`
- `v_even = (sqrt(8/3), sqrt(8)/3)`
- `a_sel = 1/2`
- `tau_E = tau_T = 1/2`
- `K00 = 2`

what does the standard coherent leptogenesis kernel predict on the
retained benchmark?

## Bottom line (corrected)

The exact source-and-CP-channel package is closed. The exact coherent
heavy-basis kernel sits just below the Davidson-Ibarra ceiling. **But the
predicted baryon asymmetry on the consistent retained benchmark is
`eta/eta_obs ≈ 0.558`, not `0.99` as an earlier draft of this note claimed.**

The earlier `0.9907` figure was obtained with `K00 = 2` used in the
epsilon_1 numerator but **not** propagated into the washout coefficient
`K`. Once `K00 = 2` is used consistently — i.e. K is doubled when the
source includes the `K00 = 2` normalization — the washout efficiency
`kappa` halves and `eta/eta_obs` drops to `0.5579`. The runner's `[D]`
classified-pass line states this explicitly:

> The retained-fit benchmark no longer lands near observation once K00 is
> used consistently in the washout path.

So the percent-level eta closure earlier claimed in this note **does not
hold**. What does survive is everything upstream of the eta calculation:
the source package, the epsilon_1 / DI ratio, and the strong-washout
regime classification.

## Exact source-side kernel package (UNCHANGED)

The refreshed branch fixes

- odd source: `gamma = 1/2`
- even responses: `E1 = sqrt(8/3)`, `E2 = sqrt(8)/3`
- heavy-basis diagonal: `K00 = 2`

so the exact heavy-basis CP tensor channels are

- `cp1 = -2 gamma E1 / 3 = -0.544331...`
- `cp2 =  2 gamma E2 / 3 =  0.314270...`

These are exact numbers from the source package. They are not in dispute.

## Exact epsilon law (UNCHANGED)

The coherent heavy-basis kernel is

`epsilon_1 = |(1/8pi) y0^2 (cp1 f23 + cp2 f3) / K00|`.

With the exact source package and the staircase benchmark
(`k_A = 7`, `k_B = 8`, `eps/B = alpha_LM/2`),

- `epsilon_1 = 2.4576198796e-6`
- `epsilon_DI = 2.6493795301e-6`
- `epsilon_1 / epsilon_DI = 0.9276209209`.

So the exact kernel sits just below the DI ceiling, not far below it.
This part is correct.

## Exact eta on the retained benchmark (CORRECTED)

Using the same retained washout law but propagating `K00 = 2` consistently
into the washout path:

- `K = 47.236...`     (was `23.618...` in the earlier inconsistent draft)
- `kappa = 1.427e-2`  (was `2.534e-2`)
- `eta = 3.414e-10`   (was `6.063e-10`)
- `eta_obs = 6.12e-10`
- `eta / eta_obs = 0.5579` (was `0.9907`)

So the exact kernel under-shoots observation by ~44% on this benchmark.
The previously claimed percent-level closure was an artifact of a
bookkeeping inconsistency that gave `K00 = 2` to the source while
keeping `K00 = 1` in the washout. The runner now uses `K00 = 2` in
both places.

## Consequence

This **does not** resolve the old DM denominator suppression at percent
level on the refreshed branch. What is now established:

- The exact source package is closed (axiomatic, sharp numbers).
- The exact coherent kernel does not have an obvious order-of-magnitude
  problem: it is within a factor of two of observation on the retained
  benchmark, and within ~7% of the Davidson-Ibarra ceiling at the
  epsilon_1 level.
- Closing the remaining ~44% gap to observation requires either a
  refinement of the washout benchmark beyond the current retained
  staircase, or an additional source contribution not in the current
  exact heavy-basis package, or both.

## Scope

This note's substantive content is:

(i)   the exact source-and-CP-channel package (imported from upstream
      support theorems, not re-derived in this packet), and
(ii)  the exact `epsilon_1 / epsilon_DI = 0.928` ratio that follows from
      (i) plus the retained benchmark constants.

Both (i) and (ii) are PASS in the runner. As of the 2026-05-16 audit
class-E repair (science-fix-loop iter18), all nine runner checks are
self-classified as **class D conditional-on-imported-upstream**, not
class C standalone-derivation. There are zero class-C standalone
checks in this runner. This matches the audit verdict that the
load-bearing source-package values (`gamma = 1/2`, `E1 = sqrt(8/3)`,
`E2 = sqrt(8)/3`, `K00 = 2`) are imported from upstream conditional
authorities rather than derived from `Cl(3)` on `Z^3` inside the
restricted packet.

The headline `eta/eta_obs ≈ 1` percent-level closure is **not**
retained; the runner's classified-pass output confirms
`eta/eta_obs ≈ 0.558`. The note no longer claims percent-level eta
closure on this benchmark.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authorities
that the load-bearing step relies on, in response to the 2026-05-05
audit's `audited_renaming` verdict (the runner imports the exact source
package values `gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3, K00 = 2`
from [`scripts/dm_leptogenesis_exact_common.py`](../scripts/dm_leptogenesis_exact_common.py)
rather than deriving them inside the restricted packet). This addendum
does not promote the note or change the conditional scope.

Candidate one-hop authorities for the imported source package
(currently registered with mixed audit status; this section makes the
dependency edges explicit so the citation graph can track them):

- [`DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md)
  — upstream candidate for the odd-source coefficient `c_odd = +1` and
  by extension `gamma = 1/2`. Currently `unaudited`.
- [`DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md)
  — upstream candidate for the even-response pair
  `(E1, E2) = (sqrt(8/3), sqrt(8)/3)`. Currently `audited_conditional`.
- [`DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md)
  — upstream candidate for the heavy-basis diagonal `K00 = 2`.
  Currently `audited_renaming`.
- The retained washout / staircase benchmark (`k_A = 7`, `k_B = 8`,
  `eps/B = alpha_LM / 2`) used in Part 3 of the runner currently has no
  separate retained-grade authority registered as a one-hop dependency.
  It is included here as an open registration target.

None of these upstream candidates carries `audited_clean` retained
status, so effective-status propagation correctly caps this note at
`audited_renaming`. The path to lifting the verdict is upstream closure
of the source-package candidates above, not local edits to this note.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_renaming` with the
substantive observation that the runner hard-codes the exact-package
values rather than deriving them from `Cl(3)` on `Z^3`, so the bounded
scope is conditional arithmetic on the imported source package and
benchmark. This addendum makes the dependency edges explicit but does
not change the verdict. The honest classification of this note remains:

- The arithmetic identities (`epsilon_1 / epsilon_DI = 0.928`,
  `eta / eta_obs = 0.558`) are runner-confirmed conditional outputs
  given the imported source package. The runner's `[D]` classified-pass
  output records this honestly.
- The exact source-and-CP-channel package and its derivation from the
  framework axiom are not closed by this note's restricted packet. The
  upstream `_codd_bosonic`, `_veven_bosonic`, and `_k00_bosonic` rows
  are the candidate authorities; this note inherits their conditional
  effective status until those rows reach `audited_clean`.

The 2026-05-16 follow-up edit (science-fix-loop iter18, this revision)
extends the honest classification into the runner itself. Previously,
Parts 1 and 2 of the runner classified their six checks as class C
(standalone derivation), even though their load-bearing values were
imported rather than derived. The 2026-05-05 audit specifically
recorded this mismatch as the load-bearing reason the row could not
lift to `audited_clean`. The iter18 edit reclassifies all nine runner
checks as class D conditional-on-imported-upstream and adds the
explicit upstream authority citations in both the module docstring and
the per-check detail strings, so that future audit passes see exactly
which upstream rows the conditional bounded claim depends on. The
runner now has zero class-C standalone checks, matching the honest
read above. The numeric outputs are unchanged.

This addendum is graph-bookkeeping only. It does not promote the note,
does not modify the runner numerics, and does not introduce any new
vocabulary. The audit lane still owns the verdict.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_exact_kernel_closure.py
```
