# Archive: h0125 failure derivation — unverifiable numerical diagnostics

**Archived:** 2026-04-30 (README added 2026-05-01)
**Audit verdict:** audited_failed (terminal; ACCEPT)

## Why this is here

`H0125_FAILURE_DERIVATION.md` was a proposed_retained negative claim
("h=0.125 failed, diagnosed by boundary leakage + beam spreading +
compounded probability loss + SNR=0.5"). The audit found it does not
close on its own terms:

- The note has **no runner** and **no cited authority** for the transfer
  norms, beam widths, detector probabilities, or SNR figures it tabulates.
- The explicit formula `P_det = (retention)^nl` printed in the note is
  inconsistent with the printed P_det column by tens to **more than one
  hundred orders of magnitude** (e.g. retention^nl ≈ 8.18e-4 vs printed
  3.7e-59 for one row).

The diagnosis is therefore not auditable as written. The repair target
(per the audit) is to write an executable h=0.125 failure diagnostic that
computes T_interior/T_corner, beam sigma, detector probability with any
geometric-spreading factor, and centroid SNR from the same propagation
model — and then update the note so every table entry follows from that
runner.

That repair has not been done. Until it is done, the safe scope is:
"boundary leakage and beam spreading are plausible failure hypotheses for
h=0.125; the quantified root-cause diagnosis and the SNR=0.5 noise
explanation are NOT retained."

## Status

Archived as a terminal-failed historical record. The audit row
`h0125_failure_derivation` will remain `audited_failed` until and unless
the repair runner is written and the note is rewritten against it.
