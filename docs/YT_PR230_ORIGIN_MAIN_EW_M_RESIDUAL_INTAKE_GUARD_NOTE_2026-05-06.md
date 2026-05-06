# PR230 Origin-Main EW M-Residual Intake Guard

**Status:** exact negative boundary / context-only intake.  This note does not
claim retained or proposed-retained top-Yukawa closure.

## Question

The current `origin/main` surface contains
`scripts/yt_ew_m_residual_channel_check.py`, a stretch-attempt packet for EW
matching-rule `M` using Fierz singlet/adjoint channel bookkeeping and CMT
mean-field language.  The PR230 question is whether that packet can be imported
as same-surface `O_H`, same-source W/Z response, or source-Higgs closure
authority.

## Result

It cannot.  The packet is useful context for the future W/Z route, but it
does not supply a PR230 closure artifact.  The runner
`scripts/frontier_yt_pr230_origin_main_ew_m_residual_intake_guard.py` records:

- the remote script explicitly says the `M` rule is not closed without an
  explicit framework EW Wilson-line construction;
- the checks are Fierz/channel bookkeeping plus CMT/u0 mean-field scaling,
  not a same-source EW action or response measurement;
- the packet emits no PR230 `O_H`, no `C_sH/C_HH` rows, no W/Z mass-fit
  response rows, no matched top/W covariance, no `delta_perp` authority, and
  no strict non-observed `g2` certificate;
- current action-first, W/Z, assembly, retained-route, and campaign gates
  still deny proposal wording.

## Claim Boundary

The packet may inform a future W/Z closure route only after a same-surface
framework EW Wilson-line action/current exists and production W/Z response rows
are present with matched covariance, `delta_perp`, and strict `g2` authority.
Its CMT/u0/Fierz content is not load-bearing PR230 `y_t` proof input under the
current firewall.

Forbidden shortcuts remain excluded:

- `H_unit` matrix-element readout;
- `yt_ward_identity` as authority;
- observed top mass or observed `y_t` selectors;
- `alpha_LM`, plaquette, or `u0` as Yukawa proof inputs;
- reduced cold pilots as production evidence;
- `c2 = 1`, `Z_match = 1`, or `kappa_s = 1` unless derived.

## Certificate

- Runner:
  [`scripts/frontier_yt_pr230_origin_main_ew_m_residual_intake_guard.py`](../scripts/frontier_yt_pr230_origin_main_ew_m_residual_intake_guard.py)
- Certificate:
  [`outputs/yt_pr230_origin_main_ew_m_residual_intake_guard_2026-05-06.json`](../outputs/yt_pr230_origin_main_ew_m_residual_intake_guard_2026-05-06.json)

The certificate records `PASS=18 FAIL=0`, `proposal_allowed=false`, and
`origin_main_ew_m_residual_closes_pr230=false`.

## Next Action

The clean physics route remains a genuine same-surface artifact, not a CMT
bookkeeping import: canonical `O_H/C_sH/C_HH` pole rows, a two-source transport
certificate, genuine W/Z response rows, Schur `A/B/C` rows, strict scalar-LSZ
moment/threshold/FV authority, or a neutral primitive-cone/irreducibility
certificate.
