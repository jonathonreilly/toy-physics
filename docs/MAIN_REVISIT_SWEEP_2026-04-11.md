# Main Revisit Sweep — 2026-04-11

**Purpose:** repo-wide map of `main` surfaces that should be revisited before
they are reused as scientific baseline, publication evidence, or fresh
frontier launch points.

This note is intentionally broader than the latest frontier retain audit. It
looks across the whole `main` repo and flags:

- stale or mixed-semantic notes that are easy to overread
- bounded results that can be mistaken for stronger closure
- bug-sensitive or redesign-sensitive runner surfaces
- historical lanes whose retained rows are narrower than old summary docs make
  them appear

Use this together with:

- [`docs/repo/LANE_STATUS_BOARD.md`](repo/LANE_STATUS_BOARD.md)
- [`docs/RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md`](RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md)
- [`docs/PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md`](PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md)
- [`docs/CANONICAL_HARNESS_INDEX.md`](CANONICAL_HARNESS_INDEX.md)

## Revisit Map

| Item | Why it needs revisiting | Gate before relying on it again | Priority |
|---|---|---|---|
| `docs/FULL_TEST_MATRIX_2026-04-10.md` and older all-architecture scorecards | This matrix mixes pre-parity, pre-bugfix, and cross-architecture card semantics. It is still useful historically, but it is too easy to read as the current repo truth. | Split current retained baseline from historical matrix semantics, or add a refreshed replacement matrix before using it as a decision surface. Until then, defer to the lane board plus current retained notes. | High |
| Irregular off-lattice direction/sign lane | `main` still says the main blocker is the lack of a frozen endogenous irregular-graph directional observable. Many side results are sign-sensitive or attractive in bounded windows, but they do not close this blocker. | A same-surface irregular observable that distinguishes attractive from repulsive coupling without leaning on cubic-force semantics or narrow low-`G` windows. | High |
| Open-cubic staggered trajectory companions | These are now retained and useful, but they are bounded cubic-surface companions only. They do not yet give both-masses closure, self-consistent two-body closure, or irregular transfer. | A retained staggered two-body lane with either both-masses closure or a stronger self-consistent partner-force / trajectory observable. | High |
| Periodic 2D staggered torus diagnostics | The wraparound-weight bug is fixed on the retained headline runners, but nearby torus probes built from similar helpers may still be unsafe. This is a classic bug-pattern lane, not a one-file issue. | Any periodic-2D result outside the explicitly corrected retained notes should be rerun or code-audited before reuse. | High |
| Self-consistency lane | The corrected structured-null result is retained, but older iid-random-control framings remain easy to quote from stale notes and summaries. The scientific point survives; the old control story should not. | Use only the structured-null / corrected-torus notes and reruns. Do not reuse older random-control summaries without re-auditing the runner surface. | High |
| Ollivier curvature lane | `main` now retains this only as a bounded potential-weighted structured-curvature proxy, but the raw numbers are strong enough that future summaries may drift back into “Einstein equation derived.” | A control that separates curvature response from smooth structured-potential response on the same surface, or a narrower permanent naming convention that prevents overclaim. | High |
| Wilson two-body / Newton lane | This lane is scientifically important, but still bounded. Screening-controlled distance softening is real; the weak-field test-mass and continuum companions are real; full both-masses closure is not. It remains easy to confuse “Newton-compatible distance exponent” with “full Newton law.” | A valid open-surface both-masses law on the same audited surface, with force-balance/action-reaction objections resolved or explicitly bounded. | High |
| Boundary-law / holographic probe lane | The robustness sweep is good, but the underlying effect is still a gapped-free-fermion-style boundary-law result with a coefficient shift, not a holography derivation. This is easy to overread as stronger than it is. | Keep using it only as a bounded Dirac-sea boundary-law probe unless a less-generic discriminator is added. | Medium |
| Branch-entanglement / BMV lane | The retained side package is real as branch-mediated entanglement, but the current scripts are not full gravity-quantumness witnesses. The 3-body lane also already needed a GHZ-to-W correction. | Redesign the witness/classifier before promoting anything beyond the current bounded branch-mediated reading. | Medium |
| Memory lane | `main` now correctly says the failure is not purely Yukawa-range driven, but the result is still protocol-sensitive and geometry-sensitive enough to invite accidental overreuse. | A redesigned observable with rigid markers or a family-transfer protocol that remains stable under size/geometry variation. | Medium |
| Emergent-geometry growth lane | This remains a real exploratory reopen, but only as a seed- and coupling-sensitive narrow window. The lane is vulnerable to summary drift because the partial positive is visually compelling. | Multi-size, multi-seed stability with a clearly bounded operating window, or an explicit non-closure note if that never materializes. | Medium |
| Anderson / eigenvalue diagnostics | The retained result is a bounded disorder-separation window plus a clean no-chaos negative. The window is easy to flatten into a universal statement across sizes or `G`. | Treat it as a finite-window diagnostic unless a broader size-stable phase map is frozen. | Medium |
| Historical ordered-lattice / valley-linear / NN-refinement package | These are retained historical results, but many of the old notes are window-specific or family-specific while older summaries can sound universal. | Before reusing them in a live claim, point back to the retained note for the exact row/window and rerun the canonical historical harness if the claim depends on extrapolation. | Medium |
| Historical mirror / `Z2 x Z2` package | Still one of the strongest historical packages, but no longer the current architecture. The risk is not that it is wrong, but that it is read as the active successor lane. | Keep it framed as historical-retained unless a deliberate revival rerun is performed. | Medium |
| Coin / chiral / Dirac-walk lane | This lane contains both real bounded low-dimensional positives and strong 3+1D blocker diagnoses. The old mixed scorecards can make it look more uniformly positive than it is. | Reuse only through the bounded 1+1D / 2+1D synthesis or the negative mixing-period diagnosis, not the old blended architecture tables. | Medium |
| Generated-geometry / Gate B historical bridge | This lane has real retained rows, but they are narrow retained transfers, not broad geometry-emergence closure. The risk is overgeneralizing the retained moderate-drift row. | Replay the exact retained row or redesign the geometry rule before making stronger transfer claims. | Medium |
| Moonshot / Schwarzschild / Hawking backlog | These files remain useful for ambition-setting, but they are not retained discovery surfaces. Their continued presence on `main` makes them easy to cite prematurely. | No reliance without a dedicated retained note and runner pair that survives the current audit standard. | Low |

## Default Rule

If a result on `main` is:

1. older than the current lane board language,
2. broader than the retained note attached to it, or
3. drawn from a bug-sensitive or redesign-only runner family,

then treat it as **revisit-before-reuse**, not as baseline repo truth.
