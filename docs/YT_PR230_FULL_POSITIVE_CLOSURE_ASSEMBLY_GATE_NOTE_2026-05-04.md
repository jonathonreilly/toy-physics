# PR230 Full Positive Closure Assembly Gate Note

Status: open / assembly gate, not retained and not proposed_retained.

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
  identity, same-surface Schur/K-prime rows plus canonical bridge, or a
  neutral-scalar rank-one/irreducibility theorem;
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

The matching/running bridge contract is executable, but the candidate bridge
certificate is absent, so this condition remains open on the current surface.

The current positive non-chunk bridge candidates remain:

- source-Higgs Gram purity, blocked by the missing same-surface `O_H`
  certificate and missing production `C_sH/C_HH` pole residues;
- same-source W/Z response, blocked by the missing same-source EW action,
  missing W/Z correlator mass-fit rows, missing sector-overlap identity, and
  missing canonical-Higgs identity;
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
rows and sector-overlap identity, same-surface Schur `A/B/C` kernel rows, or a
neutral-sector irreducibility theorem.  Rerun the assembly gate before any
retained-route proposal.
