# YT FH/LSZ Chunk-Wave Orchestrator Note

Date: 2026-05-04

PR: #230

Status: bounded production-engineering support only; closure proposal is not
authorized.

## Scope

This note records the PR230 chunk-wave orchestrator added for the L12_T24
FH/LSZ production campaign:

- runner: `scripts/frontier_yt_fh_lsz_chunk_wave_orchestrator.py`
- status certificate:
  `outputs/yt_fh_lsz_chunk_wave_orchestrator_status_2026-05-04.json`
- active launch range in this checkpoint: chunks035-040
- concurrency cap: six production jobs across all detected L12 chunks

The orchestrator is run-control infrastructure. It detects already-running
chunk production jobs by their output paths, detects completed production JSON
outputs, launches missing chunks only when the global active-job count is below
the cap, and can rerun the existing per-chunk and aggregate gates when outputs
land.

## Current Campaign State

At launch, chunks029-034 were already running under their existing monitors.
The orchestrator dry run and first live poll both detected:

- completed chunks in range 035-040: none
- all running chunks: 029, 030, 031, 032, 033, 034
- missing chunks in range 035-040: 035, 036, 037, 038, 039, 040

Because the six-job cap was already saturated, the orchestrator launched no new
chunks on the first poll. It is expected to launch chunks035-040 only as slots
open.

## Claim Boundary

The orchestrator does not create physics evidence by itself. It does not alter
the top-correlator, scalar-source, scalar two-point, source-Higgs, W/Z,
Schur/K-prime, retained-route, or campaign-status gates. It does not treat
partial chunks as complete volume evidence.

Forbidden authorities remain unused: `H_unit`, `yt_ward_identity`, observed top
mass, observed `y_t`, observed W/Z masses, `alpha_LM`, plaquette/u0, reduced
pilots, `kappa_s = 1`, `c2 = 1`, `Z_match = 1`, and undeclared unit
normalizations.

Exact next action: let chunks029-034 finish under the existing monitors. As
slots open, the orchestrator will launch chunks035-040 and record status in
its certificate. Retained closure remains blocked on a same-surface
canonical-Higgs/source-overlap certificate, W/Z response identity, scalar-pole
identity theorem, or complete production evidence passing the existing gates.
