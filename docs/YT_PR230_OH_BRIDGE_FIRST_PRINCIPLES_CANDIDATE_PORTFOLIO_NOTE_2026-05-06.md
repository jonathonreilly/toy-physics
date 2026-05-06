# PR230 O_H Bridge First-Principles Candidate Portfolio

**Status:** open / first-principles `O_H` bridge positive-candidate portfolio

```yaml
actual_current_surface_status: open / first-principles O_H bridge positive-candidate portfolio
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_pr230_oh_bridge_first_principles_candidate_portfolio.py`
**Certificate:** `outputs/yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json`

## Purpose

This block takes stock after the taste-condensate shortcut was checked and
blocked.  It asks what first-principles attack surfaces still survive for the
missing PR230 bridge:

```text
O_sp / source response  ->  canonical O_H or equivalent physical response
                         ->  y_t readout
```

The result is a positive-candidate portfolio, not closure.  It does not supply
canonical `O_H`, `C_sH/C_HH` pole rows, W/Z rows, Schur `A/B/C` rows, or a
neutral primitive-cone theorem.

## Probe Synthesis

Six read-only probes and a local synthesis pass converged on the same boundary:

- the uniform PR230 additive mass source is a taste singlet, while the current
  taste-axis Higgs operators are trace-zero taste-shift axes;
- no Cl/taste automorphism can map the identity source to a trace-zero taste
  axis because trace and spectrum are invariant;
- the adjacent kinetic-mixing shortcut is also closed on the current surface:
  taste-even Wilson-staggered dynamics gives zero `C_sH` against one
  trace-zero taste-axis insertion unless a real symmetry-breaking Higgs/taste
  source or measured source-Higgs row is supplied;
- the one-Higgs/taste-axis completeness shortcut is closed on the current
  surface: SM one-Higgs notation plus the taste scalar theorem does not select
  an electroweak Higgs taste axis or null all orthogonal top couplings;
- source-only LSZ data and `C_ss` do not determine `C_sH/C_HH`;
- W/Z response can cancel the unknown source normalization, but only with real
  same-source W/Z mass-response rows, matched covariance, `delta_perp`
  authority, and strict non-observed `g2`;
- Schur/Feshbach machinery is useful after a neutral kernel basis exists, but
  compressed source denominators do not reconstruct `A/B/C` rows;
- Perron/Krein-Rutman rank-one closure is a real theorem route only after a
  same-surface neutral primitive transfer operator or off-diagonal generator is
  certified.

The current negative results are therefore shortcut blockers, not global
route closures.

Machine-readable boundary fields in the certificate record:

```yaml
blocks_only: [shortcut, current_surface]
blocks_first_principles_derivation: false
same_surface_required: true
```

This keeps current-surface exhaustion and no-go notes from being read as a ban
on first-principles derivation after a named row, certificate, or theorem is
supplied.

## Ranked Candidates

1. **Source-coordinate transport.**  Derive a same-surface source-coordinate
   transport theorem from the PR230 uniform mass source to a canonical
   Higgs/taste source, including LSZ normalization and a forbidden-import
   firewall.  The current-surface shortcut is now closed by
   `YT_PR230_SOURCE_COORDINATE_TRANSPORT_COMPLETION_ATTEMPT`: `I_8` cannot be
   transported to trace-zero `S_i` by unit-preserving, trace-preserving, or
   taste-equivariant maps without a new source-axis/Jacobian certificate.  The
   dynamic kinetic-mixing variant is also closed by
   `YT_PR230_KINETIC_TASTE_MIXING_BRIDGE_ATTEMPT`: taste-even transfer
   polynomials force the current-surface cross row to vanish.

2. **Action-first canonical `O_H` rows.**  Derive a same-source EW/Higgs action
   on the PR230 `Cl(3)/Z^3` source surface, certify canonical `O_H`, then run
   production `C_ss/C_sH/C_HH` rows and Gram purity.  The current-surface route
   is now explicitly closed by `YT_PR230_ACTION_FIRST_ROUTE_COMPLETION`: the
   same-source EW/Higgs action, canonical `O_H`, production rows, and
   Gram-purity certificate are all absent.  The notation-only one-Higgs escape
   is also closed by `YT_PR230_ONE_HIGGS_TASTE_AXIS_COMPLETENESS_ATTEMPT`.

3. **W/Z same-source response.**  Bypass direct `O_H` by measuring matched
   top/W/Z source-response slopes.  This requires W/Z mass-fit rows, matched
   top/W covariance, `delta_perp` control, and strict non-observed `g2`.  The
   current-surface route is now closed by `YT_PR230_WZ_RESPONSE_ROUTE_COMPLETION`:
   those rows/certificates are all absent.

4. **Schur `A/B/C` neutral-kernel rows.**  Define the same-surface neutral
   scalar kernel basis and source/orthogonal projector, then emit Schur block
   rows and pole derivatives or direct two-source residue rows.  The
   current-surface route is now closed by `YT_PR230_SCHUR_ROUTE_COMPLETION`:
   sufficiency and row-definition machinery exist, but the neutral kernel
   basis, projectors, A/B/C rows, and equivalent row theorem are absent.

5. **Neutral primitive/rank-one theorem.**  Certify a same-surface neutral
   transfer operator that is nonnegative, strongly connected, and primitive,
   with an isolated lowest neutral pole and positive source/canonical-Higgs
   overlaps.  The current-surface route is now closed by
   `YT_PR230_NEUTRAL_PRIMITIVE_ROUTE_COMPLETION`: conditional Perron support
   and positivity inputs are not yet a primitive transfer, off-diagonal
   generator, or irreducibility certificate.

## Non-Claims

This note does not claim retained or proposed-retained `y_t` closure.  It does
not define `y_t` through `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, `u0`, `kappa_s=1`, `cos(theta)=1`, `c2=1`, or
`Z_match=1`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_oh_bridge_first_principles_candidate_portfolio.py
# SUMMARY: PASS=23 FAIL=0
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=51 FAIL=0
python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=111 FAIL=0
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=257 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=287 FAIL=0
```

Strict audit lint reports only the existing warning baseline after the audit
pipeline is regenerated.
