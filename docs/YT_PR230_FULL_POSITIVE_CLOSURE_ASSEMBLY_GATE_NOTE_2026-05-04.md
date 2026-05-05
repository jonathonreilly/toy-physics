# PR230 Full Positive Closure Assembly Gate Note

Status: open / assembly gate; proposal_allowed=false.

This note records the integration boundary for PR #230.  The chunk worker can
complete the production-response leg, but chunk completion alone cannot close
top-Yukawa retention.  A positive closure package must also include scalar LSZ
pole control and one same-surface bridge from the source-pole readout to the
canonical Higgs physical readout.

## Assembly Conditions

The executable gate is
`scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py`, with output
`outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json`.

It requires all of the following before any retained-proposal wording is
authorized:

- production physical-response evidence: strict direct correlator data or joint
  FH/LSZ same-source production evidence with homogeneous run-control, target
  ESS, finite-source derivative control, and collision-free provenance;
- scalar LSZ/model-class/FV/IR control: an isolated scalar-pole derivative or
  residue with model-class or analytic-continuation authority, plus
  finite-volume, IR, zero-mode, and threshold control;
- one source-overlap or physical-response bridge: `O_sp/O_H` Gram purity from
  production `C_sH/C_HH` rows, same-source W/Z response with sector-overlap
  identity and the lightweight W-response readout contract, same-surface
  Schur/K-prime rows plus canonical bridge, or a neutral-scalar
  rank-one/irreducibility theorem;
- matching/running bridge whose inputs are measured or certified, not selected
  from observed target values; this is now guarded by
  `scripts/frontier_yt_pr230_matching_running_bridge_gate.py`;
- retained-route and campaign certificates authorizing a proposal with no
  forbidden imports or open load-bearing assumptions.

## Current Result

The gate rejects the current PR #230 surface.  It also rejects a hypothetical
chunk-only completion: even perfect chunk data would still lack scalar LSZ
model-class/FV/IR control, a canonical-Higgs/source-overlap bridge, matching
authority, and retained-route authorization.

2026-05-05 chunk update: the separate polefit8x8 stream is now `36/63` chunks
ready with `576/1008` saved configurations.  This improves bounded production
support but does not change the assembly verdict: chunk-only completion still
fails the scalar-LSZ/model-class/FV/IR, source-overlap, matching, and retained
proposal gates.

2026-05-05 update: the gate also consumes
`outputs/yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json` and
`outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json`.
The current polefit8x8 `C_ss(q_hat^2)` proxy fails necessary Stieltjes
monotonicity, so the existing finite-shell proxy cannot satisfy the strict
scalar-LSZ moment-certificate requirement.  The contact-subtraction boundary
also blocks choosing a local subtraction from finite-row monotonicity
restoration alone; a same-surface contact-subtraction certificate or
microscopic scalar-denominator theorem is still required before a subtracted
object can satisfy the scalar-LSZ leg.

2026-05-05 affine-contact update: the gate also consumes
`outputs/yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json`.
The affine-contact repair route is now closed more sharply: choosing a slope
can fix first-order finite monotonicity, but second-and-higher
complete-monotonicity divided differences are invariant under affine
subtraction and fail robustly on the current rows.  The assembly gate remains
open with `PASS=39 FAIL=0`.

2026-05-05 polynomial-contact update: the gate also consumes
`outputs/yt_fh_lsz_polynomial_contact_finite_shell_no_go_2026-05-05.json`.
This closes the broader finite-shell contact interpolation shortcut.  If an
arbitrary degree-7 contact polynomial is admitted on the eight shell points,
two distinct positive one-pole Stieltjes residuals can reproduce the same
measured rows while assigning different pole locations and residues.  The
assembly gate remains open with `PASS=41 FAIL=0`.

2026-05-05 non-chunk route-family update: the gate now also consumes
`outputs/yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json` and
`outputs/yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json`.  The
route-family audit compares five live non-chunk families and selects the
scalar-LSZ polynomial-contact repair shortcut as the only currently executable
non-chunk block.  That block is closed negatively: degree `0..5` polynomial
contacts leave higher complete-monotonicity violations invariant, while
degree-seven finite interpolation can manufacture distinct Stieltjes-looking
residuals without identifying a physical contact.  The assembly gate remains
open with `PASS=42 FAIL=0`.

The matching/running bridge contract is executable, but the candidate bridge
certificate is absent, so this condition remains open on the current surface.

The current positive non-chunk bridge candidates remain:

- source-Higgs Gram purity, blocked by the missing same-surface `O_H`
  certificate and missing production `C_sH/C_HH` pole residues;
- same-source W/Z response, blocked by the missing same-source EW action,
  missing W/Z correlator mass-fit rows, missing lightweight W-response
  production row certificate, missing strict `delta_perp` tomography/null/purity
  correction certificate, missing matched top/W rows or a strict same-surface
  top/W factorization theorem, missing sector-overlap identity, and missing
  canonical-Higgs identity;
- Schur/K-prime kernel rows, blocked by absent same-surface Schur `A/B/C` rows
  and the separate canonical bridge;
- neutral-scalar rank one, blocked by the absence of a current
  primitive-cone/positivity-improving neutral-sector theorem.

## Non-Claims

This assembly gate does not claim retained or proposed_retained top-Yukawa
closure.  It does not package chunk outputs, synthesize measurement rows,
define `y_t` through a matrix element or `y_t_bare`, or use `H_unit`,
`yt_ward_identity`, `alpha_LM`, plaquette/u0, observed targets, `kappa_s=1`,
`c2=1`, `Z_match=1`, or `cos(theta)=1`.

## Next Action

Keep chunk production separate.  In parallel, pursue one real non-chunk bridge
that can satisfy the gate: a same-surface `O_H` certificate plus
`C_sH/C_HH` production rows, a same-source EW action plus W/Z mass-response
rows plus the lightweight readout certificate, strict `delta_perp` correction
authority, matched top/W rows or a strict top/W factorization theorem, and
sector-overlap identity, same-surface Schur `A/B/C` kernel rows, or a
neutral-sector irreducibility theorem.  Rerun the assembly gate before any
retained-route proposal.
