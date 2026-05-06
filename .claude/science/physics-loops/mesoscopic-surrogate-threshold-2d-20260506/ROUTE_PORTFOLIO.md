# Route Portfolio

## Route 1: Register Existing Runner And Cache Output

Status: executed.

The repo already had `scripts/mesoscopic_surrogate_threshold_2d.py` and the
legacy frozen log, but the note did not cite the runner and the audit ledger
had `runner_path: null`. This route adds the primary runner link, makes the
runner assertion-gated, refreshes the SHA-pinned cache, and regenerates audit
metadata.

Expected claim-state movement: from missing artifact to audit-ready bounded
finite computation.

## Route 2: Add A New Theorem

Status: rejected for this task.

The auditor did not ask for a persistent-mass theorem. Adding one would be a
different hard physics problem outside the 15-minute closure gate.

## Route 3: Cite Companion Notes As Authorities

Status: not used.

The companion notes are not needed for the finite support-sweep packet and
would add dependency burden. The source note instead points directly to the
runner and cache that compute the bounded result.
