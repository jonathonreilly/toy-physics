# Route Portfolio

## R1: Fixed-lattice scale symmetry

Try to derive a scale current from `Z^3` automorphisms and the current lattice
Noether theorem.

Status: closed negatively in
`docs/YT_SCALE_STATIONARITY_SUBSTRATE_NO_GO_NOTE_2026-05-01.md`.

Reason: `Z^3` has translations and discrete `GL(3,Z)` automorphisms, but no
nontrivial continuous dilation symmetry.  The Noether theorem supplies
translation and `U(1)` currents, not a scale current.

## R2: Boundary value implies tangent

Try to prove `lambda(M_Pl)=0 => beta_lambda(M_Pl)=0`.

Status: closed negatively in
`docs/YT_BETA_LAMBDA_PLANCK_STATIONARITY_NO_GO_NOTE_2026-05-01.md`.

Reason: the one-loop beta polynomial at `lambda=0` is nonzero and
Yukawa-dependent.

## R3: Finite source response implies RG tangent

Try to derive `d lambda / d log(mu)` from finite `W[J]=log|det(D+J)|`.

Status: blocked.

Reason: finite source derivatives do not define a continuum RG scale tangent
without the external EFT/RG bridge.

## R4: Trace-anomaly route

Try to derive a quantum EMT trace condition whose Planck boundary forces
`beta_lambda(M_Pl)=0`.

Status: closed negatively in
`docs/YT_TRACE_ANOMALY_STATIONARITY_NO_GO_NOTE_2026-05-01.md`.

Reason: current Noether authority does not close full EMT or quantum anomaly,
existing anomaly-trace catalogues are gauge/hypercharge arithmetic, scalar
trace data are underdetermined, and the repo has no operator-independence
theorem forcing `beta_lambda=0`.

## R5: Multiple-point / Planck stationarity selector

Adopt `beta_lambda(M_Pl)=0` as an explicit new selector.

Status: conditional support only.  The weaker one-sided vacuum-stability route
is closed negatively in
`docs/YT_VACUUM_STABILITY_STATIONARITY_NO_GO_NOTE_2026-05-01.md`.

Usefulness: gives a fast non-MC `y_t(v)` readout, but does not satisfy the
user's full retained-closure target.

Reason the weaker route fails: `lambda(M_Pl)=0` plus local stability below the
upper boundary gives `beta_lambda(M_Pl)<=0`, not equality.  Equality is the
extra tangency/double-zero premise.

## R6: Direct MC

Run production top correlator.

Status: engineering route, not instant closure.

Reason: strict production data and independent top-mass parameter pin are both
still needed for derivational status.
